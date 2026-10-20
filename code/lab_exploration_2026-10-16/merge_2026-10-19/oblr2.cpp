// 7-adic line obligation with a far residue of rank rho (LAB 19/10/2026).  Input: binary file from oblr_prep.py.
// One far vertex per p-pair; a candidate is (name triple, u in F_7^rho).  For two far vertices a, b the adjacency is
// FORCED mod 7: R(a,b) = beta(a,b) + u_a^T D u_b, beta(a,b) = sum over the names of b of Y_a (Y_a = X e_a), and must be
// 0 or 1.  Exact conditions used (all necessary in a srg(99,14,1,2) whose rank_7(A - 3I) gives this rho):
//   distinct q- and s-pairs (bijections); at most 2 shared names (L3); at most 1 shared name if adjacent (lambda);
//   margins: far common neighbours of near u, v never exceed K(u,v), and equal K at the end (L1);
//   far degree <= 8, = 8 at the end;
//   near-far counts: for near x and far w, #{far neighbours of w adjacent to x} <= 2 - [x in w] - |N_G(x) n w| (= at end);
//   far-far counts: common far neighbours of far w, w' <= (1 if adjacent else 2) - shared names (= at the end).
// Symmetry: while every assigned u is 0, only the canonical representative of each O(D)-orbit is tried.
// Prints REFUTED / FOUND / TIMEOUT (one JSON line); FOUND also prints the choices for an independent check.
// oblr2: forward checking re-runs every exact check on every open candidate after each commitment.
// usage: oblr2 <file.bin> <seconds>
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <chrono>
using namespace std;

static int n, m, rho, delta_, gorder, NN;
static int nbr[36][3];
static int K[36][36];
struct Tri { int names[6]; int qi, si; uint8_t Y[36]; uint8_t inw[36]; };
struct Cand { int ti; int canon; int u[8]; bool unz; };
static vector<vector<Tri>> tri;
static vector<vector<Cand>> cand;
static int D[8];
static long long nodes = 0; static int maxdepth = 0; static bool tflag = false;
static chrono::steady_clock::time_point t0; static double limit_s;
// state
static int choice[64]; static bool assigned[64]; static int nadj[64];
static int marg[36][36];             // far common neighbours counted so far, for near u < v in different classes
static int cntER[64][36];            // for assigned far w: number of assigned far neighbours of w adjacent to near x
static int target[64][36];           // per assigned far w (set at assignment)
static int cf[64][64];               // common far neighbours counted so far
static int adjv[64][64];             // adjacency between assigned far vertices
static int sharev[64][64];
static bool anynz = false;
static int nassigned = 0;

static inline const Tri& T(int p, int a) { return tri[p][cand[p][a].ti]; }
static inline int val(int p, int a, int q, int b) {
    const Tri& ta = T(p, a); const Tri& tb = T(q, b);
    int s = 0;
    for (int k = 0; k < 6; k++) s += ta.Y[tb.names[k]];
    const Cand& ca = cand[p][a]; const Cand& cb = cand[q][b];
    for (int i = 0; i < rho; i++) s += D[i] * ca.u[i] * cb.u[i];
    return s % 7;
}
static inline int share(int p, int a, int q, int b) {
    const Tri& ta = T(p, a); const Tri& tb = T(q, b);
    int s = 0;
    for (int k = 0; k < 6; k++) s += ta.inw[tb.names[k]];
    return s;
}
static inline bool margins_ok(int p, int a) {
    const Tri& t = T(p, a);
    for (int i = 0; i < 6; i++) for (int j = i + 1; j < 6; j++) {
        int x = t.names[i], y = t.names[j];
        if (x / n == y / n) continue;
        if (marg[x][y] + 1 > K[x][y]) return false;
    }
    return true;
}
static void margins_add(int p, int a, int dlt) {
    const Tri& t = T(p, a);
    for (int i = 0; i < 6; i++) for (int j = i + 1; j < 6; j++) {
        int x = t.names[i], y = t.names[j];
        if (x / n == y / n) continue;
        marg[x][y] += dlt; marg[y][x] += dlt;
    }
}
static void set_target(int p, int a) {
    const Tri& t = T(p, a);
    for (int x = 0; x < NN; x++) {
        int g = 0;
        for (int k = 0; k < 3; k++) g += t.inw[nbr[x][k]];
        target[p][x] = 2 - t.inw[x] - g;
    }
}

