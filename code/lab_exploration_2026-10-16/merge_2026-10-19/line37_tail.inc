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
