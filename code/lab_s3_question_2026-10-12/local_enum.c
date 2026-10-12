/* Lab session, 2026-10-12. EXHAUSTIVE enumeration of the local problem at the vertex P = 0 of the Brouwer-Haemers graph
   (see local_vertex.py for the derivation), by a plain depth-first search that does not use any SAT solver and no symmetry.

   BH: V = F_3^4, x ~ y iff q(y - x) = 0, q = x0^2 + x1^2 + x2 x3.   B(x,y) = 2 x0 y0 + 2 x1 y1 + x2 y3 + x3 y2.
   Unknowns: for each of the 60 far vertices R (non-neighbours of P) a state: 0 = "flat", or one of the ten partitions 3+3
   of the six common neighbours C(P,R) (a 6-bit mask of weight 3 whose bit 0 is 0).
   Constraints: for each of the 180 non-adjacent pairs {a, b} inside N(P), the number of far R containing a and b in C(P,R)
   (there are exactly five) whose mask separates a from b is 0 or 3.

   Output: every solution, with the number of split R, and its identification: "trivial", "line <delta>" if the split R are
   exactly the R with B(R, delta) = 0 and the mask of each split R is the partition of C(P,R) by the value of B(Z, delta)
   (delta one of the ten isotropic directions), or "OTHER".
   Memory: a few kilobytes. Build: gcc -O3 -march=native -o local_enum local_enum.c ; run: local_enum [node cap] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int V[81][4], adj[81][81];
static int NP[20], far[60], C[60][6];
static int npair, pairA[180], pairB[180], pairR[180][5], pairN[180];
static int rp[60][15], rpa[60][15], rpb[60][15], nrp[60];
static int masks[11];
static int order[60], state[60], cnt[180], rem[180];
static long long nodes, nsol, cap = -1;
static int iso[10][4], niso;

static int q(const int *x) { return (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3; }
static int Bf(const int *x, const int *y) { return (2 * x[0] * y[0] + 2 * x[1] * y[1] + x[2] * y[3] + x[3] * y[2]) % 3; }

static void report(void) {
    int split = 0, r, d, i, found = -1;
    for (r = 0; r < 60; r++) split += state[r] != 0;
    for (d = 0; d < niso && found < 0; d++) {
        int ok = 1;
        for (r = 0; r < 60 && ok; r++) {
            int m = 0;
            if (Bf(V[far[r]], iso[d]) == 0) {
                int b0 = Bf(V[C[r][0]], iso[d]);
                for (i = 1; i < 6; i++) if (Bf(V[C[r][i]], iso[d]) != b0) m |= 1 << i;
            }
            if (m != masks[state[r]]) ok = 0;
        }
        if (ok) found = d;
    }
    nsol++;
    printf("solution %lld: %d split far vertices; ", nsol, split);
    if (split == 0) printf("trivial\n");
    else if (found >= 0) printf("line delta = (%d,%d,%d,%d)\n", iso[found][0], iso[found][1], iso[found][2], iso[found][3]);
    else {
        printf("OTHER:");
        for (r = 0; r < 60; r++) printf(" %d", masks[state[r]]);
        printf("\n");
    }
    fflush(stdout);
}

static void dfs(int depth) {
    int r, s, k, ok;
    if (depth == 60) { report(); return; }
    r = order[depth];
    for (s = 0; s < 11; s++) {
        int m = masks[s];
        if (cap >= 0 && nodes >= cap) return;
        nodes++; ok = 1;
        for (k = 0; k < 15; k++) {
            int p = rp[r][k], sep = ((m >> rpa[r][k]) ^ (m >> rpb[r][k])) & 1;
            cnt[p] += sep; rem[p]--;
            if (cnt[p] > 3 || ((cnt[p] == 1 || cnt[p] == 2) && cnt[p] + rem[p] < 3)) ok = 0;
        }
        if (ok) { state[r] = s; dfs(depth + 1); }
        for (k = 0; k < 15; k++) {
            int p = rp[r][k], sep = ((m >> rpa[r][k]) ^ (m >> rpb[r][k])) & 1;
            cnt[p] -= sep; rem[p]++;
        }
    }
}

int main(int argc, char **argv) {
    int i, j, k, a, b, r, n = 0, nn = 0, nf = 0, x[4];
    if (argc > 1) cap = atoll(argv[1]);
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
    for (i = 0; i < 20; i++) for (j = i + 1; j < 20; j++) {
        a = NP[i]; b = NP[j];
        if (adj[a][b]) continue;
        pairA[npair] = a; pairB[npair] = b; pairN[npair] = 0;
        for (r = 0; r < 60; r++) {
            int pa = -1, pb = -1;
            for (k = 0; k < 6; k++) { if (C[r][k] == a) pa = k; if (C[r][k] == b) pb = k; }
            if (pa >= 0 && pb >= 0) {
                if (pairN[npair] >= 5) { printf("more than five\n"); return 1; }
                pairR[npair][pairN[npair]++] = r;
                rp[r][nrp[r]] = npair; rpa[r][nrp[r]] = pa; rpb[r][nrp[r]] = pb; nrp[r]++;
            }
        }
        if (pairN[npair] != 5) { printf("not five\n"); return 1; }
        npair++;
    }
    if (npair != 180) { printf("bad number of pairs\n"); return 1; }
    for (r = 0; r < 60; r++) if (nrp[r] != 15) { printf("bad pairs per far vertex\n"); return 1; }
    masks[0] = 0; k = 1;
    for (i = 0; i < 64; i++) if (!(i & 1) && __builtin_popcount(i) == 3) masks[k++] = i;
    if (k != 11) { printf("bad masks\n"); return 1; }
    {                                                               /* static order: most pairs shared with the placed ones */
        int placed[60] = {0}, share[60][60];
        for (i = 0; i < 60; i++) for (j = 0; j < 60; j++) {
            int c = 0, u, w;
            for (u = 0; u < 6; u++) for (w = 0; w < 6; w++) if (C[i][u] == C[j][w]) c++;
            share[i][j] = c * (c - 1) / 2;
        }
        order[0] = 0; placed[0] = 1;
        for (k = 1; k < 60; k++) {
            int best = -1, bs = -1;
            for (i = 0; i < 60; i++) if (!placed[i]) {
                int s = 0;
                for (j = 0; j < k; j++) s += share[i][order[j]];
                if (s > bs) { bs = s; best = i; }
            }
            order[k] = best; placed[best] = 1;
        }
    }
    for (i = 0; i < 180; i++) { cnt[i] = 0; rem[i] = 5; }
    dfs(0);
    printf("nodes %lld; solutions %lld; search %s\n", nodes, nsol, (cap >= 0 && nodes >= cap) ? "STOPPED AT THE NODE CAP (NOT exhaustive)" : "complete (exhaustive)");
    return 0;
}
