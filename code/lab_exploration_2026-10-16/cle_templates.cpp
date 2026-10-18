// Root component templates of a srg(99,14,1,2) at a root, any c_min (LAB, 18/10/2026).
// Faithful C++ port of cle3_templates.py (same DFS order, same filters, same counters) so that the two
// implementations cross-check each other.  Filters (all proved, see cle3_templates.py):
//   P  a block of size 2 forces v_a = -v_b (signed union-find); an odd cycle rejects;
//   O' two links of one root in different blocks cannot be in one signed class;
//   S' two links in one block of size >= 3 cannot be in one signed class;
//   K  dim ker C >= max_i (6 - c_i);
//   Z  no link on which every vector of ker C vanishes.
// Survivors are deduplicated up to Aut(non-grid graph) by the same canonical encoding as the Python code.
// usage: cle_templates <c_min> <exact 0|1> <grids k or -1 for all> [--graph g] [--fix d0opt[,d1opt]] [--out file.jsonl]
//        prints one JSON summary line; survivors (one JSON object per line) go to --out.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <map>
#include <set>
#include <string>
#include <vector>
using namespace std;

static array<pair<int,int>,21> EDGES;
static int EIDX[7][7];

static uint32_t relabel(uint32_t mask, const array<int,7>& perm) {
    uint32_t r = 0;
    for (int k = 0; k < 21; k++) if (mask >> k & 1) {
        int a = perm[EDGES[k].first], b = perm[EDGES[k].second];
        if (a > b) swap(a, b);
        r |= 1u << EIDX[a][b];
    }
    return r;
}

static void degrees(uint32_t mask, array<int,7>& deg) {
    deg.fill(0);
    for (int k = 0; k < 21; k++) if (mask >> k & 1) { deg[EDGES[k].first]++; deg[EDGES[k].second]++; }
}

// all permutations that permute vertices inside groups of equal degree (degree groups listed by increasing degree)
static void group_perms(const array<int,7>& deg, vector<array<int,7>>& out) {
    vector<vector<int>> groups;
    vector<int> vals(deg.begin(), deg.end());
    sort(vals.begin(), vals.end()); vals.erase(unique(vals.begin(), vals.end()), vals.end());
    for (int v : vals) { vector<int> g; for (int i = 0; i < 7; i++) if (deg[i] == v) g.push_back(i); groups.push_back(g); }
    // product of permutations of each group (same order as itertools.product of permutations)
    vector<vector<vector<int>>> perms_by_group;
    for (auto& g : groups) {
        vector<vector<int>> ps; vector<int> t = g;
        sort(t.begin(), t.end());
        do { ps.push_back(t); } while (next_permutation(t.begin(), t.end()));
        perms_by_group.push_back(ps);
    }
    vector<size_t> idx(groups.size(), 0);
    while (true) {
        array<int,7> perm; for (int i = 0; i < 7; i++) perm[i] = i;
        for (size_t gi = 0; gi < groups.size(); gi++)
            for (size_t x = 0; x < groups[gi].size(); x++) perm[groups[gi][x]] = perms_by_group[gi][idx[gi]][x];
        out.push_back(perm);
        int gi = (int)groups.size() - 1;
        while (gi >= 0) { if (++idx[gi] < perms_by_group[gi].size()) break; idx[gi] = 0; gi--; }
        if (gi < 0) break;
    }
}

static vector<uint32_t> graph_reps() {
    vector<uint32_t> reps; vector<char> seen(1u << 21, 0);
    array<int,7> deg; deg.fill(0); uint32_t prev = 0;
    for (uint32_t index = 0; index < (1u << 21); index++) {
        uint32_t mask = index ^ (index >> 1);
        if (index) {
            uint32_t ch = mask ^ prev; int k = 31 - __builtin_clz(ch);
            int inc = (mask & ch) ? 1 : -1;
            deg[EDGES[k].first] += inc; deg[EDGES[k].second] += inc;
        }
        prev = mask;
        bool bad = false;
        for (int i = 0; i < 7; i++) if (deg[i] == 1) bad = true;
        for (int i = 0; i + 1 < 7; i++) if (deg[i] > deg[i+1]) bad = true;
        if (bad || seen[mask]) continue;
        vector<array<int,7>> ps; group_perms(deg, ps);
        uint32_t mn = UINT32_MAX;
        for (auto& p : ps) { uint32_t r = relabel(mask, p); seen[r] = 1; mn = min(mn, r); }
        reps.push_back(mn);
    }
    sort(reps.begin(), reps.end());
    return reps;
}

