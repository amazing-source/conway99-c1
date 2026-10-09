/* star37f.c: generated from star37d.c by star37f_patch.py (options STAR37_SAT, STAR37_FC, STAR37_CORES, STAR37_PAT,
   STAR37_GREEN: see that file). Without these options the program is star37d.
   C1, lab session, 2026-10-09. Rank-37 star test for connected, prism-free, torsion-free line balls: fast version.
   Model: the one of star37.c (port of the laptop session search); organisation of the search: the one of star37c.c
   (ten slots in a fixed order, compatibility rows of 512 bits computed on demand, alive sets by word operations).
   Added here:
     1. inverse mod 7 and candidate shadows computed 64 bytes at a time;
     2. optional real filters (argument real = 1), valid at every rank. With H = 3I - G the Laplacian of the ball and
        H+ its pseudo-inverse, a far vertex f with shadow n_f has a residual vector rho_f in R^8 (Schur complement of
        7 E_{-4} = 3I - A + J/9 with respect to the 36 near points):
            |rho_f|^2 = 37/12 - n_f^T H+ n_f,     <rho_f, rho_g> = 1/12 - A_fg - n_f^T H+ n_g.
        Used: |rho_f|^2 >= 0 for every candidate; for a partial star, every 2 x 2 minor with the new member and the
        determinant of the whole Gram matrix (sizes 3, 4, 5) must be >= 0. Floating point (doubles) with tolerances
        1e-9 (norm, pairs), 1e-8, 1e-7, 1e-6 (determinants): a tuple is rejected only when the violation exceeds
        the tolerance. Inside the rows a coarser integer version of the pair test (16 bits, 9 units of slack) is
        applied first; it never removes a pair that the exact test keeps.
   With real = 0 the search is exactly the integer search of star37c.c.

   star37d <seed> <balls> <choice of U: 0 = vertex 0, 1 = most zeros of K> <real: 0 | 1> <order: 0 | 1> [check [depth]]
   order = 1: after the first member (smallest slot), the other slots are taken by increasing number of candidates
   compatible with it; order = 0: all slots by increasing size.
   check, on every ball: the fast inverse against plain Gauss-Jordan; the candidate list against the baseline list
   (filtered by the norm bound when real = 1); the verdict of the baseline search of star37.c (integer conditions
   only: no star there implies no star here); the numbers of consistent partial stars on the first 1..depth slots
   (default 4) recounted by brute force from the model formulas (determinants by Gaussian elimination).
   plant (instead of check): positive control. In every ball a combinatorial star is chosen (coverage, shared
   points, matching of the non-apex members) and its 45 pairs are declared compatible; real filters off. The fast
   search must find it, and its numbers of partial stars at every depth and of complete stars must equal those of
   the brute-force reference run to depth 10.
   Environment variable STAR37_TYPE1 set: the random balls may contain 4-cycles of type I (two mate pairs joined by
   two transversal edges, i.e. an edge of the line in a prism); still no triangle in G(T). Default: prism-free.
   Environment variable STAR37_NT set: triangles of G(T) are allowed too (a line parallel to T); the star vertex is
   then taken outside the triangles, so that the star has the same shape (two apexes, four adjacent pairs).
   Compile: gcc -O3 -march=native (AVX-512 BW + VBMI), or -DSCALAR for plain C with the same formulas.
   One process, about 30 MB (100 MB with check). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#ifndef SCALAR
#include <immintrin.h>
#endif
#define AL64 __attribute__((aligned(64)))
typedef unsigned long long u64;
static u64 rs;
static inline u64 rnd(void) { rs ^= rs >> 12; rs ^= rs << 25; rs ^= rs >> 27; return rs * 2685821657736338717ULL; }
static int A[36][36], A2[36][36], K[36][36], Gm[36][36], nb[36][3], mate[36], lay[36];
static u64 amask[36];
static int U, REAL, ORDER, ALLOW4, has4, ALLOW3, has3;
static unsigned char pordI[512][10]; static int pord[10], reffirst;   /* search order of the slots, per first member */
static double Hr[36][36];
static const double BND = 37.0 / 12;
static int SATF, FCD, FCMAXD = 9, GREENONLY, KLIM = 10, STOPFIRST, found;      /* options of star37f, see star37f_patch.py */
static unsigned usedm[11]; static long long nsatk, nfc[11], DMX[11], totn;
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static void shuffle(int *p, int n) { for (int i = n - 1; i > 0; i--) { int j = rnd() % (i + 1); int t = p[i]; p[i] = p[j]; p[j] = t; } }

static int make_ball(void) {
    int p[3][12]; has4 = 0; has3 = 0;
    for (int l = 0; l < 3; l++) { for (int i = 0; i < 12; i++) p[l][i] = i; shuffle(p[l], 12); }
    memset(A, 0, sizeof A);
    for (int i = 0; i < 36; i++) { lay[i] = i / 12; mate[i] = i ^ 1; A[i][i ^ 1] = 1; }
    for (int l = 0; l < 3; l++) for (int i = 0; i < 12; i++) { int x = 12 * l + i, y = 12 * ((l + 1) % 3) + p[l][i]; A[x][y] = A[y][x] = 1; }
    for (int i = 0; i < 36; i++) { int c = 0; amask[i] = 0; for (int j = 0; j < 36; j++) if (A[i][j]) { if (c < 3) nb[i][c] = j; c++; amask[i] |= 1ULL << j; } if (c != 3) return 0; }
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) A2[i][j] = __builtin_popcountll(amask[i] & amask[j]);
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) {
        if (i == j) { K[i][j] = 10; continue; }
        int same = lay[i] == lay[j];
        if (A[i][j]) { if (A2[i][j] != 0) { if (!ALLOW3 || same || A2[i][j] > 1) return 0; has3 = 1; } }   /* triangle of G(T) */
        K[i][j] = 2 - A[i][j] - A2[i][j] - same;
        if (K[i][j] < 0) return 0;
    }
    for (int x = 0; x < 36; x += 2) for (int a = 0; a < 3; a++) for (int b = 0; b < 3; b++) {
        int y = nb[x][a], z = nb[x + 1][b];
        if (y != x + 1 && z != x && mate[y] == z) { if (!ALLOW4) return 0; has4 = 1; }     /* 4-cycle of type I */
    }
    u64 seen = 1, fr = 1;
    while (fr) { int v = __builtin_ctzll(fr); fr &= fr - 1; u64 n = amask[v] & ~seen; seen |= n; fr |= n; }
    if (seen != (1ULL << 36) - 1) return 0;
    return 1;
}

/* ---------- inverse of M0 = 3J - 3I + A mod 7 and its determinant ---------- */
static int inv7[7] = {0, 1, 4, 5, 2, 3, 6};
static int invert_plain(int G[36][36]) {
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
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) G[i][j] = M[i][36 + j];
    return det;
}
#ifndef SCALAR
static unsigned char MULT[7][64] AL64;          /* MULT[f][x] = f x mod 7 for x < 7, repeated in every 16-byte lane */
static int invert(void) {
    static unsigned char M[36][128] AL64; int det = 1;
    memset(M, 0, sizeof M);
    for (int i = 0; i < 36; i++) { for (int j = 0; j < 36; j++) M[i][j] = (3 - (i == j ? 3 : 0) + A[i][j]) % 7; M[i][64 + i] = 1; }
    const __m512i seven = _mm512_set1_epi8(7);
    for (int c = 0; c < 36; c++) {
        int p = -1, pv = 0; for (int r = c; r < 36; r++) if (M[r][c]) { p = r; pv = M[r][c]; break; }
        if (p < 0) return 0;
        __m512i r0 = _mm512_load_si512((const void *)M[p]), r1 = _mm512_load_si512((const void *)(M[p] + 64));
        if (p != c) { _mm512_store_si512((void *)M[p], _mm512_load_si512((const void *)M[c])); _mm512_store_si512((void *)(M[p] + 64), _mm512_load_si512((const void *)(M[c] + 64))); det = (7 - det) % 7; }
        det = det * pv % 7; const __m512i mi = _mm512_load_si512((const void *)MULT[inv7[pv]]);
        r0 = _mm512_shuffle_epi8(mi, r0); r1 = _mm512_shuffle_epi8(mi, r1);
        _mm512_store_si512((void *)M[c], r0); _mm512_store_si512((void *)(M[c] + 64), r1);
        for (int r = 0; r < 36; r++) {
            int f = M[r][c]; if (r == c || !f) continue;
            const __m512i mf = _mm512_load_si512((const void *)MULT[7 - f]);
            __m512i s = _mm512_add_epi8(_mm512_load_si512((const void *)M[r]), _mm512_shuffle_epi8(mf, r0));
            _mm512_store_si512((void *)M[r], _mm512_min_epu8(s, _mm512_sub_epi8(s, seven)));
            s = _mm512_add_epi8(_mm512_load_si512((const void *)(M[r] + 64)), _mm512_shuffle_epi8(mf, r1));
            _mm512_store_si512((void *)(M[r] + 64), _mm512_min_epu8(s, _mm512_sub_epi8(s, seven)));
        }
    }
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) Gm[i][j] = M[i][64 + j];
    return det;
}
#else
static int invert(void) { return invert_plain(Gm); }
#endif