// all checks of candidate a for p-pair p against the current partial assignment (used before committing a and,
// after every commitment, to filter every open domain: forward checking with the full set of exact conditions)
static int g_nbq[64], g_nnb, g_addER[36], g_cfa[64];
static bool ABL_M = false, ABL_L = false, ABL_A = false, ABL_D = false, ABL_E = false, ABL_C = false, ABL_Q = false;
static bool admissible(int p, int a) {
    if (!ABL_M && !margins_ok(p, a)) return false;
    const Tri& ta = T(p, a);
    g_nnb = 0;
    for (int q = 0; q < m; q++) if (assigned[q]) {
        int b = choice[q];
        const Tri& tb = T(q, b);
        if (!ABL_Q && (tb.qi == ta.qi || tb.si == ta.si)) return false;
        int s = share(p, a, q, b);
        if (!ABL_L && s > 2) return false;
        int v = val(p, a, q, b);
        if (v > 1) return false;
        if (v == 1) {
            if (!ABL_A && s > 1) return false;
            if (!ABL_D && nadj[q] + 1 > 8) return false;
            g_nbq[g_nnb++] = q;
        }
    }
    if (!ABL_D && g_nnb > 8) return false;
    set_target(p, a);
    for (int x = 0; x < NN; x++) g_addER[x] = 0;
    for (int i = 0; i < g_nnb; i++) {
        int q = g_nbq[i];
        const Tri& tq = T(q, choice[q]);
        if (!ABL_E) for (int k = 0; k < 6; k++) if (cntER[q][ta.names[k]] + 1 > target[q][ta.names[k]]) return false;
        for (int k = 0; k < 6; k++) g_addER[tq.names[k]]++;
    }
    if (!ABL_E) for (int x = 0; x < NN; x++) if (g_addER[x] > target[p][x]) return false;
    if (!ABL_C) for (int i = 0; i < g_nnb; i++) for (int j = i + 1; j < g_nnb; j++) {
        int q1 = g_nbq[i], q2 = g_nbq[j];
        if (cf[q1][q2] + 1 > (adjv[q1][q2] ? 1 : 2) - sharev[q1][q2]) return false;
    }
    for (int q = 0; q < m; q++) g_cfa[q] = 0;
    for (int i = 0; i < g_nnb; i++) { int q1 = g_nbq[i]; for (int q = 0; q < m; q++) if (assigned[q] && q != q1 && adjv[q][q1]) g_cfa[q]++; }
    if (!ABL_C) for (int q = 0; q < m; q++) if (assigned[q]) {
        int b = choice[q];
        int v = val(p, a, q, b);
        int s = share(p, a, q, b);
        if (g_cfa[q] > (v ? 1 : 2) - s) return false;
    }
    return true;
}

static bool rec(vector<vector<int>>& dom, int depth) {
    nodes++;
    if ((nodes & 255) == 0) {
        double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
        if (el > limit_s) { tflag = true; return false; }
    }
    if (depth > maxdepth) maxdepth = depth;
    if (nassigned == m) {
        if (!ABL_D) for (int p = 0; p < m; p++) if (nadj[p] != 8) return false;
        if (!ABL_M) for (int x = 0; x < NN; x++) for (int y = 0; y < NN; y++)
            if (x / n != y / n && marg[x][y] != K[x][y]) return false;
        if (!ABL_E) for (int p = 0; p < m; p++) for (int x = 0; x < NN; x++) if (cntER[p][x] != target[p][x]) return false;
        if (!ABL_C) for (int p = 0; p < m; p++) for (int q = p + 1; q < m; q++)
            if (cf[p][q] != (adjv[p][q] ? 1 : 2) - sharev[p][q]) return false;
        return true;
    }
    int best = -1; size_t bc = (size_t)-1;
    for (int p = 0; p < m; p++) if (!assigned[p] && dom[p].size() < bc) { bc = dom[p].size(); best = p; }
    if (bc == 0) return false;
    int p = best;
    vector<int> mydom = dom[p];
    for (int a : mydom) {
        const Cand& ca = cand[p][a];
        if (!anynz && !ca.canon) continue;
        if (!admissible(p, a)) continue;
        // commit a
        vector<int> nbq(g_nbq, g_nbq + g_nnb);
        int addER[36]; for (int x = 0; x < NN; x++) addER[x] = g_addER[x];
        int cfa[64]; for (int q = 0; q < m; q++) cfa[q] = g_cfa[q];
        const Tri& ta = T(p, a);
        bool prev_anynz = anynz;
        if (ca.unz) anynz = true;
        margins_add(p, a, 1);
        assigned[p] = true; choice[p] = a; nadj[p] = (int)nbq.size(); nassigned++;
        for (int x = 0; x < NN; x++) cntER[p][x] = addER[x];
        for (int q : nbq) { nadj[q]++; for (int k = 0; k < 6; k++) cntER[q][ta.names[k]]++; }
        for (int q = 0; q < m; q++) if (assigned[q] && q != p) {
            int b = choice[q];
            adjv[p][q] = adjv[q][p] = val(p, a, q, b);
            sharev[p][q] = sharev[q][p] = share(p, a, q, b);
        }
        for (size_t i = 0; i < nbq.size(); i++) for (size_t j = i + 1; j < nbq.size(); j++) {
            int q1 = nbq[i], q2 = nbq[j];
            cf[q1][q2]++; cf[q2][q1]++;
        }
        for (int q = 0; q < m; q++) if (assigned[q] && q != p) { cf[p][q] = cfa[q]; cf[q][p] = cfa[q]; }
        // forward checking: every open candidate must pass all checks against the new state
        vector<vector<int>> nd(m);
        bool dead = false;
        for (int q = 0; q < m && !dead; q++) if (!assigned[q]) {
            nd[q].reserve(dom[q].size());
            for (int b : dom[q]) {
                const Tri& tb = T(q, b);                      // cheap pairwise test against a first
                if (!ABL_Q && (tb.qi == ta.qi || tb.si == ta.si)) continue;
                int s = share(p, a, q, b);
                if (!ABL_L && s > 2) continue;
                int v = val(p, a, q, b);
                if (v > 1 || (!ABL_A && v == 1 && s > 1)) continue;
                if (admissible(q, b)) nd[q].push_back(b);
            }
            if (nd[q].empty()) dead = true;
        }
        bool found = false;
        if (!dead) found = rec(nd, depth + 1);
        if (found) return true;
        // undo
        for (int q = 0; q < m; q++) if (assigned[q] && q != p) { cf[p][q] = 0; cf[q][p] = 0; }
        for (size_t i = 0; i < nbq.size(); i++) for (size_t j = i + 1; j < nbq.size(); j++) {
            int q1 = nbq[i], q2 = nbq[j];
            cf[q1][q2]--; cf[q2][q1]--;
        }
        for (int q = 0; q < m; q++) if (assigned[q] && q != p) { adjv[p][q] = adjv[q][p] = 0; sharev[p][q] = sharev[q][p] = 0; }
        for (int q : nbq) { nadj[q]--; for (int k = 0; k < 6; k++) cntER[q][ta.names[k]]--; }
        for (int x = 0; x < NN; x++) cntER[p][x] = 0;
        assigned[p] = false; nadj[p] = 0; nassigned--;
        margins_add(p, a, -1);
        anynz = prev_anynz;
        if (tflag) return false;
    }
    return false;
}

