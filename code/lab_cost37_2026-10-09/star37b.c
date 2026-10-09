/* C1, lab session, 2026-10-09. Optimised rank-37 star test for connected, prism-free, torsion-free line balls.
   Same model and same verdicts as star37.c (baseline, a port of the laptop session's search); differences:
     - candidates are (slot a, pair q of the second layer, pair r of the third layer); the norm is evaluated from
       precomputed tables; the structural tests use bit masks;
     - the relation of a chosen member with any candidate is cst[slot] + hq[q] + hr[r] (mod 7) and a table of
       shared points: six table look-ups, no loop;
     - the star vertex U is the near point with the most zero entries of K in the other layers (cheapest stars).
   star37b <seed> <number of balls> <choice of U: 0 = vertex 0, 1 = most zeros> [check]
   With "check" every ball is also run through the baseline search of star37.c on the same U and the numbers of
   candidates and of solutions are compared (and the node counts when the branching rule is the same).
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
static int U;

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
#define MAXC 40000
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

/* ---------- optimised search ---------- */
static int SL[10], NS;                       /* slot points (same layer as U, K[U][a] > 0) */
static int P1[60][2], P2[60][2], NP1, NP2;   /* pairs of the two other layers */
static unsigned char qrel1[60][60], qrel2[60][60];   /* number of common points of two pairs */
typedef struct { unsigned char s, q, r, ap, rsm; } cand_t;
static cand_t cd[MAXC]; static int NC;
static u64 cmask[MAXC];
static unsigned char mod7[256];
static long long nodes, evals; static int nsol;
static int dem[36];
static int *alive[12]; static signed char *tie[12]; static int nalive[12], chosen[10], partner[10];

static void candidates(void) {
    int L[3][12], nl[3] = {0, 0, 0};
    for (int i = 0; i < 36; i++) L[lay[i]][nl[lay[i]]++] = i;
    int lu = lay[U], o1 = (lu + 1) % 3, o2 = (lu + 2) % 3;
    NS = 0; for (int a = 0; a < 12; a++) { int va = L[lu][a]; if (va != U && K[U][va] > 0) SL[NS++] = va; }
    NP1 = NP2 = 0;
    for (int b1 = 0; b1 < 12; b1++) for (int b2 = b1 + 1; b2 < 12; b2++) { int x1 = L[o1][b1], x2 = L[o1][b2]; if (mate[x1] != x2) { P1[NP1][0] = x1; P1[NP1][1] = x2; NP1++; } }
    for (int b1 = 0; b1 < 12; b1++) for (int b2 = b1 + 1; b2 < 12; b2++) { int x1 = L[o2][b1], x2 = L[o2][b2]; if (mate[x1] != x2) { P2[NP2][0] = x1; P2[NP2][1] = x2; NP2++; } }
    for (int i = 0; i < 60; i++) for (int j = 0; j < 60; j++) {
        qrel1[i][j] = (P1[i][0] == P1[j][0]) + (P1[i][0] == P1[j][1]) + (P1[i][1] == P1[j][0]) + (P1[i][1] == P1[j][1]);
        qrel2[i][j] = (P2[i][0] == P2[j][0]) + (P2[i][0] == P2[j][1]) + (P2[i][1] == P2[j][0]) + (P2[i][1] == P2[j][1]);
    }
    /* norm tables: g = S9 + 6 r + sum over ordered pairs of Gm = S9 + sum_k (6 rowsum_k + Gm_kk) + 2 sum_{k<l} Gm_kl */
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
                cd[NC].s = s; cd[NC].q = q; cd[NC].r = r; cd[NC].ap = (((m >> yv) & 1) | ((m >> zv) & 1)) ? 1 : 0;
                cd[NC].rsm = (rowsum[U] + rowsum[va] + rowsum[x1] + rowsum[x2] + rowsum[y1] + rowsum[y2]) % 7; cmask[NC] = m; NC++;
            } } }
}

