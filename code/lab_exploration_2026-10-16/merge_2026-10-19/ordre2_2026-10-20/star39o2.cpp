// star39o2: star39.cpp (LAB 20/10/2026) instrumented for NOTE_ORDRE2_7ADIQUE (LAB, 20/10/2026 evening).
// Same input (star39_prep.py / star_prep_gen.py .bin), same search and same exact conditions as star39, plus options:
//   STAR_P3=1     second real far projector, every rank: H3 = 7 Pi^(3) = 4I + R - 2J/35 - E^T (4I + G)^{-1} E is PSD on
//                 the assigned block (incremental Cholesky, own degeneracy flag).  Pi^(3) = projector onto the
//                 3-eigenvectors of A carried by the far set (rank 18 for c = 1); H + H3 = 7 (I - E^T K^+ E).
//   STAR_NO7=1    drop the test "7I - H PSD" of star39 (it is implied by H3 PSD, and measured vacuous).
//   STAR_R9=1     exact real rank at depth 9 (c = 1 only): once 8 assigned vectors are independent (no H pivot < 1e-7),
//                 every further candidate must have its H Schur pivot |piv| <= 1e-6 (rank Pi^(-4) = 8).
//   STAR_D1MAX=n  stop after n depth-1 branches (prefix comparison of variants on the same branches).
//   STAR_DUMP8=f  write every node with exactly 8 assigned far vertices to file f (one line: 8 x (var, names, u0, u1)),
//                 at most STAR_DUMP8MAX (default 100000) lines, for the square-class test (o2_sqclass.py).
// Output adds: nodes per depth, the counters of the new cuts.
// usage: star39o2 <file.bin> <seconds>
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

struct Tri { int names[6]; int qi, si, cap, h1, h2; uint8_t Y[36]; uint8_t nbc[36]; double zq[36]; double dd; uint64_t mask;
             double zq3[36]; double dd3; };
struct Cand { int ti, canon, u0, u1; bool nz; };
struct Var { int y; vector<Tri> tri; vector<Cand> cand; };

static int rho, delta_, X, B1, B2, NV;
static int nbr[36][3], Kx[36], Dq[2];
static vector<Var> V;
static bool REAL = true, RANK = true, P3 = false, USE7 = true, R9 = false;
static const double RTOL = 1e-9;
static long long D1MAX = -1;
static FILE* dump8 = nullptr; static long long dump8max = 100000, dump8n = 0;

static bool asg[16]; static int ch[16], deg[16];
static bool usedQ[64], usedS[64]; static int marg[36];
static bool anynz = false;
static int ord[16], nasg = 0;
static double Lc[16][16], Lc7[16][16], Lc3[16][16]; static int degenAt = -1, degen3At = -1;
static long long nodes = 0, leaves = 0, rank_rejects = 0, psd_leaf_rejects = 0, real_cuts = 0, match_rejects = 0;
static long long p3_cuts = 0, r9_cuts = 0, h_cuts = 0, h7_cuts = 0;
static long long depthCount[17];
static double min_lam2 = 1e30; static bool tflag = false, d1stop = false; static double limit_s;
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
static inline double h3val(int va, int ca, int vb, int cb, int R) {
    const Tri& ta = TR(va, ca); const Tri& tb = TR(vb, cb);
    double s = 0;
    for (int k = 0; k < 6; k++) s += ta.zq3[tb.names[k]];
    return R - 2.0 / 35.0 - s;
}
static bool psd_ok(int vb, int cb) {
    if (!REAL || nasg == 0) return true;
    bool doH = (degenAt < 0), do3 = (P3 && degen3At < 0);
    if (!doH && !do3) return true;
    double y[16], y7[16], y3[16], s = 0, s7 = 0, s3 = 0;
    for (int i = 0; i < nasg; i++) {
        int va = ord[i], ca = ch[va];
        int R = Rval(va, ca, vb, cb);
        if (doH) {
            double h = hval(va, ca, vb, cb, R);
            double t = h, t7 = -h;
            for (int j = 0; j < i; j++) { t -= Lc[i][j] * y[j]; if (USE7) t7 -= Lc7[i][j] * y7[j]; }
            y[i] = t / Lc[i][i]; s += y[i] * y[i];
            if (USE7) { y7[i] = t7 / Lc7[i][i]; s7 += y7[i] * y7[i]; }
        }
        if (do3) {
            double t3 = h3val(va, ca, vb, cb, R);
            for (int j = 0; j < i; j++) t3 -= Lc3[i][j] * y3[j];
            y3[i] = t3 / Lc3[i][i]; s3 += y3[i] * y3[i];
        }
    }
    if (doH) {
        double d = TR(vb, cb).dd;
        if (d - s < -RTOL) { real_cuts++; h_cuts++; return false; }
        if (USE7 && (7.0 - d) - s7 < -RTOL) { real_cuts++; h7_cuts++; return false; }
        if (R9 && nasg >= 8 && fabs(d - s) > 1e-6) { r9_cuts++; return false; }
    }
    if (do3) {
        double d3 = TR(vb, cb).dd3;
        if (d3 - s3 < -RTOL) { p3_cuts++; return false; }
    }
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
    if (REAL && P3 && degen3At < 0) {
        double s3 = 0;
        for (int i = 0; i < n; i++) {
            int va = ord[i];
            int R = Rval(va, ch[va], v, ch[v]);
            double t3 = h3val(va, ch[va], v, ch[v], R);
            for (int j = 0; j < i; j++) t3 -= Lc3[n][j] * Lc3[i][j];
            Lc3[n][i] = t3 / Lc3[i][i];
            s3 += Lc3[n][i] * Lc3[n][i];
        }
        double piv3 = TR(v, ch[v]).dd3 - s3;
        if (piv3 < 1e-7) degen3At = n; else Lc3[n][n] = sqrt(piv3);
    }
    nasg++;
}
static void chol_pop() { nasg--; if (degenAt == nasg) degenAt = -1; if (degen3At == nasg) degen3At = -1; }

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
            for (int k = 0; k < n; k++) { double akp = a[k][p], akq = a[k][q]; a[k][p] = c * akp - s * akq; a[k][q] = s * akp + c * akq; }
            for (int k = 0; k < n; k++) { double apk = a[p][k], aqk = a[q][k]; a[p][k] = c * apk - s * aqk; a[q][k] = s * apk + c * aqk; }
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
        if (P3) {
            for (int i = 0; i < NV; i++) for (int j = 0; j < NV; j++) {
                if (i == j) H[i][j] = TR(i, ch[i]).dd3;
                else { int R = Rval(i, ch[i], j, ch[j]); H[i][j] = h3val(i, ch[i], j, ch[j], R); }
            }
            jacobi_eig(NV, H, ev);
            if (ev[0] < -1e-7) { psd_leaf_rejects++; return false; }
        }
    }
    return true;
}

