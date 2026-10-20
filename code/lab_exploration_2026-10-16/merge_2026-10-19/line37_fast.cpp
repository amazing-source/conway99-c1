// line37_fast: same semantics as line37.cpp (LAB 20/10/2026), rewritten for speed (LAB 20/10/2026, evening).
// Same input, same usage, same output format, same verdict, same x, same candidate list (same order, bit-identical dd)
// and the same search tree (same branching rule, same value order, hence the same node counts).  What changed:
//   * no heap allocation per node: the domain of each far vertex at each depth is a preallocated list (global id,
//     qi, si), in the order of line37's vectors; a child's lists are compressed from the parent's (AVX-512 VBMI2);
//   * the cheap pair filters of the forward check (q/s distinct, |W n W'| <= 2, R in {0, 1}, the R = 1 conditions,
//     saturated margins, the partners' R = 1) are evaluated 64 candidates at a time: for an assigned triple A, R(A, b)
//     depends on b only through (y_b, qi_b, si_b), so per-A byte tables TQ[qi], TS[si], cst[var] give R and the
//     share flags by table lookup (AVX-512 VBMI vpermb); the tables are built once per line, on first assignment;
//   * the real filter (psd_ok) is evaluated only on the survivors of the cheap filters, after them (as before) and
//     incrementally: the forward substitution y = L^-1 h_b of a candidate b is extended by one entry per depth instead
//     of being recomputed from scratch; every floating-point operation is the same, in the same order (same FMA
//     contractions), so every psd decision is the same bit for bit;
//   * a node is declared dead as soon as one domain is empty: the cheap filters of the far vertices first, then the
//     real filter far vertex by far vertex, smallest first (line37 interleaved them; "dead" holds iff some domain is
//     empty, and the domains of a live child are the same sets);
//   * the candidate preparation tests L2 for all si of a (y, qi) at once (each failing condition forbids the s-pairs
//     through one vertex, see prep_star) and g(W, W) mod 7 by an exact additive decomposition; dd is computed with the
//     very same 36 additions as before.
// Floating point: build with exactly the flags of line37.exe (g++ -O3 -march=native -std=c++17, GCC 16.1): the FP
// statements copied from line37.cpp (inv_real, dd, zq, hval, psd/chol, jacobi) keep their form, so GCC contracts them
// the same way (checked in the disassembly: vfnmadd231sd for t -= L*y, vfmadd231sd for s += y*y, as in line37.exe).
// Without AVX-512 VBMI/VBMI2 (or with -DL37_SCALAR) a scalar path with the same logic is compiled.
// usage: line37_fast file <lines.txt> [limit_s]     one G_T per line: s01[12] s12[12] s20[12]; one JSON line per G_T
//        line37_fast rand <count> <seed> [limit_s]  uniform random bijection triples; summary JSON (timing per stage)
//        line37_fast randv <count> <seed> [limit_s] validation: one JSON line per sample, with a hash of the candidates
//        line37_fast filev <lines.txt> [limit_s]    validation: file mode plus the candidate hash
// (any extra argument is ignored, e.g. a tag for the watchdog)
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <chrono>
#include <cmath>
#include <algorithm>
#include <random>
#include <string>
#ifdef _WIN32
#include <windows.h>
#endif
#if !defined(L37_SCALAR) && defined(__AVX512F__) && defined(__AVX512BW__) && defined(__AVX512VBMI__) && defined(__AVX512VBMI2__)
#include <immintrin.h>
#define L37_SIMD 1
#else
#define L37_SIMD 0
#endif
using namespace std;

static const int NN = 36, n12 = 12, MAXV = 16, LEV = 10;
static const double RTOL = 1e-9;
static const bool REAL = true, RANK = true;   // line37 never reads STAR_NOREAL / STAR_NORANK

static inline int pc64(uint64_t a) { return __builtin_popcountll(a); }
static inline int ctz64(uint64_t a) { return __builtin_ctzll(a); }

// ---------------- the line graph (verbatim from line37.cpp) ----------------
static int Gm[36][36], Km[36][36], Om[36][36];
static double Zr[36][36];
static int nbr[36][3];
static uint64_t nbm[36];
static const int INV7[7] = {0, 1, 4, 5, 2, 3, 6};

static void build_g(const int* s01, const int* s12, const int* s20) {
    memset(Gm, 0, sizeof Gm);
    for (int c = 0; c < 3; c++) for (int i = 0; i < n12; i++) Gm[c * n12 + i][c * n12 + (i ^ 1)] = 1;
    for (int i = 0; i < n12; i++) {
        int a = i, b = n12 + s01[i]; Gm[a][b] = Gm[b][a] = 1;
        a = n12 + i; b = 2 * n12 + s12[i]; Gm[a][b] = Gm[b][a] = 1;
        a = 2 * n12 + i; b = s20[i]; Gm[a][b] = Gm[b][a] = 1;
    }
    for (int v = 0; v < NN; v++) { int k = 0; for (int z = 0; z < NN; z++) if (Gm[v][z]) nbr[v][k++] = z; }
    for (int v = 0; v < NN; v++) { nbm[v] = 0; for (int k = 0; k < 3; k++) nbm[v] |= 1ULL << nbr[v][k]; }
}

static bool admissible() {             // K = 12I - G - G^2 + 2J - J_cl >= 0
    for (int a = 0; a < NN; a++) for (int b = 0; b < NN; b++) {
        int g2 = 0; for (int k = 0; k < 3; k++) g2 += Gm[nbr[a][k]][b];
        int v = (a == b ? 12 : 0) - Gm[a][b] - g2 + 2 - (a / n12 == b / n12 ? 1 : 0);
        Km[a][b] = v;
        if (v < 0) return false;
    }
    return true;
}

static int ncomp() {
    int comp[36]; for (int i = 0; i < NN; i++) comp[i] = -1;
    int c = 0, st[36];
    for (int x = 0; x < NN; x++) {
        if (comp[x] >= 0) continue;
        int sp = 0; st[sp++] = x; comp[x] = c;
        while (sp) { int y = st[--sp]; for (int k = 0; k < 3; k++) { int z = nbr[y][k]; if (comp[z] < 0) { comp[z] = c; st[sp++] = z; } } }
        c++;
    }
    return c;
}

static bool inv_mod7(int& detv) {      // Omega = (3I - G + J)^-1 mod 7 and det(3I - G + J) mod 7 (= tau mod 7)
    static int A[36][72];
    for (int i = 0; i < NN; i++) for (int j = 0; j < NN; j++) {
        A[i][j] = (((i == j ? 3 : 0) - Gm[i][j] + 1) % 7 + 7) % 7; A[i][NN + j] = (i == j);
    }
    int det = 1;
    for (int c = 0; c < NN; c++) {
        int r = -1; for (int k = c; k < NN; k++) if (A[k][c]) { r = k; break; }
        if (r < 0) { detv = 0; return false; }
        if (r != c) { for (int j = 0; j < 2 * NN; j++) swap(A[r][j], A[c][j]); det = (7 - det) % 7; }
        det = det * A[c][c] % 7;
        int iv = INV7[A[c][c]];
        for (int j = 0; j < 2 * NN; j++) A[c][j] = A[c][j] * iv % 7;
        for (int k = 0; k < NN; k++) if (k != c && A[k][c]) {
            int f = A[k][c];
            for (int j = 0; j < 2 * NN; j++) A[k][j] = ((A[k][j] - f * A[c][j]) % 7 + 7) % 7;
        }
    }
    for (int i = 0; i < NN; i++) for (int j = 0; j < NN; j++) Om[i][j] = A[i][NN + j];
    detv = det;
    return true;
}

