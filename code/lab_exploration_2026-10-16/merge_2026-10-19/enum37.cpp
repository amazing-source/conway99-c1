// enum37: one canonical representative per isomorphism class of line graphs G_T with a given cycle type lambda
// (LAB 20/10/2026; proof of completeness in NOTE_ENUM37.md section 1-2).
//
// Model.  Classes C0, C1, C2 of size N (N = 12 for Conway), cross structure F_lambda: (0,i)-(1,i), (1,i)-(2,i),
// (2,i)-(0,sigma(i)) with sigma the canonical permutation of type lambda (cycles = consecutive blocks), and three
// within-class perfect matchings M0, M1, M2 (indices 0..(N-1)!!-1 in a fixed order).  Classes of G_T with cycle type
// lambda <-> orbits of A_lambda = Stab(F_lambda) on triples (M0, M1, M2).  With C = C(sigma) and a fixed reverser r0
// (r0 sigma r0^-1 = sigma^-1), the A_lambda-orbit of T = (M0, M1, M2) is the union of the C-orbits (diagonal action) of
//   V0 = (M0, M1, M2)          V1 = (s M2, M0, M1)          V2 = (s M1, s M2, M0)
//   V3 = (r M0, r s M2, r s M1)  V4 = (r M1, r M0, r s M2)   V5 = (r M2, r M1, r M0)      (s = sigma, r = r0)
// T is output iff T = min_j canonC(V_j) (lexicographic on the index triple), where canonC = lex-min of a C-orbit,
// computed through the stabiliser chain C > S(m0) > S(m0, m1) (orbit-min tables on the perfect matchings).
// Generation: m0 = min of its C u r0C orbit; M1 = min of its S(m0)-orbit; M2 = min of its S(m0, M1)-orbit; every
// first coordinate of every image is >= m0 (necessary); only the variants whose first coordinate ties with m0 need
// the full canonC comparison.
//
// Output (default): one line per class "s01[N] s12[N] s20[N]" with the standard partner matching i <-> i^1 (format of
// line37.exe file mode).  Options:
//   --count          no output lines; JSON summary on stdout
//   --fastcount      same count, same acceptance rule, but the M2 that cannot tie are counted in bulk (validation of
//                    the class counts for every lambda at N = 12 in minutes; with --adm: exact admissible counts)
//   --adm            only classes with K >= 0 (criterion: no sigma-edge {i, sigma i} in M0nM1, M1nM2, sigma(M2)nM0)
//   --slice i/n      only the (m0, M1) pairs whose running index is = i mod n
//   --triples        output "M0 M1 M2" (matching indices) instead of the 36 integers
//   --selftest k     compare canonA(T) with a brute-force minimum over all of A_lambda on k random triples (z small)
//   --burnside       exact class count by Burnside over the explicit group A_lambda (z <= 20000); with --adm: K >= 0 only
//   --random k seed  k uniform random (non-canonical) triples on F_lambda in the 36-integer form (sampling per lambda)
// usage: enum37 <lambda, e.g. 5,4,2,1 or 12 or 1^12> [options]
// build: g++ -O2 -std=c++17 [-DNCL=12] enum37.cpp -o enum37.exe
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <array>
#include <string>
#include <map>
#include <unordered_set>
#include <algorithm>
#include <chrono>
#include <random>
using namespace std;

#ifndef NCL
#define NCL 12
#endif
static const int N = NCL;
typedef array<uint8_t, N> Perm;

// ------------------------------------------------------------------------------------------- perfect matchings
static int NPM;
static vector<array<uint8_t, N>> PMS;           // partner arrays

static inline int rankpm(const uint8_t* p) {
    unsigned rem = (1u << N) - 1; int idx = 0;
    while (rem) {
        int a = __builtin_ctz(rem); rem &= ~(1u << a);
        int b = p[a];
        int cnt = __builtin_popcount(rem);
        int r = __builtin_popcount(rem & ((1u << b) - 1));
        idx = idx * cnt + r;
        rem &= ~(1u << b);
    }
    return idx;
}
static void gen_pms(unsigned rem, array<uint8_t, N>& cur) {
    if (!rem) { PMS.push_back(cur); return; }
    int a = __builtin_ctz(rem); unsigned r2 = rem & ~(1u << a);
    for (unsigned t = r2; t; t &= t - 1) {
        int b = __builtin_ctz(t);
        cur[a] = (uint8_t)b; cur[b] = (uint8_t)a;
        gen_pms(r2 & ~(1u << b), cur);
    }
}
static inline int applypm(const Perm& g, int x) {
    uint8_t q[N]; const uint8_t* p = PMS[x].data();
    for (int i = 0; i < N; i++) q[g[i]] = g[p[i]];
    return rankpm(q);
}