/* real pseudo-inverse of the Laplacian (Gauss-Jordan on H + J/36, positive definite: no pivoting) */
static void real_pinv(void) {
    static double M[36][72] AL64;
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) { M[i][j] = (i == j ? 3.0 : 0.0) - A[i][j] + 1.0 / 36; M[i][36 + j] = i == j; }
    for (int c = 0; c < 36; c++) {
        double iv = 1.0 / M[c][c]; for (int j = 0; j < 72; j++) M[c][j] *= iv;
        for (int r = 0; r < 36; r++) if (r != c) { double f = M[r][c]; for (int j = 0; j < 72; j++) M[r][j] -= f * M[c][j]; }
    }
    for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) Hr[i][j] = M[i][36 + j] - 1.0 / 36;
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
static signed char *refm;                         /* refm[i * BNC + j] = integer relation of baseline candidates i, j */
static int refslot[10][1024], refn[10]; static long long refcnt[11]; static int REFD;
static double refe[MAXC];
static int refrel(int i, int j) {
    int g = S9 + 3 * brsum[i] + 3 * brsum[j];
    for (int k = 0; k < 6; k++) for (int l = 0; l < 6; l++) g += Gm[bmem[i][k]][bmem[j][l]];
    int v = (g - 3 + 70) % 7, shared = __builtin_popcountll(bmask[i] & bmask[j]) - 1;
    if (v == 0 && shared <= 1) return 0;
    if (v == 1 && shared == 0 && !bapex[i] && !bapex[j]) {
        if (SATF) for (int k = 1; k < 6; k++)
            if (__builtin_popcountll(amask[bmem[j][k]] & bmask[i]) > 1 || __builtin_popcountll(amask[bmem[i][k]] & bmask[j]) > 1) return -1;
        return 1;
    }
    return -1;
}
static double refeps(int i, int j) { double e = 0; for (int k = 0; k < 6; k++) for (int l = 0; l < 6; l++) e += Hr[bmem[i][k]][bmem[j][l]]; return e; }
static double gedet(int n, double M[5][5]) {          /* determinant by elimination with partial pivoting */
    double a[5][5], det = 1; memcpy(a, M, sizeof a);
    for (int c = 0; c < n; c++) {
        int p = c; for (int r = c + 1; r < n; r++) if (fabs(a[r][c]) > fabs(a[p][c])) p = r;
        if (a[p][c] == 0.0) return 0.0;
        if (p != c) { for (int j = 0; j < n; j++) { double t = a[c][j]; a[c][j] = a[p][j]; a[p][j] = t; } det = -det; }
        det *= a[c][c];
        for (int r = c + 1; r < n; r++) { double f = a[r][c] / a[c][c]; for (int j = c; j < n; j++) a[r][j] -= f * a[c][j]; }
    }
    return det;
}
static long long refsol;
static void refrec(int d, int *tup) {
    refcnt[d]++;
    if (d == 10) {                                   /* complete star: every member that is not an apex has its partner */
        for (int k = 0; k < 10; k++) { int has = 0; for (int l = 0; l < 10; l++) if (l != k && refm[(size_t)tup[k] * BNC + tup[l]] == 1) has = 1; if (!bapex[tup[k]] && !has) return; }
        refsol++; return;
    }
    if (d == REFD) return;
    int b = d == 0 ? 0 : pordI[reffirst][d];
    for (int t = 0; t < refn[b]; t++) {
        if (d == 0) reffirst = t;
        int c = refslot[b][t], ok = 1, adjc = 0, cov[36];
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
        if (REAL) {
            double M[5][5]; int n = d + 1; double sc = BND - refe[c]; if (sc < 0) sc = 0;
            for (int k = 0; k < d && ok; k++) { double sk = BND - refe[tup[k]]; if (sk < 0) sk = 0;
                double l = 1.0 / 12 - refm[(size_t)tup[k] * BNC + c] - refeps(tup[k], c); if (l * l > sk * sc + 1e-9) ok = 0; }
            if (ok && n >= 3 && n <= 5) {
                for (int x = 0; x < n; x++) for (int y = 0; y < n; y++) {
                    if (x == y) { double s = BND - refe[tup[x]]; M[x][y] = s < 0 ? 0 : s; }
                    else M[x][y] = 1.0 / 12 - refm[(size_t)tup[x] * BNC + tup[y]] - refeps(tup[x], tup[y]);
                }
                if (gedet(n, M) < (n == 3 ? -1e-8 : n == 4 ? -1e-7 : -1e-6)) ok = 0;
            }
            if (!ok) continue;
        }
        refrec(d + 1, tup);
    }
}

/* ---------- tables of the ball for the star at U ---------- */
static int SL[10], NS;                       /* slot points (same layer as U, K[U][a] > 0) */
static int P1[60][2], P2[60][2];             /* pairs of the two other layers */
static int one[36];
static unsigned char GQ1[36][64] AL64, GQ2[36][64] AL64;      /* (Gm[p][x1] + Gm[p][x2]) mod 7 for the pair q */
static u64 KQ1[36], KQ2[36];                                  /* pairs both points of which have K[p][.] > 0 */
static double HQ1f[36][64], HQ2f[36][64], dq1[64], dq2[64];   /* same sums for H+; H+-norm of a pair */
static short HQ1s[36][64] AL64, HQ2s[36][64] AL64;            /* 2048 * (the same sums), rounded, 16 bits */
static unsigned char mod7[256] AL64;

static void ball_tables(void) {
    int L[3][12], nl[3] = {0, 0, 0};
    for (int i = 0; i < 36; i++) L[lay[i]][nl[lay[i]]++] = i;
    int lu = lay[U], o1 = (lu + 1) % 3, o2 = (lu + 2) % 3;
    S9 = 0; for (int i = 0; i < 36; i++) { rowsum[i] = 0; for (int j = 0; j < 36; j++) rowsum[i] += Gm[i][j]; rowsum[i] %= 7; S9 += rowsum[i]; }
    S9 = 9 * S9 % 7;
    NS = 0; for (int a = 0; a < 12; a++) { int va = L[lu][a]; if (va != U && K[U][va] > 0) SL[NS++] = va; }
    int np1 = 0, np2 = 0;
    for (int b1 = 0; b1 < 12; b1++) for (int b2 = b1 + 1; b2 < 12; b2++) { int x1 = L[o1][b1], x2 = L[o1][b2]; if (mate[x1] != x2) { P1[np1][0] = x1; P1[np1][1] = x2; np1++; } }
    for (int b1 = 0; b1 < 12; b1++) for (int b2 = b1 + 1; b2 < 12; b2++) { int x1 = L[o2][b1], x2 = L[o2][b2]; if (mate[x1] != x2) { P2[np2][0] = x1; P2[np2][1] = x2; np2++; } }
    for (int i = 0; i < 36; i++) one[i] = (6 * rowsum[i] + Gm[i][i]) % 7;
    memset(GQ1, 0, sizeof GQ1); memset(GQ2, 0, sizeof GQ2);
    for (int p = 0; p < 36; p++) {
        u64 k1 = 0, k2 = 0;
        for (int q = 0; q < 60; q++) {
            int x1 = P1[q][0], x2 = P1[q][1], y1 = P2[q][0], y2 = P2[q][1];
            GQ1[p][q] = (Gm[p][x1] + Gm[p][x2]) % 7; GQ2[p][q] = (Gm[p][y1] + Gm[p][y2]) % 7;
            if (K[p][x1] > 0 && K[p][x2] > 0) k1 |= 1ULL << q;
            if (K[p][y1] > 0 && K[p][y2] > 0) k2 |= 1ULL << q;
        }
        KQ1[p] = k1; KQ2[p] = k2;
    }
    if (REAL) {
        memset(HQ1s, 0, sizeof HQ1s); memset(HQ2s, 0, sizeof HQ2s);
        for (int q = 0; q < 60; q++) {
            int x1 = P1[q][0], x2 = P1[q][1], y1 = P2[q][0], y2 = P2[q][1];
            dq1[q] = Hr[x1][x1] + Hr[x2][x2] + 2 * Hr[x1][x2]; dq2[q] = Hr[y1][y1] + Hr[y2][y2] + 2 * Hr[y1][y2];
            for (int p = 0; p < 36; p++) {
                HQ1f[p][q] = Hr[p][x1] + Hr[p][x2]; HQ2f[p][q] = Hr[p][y1] + Hr[p][y2];
                HQ1s[p][q] = (short)lrint(2048.0 * HQ1f[p][q]); HQ2s[p][q] = (short)lrint(2048.0 * HQ2f[p][q]);
            }
        }
    }
}