static void inv_real() {               // Z = (3I - G + J)^-1 over the reals (connected: invertible)
    static double A[36][72];
    for (int i = 0; i < NN; i++) for (int j = 0; j < NN; j++) {
        A[i][j] = (i == j ? 3.0 : 0.0) - Gm[i][j] + 1.0; A[i][NN + j] = (i == j);
    }
    for (int c = 0; c < NN; c++) {
        int r = c; for (int k = c + 1; k < NN; k++) if (fabs(A[k][c]) > fabs(A[r][c])) r = k;
        if (r != c) for (int j = 0; j < 2 * NN; j++) swap(A[r][j], A[c][j]);
        double iv = 1.0 / A[c][c];
        for (int j = 0; j < 2 * NN; j++) A[c][j] *= iv;
        for (int k = 0; k < NN; k++) if (k != c && A[k][c] != 0.0) {
            double f = A[k][c];
            for (int j = 0; j < 2 * NN; j++) A[k][j] -= f * A[c][j];
        }
    }
    for (int i = 0; i < NN; i++) for (int j = 0; j < NN; j++) Zr[i][j] = A[i][NN + j];
}

// ---------------- static tables (pairs) ----------------
// P1 = q-pairs (class 1), P2 = s-pairs (class 2), in the order of line37's prep_star: i < j, i/2 != j/2, i outer.
static int P1a[64], P1b[64], P2a[64], P2b[64], NP = 0;
static uint64_t qmaskP[64], smaskP[64];
static uint64_t SCm[36];                                // SCm[n] = set of si whose s-pair contains n (n in class 2)
alignas(64) static uint8_t QCB[36][64], SCB[36][64];   // QCB[n][qi] = 1 iff n in q-pair qi (n in class 1); SCB for s
static uint8_t MOD7[256];
alignas(64) static uint8_t RCLS[64];                    // sum -> 1 if R = 0, 2 if R = 1, 0 otherwise
static int RFULL[64];                                   // sum -> R = (4 - sum) mod 7

static void init_static() {
    NP = 0;
    for (int i = 0; i < n12; i++) for (int j = i + 1; j < n12; j++) if (i / 2 != j / 2) {
        P1a[NP] = n12 + i; P1b[NP] = n12 + j; P2a[NP] = 2 * n12 + i; P2b[NP] = 2 * n12 + j; NP++;
    }
    for (int k = NP; k < 64; k++) { P1a[k] = P1b[k] = n12; P2a[k] = P2b[k] = 2 * n12; }   // never used (padding)
    memset(QCB, 0, sizeof QCB); memset(SCB, 0, sizeof SCB); memset(SCm, 0, sizeof SCm);
    for (int k = 0; k < NP; k++) {
        qmaskP[k] = (1ULL << P1a[k]) | (1ULL << P1b[k]); smaskP[k] = (1ULL << P2a[k]) | (1ULL << P2b[k]);
        QCB[P1a[k]][k] = QCB[P1b[k]][k] = 1; SCB[P2a[k]][k] = SCB[P2b[k]][k] = 1;
        SCm[P2a[k]] |= 1ULL << k; SCm[P2b[k]] |= 1ULL << k;
    }
    for (int v = 0; v < 256; v++) MOD7[v] = (uint8_t)(v % 7);
    for (int s = 0; s < 64; s++) {
        int R = ((4 - s) % 7 + 7) % 7;
        RFULL[s] = R; RCLS[s] = (uint8_t)(R == 0 ? 1 : (R == 1 ? 2 : 0));
    }
}

// ---------------- the star of x: candidates ----------------
static int X, B1, B2, NV;
static int Kx[36];
static int Yv[MAXV], ncv[MAXV], wbase[MAXV];
static int totG = 0;
// per candidate (global id g = wbase[var] + index in var; at most 10 * 3600 ids, so they fit in uint16)
static vector<uint8_t> cqi, csi, ccap, cvar;
static vector<uint32_t> cnm;           // packed names q0 | q1 << 8 | s0 << 16 | s1 << 24
static vector<double> cdd;
static vector<uint64_t> cmask;

static void ensure_cap(int need) {
    if ((int)cqi.size() >= need) return;
    int n = max(need, (int)cqi.size() * 2);
    cqi.resize(n); csi.resize(n); ccap.resize(n); cvar.resize(n); cdd.resize(n); cmask.resize(n); cnm.resize(n);
}

static unsigned long long CHASH = 0;
#ifdef L37_CHECK_PREP
static long long prep_checked = 0;
#endif
static inline void hmix(unsigned long long v) { CHASH ^= v; CHASH *= 1099511628211ULL; }

