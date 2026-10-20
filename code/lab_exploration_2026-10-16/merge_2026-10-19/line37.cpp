// star39: exact search for the complete star of a near vertex x of a generic line, at rank 37 (rho = 0) or 39
// (rho = 2) (LAB 20/10/2026).  Input from star39_prep.py.  Ten far vertices W_y = {x, y} u q_y u s_y, each a candidate
// (triple, u), u in F_7^rho.  Exact conditions (all necessary in a srg(99,14,1,2) of the given rank):
//   pairs:  q and s distinct (bijections); |W n W'| <= 2 (L3); R = 4 - e^T Omega e' + u^T D u' mod 7 in {0, 1};
//   lambda = 1 at x: N(x) induces a perfect matching, so W has exactly cap(W) = 1 - |N_G(x) n W| star neighbours and two
//          star neighbours share only x; NF: if W ~ W', every name z != x of one has <= 1 G-neighbour in the other;
//   margins: #{y : n in W_y} <= K(x, n) for n in C1 u C2 (= at the end, automatically);
//   real far projector (every rank): H(a, b) = 3 delta - R - e_a^T Z e_b + 1/9 = 7 Pi_T, so H and 7I - H are PSD on
//          the assigned block (Schur complements, incremental Cholesky, tolerance 1e-9, skipped if singular) and,
//          on the complete star, H has rank <= 8 (its second smallest eigenvalue must be 0; the all-ones vector of the
//          star is in its kernel automatically).
// Branching: first the far vertex containing b1 = the C1-neighbour of x (K(x, b1) = 1: exactly one, of cap 0, all its
// pairs pinned to R = 0), then smallest domain.  O(D) symmetry: while every assigned u is 0, only canonical u.
// usage: star39 <file.bin> <seconds>        env: STAR_NOREAL=1 (no real filter), STAR_NORANK=1 (no rank-8 test)
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <chrono>
#include <cmath>
#include <algorithm>
#ifdef _WIN32
#include <windows.h>
#endif
using namespace std;

struct Tri { int names[6]; int qi, si, cap, h1, h2; uint8_t Y[36]; uint8_t nbc[36]; double zq[36]; double dd; uint64_t mask; };
struct Cand { int ti, canon, u0, u1; bool nz; };
struct Var { int y; vector<Tri> tri; vector<Cand> cand; };

static int rho, delta_, X, B1, B2, NV;
static int nbr[36][3], Kx[36], Dq[2];
static vector<Var> V;
static bool REAL = true, RANK = true;
static const double RTOL = 1e-9;

static bool asg[16]; static int ch[16], deg[16];
static bool usedQ[64], usedS[64]; static int marg[36];
static bool anynz = false;
static int ord[16], nasg = 0;
static double Lc[16][16], Lc7[16][16]; static int degenAt = -1;
static long long nodes = 0, leaves = 0, rank_rejects = 0, psd_leaf_rejects = 0, real_cuts = 0, match_rejects = 0;
static double min_lam2 = 1e30; static bool tflag = false; static double limit_s;
static chrono::steady_clock::time_point t0;
static long long d1_total = 0, d1_done = 0;

