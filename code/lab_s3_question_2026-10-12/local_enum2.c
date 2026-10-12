/* Lab session, 2026-10-12. EXHAUSTIVE enumeration of the local problem at the vertex P = 0 of the Brouwer-Haemers graph
   (derivation in local_vertex.py), by a depth-first search with domain propagation. No SAT solver, no symmetry argument.

   BH: V = F_3^4, x ~ y iff q(y - x) = 0, q = x0^2 + x1^2 + x2 x3.   B(x,y) = 2 x0 y0 + 2 x1 y1 + x2 y3 + x3 y2.
   Unknowns: for each of the 60 far vertices R (non-neighbours of P) a state: 0 = "flat", or one of the ten partitions 3+3
   of the six common neighbours C(P,R) (a 6-bit mask of weight 3 whose bit 0 is 0).
   Constraints: for each of the 180 non-adjacent pairs {a, b} inside N(P), the number of far R with a, b in C(P,R) (there
   are exactly five) whose mask separates a from b is 0 or 3.

   Search: every far vertex has a domain (subset of the 11 states). Propagation, to a fixed point: for a pair, with
   lo = number of its far vertices that must separate and hi = number that can separate, a value of one of them is removed
   when the total can no longer be 0 or 3. Branching on an undecided vertex of smallest domain. A leaf where all domains
   are singletons and propagation succeeds satisfies every constraint (then lo = hi = the number of separations).

   Modes:
     local_enum2 all            the whole problem (the trivial solution included)
     local_enum2 cubes          for every far vertex R0 and every one of its ten partitions: all solutions in which R0 has
                                that partition. Every non-trivial solution has a split R0, so the union over the 600 cubes
                                is the set of all non-trivial solutions (each counted once per split vertex).
   Every solution is identified: "trivial", "line delta" when the split R are exactly those with B(R, delta) = 0 and the
   partition of each is the partition of C(P,R) by the value of B(Z, delta), for one of the ten isotropic directions, or
   "OTHER" (printed in full).
   Memory: a few kilobytes. Build: gcc -O3 -march=native -o local_enum2 local_enum2.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ALL 0x7ff
static int V[81][4], adj[81][81];
static int NP[20], far[60], C[60][6];
static int npair, pairR[180][5], pslot[180][5], pairN[180];
static int rp[60][15], S1[60][15], nrp[60];
static int masks[11];
static int dom[60];
static long long nodes, nsol, nline[10], ntriv, nother;
static int iso[10][4], niso;
static int quiet;

static int q(const int *x) { return (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3; }
static int Bf(const int *x, const int *y) { return (2 * x[0] * y[0] + 2 * x[1] * y[1] + x[2] * y[3] + x[3] * y[2]) % 3; }

static void report(void) {
    int split = 0, r, d, i, found = -1, st[60];
    for (r = 0; r < 60; r++) { st[r] = __builtin_ctz(dom[r]); split += st[r] != 0; }
    for (d = 0; d < niso && found < 0; d++) {
        int ok = 1;
        for (r = 0; r < 60 && ok; r++) {
            int m = 0;
            if (Bf(V[far[r]], iso[d]) == 0) {
                int b0 = Bf(V[C[r][0]], iso[d]);
                for (i = 1; i < 6; i++) if (Bf(V[C[r][i]], iso[d]) != b0) m |= 1 << i;
            }
            if (m != masks[st[r]]) ok = 0;
        }
        if (ok) found = d;
    }
    nsol++;
    if (split == 0) ntriv++;
    else if (found >= 0) nline[found]++;
    else nother++;
    if (!quiet || (split != 0 && found < 0)) {
        printf("solution %lld: %d split far vertices; ", nsol, split);
        if (split == 0) printf("trivial\n");
        else if (found >= 0) printf("line delta = (%d,%d,%d,%d)\n", iso[found][0], iso[found][1], iso[found][2], iso[found][3]);
        else {
            printf("OTHER:");
            for (r = 0; r < 60; r++) printf(" %d", masks[st[r]]);
            printf("\n");
        }
        fflush(stdout);
    }
}

static int propagate(void) {
    int changed = 1, p, i;
    while (changed) {
        changed = 0;
        for (p = 0; p < 180; p++) {
            int lo = 0, hi = 0, c0[5], c1[5];
            for (i = 0; i < 5; i++) {
                int r = pairR[p][i], k = pslot[p][i], d = dom[r];
                c1[i] = (d & S1[r][k]) != 0; c0[i] = (d & ~S1[r][k] & ALL) != 0;
                lo += !c0[i]; hi += c1[i];
            }
            if (!(lo == 0 || (lo <= 3 && 3 <= hi))) return 0;
            for (i = 0; i < 5; i++) {
                int r = pairR[p][i], k = pslot[p][i];
                int lo_o = lo - !c0[i], hi_o = hi - c1[i], nd = dom[r];
                int a1 = (lo_o + 1 <= 3 && 3 <= hi_o + 1), a0 = (lo_o == 0) || (lo_o <= 3 && 3 <= hi_o);
                if (!a1) nd &= ~S1[r][k];
                if (!a0) nd &= S1[r][k];
                if (nd != dom[r]) { dom[r] = nd; changed = 1; if (!nd) return 0; }
            }
        }
    }
    return 1;
}

static void dfs(void) {
    int save[60], r, best = -1, bs = 99, s, d;
    nodes++;
    if (!propagate()) return;
    for (r = 0; r < 60; r++) {
        int c = __builtin_popcount(dom[r]);
        if (c > 1 && c < bs) { bs = c; best = r; }
    }
    if (best < 0) { report(); return; }
    memcpy(save, dom, sizeof dom); d = dom[best];
    for (s = 0; s < 11; s++) if ((d >> s) & 1) {
        dom[best] = 1 << s;
        dfs();
        memcpy(dom, save, sizeof dom);
    }
}

static unsigned long long rs = 88172645463325252ULL;
static double rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (rs >> 11) * (1.0 / 9007199254740992.0); }
/* one random dive (Knuth): returns the estimated number of nodes of the search tree below the current domains */
static double dive(int *maxdepth) {
    double w = 1.0, est = 1.0; int depth = 0;
    for (;;) {
        int r, best = -1, bs = 99, c, pick, s;
        if (!propagate()) break;
        for (r = 0; r < 60; r++) { c = __builtin_popcount(dom[r]); if (c > 1 && c < bs) { bs = c; best = r; } }
        if (best < 0) break;
        w *= bs; est += w; depth++;
        pick = (int)(rnd() * bs);
        for (s = 0; s < 11; s++) if ((dom[best] >> s) & 1) { if (!pick) break; pick--; }
        dom[best] = 1 << s;
    }
    if (depth > *maxdepth) *maxdepth = depth;
    return est;
}

