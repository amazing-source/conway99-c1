/* C1, lab session, 2026-10-09. Rank-37 star test, version with compatibility rows in bits.
   Same model and same verdicts as star37.c (port of the laptop session search) for connected, prism-free,
   torsion-free line balls. What changes is only the organisation of the search:
     - the ten slots (points of the layer of U with K = 1) are taken in a fixed order, smallest slot first;
       a star takes exactly one candidate in each slot;
     - for a candidate m and a later slot b, the row R(m,b) is a pair of 512-bit sets: candidates of b that are
       non-adjacent-compatible with m (R0) or adjacent-compatible with m (R1). A row is computed only when it is
       needed, 64 candidates per step (AVX-512 VBMI; a scalar version of the same formulas with -DSCALAR);
     - the alive candidates of a slot for a partial star are a 512-bit set obtained from the set of the parent
       by a few word operations with one row; a slot is treated only when the search reaches it.
   Pair relation (as in star37.c): v = g(i,j) - 3 mod 7, shared = points in common besides U;
       v = 0 and shared <= 1: compatible, non adjacent;  v = 1, shared = 0, neither is an apex: compatible, adjacent.
   A partial star is consistent when all pairs are compatible, every member has at most one adjacent partner and no
   near point w is covered more than K[U][w] times. A star = consistent choice in the ten slots where every member
   that is not an apex has its partner (the coverage is then exact because the demands add up to 40 + 10).

   star37c <seed> <balls> <choice of U: 0 = vertex 0, 1 = most zeros of K> [check [depth]]
   check: on every ball (1) the baseline search of star37.c gives its verdict, (2) the numbers of consistent partial
   stars on the first 1..depth slots (default 4) are recounted by brute force from the model formulas and compared
   with the node counts of the fast search.
   One process, about 30 MB (60 MB with check). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#ifndef SCALAR
#include <immintrin.h>
#endif
typedef unsigned long long u64;
static u64 rs;
static inline u64 rnd(void) { rs ^= rs >> 12; rs ^= rs << 25; rs ^= rs >> 27; return rs * 2685821657736338717ULL; }
static int A[36][36], A2[36][36], K[36][36], Gm[36][36], nb[36][3], mate[36], lay[36];
static u64 amask[36];
static int U;
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

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
        if (A[i][j]) { if (A2[i][j] != 0) return 0; }
        K[i][j] = 2 - A[i][j] - A2[i][j] - same;
        if (K[i][j] < 0) return 0;
    }
    for (int x = 0; x < 36; x += 2) for (int a = 0; a < 3; a++) for (int b = 0; b < 3; b++) {
        int y = nb[x][a], z = nb[x + 1][b];
        if (y != x + 1 && z != x && mate[y] == z) return 0;
    }
    u64 seen = 1, fr = 1;
    while (fr) { int v = __builtin_ctzll(fr); fr &= fr - 1; u64 n = amask[v] & ~seen; seen |= n; fr |= n; }
    if (seen != (1ULL << 36) - 1) return 0;
    return 1;
}

static int inv7[7] = {0, 1, 4, 5, 2, 3, 6};
static int invert(void) {
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

/* ---------- baseline search (identical to star37.c), used for the cross-check ---------- */
#define MAXC 8192
static int bmem[MAXC][6], bapex[MAXC], brsum[MAXC]; static u64 bmask[MAXC]; static int BNC;
static int rowsum[36], S9; static long long bnodes; static int bnsol; static int bdem[36];
static int *balive[12], *btie[12], bnalive[12], bchosen[10], bpartner[10];
static void bcandidates(void) {
    BNC = 0; int L[3][12], nl[3] = {0, 0, 0};
    for (int i = 0; i < 36; i++) L[lay[i]][nl[lay[i]]++] = i;
    int lu = lay[U], o1 = (lu + 1) % 3, o2 = (lu + 2) % 3;
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
            memcpy(bmem[BNC], n, sizeof n); bmask[BNC] = m; brsum[BNC] = r % 7;
            int ap = 0; for (int k = 0; k < 3; k++) if (lay[nb[U][k]] != lu && ((m >> nb[U][k]) & 1)) ap = 1;
            bapex[BNC] = ap; BNC++;
        } } } }
    }
}
static inline int brel(const int *h, int hr, u64 mi, int api, int j) {
    int s = S9 + 3 * hr + 3 * brsum[j] - 3 + 70;
    for (int k = 0; k < 6; k++) s += h[bmem[j][k]];
    int v = s % 7, inter = __builtin_popcountll(mi & bmask[j]);
    if (v == 0) return inter > 2 ? -1 : 0;
    if (v == 1) return (inter != 1 || api || bapex[j]) ? -1 : 1;
    return -1;
}
static void bdfs(int depth) {
    bnodes++;
    int *a_ = balive[depth], *ti = btie[depth], n = bnalive[depth];
    if (depth == 10) {
        for (int w = 0; w < 36; w++) if (bdem[w]) return;
        for (int k = 0; k < 10; k++) if (!bapex[bchosen[k]] && bpartner[k] < 0) return;
        bnsol++; return;
    }
    int cnt[36]; memset(cnt, 0, sizeof cnt);
    for (int t = 0; t < n; t++) for (int k = 1; k < 6; k++) cnt[bmem[a_[t]][k]]++;
    int best = -1;
    for (int w = 0; w < 36; w++) if (bdem[w] > 0) { if (cnt[w] < bdem[w]) return; if (best < 0 || cnt[w] < cnt[best]) best = w; }
    if (best < 0) return;
    int unp = 0; char has[10]; memset(has, 0, sizeof has);
    for (int t = 0; t < n; t++) if (ti[t] >= 0) has[ti[t]] = 1;
    for (int k = 0; k < depth; k++) if (!bapex[bchosen[k]] && bpartner[k] < 0) { unp++; if (!has[k]) return; }
    if (unp > 10 - depth) return;
    int *nal = balive[depth + 1], *nti = btie[depth + 1];
    for (int t = 0; t < n; t++) {
        int i = a_[t], a = ti[t];
        if (!((bmask[i] >> best) & 1ULL)) continue;
        if (a >= 0 && bpartner[a] >= 0) continue;
        int h[36]; for (int z = 0; z < 36; z++) { int s = 0; for (int k = 0; k < 6; k++) s += Gm[bmem[i][k]][z]; h[z] = s; }
        for (int k = 1; k < 6; k++) bdem[bmem[i][k]]--;
        bchosen[depth] = i; bpartner[depth] = a; if (a >= 0) bpartner[a] = depth;
        int m = 0;
        for (int s = 0; s < n; s++) {
            int j = a_[s], b = ti[s];
            if (j == i || bmask[j] == bmask[i]) continue;
            int okd = 1; for (int k = 1; k < 6; k++) if (bdem[bmem[j][k]] <= 0) { okd = 0; break; }
            if (!okd) continue;
            int r = brel(h, brsum[i], bmask[i], bapex[i], j);
            if (r < 0) continue;
            int nbv;
            if (r == 1) { if (b >= 0 || a >= 0) continue; nbv = depth; }
            else { if (b >= 0 && b == a) continue; nbv = b; }
            nal[m] = j; nti[m] = nbv; m++;
        }
        bnalive[depth + 1] = m;
        bdfs(depth + 1);
        if (a >= 0) bpartner[a] = -1;
        for (int k = 1; k < 6; k++) bdem[bmem[i][k]]++;
    }
}

