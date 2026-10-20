// enum37_brute: brute-force orbit census of line-graph structures for SMALL class size N (4 or 6), with no use of the
// lambda decomposition (LAB 20/10/2026, NOTE_ENUM37.md section 3).
// X = all triples (s01, s12, s20) of bijections of [N] (standard partner matching i <-> i^1 in each class).
// H = B_{N/2}^3 x| S3 acting by phi(c, i) = (tau(c), pi_c(i)); generators: in each class the flip (0 1), the pair swap
// (0 2)(1 3) and the pair cycle (0 2 4 ..)(1 3 5 ..) (each with tau = id), the class rotation tau = (0 1 2) and the
// class transposition tau = (1 2) (with pi = id).  Action formula: forward pair (a,b) goes to (tau a, tau b); if that pair
// is forward, s'_{tau a tau b} = pi_b s_ab pi_a^-1, else s'_{tau b tau a} = pi_a s_ab^-1 pi_b^-1 (checked against the graph
// action in enum37_validate_group.py).
// Modes:  census              -> orbits per cycle type lambda of sigma = s20 s12 s01, total, orbit-size histogram
//         check <reps.txt>    -> each line s01[N] s12[N] s20[N]; computes the H-orbit of each line, verifies that the
//                                lines are pairwise non-isomorphic and that every orbit of X is hit exactly once
// build: g++ -O2 -DNCL=6 enum37_brute.cpp -o enum37_brute6.exe
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include <array>
using namespace std;

#ifndef NCL
#define NCL 6
#endif
static const int N = NCL;
static int NF;                       // N!
static vector<array<int, N>> P;      // all permutations
static vector<int> cmp_;             // compose table: cmp_[a*NF+b] = a o b
static vector<int> inv_;
static map<array<int, N>, int> idx;

static int pid(const array<int, N>& p) { return idx.at(p); }

struct Elt { int a01, a12, a20; };
static inline uint64_t code(int a, int b, int c) { return ((uint64_t)a * NF + b) * NF + c; }

static int C(int a, int b) { return cmp_[a * NF + b]; }

// generators acting on triples of permutation ids
struct Gen { int tau[3]; int pi[3]; };
static vector<Gen> gens;

static void apply(const Gen& g, int s[3], int out[3]) {
    // s[0] = s01 (0->1), s[1] = s12 (1->2), s[2] = s20 (2->0); forward pairs (0,1),(1,2),(2,0)
    static const int A[3] = {0, 1, 2}, B[3] = {1, 2, 0};
    for (int e = 0; e < 3; e++) {
        int a = A[e], b = B[e];
        int ta = g.tau[a], tb = g.tau[b];
        int fe = -1; bool fwd = false;
        for (int f = 0; f < 3; f++) {
            if (A[f] == ta && B[f] == tb) { fe = f; fwd = true; }
            if (A[f] == tb && B[f] == ta) { fe = f; fwd = false; }
        }
        if (fwd) out[fe] = C(g.pi[b], C(s[e], inv_[g.pi[a]]));
        else out[fe] = C(g.pi[a], C(inv_[s[e]], inv_[g.pi[b]]));
    }
}

static string cyctype(int p) {
    bool seen[N] = {false};
    vector<int> t;
    for (int i = 0; i < N; i++) if (!seen[i]) { int L = 0, j = i; while (!seen[j]) { seen[j] = true; j = P[p][j]; L++; } t.push_back(L); }
    sort(t.rbegin(), t.rend());
    string s = "(";
    for (size_t k = 0; k < t.size(); k++) { if (k) s += ","; s += to_string(t[k]); }
    return s + ")";
}

static vector<uint64_t> bits;
static inline bool getb(uint64_t x) { return (bits[x >> 6] >> (x & 63)) & 1; }
static inline void setb(uint64_t x) { bits[x >> 6] |= 1ULL << (x & 63); }