int main(int argc, char **argv) {
    int i, j, k, a, b, r, n = 0, nn = 0, nf = 0, x[4];
    if (argc < 2) { printf("usage: local_enum2 all | cubes | cube <r0> <s> | est <r0> <s> <dives> <seed>\n"); return 1; }
    for (x[0] = 0; x[0] < 3; x[0]++) for (x[1] = 0; x[1] < 3; x[1]++) for (x[2] = 0; x[2] < 3; x[2]++) for (x[3] = 0; x[3] < 3; x[3]++) {
        memcpy(V[n], x, sizeof x); n++;
    }
    for (i = 0; i < 81; i++) for (j = 0; j < 81; j++) {
        int d[4];
        for (k = 0; k < 4; k++) d[k] = (V[j][k] - V[i][k] + 3) % 3;
        adj[i][j] = (i != j) && q(d) == 0;
    }
    for (i = 1; i < 81; i++) { if (adj[0][i]) NP[nn++] = i; else far[nf++] = i; }
    if (nn != 20 || nf != 60) { printf("bad counts\n"); return 1; }
    for (i = 1; i < 81; i++) if (adj[0][i]) {                      /* one representative of each isotropic direction */
        int neg = 0, dup = 0;
        for (j = 1; j < 81; j++) { int s = 1; for (k = 0; k < 4; k++) if ((V[i][k] + V[j][k]) % 3) s = 0; if (s) neg = j; }
        for (j = 0; j < niso; j++) if (memcmp(iso[j], V[neg], sizeof x) == 0) dup = 1;
        if (!dup) { memcpy(iso[niso], V[i], sizeof x); niso++; }
    }
    if (niso != 10) { printf("bad number of isotropic directions %d\n", niso); return 1; }
    for (r = 0; r < 60; r++) {
        int c = 0;
        for (i = 0; i < 20; i++) if (adj[far[r]][NP[i]]) C[r][c++] = NP[i];
        if (c != 6) { printf("bad mu\n"); return 1; }
    }
    masks[0] = 0; k = 1;
    for (i = 0; i < 64; i++) if (!(i & 1) && __builtin_popcount(i) == 3) masks[k++] = i;
    if (k != 11) { printf("bad masks\n"); return 1; }
    for (i = 0; i < 20; i++) for (j = i + 1; j < 20; j++) {
        a = NP[i]; b = NP[j];
        if (adj[a][b]) continue;
        pairN[npair] = 0;
        for (r = 0; r < 60; r++) {
            int pa = -1, pb = -1, s, m = 0;
            for (k = 0; k < 6; k++) { if (C[r][k] == a) pa = k; if (C[r][k] == b) pb = k; }
            if (pa < 0 || pb < 0) continue;
            if (pairN[npair] >= 5) { printf("more than five\n"); return 1; }
            for (s = 0; s < 11; s++) if (((masks[s] >> pa) ^ (masks[s] >> pb)) & 1) m |= 1 << s;
            pairR[npair][pairN[npair]] = r; pslot[npair][pairN[npair]] = nrp[r]; pairN[npair]++;
            rp[r][nrp[r]] = npair; S1[r][nrp[r]] = m; nrp[r]++;
        }
        if (pairN[npair] != 5) { printf("not five\n"); return 1; }
        npair++;
    }
    if (npair != 180) { printf("bad number of pairs\n"); return 1; }
    for (r = 0; r < 60; r++) if (nrp[r] != 15) { printf("bad pairs per far vertex\n"); return 1; }
    if (!strcmp(argv[1], "est")) {                                  /* Knuth estimate of the size of one cube */
        int r0 = atoi(argv[2]), s = atoi(argv[3]), dives = atoi(argv[4]), d, md = 0; double sum = 0, mx = 0, e;
        rs ^= (unsigned long long)atoll(argv[5]) * 2654435761ULL;
        for (d = 0; d < dives; d++) {
            for (r = 0; r < 60; r++) dom[r] = ALL;
            dom[r0] = 1 << s;
            e = dive(&md); sum += e; if (e > mx) mx = e;
        }
        printf("cube far[%d], mask %d: Knuth estimate of the search tree over %d dives: mean %.3e nodes (largest single dive %.3e, max depth %d)\n", r0, masks[s], dives, sum / dives, mx, md);
    } else if (!strcmp(argv[1], "cube")) {                          /* one cube: local_enum2 cube <r0> <state 1..10> */
        int r0 = atoi(argv[2]), s = atoi(argv[3]);
        for (r = 0; r < 60; r++) dom[r] = ALL;
        dom[r0] = 1 << s;
        dfs();
        printf("cube R0 = far[%d] = vertex %d, mask %d: nodes %lld; solutions %lld (other %lld); complete\n", r0, far[r0], masks[s], nodes, nsol, nother);
    } else if (!strcmp(argv[1], "all")) {
        for (r = 0; r < 60; r++) dom[r] = ALL;
        dfs();
        printf("mode all: nodes %lld; solutions %lld (trivial %lld, other %lld); search complete\n", nodes, nsol, ntriv, nother);
        for (i = 0; i < 10; i++) printf("  line delta = (%d,%d,%d,%d): %lld solution(s)\n", iso[i][0], iso[i][1], iso[i][2], iso[i][3], nline[i]);
    } else {
        int r0, s; long long tot = 0, per[60];
        quiet = 1;
        for (r0 = 0; r0 < 60; r0++) {
            long long before = nsol;
            for (s = 1; s < 11; s++) {
                for (r = 0; r < 60; r++) dom[r] = ALL;
                dom[r0] = 1 << s;
                dfs();
            }
            per[r0] = nsol - before; tot += per[r0];
        }
        printf("mode cubes (600 cubes: far vertex R0, partition): nodes %lld; solution instances %lld; of line type %lld; OTHER %lld; trivial %lld\n",
               nodes, nsol, nsol - nother - ntriv, nother, ntriv);
        printf("solutions per forced far vertex:");
        for (r0 = 0; r0 < 60; r0++) printf(" %lld", per[r0]);
        printf("\n");
        for (i = 0; i < 10; i++) printf("  line delta = (%d,%d,%d,%d): found %lld times (24 expected: once per split vertex)\n", iso[i][0], iso[i][1], iso[i][2], iso[i][3], nline[i]);
    }
    return 0;
}