/* ---------- reference count of consistent partial stars, straight from the model (check mode only) ---------- */
static signed char *refm;                         /* refm[i * BNC + j] = relation of baseline candidates i, j */
static int refslot[10][1024], refn[10]; static long long refcnt[11]; static int REFD;
static int refrel(int i, int j) {
    int g = S9 + 3 * brsum[i] + 3 * brsum[j];
    for (int k = 0; k < 6; k++) for (int l = 0; l < 6; l++) g += Gm[bmem[i][k]][bmem[j][l]];
    int v = (g - 3 + 70) % 7, shared = __builtin_popcountll(bmask[i] & bmask[j]) - 1;
    if (v == 0 && shared <= 1) return 0;
    if (v == 1 && shared == 0 && !bapex[i] && !bapex[j]) return 1;
    return -1;
}
static void refrec(int d, int *tup) {
    refcnt[d]++;
    if (d == REFD) return;
    for (int t = 0; t < refn[d]; t++) {
        int c = refslot[d][t], ok = 1, adjc = 0, cov[36];
        for (int k = 0; k < d && ok; k++) { int r = refm[(size_t)tup[k] * BNC + c]; if (r < 0) ok = 0; else adjc += r; }
        if (!ok || adjc > 1) continue;
        for (int k = 0; k < d && ok; k++) {          /* no earlier member gets a second adjacent partner */
            if (refm[(size_t)tup[k] * BNC + c] != 1) continue;
            for (int l = 0; l < d; l++) if (l != k && refm[(size_t)tup[k] * BNC + tup[l]] == 1) ok = 0;
        }
        if (!ok) continue;
        memset(cov, 0, sizeof cov); tup[d] = c;
        for (int k = 0; k <= d; k++) for (int l = 1; l < 6; l++) cov[bmem[tup[k]][l]]++;
        for (int w = 0; w < 36 && ok; w++) if (w != U && cov[w] > K[U][w]) ok = 0;
        if (!ok) continue;
        refrec(d + 1, tup);
    }
}