static inline const Tri& TR(int v, int c) { return V[v].tri[V[v].cand[c].ti]; }
static inline int Rval(int va, int ca, int vb, int cb) {
    const Cand& A = V[va].cand[ca]; const Cand& B = V[vb].cand[cb];
    const Tri& ta = V[va].tri[A.ti]; const Tri& tb = V[vb].tri[B.ti];
    int s = 0;
    for (int k = 0; k < 6; k++) s += ta.Y[tb.names[k]];
    int b = Dq[0] * A.u0 * B.u0 + Dq[1] * A.u1 * B.u1;
    int R = (4 - s + b) % 7; if (R < 0) R += 7;
    return R;
}
static inline bool compat(int va, int ca, int vb, int cb, int& Rout) {
    const Tri& ta = TR(va, ca); const Tri& tb = TR(vb, cb);
    if (ta.qi == tb.qi || ta.si == tb.si) return false;
    int share = __builtin_popcountll(ta.mask & tb.mask);
    if (share > 2) return false;
    int R = Rval(va, ca, vb, cb);
    if (R > 1) return false;
    if (R == 1) {
        if (share != 1 || ta.cap != 1 || tb.cap != 1) return false;
        for (int k = 0; k < 6; k++) { int z = tb.names[k]; if (z != X && ta.nbc[z] > 1) return false; }
        for (int k = 0; k < 6; k++) { int z = ta.names[k]; if (z != X && tb.nbc[z] > 1) return false; }
    }
    Rout = R;
    return true;
}
static inline double hval(int va, int ca, int vb, int cb, int R) {
    const Tri& ta = TR(va, ca); const Tri& tb = TR(vb, cb);
    double s = 0;
    for (int k = 0; k < 6; k++) s += ta.zq[tb.names[k]];
    return -R + 1.0 / 9.0 - s;
}
static bool psd_ok(int vb, int cb) {
    if (!REAL || degenAt >= 0 || nasg == 0) return true;
    double y[16], y7[16], s = 0, s7 = 0;
    for (int i = 0; i < nasg; i++) {
        int va = ord[i], ca = ch[va];
        int R = Rval(va, ca, vb, cb);
        double h = hval(va, ca, vb, cb, R);
        double t = h, t7 = -h;
        for (int j = 0; j < i; j++) { t -= Lc[i][j] * y[j]; t7 -= Lc7[i][j] * y7[j]; }
        y[i] = t / Lc[i][i]; y7[i] = t7 / Lc7[i][i];
        s += y[i] * y[i]; s7 += y7[i] * y7[i];
    }
    double d = TR(vb, cb).dd;
    if (d - s < -RTOL || (7.0 - d) - s7 < -RTOL) { real_cuts++; return false; }
    return true;
}
static void chol_push(int v) {
    int n = nasg; ord[n] = v;
    if (REAL && degenAt < 0) {
        double s = 0, s7 = 0;
        for (int i = 0; i < n; i++) {
            int va = ord[i];
            int R = Rval(va, ch[va], v, ch[v]);
            double h = hval(va, ch[va], v, ch[v], R);
            double t = h, t7 = -h;
            for (int j = 0; j < i; j++) { t -= Lc[n][j] * Lc[i][j]; t7 -= Lc7[n][j] * Lc7[i][j]; }
            Lc[n][i] = t / Lc[i][i]; Lc7[n][i] = t7 / Lc7[i][i];
            s += Lc[n][i] * Lc[n][i]; s7 += Lc7[n][i] * Lc7[n][i];
        }
        double d = TR(v, ch[v]).dd, piv = d - s, piv7 = (7.0 - d) - s7;
        if (piv < 1e-7 || piv7 < 1e-7) degenAt = n;
        else { Lc[n][n] = sqrt(piv); Lc7[n][n] = sqrt(piv7); }
    }
    nasg++;
}
static void chol_pop() { nasg--; if (degenAt == nasg) degenAt = -1; }

// eigenvalues of a small symmetric matrix (cyclic Jacobi)
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

static bool leaf_ok() {
    leaves++;
    for (int v = 0; v < NV; v++) if (deg[v] != TR(v, ch[v]).cap) { match_rejects++; return false; }
    if (REAL) {
        double H[16][16], ev[16];
        for (int i = 0; i < NV; i++) for (int j = 0; j < NV; j++) {
            if (i == j) H[i][j] = TR(i, ch[i]).dd;
            else { int R = Rval(i, ch[i], j, ch[j]); H[i][j] = hval(i, ch[i], j, ch[j], R); }
        }
        jacobi_eig(NV, H, ev);
        if (ev[0] < -1e-7 || ev[NV - 1] > 7 + 1e-7) { psd_leaf_rejects++; return false; }
        if (ev[1] < min_lam2) min_lam2 = ev[1];
        if (RANK && ev[1] > 1e-6) { rank_rejects++; return false; }
    }
    return true;
}