static void dfs(int depth) {
    nodes++;
    int *a_ = alive[depth]; signed char *ti = tie[depth]; int n = nalive[depth];
    if (depth == 10) {
        for (int w = 0; w < 36; w++) if (dem[w]) return;
        for (int k = 0; k < 10; k++) if (!cd[chosen[k]].ap && partner[k] < 0) return;
        nsol++; return;
    }
    int cnt[36]; memset(cnt, 0, sizeof cnt);
    for (int t = 0; t < n; t++) { const cand_t *c = &cd[a_[t]]; cnt[SL[c->s]]++; cnt[P1[c->q][0]]++; cnt[P1[c->q][1]]++; cnt[P2[c->r][0]]++; cnt[P2[c->r][1]]++; }
    int best = -1;
    for (int w = 0; w < 36; w++) if (dem[w] > 0) { if (cnt[w] < dem[w]) return; if (best < 0 || cnt[w] < cnt[best]) best = w; }
    if (best < 0) return;
    int unp = 0; char has[10]; memset(has, 0, sizeof has);
    for (int t = 0; t < n; t++) if (ti[t] >= 0) has[(int)ti[t]] = 1;
    for (int k = 0; k < depth; k++) if (!cd[chosen[k]].ap && partner[k] < 0) { unp++; if (!has[k]) return; }
    if (unp > 10 - depth) return;
    int *nal = alive[depth + 1]; signed char *nti = tie[depth + 1];
    for (int t = 0; t < n; t++) {
        int i = a_[t], a = ti[t];
        if (!((cmask[i] >> best) & 1ULL)) continue;
        if (a >= 0 && partner[a] >= 0) continue;
        const cand_t *ci = &cd[i]; int pts[6] = {U, SL[ci->s], P1[ci->q][0], P1[ci->q][1], P2[ci->r][0], P2[ci->r][1]};
        int h[36]; for (int z = 0; z < 36; z++) { int s = 0; for (int k = 0; k < 6; k++) s += Gm[pts[k]][z]; h[z] = s + 3 * rowsum[z]; }
        unsigned char hq[60], hr[60], cst[10]; int base = S9 + 3 * ci->rsm - 3 + 70 + h[U];
        for (int q = 0; q < 60; q++) hq[q] = mod7[h[P1[q][0]] + h[P1[q][1]]];
        for (int r = 0; r < 60; r++) hr[r] = mod7[h[P2[r][0]] + h[P2[r][1]]];
        for (int s = 0; s < NS; s++) cst[s] = (base + h[SL[s]]) % 7;
        for (int k = 1; k < 6; k++) dem[pts[k]]--;
        u64 deadm = 0; for (int w = 0; w < 36; w++) if (w != U && dem[w] <= 0) deadm |= 1ULL << w;
        chosen[depth] = i; partner[depth] = a; if (a >= 0) partner[a] = depth;
        const unsigned char *q1 = qrel1[ci->q], *q2 = qrel2[ci->r]; int api = ci->ap, m = 0;
        for (int s = 0; s < n; s++) {
            int j = a_[s]; const cand_t *cj = &cd[j];
            if (cmask[j] & deadm) continue;
            evals++;
            int v = mod7[cst[cj->s] + hq[cj->q] + hr[cj->r]], inter = q1[cj->q] + q2[cj->r], r, b = ti[s];
            if (v == 0) { if (inter > 1) continue; r = 0; }
            else if (v == 1) { if (inter != 0 || api || cj->ap) continue; r = 1; }
            else continue;
            int nbv;
            if (r == 1) { if (b >= 0 || a >= 0) continue; nbv = depth; }
            else { if (b >= 0 && b == a) continue; nbv = b; }
            nal[m] = j; nti[m] = nbv; m++;
        }
        nalive[depth + 1] = m;
        dfs(depth + 1);
        if (a >= 0) partner[a] = -1;
        for (int k = 1; k < 6; k++) dem[pts[k]]++;
    }
}