static vector<array<int,7>> automorphisms(uint32_t mask) {
    array<int,7> deg; degrees(mask, deg);
    vector<array<int,7>> ps, out; group_perms(deg, ps);
    for (auto& p : ps) if (relabel(mask, p) == mask) out.push_back(p);
    return out;
}

typedef vector<vector<int>> Partition;      // blocks, each sorted, block order as generated
static void set_partitions(const vector<int>& items, size_t from, vector<Partition>& out) {
    if (from == items.size()) { out.push_back(Partition()); return; }
    int first = items[from];
    vector<Partition> subs; set_partitions(items, from + 1, subs);
    for (auto& sub : subs) {
        for (size_t i = 0; i < sub.size(); i++) {
            Partition q;
            for (size_t j = 0; j < i; j++) q.push_back(sub[j]);
            vector<int> b; b.push_back(first); b.insert(b.end(), sub[i].begin(), sub[i].end()); q.push_back(b);
            for (size_t j = i + 1; j < sub.size(); j++) q.push_back(sub[j]);
            out.push_back(q);
        }
        Partition q; q.push_back(vector<int>{first}); q.insert(q.end(), sub.begin(), sub.end()); out.push_back(q);
    }
}
struct Option { Partition parts; int c; };
static vector<Option> admissible(const vector<int>& items, int kmin) {
    vector<Partition> all; set_partitions(items, 0, all);
    vector<Option> out;
    for (auto& P : all) {
        bool ok = true; for (auto& b : P) if (b.size() < 2) ok = false;
        if (!ok) continue;
        int c = 6 - (int)items.size() + (int)P.size();
        if (c < kmin) continue;
        Option o; o.c = c;
        for (auto b : P) { sort(b.begin(), b.end()); o.parts.push_back(b); }
        out.push_back(o);
    }
    return out;
}

struct UF {
    vector<int> p, s, log;
    void init(int n) { p.resize(n); s.assign(n, 1); for (int i = 0; i < n; i++) p[i] = i; log.clear(); }
    pair<int,int> find(int x) const { int sg = 1; while (p[x] != x) { sg *= s[x]; x = p[x]; } return {x, sg}; }
    bool relate_opposite(int a, int b) {
        auto A = find(a), Bb = find(b);
        if (A.first == Bb.first) return A.second == -Bb.second;
        p[Bb.first] = A.first; s[Bb.first] = -A.second * Bb.second; log.push_back(Bb.first); return true;
    }
    size_t mark() const { return log.size(); }
    void undo(size_t m) { while (log.size() > m) { int x = log.back(); log.pop_back(); p[x] = x; s[x] = 1; } }
};

static int nullity(int nv, const vector<pair<int,int>>& links, int omit) {
    // dim ker of the unoriented incidence = |E| - |V| + #bipartite components (isolated vertices count as bipartite)
    int adjn[32] = {0}, adj[32][32];
    for (int i = 0; i < (int)links.size(); i++) if (i != omit) {
        int a = links[i].first, b = links[i].second;
        adj[a][adjn[a]++] = b; adj[b][adjn[b]++] = a;
    }
    int col[32]; for (int v = 0; v < nv; v++) col[v] = -1;
    int bip = 0, st[64];
    for (int s0 = 0; s0 < nv; s0++) {
        if (col[s0] != -1) continue;
        col[s0] = 0; int sp = 0; st[sp++] = s0; bool ok = true;
        while (sp) { int a = st[--sp]; for (int x = 0; x < adjn[a]; x++) { int b = adj[a][x]; if (col[b] == -1) { col[b] = 1 - col[a]; st[sp++] = b; } else if (col[b] == col[a]) ok = false; } }
        bip += ok;
    }
    return (int)links.size() - (omit >= 0 ? 1 : 0) - nv + bip;
}

