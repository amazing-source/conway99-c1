/* Lab session, 2026-10-12. Heuristic search for a codeword of maximal weight in the code C of split patterns of BH
   (C = L(Z^1), dimension 460, length 2430; see parity_code.py). Simulated annealing on the line-even edge functions:
   a move toggles two edges of a line. Prints the best weight, the number of flat pairs per direction (30 values) and the
   distribution of the number of flat pairs per vertex for the best word.
   parity_code2 <seconds> <seed> [T0] [T1]       Build: gcc -O3 -march=native -o parity_code2 parity_code2.c -lm */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
static int V[81][4], adj[81][81], eid[81][81], ne, npair, pid[81][81];
static int eu[810], evv[810], pa[2430], pb[2430];
static int bund[810][36], nb[810];
static int gen[810][2], ngen, gl[810][72], ngl[810];
static signed char sp[2430], bestsp[2430];
static unsigned long long rs;
static double rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (rs >> 11) * (1.0 / 9007199254740992.0); }
static int q(const int *x) { return (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3; }
int main(int argc, char **argv) {
    int i, j, k, n = 0, x[4], w = 0, best = 0; double secs, T0 = 3.0, T1 = 0.25; clock_t t0; long long it = 0;
    if (argc < 3) { printf("usage\n"); return 1; }
    secs = atof(argv[1]); rs = 88172645463325252ULL ^ ((unsigned long long)atoll(argv[2]) * 0x9E3779B97F4A7C15ULL);
    if (argc > 3) T0 = atof(argv[3]);
    if (argc > 4) T1 = atof(argv[4]);
    for (x[0] = 0; x[0] < 3; x[0]++) for (x[1] = 0; x[1] < 3; x[1]++) for (x[2] = 0; x[2] < 3; x[2]++) for (x[3] = 0; x[3] < 3; x[3]++) { memcpy(V[n], x, sizeof x); n++; }
    for (i = 0; i < 81; i++) for (j = 0; j < 81; j++) { int d[4]; for (k = 0; k < 4; k++) d[k] = (V[j][k] - V[i][k] + 3) % 3; adj[i][j] = (i != j) && q(d) == 0; }
    for (i = 0; i < 81; i++) for (j = i + 1; j < 81; j++) {
        if (adj[i][j]) { eu[ne] = i; evv[ne] = j; eid[i][j] = eid[j][i] = ne++; }
        else { pa[npair] = i; pb[npair] = j; pid[i][j] = pid[j][i] = npair++; }
    }
    for (i = 0; i < npair; i++) for (k = 0; k < 81; k++) if (adj[pa[i]][k] && adj[pb[i]][k]) { int e1 = eid[pa[i]][k], e2 = eid[k][pb[i]]; bund[e1][nb[e1]++] = i; bund[e2][nb[e2]++] = i; }
    for (i = 0; i < 81; i++) for (j = i + 1; j < 81; j++) if (adj[i][j]) for (k = j + 1; k < 81; k++) if (adj[i][k] && adj[j][k]) {
        int es[3] = { eid[i][j], eid[j][k], eid[i][k] }, a, b;
        for (a = 0; a < 3; a++) for (b = a + 1; b < 3; b++) { gen[ngen][0] = es[a]; gen[ngen][1] = es[b]; ngen++; }
    }
    for (i = 0; i < ngen; i++) {            /* pairs toggled: symmetric difference of the two bundles (disjoint here) */
        static char mark[2430]; memset(mark, 0, sizeof mark);
        for (j = 0; j < 2; j++) for (k = 0; k < nb[gen[i][j]]; k++) mark[bund[gen[i][j]][k]] ^= 1;
        for (k = 0; k < 2430; k++) if (mark[k]) gl[i][ngl[i]++] = k;
    }
    t0 = clock();
    for (;;) {
        double el = (double)(clock() - t0) / CLOCKS_PER_SEC, T; int g, d = 0;
        if (el > secs) break;
        T = T0 * pow(T1 / T0, el / secs);
        for (k = 0; k < 4096; k++) {
            g = (int)(rnd() * ngen); d = ngl[g];
            for (j = 0; j < ngl[g]; j++) d -= 2 * sp[gl[g][j]];
            if (d >= 0 || rnd() < exp(d / T)) {
                for (j = 0; j < ngl[g]; j++) sp[gl[g][j]] ^= 1;
                w += d; if (w > best) { best = w; memcpy(bestsp, sp, sizeof sp); }
            }
            it++;
        }
    }
    printf("seed %s: %lld moves; best weight %d of 2430 (flat pairs %d)\n", argv[2], it, best, 2430 - best);
    {
        int fv[81], hist[61]; memset(fv, 0, sizeof fv); memset(hist, 0, sizeof hist);
        for (i = 0; i < npair; i++) if (!bestsp[i]) { fv[pa[i]]++; fv[pb[i]]++; }
        for (i = 0; i < 81; i++) hist[fv[i]]++;
        printf("flat pairs per vertex (value:count):"); for (i = 0; i <= 60; i++) if (hist[i]) printf(" %d:%d", i, hist[i]); printf("\n");
    }
    return 0;
}