int main(int argc, char **argv) {
    rs = strtoull(argv[1], 0, 10) * 0x9E3779B97F4A7C15ULL + 1; int NB = atoi(argv[2]); int UMODE = argc > 3 ? atoi(argv[3]) : 0; int CHECK = argc > 4;
    for (int k = 0; k < 12; k++) { alive[k] = malloc(sizeof(int) * MAXC); tie[k] = malloc(MAXC); balive[k] = malloc(sizeof(int) * MAXC); btie[k] = malloc(sizeof(int) * MAXC); }
    for (int i = 0; i < 256; i++) mod7[i] = i % 7;
    long long tried = 0, valid = 0, tors = 0, resid = 0, tested = 0, totnodes = 0, totc = 0, alive_balls = 0, mism = 0, totb = 0; double tsearch = 0, tcand = 0, tinv = 0, tbase = 0;
    while (tested < NB) {
        tried++;
        if (!make_ball()) continue;
        valid++;
        clock_t ci0 = clock(); int det = invert(); tinv += (double)(clock() - ci0) / CLOCKS_PER_SEC;
        if (det == 0) { tors++; continue; }
        if (det == 1 || det == 2 || det == 4) { resid++; continue; }
        U = 0;
        if (UMODE == 1) { int bz = -1; for (int x = 0; x < 36; x++) { int z = 0; for (int k = 0; k < 36; k++) if (lay[k] != lay[x] && K[x][k] == 0) z++; if (z > bz) { bz = z; U = x; } } }
        clock_t c0 = clock();
        S9 = 0; for (int i = 0; i < 36; i++) { rowsum[i] = 0; for (int j = 0; j < 36; j++) rowsum[i] += Gm[i][j]; rowsum[i] %= 7; S9 += rowsum[i]; }
        S9 = 9 * S9 % 7;
        candidates(); clock_t c1 = clock();
        for (int k = 0; k < 36; k++) dem[k] = K[U][k]; dem[U] = 0;
        for (int i = 0; i < NC; i++) { alive[0][i] = i; tie[0][i] = -1; }
        nalive[0] = NC; nodes = 0; nsol = 0;
        dfs(0);
        clock_t c2 = clock();
        tcand += (double)(c1 - c0) / CLOCKS_PER_SEC; tsearch += (double)(c2 - c1) / CLOCKS_PER_SEC;
        tested++; totnodes += nodes; totc += NC; if (nsol) alive_balls++;
        if (CHECK) {
            clock_t b0 = clock(); bcandidates();
            for (int k = 0; k < 36; k++) bdem[k] = K[U][k]; bdem[U] = 0;
            for (int i = 0; i < BNC; i++) { balive[0][i] = i; btie[0][i] = -1; }
            bnalive[0] = BNC; bnodes = 0; bnsol = 0; bdfs(0); tbase += (double)(clock() - b0) / CLOCKS_PER_SEC; totb += bnodes;
            if (BNC != NC || bnsol != nsol || bnodes != nodes) { mism++; if (mism <= 5) printf("MISMATCH ball %lld: candidates %d / %d, solutions %d / %d, nodes %lld / %lld\n", tested, NC, BNC, nsol, bnsol, nodes, bnodes); }
        }
    }
    printf("drawn %lld, valid prism-free connected %lld, torsion %lld, residue discriminant %lld, tested %lld\n", tried, valid, tors, resid, tested);
    printf("mean candidates %.0f, mean nodes %.0f, pair evaluations per ball %.0f, balls with a star %lld\n", (double)totc / tested, (double)totnodes / tested, (double)evals / tested, alive_balls);
    printf("time per tested ball: inverse %.3f ms (per valid ball), candidates %.3f ms, search %.3f ms\n", 1e3 * tinv / valid, 1e3 * tcand / tested, 1e3 * tsearch / tested);
    if (CHECK) printf("cross-check against the baseline search on the same balls and vertices: %lld mismatches; baseline %.3f ms per ball\n", mism, 1e3 * tbase / tested);
    return 0;
}
