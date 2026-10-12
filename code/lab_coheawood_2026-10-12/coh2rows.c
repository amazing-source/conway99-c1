/* C1, lab session, 2026-10-12. The co-Heawood branch WITHOUT any rank hypothesis: two rows at once.

   World (NOTE 17.95): X, Y with the biplane, 15 far vertices, 70 boundary vertices in a 7 x 7 array of cells.
   Base = X + Y + far + the ten boundary neighbours B0 of x_0 (a cubic graph on B0 whose edges are the far vertices;
   33 508 orbits, file written by fano37 with FANO37_DUMP). The cell B1 of x_1 is then completed with the
   combinatorial rules of fano37.c ONLY (no condition modulo 7): a member = 3 far neighbours and 1 or 2 neighbours
   in B0; every far vertex in exactly two triples; every vertex of B0 with its quota of neighbours in B1; common
   neighbours of two members, and of a member and a vertex of B0, bounded as in fano37.c.

   Rank-free condition tested on a complete cell (Codex's note of 12/10, formula (1), re-derived in NOTE 17.101):
   H = 147 x (orthogonal projector on the (-4)-eigenvectors of the graph that vanish on X + Y + far) has
       H_rr = 36 - 6 B_st,   H_rr' = 12 - 21 e - 9 ([s=u] + [t=v]) - 7 q - 3 (B_sv + B_ut)
   (cells (s,t), (u,v); e adjacency; q common far neighbours), is positive semidefinite of rank 16, so the 20 x 20
   block of the two rows B0 + B1 must have rank <= 16 (it has rank <= 18 for free: both rows sum to zero).

   The number of complete cells is far too large to enumerate, so this program SAMPLES: random dives (Knuth's
   estimator: at every member a uniformly random alive candidate, weight = product of the numbers of alive
   candidates), which gives an unbiased estimate of the number N2 of complete cells of the base, and the rank of
   H (modulo the prime 1 000 000 007, a lower bound of nothing but equal to the rational rank with overwhelming
   probability; ranks <= 16 are printed for an exact check) on every completed dive.

   coh2rows <bases_orbits.txt> <index of the base> <number of dives> [seed]
   gcc -O3 -march=native -o coh2rows coh2rows.c          One process, about 20 MB. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <math.h>
typedef unsigned long long u64;
#define MAXC 32768
#define PR 1000000007LL
static const int LINES[7][3] = {{0,1,2},{0,3,4},{0,5,6},{1,3,5},{1,4,6},{2,3,6},{2,4,5}};
static int on(int p, int j) { return LINES[j][0] == p || LINES[j][1] == p || LINES[j][2] == p; }
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static const int FLp[3][2] = {{4, 6}, {5, 8}, {7, 9}};
static int B0lab[10], B1lab[10], quota1[10], quota0[10], adj1[10][10], forb[10][10];
static int TR[455][3], TRm[455];
static int E[15][2], blk0[10];
static int nc[10]; static unsigned short cpm[10][MAXC], ctm[10][MAXC];
static u64 rng = 88172645463325252ULL;
static u64 rnd(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }

static void cell(int point, int *lab) {
    int n = 0;
    for (int j = 0; j < 7; j++) if (!on(point, j)) lab[n++] = j;
    for (int j = 0; j < 7; j++) if (on(point, j)) { lab[n++] = j; lab[n++] = j; }
}

static void candidates(void) {                       /* the combinatorial candidates of fano37.c, without the conditions modulo 7 */
    for (int m = 0; m < 10; m++) {
        int j = B1lab[m], q = quota1[m]; nc[m] = 0;
        for (int a = 0; a < 10; a++) for (int b = (q == 2 ? a + 1 : a); b < (q == 2 ? 10 : a + 1); b++) {
            int pm = (1 << a) | (1 << b);
            if (B0lab[a] == j && j != 0) continue;
            if (q == 2) { if (B0lab[b] == j && j != 0) continue; if (forb[a][b] || (blk0[a] & blk0[b]) || B0lab[a] == B0lab[b]) continue; }
            int nofar = 0; for (int k = 0; k < 15; k++) if (((pm >> E[k][0]) & 1) && ((pm >> E[k][1]) & 1)) nofar |= 1 << k;
            for (int ti = 0; ti < 455; ti++) {
                int tm = TRm[ti]; if (tm & nofar) continue;
                int ok = 1;
                for (int t = 0; t < 10 && ok; t++) if ((B0lab[t] == j) + __builtin_popcount(tm & blk0[t]) > (((pm >> t) & 1) ? 1 : 2)) ok = 0;
                if (!ok) continue;
                if (nc[m] >= MAXC) { fprintf(stderr, "too many candidates\n"); exit(3); }
                cpm[m][nc[m]] = pm; ctm[m][nc[m]] = tm; nc[m]++;
            }
        }
    }
}