/* ---------- candidates: (slot a, pair q of the second layer, pair r of the third layer) ---------- */
typedef struct { unsigned char s, q, r, ap, rsm; } cand_t;
static cand_t cd0[MAXC], cd[MAXC]; static int NC;
static u64 cmask0[MAXC], cmask[MAXC]; static double ce0[MAXC];
static int soff[11];

/* structure of a shadow m: a member has at most one neighbour inside, an outside point at most two */
static inline int shadow_ok(u64 m) {
    u64 c1 = 0, c2 = 0, c4 = 0, mm = m;
    while (mm) { u64 a = amask[__builtin_ctzll(mm)]; mm &= mm - 1; u64 t = c1 & a; c1 ^= a; u64 u = c2 & t; c2 ^= t; c4 |= u; }
    return !((c2 | c4) & m) && !(((c1 & c2) | c4) & ~m);
}
static inline double shadow_e(int va, int q, int r) {
    int x1 = P1[q][0], x2 = P1[q][1];
    return Hr[U][U] + Hr[va][va] + 2 * Hr[U][va] + dq1[q] + dq2[r] + 2 * (HQ1f[U][q] + HQ1f[va][q] + HQ2f[U][r] + HQ2f[va][r] + HQ2f[x1][r] + HQ2f[x2][r]);
}
static void candidates(void) {
    int lu = lay[U], o1 = (lu + 1) % 3, o2 = (lu + 2) % 3;
    int yv = -1, zv = -1; for (int k = 0; k < 3; k++) if (lay[nb[U][k]] == o1) yv = nb[U][k]; else if (lay[nb[U][k]] == o2) zv = nb[U][k];
    int nq[64], nr[64]; memset(nq, 0, sizeof nq); memset(nr, 0, sizeof nr);
    for (int q = 0; q < 60; q++) {
        int x1 = P1[q][0], x2 = P1[q][1], y1 = P2[q][0], y2 = P2[q][1];
        nq[q] = (one[x1] + one[x2] + 2 * Gm[x1][x2] + 2 * GQ1[U][q]) % 7; nr[q] = (one[y1] + one[y2] + 2 * Gm[y1][y2] + 2 * GQ2[U][q]) % 7;
    }
    NC = 0;
#ifndef SCALAR
    static unsigned char B[60][64] AL64, NRb[64] AL64;
    for (int r = 0; r < 64; r++) NRb[r] = nr[r];
    const __m512i lut = _mm512_load_si512((const void *)mod7), nrv = _mm512_load_si512((const void *)NRb), zero = _mm512_setzero_si512();
    u64 okq = KQ1[U];
    for (int q = 0; q < 60; q++) if ((okq >> q) & 1) {
        __m512i t = _mm512_add_epi8(_mm512_load_si512((const void *)GQ2[P1[q][0]]), _mm512_load_si512((const void *)GQ2[P1[q][1]]));
        t = _mm512_add_epi8(_mm512_add_epi8(t, t), _mm512_add_epi8(nrv, _mm512_set1_epi8(nq[q])));
        _mm512_store_si512((void *)B[q], _mm512_permutexvar_epi8(t, lut));
    }
    for (int s = 0; s < NS; s++) {
        soff[s] = NC;
        int va = SL[s]; int n0 = (S9 + one[U] + one[va] + 2 * Gm[U][va]) % 7;
        const __m512i a2 = _mm512_add_epi8(_mm512_load_si512((const void *)GQ2[va]), _mm512_load_si512((const void *)GQ2[va]));
        u64 qm = okq & KQ1[va], rbase = KQ2[U] & KQ2[va] & ((1ULL << 60) - 1);
        while (qm) {
            int q = __builtin_ctzll(qm); qm &= qm - 1; int x1 = P1[q][0], x2 = P1[q][1];
            __m512i sum = _mm512_add_epi8(_mm512_add_epi8(_mm512_load_si512((const void *)B[q]), a2), _mm512_set1_epi8((n0 + 2 * GQ1[va][q]) % 7));
            u64 rm = _mm512_cmpeq_epi8_mask(_mm512_permutexvar_epi8(sum, lut), zero) & rbase & KQ2[x1] & KQ2[x2];
            u64 mq = (1ULL << U) | (1ULL << va) | (1ULL << x1) | (1ULL << x2);
            while (rm) {
                int r = __builtin_ctzll(rm); rm &= rm - 1; int y1 = P2[r][0], y2 = P2[r][1];
                u64 m = mq | (1ULL << y1) | (1ULL << y2);
                if (!shadow_ok(m)) continue;
                double e = 0;
                if (REAL) { e = shadow_e(va, q, r); if (e > BND + 1e-9) continue; }
                if (NC >= MAXC) { fprintf(stderr, "too many candidates\n"); exit(5); }
                cd0[NC].s = s; cd0[NC].q = q; cd0[NC].r = r; cd0[NC].ap = (((m >> yv) & 1) | ((m >> zv) & 1)) ? 1 : 0;
                cd0[NC].rsm = (rowsum[U] + rowsum[va] + rowsum[x1] + rowsum[x2] + rowsum[y1] + rowsum[y2]) % 7; cmask0[NC] = m; ce0[NC] = e; NC++;
            }
        }
    }
#else
    for (int s = 0; s < NS; s++) {
        soff[s] = NC;
        int va = SL[s]; int n0 = (S9 + one[U] + one[va] + 2 * Gm[U][va]) % 7;
        for (int q = 0; q < 60; q++) { if (!((KQ1[U] >> q) & 1) || !((KQ1[va] >> q) & 1)) continue; int x1 = P1[q][0], x2 = P1[q][1];
            for (int r = 0; r < 60; r++) { int y1 = P2[r][0], y2 = P2[r][1];
                if (!((KQ2[U] >> r) & 1) || !((KQ2[va] >> r) & 1) || !((KQ2[x1] >> r) & 1) || !((KQ2[x2] >> r) & 1)) continue;
                if ((n0 + nq[q] + 2 * GQ1[va][q] + nr[r] + 2 * (GQ2[x1][r] + GQ2[x2][r]) + 2 * GQ2[va][r]) % 7) continue;
                u64 m = (1ULL << U) | (1ULL << va) | (1ULL << x1) | (1ULL << x2) | (1ULL << y1) | (1ULL << y2);
                if (!shadow_ok(m)) continue;
                double e = 0;
                if (REAL) { e = shadow_e(va, q, r); if (e > BND + 1e-9) continue; }
                if (NC >= MAXC) { fprintf(stderr, "too many candidates\n"); exit(5); }
                cd0[NC].s = s; cd0[NC].q = q; cd0[NC].r = r; cd0[NC].ap = (((m >> yv) & 1) | ((m >> zv) & 1)) ? 1 : 0;
                cd0[NC].rsm = (rowsum[U] + rowsum[va] + rowsum[x1] + rowsum[x2] + rowsum[y1] + rowsum[y2]) % 7; cmask0[NC] = m; ce0[NC] = e; NC++;
            } } }
#endif
    soff[NS] = NC;
}

/* ---------- fast search ---------- */
typedef struct { u64 w[8]; } bs_t;
typedef struct { bs_t r0, r1; } row_t;
static int ord[10], off[11], nsl[10], TOOBIG;                 /* slots in search order; candidates renumbered in that order */
static unsigned char QB[10][512] AL64, RB[10][512] AL64;
static unsigned short TJ[10][512] AL64;                       /* ceil(16384 |rho|) + 1 of the candidates of a slot */
static bs_t NAP[10], VAL[10], PT[10][36];
static unsigned char CU1[64] AL64, CU2[64] AL64, WP1[36][64] AL64, WP2[36][64] AL64;
static unsigned char cpts[MAXC][6]; static double cS[MAXC];   /* points and squared residual norm of a candidate */
static unsigned short ridx[MAXC][10]; static row_t rowpool[65536] AL64; static int nrowpool;
static u64 D1, D2;                                            /* near points other than U with demand 1, 2 */
static bs_t AL[11][10] AL64, TI[11][10] AL64; static unsigned LVm[11];
static int memb[10], ptie[10], partner[10];
static u64 c1m[11], c2m[11];
static int mg[10]; static unsigned char hvok[10];
static double hv[10][40] AL64, sM[10], LG[10][10];            /* members: sums of rows of H+, squared norms, Gram */
static long long cntd[11], nrows, nsteps, nrej; static int nsol;
static u64 SATm[MAXC]; static bs_t PS[10][36];              /* points with two G-neighbours in a shadow; candidates of a slot by such point */
static int PLANT, plantg[10], plantpartner[10], cpos[MAXC]; static long long plnodes;   /* positive control, see main */

