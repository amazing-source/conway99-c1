// Second, independent enumerator of root templates (LAB, 18/10/2026): pruning by EXACT LINEAR ALGEBRA, no union-find.
// Written separately from cle_templates.cpp (own graph list, own partition generator, own pruning, own output) so that
// the two programs cross-check each other on every k and every c_min.
//
// Template at a root v: J = graph of the non-grid pairs of the 7 root lines (no vertex of degree 1); for each root r a
// partition of its J-neighbours into blocks of size >= 2 (the components of G_{l_r}); c_r = (6 - deg_r) + #blocks.
// C = unoriented incidence (blocks x non-grid rectangles).  Every realisation has its vector rows in ker C, hence:
//   Z  : e_e in rowspace(C)                      -> v_e = 0, impossible (R_ee >= 4);
//   EQ : e_e - s e_f in rowspace(C), s = +-1, e, f two rectangles at one root r
//        - in different blocks of r              -> R_ef = s R_ee != 0, impossible (R_ef = 0 across components);
//        - in one block of size >= 3             -> s = +1: R_ef = R_ee > 0, impossible (R_ef <= 0 on a shared line);
//                                                   s = -1: the cut {e, f} of the block has weight 0, impossible (<= -2);
//   K  : dim ker C < max_r (6 - c_r)              -> impossible (rank R >= 6 - c_r, rank R <= dim ker C).
// Pruning: the rows of the roots chosen so far span a subspace of rowspace(C), so Z / EQ found on a partial assignment
// hold for every completion.  Arithmetic modulo p = 2^61 - 1; all minors of these {-1,0,1} matrices with rows of norm
// <= sqrt(6) are below 6^11 < p, so rank tests mod p are exact.
// Graph list: all labelled masks without a vertex of degree 1, kept iff minimal in their S7-orbit (brute force over
// the 5040 permutations).  Partitions: own generator, counts checked against A000296 (1, 0, 1, 1, 4, 11, 41).
// usage: cle_templates_la <c_min> <exact 0|1> <grids k or -1> [--graph g] [--fix0 a] [--out file]
//   output lines: "mask|blocks of root 0|...|blocks of root 6", blocks as digit strings separated by '.', e.g. "56.123"
//   (one line per surviving LABELLED template whose root-0 option index is fixed if --fix0; deduplication up to
//   Aut(J) is left to the comparator, which uses its own canonical form).
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <set>
#include <string>
#include <vector>
using namespace std;

static int PI_[21][2];
static int IDX[7][7];
static const uint64_t P = (1ULL << 61) - 1;
static inline uint64_t mulm(uint64_t a, uint64_t b) {
    unsigned __int128 r = (unsigned __int128)a * b;
    uint64_t s = (uint64_t)(r & P) + (uint64_t)(r >> 61);
    while (s >= P) s -= P;
    return s;
}
static inline uint64_t subm(uint64_t a, uint64_t b) { return a >= b ? a - b : a + P - b; }
static uint64_t powm(uint64_t a, uint64_t e) { uint64_t r = 1; while (e) { if (e & 1) r = mulm(r, a); a = mulm(a, a); e >>= 1; } return r; }

static uint32_t permute(uint32_t mask, const int* p) {
    uint32_t r = 0;
    for (int k = 0; k < 21; k++) if (mask >> k & 1) r |= 1u << IDX[p[PI_[k][0]]][p[PI_[k][1]]];
    return r;
}

// all partitions of items into blocks of size >= 2 (blocks as bitmasks over root labels)
static void parts_rec(const vector<int>& items, vector<int>& used, vector<uint32_t>& cur, vector<vector<uint32_t>>& out) {
    int first = -1;
    for (size_t i = 0; i < items.size(); i++) if (!used[i]) { first = (int)i; break; }
    if (first < 0) { out.push_back(cur); return; }
    used[first] = 1;
    vector<int> rest; for (size_t i = first + 1; i < items.size(); i++) if (!used[i]) rest.push_back((int)i);
    int R = (int)rest.size();
    for (uint32_t sub = 1; sub < (1u << R); sub++) {            // at least one mate for the first item
        uint32_t blk = 1u << items[first];
        for (int t = 0; t < R; t++) if (sub >> t & 1) { used[rest[t]] = 1; blk |= 1u << items[rest[t]]; }
        cur.push_back(blk);
        parts_rec(items, used, cur, out);
        cur.pop_back();
        for (int t = 0; t < R; t++) if (sub >> t & 1) used[rest[t]] = 0;
    }
    used[first] = 0;
}