/* ---------- candidates (as in star37b.c) ---------- */
static int SL[10], NS;                       /* slot points (same layer as U, K[U][a] > 0) */
static int P1[60][2], P2[60][2];             /* pairs of the two other layers */
typedef struct { unsigned char s, q, r, ap, rsm; } cand_t;
static cand_t cd0[MAXC], cd[MAXC]; static int NC;
static u64 cmask0[MAXC], cmask[MAXC];
static int soff[11];

static void candidates(void) {
    int L[3][12], nl[3] = {0, 0, 0};
    for (int i = 0; i < 36; i++) L[lay[i]][nl[lay[i]]++] = i;
    int lu = lay[U], o1 = (lu + 1) % 3, o2 = (lu + 2) % 3;
    NS = 0; for (int a = 0; a < 12; a++) { int va = L[lu][a]; if (va != U && K[U][va] > 0) SL[NS++] = va; }
    int np1 = 0, np2 = 0;
    for (int b1 = 0; b1 < 12; b1++) for (int b2 = b1 + 1; b2 < 12; b2++) { int x1 = L[o1][b1], x2 = L[o1][b2]; if (mate[x1] != x2) { P1[np1][0] = x1; P1[np1][1] = x2; np1++; } }
    for (int b1 = 0; b1 < 12; b1++) for (int b2 = b1 + 1; b2 < 12; b2++) { int x1 = L[o2][b1], x2 = L[o2][b2]; if (mate[x1] != x2) { P2[np2][0] = x1; P2[np2][1] = x2; np2++; } }
    /* norm: g = S9 + sum_k (6 rowsum_k + Gm_kk) + 2 sum_{k<l} Gm_kl */
    int one[36]; for (int i = 0; i < 36; i++) one[i] = 6 * rowsum[i] + Gm[i][i];
    int nq[60], nr[60]; static unsigned char nqr[60][60]; u64 okq = 0, okr = 0; static u64 okqr[60];
    for (int q = 0; q < 60; q++) { int x1 = P1[q][0], x2 = P1[q][1]; nq[q] = (one[x1] + one[x2] + 2 * Gm[x1][x2] + 2 * (Gm[U][x1] + Gm[U][x2])) % 7; if (K[U][x1] > 0 && K[U][x2] > 0) okq |= 1ULL << q; }
    for (int r = 0; r < 60; r++) { int y1 = P2[r][0], y2 = P2[r][1]; nr[r] = (one[y1] + one[y2] + 2 * Gm[y1][y2] + 2 * (Gm[U][y1] + Gm[U][y2])) % 7; if (K[U][y1] > 0 && K[U][y2] > 0) okr |= 1ULL << r; }
    for (int q = 0; q < 60; q++) { okqr[q] = 0; int x1 = P1[q][0], x2 = P1[q][1];
        for (int r = 0; r < 60; r++) { int y1 = P2[r][0], y2 = P2[r][1];
            nqr[q][r] = (2 * (Gm[x1][y1] + Gm[x1][y2] + Gm[x2][y1] + Gm[x2][y2])) % 7;
            if (K[x1][y1] > 0 && K[x1][y2] > 0 && K[x2][y1] > 0 && K[x2][y2] > 0) okqr[q] |= 1ULL << r; } }
    NC = 0; int yv = -1, zv = -1; for (int k = 0; k < 3; k++) if (lay[nb[U][k]] == o1) yv = nb[U][k]; else if (lay[nb[U][k]] == o2) zv = nb[U][k];
    for (int s = 0; s < NS; s++) {
        soff[s] = NC;
        int va = SL[s]; int n0 = (S9 + one[U] + one[va] + 2 * Gm[U][va]) % 7;
        for (int q = 0; q < 60; q++) { if (!((okq >> q) & 1)) continue; int x1 = P1[q][0], x2 = P1[q][1]; if (K[va][x1] == 0 || K[va][x2] == 0) continue;
            int nqa = (n0 + nq[q] + 2 * (Gm[va][x1] + Gm[va][x2])) % 7;
            u64 rm = okr & okqr[q];
            while (rm) { int r = __builtin_ctzll(rm); rm &= rm - 1; int y1 = P2[r][0], y2 = P2[r][1];
                if (K[va][y1] == 0 || K[va][y2] == 0) continue;
                if ((nqa + nr[r] + nqr[q][r] + 2 * (Gm[va][y1] + Gm[va][y2])) % 7) continue;
                u64 m = (1ULL << U) | (1ULL << va) | (1ULL << x1) | (1ULL << x2) | (1ULL << y1) | (1ULL << y2); int ok = 1;
                u64 mm = m; while (mm) { int k = __builtin_ctzll(mm); mm &= mm - 1; if (__builtin_popcountll(amask[k] & m) > 1) { ok = 0; break; } }
                if (!ok) continue;
                for (int z = 0; z < 36; z++) if (!((m >> z) & 1) && __builtin_popcountll(amask[z] & m) > 2) { ok = 0; break; }
                if (!ok) continue;
                if (NC >= MAXC) { fprintf(stderr, "too many candidates\n"); exit(5); }
                cd0[NC].s = s; cd0[NC].q = q; cd0[NC].r = r; cd0[NC].ap = (((m >> yv) & 1) | ((m >> zv) & 1)) ? 1 : 0;
                cd0[NC].rsm = (rowsum[U] + rowsum[va] + rowsum[x1] + rowsum[x2] + rowsum[y1] + rowsum[y2]) % 7; cmask0[NC] = m; NC++;
            } } }
    soff[NS] = NC;
}

