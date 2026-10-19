// Rank-37 obligation search for one generic line (LAB 19/10/2026).  Input: binary file from obl37_prep.py.
// Variables: the 60 p-pairs (far vertices); domain = candidate triples (bitsets).  Choosing a candidate filters every
// other domain by the compatibility bitsets (forced adjacency in {0,1}, distinct q/s pairs, L3), checks the margins
// K (counts never exceed K, and at the end equal K), keeps the number of forced far neighbours of every assigned far
// vertex <= 8, and at the end requires exactly 8.  Prints REFUTED / FOUND / TIMEOUT with node counts.
// usage: obl37 <file.bin> <seconds>
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <array>
#include <chrono>
using namespace std;
static int n, m, W, WORDS;
static vector<int> sz;
static vector<vector<array<int,6>>> names;
static int K01[12][12], K02[12][12], K12[12][12];
static vector<uint64_t> compat, adjb;            // [p][p2][i][words]
static inline uint64_t* C(int p, int p2, int i) { return &compat[(((size_t)p * m + p2) * W + i) * WORDS]; }
static inline uint64_t* Aj(int p, int p2, int i) { return &adjb[(((size_t)p * m + p2) * W + i) * WORDS]; }
static long long nodes = 0; static int maxdepth = 0;
static chrono::steady_clock::time_point t0; static double limit;
static int c01[12][12], c02[12][12], c12[12][12];
static int choice[64]; static bool assigned[64]; static int nadj[64];
static bool timeout_flag = false;
static int popc(const uint64_t* b) { int s = 0; for (int w = 0; w < WORDS; w++) s += __builtin_popcountll(b[w]); return s; }
static bool rec(vector<uint64_t>& dom, int depth) {
    nodes++;
    if ((nodes & 1023) == 0) {
        double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
        if (el > limit) { timeout_flag = true; return false; }
    }
    if (depth > maxdepth) maxdepth = depth;
    if (depth == m) {
        for (int p = 0; p < m; p++) if (nadj[p] != 8) return false;
        for (int a = 0; a < n; a++) for (int b = 0; b < n; b++)
            if (c01[a][b] != K01[a][b] || c02[a][b] != K02[a][b] || c12[a][b] != K12[a][b]) return false;
        return true;
    }
    int best = -1, bc = 1 << 30;
    for (int p = 0; p < m; p++) if (!assigned[p]) { int c = popc(&dom[(size_t)p * WORDS]); if (c < bc) { bc = c; best = p; } }
    if (bc == 0) return false;
    int p = best;
    uint64_t* dp = &dom[(size_t)p * WORDS];
    for (int i = 0; i < sz[p]; i++) {
        if (!((dp[i >> 6] >> (i & 63)) & 1)) continue;
        const auto& nm = names[p][i];       // names: 2 in class 0 (0..11), 2 in class 1 (12..23), 2 in class 2 (24..35)
        int u0 = nm[0], u1 = nm[1], v0 = nm[2] - n, v1 = nm[3] - n, w0 = nm[4] - 2 * n, w1 = nm[5] - 2 * n;
        int us[2] = {u0, u1}, vs[2] = {v0, v1}, ws[2] = {w0, w1};
        bool ok = true;
        for (int a = 0; a < 2 && ok; a++) for (int b = 0; b < 2 && ok; b++) {
            if (c01[us[a]][vs[b]] + 1 > K01[us[a]][vs[b]]) ok = false;
            if (c02[us[a]][ws[b]] + 1 > K02[us[a]][ws[b]]) ok = false;
            if (c12[vs[a]][ws[b]] + 1 > K12[vs[a]][ws[b]]) ok = false;
        }
        if (!ok) continue;
        // forced adjacency with already assigned far vertices: degree caps
        int deg = 0; bool okd = true;
        for (int q = 0; q < m && okd; q++) if (assigned[q]) {
            int j = choice[q];
            if ((Aj(q, p, j)[i >> 6] >> (i & 63)) & 1) { deg++; if (nadj[q] + 1 > 8) okd = false; }
        }
        if (!okd || deg > 8) continue;
        vector<uint64_t> nd(dom);
        bool dead = false;
        for (int q = 0; q < m; q++) if (!assigned[q] && q != p) {
            uint64_t* dq = &nd[(size_t)q * WORDS]; const uint64_t* cc = C(p, q, i);
            uint64_t any = 0;
            for (int w = 0; w < WORDS; w++) { dq[w] &= cc[w]; any |= dq[w]; }
            if (!any) { dead = true; break; }
        }
        if (dead) continue;
        for (int a = 0; a < 2; a++) for (int b = 0; b < 2; b++) { c01[us[a]][vs[b]]++; c02[us[a]][ws[b]]++; c12[vs[a]][ws[b]]++; }
        for (int q = 0; q < m; q++) if (assigned[q] && ((Aj(q, p, choice[q])[i >> 6] >> (i & 63)) & 1)) nadj[q]++;
        assigned[p] = true; choice[p] = i; nadj[p] = deg;
        if (rec(nd, depth + 1)) return true;
        assigned[p] = false;
        for (int q = 0; q < m; q++) if (assigned[q] && ((Aj(q, p, choice[q])[i >> 6] >> (i & 63)) & 1)) nadj[q]--;
        for (int a = 0; a < 2; a++) for (int b = 0; b < 2; b++) { c01[us[a]][vs[b]]--; c02[us[a]][ws[b]]--; c12[vs[a]][ws[b]]--; }
        if (timeout_flag) return false;
    }
    return false;
}
int main(int argc, char** argv) {
    FILE* f = fopen(argv[1], "rb"); limit = atof(argv[2]);
    int hdr[4]; fread(hdr, 4, 4, f); n = hdr[0]; m = hdr[1]; W = hdr[2]; WORDS = hdr[3];
    sz.resize(m); fread(sz.data(), 4, m, f);
    names.resize(m);
    for (int p = 0; p < m; p++) { names[p].resize(sz[p]); for (int i = 0; i < sz[p]; i++) fread(names[p][i].data(), 4, 6, f); }
    vector<int> Kall(3 * n * n); fread(Kall.data(), 4, 3 * n * n, f);
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) { K01[a][b] = Kall[a * n + b]; K02[a][b] = Kall[n * n + a * n + b]; K12[a][b] = Kall[2 * n * n + a * n + b]; }
    compat.assign((size_t)m * m * W * WORDS, 0); adjb.assign((size_t)m * m * W * WORDS, 0);
    for (int p = 0; p < m; p++) for (int q = 0; q < m; q++) {
        if (q == p) continue;
        for (int i = 0; i < sz[p]; i++) fread(C(p, q, i), 8, WORDS, f);
        for (int i = sz[p]; i < W; i++) {}
        // rows beyond sz[p] were not written: the prep writes exactly sz[p] rows per matrix
        for (int i = 0; i < sz[p]; i++) fread(Aj(p, q, i), 8, WORDS, f);
    }
    fclose(f);
    vector<uint64_t> dom((size_t)m * WORDS, 0);
    for (int p = 0; p < m; p++) for (int i = 0; i < sz[p]; i++) dom[(size_t)p * WORDS + (i >> 6)] |= 1ULL << (i & 63);
    t0 = chrono::steady_clock::now();
    bool found = rec(dom, 0);
    double el = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    printf("{\"status\": \"%s\", \"nodes\": %lld, \"max_depth\": %d, \"seconds\": %.2f}\n",
           found ? "FOUND" : (timeout_flag ? "TIMEOUT" : "REFUTED"), nodes, maxdepth, el);
    return 0;
}