// BFS of the orbit of x0; marks visited; returns size and min code
static uint64_t orbit(uint64_t x0, uint64_t& mn, vector<uint64_t>& q, bool mark_only_local, vector<uint64_t>* touched) {
    q.clear(); q.push_back(x0); setb(x0); mn = x0;
    if (touched) touched->push_back(x0);
    for (size_t h = 0; h < q.size(); h++) {
        uint64_t x = q[h];
        int s[3] = {(int)(x / ((uint64_t)NF * NF)), (int)((x / NF) % NF), (int)(x % NF)}, o[3];
        for (auto& g : gens) {
            apply(g, s, o);
            uint64_t y = code(o[0], o[1], o[2]);
            if (!getb(y)) { setb(y); q.push_back(y); if (y < mn) mn = y; if (touched) touched->push_back(y); }
        }
    }
    (void)mark_only_local;
    return q.size();
}

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: enum37_brute census | check <reps.txt>\n"); return 1; }
    array<int, N> p; for (int i = 0; i < N; i++) p[i] = i;
    do { idx[p] = (int)P.size(); P.push_back(p); } while (next_permutation(p.begin(), p.end()));
    NF = (int)P.size();
    cmp_.resize((size_t)NF * NF); inv_.resize(NF);
    for (int a = 0; a < NF; a++) {
        array<int, N> iv; for (int i = 0; i < N; i++) iv[P[a][i]] = i; inv_[a] = pid(iv);
        for (int b = 0; b < NF; b++) { array<int, N> r; for (int i = 0; i < N; i++) r[i] = P[a][P[b][i]]; cmp_[a * NF + b] = pid(r); }
    }
    int idp = 0;
    auto mk = [&](vector<int> v) { array<int, N> r; for (int i = 0; i < N; i++) r[i] = v[i]; return pid(r); };
    vector<int> flip(N), pswap(N), pcyc(N);
    for (int i = 0; i < N; i++) { flip[i] = i; pswap[i] = i; pcyc[i] = (i + 2) % N; }
    flip[0] = 1; flip[1] = 0;
    pswap[0] = 2; pswap[2] = 0; pswap[1] = 3; pswap[3] = 1;
    vector<int> bgen = {mk(flip), mk(pswap)};
    if (N / 2 >= 3) bgen.push_back(mk(pcyc));
    for (int c = 0; c < 3; c++) for (int b : bgen) {
        Gen g; for (int k = 0; k < 3; k++) { g.tau[k] = k; g.pi[k] = idp; } g.pi[c] = b; gens.push_back(g);
    }
    { Gen g; g.tau[0] = 1; g.tau[1] = 2; g.tau[2] = 0; for (int k = 0; k < 3; k++) g.pi[k] = idp; gens.push_back(g); }
    { Gen g; g.tau[0] = 0; g.tau[1] = 2; g.tau[2] = 1; for (int k = 0; k < 3; k++) g.pi[k] = idp; gens.push_back(g); }
    uint64_t total = (uint64_t)NF * NF * NF;
    bits.assign((total + 63) / 64, 0);
    vector<uint64_t> q;
    string mode = argv[1];
    if (mode == "census") {
        map<string, long long> per; map<long long, long long> sizes; long long norb = 0;
        FILE* fo = argc > 2 ? fopen(argv[2], "w") : nullptr;
        for (uint64_t x = 0; x < total; x++) {
            if (getb(x)) continue;
            uint64_t mn; uint64_t sz = orbit(x, mn, q, false, nullptr);
            int s01 = (int)(x / ((uint64_t)NF * NF)), s12 = (int)((x / NF) % NF), s20 = (int)(x % NF);
            string lam = cyctype(C(s20, C(s12, s01)));
            per[lam]++; sizes[(long long)sz]++; norb++;
            if (fo) fprintf(fo, "%llu %s\n", (unsigned long long)mn, lam.c_str());
        }
        if (fo) fclose(fo);
        printf("{\"N\": %d, \"X\": %llu, \"orbits\": %lld, \"per_lambda\": {", N, (unsigned long long)total, norb);
        bool first = true;
        for (auto& kv : per) { printf("%s\"%s\": %lld", first ? "" : ", ", kv.first.c_str(), kv.second); first = false; }
        printf("}, \"orbit_sizes\": {");
        first = true;
        for (auto& kv : sizes) { printf("%s\"%lld\": %lld", first ? "" : ", ", kv.first, kv.second); first = false; }
        printf("}}\n");
        return 0;
    }
    if (mode == "check") {
        FILE* f = fopen(argv[2], "r");
        vector<uint64_t> mins; map<string, long long> per; long long lines = 0, dup = 0;
        vector<uint64_t> touched;
        while (true) {
            int v[3 * N]; bool ok = true;
            for (int k = 0; k < 3 * N; k++) if (fscanf(f, "%d", &v[k]) != 1) { ok = false; break; }
            if (!ok) break;
            array<int, N> a, b, c;
            for (int i = 0; i < N; i++) { a[i] = v[i]; b[i] = v[N + i]; c[i] = v[2 * N + i]; }
            uint64_t x = code(pid(a), pid(b), pid(c));
            lines++;
            if (getb(x)) { dup++; continue; }       // already in the orbit of an earlier line
            uint64_t mn; orbit(x, mn, q, false, &touched);
            mins.push_back(mn);
            per[cyctype(C(pid(c), C(pid(b), pid(a))))]++;
        }
        uint64_t covered = 0; for (auto w : bits) covered += __builtin_popcountll(w);
        printf("{\"N\": %d, \"lines\": %lld, \"duplicates\": %lld, \"distinct_orbits\": %zu, \"covered\": %llu, \"X\": %llu, "
               "\"complete\": %s, \"per_lambda\": {", N, lines, dup, mins.size(), (unsigned long long)covered,
               (unsigned long long)total, covered == total ? "true" : "false");
        bool first = true;
        for (auto& kv : per) { printf("%s\"%s\": %lld", first ? "" : ", ", kv.first.c_str(), kv.second); first = false; }
        printf("}}\n");
        return 0;
    }
    return 1;
}