// the 10 domains of the star of x (rank 37: u = 0, g(W, W) = 0); returns false if x is in a transversal triangle.
// Same tests as line37's prep_star (K(x, .) >= 1, L2, g(W, W) = 0 mod 7, 0 <= dd <= 7 with the same tolerances),
// evaluated in another order (all are necessary conditions on the same triple; none has a side effect).
static bool prep_star(int x, long long& ncand) {
    int xb = x ^ 1, b1 = -1, b2 = -1;
    for (int k = 0; k < 3; k++) { int z = nbr[x][k]; if (z >= n12 && z < 2 * n12) b1 = z; if (z >= 2 * n12) b2 = z; }
    if (Gm[b1][b2]) return false;
    X = x; B1 = b1; B2 = b2;
    for (int z = 0; z < NN; z++) Kx[z] = Km[x][z];
    bool qv[64], sv[64];
    uint64_t svmask = 0;
    for (int k = 0; k < NP; k++) {
        qv[k] = !(Km[x][P1a[k]] == 0 || Km[x][P1b[k]] == 0);
        sv[k] = !(Km[x][P2a[k]] == 0 || Km[x][P2b[k]] == 0);
        if (sv[k]) svmask |= 1ULL << k;
    }
    int n2v[36];                       // the class-2 neighbour of every vertex of classes 0 and 1
    for (int v = 0; v < 2 * n12; v++) { n2v[v] = -1; for (int k = 0; k < 3; k++) if (nbr[v][k] >= 2 * n12) n2v[v] = nbr[v][k]; }
    // g(W, W) = sum over the 36 ordered pairs of W x W of Omega, split by blocks {x, y}, Q, S (exact integers)
    static int Gq[64], Gs[64], XQ[36][64], XS[36][64];
    for (int k = 0; k < NP; k++) {
        int a = P1a[k], b = P1b[k];
        Gq[k] = Om[a][a] + Om[a][b] + Om[b][a] + Om[b][b];
        a = P2a[k]; b = P2b[k];
        Gs[k] = Om[a][a] + Om[a][b] + Om[b][a] + Om[b][b];
        for (int u = 0; u < n12; u++) XQ[u][k] = Om[u][P1a[k]] + Om[P1a[k]][u] + Om[u][P1b[k]] + Om[P1b[k]][u];
        for (int u = 0; u < 2 * n12; u++) XS[u][k] = Om[u][P2a[k]] + Om[P2a[k]][u] + Om[u][P2b[k]] + Om[P2b[k]][u];
    }
    NV = 0; ncand = 0; int gtot = 0;
    CHASH = 1469598103934665603ULL;
    for (int y = 0; y < n12; y++) {
        if (y == x || y == xb) continue;
        int w = NV++; Yv[w] = y; wbase[w] = gtot;
        int cnt = 0;
        ensure_cap(gtot + 3600 + 64);
        int gxy = Om[x][x] + Om[x][y] + Om[y][x] + Om[y][y];
        uint64_t mxy = (1ULL << x) | (1ULL << y);
        for (int qi = 0; qi < NP; qi++) {
            if (!qv[qi]) continue;
            int q0 = P1a[qi], q1 = P1b[qi];
            uint64_t mq = mxy | qmaskP[qi];
            int gq = gxy + Gq[qi] + XQ[x][qi] + XQ[y][qi];
            // L2 (every vertex of W has <= 1 neighbour in W, every vertex outside W has <= 2), for all si at once.
            // A vertex outside W with 3 neighbours in W has its mate in W, so the outside vertices to test are the
            // 6 mates of W (all outside W).  With W = {x, y} u Q u S, Q = {q0, q1}, S = {s0, s1}:
            //  v in {x, y, q0, q1}: |N(v) n W| = a_v + [n2(v) in S], a_v = |N(v) n ({x, y} u Q)|  (n2 = class-2 nbr)
            //  its mate m:          |N(m) n W| = a_m + [n2(m) in S]
            //  s in S:              |N(s) n W| = c(s) = [n0(s) in {x, y}] + [n1(s) in Q]
            //  the mate t of s:     |N(t) n W| = 1 + c(t)
            // and c(s) = 2 iff s in {n2(x), n2(y)} n {n2(q0), n2(q1)}.  Each failing condition forbids the s-pairs
            // containing one given vertex (SCm), or every si.
            uint64_t forb = 0; bool allbad = false;
            {
                const int V4[4] = {x, y, q0, q1};
                for (int k = 0; k < 4; k++) {
                    int v = V4[k], m = v ^ 1;
                    int av = pc64(nbm[v] & mq), am = pc64(nbm[m] & mq);
                    if (av >= 2 || am >= 3) allbad = true;
                    if (av == 1) forb |= SCm[n2v[v]];
                    if (am == 2) forb |= SCm[n2v[m]];
                }
                const int sx = n2v[x], sy = n2v[y], sq0 = n2v[q0], sq1 = n2v[q1];
                if (sx == sq0 || sx == sq1) forb |= SCm[sx] | SCm[sx ^ 1];
                if (sy == sq0 || sy == sq1) forb |= SCm[sy] | SCm[sy ^ 1];
            }
#ifdef L37_CHECK_PREP
            for (int si = 0; si < NP; si++) {      // debug: the direct test on every triple
                if (!sv[si]) continue;
                int s0 = P2a[si], s1 = P2b[si];
                uint64_t mask = mq | smaskP[si];
                bool ok = !(pc64(nbm[x] & mask) > 1 || pc64(nbm[y] & mask) > 1 || pc64(nbm[q0] & mask) > 1 ||
                            pc64(nbm[q1] & mask) > 1 || pc64(nbm[s0] & mask) > 1 || pc64(nbm[s1] & mask) > 1);
                ok = ok && !(pc64(nbm[x ^ 1] & mask) > 2 || pc64(nbm[y ^ 1] & mask) > 2 || pc64(nbm[q0 ^ 1] & mask) > 2 ||
                             pc64(nbm[q1 ^ 1] & mask) > 2 || pc64(nbm[s0 ^ 1] & mask) > 2 || pc64(nbm[s1 ^ 1] & mask) > 2);
                // the line37 test itself (cnt over all outside vertices)
                bool ok2 = true;
                { int W[6] = {x, y, q0, q1, s0, s1};
                  for (int k = 0; k < 6 && ok2; k++) { int c = 0; for (int j = 0; j < 3; j++) c += (mask >> nbr[W[k]][j]) & 1; if (c > 1) ok2 = false; }
                  int cntz[36] = {0};
                  for (int k = 0; k < 6 && ok2; k++) for (int j = 0; j < 3; j++) { int z = nbr[W[k]][j]; if (!((mask >> z) & 1) && ++cntz[z] > 2) ok2 = false; } }
                bool ok3 = !allbad && !((forb >> si) & 1);
                if (ok != ok3 || ok != ok2) { fprintf(stderr, "PREP CHECK FAILED y=%d qi=%d si=%d direct=%d line37=%d decomposed=%d\n", y, qi, si, ok, ok2, ok3); exit(3); }
                prep_checked++;
            }
#endif
            if (allbad) continue;
            uint64_t allowed = svmask & ~forb;
            while (allowed) {
                int si = ctz64(allowed); allowed &= allowed - 1;
                int s0 = P2a[si], s1 = P2b[si];
                uint64_t mask = mq | smaskP[si];
                int g = gq + Gs[si] + XS[x][si] + XS[y][si] + XS[q0][si] + XS[q1][si];
                if (g % 7) continue;
                int W[6] = {x, y, q0, q1, s0, s1};
                double ez = 0; for (int a = 0; a < 6; a++) for (int b = 0; b < 6; b++) ez += Zr[W[a]][W[b]];
                double dd = 3.0 + 1.0 / 9.0 - ez;
                if (dd < -1e-9 || dd > 7 + 1e-9) continue;
                int gid = gtot + cnt;
                cqi[gid] = (uint8_t)qi; csi[gid] = (uint8_t)si; cvar[gid] = (uint8_t)w; cdd[gid] = dd; cmask[gid] = mask;
                cnm[gid] = (uint32_t)q0 | ((uint32_t)q1 << 8) | ((uint32_t)s0 << 16) | ((uint32_t)s1 << 24);
                ccap[gid] = (uint8_t)(1 - pc64(nbm[x] & mask));
                unsigned long long db; memcpy(&db, &dd, 8);
                hmix((unsigned long long)w); hmix((unsigned long long)qi); hmix((unsigned long long)si); hmix(db);
                cnt++;
            }
        }
        ncv[w] = cnt;
        gtot += cnt;
        ncand += cnt;
    }
    totG = gtot;
    return true;
}

// ---------------- per assigned triple A: lookup tables (built once per line, on first assignment) ----------------
// For an assigned triple A and a candidate b of far vertex w: Rval(A, b) = (4 - sum_{z in W_b} Y_A[z]) mod 7 with
// Y_A[z] = sum_{u in W_A} Omega[z][u] (line37's orientation).  W_b = {x, y_w} u Q(qi_b) u S(si_b), hence
//   sum = cst[w] + rq[qi_b] + rs[si_b] (mod 7),   TQ[qi] = rq[qi] | 8 [q0_A in Q] | 16 [q1_A in Q] | 32 R1okQ,
// R1okQ = (b1 not in Q) and nbc_A(q) <= 1 for both q in Q (the q-part of cap_b = 1 and of the NF test for b's names);
// TS likewise with b2.  hval(A, b) = -R + 1/9 - (((((0 + zq[x]) + zq[y_w]) + zq[q0]) + zq[q1]) + zq[s0]) + zq[s1].
struct alignas(64) ATab {
    uint8_t TQ[64], TS[64];
    uint8_t cst[16], nfY[16];
    double base2[16];          // (0 + zq[x]) + zq[y_w], the first two additions of hval
    double zq[40];             // zq[z] = (((((0 + Zr[z][x]) + Zr[z][y]) + Zr[z][q0]) + Zr[z][q1]) + Zr[z][s0]) + Zr[z][s1]
};
static vector<ATab> AT;
static vector<uint32_t> ATst; static uint32_t STAMP = 0;
// per line: OQ[u][qi] = (Omega[q0][u] + Omega[q1][u]) mod 7, OS likewise, OXY[u][w] = (Omega[x][u] + Omega[y_w][u]) mod 7
alignas(64) static uint8_t OQ[36][64], OS[36][64], OXY[36][16];
alignas(64) static double ZrT[36][40];
alignas(64) static uint8_t QCB8[36][64], QCB16[36][64], SCB8[36][64], SCB16[36][64], MOD7V[64];