static bool rec(vector<vector<int>>& dom, int depth) {
    nodes++;
    if ((nodes & 1023) == 0) {
        double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
        if (el > limit_s) { tflag = true; return false; }
        static double last = 0;
        if (el - last > 60) { last = el; fprintf(stderr, "[%.0fs] nodes %lld, depth-1 branch %lld/%lld, leaves %lld\n", el, nodes, d1_done, d1_total, leaves); }
    }
    if (nasg == NV) return leaf_ok();
    // branching set
    vector<pair<int, int>> br;
    bool b1mode = (marg[B1] == 0 && Kx[B1] == 1);
    if (b1mode) {
        for (int v = 0; v < NV; v++) if (!asg[v]) for (int c : dom[v]) if (TR(v, c).h1) br.push_back({v, c});
    } else {
        int best = -1; size_t bc = (size_t)-1;
        for (int v = 0; v < NV; v++) if (!asg[v] && dom[v].size() < bc) { bc = dom[v].size(); best = v; }
        if (bc == 0) return false;
        for (int c : dom[best]) br.push_back({best, c});
    }
    if (depth == 0) d1_total = (long long)br.size();
    for (auto& pc : br) {
        int v = pc.first, c = pc.second;
        if (depth == 0) d1_done++;
        const Cand& cd = V[v].cand[c];
        if (!anynz && cd.nz && !cd.canon) continue;
        // matching capacities against the assigned vertices
        int partners[16], np = 0; bool ok = true;
        for (int i = 0; i < nasg; i++) {
            int w = ord[i];
            if (Rval(w, ch[w], v, c) == 1) {
                if (deg[w] >= TR(w, ch[w]).cap) { ok = false; break; }
                partners[np++] = w;
            }
        }
        if (!ok || np > TR(v, c).cap) continue;
        // commit
        const Tri& t = TR(v, c);
        asg[v] = true; ch[v] = c; deg[v] = np;
        for (int i = 0; i < np; i++) deg[partners[i]]++;
        usedQ[t.qi] = usedS[t.si] = true;
        for (int k = 2; k < 6; k++) marg[t.names[k]]++;
        bool prev_nz = anynz; if (cd.nz) anynz = true;
        chol_push(v);
        // forward checking
        vector<vector<int>> nd(NV);
        bool dead = false;
        for (int w = 0; w < NV && !dead; w++) {
            if (asg[w]) continue;
            nd[w].reserve(dom[w].size());
            for (int c2 : dom[w]) {
                const Tri& t2 = TR(w, c2);
                if (usedQ[t2.qi] || usedS[t2.si]) continue;
                bool mok = true;
                for (int k = 2; k < 6; k++) if (marg[t2.names[k]] + 1 > Kx[t2.names[k]]) { mok = false; break; }
                if (!mok) continue;
                int R;
                if (!compat(v, c, w, c2, R)) continue;
                if (R == 1 && deg[v] >= t.cap) continue;
                bool sok = true;
                for (int i = 0; i < np; i++) { int p2 = partners[i]; if (Rval(p2, ch[p2], w, c2) == 1) { sok = false; break; } }
                if (!sok) continue;
                if (!psd_ok(w, c2)) continue;
                nd[w].push_back(c2);
            }
            if (nd[w].empty()) dead = true;
        }
        bool found = false;
        if (!dead) found = rec(nd, depth + 1);
        if (found) return true;
        // undo
        chol_pop();
        anynz = prev_nz;
        for (int k = 2; k < 6; k++) marg[t.names[k]]--;
        usedQ[t.qi] = usedS[t.si] = false;
        for (int i = 0; i < np; i++) deg[partners[i]]--;
        deg[v] = 0; asg[v] = false;
        if (tflag) return false;
    }
    return false;
}

// ---- line37: everything below is new; the engine above is star39.cpp verbatim (LAB 20/10/2026) ----
// Complete rank-37 star test of one line graph G_T given by its three bijections, all in C++.  Same conditions as
// star39_prep.py (rho = 0) + star39.cpp: G_T, admissibility K >= 0, connectivity, Omega = (3I - G + J)^-1 mod 7 (it
// exists iff 7 does not divide tau, since det(3I - G + J) = 36^2 tau = tau mod 7), L23 ((tau|7) = -1 is needed for a
// generic line at rank 37), Z = (3I - G + J)^-1 over the reals, the first x of C0 outside a transversal triangle, the
// 10 domains (K(x, .) >= 1, L2, real unary 0 <= H(W, W) <= 7, g(W, W) = 0), then the exact star search.
// usage: line37 file <lines.txt> [limit_s]     one G_T per line: s01[12] s12[12] s20[12]; one JSON line per G_T
//        line37 rand <count> <seed> [limit_s]  uniform random bijection triples; summary JSON (timing per stage)
#include <random>
#include <string>

