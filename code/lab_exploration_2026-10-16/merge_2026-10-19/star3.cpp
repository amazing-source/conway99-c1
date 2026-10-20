// star3: star39.cpp with a residue of rank up to 3, u in F_7^3 (LAB 20/10/2026).  Identical search; input from
// star_prep_gen.py --fmt3 (Dq and u have three components).  The header of star39.cpp follows, unchanged.
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
// usage: star3 <file.bin> <seconds>        env: STAR_NOREAL=1 (no real filter), STAR_NORANK=1 (no rank-8 test)
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
struct Cand { int ti, canon, u0, u1, u2; bool nz; };
struct Var { int y; vector<Tri> tri; vector<Cand> cand; };

static int rho, delta_, X, B1, B2, NV;
static int nbr[36][3], Kx[36], Dq[3];
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
    int b = Dq[0] * A.u0 * B.u0 + Dq[1] * A.u1 * B.u1 + Dq[2] * A.u2 * B.u2;
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

int main(int argc, char** argv) {
#ifdef _WIN32
    SetPriorityClass(GetCurrentProcess(), IDLE_PRIORITY_CLASS);
#endif
    if (argc < 3) { fprintf(stderr, "usage: star3 <file.bin> <seconds>\n"); return 1; }
    FILE* f = fopen(argv[1], "rb"); limit_s = atof(argv[2]);
    if (getenv("STAR_NOREAL")) REAL = false;
    if (getenv("STAR_NORANK")) RANK = false;
    int hdr[6]; fread(hdr, 4, 6, f); rho = hdr[0]; delta_ = hdr[1]; X = hdr[2]; B1 = hdr[3]; B2 = hdr[4]; NV = hdr[5];
    vector<int> nb(108); fread(nb.data(), 4, 108, f);
    for (int v = 0; v < 36; v++) for (int k = 0; k < 3; k++) nbr[v][k] = nb[v * 3 + k];
    fread(Kx, 4, 36, f); fread(Dq, 4, 3, f);
    V.resize(NV);
    size_t totc = 0;
    for (int v = 0; v < NV; v++) {
        int h3[3]; fread(h3, 4, 3, f); V[v].y = h3[0];
        V[v].tri.resize(h3[1]); V[v].cand.resize(h3[2]);
        for (auto& t : V[v].tri) {
            fread(t.names, 4, 6, f); int h5[5]; fread(h5, 4, 5, f);
            t.qi = h5[0]; t.si = h5[1]; t.cap = h5[2]; t.h1 = h5[3]; t.h2 = h5[4];
            fread(t.Y, 1, 36, f); fread(t.nbc, 1, 36, f); fread(t.zq, 8, 36, f); fread(&t.dd, 8, 1, f);
            t.mask = 0; for (int k = 0; k < 6; k++) t.mask |= (1ULL << t.names[k]);
        }
        for (auto& c : V[v].cand) { int h5[5]; fread(h5, 4, 5, f); c.ti = h5[0]; c.canon = h5[1]; c.u0 = h5[2]; c.u1 = h5[3]; c.u2 = h5[4]; c.nz = (c.u0 || c.u1 || c.u2); }
        totc += V[v].cand.size();
    }
    fclose(f);
    vector<vector<int>> dom(NV);
    for (int v = 0; v < NV; v++) { dom[v].resize(V[v].cand.size()); for (size_t c = 0; c < V[v].cand.size(); c++) dom[v][c] = (int)c; }
    t0 = chrono::steady_clock::now();
    bool found = rec(dom, 0);
    double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("{\"rho\": %d, \"delta\": %d, \"x\": %d, \"real\": %d, \"rank_test\": %d, \"status\": \"%s\", \"candidates\": %zu, "
           "\"nodes\": %lld, \"leaves\": %lld, \"match_rejects\": %lld, \"psd_leaf_rejects\": %lld, \"rank_rejects\": %lld, "
           "\"min_lam2\": %.3e, \"real_cuts\": %lld, \"depth1\": \"%lld/%lld\", \"seconds\": %.1f",
           rho, delta_, X, (int)REAL, (int)RANK, found ? "SAT" : (tflag ? "TIMEOUT" : "UNSAT"), totc, nodes, leaves,
           match_rejects, psd_leaf_rejects, rank_rejects, min_lam2 < 1e29 ? min_lam2 : -1.0, real_cuts, d1_done, d1_total, el);
    if (found) {
        printf(", \"solution\": [");
        for (int v = 0; v < NV; v++) {
            const Tri& t = TR(v, ch[v]); const Cand& c = V[v].cand[ch[v]];
            printf("%s[%d,%d,%d,%d,%d,%d,%d,%d,%d]", v ? "," : "", t.names[0], t.names[1], t.names[2], t.names[3], t.names[4], t.names[5], c.u0, c.u1, c.u2);
        }
        printf("]");
    }
    printf("}\n");
    return 0;
}