// ------------------------------------------------------------------------------------------- permutations
static inline Perm pid() { Perm p; for (int i = 0; i < N; i++) p[i] = (uint8_t)i; return p; }
static inline Perm pcomp(const Perm& a, const Perm& b) { Perm r; for (int i = 0; i < N; i++) r[i] = a[b[i]]; return r; }  // a o b
static inline Perm pinv(const Perm& a) { Perm r; for (int i = 0; i < N; i++) r[a[i]] = (uint8_t)i; return r; }
static inline uint64_t pcode(const Perm& a) { uint64_t c = 0; for (int i = 0; i < N; i++) c = c << 4 | a[i]; return c; }
static inline bool isid(const Perm& a) { for (int i = 0; i < N; i++) if (a[i] != i) return false; return true; }

// closure of a generating set into an explicit element list (Dimino-like: recompute when a new generator arrives)
struct Group {
    vector<Perm> gens, elts; unordered_set<uint64_t> in;
    Group() { Perm e = pid(); elts.push_back(e); in.insert(pcode(e)); }
    bool add(const Perm& g) {                  // returns true if g was new
        if (in.count(pcode(g))) return false;
        gens.push_back(g);
        // re-close: BFS from the identity
        elts.clear(); in.clear();
        Perm e = pid(); elts.push_back(e); in.insert(pcode(e));
        for (size_t h = 0; h < elts.size(); h++)
            for (auto& s : gens) { Perm f = pcomp(s, elts[h]); uint64_t c = pcode(f); if (!in.count(c)) { in.insert(c); elts.push_back(f); } }
        return true;
    }
};

// ------------------------------------------------------------------------------------------- lambda data
static vector<int> lam;
static Perm SIG, R0;
static vector<Perm> CG;                        // generators of C(sigma)
static long double ZL;                         // z_lambda
static vector<uint16_t> rootmin; static vector<Perm> roottrans;   // t(X) = rootmin[X]
static vector<uint16_t> sigPM, r0PM, r0sPM, minpm;
static vector<uint16_t> emask, semask;          // sigma-edge masks of X and of sigma(X)

struct Node1 { bool trivial = true; vector<Perm> elts; vector<Perm> gens; vector<uint16_t> mn; vector<Perm> tr; };
static int curM0 = -1; static Node1 node1;
// level-2 cache for the current m0: slot2[m1] = -1 (not computed), -2 (trivial stabiliser) or an index into tab2
static vector<int> slot2; static vector<vector<uint16_t>> tab2;
static size_t node2max = 0; static long long node2builds = 0;

static void orbits_with(const vector<Perm>& gens, vector<uint16_t>& mn, vector<Perm>* tr) {
    vector<char> vis(NPM, 0); vector<int> q; q.reserve(NPM);
    vector<Perm> u; if (tr) { u.assign(NPM, pid()); tr->assign(NPM, pid()); }
    mn.assign(NPM, 0);
    for (int x0 = 0; x0 < NPM; x0++) {
        if (vis[x0]) continue;
        q.clear(); q.push_back(x0); vis[x0] = 1; mn[x0] = (uint16_t)x0;
        if (tr) { u[x0] = pid(); (*tr)[x0] = pid(); }
        for (size_t h = 0; h < q.size(); h++) {
            int x = q[h];
            for (auto& g : gens) {
                int y = applypm(g, x);
                if (!vis[y]) {
                    vis[y] = 1; mn[y] = (uint16_t)x0; q.push_back(y);
                    if (tr) { u[y] = pcomp(g, u[x]); (*tr)[y] = pinv(u[y]); }
                }
            }
        }
    }
}

static void build_node1(int m0) {
    node1 = Node1(); slot2.assign(NPM, -1); tab2.clear(); curM0 = m0;
    // Schreier generators of Stab_C(m0): t_{gX} o g o t_X^-1 for X in the orbit of m0
    Group S; long long orb = 0;
    for (int x = 0; x < NPM; x++) {
        if (rootmin[x] != m0) continue;
        orb++;
        Perm ux = pinv(roottrans[x]);
        for (auto& g : CG) {
            int y = applypm(g, x);
            Perm s = pcomp(roottrans[y], pcomp(g, ux));
            if (!isid(s)) S.add(s);
        }
    }
    long double prod = (long double)S.elts.size() * orb;
    if (prod != ZL) { fprintf(stderr, "orbit-stabiliser check failed at m0=%d: |S|=%zu |O|=%lld z=%.0Lf\n", m0, S.elts.size(), orb, ZL); exit(2); }
    if (S.elts.size() == 1) return;
    node1.trivial = false; node1.elts = S.elts; node1.gens = S.gens;
    orbits_with(node1.gens, node1.mn, &node1.tr);
}