static void init_static_tables() {
    for (int n = 0; n < 36; n++) for (int k = 0; k < 64; k++) {
        QCB8[n][k] = (uint8_t)(QCB[n][k] << 3); QCB16[n][k] = (uint8_t)(QCB[n][k] << 4);
        SCB8[n][k] = (uint8_t)(SCB[n][k] << 3); SCB16[n][k] = (uint8_t)(SCB[n][k] << 4);
    }
    for (int k = 0; k < 64; k++) MOD7V[k] = (uint8_t)(k % 7);
}

static void prep_tables() {           // per line, after prep_star
    for (int u = 0; u < NN; u++) {
        for (int k = 0; k < 64; k++) {
            if (k < NP) {
                OQ[u][k] = (uint8_t)((Om[P1a[k]][u] + Om[P1b[k]][u]) % 7);
                OS[u][k] = (uint8_t)((Om[P2a[k]][u] + Om[P2b[k]][u]) % 7);
            } else { OQ[u][k] = 0; OS[u][k] = 0; }
        }
        for (int w = 0; w < 16; w++) OXY[u][w] = (uint8_t)(w < NV ? (Om[X][u] + Om[Yv[w]][u]) % 7 : 0);
        for (int z = 0; z < 40; z++) ZrT[u][z] = z < NN ? Zr[z][u] : 0.0;
    }
    if ((int)AT.size() < totG) { AT.resize(totG); ATst.resize(totG, 0); }
    STAMP++;
    if (STAMP == 0) { fill(ATst.begin(), ATst.end(), 0u); STAMP = 1; }
}

static void build_atab(int g) {
    ATab& T = AT[g];
    int w = cvar[g], qi = cqi[g], si = csi[g];
    const int W[6] = {X, Yv[w], P1a[qi], P1b[qi], P2a[si], P2b[si]};
    // c2 = the vertices z with nbc_A(z) = |N(z) n W_A| >= 2
    uint64_t c1 = 0, c2 = 0;
    for (int k = 0; k < 6; k++) { uint64_t nb = nbm[W[k]]; c2 |= c1 & nb; c1 |= nb; }
#if L37_SIMD
    {
        __m512i aq = _mm512_add_epi8(_mm512_add_epi8(_mm512_add_epi8(_mm512_loadu_si512(OQ[W[0]]), _mm512_loadu_si512(OQ[W[1]])),
                                                     _mm512_add_epi8(_mm512_loadu_si512(OQ[W[2]]), _mm512_loadu_si512(OQ[W[3]]))),
                                     _mm512_add_epi8(_mm512_loadu_si512(OQ[W[4]]), _mm512_loadu_si512(OQ[W[5]])));
        __m512i as = _mm512_add_epi8(_mm512_add_epi8(_mm512_add_epi8(_mm512_loadu_si512(OS[W[0]]), _mm512_loadu_si512(OS[W[1]])),
                                                     _mm512_add_epi8(_mm512_loadu_si512(OS[W[2]]), _mm512_loadu_si512(OS[W[3]]))),
                                     _mm512_add_epi8(_mm512_loadu_si512(OS[W[4]]), _mm512_loadu_si512(OS[W[5]])));
        __m512i m7 = _mm512_loadu_si512(MOD7V);
        __m512i bq = _mm512_loadu_si512(QCB[B1]), bs = _mm512_loadu_si512(SCB[B2]);
        uint64_t cq = (c2 >> n12) & 0xFFFULL, cs = (c2 >> (2 * n12)) & 0xFFFULL;
        while (cq) { int z = n12 + ctz64(cq); cq &= cq - 1; bq = _mm512_or_si512(bq, _mm512_loadu_si512(QCB[z])); }
        while (cs) { int z = 2 * n12 + ctz64(cs); cs &= cs - 1; bs = _mm512_or_si512(bs, _mm512_loadu_si512(SCB[z])); }
        const __m512i zero = _mm512_setzero_si512(), b5 = _mm512_set1_epi8(0x20);
        __m512i tq = _mm512_or_si512(_mm512_or_si512(_mm512_permutexvar_epi8(aq, m7), _mm512_loadu_si512(QCB8[W[2]])),
                                     _mm512_or_si512(_mm512_loadu_si512(QCB16[W[3]]), _mm512_maskz_mov_epi8(_mm512_cmpeq_epi8_mask(bq, zero), b5)));
        __m512i ts = _mm512_or_si512(_mm512_or_si512(_mm512_permutexvar_epi8(as, m7), _mm512_loadu_si512(SCB8[W[4]])),
                                     _mm512_or_si512(_mm512_loadu_si512(SCB16[W[5]]), _mm512_maskz_mov_epi8(_mm512_cmpeq_epi8_mask(bs, zero), b5)));
        _mm512_storeu_si512(T.TQ, tq); _mm512_storeu_si512(T.TS, ts);
    }
#else
    {
        uint8_t badq[64], bads[64];
        memcpy(badq, QCB[B1], 64); memcpy(bads, SCB[B2], 64);
        for (int z = n12; z < 2 * n12; z++) if ((c2 >> z) & 1) for (int k = 0; k < 64; k++) badq[k] |= QCB[z][k];
        for (int z = 2 * n12; z < 3 * n12; z++) if ((c2 >> z) & 1) for (int k = 0; k < 64; k++) bads[k] |= SCB[z][k];
        for (int k = 0; k < 64; k++) {
            int aq = OQ[W[0]][k] + OQ[W[1]][k] + OQ[W[2]][k] + OQ[W[3]][k] + OQ[W[4]][k] + OQ[W[5]][k];
            int as = OS[W[0]][k] + OS[W[1]][k] + OS[W[2]][k] + OS[W[3]][k] + OS[W[4]][k] + OS[W[5]][k];
            T.TQ[k] = (uint8_t)(MOD7[aq] | QCB8[W[2]][k] | QCB16[W[3]][k] | (badq[k] ? 0 : 0x20));
            T.TS[k] = (uint8_t)(MOD7[as] | SCB8[W[4]][k] | SCB16[W[5]][k] | (bads[k] ? 0 : 0x20));
        }
    }
#endif
    for (int v = 0; v < 16; v++) {
        if (v < NV) {
            int a = OXY[W[0]][v] + OXY[W[1]][v] + OXY[W[2]][v] + OXY[W[3]][v] + OXY[W[4]][v] + OXY[W[5]][v];
            T.cst[v] = MOD7[a];
            T.nfY[v] = (uint8_t)(((c2 >> Yv[v]) & 1) == 0);
        } else { T.cst[v] = 0; T.nfY[v] = 0; }
    }
#if L37_SIMD
    for (int z = 0; z < 40; z += 8) {      // lane z: (((((0 + Zr[z][x]) + Zr[z][y]) + Zr[z][q0]) + Zr[z][q1]) + Zr[z][s0]) + Zr[z][s1]
        __m512d zs = _mm512_setzero_pd();
        zs = _mm512_add_pd(zs, _mm512_loadu_pd(&ZrT[W[0]][z])); zs = _mm512_add_pd(zs, _mm512_loadu_pd(&ZrT[W[1]][z]));
        zs = _mm512_add_pd(zs, _mm512_loadu_pd(&ZrT[W[2]][z])); zs = _mm512_add_pd(zs, _mm512_loadu_pd(&ZrT[W[3]][z]));
        zs = _mm512_add_pd(zs, _mm512_loadu_pd(&ZrT[W[4]][z])); zs = _mm512_add_pd(zs, _mm512_loadu_pd(&ZrT[W[5]][z]));
        _mm512_storeu_pd(&T.zq[z], zs);
    }
#else
    for (int z = 0; z < 40; z++) {
        double zs = 0;
        zs += ZrT[W[0]][z]; zs += ZrT[W[1]][z]; zs += ZrT[W[2]][z]; zs += ZrT[W[3]][z]; zs += ZrT[W[4]][z]; zs += ZrT[W[5]][z];
        T.zq[z] = zs;
    }
#endif
    for (int v = 0; v < 16; v++) {
        double s = 0;
        if (v < NV) { s += T.zq[X]; s += T.zq[Yv[v]]; }
        T.base2[v] = s;
    }
    ATst[g] = STAMP;
}
static inline const ATab& atab(int g) { if (ATst[g] != STAMP) build_atab(g); return AT[g]; }