/* ---------- fast search ---------- */
typedef struct { u64 w[8]; } bs_t;
typedef struct { bs_t r0, r1; } row_t;
static int ord[10], off[11], nsl[10], TOOBIG;                 /* slots in search order; candidates renumbered in that order */
static unsigned char QB[10][512] __attribute__((aligned(64))), RB[10][512] __attribute__((aligned(64)));
static bs_t NAP[10], VAL[10], PT[10][36];
static unsigned char GQ1[36][64] __attribute__((aligned(64))), GQ2[36][64] __attribute__((aligned(64)));
static unsigned char CU1[64] __attribute__((aligned(64))), CU2[64] __attribute__((aligned(64)));
static unsigned char WP1[36][64] __attribute__((aligned(64))), WP2[36][64] __attribute__((aligned(64)));
static unsigned char TQm[MAXC][64] __attribute__((aligned(64))), TRm[MAXC][64] __attribute__((aligned(64)));
static unsigned char cstm[MAXC][10], tdone[MAXC], rdone[MAXC][10];
static row_t (*rows)[10];
static u64 D1, D2;                                            /* near points other than U with demand 1, 2 */
static bs_t AL[11][10] __attribute__((aligned(64))), TI[11][10] __attribute__((aligned(64))); static unsigned LVm[11];
static int memb[10], ptie[10], partner[10];
static u64 c1m[11], c2m[11];
static long long cntd[11], nrows, nprep; static int nsol;
static unsigned char mod7[256];

