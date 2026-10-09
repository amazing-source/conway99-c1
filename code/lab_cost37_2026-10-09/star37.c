/* C1, lab session, 2026-10-09. Cost of the rank-37 star test on CONNECTED, prism-free, torsion-free line balls.
   Model (the laptop session's fast.c, connected case: no residual space, no sign):
     ball = cubic graph G on 36 near points, three layers of 12, mates inside the layers, three cross matchings;
     M0 = 3J - 3I + A_G over F_7, Gm = M0^-1 (the ball is skipped when M0 is singular: torsion);
     rank 37 needs det(M0) to be a non-residue mod 7 (3, 5, 6): discriminant filter L23;
     a far neighbour of the near point U is a shadow s = {U, a, b1, b2, c1, c2} (two points per layer) with
        g(s, s) = (3 + 1_s)^T Gm (3 + 1_s) = 0,
     two far neighbours i, j of U:  g(s_i, s_j) - 3 = 0 (non adjacent, at most one common point besides U)
                                              or = 1 (adjacent: only U in common, neither is an apex),
     star of U = 10 shadows covering every near point y exactly K[U][y] times, every non-apex member having exactly
     one adjacent partner.
   The program draws random balls, runs the exhaustive star search at one vertex and reports candidates, nodes, time.
     star37 <seed> <number of balls> <mode>      mode 0: forward filtering only (baseline)
   One process, a few MB. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
typedef unsigned long long u64;
static u64 rs;
static inline u64 rnd(void) { rs ^= rs >> 12; rs ^= rs << 25; rs ^= rs >> 27; return rs * 2685821657736338717ULL; }
static int A[36][36], A2[36][36], K[36][36], Gm[36][36], nb[36][3], mate[36], lay[36];
static u64 amask[36];
#define MAXC 40000
static int mem[MAXC][6], apex[MAXC], rsum[MAXC]; static u64 mask[MAXC]; static int NC;
static int rowsum[36], S9; static int U;
static long long nodes; static int nsol; static int MODE;
static int dem[36];

static void shuffle(int *p, int n) { for (int i = n - 1; i > 0; i--) { int j = rnd() % (i + 1); int t = p[i]; p[i] = p[j]; p[j] = t; } }

static int make_ball(void) {
    int p[3][12];
    for (int l = 0; l < 3; l++) { for (int i = 0; i < 12; i++) p[l][i] = i; shuffle(p[l], 12); }
    memset(A, 0, sizeof A);
    for (int i = 0; i < 36; i++) { lay[i] = i / 12; mate[i] = i ^ 1; A[i][i ^ 1] = 1; }
    for (int l = 0; l < 3; l++) for (int i = 0; i < 12; i++) { int x = 12 * l + i, y = 12 * ((l + 1) % 3) + p[l][i]; A[x][y] = A[y][x] = 1; }
    for (int i = 0; i < 36; i++) { int c = 0; amask[i] = 0; for (int j = 0; j < 36; j++) if (A[i][j]) { if (c < 3) nb[i][c] = j; c++; amask[i] |= 1ULL << j; } if (c != 3) return 0; }
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) A2[i][j] = __builtin_popcountll(amask[i] & amask[j]);
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) {
        if (i == j) { K[i][j] = 10; continue; }
        int same = lay[i] == lay[j];
        if (A[i][j]) { if (A2[i][j] != 0) return 0; }                 /* mates: none; cross edge: no triangle (prism-free) */
        K[i][j] = 2 - A[i][j] - A2[i][j] - same;
        if (K[i][j] < 0) return 0;
    }
    /* no two-layer 4-cycle: the cross neighbours (in one layer) of the two points of a mate pair are not mates */
    for (int x = 0; x < 36; x += 2) for (int a = 0; a < 3; a++) for (int b = 0; b < 3; b++) {
        int y = nb[x][a], z = nb[x + 1][b];
        if (y != x + 1 && z != x && mate[y] == z) return 0;
    }
    /* connected */
    u64 seen = 1, fr = 1;
    while (fr) { int v = __builtin_ctzll(fr); fr &= fr - 1; u64 n = amask[v] & ~seen; seen |= n; fr |= n; }
    if (seen != (1ULL << 36) - 1) return 0;
    return 1;
}