// line37's Rval(ta = A, tb = b) and hval(A, b, R), A assigned (table built)
static inline int Rval_f(int A, int b) {
    const ATab& T = AT[A];
    return RFULL[(T.TQ[cqi[b]] & 7) + (T.TS[csi[b]] & 7) + T.cst[cvar[b]]];
}
static inline double hval_f(int A, int b, int R) {
    const ATab& T = AT[A];
    int qi = cqi[b], si = csi[b];
    double s = T.base2[cvar[b]];
    s += T.zq[P1a[qi]]; s += T.zq[P1b[qi]]; s += T.zq[P2a[si]]; s += T.zq[P2b[si]];
    return -R + 1.0 / 9.0 - s;
}

// ---------------- search state (as in line37; ch[] holds global candidate ids) ----------------
static bool asg[16]; static int ch[16], deg[16];
static int marg[36];
static int ord[16], nasg = 0;
static double Lc[16][16], Lc7[16][16]; static int degenAt = -1;
static long long nodes = 0, leaves = 0, rank_rejects = 0, psd_leaf_rejects = 0, real_cuts = 0, match_rejects = 0;
static double min_lam2 = 1e30; static bool tflag = false; static double limit_s;
static chrono::steady_clock::time_point t0;
static long long d1_total = 0, d1_done = 0;
// domains: for every depth L and far vertex w, the list of its candidates in increasing order (the order of line37's
// vectors): global id (uint16), qi, si (bytes).  Lists of depth L + 1 are compressed from those of depth L.
static int LS = 0;                     // per-depth stride of the list arrays
static int lofs[16];                   // offset of far vertex w inside a depth (room for ncv[w] + 64: vector stores)
static vector<uint16_t> LGID; static vector<uint8_t> LQI, LSI;
static int LN[LEV + 2][16];            // list sizes = line37's dom[w].size()
static uint64_t MSK[16][64], M1K[16][64];   // forward check scratch: kept bits per batch of 64, and those with R = 1
static vector<uint8_t> ch1;            // h1 (b1 in W) per global id
// forward substitution of a candidate g against the assigned block, stored per depth (structure of arrays):
// PSY[i * totG + g] = y_i, PSY7 = y7_i, PSS = s after entry i, PSS7 = s7 after entry i; valid along the current path
static vector<double> PSY, PSY7, PSS, PSS7;

static void chol_push(int v) {         // line37's chol_push, R and h from the tables
    int n = nasg; ord[n] = v;
    if (REAL && degenAt < 0) {
        double s = 0, s7 = 0;
        for (int i = 0; i < n; i++) {
            int va = ord[i];
            int R = Rval_f(ch[va], ch[v]);
            double h = hval_f(ch[va], ch[v], R);
            double t = h, t7 = -h;
            for (int j = 0; j < i; j++) { t -= Lc[n][j] * Lc[i][j]; t7 -= Lc7[n][j] * Lc7[i][j]; }
            Lc[n][i] = t / Lc[i][i]; Lc7[n][i] = t7 / Lc7[i][i];
            s += Lc[n][i] * Lc[n][i]; s7 += Lc7[n][i] * Lc7[n][i];
        }
        double d = cdd[ch[v]], piv = d - s, piv7 = (7.0 - d) - s7;
        if (piv < 1e-7 || piv7 < 1e-7) degenAt = n;
        else { Lc[n][n] = sqrt(piv); Lc7[n][n] = sqrt(piv7); }
    }
    nasg++;
}
static void chol_pop() { nasg--; if (degenAt == nasg) degenAt = -1; }

// eigenvalues of a small symmetric matrix (cyclic Jacobi) -- verbatim
static void jacobi_eig(int n, double A[16][16], double* ev) {
    double a[16][16];
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) a[i][j] = A[i][j];
    for (int sweep = 0; sweep < 100; sweep++) {
        double off = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) off += a[i][j] * a[i][j];
        if (off < 1e-30) break;
        for (int p = 0; p < n; p++) for (int q = p + 1; q < n; q++) {
            if (fabs(a[p][q]) < 1e-300) continue;
            double theta = (a[q][q] - a[p][p]) / (2 * a[p][q]);
            double t = (theta >= 0 ? 1.0 : -1.0) / (fabs(theta) + sqrt(theta * theta + 1));
            double c = 1 / sqrt(t * t + 1), s = t * c;
            for (int k = 0; k < n; k++) {
                double akp = a[k][p], akq = a[k][q];
                a[k][p] = c * akp - s * akq; a[k][q] = s * akp + c * akq;
            }
            for (int k = 0; k < n; k++) {
                double apk = a[p][k], aqk = a[q][k];
                a[p][k] = c * apk - s * aqk; a[q][k] = s * apk + c * aqk;
            }
        }
    }
    for (int i = 0; i < n; i++) ev[i] = a[i][i];
    sort(ev, ev + n);
}

static bool leaf_ok() {                // verbatim, R and h from the tables
    leaves++;
    for (int v = 0; v < NV; v++) if (deg[v] != ccap[ch[v]]) { match_rejects++; return false; }
    if (REAL) {
        double H[16][16], ev[16];
        for (int i = 0; i < NV; i++) for (int j = 0; j < NV; j++) {
            if (i == j) H[i][j] = cdd[ch[i]];
            else { int R = Rval_f(ch[i], ch[j]); H[i][j] = hval_f(ch[i], ch[j], R); }
        }
        jacobi_eig(NV, H, ev);
        if (ev[0] < -1e-7 || ev[NV - 1] > 7 + 1e-7) { psd_leaf_rejects++; return false; }
        if (ev[1] < min_lam2) min_lam2 = ev[1];
        if (RANK && ev[1] > 1e-6) { rank_rejects++; return false; }
    }
    return true;
}

// psd_ok(b) of line37 when the newest assigned triple (index lev in ord) is A: the forward substitution of b against the
// assigned block, entries 0..lev-1 taken from PSY/PSY7 (computed when the earlier triples were assigned, with the same
// rows of Lc), entry lev computed now; the partial sums s, s7 likewise.  Same operations in the same order as line37's
// loop (t = h; t -= Lc[i][j] * y[j] for j < i; y[i] = t / Lc[i][i]; s += y[i] * y[i]), hence the same doubles.
static inline bool psd_inc(int g, int R, int lev, const ATab& T, int w) {
    const size_t G = (size_t)totG;
    double s, s7;
    if (lev == 0) { s = 0; s7 = 0; } else { s = PSS[(lev - 1) * G + g]; s7 = PSS7[(lev - 1) * G + g]; }
    uint32_t nm = cnm[g];
    double hs = T.base2[w];
    hs += T.zq[nm & 255]; hs += T.zq[(nm >> 8) & 255]; hs += T.zq[(nm >> 16) & 255]; hs += T.zq[nm >> 24];
    double h = -R + 1.0 / 9.0 - hs;
    double t = h, t7 = -h;
    for (int j = 0; j < lev; j++) { t -= Lc[lev][j] * PSY[j * G + g]; t7 -= Lc7[lev][j] * PSY7[j * G + g]; }
    double yv = t / Lc[lev][lev], y7v = t7 / Lc7[lev][lev];
    s += yv * yv; s7 += y7v * y7v;
    PSY[lev * G + g] = yv; PSY7[lev * G + g] = y7v; PSS[lev * G + g] = s; PSS7[lev * G + g] = s7;
    double d = cdd[g];
    bool fail = (d - s < -RTOL) | ((7.0 - d) - s7 < -RTOL);
    real_cuts += fail;
    return !fail;
}