// --la (18/10, audit): exact linear-algebra filter on the representatives.  Every realisation has its vector rows in
// ker C, so if every x in ker C has x_e = s x_f (s = +-1) for two links e, f at one root, then v_e = s v_f:
//   e, f in different blocks of that root -> R_ef = s R_ee != 0, but R_ef = 0 across components of one line;
//   e, f in one block of size >= 3      -> s = +1 contradicts R_ef <= 0 < R_ee; s = -1 gives a cut of weight 0 > -2.
// Ranks are computed modulo p = 2^61 - 1.  C and [C; e_e - s e_f] have entries in {-1, 0, 1} and rows of norm
// <= sqrt(6), so every minor is below 6^11 < p in absolute value: a minor vanishes mod p iff it vanishes over Q,
// hence the mod-p kernel test is exact.  Cross-checked against cle3_filter_crosscheck.py (Fraction arithmetic).
static const uint64_t LA_P = (1ULL << 61) - 1;
static uint64_t la_mul(uint64_t a, uint64_t b) { unsigned __int128 r = (unsigned __int128)a * b; uint64_t lo = (uint64_t)(r & LA_P), hi = (uint64_t)(r >> 61); uint64_t s = lo + hi; if (s >= LA_P) s -= LA_P; if (s >= LA_P) s -= LA_P; return s; }
static uint64_t la_pow(uint64_t a, uint64_t e) { uint64_t r = 1; while (e) { if (e & 1) r = la_mul(r, a); a = la_mul(a, a); e >>= 1; } return r; }
static char la_check(int nv, const vector<pair<int,int>>& links, const Partition* const* choice, int eidx[7][7]) {
    int m = (int)links.size();
    vector<vector<uint64_t>> A(nv, vector<uint64_t>(m, 0));
    for (int i = 0; i < m; i++) { A[links[i].first][i] = 1; A[links[i].second][i] = 1; }
    vector<int> pivcol; int rank = 0;
    for (int col = 0; col < m && rank < nv; col++) {
        int piv = -1; for (int r = rank; r < nv; r++) if (A[r][col]) { piv = r; break; }
        if (piv < 0) continue;
        swap(A[rank], A[piv]);
        uint64_t inv = la_pow(A[rank][col], LA_P - 2);
        for (int c = 0; c < m; c++) A[rank][c] = la_mul(A[rank][c], inv);
        for (int r = 0; r < nv; r++) if (r != rank && A[r][col]) {
            uint64_t f = A[r][col];
            for (int c = 0; c < m; c++) if (A[rank][c]) { uint64_t t = la_mul(f, A[rank][c]); A[r][c] = A[r][c] >= t ? A[r][c] - t : A[r][c] + LA_P - t; }
        }
        pivcol.push_back(col); rank++;
    }
    vector<char> is_piv(m, 0); for (int c : pivcol) is_piv[c] = 1;
    vector<int> freec; for (int c = 0; c < m; c++) if (!is_piv[c]) freec.push_back(c);
    int d = (int)freec.size();
    vector<vector<uint64_t>> K(m, vector<uint64_t>(d, 0));     // K[e][t] = coordinate e of the t-th kernel vector
    for (int t = 0; t < d; t++) {
        K[freec[t]][t] = 1;
        for (int r = 0; r < rank; r++) { uint64_t v = A[r][freec[t]]; K[pivcol[r]][t] = v ? LA_P - v : 0; }
    }
    auto zero = [&](int e) { for (int t = 0; t < d; t++) if (K[e][t]) return false; return true; };
    auto same = [&](int e, int f, int s) {
        for (int t = 0; t < d; t++) { uint64_t g = s > 0 ? K[f][t] : (K[f][t] ? LA_P - K[f][t] : 0); if (K[e][t] != g) return false; }
        return true;
    };
    for (int e = 0; e < m; e++) if (zero(e)) return 'z';
    for (int r = 0; r < 7; r++) {
        const Partition& P = *choice[r];
        vector<pair<int,int>> at;                      // (link, block index)
        for (int bi = 0; bi < (int)P.size(); bi++) for (int j : P[bi]) at.push_back({eidx[r][j], bi});
        for (size_t x = 0; x < at.size(); x++) for (size_t y = x + 1; y < at.size(); y++)
            for (int s = 1; s >= -1; s -= 2) if (same(at[x].first, at[y].first, s)) {
                if (at[x].second != at[y].second) return 't';
                if (P[at[x].second].size() >= 3) return 'b';
            }
    }
    return 0;
}