static int inv7[7] = {0, 1, 4, 5, 2, 3, 6};
static int invert(void) {                       /* Gm = M0^-1 mod 7, returns det mod 7 (0 if singular) */
    static int M[36][72]; int det = 1;
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) { M[i][j] = (3 - (i == j ? 3 : 0) + A[i][j]) % 7; M[i][36 + j] = i == j; }
    for (int c = 0; c < 36; c++) {
        int p = -1; for (int r = c; r < 36; r++) if (M[r][c]) { p = r; break; }
        if (p < 0) return 0;
        if (p != c) { for (int j = 0; j < 72; j++) { int t = M[c][j]; M[c][j] = M[p][j]; M[p][j] = t; } det = (7 - det) % 7; }
        det = det * M[c][c] % 7; int iv = inv7[M[c][c]];
        for (int j = 0; j < 72; j++) M[c][j] = M[c][j] * iv % 7;
        for (int r = 0; r < 36; r++) if (r != c && M[r][c]) { int f = M[r][c]; for (int j = 0; j < 72; j++) M[r][j] = (M[r][j] + (7 - f) * M[c][j]) % 7; }
    }
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) Gm[i][j] = M[i][36 + j];
    return det;
}

static void candidates(void) {
    NC = 0; int L[3][12], nl[3] = {0, 0, 0};
    for (int i = 0; i < 36; i++) L[lay[i]][nl[lay[i]]++] = i;
    int lu = lay[U], o1 = (lu + 1) % 3, o2 = (lu + 2) % 3;
    S9 = 0; for (int i = 0; i < 36; i++) { rowsum[i] = 0; for (int j = 0; j < 36; j++) rowsum[i] += Gm[i][j]; rowsum[i] %= 7; S9 += rowsum[i]; }
    S9 = 9 * S9 % 7;
    for (int a = 0; a < 12; a++) {
        int va = L[lu][a]; if (va == U || K[U][va] == 0) continue;
        for (int b1 = 0; b1 < 12; b1++) { int x1 = L[o1][b1]; if (K[U][x1] == 0 || K[va][x1] == 0) continue;
        for (int b2 = b1 + 1; b2 < 12; b2++) { int x2 = L[o1][b2]; if (mate[x1] == x2 || K[U][x2] == 0 || K[va][x2] == 0) continue;
        for (int c1 = 0; c1 < 12; c1++) { int y1 = L[o2][c1]; if (K[U][y1] == 0 || K[va][y1] == 0 || K[x1][y1] == 0 || K[x2][y1] == 0) continue;
        for (int c2 = c1 + 1; c2 < 12; c2++) { int y2 = L[o2][c2]; if (mate[y1] == y2 || K[U][y2] == 0 || K[va][y2] == 0 || K[x1][y2] == 0 || K[x2][y2] == 0) continue;
            int n[6] = {U, va, x1, x2, y1, y2}; u64 m = 0; for (int k = 0; k < 6; k++) m |= 1ULL << n[k];
            int ok = 1;
            for (int k = 0; k < 6 && ok; k++) if (__builtin_popcountll(amask[n[k]] & m) > 1) ok = 0;
            if (!ok) continue;
            for (int z = 0; z < 36 && ok; z++) if (!((m >> z) & 1) && __builtin_popcountll(amask[z] & m) > 2) ok = 0;
            if (!ok) continue;
            int g = S9, r = 0;
            for (int k = 0; k < 6; k++) { r += rowsum[n[k]]; for (int l = 0; l < 6; l++) g += Gm[n[k]][n[l]]; }
            g = (g + 6 * r) % 7;
            if (g) continue;
            if (NC >= MAXC) { fprintf(stderr, "too many candidates\n"); exit(5); }
            memcpy(mem[NC], n, sizeof n); mask[NC] = m; rsum[NC] = r % 7;
            int ap = 0; for (int k = 0; k < 3; k++) if (lay[nb[U][k]] != lu && ((m >> nb[U][k]) & 1)) ap = 1;
            apex[NC] = ap; NC++;
        } } } }
    }
}

/* relation of candidate j with the chosen candidate whose column sums are in h[] and whose row-sum term is hr */
static inline int rel(const int *h, int hr, u64 mi, int api, int j) {
    int s = S9 + 3 * hr + 3 * rsum[j] - 3 + 70;
    for (int k = 0; k < 6; k++) s += h[mem[j][k]];
    int v = s % 7, inter = __builtin_popcountll(mi & mask[j]);
    if (v == 0) return inter > 2 ? -1 : 0;
    if (v == 1) return (inter != 1 || api || apex[j]) ? -1 : 1;
    return -1;
}

static int *alive[12], *tie[12], nalive[12], chosen[10], partner[10];

