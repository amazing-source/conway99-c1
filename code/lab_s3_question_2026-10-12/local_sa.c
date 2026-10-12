/* Lab session, 2026-10-12. Local problem at P = 0 of the Brouwer-Haemers graph (see local_enum2.c for the model):
   stochastic search (simulated annealing) for a local solution in which the block far[0] is in a given state.
   A solution = a state for each of the 60 blocks (0 = flat, 1..10 = partitions 3+3) such that each of the 180 pairs is
   separated by 0 or 3 of its five blocks. Cost = number of pairs whose number of separators is not 0 or 3.
   This is a SEARCH, not a proof: finding nothing proves nothing.
   local_sa <state of far[0], 1..10> <seconds> <seed> [T0] [T1]
   Output: the best cost reached; if 0, the solution (states), the number of split blocks and their types. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

static int V[81][4], adj[81][81];
static int NP[20], far[60], C[60][6];
static int npair, pairN[180], rp[60][15], rpa[60][15], rpb[60][15], nrp[60];
static int masks[11], state[60], cnt[180];
static unsigned long long rs;
static double rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (rs >> 11) * (1.0 / 9007199254740992.0); }
static int q(const int *x) { return (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3; }
static int bad(int c) { return c != 0 && c != 3; }
static int typeB(int r, int s) {            /* 0 flat, 1 type A, 2 type B */
    int m = masks[s], i, j, sep = 0, k;
    if (!s) return 0;
    for (i = 0; i < 6; i++) for (j = i + 1; j < 6; j++) {
        int grid = 1;
        for (k = 0; k < 4; k++) if ((V[C[r][i]][k] + V[C[r][j]][k]) % 3 != V[far[r]][k]) grid = 0;
        if (grid && (((m >> i) ^ (m >> j)) & 1)) sep++;
    }
    return sep == 3 ? 1 : 2;
}

int main(int argc, char **argv) {
    int i, j, k, a, b, r, n = 0, nn = 0, nf = 0, x[4], s0, cost, best;
    double secs, T0 = 1.2, T1 = 0.12; clock_t t0;
    long long moves = 0, restarts = 0;
    if (argc < 4) { printf("usage: local_sa <state 1..10> <seconds> <seed> [T0] [T1]\n"); return 1; }
    s0 = atoi(argv[1]); secs = atof(argv[2]); rs = 88172645463325252ULL ^ (unsigned long long)atoll(argv[3]) * 2654435761ULL;
    if (argc > 4) T0 = atof(argv[4]);
    if (argc > 5) T1 = atof(argv[5]);
    for (x[0] = 0; x[0] < 3; x[0]++) for (x[1] = 0; x[1] < 3; x[1]++) for (x[2] = 0; x[2] < 3; x[2]++) for (x[3] = 0; x[3] < 3; x[3]++) { memcpy(V[n], x, sizeof x); n++; }
    for (i = 0; i < 81; i++) for (j = 0; j < 81; j++) {
        int d[4];
        for (k = 0; k < 4; k++) d[k] = (V[j][k] - V[i][k] + 3) % 3;
        adj[i][j] = (i != j) && q(d) == 0;
    }
    for (i = 1; i < 81; i++) { if (adj[0][i]) NP[nn++] = i; else far[nf++] = i; }
    for (r = 0; r < 60; r++) { int c = 0; for (i = 0; i < 20; i++) if (adj[far[r]][NP[i]]) C[r][c++] = NP[i]; }
    masks[0] = 0; k = 1;
    for (i = 0; i < 64; i++) if (!(i & 1) && __builtin_popcount(i) == 3) masks[k++] = i;
    for (i = 0; i < 20; i++) for (j = i + 1; j < 20; j++) {
        a = NP[i]; b = NP[j];
        if (adj[a][b]) continue;
        for (r = 0; r < 60; r++) {
            int pa = -1, pb = -1;
            for (k = 0; k < 6; k++) { if (C[r][k] == a) pa = k; if (C[r][k] == b) pb = k; }
            if (pa < 0 || pb < 0) continue;
            rp[r][nrp[r]] = npair; rpa[r][nrp[r]] = pa; rpb[r][nrp[r]] = pb; nrp[r]++; pairN[npair]++;
        }
        npair++;
    }
    if (npair != 180) { printf("bad pairs\n"); return 1; }
    t0 = clock(); best = 1000;
    while ((double)(clock() - t0) / CLOCKS_PER_SEC < secs) {
        double T = T0; long long it, len = 4000000;
        restarts++;
        for (r = 0; r < 60; r++) state[r] = (int)(rnd() * 11);
        state[0] = s0;
        memset(cnt, 0, sizeof cnt);
        for (r = 0; r < 60; r++) for (k = 0; k < 15; k++) cnt[rp[r][k]] += ((masks[state[r]] >> rpa[r][k]) ^ (masks[state[r]] >> rpb[r][k])) & 1;
        cost = 0; for (i = 0; i < 180; i++) cost += bad(cnt[i]);
        for (it = 0; it < len && cost > 0; it++) {
            int ns, mo, mn, d = 0;
            T = T0 * pow(T1 / T0, (double)it / len);
            r = 1 + (int)(rnd() * 59); ns = (int)(rnd() * 11);
            if (ns == state[r]) continue;
            mo = masks[state[r]]; mn = masks[ns];
            for (k = 0; k < 15; k++) {
                int p = rp[r][k], so = ((mo >> rpa[r][k]) ^ (mo >> rpb[r][k])) & 1, sn = ((mn >> rpa[r][k]) ^ (mn >> rpb[r][k])) & 1;
                if (so != sn) d += bad(cnt[p] - so + sn) - bad(cnt[p]);
            }
            if (d <= 0 || rnd() < exp(-d / T)) {
                for (k = 0; k < 15; k++) {
                    int p = rp[r][k];
                    cnt[p] += (((mn >> rpa[r][k]) ^ (mn >> rpb[r][k])) & 1) - (((mo >> rpa[r][k]) ^ (mo >> rpb[r][k])) & 1);
                }
                state[r] = ns; cost += d;
            }
            moves++;
        }
        if (cost < best) best = cost;
        if (cost == 0) {
            int ns = 0, nA = 0, nB = 0;
            for (r = 0; r < 60; r++) { int t = typeB(r, state[r]); ns += t != 0; nA += t == 1; nB += t == 2; }
            printf("SOLUTION (cost 0) after %lld restarts: split blocks %d (type A %d, type B %d); states:", restarts, ns, nA, nB);
            for (r = 0; r < 60; r++) printf(" %d", state[r]);
            printf("\n"); fflush(stdout);
            return 0;
        }
    }
    printf("state %d (type %s) of far[0]: no solution found; best cost %d; restarts %lld; moves %lld\n", s0, typeB(0, s0) == 1 ? "A" : "B", best, restarts, moves);
    return 0;
}