static void tables(void) {
    /* search order: slots by increasing number of candidates */
    int cnt[10]; for (int s = 0; s < 10; s++) { cnt[s] = soff[s + 1] - soff[s]; ord[s] = s; }
    for (int i = 1; i < 10; i++) { int v = ord[i], j = i; while (j > 0 && cnt[ord[j - 1]] > cnt[v]) { ord[j] = ord[j - 1]; j--; } ord[j] = v; }
    TOOBIG = 0; int g = 0;
    memset(PT, 0, sizeof PT); memset(NAP, 0, sizeof NAP); memset(VAL, 0, sizeof VAL); memset(QB, 0, sizeof QB); memset(RB, 0, sizeof RB);
    for (int p = 0; p < 10; p++) {
        int s = ord[p]; off[p] = g; nsl[p] = cnt[s]; if (cnt[s] > 512) { TOOBIG = 1; return; }
        for (int k = 0; k < cnt[s]; k++, g++) {
            cd[g] = cd0[soff[s] + k]; cmask[g] = cmask0[soff[s] + k];
            QB[p][k] = cd[g].q; RB[p][k] = cd[g].r; VAL[p].w[k >> 6] |= 1ULL << (k & 63);
            if (!cd[g].ap) NAP[p].w[k >> 6] |= 1ULL << (k & 63);
            u64 mm = cmask[g]; while (mm) { int w = __builtin_ctzll(mm); mm &= mm - 1; PT[p][w].w[k >> 6] |= 1ULL << (k & 63); }
        }
    }
    off[10] = g;
    D1 = D2 = 0; for (int w = 0; w < 36; w++) if (w != U) { if (K[U][w] == 1) D1 |= 1ULL << w; else if (K[U][w] == 2) D2 |= 1ULL << w; }
    memset(GQ1, 0, sizeof GQ1); memset(GQ2, 0, sizeof GQ2); memset(WP1, 0, sizeof WP1); memset(WP2, 0, sizeof WP2); memset(CU1, 0, sizeof CU1); memset(CU2, 0, sizeof CU2);
    for (int q = 0; q < 60; q++) {
        int x1 = P1[q][0], x2 = P1[q][1], y1 = P2[q][0], y2 = P2[q][1];
        for (int p = 0; p < 36; p++) { GQ1[p][q] = (Gm[p][x1] + Gm[p][x2]) % 7; GQ2[p][q] = (Gm[p][y1] + Gm[p][y2]) % 7; }
        CU1[q] = (3 * (rowsum[x1] + rowsum[x2]) + GQ1[U][q]) % 7; CU2[q] = (3 * (rowsum[y1] + rowsum[y2]) + GQ2[U][q]) % 7;
        WP1[x1][q] = K[U][x1] == 1 ? 64 : 32; WP1[x2][q] = K[U][x2] == 1 ? 64 : 32;
        WP2[y1][q] = K[U][y1] == 1 ? 64 : 32; WP2[y2][q] = K[U][y2] == 1 ? 64 : 32;
    }
    memset(tdone, 0, NC); memset(rdone, 0, (size_t)NC * 10);
}

/* tables of candidate g: TQ[q] = (sum over the six points of g of the Gm-sums with the pair q) mod 7 + 32 * weight,
   weight = number of points of q shared with g, raised to 2 when a shared point has demand 1 (same for TR) */
static void prep(int g) {
    tdone[g] = 1; nprep++;
    int a = SL[cd[g].s], x1 = P1[cd[g].q][0], x2 = P1[cd[g].q][1], y1 = P2[cd[g].r][0], y2 = P2[cd[g].r][1];
#ifndef SCALAR
    const __m512i lut = _mm512_loadu_si512((const void *)mod7), c64 = _mm512_set1_epi8(64);
    __m512i s = _mm512_load_si512((const void *)CU1);
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ1[a])); s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ1[x1]));
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ1[x2])); s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ1[y1]));
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ1[y2]));
    __m512i w = _mm512_min_epu8(_mm512_add_epi8(_mm512_load_si512((const void *)WP1[x1]), _mm512_load_si512((const void *)WP1[x2])), c64);
    _mm512_store_si512((void *)TQm[g], _mm512_add_epi8(_mm512_permutexvar_epi8(s, lut), w));
    s = _mm512_load_si512((const void *)CU2);
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ2[a])); s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ2[x1]));
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ2[x2])); s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ2[y1]));
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ2[y2]));
    w = _mm512_min_epu8(_mm512_add_epi8(_mm512_load_si512((const void *)WP2[y1]), _mm512_load_si512((const void *)WP2[y2])), c64);
    _mm512_store_si512((void *)TRm[g], _mm512_add_epi8(_mm512_permutexvar_epi8(s, lut), w));
#else
    for (int q = 0; q < 64; q++) {
        int w = WP1[x1][q] + WP1[x2][q]; if (w > 64) w = 64;
        TQm[g][q] = (CU1[q] + GQ1[a][q] + GQ1[x1][q] + GQ1[x2][q] + GQ1[y1][q] + GQ1[y2][q]) % 7 + w;
        w = WP2[y1][q] + WP2[y2][q]; if (w > 64) w = 64;
        TRm[g][q] = (CU2[q] + GQ2[a][q] + GQ2[x1][q] + GQ2[x2][q] + GQ2[y1][q] + GQ2[y2][q]) % 7 + w;
    }
#endif
    int pts[6] = {U, a, x1, x2, y1, y2}, hU = 3 * rowsum[U], base;
    for (int k = 0; k < 6; k++) hU += Gm[pts[k]][U];
    base = S9 + 3 * cd[g].rsm - 3 + 70 + hU;
    for (int p = 0; p < 10; p++) { int z = SL[ord[p]], h = 3 * rowsum[z]; for (int k = 0; k < 6; k++) h += Gm[pts[k]][z]; cstm[g][p] = (base + h) % 7; }
}