static void slot_tables(void) {
    int cnt[10]; for (int s = 0; s < 10; s++) { cnt[s] = soff[s + 1] - soff[s]; ord[s] = s; }
    for (int i = 1; i < 10; i++) { int v = ord[i], j = i; while (j > 0 && cnt[ord[j - 1]] > cnt[v]) { ord[j] = ord[j - 1]; j--; } ord[j] = v; }
    TOOBIG = 0; int g = 0;
    memset(PT, 0, sizeof PT); memset(NAP, 0, sizeof NAP); memset(VAL, 0, sizeof VAL); memset(QB, 0, sizeof QB); memset(RB, 0, sizeof RB); memset(TJ, 0, sizeof TJ);
    if (SATF) memset(PS, 0, sizeof PS);
    for (int p = 0; p < 10; p++) {
        int s = ord[p]; off[p] = g; nsl[p] = cnt[s]; if (cnt[s] > 512) { TOOBIG = 1; return; }
        for (int k = 0; k < cnt[s]; k++, g++) {
            cd[g] = cd0[soff[s] + k]; cmask[g] = cmask0[soff[s] + k]; cpos[g] = p;
            cpts[g][0] = U; cpts[g][1] = SL[s]; cpts[g][2] = P1[cd[g].q][0]; cpts[g][3] = P1[cd[g].q][1]; cpts[g][4] = P2[cd[g].r][0]; cpts[g][5] = P2[cd[g].r][1];
            double sv = BND - ce0[soff[s] + k]; if (sv < 0) sv = 0; cS[g] = sv;
            if (REAL) TJ[p][k] = (unsigned short)(ceil(16384.0 * sqrt(sv)) + 1);
            QB[p][k] = cd[g].q; RB[p][k] = cd[g].r; VAL[p].w[k >> 6] |= 1ULL << (k & 63);
            if (!cd[g].ap) NAP[p].w[k >> 6] |= 1ULL << (k & 63);
            u64 mm = cmask[g]; while (mm) { int w = __builtin_ctzll(mm); mm &= mm - 1; PT[p][w].w[k >> 6] |= 1ULL << (k & 63); }
            if (SATF) { u64 sat = 0, once = 0, m2 = cmask[g]; while (m2) { u64 a = amask[__builtin_ctzll(m2)]; m2 &= m2 - 1; sat |= once & a; once |= a; }
                SATm[g] = sat; while (sat) { int w = __builtin_ctzll(sat); sat &= sat - 1; PS[p][w].w[k >> 6] |= 1ULL << (k & 63); } }
        }
    }
    off[10] = g;
    D1 = D2 = 0; for (int w = 0; w < 36; w++) if (w != U) { if (K[U][w] == 1) D1 |= 1ULL << w; else if (K[U][w] == 2) D2 |= 1ULL << w; }
    memset(WP1, 0, sizeof WP1); memset(WP2, 0, sizeof WP2); memset(CU1, 0, sizeof CU1); memset(CU2, 0, sizeof CU2);
    for (int q = 0; q < 60; q++) {
        int x1 = P1[q][0], x2 = P1[q][1], y1 = P2[q][0], y2 = P2[q][1];
        CU1[q] = (3 * (rowsum[x1] + rowsum[x2]) + GQ1[U][q]) % 7; CU2[q] = (3 * (rowsum[y1] + rowsum[y2]) + GQ2[U][q]) % 7;
        WP1[x1][q] = K[U][x1] == 1 ? 64 : 32; WP1[x2][q] = K[U][x2] == 1 ? 64 : 32;
        WP2[y1][q] = K[U][y1] == 1 ? 64 : 32; WP2[y2][q] = K[U][y2] == 1 ? 64 : 32;
    }
    memset(ridx, 0, (size_t)NC * sizeof ridx[0]); nrowpool = 1;
}

/* Row of candidate g against the slot in position p.
   Integer part: z = TQ[q] + TR[r] + cst = 32 * weight + (value in 0..18), TQ[q] = (sum over the six points of g of the
   Gm-sums with the pair q) mod 7 + 32 * (number of points of q shared with g, raised to 2 when a shared point has
   demand 1); non-adjacent-compatible: value in {0, 7, 14} and weight <= 1; adjacent-compatible: value in {1, 8, 15}
   and weight 0, neither an apex.
   Real part (real = 1): eps = n_g^T H+ n_j in units of 1/2048, from rounded tables (error below 7 units, sums taken
   mod 2^16, the true value is below 6400); kept when |2048 c - eps| <= 2048 |rho_g| |rho_j| + 9, c = 1/12 or -11/12. */
static row_t *mkrow(int g, int p) {
    if (nrowpool >= 65535) { fprintf(stderr, "row pool full\n"); exit(6); }
    ridx[g][p] = nrowpool; row_t *R = &rowpool[nrowpool++]; nrows++;
    const unsigned char *pt = cpts[g]; int a = pt[1], x1 = pt[2], x2 = pt[3], y1 = pt[4], y2 = pt[5], n = nsl[p], nap = !cd[g].ap, sp = SL[ord[p]];
    int hU = 3 * rowsum[U], hS = 3 * rowsum[sp]; for (int k = 0; k < 6; k++) { hU += Gm[pt[k]][U]; hS += Gm[pt[k]][sp]; }
    int cst = (S9 + 3 * cd[g].rsm - 3 + 70 + hU + hS) % 7, c0e = 0, c1e = 0, Ti = 0;
    if (REAL) {
        double es = 0; for (int k = 0; k < 6; k++) es += Hr[pt[k]][U] + Hr[pt[k]][sp];
        int esq = (int)lrint(2048.0 * es); c0e = 171 - esq; c1e = -1877 - esq; Ti = (int)ceil(8192.0 * sqrt(cS[g])) + 1;
    }
#ifndef SCALAR
    const __m512i lut = _mm512_load_si512((const void *)mod7), c64 = _mm512_set1_epi8(64);
    __m512i s = _mm512_load_si512((const void *)CU1);
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ1[a])); s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ1[x1]));
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ1[x2])); s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ1[y1]));
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ1[y2]));
    const __m512i tq = _mm512_add_epi8(_mm512_permutexvar_epi8(s, lut), _mm512_min_epu8(_mm512_add_epi8(_mm512_load_si512((const void *)WP1[x1]), _mm512_load_si512((const void *)WP1[x2])), c64));
    s = _mm512_load_si512((const void *)CU2);
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ2[a])); s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ2[x1]));
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ2[x2])); s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ2[y1]));
    s = _mm512_add_epi8(s, _mm512_load_si512((const void *)GQ2[y2]));
    const __m512i tr = _mm512_add_epi8(_mm512_permutexvar_epi8(s, lut), _mm512_min_epu8(_mm512_add_epi8(_mm512_load_si512((const void *)WP2[y1]), _mm512_load_si512((const void *)WP2[y2])), c64));
    const __m512i cs = _mm512_set1_epi8(cst), lo4 = _mm512_set1_epi8(15), b1 = _mm512_set1_epi8(1), b2 = _mm512_set1_epi8(2);
    const __m512i lutlo = _mm512_broadcast_i32x4(_mm_setr_epi8(1, 2, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1, 2));
    const __m512i luthi = _mm512_broadcast_i32x4(_mm_setr_epi8(3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0));
    __m512i eq0 = _mm512_setzero_si512(), eq1 = eq0, er0 = eq0, er1 = eq0;
    if (REAL) for (int k = 0; k < 6; k++) {
        eq0 = _mm512_add_epi16(eq0, _mm512_load_si512((const void *)HQ1s[pt[k]])); eq1 = _mm512_add_epi16(eq1, _mm512_load_si512((const void *)(HQ1s[pt[k]] + 32)));
        er0 = _mm512_add_epi16(er0, _mm512_load_si512((const void *)HQ2s[pt[k]])); er1 = _mm512_add_epi16(er1, _mm512_load_si512((const void *)(HQ2s[pt[k]] + 32)));
    }
    const __m512i v0 = _mm512_set1_epi16((short)c0e), v1 = _mm512_set1_epi16((short)c1e), tiv = _mm512_set1_epi16((short)Ti), nine = _mm512_set1_epi16(9);
    for (int c = 0; c < 8; c++) {
        if (c * 64 >= n) { R->r0.w[c] = 0; R->r1.w[c] = 0; continue; }
        const __m512i iq = _mm512_load_si512((const void *)(QB[p] + 64 * c)), ir = _mm512_load_si512((const void *)(RB[p] + 64 * c));
        __m512i z = _mm512_add_epi8(_mm512_add_epi8(_mm512_permutexvar_epi8(iq, tq), _mm512_permutexvar_epi8(ir, tr)), cs);
        __m512i res = _mm512_and_si512(_mm512_shuffle_epi8(lutlo, _mm512_and_si512(z, lo4)),
                                       _mm512_shuffle_epi8(luthi, _mm512_and_si512(_mm512_srli_epi16(z, 4), lo4)));
        u64 m0 = _mm512_test_epi8_mask(res, b1) & VAL[p].w[c], m1 = nap ? (_mm512_test_epi8_mask(res, b2) & NAP[p].w[c]) : 0;
        if (REAL && (m0 | m1)) {
            u64 k0 = 0, k1 = 0;
            for (int h = 0; h < 2; h++) {
                const __m512i jq = _mm512_cvtepu8_epi16(_mm512_extracti64x4_epi64(iq, h)), jr = _mm512_cvtepu8_epi16(_mm512_extracti64x4_epi64(ir, h));
                const __m512i e = _mm512_add_epi16(_mm512_permutex2var_epi16(eq0, jq, eq1), _mm512_permutex2var_epi16(er0, jr, er1));
                const __m512i rhs = _mm512_add_epi16(_mm512_mulhi_epu16(_mm512_load_si512((const void *)(TJ[p] + 64 * c + 32 * h)), tiv), nine);
                k0 |= (u64)_mm512_cmple_epi16_mask(_mm512_abs_epi16(_mm512_sub_epi16(v0, e)), rhs) << (32 * h);
                k1 |= (u64)_mm512_cmple_epi16_mask(_mm512_abs_epi16(_mm512_sub_epi16(v1, e)), rhs) << (32 * h);
            }
            m0 &= k0; m1 &= k1;
        }
        R->r0.w[c] = m0; R->r1.w[c] = m1;
    }