int main(int argc, char** argv) {
    FILE* f = fopen(argv[1], "rb"); limit_s = atof(argv[2]);
    if (const char* ab = getenv("OBLR_ABL")) for (const char* c = ab; *c; c++) {
        if (*c == 'm') ABL_M = true; if (*c == 'l') ABL_L = true; if (*c == 'a') ABL_A = true;
        if (*c == 'd') ABL_D = true; if (*c == 'e') ABL_E = true; if (*c == 'c') ABL_C = true;
        if (*c == 'q') ABL_Q = true; }
    int hdr[5]; fread(hdr, 4, 5, f); n = hdr[0]; m = hdr[1]; rho = hdr[2]; delta_ = hdr[3]; gorder = hdr[4];
    NN = 3 * n;
    vector<int> nb(NN * 3); fread(nb.data(), 4, NN * 3, f);
    for (int x = 0; x < NN; x++) for (int k = 0; k < 3; k++) nbr[x][k] = nb[x * 3 + k];
    vector<int> Kall(NN * NN); fread(Kall.data(), 4, NN * NN, f);
    for (int x = 0; x < NN; x++) for (int y = 0; y < NN; y++) K[x][y] = Kall[x * NN + y];
    tri.resize(m); cand.resize(m);
    size_t totc = 0;
    for (int p = 0; p < m; p++) {
        int nt, ncnd; fread(&nt, 4, 1, f); fread(&ncnd, 4, 1, f);
        tri[p].resize(nt);
        for (int t = 0; t < nt; t++) {
            Tri& tr = tri[p][t];
            fread(tr.names, 4, 6, f); fread(&tr.qi, 4, 1, f); fread(&tr.si, 4, 1, f); fread(tr.Y, 1, NN, f);
            memset(tr.inw, 0, sizeof(tr.inw));
            for (int k = 0; k < 6; k++) tr.inw[tr.names[k]] = 1;
        }
        cand[p].resize(ncnd);
        for (int c = 0; c < ncnd; c++) {
            Cand& cd = cand[p][c];
            fread(&cd.ti, 4, 1, f); fread(&cd.canon, 4, 1, f);
            cd.unz = false;
            if (rho > 0) { fread(cd.u, 4, rho, f); for (int i = 0; i < rho; i++) if (cd.u[i]) cd.unz = true; }
        }
        totc += ncnd;
    }
    int Dbuf[8] = {0}; fread(Dbuf, 4, rho > 0 ? rho : 1, f);
    for (int i = 0; i < rho; i++) D[i] = Dbuf[i];
    fclose(f);
    vector<vector<int>> dom(m);
    for (int p = 0; p < m; p++) { dom[p].resize(cand[p].size()); for (size_t c = 0; c < cand[p].size(); c++) dom[p][c] = (int)c; }
    t0 = chrono::steady_clock::now();
    bool found = rec(dom, 0);
    double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("{\"ablated\": \"%s\", \"status\": \"%s\", \"rho\": %d, \"delta\": %d, \"candidates\": %zu, \"nodes\": %lld, \"max_depth\": %d, \"seconds\": %.2f",
           getenv("OBLR_ABL") ? getenv("OBLR_ABL") : "", found ? "FOUND" : (tflag ? "TIMEOUT" : "REFUTED"), rho, delta_, totc, nodes, maxdepth, el);
    if (found) { printf(", \"choice\": ["); for (int p = 0; p < m; p++) printf("%s%d", p ? "," : "", choice[p]); printf("]"); }
    printf("}\n");
    return 0;
}