/* row of candidate g against the slot in position p: z = TQ[q] + TR[r] + cst = 32 * weight + (value in 0..18);
   non-adjacent-compatible: value in {0, 7, 14} and weight <= 1; adjacent-compatible: value in {1, 8, 15}, weight 0 */
static void mkrow(int g, int p) {
    rdone[g][p] = 1; nrows++;
    if (!tdone[g]) prep(g);
    row_t *R = &rows[g][p]; int n = nsl[p], nap = !cd[g].ap;
#ifndef SCALAR
    const __m512i tq = _mm512_load_si512((const void *)TQm[g]), tr = _mm512_load_si512((const void *)TRm[g]), cs = _mm512_set1_epi8(cstm[g][p]);
    const __m512i lo4 = _mm512_set1_epi8(15), b1 = _mm512_set1_epi8(1), b2 = _mm512_set1_epi8(2);
    const __m512i lutlo = _mm512_broadcast_i32x4(_mm_setr_epi8(1, 2, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1, 2));
    const __m512i luthi = _mm512_broadcast_i32x4(_mm_setr_epi8(3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0));
    for (int c = 0; c < 8; c++) {
        if (c * 64 >= n) { R->r0.w[c] = 0; R->r1.w[c] = 0; continue; }
        __m512i z = _mm512_add_epi8(_mm512_add_epi8(_mm512_permutexvar_epi8(_mm512_load_si512((const void *)(QB[p] + 64 * c)), tq),
                                                    _mm512_permutexvar_epi8(_mm512_load_si512((const void *)(RB[p] + 64 * c)), tr)), cs);
        __m512i res = _mm512_and_si512(_mm512_shuffle_epi8(lutlo, _mm512_and_si512(z, lo4)),
                                       _mm512_shuffle_epi8(luthi, _mm512_and_si512(_mm512_srli_epi16(z, 4), lo4)));
        R->r0.w[c] = _mm512_test_epi8_mask(res, b1) & VAL[p].w[c];
        R->r1.w[c] = nap ? (_mm512_test_epi8_mask(res, b2) & NAP[p].w[c]) : 0;
    }
#else
    memset(R, 0, sizeof *R);
    for (int k = 0; k < n; k++) {
        int z = TQm[g][QB[p][k]] + TRm[g][RB[p][k]] + cstm[g][p], w = z >> 5, v = z & 31;
        if ((v == 0 || v == 7 || v == 14) && w <= 1) R->r0.w[k >> 6] |= 1ULL << (k & 63);
        if ((v == 1 || v == 8 || v == 15) && w == 0 && nap && !cd[off[p] + k].ap) R->r1.w[k >> 6] |= 1ULL << (k & 63);
    }
#endif
}
static inline row_t *getrow(int g, int p) { if (!rdone[g][p]) mkrow(g, p); return &rows[g][p]; }

/* alive candidates of the slot in position b for the partial star memb[0..d-1] (d >= 1), as two 512-bit sets:
   AL = candidates consistent with all the members, TI = candidates adjacent-compatible with some member (their tie).
   One step = one member: a member without partner keeps its non-adjacent candidates and its adjacent candidates that
   have no tie yet; a member that has just taken its partner a keeps only its non-adjacent candidates and removes the
   candidates tied to a; points of demand 2 covered for the second time remove the candidates that contain them.
   A set is computed only when the search reaches the slot. */