static void do_dump8() {
    if (!dump8 || dump8n >= dump8max) return;
    dump8n++;
    for (int i = 0; i < nasg; i++) {
        int v = ord[i]; const Tri& t = TR(v, ch[v]); const Cand& c = V[v].cand[ch[v]];
        fprintf(dump8, "%s%d:%d,%d,%d,%d,%d,%d:%d,%d", i ? " " : "", v, t.names[0], t.names[1], t.names[2], t.names[3], t.names[4], t.names[5], c.u0, c.u1);
    }
    fprintf(dump8, "\n");
}

static bool rec(vector<vector<int>>& dom, int depth) {
    nodes++;
    depthCount[nasg]++;
    if (nasg == 8) do_dump8();
    if ((nodes & 1023) == 0) {
        double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
        if (el > limit_s) { tflag = true; return false; }
        static double last = 0;
        if (el - last > 60) { last = el; fprintf(stderr, "[%.0fs] nodes %lld, depth-1 branch %lld/%lld, leaves %lld\n", el, nodes, d1_done, d1_total, leaves); }
    }
    if (nasg == NV) return leaf_ok();
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
        if (depth == 0) { if (D1MAX >= 0 && d1_done >= D1MAX) { d1stop = true; return false; } d1_done++; }
        const Cand& cd = V[v].cand[c];
        if (!anynz && cd.nz && !cd.canon) continue;
        int partners[16], np = 0; bool ok = true;
        for (int i = 0; i < nasg; i++) {
            int w = ord[i];
            if (Rval(w, ch[w], v, c) == 1) {
                if (deg[w] >= TR(w, ch[w]).cap) { ok = false; break; }
                partners[np++] = w;
            }
        }
        if (!ok || np > TR(v, c).cap) continue;
        const Tri& t = TR(v, c);
        asg[v] = true; ch[v] = c; deg[v] = np;
        for (int i = 0; i < np; i++) deg[partners[i]]++;
        usedQ[t.qi] = usedS[t.si] = true;
        for (int k = 2; k < 6; k++) marg[t.names[k]]++;
        bool prev_nz = anynz; if (cd.nz) anynz = true;
        chol_push(v);
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
        chol_pop();
        anynz = prev_nz;
        for (int k = 2; k < 6; k++) marg[t.names[k]]--;
        usedQ[t.qi] = usedS[t.si] = false;
        for (int i = 0; i < np; i++) deg[partners[i]]--;
        deg[v] = 0; asg[v] = false;
        if (tflag || d1stop) return false;
    }
    return false;
}

static void inv36(double M[36][36], double Out[36][36]) {
    double a[36][72];
    for (int i = 0; i < 36; i++) { for (int j = 0; j < 36; j++) { a[i][j] = M[i][j]; a[i][36 + j] = (i == j); } }
    for (int c = 0; c < 36; c++) {
        int p = c; for (int r = c + 1; r < 36; r++) if (fabs(a[r][c]) > fabs(a[p][c])) p = r;
        for (int j = 0; j < 72; j++) swap(a[c][j], a[p][j]);
        double iv = 1.0 / a[c][c];
        for (int j = 0; j < 72; j++) a[c][j] *= iv;
        for (int r = 0; r < 36; r++) if (r != c && a[r][c] != 0) { double f = a[r][c]; for (int j = 0; j < 72; j++) a[r][j] -= f * a[c][j]; }
    }
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) Out[i][j] = a[i][36 + j];
}

