// Row domains for the Hoffman-coclique boundary.  Input (stdin): nb c deg ; then nb lines with the block mask as a
// list "t s1 .. st".  Args: row index, max solutions to store (0 = count only), output file (optional).
// A row = set of `deg` blocks (other than the row's own) covering each point s once if s in B_w, twice otherwise,
// with pairwise intersections <= 1 and intersection with B_w <= 1.  Exhaustive (branch on the most constrained point,
// all subsets of its required size).
#include <bits/stdc++.h>
using namespace std;
typedef bitset<512> BS;
int nb, c, DEG; vector<vector<int>> blk; vector<BS> P, comp; vector<uint64_t> M;
long long cnt = 0; long long storecap = 0; vector<vector<int>> store; vector<int> chosen;
void rec(const BS& cands, vector<int>& need, int deg) {
    if (deg == 0) { for (int s = 0; s < c; s++) if (need[s]) return; cnt++; if ((long long)store.size() < storecap) store.push_back(chosen); return; }
    int best = -1; long long bc = LLONG_MAX; BS bset;
    for (int s = 0; s < c; s++) if (need[s] > 0) { BS x = cands & P[s]; long long k = x.count(); if (k < need[s]) return; if (k < bc) { bc = k; best = s; bset = x; } }
    if (best < 0) return;
    vector<int> L; for (int u = bset._Find_first(); u < (int)bset.size(); u = bset._Find_next(u)) L.push_back(u);
    int r = need[best];
    auto apply = [&](vector<int>& us) {
        vector<int> nd = need; uint64_t sat = 0;
        for (int u : us) for (int s : blk[u]) { if (--nd[s] < 0) return; }
        for (int s = 0; s < c; s++) if (nd[s] == 0) sat |= (1ULL << s);
        BS nc = cands & ~P[best];
        for (int u : us) nc &= comp[u];
        // remove blocks touching saturated points
        for (int u = nc._Find_first(); u < (int)nc.size(); u = nc._Find_next(u)) if (M[u] & sat) nc.reset(u);
        for (int u : us) chosen.push_back(u);
        rec(nc, nd, deg - (int)us.size());
        for (size_t i = 0; i < us.size(); i++) chosen.pop_back();
    };
    if (r == 1) { for (int u : L) { vector<int> us{u}; apply(us); } }
    else { for (size_t i = 0; i < L.size(); i++) for (size_t j = i + 1; j < L.size(); j++) if (comp[L[i]][L[j]]) { vector<int> us{L[i], L[j]}; apply(us); } }
}
int main(int argc, char** argv) {
    int w = atoi(argv[1]); storecap = argc > 2 ? atoll(argv[2]) : 0;
    cin >> nb >> c >> DEG; blk.resize(nb); M.assign(nb, 0); P.assign(c, BS()); comp.assign(nb, BS());
    for (int i = 0; i < nb; i++) { int t; cin >> t; blk[i].resize(t); for (auto& s : blk[i]) { cin >> s; M[i] |= 1ULL << s; P[s].set(i); } }
    for (int i = 0; i < nb; i++) for (int j = 0; j < nb; j++) if (i != j && __builtin_popcountll(M[i] & M[j]) <= 1) comp[i].set(j);
    vector<int> need(c); for (int s = 0; s < c; s++) need[s] = (M[w] >> s & 1) ? 1 : 2;
    BS cands = comp[w];
    auto t0 = chrono::steady_clock::now();
    rec(cands, need, DEG);
    double dt = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    fprintf(stderr, "row %d: domain %lld (%.2fs)\n", w, cnt, dt);
    if (argc > 3) { FILE* f = fopen(argv[3], "w"); for (auto& v : store) { for (int u : v) fprintf(f, "%d ", u); fprintf(f, "\n"); } fclose(f); }
    printf("%lld\n", cnt);
}