// orbit-min table of S(m0, m1) = Stab_{S(m0)}(m1) on the perfect matchings, or nullptr if that stabiliser is trivial.
// Tables are kept for the whole m0 (heap buffers of the inner vectors never move); the cache is only flushed between
// two M1 values of the main loop (flush_node2), never while a pointer is in use.
static const uint16_t* get_node2(int m1) {
    int sl = slot2[m1];
    if (sl == -2) return nullptr;
    if (sl >= 0) return tab2[sl].data();
    node2builds++;
    Group S;
    if (!node1.trivial)
        for (auto& s : node1.elts) if (applypm(s, m1) == m1 && !isid(s)) S.add(s);
    if (S.elts.size() <= 1) { slot2[m1] = -2; return nullptr; }
    tab2.emplace_back();
    orbits_with(S.gens, tab2.back(), nullptr);
    slot2[m1] = (int)tab2.size() - 1;
    if (tab2.size() > node2max) node2max = tab2.size();
    return tab2.back().data();
}
static void flush_node2() {                      // memory guard: at most ~6000 tables of 20 KB
    if (tab2.size() > 6000) { tab2.clear(); slot2.assign(NPM, -1); }
}

// lexicographic minimum of the C-orbit of (X, Y, Z); requires rootmin[X] == curM0 (tie case) -- general otherwise
static inline void canonC(int X, int Y, int Z, int out[3]) {
    int m = rootmin[X];
    const Perm& t = roottrans[X];
    int y = applypm(t, Y), z = applypm(t, Z);
    if (m != curM0) build_node1(m);            // never happens in the tie checks (m == curM0 there)
    if (node1.trivial) { out[0] = m; out[1] = y; out[2] = z; return; }
    int m1 = node1.mn[y];
    z = applypm(node1.tr[y], z);
    const uint16_t* n2 = get_node2(m1);
    out[0] = m; out[1] = m1; out[2] = n2 ? n2[z] : z;
}
static inline bool lexless(const int a[3], int b0, int b1, int b2) {
    if (a[0] != b0) return a[0] < b0;
    if (a[1] != b1) return a[1] < b1;
    return a[2] < b2;
}

// ------------------------------------------------------------------------------------------- output
static void to_standard(int M0, int M1, int M2, int out[3 * N]) {
    int Ms[3] = {M0, M1, M2};
    Perm psi[3];
    for (int c = 0; c < 3; c++) {
        const uint8_t* p = PMS[Ms[c]].data();
        int k = 0; bool done[N] = {false};
        for (int i = 0; i < N; i++) if (!done[i]) { psi[c][i] = (uint8_t)(2 * k); psi[c][p[i]] = (uint8_t)(2 * k + 1); done[i] = done[p[i]] = true; k++; }
    }
    Perm s01 = pcomp(psi[1], pinv(psi[0]));
    Perm s12 = pcomp(psi[2], pinv(psi[1]));
    Perm s20 = pcomp(psi[0], pcomp(SIG, pinv(psi[2])));
    for (int i = 0; i < N; i++) { out[i] = s01[i]; out[N + i] = s12[i]; out[2 * N + i] = s20[i]; }
}