int main(int argc, char** argv) {
    { int k = 0; for (int a = 0; a < 7; a++) for (int b = a + 1; b < 7; b++) { EDGES[k] = {a, b}; EIDX[a][b] = EIDX[b][a] = k; k++; } }
    if (argc < 4) { fprintf(stderr, "usage: cle_templates <c_min> <exact 0|1> <grids|-1> [--graph g] [--fix a[,b]] [--out f]\n"); return 2; }
    int kmin = atoi(argv[1]); bool exact = atoi(argv[2]) != 0; int grids = atoi(argv[3]);
    int graph_only = -1; vector<int> fix; const char* outpath = nullptr; bool use_la = false;
    for (int a = 4; a < argc; a++) {
        if (!strcmp(argv[a], "--la")) use_la = true;
        else if (!strcmp(argv[a], "--graph")) graph_only = atoi(argv[++a]);
        else if (!strcmp(argv[a], "--fix")) { string s = argv[++a]; size_t pos = 0; while (pos <= s.size()) { size_t q = s.find(',', pos); if (q == string::npos) q = s.size(); fix.push_back(atoi(s.substr(pos, q - pos).c_str())); pos = q + 1; } }
        else if (!strcmp(argv[a], "--out")) outpath = argv[++a];
    }
    FILE* out = outpath ? fopen(outpath, "w") : nullptr;
    vector<uint32_t> reps_all = graph_reps(), reps;
    for (uint32_t m : reps_all) if (grids < 0 || __builtin_popcount(m) == 21 - grids) reps.push_back(m);
    map<string, long long> stats; map<int, long long> hist; long long survivors_total = 0;
    int gnum = -1;
    for (uint32_t mask : reps) {
        gnum++;
        if (graph_only >= 0 && gnum != graph_only) continue;
        vector<pair<int,int>> edges; for (int k = 0; k < 21; k++) if (mask >> k & 1) edges.push_back(EDGES[k]);
        int ne = edges.size();
        int eidx[7][7]; for (int k = 0; k < ne; k++) { eidx[edges[k].first][edges[k].second] = k; eidx[edges[k].second][edges[k].first] = k; }
        vector<int> nb[7];
        for (int i = 0; i < 7; i++) for (auto& e : edges) { if (e.first == i) nb[i].push_back(e.second); else if (e.second == i) nb[i].push_back(e.first); }
        vector<Option> opts[7];
        bool empty = false, any_cmin = false;
        for (int i = 0; i < 7; i++) { opts[i] = admissible(nb[i], kmin); if (opts[i].empty()) empty = true; for (auto& o : opts[i]) if (o.c == kmin) any_cmin = true; }
        if (empty) continue;
        if (exact && !any_cmin) continue;
        array<int,7> order; for (int i = 0; i < 7; i++) order[i] = i;
        stable_sort(order.begin(), order.end(), [&](int x, int y) { return nb[x].size() > nb[y].size(); });
        UF uf; uf.init(ne);
        const Partition* choice[7] = {nullptr};
        int choice_c[7];        // by depth
        int choice_v[7];
        set<string> seen_keys; vector<array<int,7>> auts; bool auts_ready = false;
        auto root_ok = [&](int i) -> char {
            const Partition& parts = *choice[i];
            int cls[21]; for (int x = 0; x < ne; x++) cls[x] = -1;      // class root -> block index (same logic as the dict)
            for (int bi = 0; bi < (int)parts.size(); bi++)
                for (int j : parts[bi]) {
                    int r = uf.find(eidx[i][j]).first;
                    if (cls[r] != -1) {
                        if (cls[r] != bi) return 'O';
                        if (parts[bi].size() >= 3) return 'S';
                    }
                    cls[r] = bi;
                }
            return 0;
        };
        // recursive DFS (lambda)
        std::function<void(int)> rec = [&](int depth) {
            if (depth == 7) {
                stats["leaves"]++;
                bool has = false; for (int d = 0; d < 7; d++) if (choice_c[d] == kmin) has = true;
                if (exact && !has) { stats["no_root_at_cmin"]++; return; }
                vector<pair<int,const vector<int>*>> nodes; int lookup[7][7];
                for (int r = 0; r < 7; r++) for (auto& part : *choice[r]) { int nd = nodes.size(); nodes.push_back({r, &part}); for (int j : part) lookup[r][j] = nd; }
                vector<pair<int,int>> links; for (auto& e : edges) links.push_back({lookup[e.first][e.second], lookup[e.second][e.first]});
                int nv = nodes.size();
                int nul = nullity(nv, links, -1);
                int need = 0; for (int d = 0; d < 7; d++) need = max(need, 6 - choice_c[d]);
                if (nul < need) { stats["K_rank_below_root_span"]++; return; }
                for (int i = 0; i < (int)links.size(); i++) if (nullity(nv, links, i) == nul) { stats["Z_forced_zero_link"]++; return; }
                stats["survivor_labelled"]++;
                if (!auts_ready) { auts = automorphisms(mask); auts_ready = true; }
                string best;
                for (auto& perm : auts) {
                    char key[21];
                    for (int i = 0; i < 7; i++) {
                        unsigned char m3[3] = {0, 0, 0}; int nbk = 0;
                        for (auto& part : *choice[i]) { unsigned char bm = 0; for (int a : part) bm |= (unsigned char)(1u << perm[a]); m3[nbk++] = bm; }
                        sort(m3, m3 + 3);
                        for (int x = 0; x < 3; x++) key[perm[i] * 3 + x] = (char)m3[x];
                    }
                    string k(key, 21);
                    if (best.empty() || k < best) best = k;
                }
                if (seen_keys.count(best)) return;
                seen_keys.insert(best);
                if (use_la) {                           // verdict is Aut-invariant: testing the representative suffices
                    char why = la_check(nv, links, choice, eidx);
                    if (why) { stats[why == 't' ? "LA_equal_two_blocks" : why == 'b' ? "LA_equal_big_block" : "LA_zero_SHOULD_NOT_HAPPEN"]++; return; }
                }
                hist[nul]++; survivors_total++;
                if (out) {
                    string hex; char hb[3]; for (unsigned char ch : best) { snprintf(hb, 3, "%02x", ch); hex += hb; }
                    fprintf(out, "{\"graph_mask\": %u, \"canonical\": \"%s\", \"nongrid_edges\": [", mask, hex.c_str());
                    for (size_t k = 0; k < edges.size(); k++) fprintf(out, "%s[%d, %d]", k ? ", " : "", edges[k].first, edges[k].second);
                    fprintf(out, "], \"component_count_by_root_line\": [");
                    int cv[7]; for (int d = 0; d < 7; d++) cv[choice_v[d]] = choice_c[d];
                    for (int i = 0; i < 7; i++) fprintf(out, "%s%d", i ? ", " : "", cv[i]);
                    fprintf(out, "], \"nontrivial_component_groups\": [");
                    for (int i = 0; i < 7; i++) {
                        fprintf(out, "%s[", i ? ", " : "");
                        const Partition& P = *choice[i];
                        for (size_t bi = 0; bi < P.size(); bi++) { fprintf(out, "%s[", bi ? ", " : ""); for (size_t x = 0; x < P[bi].size(); x++) fprintf(out, "%s%d", x ? ", " : "", P[bi][x]); fprintf(out, "]"); }
                        fprintf(out, "]");
                    }
                    fprintf(out, "], \"kernel_dimension\": %d}\n", nul);
                }
                return;
            }
            int i = order[depth];
            for (int oi = 0; oi < (int)opts[i].size(); oi++) {
                if (depth < (int)fix.size() && oi != fix[depth]) continue;
                const Option& o = opts[i][oi];
                size_t mk = uf.mark(); bool ok = true;
                for (auto& part : o.parts) if (part.size() == 2) { if (!uf.relate_opposite(eidx[i][part[0]], eidx[i][part[1]])) { ok = false; break; } }
                if (!ok) { stats["P_odd_cycle"]++; uf.undo(mk); continue; }
                choice[i] = &o.parts; choice_c[depth] = o.c; choice_v[depth] = i;
                char bad = 0;
                for (int d2 = 0; d2 <= depth; d2++) { bad = root_ok(order[d2]); if (bad) break; }
                if (bad) stats[bad == 'O' ? "O_cross_block_class" : "S_block_class"]++;
                else rec(depth + 1);
                choice[i] = nullptr; uf.undo(mk);
            }
        };
        rec(0);
    }
    if (out) fclose(out);
    printf("{\"c_min\": %d, \"exact\": %s, \"grids\": %d, \"graph\": %d, \"graphs\": %zu, \"survivors_up_to_aut\": %lld, \"stats\": {", kmin, exact ? "true" : "false", grids, graph_only, reps.size(), survivors_total);
    bool first = true; for (auto& kv : stats) { printf("%s\"%s\": %lld", first ? "" : ", ", kv.first.c_str(), kv.second); first = false; }
    printf("}, \"kernel_dimension_histogram\": {"); first = true;
    for (auto& kv : hist) { printf("%s\"%d\": %lld", first ? "" : ", ", kv.first, kv.second); first = false; }
    printf("}}\n");
    return 0;
}