// cheap filters of line37's forward check for one batch of (up to) 64 candidates of far vertex w (bytes q[], s[],
// ids gp[], lanes of 'valid') against the new triple A: keep b iff qi_b != qi_A, si_b != si_A, no saturated margin,
// compat(A, b) (share <= 2, R in {0, 1}, R = 1 => share = 1, cap_A = cap_b = 1, NF), not (R = 1 and A full), and
// Rval(p, b) != 1 for the partners p of A.  Returns the kept lanes; *m1out = kept lanes with R(A, b) = 1.
static inline uint64_t kernb(const ATab& T, int w, const uint8_t* q, const uint8_t* s, const uint16_t* gp, uint64_t valid,
                             uint8_t satQ, uint8_t satS, bool r1w, const int* pg, int np, const int* namesA, uint64_t* m1out) {
    uint64_t m0, m1;
#if L37_SIMD
    __m512i vq = _mm512_loadu_si512((const void*)q), vs = _mm512_loadu_si512((const void*)s);
    __m512i tq = _mm512_permutexvar_epi8(vq, _mm512_loadu_si512((const void*)T.TQ));
    __m512i ts = _mm512_permutexvar_epi8(vs, _mm512_loadu_si512((const void*)T.TS));
    const __m512i c7 = _mm512_set1_epi8(7), c18 = _mm512_set1_epi8(0x18), rcl = _mm512_loadu_si512((const void*)RCLS);
    __m512i sum = _mm512_add_epi8(_mm512_add_epi8(_mm512_and_si512(tq, c7), _mm512_and_si512(ts, c7)), _mm512_set1_epi8((char)T.cst[w]));
    __m512i rc = _mm512_permutexvar_epi8(sum, rcl);
    uint64_t k0 = _mm512_cmpeq_epi8_mask(rc, _mm512_set1_epi8(1));
    uint64_t k1 = _mm512_cmpeq_epi8_mask(rc, _mm512_set1_epi8(2));
    uint64_t kq = _mm512_test_epi8_mask(tq, c18), ks = _mm512_test_epi8_mask(ts, c18);
    uint64_t kqq = _mm512_cmpeq_epi8_mask(_mm512_and_si512(tq, c18), c18), kss = _mm512_cmpeq_epi8_mask(_mm512_and_si512(ts, c18), c18);
    uint64_t ksat = _mm512_test_epi8_mask(tq, _mm512_set1_epi8((char)satQ)) | _mm512_test_epi8_mask(ts, _mm512_set1_epi8((char)satS));
    m0 = k0 & ~(kq & ks) & ~kqq & ~kss & ~ksat & valid;
    m1 = 0;
    if (r1w) m1 = k1 & ~(kq | ks) & (uint64_t)_mm512_test_epi8_mask(_mm512_and_si512(tq, ts), _mm512_set1_epi8(0x20)) & valid;
    for (int p = 0; p < np && (m0 | m1); p++) {
        const ATab& P = AT[pg[p]];
        __m512i tqp = _mm512_permutexvar_epi8(vq, _mm512_loadu_si512((const void*)P.TQ));
        __m512i tsp = _mm512_permutexvar_epi8(vs, _mm512_loadu_si512((const void*)P.TS));
        __m512i sp = _mm512_add_epi8(_mm512_add_epi8(_mm512_and_si512(tqp, c7), _mm512_and_si512(tsp, c7)), _mm512_set1_epi8((char)P.cst[w]));
        uint64_t ex = _mm512_cmpeq_epi8_mask(_mm512_permutexvar_epi8(sp, rcl), _mm512_set1_epi8(2));
        m0 &= ~ex; m1 &= ~ex;
    }
#else
    m0 = 0; m1 = 0;
    uint64_t bits = valid;
    while (bits) {
        int c = ctz64(bits); uint64_t bit = bits & (0 - bits); bits ^= bit;
        uint8_t tq = T.TQ[q[c] & 63], ts = T.TS[s[c] & 63];
        int rc = RCLS[(tq & 7) + (ts & 7) + T.cst[w]];
        bool hq = (tq & 0x18) != 0, hs = (ts & 0x18) != 0;
        bool keep;
        if (rc == 1) keep = !(hq && hs) && (tq & 0x18) != 0x18 && (ts & 0x18) != 0x18 && !((tq & satQ) || (ts & satS));
        else if (rc == 2) keep = r1w && !hq && !hs && (tq & ts & 0x20);
        else keep = false;
        if (!keep) continue;
        for (int p = 0; p < np && keep; p++) {
            const ATab& P = AT[pg[p]];
            if (RCLS[(P.TQ[q[c] & 63] & 7) + (P.TS[s[c] & 63] & 7) + P.cst[w]] == 2) keep = false;
        }
        if (!keep) continue;
        if (rc == 2) m1 |= bit; else m0 |= bit;
    }
#endif
    // NF, second half: every name z != x of A has <= 1 G-neighbour in W_b (only for R = 1 candidates, rare)
    uint64_t r = m1;
    while (r) {
        int c = ctz64(r); uint64_t bit = r & (0 - r); r ^= bit;
        uint64_t mb = cmask[gp[c]];
        for (int i = 0; i < 5; i++) if (pc64(nbm[namesA[i]] & mb) > 1) { m1 ^= bit; break; }
    }
    *m1out = m1;
    return m0 | m1;
}