// ------------------------------------------------------------------------------------------- explicit group (selftest)
static void explicit_C_R(vector<Perm>& Cel, vector<Perm>& Rel) {
    Group G; for (auto& g : CG) G.add(g);
    Cel = G.elts; Rel.clear();
    for (auto& g : Cel) Rel.push_back(pcomp(g, R0));
}

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: enum37 <lambda> [--count] [--adm] [--slice i/n] [--triples] [--selftest k]\n"); return 1; }
    // parse lambda
    {
        string s = argv[1];
        size_t c = s.find('^');
        if (c != string::npos) { int p = atoi(s.substr(0, c).c_str()), m = atoi(s.substr(c + 1).c_str()); lam.assign(m, p); }
        else { size_t st = 0; while (st < s.size()) { size_t e = s.find(',', st); if (e == string::npos) e = s.size(); lam.push_back(atoi(s.substr(st, e - st).c_str())); st = e + 1; } }
        sort(lam.rbegin(), lam.rend());
        int tot = 0; for (int p : lam) tot += p;
        if (tot != N) { fprintf(stderr, "lambda must be a partition of %d\n", N); return 1; }
    }
    bool countonly = false, adm = false, triples = false, fastcount = false, burnside = false; int sl_i = 0, sl_n = 1; long long selftest = 0;
    long long randk = 0; unsigned long long randseed = 1;
    for (int a = 2; a < argc; a++) {
        string o = argv[a];
        if (o == "--count") countonly = true;
        else if (o == "--fastcount") { countonly = true; fastcount = true; }
        else if (o == "--adm") adm = true;
        else if (o == "--triples") triples = true;
        else if (o == "--slice") { sscanf(argv[++a], "%d/%d", &sl_i, &sl_n); }
        else if (o == "--selftest") selftest = atoll(argv[++a]);
        else if (o == "--burnside") burnside = true;
        else if (o == "--random") { randk = atoll(argv[++a]); randseed = strtoull(argv[++a], 0, 10); }
        else { fprintf(stderr, "unknown option %s\n", o.c_str()); return 1; }
    }
    auto T0 = chrono::steady_clock::now();
    { array<uint8_t, N> cur{}; gen_pms((1u << N) - 1, cur); }
    NPM = (int)PMS.size();
    for (int i = 0; i < NPM; i++) if (rankpm(PMS[i].data()) != i) { fprintf(stderr, "rank error\n"); return 2; }
    // sigma, generators of C(sigma), reverser r0, z_lambda
    SIG = pid(); R0 = pid();
    vector<int> start; { int pos = 0; for (int L : lam) { start.push_back(pos); for (int x = 0; x < L; x++) { SIG[pos + x] = (uint8_t)(pos + (x + 1) % L); R0[pos + x] = (uint8_t)(pos + (L - x) % L); } pos += L; } }
    ZL = 1;
    for (size_t j = 0; j < lam.size();) {
        size_t e = j; while (e < lam.size() && lam[e] == lam[j]) e++;
        int k = lam[j], m = (int)(e - j);
        for (int i = 0; i < m; i++) ZL *= (long double)k * (i + 1);
        if (k >= 2) { Perm g = pid(); for (int x = 0; x < k; x++) g[start[j] + x] = (uint8_t)(start[j] + (x + 1) % k); CG.push_back(g); }
        if (m >= 2) { Perm g = pid(); for (int x = 0; x < k; x++) { g[start[j] + x] = (uint8_t)(start[j + 1] + x); g[start[j + 1] + x] = (uint8_t)(start[j] + x); } CG.push_back(g); }
        if (m >= 3) { Perm g = pid(); for (int i = 0; i < m; i++) for (int x = 0; x < k; x++) g[start[j + i] + x] = (uint8_t)(start[j + (i + 1) % m] + x); CG.push_back(g); }
        j = e;
    }
    for (auto& g : CG) if (pcomp(g, SIG) != pcomp(SIG, g)) { fprintf(stderr, "generator does not commute\n"); return 2; }
    if (pcomp(pcomp(R0, SIG), pinv(R0)) != pinv(SIG)) { fprintf(stderr, "r0 is not a reverser\n"); return 2; }
    // root orbits on the perfect matchings
    orbits_with(CG, rootmin, &roottrans);
    for (int x = 0; x < NPM; x++) if (applypm(roottrans[x], x) != rootmin[x]) { fprintf(stderr, "transversal error\n"); return 2; }
    sigPM.resize(NPM); r0PM.resize(NPM); r0sPM.resize(NPM); minpm.resize(NPM);
    Perm R0S = pcomp(R0, SIG);
    for (int x = 0; x < NPM; x++) { sigPM[x] = (uint16_t)applypm(SIG, x); r0PM[x] = (uint16_t)applypm(R0, x); r0sPM[x] = (uint16_t)applypm(R0S, x); }
    for (int x = 0; x < NPM; x++) minpm[x] = min(rootmin[x], rootmin[r0PM[x]]);
    // sigma-edges and masks
    {
        int eid[N][N]; memset(eid, -1, sizeof eid); int ne = 0;
        for (int i = 0; i < N; i++) if (SIG[i] != i && eid[i][SIG[i]] < 0) { eid[i][SIG[i]] = eid[SIG[i]][i] = ne++; }
        emask.assign(NPM, 0); semask.assign(NPM, 0);
        for (int x = 0; x < NPM; x++) { uint16_t m = 0; for (int i = 0; i < N; i++) { int j = PMS[x][i]; if (i < j && eid[i][j] >= 0) m |= (uint16_t)(1u << eid[i][j]); } emask[x] = m; }
        for (int x = 0; x < NPM; x++) semask[x] = emask[sigPM[x]];
    }
    int nroot = 0; for (int x = 0; x < NPM; x++) if (rootmin[x] == x) nroot++;
    // eligible lists: PMs sorted by minpm descending -> prefix {X : minpm[X] >= m0}
    vector<int> order(NPM); for (int i = 0; i < NPM; i++) order[i] = i;
    stable_sort(order.begin(), order.end(), [](int a, int b) { return minpm[a] > minpm[b]; });

    if (randk) {
        // uniform random triples (M0, M1, M2) on F_lambda (NOT canonical), in the 36-integer standard form: a sample of
        // the classes of type lambda weighted by 1/|Aut| (uniform on the free orbits); with --adm only K >= 0 ones
        mt19937_64 rng(randseed);
        long long out = 0, tries = 0;
        while (out < randk) {
            int M0 = (int)(rng() % NPM), M1 = (int)(rng() % NPM), M2 = (int)(rng() % NPM);
            tries++;
            if (adm && ((emask[M0] & emask[M1]) || (emask[M1] & emask[M2]) || (emask[M0] & semask[M2]))) continue;
            int s[3 * N]; to_standard(M0, M1, M2, s);
            for (int k = 0; k < 3 * N; k++) printf(k ? " %d" : "%d", s[k]);
            printf("\n"); out++;
        }
        fprintf(stderr, "{\"lambda\": \"%s\", \"random\": %lld, \"tries\": %lld, \"adm\": %s}\n", argv[1], out, tries, adm ? "true" : "false");
        return 0;
    }
    if (burnside) {
        // Burnside over the explicit group A_lambda (|C| = z <= 20000), optionally restricted to admissible triples:
        //   N = [ sum_{g in C} Fix(g,g,g) + 2 sum_{g in C} Fix(rho; g,g,g sigma) + 3 sum_{h in R} Fix((02); h,h,h) ] / 6z
        //   Fix(g,g,g)           = triples in L_g^3
        //   Fix(rho; g,g,g s)    = {(M, gM, g^2 M) : sigma g^3 M = M}
        //   Fix((02); h,h,h)     = {(M0, M1, h M0) : h^2 M0 = M0, h M1 = M1}
        // (the three transposition cosets, resp. the two 3-cycle cosets, are conjugate in A_lambda; admissibility is
        // A_lambda-invariant, so they contribute equally).  L_p = perfect matchings fixed by p.
        if (ZL > 20000) { fprintf(stderr, "z too large for --burnside\n"); return 1; }
        vector<Perm> Cel, Rel; explicit_C_R(Cel, Rel);
        if ((long double)Cel.size() != ZL) { fprintf(stderr, "|C| = %zu != z\n", Cel.size()); return 2; }
        int ne = 0; { uint16_t all = 0; for (int x = 0; x < NPM; x++) all |= emask[x]; while (all >> ne) ne++; }
        const size_t FULL = ((size_t)1 << ne) - 1;
        auto fixed = [&](const Perm& p) { vector<int> L; for (int x = 0; x < NPM; x++) if (applypm(p, x) == x) L.push_back(x); return L; };
        auto okT = [&](int a, int b, int c) { return !(emask[a] & emask[b]) && !(emask[b] & emask[c]) && !(emask[a] & semask[c]); };
        vector<long long> h0(FULL + 1), z2(FULL + 1);
        // admissible triples in L^3: for each M1 (grouped by A = emask[M1]): sum_{X & Y = 0} h0[X] h2[Y]
        auto id_term = [&](const vector<int>& L) -> long long {
            long long s = (long long)L.size();
            if (!adm) return s * s * s;
            map<int, long long> byA; for (int x : L) byA[emask[x]]++;
            long long tot = 0;
            for (auto& kv : byA) {
                int A = kv.first;
                fill(h0.begin(), h0.end(), 0); fill(z2.begin(), z2.end(), 0);
                for (int x : L) { if (!(emask[x] & A)) { h0[emask[x]]++; z2[semask[x]]++; } }
                for (int bit = 0; bit < ne; bit++) for (size_t S = 0; S <= FULL; S++) if (S >> bit & 1) z2[S] += z2[S ^ ((size_t)1 << bit)];
                long long c = 0; for (size_t X = 0; X <= FULL; X++) if (h0[X]) c += h0[X] * z2[FULL & ~X];
                tot += c * kv.second;
            }
            return tot;
        };
        long long S_id = 0, S_rot = 0, S_ref = 0;
        for (auto& g : Cel) {
            vector<int> Lg = fixed(g);
            S_id += id_term(Lg);
            Perm g2 = pcomp(g, g), sg3 = pcomp(SIG, pcomp(g2, g));
            vector<int> L3 = fixed(sg3);
            for (int M : L3) { int a1 = applypm(g, M), a2 = applypm(g2, M); if (!adm || okT(M, a1, a2)) S_rot++; }
        }
        for (auto& h : Rel) {
            vector<int> Lh = fixed(h), Lh2 = fixed(pcomp(h, h));
            vector<long long> hz(FULL + 1, 0);
            for (int x : Lh) hz[emask[x]]++;
            for (int bit = 0; bit < ne; bit++) for (size_t S = 0; S <= FULL; S++) if (S >> bit & 1) hz[S] += hz[S ^ ((size_t)1 << bit)];
            for (int M0 : Lh2) {
                int M2 = applypm(h, M0);
                if (adm && (emask[M0] & semask[M2])) continue;
                S_ref += adm ? hz[FULL & ~(size_t)(emask[M0] | emask[M2])] : (long long)Lh.size();
            }
        }
        long long z = (long long)ZL, num = S_id + 2 * S_rot + 3 * S_ref;
        string ls; for (size_t k = 0; k < lam.size(); k++) { if (k) ls += ","; ls += to_string(lam[k]); }
        printf("{\"N\": %d, \"lambda\": \"%s\", \"z\": %lld, \"adm\": %s, \"S_id\": %lld, \"S_rot\": %lld, \"S_ref\": %lld, "
               "\"divisible\": %s, \"classes\": %lld, \"wall_s\": %.3f}\n", N, ls.c_str(), z, adm ? "true" : "false", S_id, S_rot,
               S_ref, num % (6 * z) == 0 ? "true" : "false", num / (6 * z),
               chrono::duration<double>(chrono::steady_clock::now() - T0).count());
        return num % (6 * z) == 0 ? 0 : 3;
    }
    if (selftest) {
        vector<Perm> Cel, Rel; explicit_C_R(Cel, Rel);
        if ((long double)Cel.size() != ZL) { fprintf(stderr, "|C| = %zu != z\n", Cel.size()); return 2; }
        mt19937_64 rng(12345);
        long long bad = 0;
        for (long long it = 0; it < selftest; it++) {
            int M[3]; for (int c = 0; c < 3; c++) M[c] = (int)(rng() % NPM);
            if (it % 3 == 1) M[1] = applypm(Cel[rng() % Cel.size()], M[0]);          // force ties sometimes
            if (it % 3 == 2) M[2] = applypm(Rel[rng() % Rel.size()], M[0]);
            // brute force over A_lambda: the six images listed in enum37_burnside.py
            int best[3] = {1 << 30, 0, 0};
            auto upd = [&](int a, int b, int c) { int o[3] = {a, b, c}; if (lexless(o, best[0], best[1], best[2])) { best[0] = a; best[1] = b; best[2] = c; } };
            for (auto& g : Cel) {
                Perm gs = pcomp(g, SIG);
                upd(applypm(g, M[0]), applypm(g, M[1]), applypm(g, M[2]));
                upd(applypm(gs, M[2]), applypm(g, M[0]), applypm(g, M[1]));
                upd(applypm(gs, M[1]), applypm(gs, M[2]), applypm(g, M[0]));
            }
            for (auto& h : Rel) {
                Perm hs = pcomp(h, SIG);
                upd(applypm(h, M[0]), applypm(hs, M[2]), applypm(hs, M[1]));
                upd(applypm(h, M[1]), applypm(h, M[0]), applypm(hs, M[2]));
                upd(applypm(h, M[2]), applypm(h, M[1]), applypm(h, M[0]));
            }
            // fast: min over the six variants of canonC
            int V[6][3] = {{M[0], M[1], M[2]}, {sigPM[M[2]], M[0], M[1]}, {sigPM[M[1]], sigPM[M[2]], M[0]},
                           {r0PM[M[0]], r0sPM[M[2]], r0sPM[M[1]]}, {r0PM[M[1]], r0PM[M[0]], r0sPM[M[2]]}, {r0PM[M[2]], r0PM[M[1]], r0PM[M[0]]}};
            int fb[3] = {1 << 30, 0, 0};
            for (int j = 0; j < 6; j++) {
                int o[3];
                int m = rootmin[V[j][0]];
                if (m != curM0) build_node1(m);
                canonC(V[j][0], V[j][1], V[j][2], o);
                if (lexless(o, fb[0], fb[1], fb[2])) { fb[0] = o[0]; fb[1] = o[1]; fb[2] = o[2]; }
            }
            if (fb[0] != best[0] || fb[1] != best[1] || fb[2] != best[2]) bad++;
        }
        printf("{\"lambda\": \"%s\", \"selftest\": %lld, \"mismatches\": %lld, \"z\": %.0Lf}\n", argv[1], selftest, bad, ZL);
        return bad ? 3 : 0;
    }

    // ------------------------------------------------------------------------------------- enumeration
    static char obuf[1 << 16]; setvbuf(stdout, obuf, _IOFBF, sizeof obuf);
    long long reps = 0, cand = 0, pairs = 0, ties = 0, tie_rej = 0, kpr1 = 0, kpr2 = 0, m0count = 0;
    long long pairidx = -1, fastpairs = 0;
    int ne = 0; { uint16_t all = 0; for (int x = 0; x < NPM; x++) all |= emask[x]; while (all >> ne) ne++; }
    vector<long long> zeta((size_t)1 << ne);
    long long m1_killed = 0;
    vector<uint16_t> phiPM(NPM);
    for (int m0 = 0; m0 < NPM; m0++) {
        if (rootmin[m0] != m0 || minpm[m0] != m0) continue;
        m0count++;
        build_node1(m0);
        int cnt = 0; while (cnt < NPM && minpm[order[cnt]] >= m0) cnt++;
        bool tR0 = rootmin[r0PM[m0]] == m0;
        // S(m0) trivial and tR0: canonC(V3) = (m0, phi M2, phi M1) with phi = t3 r0 sigma, t3 = roottrans[r0 m0]
        bool v3tab = tR0 && node1.trivial;
        if (v3tab) { const Perm& t3 = roottrans[r0PM[m0]]; for (int x = 0; x < NPM; x++) phiPM[x] = (uint16_t)applypm(t3, r0sPM[x]); }
        // bulk counting (--fastcount): the eligible M2 that can tie with m0, and (with --adm) a subset-sum table
        // zeta[S] = #{eligible M2 : sigma(M2) n m0 has no sigma-edge, sigma-edges of M2 contained in S}
        vector<int> tieList;
        if (fastcount) {
            for (int b = 0; b < cnt; b++) { int M2 = order[b]; if (rootmin[M2] == m0 || rootmin[r0PM[M2]] == m0) tieList.push_back(M2); }
            if (adm) {
                fill(zeta.begin(), zeta.end(), 0);
                for (int b = 0; b < cnt; b++) { int M2 = order[b]; if (!(emask[m0] & semask[M2])) zeta[emask[M2]]++; }
                for (int bit = 0; bit < ne; bit++) for (size_t S = 0; S < zeta.size(); S++) if (S >> bit & 1) zeta[S] += zeta[S ^ ((size_t)1 << bit)];
            }
        }
        for (int a = 0; a < cnt; a++) {
            int M1 = order[a];
            if (!node1.trivial && node1.mn[M1] != M1) continue;
            if (adm && (emask[m0] & emask[M1])) { kpr1++; continue; }
            pairidx++;
            if (pairidx % sl_n != sl_i) continue;
            pairs++;
            flush_node2();
            const uint16_t* n2 = node1.trivial ? nullptr : get_node2(M1);
            bool tC1 = rootmin[M1] == m0, tR1 = rootmin[r0PM[M1]] == m0;
            // S(m0) trivial and tR1: canonC(V4) = (m0, t4 r0 m0, t4 r0 sigma M2), t4 = roottrans[r0 M1]
            int v4mode = 0; Perm t4;              // 0: V4 cannot reject, 1: per-M2 test, 2: general canonC
            if (tR1) {
                if (node1.trivial) {
                    t4 = roottrans[r0PM[M1]];
                    int a4 = applypm(t4, r0PM[m0]);
                    if (a4 < M1) { m1_killed++; continue; }        // V4 < T for every M2
                    if (a4 == M1) v4mode = 1;
                } else v4mode = 2;
            }
            if (fastcount && !n2 && !tC1 && !tR0 && v4mode == 0) {
                // every eligible M2 passing the K-prune is accepted except the tied ones rejected by V1 or V5
                long long base = adm ? zeta[((size_t)1 << ne) - 1 - emask[M1]] : cnt;
                cand += base; kpr2 += cnt - base; fastpairs++;
                for (int M2 : tieList) {
                    if (adm && ((emask[M1] & emask[M2]) || (emask[m0] & semask[M2]))) continue;
                    ties++;
                    int o[3]; bool rej = false;
                    if (rootmin[M2] == m0) { canonC(sigPM[M2], m0, M1, o); if (lexless(o, m0, M1, M2)) rej = true; }
                    if (!rej && rootmin[r0PM[M2]] == m0) { canonC(r0PM[M2], r0PM[M1], r0PM[m0], o); if (lexless(o, m0, M1, M2)) rej = true; }
                    if (rej) { tie_rej++; base--; }
                }
                reps += base;
                continue;
            }
            for (int b = 0; b < cnt; b++) {
                int M2 = order[b];
                if (n2 && n2[M2] != M2) continue;
                if (adm && ((emask[M1] & emask[M2]) || (emask[m0] & semask[M2]))) { kpr2++; continue; }
                cand++;
                bool tC2 = rootmin[M2] == m0, tR2 = rootmin[r0PM[M2]] == m0;
                if (tC2 | tC1 | tR0 | (v4mode != 0) | tR2) {
                    ties++;
                    int o[3]; bool rej = false;
                    if (tC2) { canonC(sigPM[M2], m0, M1, o); if (lexless(o, m0, M1, M2)) rej = true; }
                    if (!rej && tC1) { canonC(sigPM[M1], sigPM[M2], m0, o); if (lexless(o, m0, M1, M2)) rej = true; }
                    if (!rej && tR0) {
                        if (v3tab) { int p2 = phiPM[M2], p1 = phiPM[M1]; if (p2 < M1 || (p2 == M1 && p1 < M2)) rej = true; }
                        else { canonC(r0PM[m0], r0sPM[M2], r0sPM[M1], o); if (lexless(o, m0, M1, M2)) rej = true; }
                    }
                    if (!rej && v4mode == 1) { if (applypm(t4, r0sPM[M2]) < M2) rej = true; }
                    if (!rej && v4mode == 2) { canonC(r0PM[M1], r0PM[m0], r0sPM[M2], o); if (lexless(o, m0, M1, M2)) rej = true; }
                    if (!rej && tR2) { canonC(r0PM[M2], r0PM[M1], r0PM[m0], o); if (lexless(o, m0, M1, M2)) rej = true; }
                    if (rej) { tie_rej++; continue; }
                }
                reps++;
                if (!countonly) {
                    if (triples) printf("%d %d %d\n", m0, M1, M2);
                    else {
                        int s[3 * N]; to_standard(m0, M1, M2, s);
                        char line[512]; int p = 0;
                        for (int k = 0; k < 3 * N; k++) p += sprintf(line + p, k ? " %d" : "%d", s[k]);
                        line[p++] = '\n'; line[p] = 0; fputs(line, stdout);
                    }
                }
            }
        }
    }
    double wall = chrono::duration<double>(chrono::steady_clock::now() - T0).count();
    fflush(stdout);
    FILE* fs = countonly ? stdout : stderr;
    string ls; for (size_t k = 0; k < lam.size(); k++) { if (k) ls += ","; ls += to_string(lam[k]); }
    fprintf(fs, "{\"N\": %d, \"lambda\": \"%s\", \"z\": %.0Lf, \"adm\": %s, \"slice\": \"%d/%d\", \"classes\": %lld, "
                "\"root_orbits\": %d, \"m0_reps\": %lld, \"pairs\": %lld, \"candidates\": %lld, \"tie_checks\": %lld, "
                "\"tie_rejects\": %lld, \"kprune1\": %lld, \"kprune2\": %lld, \"node2_tables_max\": %zu, \"node2_builds\": %lld, "
                "\"fastcount\": %s, \"fast_pairs\": %lld, \"m1_killed\": %lld, \"wall_s\": %.3f}\n",
            N, ls.c_str(), ZL, adm ? "true" : "false", sl_i, sl_n, reps, nroot, m0count, pairs, cand, ties, tie_rej,
            kpr1, kpr2, node2max, node2builds, fastcount ? "true" : "false", fastpairs, m1_killed, wall);
    return 0;
}