#else
    unsigned char tq[64], tr[64]; short eq[64], er[64];
    for (int q = 0; q < 64; q++) {
        int w = WP1[x1][q] + WP1[x2][q]; if (w > 64) w = 64;
        tq[q] = (CU1[q] + GQ1[a][q] + GQ1[x1][q] + GQ1[x2][q] + GQ1[y1][q] + GQ1[y2][q]) % 7 + w;
        w = WP2[y1][q] + WP2[y2][q]; if (w > 64) w = 64;
        tr[q] = (CU2[q] + GQ2[a][q] + GQ2[x1][q] + GQ2[x2][q] + GQ2[y1][q] + GQ2[y2][q]) % 7 + w;
        int sq = 0, sr = 0; if (REAL) for (int k = 0; k < 6; k++) { sq += HQ1s[pt[k]][q]; sr += HQ2s[pt[k]][q]; }
        eq[q] = (short)sq; er[q] = (short)sr;
    }
    memset(R, 0, sizeof *R);
    for (int k = 0; k < n; k++) {
        int z = tq[QB[p][k]] + tr[RB[p][k]] + cst, w = z >> 5, v = z & 31;
        int m0 = (v == 0 || v == 7 || v == 14) && w <= 1, m1 = (v == 1 || v == 8 || v == 15) && w == 0 && nap && !cd[off[p] + k].ap;
        if (GREENONLY) { m0 = v % 7 == 0; m1 = v % 7 == 1; }
        if (REAL && (m0 | m1)) {
            short e = (short)(eq[QB[p][k]] + er[RB[p][k]]); int rhs = (int)(((unsigned)TJ[p][k] * (unsigned)Ti) >> 16) + 9;
            if (abs((short)(c0e - e)) > rhs) m0 = 0;
            if (abs((short)(c1e - e)) > rhs) m1 = 0;
        }
        if (m0) R->r0.w[k >> 6] |= 1ULL << (k & 63);
        if (m1) R->r1.w[k >> 6] |= 1ULL << (k & 63);
    }
#endif
    if (SATF && nap) {                                /* saturation rule, both directions */
        bs_t kill; memset(&kill, 0, sizeof kill);
        u64 sm = SATm[g]; while (sm) { int w = __builtin_ctzll(sm); sm &= sm - 1; for (int c = 0; c < 8; c++) kill.w[c] |= PT[p][w].w[c]; }
        u64 mm = cmask[g] & ~(1ULL << U); while (mm) { int w = __builtin_ctzll(mm); mm &= mm - 1; for (int c = 0; c < 8; c++) kill.w[c] |= PS[p][w].w[c]; }
        for (int c = 0; c < 8; c++) { nsatk += __builtin_popcountll(R->r1.w[c] & kill.w[c]); R->r1.w[c] &= ~kill.w[c]; }
    }
    if (PLANT && plantg[cpos[g]] == g) {              /* planted star: its members are declared compatible with one another */
        int k = plantg[p] - off[p]; u64 bit = 1ULL << (k & 63);
        R->r0.w[k >> 6] &= ~bit; R->r1.w[k >> 6] &= ~bit;
        if (plantpartner[cpos[g]] == p) R->r1.w[k >> 6] |= bit; else R->r0.w[k >> 6] |= bit;
    }
    return R;
}
static inline row_t *getrow(int g, int p) { int i = ridx[g][p]; return i ? &rowpool[i] : mkrow(g, p); }

/* alive candidates of the slot in position b for the partial star memb[0..d-1] (d >= 1), as two 512-bit sets:
   AL = candidates consistent with all the members (integer conditions and coarse pair test), TI = candidates
   adjacent-compatible with some member (their tie). One step = one member: a member without partner keeps its
   non-adjacent candidates and its adjacent candidates that have no tie yet; a member that has just taken its
   partner a keeps only its non-adjacent candidates and removes the candidates tied to a; points of demand 2 covered
   for the second time remove the candidates that contain them. Returns the mask of the non-empty words. */