int main(int argc, char** argv) {
#ifdef _WIN32
    SetPriorityClass(GetCurrentProcess(), IDLE_PRIORITY_CLASS);
#endif
    if (argc < 3) { fprintf(stderr, "usage: star39o2 <file.bin> <seconds>\n"); return 1; }
    FILE* f = fopen(argv[1], "rb"); limit_s = atof(argv[2]);
    if (!f) { fprintf(stderr, "cannot open %s\n", argv[1]); return 1; }
    if (getenv("STAR_NOREAL")) REAL = false;
    if (getenv("STAR_NORANK")) RANK = false;
    if (getenv("STAR_P3")) P3 = true;
    if (getenv("STAR_NO7")) USE7 = false;
    if (getenv("STAR_R9")) R9 = true;
    if (getenv("STAR_D1MAX")) D1MAX = atoll(getenv("STAR_D1MAX"));
    if (getenv("STAR_DUMP8")) { dump8 = fopen(getenv("STAR_DUMP8"), "w"); if (getenv("STAR_DUMP8MAX")) dump8max = atoll(getenv("STAR_DUMP8MAX")); }
    int hdr[6]; fread(hdr, 4, 6, f); rho = hdr[0]; delta_ = hdr[1]; X = hdr[2]; B1 = hdr[3]; B2 = hdr[4]; NV = hdr[5];
    vector<int> nb(108); fread(nb.data(), 4, 108, f);
    for (int v = 0; v < 36; v++) for (int k = 0; k < 3; k++) nbr[v][k] = nb[v * 3 + k];
    fread(Kx, 4, 36, f); fread(Dq, 4, 2, f);
    // Z3 = (4I + G)^{-1}
    static double M4[36][36], Z3[36][36];
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) M4[i][j] = (i == j) ? 4.0 : 0.0;
    for (int v = 0; v < 36; v++) for (int k = 0; k < 3; k++) M4[v][nbr[v][k]] += 1.0;
    inv36(M4, Z3);
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
            double e3 = 0;
            for (int z = 0; z < 36; z++) { double s = 0; for (int k = 0; k < 6; k++) s += Z3[z][t.names[k]]; t.zq3[z] = s; }
            for (int k = 0; k < 6; k++) e3 += t.zq3[t.names[k]];
            t.dd3 = 4.0 - 2.0 / 35.0 - e3;
        }
        for (auto& c : V[v].cand) { int h4[4]; fread(h4, 4, 4, f); c.ti = h4[0]; c.canon = h4[1]; c.u0 = h4[2]; c.u1 = h4[3]; c.nz = (c.u0 || c.u1); }
        totc += V[v].cand.size();
    }
    fclose(f);
    // unary H3 filter (counted) when P3
    long long unary3 = 0;
    vector<vector<int>> dom(NV);
    for (int v = 0; v < NV; v++) {
        for (size_t c = 0; c < V[v].cand.size(); c++) {
            if (P3 && REAL && TR(v, (int)c).dd3 < -RTOL) { unary3++; continue; }
            dom[v].push_back((int)c);
        }
    }
    t0 = chrono::steady_clock::now();
    bool found = rec(dom, 0);
    double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("{\"rho\": %d, \"delta\": %d, \"x\": %d, \"real\": %d, \"rank_test\": %d, \"P3\": %d, \"use7\": %d, \"R9\": %d, \"status\": \"%s\", \"candidates\": %zu, "
           "\"unary_p3_cut\": %lld, \"nodes\": %lld, \"leaves\": %lld, \"match_rejects\": %lld, \"psd_leaf_rejects\": %lld, \"rank_rejects\": %lld, "
           "\"real_cuts\": %lld, \"h_cuts\": %lld, \"h7_cuts\": %lld, \"p3_cuts\": %lld, \"r9_cuts\": %lld, \"depth1\": \"%lld/%lld\", \"seconds\": %.1f, \"dump8\": %lld, \"by_depth\": [",
           rho, delta_, X, (int)REAL, (int)RANK, (int)P3, (int)USE7, (int)R9,
           found ? "SAT" : (tflag ? "TIMEOUT" : (d1stop ? "PREFIX" : "UNSAT")), totc, unary3, nodes, leaves,
           match_rejects, psd_leaf_rejects, rank_rejects, real_cuts, h_cuts, h7_cuts, p3_cuts, r9_cuts, d1_done, d1_total, el, dump8n);
    for (int d = 0; d <= NV; d++) printf("%s%lld", d ? ", " : "", depthCount[d]);
    printf("]");
    if (found) {
        printf(", \"solution\": [");
        for (int v = 0; v < NV; v++) {
            const Tri& t = TR(v, ch[v]); const Cand& c = V[v].cand[ch[v]];
            printf("%s[%d,%d,%d,%d,%d,%d,%d,%d]", v ? "," : "", t.names[0], t.names[1], t.names[2], t.names[3], t.names[4], t.names[5], c.u0, c.u1);
        }
        printf("]");
    }
    printf("}\n");
    if (dump8) fclose(dump8);
    return 0;
}