static unsigned getset(int d, int b) {
    LVm[d] |= 1u << b;
    const row_t *R = getrow(memb[d - 1], b);
    if (d == 1) {
#ifndef SCALAR
        __m512i r0 = _mm512_loadu_si512((const void *)&R->r0), r1 = _mm512_loadu_si512((const void *)&R->r1);
        __m512i al1 = _mm512_or_si512(r0, r1);
        _mm512_storeu_si512((void *)&AL[1][b], al1); _mm512_storeu_si512((void *)&TI[1][b], r1);
        return _mm512_test_epi64_mask(al1, al1);
#else
        unsigned nz1 = 0;
        for (int c = 0; c < 8; c++) { AL[1][b].w[c] = R->r0.w[c] | R->r1.w[c]; TI[1][b].w[c] = R->r1.w[c]; if (AL[1][b].w[c]) nz1 |= 1u << c; }
        return nz1;
#endif
    }
    if (!((LVm[d - 1] >> b) & 1)) getset(d - 1, b);
    int a = ptie[d - 1]; u64 news = c1m[d - 1] & cmask[memb[d - 1]] & D2;
#ifndef SCALAR
    __m512i al = _mm512_loadu_si512((const void *)&AL[d - 1][b]), ti = _mm512_loadu_si512((const void *)&TI[d - 1][b]);
    __m512i r0 = _mm512_loadu_si512((const void *)&R->r0), r1 = _mm512_loadu_si512((const void *)&R->r1);
    if (a >= 0) al = _mm512_and_si512(al, _mm512_andnot_si512(_mm512_loadu_si512((const void *)&rows[memb[a]][b].r1), r0));
    else { al = _mm512_and_si512(al, _mm512_or_si512(r0, _mm512_andnot_si512(ti, r1))); ti = _mm512_or_si512(ti, r1); }
    while (news) { int w = __builtin_ctzll(news); news &= news - 1; al = _mm512_andnot_si512(_mm512_loadu_si512((const void *)&PT[b][w]), al); }
    _mm512_storeu_si512((void *)&AL[d][b], al); _mm512_storeu_si512((void *)&TI[d][b], ti);
    return _mm512_test_epi64_mask(al, al);
#else
    unsigned nz = 0;
    const bs_t *pa = &AL[d - 1][b], *pt = &TI[d - 1][b];
    for (int c = 0; c < 8; c++) {
        u64 al, ti = pt->w[c];
        if (a >= 0) al = pa->w[c] & R->r0.w[c] & ~rows[memb[a]][b].r1.w[c];
        else { al = pa->w[c] & (R->r0.w[c] | (R->r1.w[c] & ~ti)); ti |= R->r1.w[c]; }
        u64 s2 = news; while (s2) { int w = __builtin_ctzll(s2); s2 &= s2 - 1; al &= ~PT[b][w].w[c]; }
        AL[d][b].w[c] = al; TI[d][b].w[c] = ti; if (al) nz |= 1u << c;
    }
    return nz;
#endif
}

static void dfs(int d) {
    if (d == 10) {
        if ((c1m[10] & D1) != D1 || (c2m[10] & D2) != D2) return;
        for (int k = 0; k < 10; k++) if (!cd[memb[k]].ap && partner[k] < 0) return;
        nsol++; return;
    }
    unsigned nz = getset(d, d);
    const bs_t *al = &AL[d][d], *ti = &TI[d][d]; u64 ub = ~(1ULL << U);
    while (nz) {
        int c = __builtin_ctz(nz); nz &= nz - 1;
        u64 bits = al->w[c];
        while (bits) {
            int k = __builtin_ctzll(bits); bits &= bits - 1;
            int g = off[d] + 64 * c + k, a = -1; u64 cm = cmask[g] & ub;
            if ((ti->w[c] >> k) & 1) for (int m = 0; m < d; m++) if ((rows[memb[m]][d].r1.w[c] >> k) & 1) { a = m; break; }
            cntd[d + 1]++;
            memb[d] = g; ptie[d] = a; partner[d] = a; if (a >= 0) partner[a] = d;
            c2m[d + 1] = c2m[d] | (c1m[d] & cm); c1m[d + 1] = c1m[d] | cm;
            LVm[d + 1] = 0;
            dfs(d + 1);
            if (a >= 0) partner[a] = -1;
        }
    }
}

static void search(void) {
    u64 ub = ~(1ULL << U);
    memset(cntd, 0, sizeof cntd); nsol = 0; cntd[0] = 1;
    for (int k = 0; k < 10; k++) partner[k] = -1;
    for (int i = off[0]; i < off[1]; i++) {
        cntd[1]++;
        memb[0] = i; ptie[0] = -1; c1m[1] = cmask[i] & ub; c2m[1] = 0; LVm[1] = 0;
        dfs(1);
    }
}