// forward checking of line37 after the commit of (v, A) at depth L: lists of depth L + 1 from those of depth L.
// Returns true if some unassigned far vertex gets an empty domain (line37's "dead"; then nothing else is needed).
// Order of evaluation: all cheap filters first, then the real filter far vertex by far vertex (smallest first); the
// kept sets are the same as line37's (the filters are a conjunction without side effects).
static bool forward(int v, int A, const int* partners, int np, int L) {
    const ATab& T = AT[A];
    int qa = cqi[A], sa = csi[A];
    int q0 = P1a[qa], q1 = P1b[qa], s0 = P2a[sa], s1 = P2b[sa];
    // margins after the commit: a name n of A is saturated if marg[n] + 1 > K(x, n); older saturated names were
    // removed from the lists when they saturated (and qi_A, si_A themselves are removed as "used" by compat)
    uint8_t satQ = (uint8_t)((marg[q0] + 1 > Kx[q0] ? 0x08 : 0) | (marg[q1] + 1 > Kx[q1] ? 0x10 : 0));
    uint8_t satS = (uint8_t)((marg[s0] + 1 > Kx[s0] ? 0x08 : 0) | (marg[s1] + 1 > Kx[s1] ? 0x10 : 0));
    bool allowR1 = (ccap[A] == 1 && deg[v] < ccap[A]);
    int pg[16]; for (int p = 0; p < np; p++) pg[p] = ch[partners[p]];
    const int namesA[5] = {Yv[cvar[A]], q0, q1, s0, s1};
    const size_t pb = (size_t)L * LS, cb = (size_t)(L + 1) * LS;
    int cnt[16];
    for (int w = 0; w < NV; w++) {
        if (asg[w]) continue;
        int n = LN[L][w], nb = (n + 63) >> 6, c = 0;
        const uint8_t* q = &LQI[pb + lofs[w]]; const uint8_t* s = &LSI[pb + lofs[w]]; const uint16_t* gp = &LGID[pb + lofs[w]];
        bool r1w = allowR1 && T.nfY[w];
        for (int b = 0; b < nb; b++) {
            int rem = n - 64 * b;
            uint64_t valid = rem >= 64 ? ~0ULL : ((1ULL << rem) - 1);
            uint64_t m1, m = kernb(T, w, q + 64 * b, s + 64 * b, gp + 64 * b, valid, satQ, satS, r1w, pg, np, namesA, &m1);
            MSK[w][b] = m; M1K[w][b] = m1; c += pc64(m);
        }
        cnt[w] = c;
        if (c == 0) return true;
    }
    if (REAL && degenAt < 0) {         // nasg >= 1 here
        int lev = nasg - 1;
        int wl[16], nw = 0;
        for (int w = 0; w < NV; w++) if (!asg[w]) wl[nw++] = w;
        for (int i = 1; i < nw; i++) {          // insertion sort by cheap count (stable), no allocation
            int key = wl[i], j = i - 1;
            while (j >= 0 && cnt[wl[j]] > cnt[key]) { wl[j + 1] = wl[j]; j--; }
            wl[j + 1] = key;
        }
        for (int ii = 0; ii < nw; ii++) {
            int w = wl[ii], c = 0, nb = (LN[L][w] + 63) >> 6;
            const uint16_t* gp = &LGID[pb + lofs[w]];
            for (int b = 0; b < nb; b++) {
                uint64_t m = MSK[w][b], r1 = M1K[w][b], bits = m;
                const uint16_t* gb = gp + 64 * b;
                while (bits) {
                    int k = ctz64(bits); bits &= bits - 1;
                    bool ok = psd_inc(gb[k], (int)((r1 >> k) & 1), lev, T, w);
                    m &= ~((uint64_t)!ok << k);
                }
                MSK[w][b] = m; c += pc64(m);
            }
            cnt[w] = c;
            if (c == 0) return true;
        }
    }
    // the child's lists (order preserved)
    for (int w = 0; w < NV; w++) {
        if (asg[w]) continue;
        int nb = (LN[L][w] + 63) >> 6, off = 0;
        const uint8_t* q = &LQI[pb + lofs[w]]; const uint8_t* s = &LSI[pb + lofs[w]]; const uint16_t* gp = &LGID[pb + lofs[w]];
        uint8_t* cq = &LQI[cb + lofs[w]]; uint8_t* cs = &LSI[cb + lofs[w]]; uint16_t* cg = &LGID[cb + lofs[w]];
        for (int b = 0; b < nb; b++) {
            uint64_t m = MSK[w][b];
            if (!m) continue;
#if L37_SIMD
            _mm512_storeu_si512((void*)(cq + off), _mm512_maskz_compress_epi8(m, _mm512_loadu_si512((const void*)(q + 64 * b))));
            _mm512_storeu_si512((void*)(cs + off), _mm512_maskz_compress_epi8(m, _mm512_loadu_si512((const void*)(s + 64 * b))));
            uint32_t mlo = (uint32_t)m, mhi = (uint32_t)(m >> 32);
            _mm512_storeu_si512((void*)(cg + off), _mm512_maskz_compress_epi16(mlo, _mm512_loadu_si512((const void*)(gp + 64 * b))));
            _mm512_storeu_si512((void*)(cg + off + __builtin_popcount(mlo)),
                                _mm512_maskz_compress_epi16(mhi, _mm512_loadu_si512((const void*)(gp + 64 * b + 32))));
            off += pc64(m);
#else
            while (m) {
                int k = ctz64(m); m &= m - 1;
                cq[off] = q[64 * b + k]; cs[off] = s[64 * b + k]; cg[off] = gp[64 * b + k]; off++;
            }
#endif
        }
        LN[L + 1][w] = off;
    }
    return false;
}

static bool rec(int depth);

// one value (v, A) of the branching loop of line37's rec; returns true if a solution was found below
static bool try_branch(int v, int A, int depth) {
    if (depth == 0) d1_done++;
    int partners[16], np = 0; bool ok = true;
    for (int i = 0; i < nasg; i++) {
        int w = ord[i];
        if (Rval_f(ch[w], A) == 1) {
            if (deg[w] >= ccap[ch[w]]) { ok = false; break; }
            partners[np++] = w;
        }
    }
    if (!ok || np > ccap[A]) return false;
    // commit
    asg[v] = true; ch[v] = A; deg[v] = np;
    for (int i = 0; i < np; i++) deg[partners[i]]++;
    int qa = cqi[A], sa = csi[A];
    int nm[4] = {P1a[qa], P1b[qa], P2a[sa], P2b[sa]};
    for (int k = 0; k < 4; k++) marg[nm[k]]++;
    atab(A);
    chol_push(v);
    bool dead = forward(v, A, partners, np, depth);
    bool found = false;
    if (!dead) found = rec(depth + 1);
    if (found) return true;
    // undo
    chol_pop();
    for (int k = 0; k < 4; k++) marg[nm[k]]--;
    for (int i = 0; i < np; i++) deg[partners[i]]--;
    deg[v] = 0; asg[v] = false;
    return false;
}

static bool rec(int depth) {
    nodes++;
    if ((nodes & 1023) == 0) {
        double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
        if (el > limit_s) { tflag = true; return false; }
        static double last = 0;
        if (el - last > 60) { last = el; fprintf(stderr, "[%.0fs] nodes %lld, depth-1 branch %lld/%lld, leaves %lld\n", el, nodes, d1_done, d1_total, leaves); }
    }
    if (nasg == NV) return leaf_ok();
    const size_t pb = (size_t)depth * LS;
    bool b1mode = (marg[B1] == 0 && Kx[B1] == 1);
    if (b1mode) {                      // every candidate containing b1, far vertices in order, then smallest domain
        if (depth == 0) {
            long long n = 0;
            for (int v = 0; v < NV; v++) if (!asg[v]) {
                const uint16_t* gp = &LGID[pb + lofs[v]];
                for (int i = 0; i < LN[depth][v]; i++) n += ch1[gp[i]];
            }
            d1_total = n;
        }
        for (int v = 0; v < NV; v++) {
            if (asg[v]) continue;
            const uint16_t* gp = &LGID[pb + lofs[v]];
            int n = LN[depth][v];
            for (int i = 0; i < n; i++) {
                int g = gp[i];
                if (!ch1[g]) continue;
                if (try_branch(v, g, depth)) return true;
                if (tflag) return false;
            }
        }
    } else {
        int best = -1, bc = 0x7fffffff;
        for (int v = 0; v < NV; v++) if (!asg[v] && LN[depth][v] < bc) { bc = LN[depth][v]; best = v; }
        if (bc == 0) return false;
        if (depth == 0) d1_total = bc;
        const uint16_t* gp = &LGID[pb + lofs[best]];
        for (int i = 0; i < bc; i++) {
            if (try_branch(best, gp[i], depth)) return true;
            if (tflag) return false;
        }
    }
    return false;
}

static void reset_engine() {
    memset(asg, 0, sizeof asg); memset(ch, 0, sizeof ch); memset(deg, 0, sizeof deg); memset(marg, 0, sizeof marg);
    nasg = 0; degenAt = -1;
    nodes = leaves = rank_rejects = psd_leaf_rejects = real_cuts = match_rejects = 0;
    min_lam2 = 1e30; tflag = false; d1_total = d1_done = 0;
    t0 = chrono::steady_clock::now();
}