static long long rank_mod(long long H[20][20]) {
    static long long Mx[20][20]; int r = 0;
    for (int i = 0; i < 20; i++) for (int j = 0; j < 20; j++) Mx[i][j] = ((H[i][j] % PR) + PR) % PR;
    for (int c = 0; c < 20 && r < 20; c++) {
        int p = -1; for (int i = r; i < 20; i++) if (Mx[i][c]) { p = i; break; }
        if (p < 0) continue;
        if (p != r) for (int j = 0; j < 20; j++) { long long t = Mx[r][j]; Mx[r][j] = Mx[p][j]; Mx[p][j] = t; }
        long long iv = 1, b = Mx[r][c], e = PR - 2; while (e) { if (e & 1) iv = iv * b % PR; b = b * b % PR; e >>= 1; }
        for (int j = 0; j < 20; j++) Mx[r][j] = Mx[r][j] * iv % PR;
        for (int i = 0; i < 20; i++) if (i != r && Mx[i][c]) { long long f = Mx[i][c]; for (int j = 0; j < 20; j++) Mx[i][j] = ((Mx[i][j] - f * Mx[r][j]) % PR + PR) % PR; }
        r++;
    }
    return r;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: coh2rows <bases_orbits.txt> <index> <dives> [seed]\n"); return 1; }
    int idx = atoi(argv[2]); long long dives = atoll(argv[3]); if (argc > 4) rng ^= (u64)atoll(argv[4]) * 0x9E3779B97F4A7C15ULL;
    FILE *f = fopen(argv[1], "r"); if (!f) return 1;
    char line[1024]; int ln = 0, got = 0; long long size = 0;
    while (fgets(line, sizeof line, f)) { if (ln++ == idx) { char *p = line; size = strtoll(p, &p, 10); for (int k = 0; k < 15; k++) { E[k][0] = strtol(p, &p, 10); E[k][1] = strtol(p, &p, 10); } got = 1; break; } }
    fclose(f); if (!got) { fprintf(stderr, "no such base\n"); return 1; }
    cell(0, B0lab); cell(1, B1lab);
    for (int m = 0; m < 10; m++) { quota1[m] = 1 + on(0, B1lab[m]); quota0[m] = 1 + on(1, B0lab[m]); }
    for (int l = 0; l < 3; l++) { int a = FLp[l][0], b = FLp[l][1]; adj1[a][b] = adj1[b][a] = 1; forb[a][b] = forb[b][a] = 1; }
    forb[4][5] = forb[5][4] = forb[6][7] = forb[7][6] = forb[8][9] = forb[9][8] = 1;
    { int n = 0; for (int a = 0; a < 15; a++) for (int b = a + 1; b < 15; b++) for (int c = b + 1; c < 15; c++) { TR[n][0] = a; TR[n][1] = b; TR[n][2] = c; TRm[n] = (1 << a) | (1 << b) | (1 << c); n++; } }
    memset(blk0, 0, sizeof blk0);
    for (int k = 0; k < 15; k++) for (int e = 0; e < 2; e++) blk0[E[k][e]] |= 1 << k;
    candidates();
    printf("base %d (orbit of %lld labelled bases); combinatorial candidates per member of B1:", idx, size); for (int m = 0; m < 10; m++) printf(" %d", nc[m]); printf("\n");
    int ord[10]; for (int m = 0; m < 10; m++) ord[m] = m;
    for (int a = 1; a < 10; a++) { int v = ord[a], b = a; while (b > 0 && nc[ord[b - 1]] > nc[v]) { ord[b] = ord[b - 1]; b--; } ord[b] = v; }
    static int alive[MAXC]; int memb[10]; double t0 = now();
    double sumw = 0, sumw2 = 0; long long done = 0, rankhist[21]; double rankw[21]; memset(rankhist, 0, sizeof rankhist); for (int i = 0; i <= 20; i++) rankw[i] = 0;
    long long depthreach[11]; memset(depthreach, 0, sizeof depthreach);
    for (long long dv = 0; dv < dives; dv++) {
        int fcn[15], bcn[10]; memset(fcn, 0, sizeof fcn); memset(bcn, 0, sizeof bcn); double w = 1; int x;
        for (x = 0; x < 10; x++) {
            int m = ord[x], na = 0;
            for (int c = 0; c < nc[m]; c++) {
                int tm = ctm[m][c], pm = cpm[m][c], ok = 1;
                for (unsigned g = tm; g && ok; g &= g - 1) if (fcn[__builtin_ctz(g)] >= 2) ok = 0;
                for (unsigned g = pm; g && ok; g &= g - 1) { int t = __builtin_ctz(g); if (bcn[t] >= quota0[t]) ok = 0; }
                for (int y = 0; y < x && ok; y++) {
                    int o = ord[y], lim = (adj1[m][o] || B1lab[m] == B1lab[o]) ? 0 : 1;
                    if (__builtin_popcount(tm & ctm[o][memb[y]]) + __builtin_popcount(pm & cpm[o][memb[y]]) > lim) ok = 0;
                }
                if (ok) alive[na++] = c;
            }
            if (!na) break;
            depthreach[x + 1]++;
            int c = alive[rnd() % na]; w *= na; memb[x] = c;
            for (unsigned g = ctm[m][c]; g; g &= g - 1) fcn[__builtin_ctz(g)]++;
            for (unsigned g = cpm[m][c]; g; g &= g - 1) bcn[__builtin_ctz(g)]++;
        }
        if (x < 10) continue;
        done++; sumw += w; sumw2 += w * w;
        /* the 20 x 20 block of H on B0 (positions 0..9) and B1 (members 0..9) */
        long long H[20][20]; int tmm[10], pmm[10];
        for (int y = 0; y < 10; y++) { tmm[ord[y]] = ctm[ord[y]][memb[y]]; pmm[ord[y]] = cpm[ord[y]][memb[y]]; }
        for (int i = 0; i < 20; i++) for (int j = 0; j < 20; j++) {
            int ri = i < 10 ? 0 : 1, rj = j < 10 ? 0 : 1, a = i % 10, b = j % 10;
            int li = ri ? B1lab[a] : B0lab[a], lj = rj ? B1lab[b] : B0lab[b];
            if (i == j) { H[i][j] = 36 - 6 * (!on(ri, li)); continue; }
            int e, q, sg;
            if (ri == rj) {
                sg = 1 + (li == lj);
                if (ri == 0) { e = 0; for (int l = 0; l < 3; l++) if ((FLp[l][0] == a && FLp[l][1] == b) || (FLp[l][0] == b && FLp[l][1] == a)) e = 1; q = __builtin_popcount(blk0[a] & blk0[b]); }
                else { e = adj1[a][b]; q = __builtin_popcount(tmm[a] & tmm[b]); }
            } else {
                int t = ri == 0 ? a : b, m = ri == 0 ? b : a;
                sg = (li == lj); e = (pmm[m] >> t) & 1; q = __builtin_popcount(blk0[t] & tmm[m]);
            }
            H[i][j] = 12 - 21 * e - 9 * sg - 7 * q - 3 * ((!on(ri, lj)) + (!on(rj, li)));
        }
        int rk = (int)rank_mod(H); rankhist[rk]++; rankw[rk] += w;
        if (rk <= 16) {
            printf("RANK %d cell:", rk); for (int m = 0; m < 10; m++) printf(" (%x,%x)", pmm[m], tmm[m]); printf("\n"); fflush(stdout);
        }
    }
    double mean = sumw / dives, var = sumw2 / dives - mean * mean;
    printf("dives %lld, completed %lld; dives alive after each member:", dives, done); for (int d = 1; d <= 10; d++) printf(" %lld", depthreach[d]);
    printf("\nestimated number of complete cells of this base N2 = %.3e (standard error %.1e)\n", mean, sqrt(var / dives));
    printf("rank of the 20 x 20 block of H on the completed dives (count; estimated share of the complete cells):");
    for (int r = 0; r <= 20; r++) if (rankhist[r]) printf("  %d: %lld (%.3f)", r, rankhist[r], rankw[r] / sumw);
    printf("\ntime %.1f s\n", now() - t0);
    return 0;
}