static void dfs(int depth) {
    nodes++;
    int *a_ = alive[depth], *ti = tie[depth], n = nalive[depth];
    if (depth == 10) {
        for (int w = 0; w < 36; w++) if (dem[w]) return;
        for (int k = 0; k < 10; k++) if (!apex[chosen[k]] && partner[k] < 0) return;
        nsol++; return;
    }
    int cnt[36]; memset(cnt, 0, sizeof cnt);
    for (int t = 0; t < n; t++) for (int k = 1; k < 6; k++) cnt[mem[a_[t]][k]]++;
    int best = -1;
    for (int w = 0; w < 36; w++) if (dem[w] > 0) { if (cnt[w] < dem[w]) return; if (best < 0 || cnt[w] < cnt[best]) best = w; }
    if (best < 0) return;
    int unp = 0; char has[10]; memset(has, 0, sizeof has);
    for (int t = 0; t < n; t++) if (ti[t] >= 0) has[ti[t]] = 1;
    for (int k = 0; k < depth; k++) if (!apex[chosen[k]] && partner[k] < 0) { unp++; if (!has[k]) return; }
    if (unp > 10 - depth) return;
    int *nal = alive[depth + 1], *nti = tie[depth + 1];
    for (int t = 0; t < n; t++) {
        int i = a_[t], a = ti[t];
        if (!((mask[i] >> best) & 1ULL)) continue;
        if (a >= 0 && partner[a] >= 0) continue;
        int h[36]; for (int z = 0; z < 36; z++) { int s = 0; for (int k = 0; k < 6; k++) s += Gm[mem[i][k]][z]; h[z] = s; }
        for (int k = 1; k < 6; k++) dem[mem[i][k]]--;
        chosen[depth] = i; partner[depth] = a; if (a >= 0) partner[a] = depth;
        int m = 0;
        for (int s = 0; s < n; s++) {
            int j = a_[s], b = ti[s];
            if (j == i || mask[j] == mask[i]) continue;
            int okd = 1; for (int k = 1; k < 6; k++) if (dem[mem[j][k]] <= 0) { okd = 0; break; }
            if (!okd) continue;
            int r = rel(h, rsum[i], mask[i], apex[i], j);
            if (r < 0) continue;
            int nbv;
            if (r == 1) { if (b >= 0 || a >= 0) continue; nbv = depth; }
            else { if (b >= 0 && b == a) continue; nbv = b; }
            nal[m] = j; nti[m] = nbv; m++;
        }
        nalive[depth + 1] = m;
        dfs(depth + 1);
        if (a >= 0) partner[a] = -1;
        for (int k = 1; k < 6; k++) dem[mem[i][k]]++;
    }
}

int main(int argc, char **argv) {
    rs = strtoull(argv[1], 0, 10) * 0x9E3779B97F4A7C15ULL + 1; int NB = atoi(argv[2]); MODE = argc > 3 ? atoi(argv[3]) : 0;
    for (int k = 0; k < 12; k++) { alive[k] = malloc(sizeof(int) * MAXC); tie[k] = malloc(sizeof(int) * MAXC); }
    long long tried = 0, valid = 0, tors = 0, resid = 0, tested = 0, totnodes = 0, maxnodes = 0, totc = 0, alive_balls = 0; double tsearch = 0, tcand = 0;
    while (tested < NB) {
        tried++;
        if (!make_ball()) continue;
        valid++;
        int det = invert();
        if (det == 0) { tors++; continue; }
        if (det == 1 || det == 2 || det == 4) { resid++; continue; }
        U = 0;
        clock_t c0 = clock(); candidates(); clock_t c1 = clock();
        for (int k = 0; k < 36; k++) dem[k] = K[U][k]; dem[U] = 0;
        for (int i = 0; i < NC; i++) { alive[0][i] = i; tie[0][i] = -1; }
        nalive[0] = NC; nodes = 0; nsol = 0;
        dfs(0);
        clock_t c2 = clock();
        tcand += (double)(c1 - c0) / CLOCKS_PER_SEC; tsearch += (double)(c2 - c1) / CLOCKS_PER_SEC;
        tested++; totnodes += nodes; totc += NC; if (nodes > maxnodes) maxnodes = nodes; if (nsol) alive_balls++;
        if (tested <= 8) printf("ball %lld: det %d, candidates %d, nodes %lld, solutions %d\n", tested, det, NC, nodes, nsol);
    }
    printf("drawn %lld, valid prism-free connected %lld, torsion %lld, residue discriminant %lld, tested %lld\n", tried, valid, tors, resid, tested);
    printf("mean candidates %.0f, mean nodes %.0f, max nodes %lld, balls with a star %lld\n", (double)totc / tested, (double)totnodes / tested, maxnodes, alive_balls);
    printf("time per ball: candidates %.3f ms, search %.3f ms\n", 1e3 * tcand / tested, 1e3 * tsearch / tested);
    return 0;
}