struct Outcome { string status; int x; long long cand, nodes; double t_build, t_prep, t_search; unsigned long long chash; };

static double since(chrono::steady_clock::time_point a) { return chrono::duration<double>(chrono::steady_clock::now() - a).count(); }

static Outcome test_line(const int* s01, const int* s12, const int* s20) {
    Outcome o{"", -1, 0, 0, 0, 0, 0, 0};
    auto a = chrono::steady_clock::now();
    build_g(s01, s12, s20);
    if (!admissible()) { o.status = "K<0"; o.t_build = since(a); return o; }
    if (ncomp() != 1) { o.status = "disconnected"; o.t_build = since(a); return o; }
    int detv;
    if (!inv_mod7(detv)) { o.status = "7-torsion"; o.t_build = since(a); return o; }
    int leg = (detv * detv % 7 * detv % 7 == 1) ? 1 : -1;
    if (leg == 1) { o.status = "L23"; o.t_build = since(a); return o; }
    inv_real();
    o.t_build = since(a);
    a = chrono::steady_clock::now();
    bool okx = false;
    for (int x = 0; x < n12 && !okx; x++) if (prep_star(x, o.cand)) { o.x = x; okx = true; }
    if (okx) prep_tables();
    o.t_prep = since(a);
    o.chash = okx ? CHASH : 0;
    if (!okx) { o.status = "no-x"; return o; }
    a = chrono::steady_clock::now();
    reset_engine();
    LS = 0;
    for (int w = 0; w < NV; w++) { lofs[w] = LS; LS += ((ncv[w] + 64 + 63) / 64) * 64; }
    size_t need = (size_t)(LEV + 2) * LS;
    if (LGID.size() < need) { LGID.resize(need); LQI.resize(need); LSI.resize(need); }
    if (PSY.size() < (size_t)totG * LEV) { PSY.resize((size_t)totG * LEV); PSY7.resize((size_t)totG * LEV); PSS.resize((size_t)totG * LEV); PSS7.resize((size_t)totG * LEV); }
    if ((int)ch1.size() < totG) ch1.resize(totG);
    for (int w = 0; w < NV; w++) {
        for (int c = 0; c < ncv[w]; c++) {
            int g = wbase[w] + c;
            LGID[lofs[w] + c] = (uint16_t)g; LQI[lofs[w] + c] = cqi[g]; LSI[lofs[w] + c] = csi[g];
            ch1[g] = (uint8_t)((cmask[g] >> B1) & 1);
        }
        LN[0][w] = ncv[w];
    }
    bool found = rec(0);
    o.t_search = since(a);
    o.nodes = nodes;
    o.status = found ? "SAT" : (tflag ? "TIMEOUT" : "UNSAT");
    return o;
}

int main(int argc, char** argv) {
#ifdef _WIN32
    SetPriorityClass(GetCurrentProcess(), IDLE_PRIORITY_CLASS);
#endif
    init_static(); init_static_tables();
#ifdef L37_CHECK_PREP
    atexit([] { fprintf(stderr, "prep check: %lld triples, all three L2 tests agree\n", prep_checked); });
#endif
    if (argc < 3) { fprintf(stderr, "usage: line37_fast file <lines.txt> [limit] | line37_fast rand <count> <seed> [limit]\n"); return 1; }
    string mode = argv[1];
    if (mode == "file" || mode == "filev") {
        bool v = (mode == "filev");
        limit_s = argc > 3 ? atof(argv[3]) : 600;
        FILE* f = fopen(argv[2], "r");
        if (!f) { fprintf(stderr, "cannot open %s\n", argv[2]); return 1; }
        int s[36], idx = 0;
        while (true) {
            bool okr = true;
            for (int k = 0; k < 36; k++) if (fscanf(f, "%d", &s[k]) != 1) { okr = false; break; }
            if (!okr) break;
            Outcome o = test_line(s, s + 12, s + 24);
            if (v) printf("{\"line\": %d, \"status\": \"%s\", \"x\": %d, \"candidates\": %lld, \"nodes\": %lld, \"chash\": \"%016llx\"}\n",
                          idx++, o.status.c_str(), o.x, o.cand, o.nodes, o.chash);
            else printf("{\"line\": %d, \"status\": \"%s\", \"x\": %d, \"candidates\": %lld, \"nodes\": %lld, \"build_ms\": %.3f, "
                        "\"prep_ms\": %.3f, \"search_ms\": %.3f}\n", idx++, o.status.c_str(), o.x, o.cand, o.nodes,
                        1e3 * o.t_build, 1e3 * o.t_prep, 1e3 * o.t_search);
            fflush(stdout);
        }
        return 0;
    }
    bool verbose = (mode == "randv");
    long long count = atoll(argv[2]); unsigned long long seed = strtoull(argv[3], 0, 10);
    limit_s = argc > 4 ? atof(argv[4]) : 600;
    mt19937_64 rng(seed);
    int s01[12], s12[12], s20[12];
    long long by[8] = {0}; const char* names[8] = {"K<0", "disconnected", "7-torsion", "L23", "no-x", "UNSAT", "SAT", "TIMEOUT"};
    double tb = 0, tp = 0, ts = 0, tmax = 0; long long nmax = 0, ntest = 0;
    vector<double> tl;
    auto T0 = chrono::steady_clock::now();
    for (long long it = 0; it < count; it++) {
        for (int* s : {s01, s12, s20}) { for (int i = 0; i < 12; i++) s[i] = i; shuffle(s, s + 12, rng); }
        Outcome o = test_line(s01, s12, s20);
        int k = 0; while (k < 8 && o.status != names[k]) k++;
        by[k]++;
        tb += o.t_build;
        if (o.status == "UNSAT" || o.status == "SAT" || o.status == "TIMEOUT") {
            tp += o.t_prep; ts += o.t_search; ntest++;
            double tt = o.t_build + o.t_prep + o.t_search; tl.push_back(tt);
            if (tt > tmax) tmax = tt;
            if (o.nodes > nmax) nmax = o.nodes;
        }
        if (verbose) printf("{\"i\": %lld, \"status\": \"%s\", \"x\": %d, \"candidates\": %lld, \"nodes\": %lld, \"chash\": \"%016llx\"}\n",
                            it, o.status.c_str(), o.x, o.cand, o.nodes, o.chash);
        if (o.status == "SAT" || o.status == "TIMEOUT")
            fprintf(stderr, "line %lld: %s (s01..s20 follow)\n", it, o.status.c_str());
    }
    double wall = since(T0);
    sort(tl.begin(), tl.end());
    printf("{\"count\": %lld, \"seed\": %llu", count, seed);
    for (int k = 0; k < 8; k++) printf(", \"%s\": %lld", names[k], by[k]);
    printf(", \"tested\": %lld, \"build_ms_per_line\": %.4f, \"prep_ms_per_tested\": %.4f, \"search_ms_per_tested\": %.4f, "
           "\"tested_ms_median\": %.4f, \"tested_ms_p99\": %.4f, \"tested_ms_max\": %.4f, \"nodes_max\": %lld, "
           "\"wall_s\": %.2f, \"ms_per_sample\": %.4f}\n", ntest, 1e3 * tb / max(count, 1LL), 1e3 * tp / max(ntest, 1LL),
           1e3 * ts / max(ntest, 1LL), tl.empty() ? 0 : 1e3 * tl[tl.size() / 2], tl.empty() ? 0 : 1e3 * tl[(size_t)(tl.size() * 0.99)],
           1e3 * tmax, nmax, wall, 1e3 * wall / max(count, 1LL));
    return 0;
}