static const int NN = 36, n12 = 12;
static int Gm[36][36], Km[36][36], Om[36][36];
static double Zr[36][36];
static const int INV7[7] = {0, 1, 4, 5, 2, 3, 6};

static void reset_engine() {
    memset(asg, 0, sizeof asg); memset(ch, 0, sizeof ch); memset(deg, 0, sizeof deg);
    memset(usedQ, 0, sizeof usedQ); memset(usedS, 0, sizeof usedS); memset(marg, 0, sizeof marg);
    anynz = false; nasg = 0; degenAt = -1;
    nodes = leaves = rank_rejects = psd_leaf_rejects = real_cuts = match_rejects = 0;
    min_lam2 = 1e30; tflag = false; d1_total = d1_done = 0;
    t0 = chrono::steady_clock::now();
}

static void build_g(const int* s01, const int* s12, const int* s20) {
    memset(Gm, 0, sizeof Gm);
    for (int c = 0; c < 3; c++) for (int i = 0; i < n12; i++) Gm[c * n12 + i][c * n12 + (i ^ 1)] = 1;
    for (int i = 0; i < n12; i++) {
        int a = i, b = n12 + s01[i]; Gm[a][b] = Gm[b][a] = 1;
        a = n12 + i; b = 2 * n12 + s12[i]; Gm[a][b] = Gm[b][a] = 1;
        a = 2 * n12 + i; b = s20[i]; Gm[a][b] = Gm[b][a] = 1;
    }
    for (int v = 0; v < NN; v++) { int k = 0; for (int z = 0; z < NN; z++) if (Gm[v][z]) nbr[v][k++] = z; }
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

// the 10 domains of the star of x (rank 37: u = 0, g(W, W) = 0); returns false if x is in a transversal triangle
static bool prep_star(int x, long long& ncand) {
    int xb = x ^ 1, b1 = -1, b2 = -1;
    for (int k = 0; k < 3; k++) { int z = nbr[x][k]; if (z >= n12 && z < 2 * n12) b1 = z; if (z >= 2 * n12) b2 = z; }
    if (Gm[b1][b2]) return false;
    rho = 0; delta_ = 0; X = x; B1 = b1; B2 = b2; Dq[0] = Dq[1] = 0;
    for (int z = 0; z < NN; z++) Kx[z] = Km[x][z];
    vector<pair<int, int>> P1, P2;
    for (int i = 0; i < n12; i++) for (int j = i + 1; j < n12; j++) if (i / 2 != j / 2) {
        P1.push_back({n12 + i, n12 + j}); P2.push_back({2 * n12 + i, 2 * n12 + j});
    }
    V.assign(0, Var());
    ncand = 0;
    for (int y = 0; y < n12; y++) {
        if (y == x || y == xb) continue;
        Var var; var.y = y;
        for (int qi = 0; qi < (int)P1.size(); qi++) {
            int q0 = P1[qi].first, q1 = P1[qi].second;
            if (Km[x][q0] == 0 || Km[x][q1] == 0) continue;
            for (int si = 0; si < (int)P2.size(); si++) {
                int s0 = P2[si].first, s1 = P2[si].second;
                if (Km[x][s0] == 0 || Km[x][s1] == 0) continue;
                int W[6] = {x, y, q0, q1, s0, s1};
                uint64_t mask = 0; for (int k = 0; k < 6; k++) mask |= 1ULL << W[k];
                bool ok = true;
                for (int k = 0; k < 6 && ok; k++) {
                    int c = 0; for (int j = 0; j < 3; j++) c += (mask >> nbr[W[k]][j]) & 1;
                    if (c > 1) ok = false;
                }
                if (!ok) continue;
                int cnt[36] = {0};
                for (int k = 0; k < 6 && ok; k++) for (int j = 0; j < 3; j++) {
                    int z = nbr[W[k]][j];
                    if (!((mask >> z) & 1) && ++cnt[z] > 2) ok = false;
                }
                if (!ok) continue;
                double ez = 0; for (int a = 0; a < 6; a++) for (int b = 0; b < 6; b++) ez += Zr[W[a]][W[b]];
                double dd = 3.0 + 1.0 / 9.0 - ez;
                if (dd < -1e-9 || dd > 7 + 1e-9) continue;
                int g = 0; for (int a = 0; a < 6; a++) for (int b = 0; b < 6; b++) g += Om[W[a]][W[b]];
                if (g % 7) continue;
                Tri t;
                for (int k = 0; k < 6; k++) t.names[k] = W[k];
                t.qi = qi; t.si = si;
                int nx = 0; for (int j = 0; j < 3; j++) nx += (mask >> nbr[x][j]) & 1;
                t.cap = 1 - nx; t.h1 = (mask >> b1) & 1; t.h2 = (mask >> b2) & 1;
                for (int z = 0; z < NN; z++) {
                    int s = 0; double zs = 0;
                    for (int k = 0; k < 6; k++) { s += Om[z][W[k]]; zs += Zr[z][W[k]]; }
                    t.Y[z] = (uint8_t)(s % 7); t.zq[z] = zs;
                    int c = 0; for (int j = 0; j < 3; j++) c += (mask >> nbr[z][j]) & 1;
                    t.nbc[z] = (uint8_t)c;
                }
                t.dd = dd; t.mask = mask;
                Cand cd; cd.ti = (int)var.tri.size(); cd.canon = 1; cd.u0 = 0; cd.u1 = 0; cd.nz = false;
                var.tri.push_back(t); var.cand.push_back(cd);
            }
        }
        ncand += (long long)var.cand.size();
        V.push_back(var);
    }
    NV = (int)V.size();
    return true;
}

struct Outcome { string status; int x; long long cand, nodes; double t_build, t_prep, t_search; };

static double since(chrono::steady_clock::time_point a) { return chrono::duration<double>(chrono::steady_clock::now() - a).count(); }

static Outcome test_line(const int* s01, const int* s12, const int* s20) {
    Outcome o{"", -1, 0, 0, 0, 0, 0};
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
    o.t_prep = since(a);
    if (!okx) { o.status = "no-x"; return o; }
    a = chrono::steady_clock::now();
    reset_engine();
    vector<vector<int>> dom(NV);
    for (int v = 0; v < NV; v++) { dom[v].resize(V[v].cand.size()); for (size_t c = 0; c < V[v].cand.size(); c++) dom[v][c] = (int)c; }
    bool found = rec(dom, 0);
    o.t_search = since(a);
    o.nodes = nodes;
    o.status = found ? "SAT" : (tflag ? "TIMEOUT" : "UNSAT");
    return o;
}

int main(int argc, char** argv) {
#ifdef _WIN32
    SetPriorityClass(GetCurrentProcess(), IDLE_PRIORITY_CLASS);
#endif
    if (argc < 3) { fprintf(stderr, "usage: line37 file <lines.txt> [limit] | line37 rand <count> <seed> [limit]\n"); return 1; }
    string mode = argv[1];
    if (mode == "file") {
        limit_s = argc > 3 ? atof(argv[3]) : 600;
        FILE* f = fopen(argv[2], "r");
        int s[36], idx = 0;
        while (true) {
            bool okr = true;
            for (int k = 0; k < 36; k++) if (fscanf(f, "%d", &s[k]) != 1) { okr = false; break; }
            if (!okr) break;
            Outcome o = test_line(s, s + 12, s + 24);
            printf("{\"line\": %d, \"status\": \"%s\", \"x\": %d, \"candidates\": %lld, \"nodes\": %lld, \"build_ms\": %.3f, "
                   "\"prep_ms\": %.3f, \"search_ms\": %.3f}\n", idx++, o.status.c_str(), o.x, o.cand, o.nodes,
                   1e3 * o.t_build, 1e3 * o.t_prep, 1e3 * o.t_search);
            fflush(stdout);
        }
        return 0;
    }
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