int main(int argc, char **argv) {
    rs = strtoull(argv[1], 0, 10) * 0x9E3779B97F4A7C15ULL + 1; int NB = atoi(argv[2]); int UMODE = argc > 3 ? atoi(argv[3]) : 0; int CHECK = argc > 4;
    REFD = argc > 5 ? atoi(argv[5]) : 4;
    rows = malloc(sizeof(row_t[10]) * MAXC);
    if (CHECK) { for (int k = 0; k < 12; k++) { balive[k] = malloc(sizeof(int) * MAXC); btie[k] = malloc(sizeof(int) * MAXC); } refm = malloc((size_t)MAXC * MAXC); }
    for (int i = 0; i < 256; i++) mod7[i] = i % 7;
    long long tried = 0, valid = 0, tors = 0, resid = 0, tested = 0, totc = 0, alive_balls = 0, mism = 0, big = 0, tot[11]; memset(tot, 0, sizeof tot);
    double tsearch = 0, tcand = 0, tinv = 0, ttab = 0, tbase = 0; int maxslot = 0, maxdepth = 0;
    while (tested < NB) {
        tried++;
        if (!make_ball()) continue;
        valid++;
        double t0 = now(); int det = invert(); tinv += now() - t0;
        if (det == 0) { tors++; continue; }
        if (det == 1 || det == 2 || det == 4) { resid++; continue; }
        U = 0;
        if (UMODE == 1) { int bz = -1; for (int x = 0; x < 36; x++) { int z = 0; for (int k = 0; k < 36; k++) if (lay[k] != lay[x] && K[x][k] == 0) z++; if (z > bz) { bz = z; U = x; } } }
        double c0 = now();
        S9 = 0; for (int i = 0; i < 36; i++) { rowsum[i] = 0; for (int j = 0; j < 36; j++) rowsum[i] += Gm[i][j]; rowsum[i] %= 7; S9 += rowsum[i]; }
        S9 = 9 * S9 % 7;
        candidates(); double c1 = now();
        tables(); double c2 = now();
        if (TOOBIG) { big++; fprintf(stderr, "ball %lld: a slot has more than 512 candidates, not handled by this version\n", tested); tested++; continue; }
        search(); double c3 = now();
        tcand += c1 - c0; ttab += c2 - c1; tsearch += c3 - c2;
        tested++; totc += NC; if (nsol) alive_balls++;
        for (int d = 0; d <= 10; d++) { tot[d] += cntd[d]; if (cntd[d] && d > maxdepth) maxdepth = d; }
        for (int p = 0; p < 10; p++) if (nsl[p] > maxslot) maxslot = nsl[p];
        if (CHECK) {
            double b0 = now(); bcandidates();
            for (int k = 0; k < 36; k++) bdem[k] = K[U][k]; bdem[U] = 0;
            for (int i = 0; i < BNC; i++) { balive[0][i] = i; btie[0][i] = -1; }
            bnalive[0] = BNC; bnodes = 0; bnsol = 0; bdfs(0); tbase += now() - b0;
            int bad = (BNC != NC || bnsol != nsol);
            for (int i = 0; i < BNC; i++) for (int j = 0; j < BNC; j++) refm[(size_t)i * BNC + j] = (bmem[i][1] == bmem[j][1]) ? -1 : refrel(i, j);
            for (int p = 0; p < 10; p++) { refn[p] = 0; for (int i = 0; i < BNC; i++) if (bmem[i][1] == SL[ord[p]]) refslot[p][refn[p]++] = i; }
            int tup[10]; memset(refcnt, 0, sizeof refcnt); refrec(0, tup);
            for (int d = 0; d <= REFD; d++) if (refcnt[d] != cntd[d]) bad = 1;
            if (bad) { mism++; if (mism <= 5) { printf("MISMATCH ball %lld: candidates %d / %d, solutions %d / %d; partial stars by depth (fast / reference):", tested, NC, BNC, nsol, bnsol);
                for (int d = 1; d <= REFD; d++) printf(" %lld / %lld", cntd[d], refcnt[d]); printf("\n"); } }
        }
    }
    printf("drawn %lld, valid prism-free connected %lld, torsion %lld, residue discriminant %lld, tested %lld (slot too big: %lld)\n", tried, valid, tors, resid, tested, big);
    printf("mean candidates %.0f, largest slot %d, balls with a star %lld, deepest level reached %d\n", (double)totc / tested, maxslot, alive_balls, maxdepth);
    printf("mean consistent partial stars by depth:"); for (int d = 1; d <= maxdepth; d++) printf(" %.1f", (double)tot[d] / tested); printf("\n");
    printf("per tested ball: rows %.0f, candidate tables %.0f\n", (double)nrows / tested, (double)nprep / tested);
    printf("time: inverse %.4f ms per valid ball; per tested ball: candidates %.4f ms, tables %.4f ms, search %.4f ms\n", 1e3 * tinv / valid, 1e3 * tcand / tested, 1e3 * ttab / tested, 1e3 * tsearch / tested);
    if (CHECK) printf("check: %lld balls differ from the baseline verdict or from the reference counts up to depth %d; baseline search %.3f ms per ball\n", mism, REFD, 1e3 * tbase / tested);
    return 0;
}