struct Row { vector<uint64_t> v; int piv; };

int main(int argc, char** argv) {
    { int k = 0; for (int a = 0; a < 7; a++) for (int b = a + 1; b < 7; b++) { PI_[k][0] = a; PI_[k][1] = b; IDX[a][b] = IDX[b][a] = k; k++; } }
    if (argc < 4) { fprintf(stderr, "usage: cle_templates_la <c_min> <exact 0|1> <grids|-1> [--graph g] [--fix0 a] [--out f]\n"); return 2; }
    int cmin = atoi(argv[1]); bool exact = atoi(argv[2]) != 0; int grids = atoi(argv[3]);
    int graph_only = -1, fix0 = -1, fix1 = -1; const char* outpath = nullptr; bool dedup = false, print_opts = false, partial_k = false; int estimate = 0;
    for (int a = 4; a < argc; a++) {
        if (!strcmp(argv[a], "--graph")) graph_only = atoi(argv[++a]);
        else if (!strcmp(argv[a], "--fix0")) fix0 = atoi(argv[++a]);
        else if (!strcmp(argv[a], "--fix1")) fix1 = atoi(argv[++a]);
        else if (!strcmp(argv[a], "--print-opts")) print_opts = true;
        else if (!strcmp(argv[a], "--pk")) partial_k = true;
        else if (!strcmp(argv[a], "--estimate")) estimate = atoi(argv[++a]);
        else if (!strcmp(argv[a], "--out")) outpath = argv[++a];
        else if (!strcmp(argv[a], "--dedup")) dedup = true;
    }
    // A000296 self-check of the partition generator
    { const int expect[7] = {1, 0, 1, 1, 4, 11, 41};
      for (int d = 0; d <= 6; d++) { vector<int> it(d), used(d, 0); for (int i = 0; i < d; i++) it[i] = i; vector<uint32_t> cur; vector<vector<uint32_t>> out; parts_rec(it, used, cur, out);
          if ((int)out.size() != expect[d]) { fprintf(stderr, "partition count %zu != A000296(%d)\n", out.size(), d); return 3; } } }
    // graph list: orbit minima (no vertex of degree 1), brute force over S7
    vector<array<int,7>> perms; { array<int,7> p; for (int i = 0; i < 7; i++) p[i] = i; do perms.push_back(p); while (next_permutation(p.begin(), p.end())); }
    vector<uint32_t> reps;
    for (uint32_t mask = 0; mask < (1u << 21); mask++) {
        if (grids >= 0 && __builtin_popcount(mask) != 21 - grids) continue;
        int deg[7] = {0}; for (int k = 0; k < 21; k++) if (mask >> k & 1) { deg[PI_[k][0]]++; deg[PI_[k][1]]++; }
        bool bad = false; for (int i = 0; i < 7; i++) if (deg[i] == 1) bad = true;
        if (bad) continue;
        bool minimal = true;
        for (auto& p : perms) if (permute(mask, p.data()) < mask) { minimal = false; break; }
        if (minimal) reps.push_back(mask);
    }
    FILE* out = outpath ? fopen(outpath, "w") : nullptr;
    long long nodes = 0, pruned_Z = 0, pruned_EQ = 0, pruned_K = 0, leaves = 0, rej_c = 0, rej_K = 0, survivors = 0;
    for (int g = 0; g < (int)reps.size(); g++) {
        if (graph_only >= 0 && g != graph_only) continue;
        uint32_t mask = reps[g];
        vector<int> lk; int link_of[7][7]; int m = 0;
        for (int k = 0; k < 21; k++) if (mask >> k & 1) { link_of[PI_[k][0]][PI_[k][1]] = link_of[PI_[k][1]][PI_[k][0]] = m++; }
        vector<int> nbrs[7];
        for (int r = 0; r < 7; r++) for (int j = 0; j < 7; j++) if (j != r && (mask >> IDX[r][j] & 1)) nbrs[r].push_back(j);
        vector<vector<vector<uint32_t>>> opts(7);
        vector<vector<int>> optc(7);
        for (int r = 0; r < 7; r++) {
            vector<int> used(nbrs[r].size(), 0); vector<uint32_t> cur; vector<vector<uint32_t>> all;
            parts_rec(nbrs[r], used, cur, all);
            for (auto& pt : all) { int c = 6 - (int)nbrs[r].size() + (int)pt.size(); if (c >= cmin) { opts[r].push_back(pt); optc[r].push_back(c); } }
        }
        bool empty = false; for (int r = 0; r < 7; r++) if (opts[r].empty()) empty = true;
        if (empty) continue;
        vector<array<int,7>> auts; for (auto& p : perms) if (permute(mask, p.data()) == mask) auts.push_back(p);
        vector<string> seen_keys;  // sorted later; small per graph
        std::set<string> seen;
        // root order: decreasing degree, ties by label
        array<int,7> ord; for (int i = 0; i < 7; i++) ord[i] = i;
        stable_sort(ord.begin(), ord.end(), [&](int x, int y) { return nbrs[x].size() > nbrs[y].size(); });
        if (print_opts) {
            printf("{\"graph\": %d, \"mask\": %u, \"order\": [", g, mask);
            for (int d = 0; d < 7; d++) printf("%s%d", d ? ", " : "", ord[d]);
            printf("]");
            for (int d = 0; d < 2; d++) {
                printf(", \"opts%d\": [", d);
                const vector<vector<uint32_t>>& L = opts[ord[d]];
                for (size_t oi = 0; oi < L.size(); oi++) {
                    printf("%s[", oi ? ", " : "");
                    for (size_t bi = 0; bi < L[oi].size(); bi++) { printf("%s[", bi ? ", " : ""); bool first = true; for (int j = 0; j < 7; j++) if (L[oi][bi] >> j & 1) { printf("%s%d", first ? "" : ", ", j); first = false; } printf("]"); }
                    printf("]");
                }
                printf("]");
            }
            printf("}\n");
            continue;
        }
        vector<vector<Row>> basis(8);             // basis[d] = RREF after depth d
        int choice[7]; int cval[7];
        // check Z and EQ for the roots chosen in ord[0..depth-1], with RREF B
        auto test = [&](const vector<Row>& B, int depth) -> char {
            int rank = (int)B.size();
            vector<char> isp(m, 0); for (auto& r : B) isp[r.piv] = 1;
            vector<int> freec; for (int c = 0; c < m; c++) if (!isp[c]) freec.push_back(c);
            int d = (int)freec.size();
            vector<vector<uint64_t>> K(m, vector<uint64_t>(d, 0));
            for (int t = 0; t < d; t++) { K[freec[t]][t] = 1; for (int i = 0; i < rank; i++) { uint64_t v = B[i].v[freec[t]]; K[B[i].piv][t] = v ? P - v : 0; } }
            for (int e = 0; e < m; e++) { bool z = true; for (int t = 0; t < d; t++) if (K[e][t]) { z = false; break; } if (z) return 'Z'; }
            for (int dd = 0; dd < depth; dd++) {
                int r = ord[dd]; const vector<uint32_t>& pt = opts[r][choice[dd]];
                vector<pair<int,int>> at;
                for (int bi = 0; bi < (int)pt.size(); bi++) for (int j = 0; j < 7; j++) if (pt[bi] >> j & 1) at.push_back({link_of[r][j], bi});
                for (size_t x = 0; x < at.size(); x++) for (size_t y = x + 1; y < at.size(); y++) {
                    bool plus = true, minus = true;
                    for (int t = 0; t < d && (plus || minus); t++) {
                        uint64_t a = K[at[x].first][t], b = K[at[y].first][t];
                        if (a != b) plus = false;
                        if (a != (b ? P - b : 0)) minus = false;
                    }
                    if (!plus && !minus) continue;
                    if (at[x].second != at[y].second) return 'E';
                    if (__builtin_popcount(pt[at[x].second]) >= 3) return 'E';
                }
            }
            return 0;
        };
        auto add_rows = [&](vector<Row> B, int r, const vector<uint32_t>& pt) {
            for (uint32_t blk : pt) {
                vector<uint64_t> v(m, 0);
                for (int j = 0; j < 7; j++) if (blk >> j & 1) v[link_of[r][j]] = 1;
                for (auto& row : B) if (v[row.piv]) { uint64_t f = v[row.piv]; for (int c = 0; c < m; c++) if (row.v[c]) v[c] = subm(v[c], mulm(f, row.v[c])); }
                int piv = -1; for (int c = 0; c < m; c++) if (v[c]) { piv = c; break; }
                if (piv < 0) continue;
                uint64_t inv = powm(v[piv], P - 2);
                for (int c = 0; c < m; c++) v[c] = mulm(v[c], inv);
                for (auto& row : B) if (row.v[piv]) { uint64_t f = row.v[piv]; for (int c = 0; c < m; c++) if (v[c]) row.v[c] = subm(row.v[c], mulm(f, v[c])); }
                B.push_back({v, piv});
            }
            return B;
        };
        if (estimate > 0) {        // Knuth's unbiased estimator of the search tree (random probes, fixed seed)
            unsigned long long rng = 88172645463325252ULL ^ (unsigned long long)mask;
            auto rnd = [&]() { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; };
            double sum_leaves = 0, sum_surv = 0, sum_nodes = 0, sum_surv2 = 0;
            for (int pr = 0; pr < estimate; pr++) {
                double w = 1; vector<Row> B; double surv = 0;
                for (int d = 0; d < 7; d++) {
                    int r = ord[d]; vector<int> ok; vector<vector<Row>> nb;
                    for (int o = 0; o < (int)opts[r].size(); o++) {
                        if (d == 0 && fix0 >= 0 && o != fix0) continue;
                        if (d == 1 && fix1 >= 0 && o != fix1) continue;
                        choice[d] = o; cval[d] = optc[r][o];
                        vector<Row> B2 = add_rows(B, r, opts[r][o]);
                        char why = test(B2, d + 1);
                        if (!why && partial_k) { int np = 0; for (int dd = 0; dd <= d; dd++) np = max(np, 6 - cval[dd]); if (m - (int)B2.size() < np) why = 'K'; }
                        if (!why) { ok.push_back(o); nb.push_back(B2); }
                    }
                    sum_nodes += w * ok.size();
                    if (ok.empty()) { w = 0; break; }
                    int pick = (int)(rnd() % ok.size());
                    choice[d] = ok[pick]; cval[d] = optc[r][ok[pick]]; B = nb[pick]; w *= ok.size();
                }
                if (w == 0) continue;
                sum_leaves += w;
                bool has = false; int need = 0;
                for (int dd = 0; dd < 7; dd++) { if (cval[dd] == cmin) has = true; need = max(need, 6 - cval[dd]); }
                if ((!exact || has) && m - (int)B.size() >= need) { surv = w; sum_surv += w; sum_surv2 += w * w; }
            }
            double n = estimate, mean = sum_surv / n, var = sum_surv2 / n - mean * mean;
            printf("{\"graph\": %d, \"probes\": %d, \"est_nodes\": %.4g, \"est_leaves\": %.4g, \"est_survivors_labelled\": %.4g, \"rel_stderr\": %.3g}\n",
                   g, estimate, sum_nodes / n, sum_leaves / n, mean, mean > 0 ? sqrt(var / n) / mean : 0.0);
            continue;
        }
        // iterative DFS over depths
        vector<int> it(8, -1); int depth = 0; basis[0].clear();
        while (depth >= 0) {
            int r = ord[depth];
            it[depth]++;
            if (depth == 0 && fix0 >= 0) { if (it[0] > fix0) { depth--; continue; } if (it[0] < fix0) it[0] = fix0; }
            if (depth == 1 && fix1 >= 0) { if (it[1] > fix1) { it[1] = -1; depth--; continue; } if (it[1] < fix1) it[1] = fix1; }
            if (it[depth] >= (int)opts[r].size()) { it[depth] = -1; depth--; continue; }
            choice[depth] = it[depth]; cval[depth] = optc[r][it[depth]];
            nodes++;
            basis[depth + 1] = add_rows(basis[depth], r, opts[r][it[depth]]);
            char why = test(basis[depth + 1], depth + 1);
            // --pk: ker C (all roots) is a subspace of ker C (roots chosen so far), so if the latter is already
            // smaller than 6 - c_r for a chosen root r, the rank condition K fails for every completion.
            if (!why && partial_k) {
                int need_p = 0; for (int dd = 0; dd <= depth; dd++) need_p = max(need_p, 6 - cval[dd]);
                if (m - (int)basis[depth + 1].size() < need_p) why = 'K';
            }
            if (why) { if (why == 'Z') pruned_Z++; else if (why == 'K') pruned_K++; else pruned_EQ++; continue; }
            if (depth + 1 < 7) { depth++; it[depth] = -1; continue; }
            leaves++;
            bool has = false; int need = 0;
            for (int dd = 0; dd < 7; dd++) { if (cval[dd] == cmin) has = true; need = max(need, 6 - cval[dd]); }
            if (exact && !has) { rej_c++; continue; }
            int dimker = m - (int)basis[7].size();
            if (dimker < need) { rej_K++; continue; }
            if (dedup) {
                string best;
                for (auto& p : auts) {
                    string k(21, char(0));
                    for (int dd = 0; dd < 7; dd++) {
                        int rr = ord[dd]; unsigned char b3[3] = {0, 0, 0}; int nb = 0;
                        for (uint32_t blk : opts[rr][choice[dd]]) { unsigned char mb = 0; for (int j = 0; j < 7; j++) if (blk >> j & 1) mb |= (unsigned char)(1u << p[j]); b3[nb++] = mb; }
                        sort(b3, b3 + 3);
                        for (int x = 0; x < 3; x++) k[p[rr] * 3 + x] = (char)b3[x];
                    }
                    if (best.empty() || k < best) best = k;
                }
                if (!seen.insert(best).second) continue;
            }
            survivors++;
            if (out) {
                string s = to_string(mask);
                vector<string> per(7);
                for (int dd = 0; dd < 7; dd++) {
                    int rr = ord[dd]; string b;
                    for (uint32_t blk : opts[rr][choice[dd]]) { if (!b.empty()) b += '.'; for (int j = 0; j < 7; j++) if (blk >> j & 1) b += char('0' + j); }
                    per[rr] = b;
                }
                for (int rr = 0; rr < 7; rr++) { s += '|'; s += per[rr]; }
                fprintf(out, "%s\n", s.c_str());
            }
        }
    }
    if (out) fclose(out);
    printf("{\"c_min\": %d, \"exact\": %s, \"grids\": %d, \"graph\": %d, \"fix0\": %d, \"graphs\": %zu, \"nodes\": %lld, \"pruned_Z\": %lld, \"pruned_EQ\": %lld, \"pruned_K\": %lld, \"leaves\": %lld, \"rejected_exact\": %lld, \"rejected_K\": %lld, \"survivors_labelled\": %lld}\n",
           cmin, exact ? "true" : "false", grids, graph_only, fix0, reps.size(), nodes, pruned_Z, pruned_EQ, pruned_K, leaves, rej_c, rej_K, survivors);
    return 0;
}