static unsigned getset(int d, int b) {
    LVm[d] |= 1u << b; nsteps++;
    const row_t *R = getrow(memb[d - 1], b);
    if (d == 1) {
#ifndef SCALAR
        __m512i r0 = _mm512_loadu_si512((const void *)&R->r0), r1 = _mm512_loadu_si512((const void *)&R->r1), al1 = _mm512_or_si512(r0, r1);
        _mm512_store_si512((void *)&AL[1][b], al1); _mm512_store_si512((void *)&TI[1][b], r1);
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
    __m512i al = _mm512_load_si512((const void *)&AL[d - 1][b]), ti = _mm512_load_si512((const void *)&TI[d - 1][b]);
    __m512i r0 = _mm512_loadu_si512((const void *)&R->r0), r1 = _mm512_loadu_si512((const void *)&R->r1);
    if (a >= 0) al = _mm512_and_si512(al, _mm512_andnot_si512(_mm512_loadu_si512((const void *)&getrow(memb[a], b)->r1), r0));
    else { al = _mm512_and_si512(al, _mm512_or_si512(r0, _mm512_andnot_si512(ti, r1))); ti = _mm512_or_si512(ti, r1); }
    while (news) { int w = __builtin_ctzll(news); news &= news - 1; al = _mm512_andnot_si512(_mm512_loadu_si512((const void *)&PT[b][w]), al); }
    _mm512_store_si512((void *)&AL[d][b], al); _mm512_store_si512((void *)&TI[d][b], ti);
    return _mm512_test_epi64_mask(al, al);
#else
    unsigned nz = 0; const bs_t *pa = &AL[d - 1][b], *pt = &TI[d - 1][b]; const row_t *Ra = a >= 0 ? getrow(memb[a], b) : R;
    for (int c = 0; c < 8; c++) {
        u64 al, ti = pt->w[c];
        if (GREENONLY) al = pa->w[c] & (R->r0.w[c] | R->r1.w[c]);
        else {
        if (a >= 0) al = pa->w[c] & R->r0.w[c] & ~Ra->r1.w[c];
        else { al = pa->w[c] & (R->r0.w[c] | (R->r1.w[c] & ~ti)); ti |= R->r1.w[c]; }
        u64 s2 = news; while (s2) { int w = __builtin_ctzll(s2); s2 &= s2 - 1; al &= ~PT[b][w].w[c]; }
        }
        AL[d][b].w[c] = al; TI[d][b].w[c] = ti; if (al) nz |= 1u << c;
    }
    return nz;
#endif
}

/* real conditions for the new member g at index d with tie a; on success the member data are installed */
static inline double det3(double a, double b, double c, double x, double y, double z) {   /* [[a,x,y],[x,b,z],[y,z,c]] */
    return a * (b * c - z * z) - x * (x * c - z * y) + y * (x * z - b * y);
}
static inline int install(int d, int g, int a) {
    if (!REAL) return 1;
    const unsigned char *pt = cpts[g]; double sx = cS[g], l[10];
    if (d && !hvok[d - 1]) {                          /* sums of rows of H+ of the last member, only when a child needs them */
        const unsigned char *q = cpts[mg[d - 1]]; hvok[d - 1] = 1;
        for (int z = 0; z < 36; z++) hv[d - 1][z] = Hr[q[0]][z] + Hr[q[1]][z] + Hr[q[2]][z] + Hr[q[3]][z] + Hr[q[4]][z] + Hr[q[5]][z];
    }
    for (int k = 0; k < d; k++) {
        double eps = hv[k][pt[0]] + hv[k][pt[1]] + hv[k][pt[2]] + hv[k][pt[3]] + hv[k][pt[4]] + hv[k][pt[5]];
        l[k] = 1.0 / 12 - (a == k) - eps;
        if (l[k] * l[k] > sM[k] * sx + 1e-9) return 0;
    }
    if (d == 2) { if (det3(sM[0], sM[1], sx, LG[0][1], l[0], l[1]) < -1e-8) return 0; }
    else if (d == 3) {
        double m00 = sM[0], m01 = LG[0][1], m02 = LG[0][2], m03 = l[0], m11 = sM[1], m12 = LG[1][2], m13 = l[1], m22 = sM[2], m23 = l[2], m33 = sx;
        double s0 = m00 * m11 - m01 * m01, s1 = m00 * m12 - m01 * m02, s2 = m00 * m13 - m01 * m03, s3 = m01 * m12 - m11 * m02, s4 = m01 * m13 - m11 * m03, s5 = m02 * m13 - m12 * m03;
        double c5 = m22 * m33 - m23 * m23, c4 = m12 * m33 - m13 * m23, c3 = m12 * m23 - m13 * m22, c2 = m02 * m33 - m03 * m23, c1 = m02 * m23 - m03 * m22, c0 = m02 * m13 - m03 * m12;
        if (s0 * c5 - s1 * c4 + s2 * c3 + s3 * c2 - s4 * c1 + s5 * c0 < -1e-7) return 0;
    } else if (d == 4) {
        double M[5][5];
        for (int x = 0; x < 4; x++) { M[x][x] = sM[x]; for (int y = x + 1; y < 4; y++) M[x][y] = M[y][x] = LG[x][y]; M[x][4] = M[4][x] = l[x]; }
        M[4][4] = sx;
        if (gedet(5, M) < -1e-6) return 0;
    }
    sM[d] = sx; for (int k = 0; k < d; k++) LG[k][d] = LG[d][k] = l[k];
    mg[d] = g; hvok[d] = 0;
    return 1;
}

static void dfs(int d) {
    if (d == KLIM) {
        if (KLIM == 10 && !GREENONLY) {
            if ((c1m[10] & D1) != D1 || (c2m[10] & D2) != D2) return;
            for (int k = 0; k < 10; k++) if (!cd[memb[k]].ap && partner[k] < 0) return;
        }
        nsol++; found = 1; return;
    }
    int b; unsigned nz;
    if (FCD && d > FCMAXD) {                          /* below the forward-checking depth: first unused slot, lazily */
        b = 0; while ((usedm[d] >> b) & 1) b++;
        nz = getset(d, b); pord[d] = b;
    } else if (FCD) {                                 /* forward checking on every remaining slot, smallest alive set first */
        int bc = 1 << 30; b = -1; nz = 0;
        for (int s = 0; s < 10; s++) if (!((usedm[d] >> s) & 1)) {
            unsigned z = getset(d, s); if (!z) { nfc[d]++; return; }
            int c = 0; for (int q = 0; q < 8; q++) c += __builtin_popcountll(AL[d][s].w[q]);
            if (c < bc) { bc = c; b = s; nz = z; }
        }
        if (FCD >= 2) for (int m = 0; m < d; m++) if (!cd[memb[m]].ap && partner[m] < 0) {
            int ok = 0;
            for (int s = 0; s < 10 && !ok; s++) if (!((usedm[d] >> s) & 1)) { const row_t *Rm = getrow(memb[m], s); for (int q = 0; q < 8; q++) if (Rm->r1.w[q] & AL[d][s].w[q]) { ok = 1; break; } }
            if (!ok) { nfc[d]++; return; }
        }
        if (FCD >= 3) {
            u64 need2 = D2 & ~c1m[d], nd = (D1 & ~c1m[d]) | (D2 & ~c2m[d]);
            while (nd) { int w = __builtin_ctzll(nd); nd &= nd - 1; int cnt = 0, want = ((need2 >> w) & 1) ? 2 : 1;
                for (int s = 0; s < 10 && cnt < want; s++) if (!((usedm[d] >> s) & 1)) for (int q = 0; q < 8; q++) if (PT[s][w].w[q] & AL[d][s].w[q]) { cnt++; break; }
                if (cnt < want) { nfc[d]++; return; } }
        }
        pord[d] = b;
    } else { b = pord[d]; nz = getset(d, b); }
    const bs_t *al = &AL[d][b], *ti = &TI[d][b]; u64 ub = ~(1ULL << U);
    while (nz) {
        int c = __builtin_ctz(nz); nz &= nz - 1;
        u64 bits = al->w[c];
        while (bits) {
            int k = __builtin_ctzll(bits); bits &= bits - 1;
            int g = off[b] + 64 * c + k, a = -1; u64 cm = cmask[g] & ub;
            if (!GREENONLY && ((ti->w[c] >> k) & 1)) for (int m = 0; m < d; m++) if ((getrow(memb[m], b)->r1.w[c] >> k) & 1) { a = m; break; }
            if (!install(d, g, a)) { nrej++; continue; }
            cntd[d + 1]++;
            memb[d] = g; ptie[d] = a; partner[d] = a; if (a >= 0) partner[a] = d;
            c2m[d + 1] = c2m[d] | (c1m[d] & cm); c1m[d + 1] = c1m[d] | cm;
            LVm[d + 1] = 0; usedm[d + 1] = usedm[d] | (1u << b);
            dfs(d + 1);
            if (a >= 0) partner[a] = -1;
            if (STOPFIRST && found) return;
        }
    }
}

static void search(void) {
    u64 ub = ~(1ULL << U);
    memset(cntd, 0, sizeof cntd); nsol = 0; cntd[0] = 1;
    for (int k = 0; k < 10; k++) partner[k] = -1;
    for (int i = off[0]; i < off[1]; i++) {
        cntd[1]++;
        install(0, i, -1);
        memb[0] = i; ptie[0] = -1; c1m[1] = cmask[i] & ub; c2m[1] = 0; LVm[1] = 0; usedm[1] = 1u;
        pord[0] = 0; for (int b = 1; b < 10; b++) pord[b] = b;
        if (ORDER) {                                  /* remaining slots by increasing number of candidates compatible with i */
            int cnt[10];
            for (int b = 1; b < 10; b++) { getset(1, b); cnt[b] = 0; for (int c = 0; c < 8; c++) cnt[b] += __builtin_popcountll(AL[1][b].w[c]); }
            for (int x = 2; x < 10; x++) { int v = pord[x], j = x; while (j > 1 && cnt[pord[j - 1]] > cnt[v]) { pord[j] = pord[j - 1]; j--; } pord[j] = v; }
        }
        for (int b = 0; b < 10; b++) pordI[i - off[0]][b] = pord[b];
        dfs(1);
    }
}

/* ---------- minimal conflicting sets of slots (STAR37_CORES) ---------- */
static long long CK[11], CKMIN[11], CPOS[10], CNT_CORE, CDIST[8], SDIST[8], CBALLS, CTESTS;
static int subset_feasible(const int *sl, int k) {    /* a consistent selection on the slots sl[0..k-1] (in this order)? */
    u64 ubs = ~(1ULL << U); int fsave = FCD; FCD = 0;
    KLIM = k; STOPFIRST = 1; found = 0;
    for (int x = 0; x < k; x++) pord[x] = sl[x];
    for (int x = 0; x < 10; x++) partner[x] = -1;
    for (int i = off[sl[0]]; i < off[sl[0] + 1] && !found; i++) {
        install(0, i, -1);
        memb[0] = i; ptie[0] = -1; c2m[1] = 0; c1m[1] = cmask[i] & ubs; LVm[1] = 0; usedm[1] = 1u << sl[0];
        dfs(1);
    }
    KLIM = 10; STOPFIRST = 0; FCD = fsave; CTESTS++;
    return found;
}
static void cores(void) {
    static unsigned core[1024]; int nc = 0, kmin = 0, dist[36], q[36], h = 0, tl = 0;
    for (int i = 0; i < 36; i++) dist[i] = -1;
    dist[U] = 0; q[tl++] = U;
    while (h < tl) { int x = q[h++]; for (int e = 0; e < 3; e++) { int y = nb[x][e]; if (dist[y] < 0) { dist[y] = dist[x] + 1; q[tl++] = y; } } }
    for (int p = 0; p < 10; p++) { int dd = dist[SL[ord[p]]]; if (dd > 7 || dd < 0) dd = 7; SDIST[dd]++; }
    for (int k = 2; k <= 10; k++)
        for (unsigned m = 0; m < 1024; m++) if (__builtin_popcount(m) == k) {
            int sub = 0; for (int c = 0; c < nc; c++) if ((core[c] & m) == core[c]) { sub = 1; break; }
            if (sub) continue;
            int sl[10], n = 0; for (int p = 0; p < 10; p++) if ((m >> p) & 1) sl[n++] = p;
            if (subset_feasible(sl, k)) continue;
            core[nc++] = m; CK[k]++; CNT_CORE++; if (!kmin) kmin = k;
            for (int p = 0; p < 10; p++) if ((m >> p) & 1) { CPOS[p]++; int dd = dist[SL[ord[p]]]; if (dd > 7 || dd < 0) dd = 7; CDIST[dd]++; }
        }
    CKMIN[kmin]++; CBALLS++;
}

/* ---------- joint distribution of the Green values of three and of four candidates (STAR37_PAT) ---------- */
static long long PT3[343], PT4[117649], PT3n, PT4n;
static void patterns(void) {
    static unsigned char *V[4][4]; static int hc[2048][36];
    int n[4], o[4], tot = off[4]; for (int a = 0; a < 4; a++) { n[a] = nsl[a]; o[a] = off[a]; }
    if (tot > 2048) return;
    for (int g = 0; g < tot; g++) for (int z = 0; z < 36; z++) { int t = 0; for (int k = 0; k < 6; k++) t += Gm[cpts[g][k]][z]; hc[g][z] = t; }
    for (int a = 0; a < 4; a++) for (int b = a + 1; b < 4; b++) {
        V[a][b] = realloc(V[a][b], (size_t)n[a] * n[b] + 1);
        for (int i = 0; i < n[a]; i++) for (int j = 0; j < n[b]; j++) {
            int g = o[a] + i, h = o[b] + j, t = S9 + 3 * cd[g].rsm + 3 * cd[h].rsm - 3 + 70;
            for (int k = 0; k < 6; k++) t += hc[g][cpts[h][k]];
            V[a][b][(size_t)i * n[b] + j] = (unsigned char)(t % 7);
        }
    }
    for (int i = 0; i < n[0]; i++) for (int j = 0; j < n[1]; j++) {
        int v01 = V[0][1][(size_t)i * n[1] + j]; const unsigned char *r02 = V[0][2] + (size_t)i * n[2], *r12 = V[1][2] + (size_t)j * n[2];
        for (int k = 0; k < n[2]; k++) PT3[v01 * 49 + r02[k] * 7 + r12[k]]++;
    }
    PT3n += (long long)n[0] * n[1] * n[2];
    for (int t = 0; t < 4000000; t++) {
        int i = rnd() % n[0], j = rnd() % n[1], k = rnd() % n[2], l = rnd() % n[3];
        int idx = V[0][1][(size_t)i * n[1] + j];
        idx = idx * 7 + V[0][2][(size_t)i * n[2] + k]; idx = idx * 7 + V[0][3][(size_t)i * n[3] + l];
        idx = idx * 7 + V[1][2][(size_t)j * n[2] + k]; idx = idx * 7 + V[1][3][(size_t)j * n[3] + l]; idx = idx * 7 + V[2][3][(size_t)k * n[3] + l];
        PT4[idx]++;
    }
    PT4n += 4000000;
}

static inline int satfree(int g, int h) {             /* the two shadows respect the saturation rule in both directions */
    u64 ubs = ~(1ULL << U), m = cmask[h] & ubs;
    while (m) { int w = __builtin_ctzll(m); m &= m - 1; if (__builtin_popcountll(amask[w] & cmask[g]) > 1) return 0; }
    m = cmask[g] & ubs;
    while (m) { int w = __builtin_ctzll(m); m &= m - 1; if (__builtin_popcountll(amask[w] & cmask[h]) > 1) return 0; }
    return 1;
}

/* positive control: a combinatorial star (one candidate per slot, exact coverage, two members sharing at most one
   point besides U) with a perfect matching of its eight non-apex members into pairs of disjoint shadows */
static int pl_match(unsigned used) {
    u64 ub = ~(1ULL << U); int i = -1;
    for (int p = 0; p < 10; p++) if (!((used >> p) & 1) && !cd[plantg[p]].ap) { i = p; break; }
    if (i < 0) return 1;
    for (int j = i + 1; j < 10; j++) if (!((used >> j) & 1) && !cd[plantg[j]].ap && !(cmask[plantg[i]] & cmask[plantg[j]] & ub) && (!SATF || satfree(plantg[i], plantg[j]))) {
        plantpartner[i] = j; plantpartner[j] = i;
        if (pl_match(used | 1u << i | 1u << j)) return 1;
    }
    return 0;
}
static int pl_dfs(int p, u64 c1, u64 c2) {
    u64 ub = ~(1ULL << U);
    if (p == 10) { if ((c1 & D1) != D1 || (c2 & D2) != D2) return 0; for (int k = 0; k < 10; k++) plantpartner[k] = -1; return pl_match(0); }
    int n = nsl[p]; if (!n) return 0;
    int start = rnd() % n;
    for (int t = 0; t < n; t++) {
        int g = off[p] + (start + t) % n, ok = 1; u64 cm = cmask[g] & ub;
        if (cm & ((c1 & D1) | c2)) continue;
        for (int k = 0; k < p && ok; k++) if (__builtin_popcountll(cmask[plantg[k]] & cm) > 1) ok = 0;
        if (!ok) continue;
        plantg[p] = g;
        if (++plnodes > 3000000) return 0;
        if (pl_dfs(p + 1, c1 | cm, c2 | (c1 & cm))) return 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: star37d <seed> <balls> <U: 0|1> <real: 0|1> <order: 0|1> [check [depth]]\n"); return 1; }
    rs = strtoull(argv[1], 0, 10) * 0x9E3779B97F4A7C15ULL + 1; int NB = atoi(argv[2]); int UMODE = atoi(argv[3]); REAL = atoi(argv[4]); ORDER = atoi(argv[5]); int CHECK = argc > 6;
    REFD = argc > 7 ? atoi(argv[7]) : 4;
    ALLOW4 = getenv("STAR37_TYPE1") != NULL; long long with4 = 0, with4t = 0;
    ALLOW3 = getenv("STAR37_NT") != NULL; long long with3 = 0, with3t = 0, nou = 0; if (ALLOW3) ALLOW4 = 1;
    SATF = getenv("STAR37_SAT") != NULL; FCD = getenv("STAR37_FC") ? atoi(getenv("STAR37_FC")) : 0; GREENONLY = getenv("STAR37_GREEN") != NULL;
    if (getenv("STAR37_FCMAX")) FCMAXD = atoi(getenv("STAR37_FCMAX"));
    int CORES = getenv("STAR37_CORES") != NULL, PAT = getenv("STAR37_PAT") != NULL;
#ifndef SCALAR
    if (GREENONLY) { fprintf(stderr, "STAR37_GREEN needs the scalar build (-DSCALAR)\n"); return 1; }
#endif
    int PLANTMODE = CHECK && !strcmp(argv[6], "plant"); long long planted = 0, plfound = 0, plfail = 0;
    if (PLANTMODE) { REAL = 0; REFD = 10; }
    if (CHECK) { for (int k = 0; k < 12; k++) { balive[k] = malloc(sizeof(int) * MAXC); btie[k] = malloc(sizeof(int) * MAXC); } refm = malloc((size_t)MAXC * MAXC); }
    for (int i = 0; i < 256; i++) mod7[i] = i % 7;
#ifndef SCALAR
    for (int f = 0; f < 7; f++) for (int x = 0; x < 64; x++) MULT[f][x] = (x & 15) < 7 ? f * (x & 15) % 7 : 0;
#endif
    long long tried = 0, valid = 0, tors = 0, resid = 0, tested = 0, totc = 0, alive_balls = 0, mism = 0, big = 0, tot[11], bstar = 0; memset(tot, 0, sizeof tot);
    double tsearch = 0, tcand = 0, tinv = 0, ttab = 0, tbase = 0, tgen = 0; int maxslot = 0, maxdepth = 0; double t00 = now();
    while (tested < NB) {
        tried++;
        double g0 = now(); int okb = make_ball(); tgen += now() - g0;
        if (!okb) continue;
        valid++; with4 += has4; with3 += has3;
        double t0 = now(); int det = invert(); tinv += now() - t0;
        if (CHECK) { static int G2[36][36]; int d2 = invert_plain(G2); int bad = d2 != det; if (det) for (int i = 0; i < 36; i++) for (int j = 0; j < 36; j++) if (G2[i][j] != Gm[i][j]) bad = 1;
            if (bad) { printf("MISMATCH: fast inverse differs from plain Gauss-Jordan (valid ball %lld)\n", valid); mism++; } }
        if (det == 0) { tors++; continue; }
        if (det == 1 || det == 2 || det == 4) { resid++; continue; }
        U = -1;                                        /* the star vertex is taken outside the triangles of G(T) */
        { int bz = -1; for (int x = 0; x < 36; x++) {
            int c[2], nc = 0; for (int k = 0; k < 3; k++) if (lay[nb[x][k]] != lay[x]) c[nc++] = nb[x][k];
            if (A[c[0]][c[1]]) continue;
            int z = 0; for (int k = 0; k < 36; k++) if (lay[k] != lay[x] && K[x][k] == 0) z++;
            if (U < 0 || (UMODE == 1 && z > bz)) { bz = z; U = x; } } }
        if (U < 0) { nou++; continue; }
        double c0 = now();
        if (REAL) real_pinv();
        ball_tables(); candidates(); double c1 = now();
        slot_tables(); double c2 = now();
        if (TOOBIG) { big++; fprintf(stderr, "ball %lld: a slot has more than 512 candidates, not handled by this version\n", tested); tested++; continue; }
        PLANT = 0;
        if (PLANTMODE) { plnodes = 0; if (pl_dfs(0, 0, 0)) { PLANT = 1; planted++; } else plfail++; }
        search(); double c3 = now();
        tcand += c1 - c0; ttab += c2 - c1; tsearch += c3 - c2;
        tested++; with4t += has4; with3t += has3; totc += NC; if (nsol) alive_balls++;
        for (int d = 0; d <= 10; d++) { tot[d] += cntd[d]; if (cntd[d] && d > maxdepth) maxdepth = d; }
        for (int p = 0; p < 10; p++) if (nsl[p] > maxslot) maxslot = nsl[p];
        { int dm = 0; for (int d = 0; d <= 10; d++) if (cntd[d]) dm = d; DMX[dm]++; for (int d = 1; d <= 10; d++) totn += cntd[d]; }
        if (CHECK) {
            double b0 = now(); bcandidates();
            for (int k = 0; k < 36; k++) bdem[k] = K[U][k];
            bdem[U] = 0;
            for (int i = 0; i < BNC; i++) { balive[0][i] = i; btie[0][i] = -1; }
            bnalive[0] = BNC; bnodes = 0; bnsol = 0; bdfs(0); tbase += now() - b0;
            if (bnsol) bstar++;
            int bad = (bnsol == 0 && nsol != 0 && !PLANT), kept = 0;
            for (int i = 0; i < BNC; i++) {              /* candidate lists: same shadows in the same order */
                refe[i] = REAL ? refeps(i, i) : 0.0;
                if (REAL && refe[i] > BND + 1e-9) continue;
                if (kept >= NC || cmask0[kept] != bmask[i] || cd0[kept].ap != bapex[i]) bad = 1;
                kept++;
            }
            if (kept != NC) bad = 1;
            for (int i = 0; i < BNC; i++) for (int j = 0; j < BNC; j++) refm[(size_t)i * BNC + j] = (bmem[i][1] == bmem[j][1]) ? -1 : refrel(i, j);
            for (int p = 0; p < 10; p++) { refn[p] = 0; for (int i = 0; i < BNC; i++) if (bmem[i][1] == SL[ord[p]] && !(REAL && refe[i] > BND + 1e-9)) refslot[p][refn[p]++] = i; }
            if (PLANT) for (int x = 0; x < 10; x++) for (int y = 0; y < 10; y++) if (x != y) {
                int i = soff[ord[x]] + plantg[x] - off[x], j = soff[ord[y]] + plantg[y] - off[y];
                refm[(size_t)i * BNC + j] = plantpartner[x] == y ? 1 : 0; }
            int tup[10]; memset(refcnt, 0, sizeof refcnt); refsol = 0; refrec(0, tup);
            if (PLANT) { if (nsol >= 1) plfound++; if (refsol != nsol) bad = 1; }
            if (!FCD) for (int d = 0; d <= REFD; d++) if (refcnt[d] != cntd[d]) bad = 1;
            if (bad) { mism++; if (mism <= 5) { printf("MISMATCH ball %lld: candidates %d / %d of %d, solutions %d / baseline %d; partial stars by depth (fast / reference):", tested, NC, kept, BNC, nsol, bnsol);
                for (int d = 1; d <= REFD; d++) printf(" %lld / %lld", cntd[d], refcnt[d]);
                if (PLANT) printf("; complete stars %d / %lld", nsol, refsol);
                printf("\n"); } }
        }
        if (PAT) patterns();
        if (CORES) cores();
    }
    double wall = now() - t00;
    printf("slot order %s; ", ORDER ? "per first member" : "fixed");
    if (ALLOW3) printf("class: connected, triangles of G(T) and 4-cycles of type I ALLOWED (with a triangle: %lld of the valid balls, %lld of the tested ones; with a 4-cycle of type I: %lld, %lld; balls where every point is in a triangle, skipped: %lld); ", with3, with3t, with4, with4t, nou);
    else if (ALLOW4) printf("class: connected, no triangle in G(T), 4-cycles of type I ALLOWED (%lld of the valid balls and %lld of the tested ones have one); ", with4, with4t);
    printf("real filters %s; drawn %lld, valid connected %lld, torsion %lld, residue discriminant %lld, tested %lld (slot too big: %lld)\n", REAL ? "ON" : "off", tried, valid, tors, resid, tested, big);
    printf("mean candidates %.0f, largest slot %d, balls with a star %lld, deepest level reached %d\n", (double)totc / tested, maxslot, alive_balls, maxdepth);
    printf("mean consistent partial stars by depth:"); for (int d = 1; d <= maxdepth; d++) printf(" %.1f", (double)tot[d] / tested);
    printf("\nper tested ball: rows %.0f, set steps %.0f, children rejected by the exact real tests %.0f\n", (double)nrows / tested, (double)nsteps / tested, (double)nrej / tested);
    printf("time: inverse %.4f ms per valid ball; per tested ball: tables and candidates %.4f ms, slots %.4f ms, search %.4f ms; total per tested ball without the generator %.4f ms\n",
           1e3 * tinv / valid, 1e3 * tcand / tested, 1e3 * ttab / tested, 1e3 * tsearch / tested, 1e3 * (tinv + tcand + ttab + tsearch) / tested);
    if (!CHECK) printf("wall %.2f s, of which random generation and rejection %.2f s\n", wall, tgen);
    if (PLANTMODE) printf("positive control: a combinatorial star was planted in %lld balls (none found to plant in %lld); the fast search found a complete star in %lld of them\n", planted, plfail, plfound);
    printf("options: saturation rule %s (adjacent-compatible pairs removed in the rows computed: %.1f per ball), forward checking level %d%s\n", SATF ? "ON" : "off", (double)nsatk / tested, FCD, GREENONLY ? ", GREEN VALUES ONLY" : "");
    printf("nodes per ball %.1f; balls by deepest consistent partial star:", (double)totn / tested); for (int d = 0; d <= 10; d++) if (DMX[d]) printf("  %d: %lld", d, DMX[d]); printf("\n");
    if (FCD) { printf("branches cut by forward checking per ball, by depth:"); for (int d = 1; d <= 9; d++) printf(" %.1f", (double)nfc[d] / tested); printf("\n"); }
    if (PAT) {
        long long e3 = 0, mn3 = 1LL << 60, mx3 = 0, e4 = 0, mn4 = 1LL << 60, mx4 = 0;
        for (int i = 0; i < 343; i++) { if (!PT3[i]) e3++; if (PT3[i] < mn3) mn3 = PT3[i]; if (PT3[i] > mx3) mx3 = PT3[i]; }
        for (int i = 0; i < 117649; i++) { if (!PT4[i]) e4++; if (PT4[i] < mn4) mn4 = PT4[i]; if (PT4[i] > mx4) mx4 = PT4[i]; }
        printf("Green values of three candidates (the three smallest slots, all %lld triples): 343 patterns, %lld never realised, smallest / mean / largest count %lld / %.0f / %lld\n", PT3n, e3, mn3, (double)PT3n / 343, mx3);
        printf("Green values of four candidates (the four smallest slots, %lld random quadruples): 117649 patterns, %lld never realised, smallest / mean / largest count %lld / %.0f / %lld\n", PT4n, e4, mn4, (double)PT4n / 117649, mx4);
    }
    if (CORES && CBALLS) {
        printf("minimal conflicting sets of slots: %lld balls, %.1f sets per ball, %.0f feasibility tests per ball\n", CBALLS, (double)CNT_CORE / CBALLS, (double)CTESTS / CBALLS);
        printf("  sets per ball by size:"); for (int k = 2; k <= 10; k++) if (CK[k]) printf("  %d: %.2f", k, (double)CK[k] / CBALLS); printf("\n");
        printf("  balls by size of their smallest conflicting set:"); for (int k = 2; k <= 10; k++) if (CKMIN[k]) printf("  %d: %lld", k, CKMIN[k]); printf("\n");
        { long long t = 0; for (int p = 0; p < 10; p++) t += CPOS[p]; printf("  share of each slot in these sets, by rank (0 = fewest candidates):"); for (int p = 0; p < 10; p++) printf(" %.3f", (double)CPOS[p] / t); printf("\n"); }
        { long long ta = 0, tc = 0; for (int x = 0; x < 8; x++) { ta += SDIST[x]; tc += CDIST[x]; }
          printf("  slot points by distance from U in G(T), share among all slots / among the slots of these sets:"); for (int x = 2; x < 8; x++) if (SDIST[x]) printf("  d=%d: %.3f / %.3f", x, (double)SDIST[x] / ta, (double)CDIST[x] / tc); printf("\n"); }
    }
    if (CHECK) printf("check: %lld mismatches (inverse, candidate list, verdict, counts up to depth %d); baseline search %.3f ms per ball, stars found by the baseline %lld\n", mism, REFD, 1e3 * tbase / tested, bstar);
    return 0;
}
