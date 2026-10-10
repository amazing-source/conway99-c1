/* C1, lab session, 2026-10-10. Rank 37 against an integral (-4)-eigenvector of norm 14: the test of fano37_pilot.py
   in C, over ALL the bases (or one class of them modulo an integer), with the bases of Seidel rank 35 treated too.

   Model (see fano37_pilot.py and NOTE 17.94). Rank 37 <=> the Seidel matrix J - I - 2A has rank 36 modulo 7: the
   vertices are isotropic vectors of a 36-dimensional non-degenerate space W, product 6 (= -1) on edges and 1 on
   non-edges.
   Base (39 vertices): X (7), Y (7) with the biplane, the 15 far vertices, the ten boundary neighbours B0 of x_0;
   the unknown is a simple cubic graph on B0 whose 15 edges are the far vertices, avoiding six pairs: 800 427 labelled
   graphs. The ten boundary neighbours B1 of x_1 are then searched: candidate = (1 or 2 neighbours in B0, 3 far
   neighbours); the 45 products are prescribed; every far vertex lies in exactly two of the ten triples, every vertex
   of B0 has its quota of neighbours in B1.
   * Base of Seidel rank 36: it spans W; its determinant (on 36 independent vertices) must be a non-residue
     (discriminant of W); a candidate is the vector with the prescribed products with the base and must be isotropic.
   * Base of Seidel rank 35: it spans a non-degenerate hyperplane V; W = V + <n>, <n,n> = nu, the class of nu being
     fixed by the discriminant of W; a candidate is v + t n with v in V given by its products with the base, which
     must agree on the dependent base vertices too (one condition that is not automatic), and t^2 nu = -<v,v>.
   * Symmetry (option): the 24 collineations fixing the point 0 act on the bases; only the least graph of every orbit
     is tested (the cell of x_1 of an image is the cell of another core point of the original).

   fano37 all <mod> <res> [max bases] [fc]     every base (every orbit with FANO37_ORBIT) of serial number res mod mod
   fano37 base a0 b0 ... a14 b14 [fc]          one base given by its 15 edges on B0 (positions 0..9), verbose
   fc: forward checking on all the remaining members at every node (the search of the Python pilot; same node counts);
   default: lazy alive sets (only the next member), same verdicts.
   Environment: FANO37_ORBIT = one base per orbit; FANO37_CAP = node cap per base; FANO37_NODISC = no use of the
   discriminant of W (rank 36: residue determinants are searched too; rank 35: both classes of nu);
   FANO37_RANKONLY = ranks and determinants only; FANO37_NOGRAM = control, the products are not tested;
   FANO37_PLANT = control: a cell found without the products is planted (its own products become the prescribed
   ones) and the search must find a complete cell.
   gcc -O3 -march=native -o fano37 fano37.c      One process, about 60 MB. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
typedef unsigned long long u64;
#define NBASE 39
#define MAXP 48
#define MAXC 8192
#define WMAX (MAXC / 64)
#define POOLWORDS 6400000
static const int LINES[7][3] = {{0,1,2},{0,3,4},{0,5,6},{1,3,5},{1,4,6},{2,3,6},{2,4,5}};
static int on(int p, int j) { return LINES[j][0] == p || LINES[j][1] == p || LINES[j][2] == p; }
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static const int inv7[7] = {0, 1, 4, 5, 2, 3, 6};
static const int sqrt7[7] = {0, 1, 3, -1, 2, -1, -1};
static const int FLp[3][2] = {{4, 6}, {5, 8}, {7, 9}};
static int B0lab[10], B1lab[10], quota1[10], quota0[10], adj1[10][10], forb[10][10];
static int TR[455][3], TRm[455];

static void cell(int point, int *lab) {
    int n = 0;
    for (int j = 0; j < 7; j++) if (!on(point, j)) lab[n++] = j;
    for (int j = 0; j < 7; j++) if (on(point, j)) { lab[n++] = j; lab[n++] = j; }
}

/* ---------- one base ---------- */
static int E[15][2], blk0[10], DIM, NU, Isel[36], nout, Iout[NBASE], pos[NBASE], K[NBASE][NBASE], Kinv[36][36], Lw[NBASE][36];
static int np[10], Pm[10][MAXP]; static unsigned char U[10][MAXP][36], Wv[10][MAXP][36];
static int nc[10]; static unsigned short cpat[10][MAXC], ctri[10][MAXC], cpm[10][MAXC], ctm[10][MAXC]; static unsigned char ct[10][MAXC];
static unsigned char KC[15][36]; static int FK[15][15];
static int W, ord[10], WANT[10][10];
static u64 PTF[10][15][WMAX], PTB[10][10][WMAX], ALs[11][10][WMAX];
static unsigned LV[11], newF[11], newB[11]; static int memb[10], fcn[11][15], bcn[11][10];
static int *rowidx; static u64 *pool; static int npool;
static long long nodes, lvl[11], NODECAP = 1LL << 60, nincons36; static int found, FCMODE, VERBOSE, NODISC, RANKONLY, NOGRAM, PLANT, STOPFIRST, sol[10];

static int rank_and_inverse(int *det_out) {         /* rank of K; if it is 35 or 36, inverse of K on independent vertices */
    static int bas[NBASE][NBASE]; int piv[NBASE], nb = 0, isin[NBASE]; memset(isin, 0, sizeof isin);
    for (int i = 0; i < NBASE; i++) {
        int v[NBASE]; memcpy(v, K[i], sizeof v);
        for (int b = 0; b < nb; b++) if (v[piv[b]]) { int f = v[piv[b]]; for (int j = 0; j < NBASE; j++) v[j] = (v[j] + (7 - f) * bas[b][j]) % 7; }
        int p = -1; for (int j = 0; j < NBASE; j++) if (v[j]) { p = j; break; }
        if (p < 0) continue;
        int iv = inv7[v[p]]; for (int j = 0; j < NBASE; j++) bas[nb][j] = v[j] * iv % 7;
        piv[nb] = p; if (nb < 36) Isel[nb] = i; isin[i] = 1; nb++;
    }
    if (nb != 36 && nb != 35) return nb;
    DIM = nb; nout = 0; for (int i = 0; i < NBASE; i++) if (!isin[i]) Iout[nout++] = i;
    static int M[36][72]; int det = 1, n = DIM;
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) { M[i][j] = K[Isel[i]][Isel[j]]; M[i][n + j] = i == j; }
    for (int c = 0; c < n; c++) {
        int p = -1; for (int r = c; r < n; r++) if (M[r][c]) { p = r; break; }
        if (p < 0) { fprintf(stderr, "singular principal minor\n"); exit(5); }
        if (p != c) { for (int j = 0; j < 2 * n; j++) { int t = M[c][j]; M[c][j] = M[p][j]; M[p][j] = t; } det = (7 - det) % 7; }
        det = det * M[c][c] % 7; int iv = inv7[M[c][c]]; for (int j = 0; j < 2 * n; j++) M[c][j] = M[c][j] * iv % 7;
        for (int r = 0; r < n; r++) if (r != c && M[r][c]) { int f = 7 - M[r][c]; for (int j = 0; j < 2 * n; j++) M[r][j] = (M[r][j] + f * M[c][j]) % 7; }
    }
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) Kinv[i][j] = M[i][n + j];
    for (int o = 0; o < nout; o++) for (int c = 0; c < n; c++) { int s = 0; for (int d = 0; d < n; d++) s += K[Iout[o]][Isel[d]] * Kinv[d][c]; Lw[o][c] = s % 7; }
    *det_out = det; return nb;
}

static void build_base(void) {
    static int A[NBASE][NBASE]; memset(A, 0, sizeof A); memset(blk0, 0, sizeof blk0);
    for (int x = 0; x < 7; x++) for (int y = 0; y < 7; y++) if (!on(x, y)) A[x][7 + y] = A[7 + y][x] = 1;
    for (int t = 0; t < 10; t++) { A[29 + t][0] = A[0][29 + t] = 1; A[29 + t][7 + B0lab[t]] = A[7 + B0lab[t]][29 + t] = 1; }
    for (int l = 0; l < 3; l++) A[29 + FLp[l][0]][29 + FLp[l][1]] = A[29 + FLp[l][1]][29 + FLp[l][0]] = 1;
    for (int k = 0; k < 15; k++) for (int e = 0; e < 2; e++) { A[14 + k][29 + E[k][e]] = A[29 + E[k][e]][14 + k] = 1; blk0[E[k][e]] |= 1 << k; }
    for (int i = 0; i < NBASE; i++) for (int j = 0; j < NBASE; j++) K[i][j] = i == j ? 0 : (A[i][j] ? 6 : 1);
}

static void candidates(void) {
    int n = DIM, inu = inv7[NU];
    for (int k = 0; k < 15; k++) { int p = pos[14 + k]; for (int c = 0; c < n; c++) KC[k][c] = p >= 0 ? Kinv[c][p] : 0; }
    for (int k = 0; k < 15; k++) for (int l = 0; l < 15; l++) FK[k][l] = (pos[14 + k] >= 0 && pos[14 + l] >= 0) ? 4 * Kinv[pos[14 + k]][pos[14 + l]] % 7 : 0;
    int dk[NBASE][15];                               /* consistency on the dependent base vertices: contribution of a far neighbour */
    for (int o = 0; o < nout; o++) for (int k = 0; k < 15; k++) dk[o][k] = ((pos[14 + k] >= 0 ? 5 * Lw[o][pos[14 + k]] : 0) + (Iout[o] == 14 + k ? 2 : 0)) % 7;
    for (int m = 0; m < 10; m++) {
        int j = B1lab[m], q = quota1[m]; np[m] = 0; nc[m] = 0;
        for (int a = 0; a < 10; a++) for (int b = (q == 2 ? a + 1 : a); b < (q == 2 ? 10 : a + 1); b++) {
            int pm = (1 << a) | (1 << b);
            if (B0lab[a] == j && j != 0) continue;
            if (q == 2) { if (B0lab[b] == j && j != 0) continue; if (forb[a][b] || (blk0[a] & blk0[b]) || B0lab[a] == B0lab[b]) continue; }
            int p = np[m]++; Pm[m][p] = pm;
            int av[NBASE]; memset(av, 0, sizeof av); av[1] = 1; av[7 + j] = 1; for (int t = 0; t < 10; t++) if ((pm >> t) & 1) av[29 + t] = 1;
            for (int c = 0; c < n; c++) U[m][p][c] = av[Isel[c]] ? 6 : 1;
            int qP = 0; for (int c = 0; c < n; c++) { int s = 0; for (int d = 0; d < n; d++) s += Kinv[c][d] * U[m][p][d]; Wv[m][p][c] = s % 7; qP += U[m][p][c] * (s % 7); }
            qP %= 7;
            int cw[NBASE]; for (int o = 0; o < nout; o++) { int s = 0; for (int c = 0; c < n; c++) s += Lw[o][c] * U[m][p][c]; cw[o] = (s + (av[Iout[o]] ? 1 : 6)) % 7; }
            int fw[15]; for (int k = 0; k < 15; k++) fw[k] = pos[14 + k] >= 0 ? 3 * Wv[m][p][pos[14 + k]] % 7 : 0;
            int nofar = 0; for (int k = 0; k < 15; k++) if (((pm >> E[k][0]) & 1) && ((pm >> E[k][1]) & 1)) nofar |= 1 << k;
            for (int ti = 0; ti < 455; ti++) {
                int tm = TRm[ti]; if (tm & nofar) continue;
                int ok = 1;
                for (int t = 0; t < 10 && ok; t++) if ((B0lab[t] == j) + __builtin_popcount(tm & blk0[t]) > (((pm >> t) & 1) ? 1 : 2)) ok = 0;
                if (!ok) continue;
                int k1 = TR[ti][0], k2 = TR[ti][1], k3 = TR[ti][2];
                for (int o = 0; o < nout && ok; o++) if ((cw[o] + dk[o][k1] + dk[o][k2] + dk[o][k3]) % 7) ok = 0;
                if (!ok) { if (DIM == 36) nincons36++; continue; }
                int Q = (qP + fw[k1] + fw[k2] + fw[k3] + FK[k1][k1] + FK[k2][k2] + FK[k3][k3] + 2 * (FK[k1][k2] + FK[k1][k3] + FK[k2][k3])) % 7;
                int t1 = 0, nt = 1;
                if (DIM == 36) { if (Q) continue; }
                else { int tsq = (7 - Q) % 7 * inu % 7; if (sqrt7[tsq] < 0) continue; t1 = sqrt7[tsq]; nt = t1 ? 2 : 1; }
                for (int e = 0; e < nt; e++) {
                    if (nc[m] >= MAXC) { fprintf(stderr, "too many candidates\n"); exit(3); }
                    cpat[m][nc[m]] = p; ctri[m][nc[m]] = ti; cpm[m][nc[m]] = pm; ctm[m][nc[m]] = tm; ct[m][nc[m]] = e ? 7 - t1 : t1; nc[m]++;
                }
            }
        }
    }
}

static int product(int a, int i, int b, int c) {    /* product of candidate i of member a and candidate c of member b (slow, for the controls) */
    int p = cpat[a][i], ti = ctri[a][i], q = cpat[b][c], tj = ctri[b][c], s = 0;
    for (int x = 0; x < DIM; x++) {
        int h = (Wv[a][p][x] + 5 * (KC[TR[ti][0]][x] + KC[TR[ti][1]][x] + KC[TR[ti][2]][x])) % 7, sb = U[b][q][x];
        for (int e = 0; e < 3; e++) if (pos[14 + TR[tj][e]] == x) sb = 6;
        s += h * sb;
    }
    return (s + ct[a][i] * ct[b][c] * NU) % 7;
}

static u64 *row(int a, int i, int b) {              /* candidates of member b compatible with candidate i of member a */
    int *ri = &rowidx[(a * MAXC + i) * 10 + b];
    if (*ri) return pool + (size_t)(*ri) * W;
    if ((size_t)(npool + 1) * W > POOLWORDS) { fprintf(stderr, "row pool full\n"); exit(4); }
    *ri = npool; u64 *R = pool + (size_t)npool * W; npool++; memset(R, 0, W * sizeof(u64));
    int p = cpat[a][i], ti = ctri[a][i], k1 = TR[ti][0], k2 = TR[ti][1], k3 = TR[ti][2], h[36], HP[MAXP], HT[15]; unsigned char TT[455];
    for (int c = 0; c < DIM; c++) h[c] = (Wv[a][p][c] + 5 * (KC[k1][c] + KC[k2][c] + KC[k3][c])) % 7;
    for (int q = 0; q < np[b]; q++) { int s = 0; for (int c = 0; c < DIM; c++) s += h[c] * U[b][q][c]; HP[q] = s % 7; }
    for (int k = 0; k < 15; k++) HT[k] = pos[14 + k] >= 0 ? 5 * h[pos[14 + k]] % 7 : 0;
    for (int t = 0; t < 455; t++) TT[t] = (HT[TR[t][0]] + HT[TR[t][1]] + HT[TR[t][2]]) % 7;
    int want = WANT[a][b], lim = (adj1[a][b] || B1lab[a] == B1lab[b]) ? 0 : 1, pm = cpm[a][i], tm = ctm[a][i], tn = ct[a][i] * NU % 7;
    for (int c = 0; c < nc[b]; c++) {
        if (!NOGRAM && (HP[cpat[b][c]] + TT[ctri[b][c]] + tn * ct[b][c]) % 7 != want) continue;
        if (__builtin_popcount(tm & ctm[b][c]) + __builtin_popcount(pm & cpm[b][c]) > lim) continue;
        R[c >> 6] |= 1ULL << (c & 63);
    }
    return R;
}

static u64 *getset(int d, int y) {                  /* alive candidates of the member in position y after d placements */
    u64 *S = ALs[d][y];
    if ((LV[d] >> y) & 1) return S;
    LV[d] |= 1u << y;
    int m = ord[y];
    if (d == 0) { memset(S, 0, W * sizeof(u64)); for (int c = 0; c < nc[m]; c++) S[c >> 6] |= 1ULL << (c & 63); return S; }
    const u64 *prev = getset(d - 1, y), *R = row(ord[d - 1], memb[d - 1], m);
    for (int w = 0; w < W; w++) S[w] = prev[w] & R[w];
    for (unsigned f = newF[d]; f; f &= f - 1) { const u64 *x = PTF[m][__builtin_ctz(f)]; for (int w = 0; w < W; w++) S[w] &= ~x[w]; }
    for (unsigned f = newB[d]; f; f &= f - 1) { const u64 *x = PTB[m][__builtin_ctz(f)]; for (int w = 0; w < W; w++) S[w] &= ~x[w]; }
    return S;
}

static void rec(int x) {
    if (x == 10) {
        for (int k = 0; k < 15; k++) if (fcn[10][k] != 2) return;
        for (int t = 0; t < 10; t++) if (bcn[10][t] != quota0[t]) return;
        if (!found) for (int y = 0; y < 10; y++) sol[ord[y]] = memb[y];
        found++; return;
    }
    const u64 *al = getset(x, x); int m = ord[x];
    for (int w = 0; w < W; w++) for (u64 bits = al[w]; bits; bits &= bits - 1) {
        int i = 64 * w + __builtin_ctzll(bits);
        nodes++; lvl[x + 1]++;
        if (nodes > NODECAP) return;
        memcpy(fcn[x + 1], fcn[x], sizeof fcn[0]); memcpy(bcn[x + 1], bcn[x], sizeof bcn[0]);
        unsigned nf = 0, nb = 0;
        for (unsigned f = ctm[m][i]; f; f &= f - 1) { int k = __builtin_ctz(f); if (++fcn[x + 1][k] == 2) nf |= 1u << k; }
        for (unsigned f = cpm[m][i]; f; f &= f - 1) { int t = __builtin_ctz(f); if (++bcn[x + 1][t] == quota0[t]) nb |= 1u << t; }
        newF[x + 1] = nf; newB[x + 1] = nb; memb[x] = i; LV[x + 1] = 0;
        if (FCMODE) {
            int dead = 0;
            for (int y = x + 1; y < 10 && !dead; y++) { const u64 *s = getset(x + 1, y); int any = 0; for (int v = 0; v < W; v++) if (s[v]) { any = 1; break; } if (!any) dead = 1; }
            if (dead) continue;
        }
        rec(x + 1);
        if (nodes > NODECAP || (STOPFIRST && found)) return;
    }
}

static void search(void) {                          /* candidates must be ready; resets the rows and runs the search */
    for (int m = 0; m < 10; m++) memset(rowidx + (size_t)m * MAXC * 10, 0, (size_t)nc[m] * 10 * sizeof(int));
    npool = 1; nodes = 0; found = 0; memset(lvl, 0, sizeof lvl); memset(fcn[0], 0, sizeof fcn[0]); memset(bcn[0], 0, sizeof bcn[0]); LV[0] = 0; newF[0] = newB[0] = 0;
    int empty = 0; for (int m = 0; m < 10; m++) if (!nc[m]) empty = 1;
    if (!empty) rec(0);
}

static long long cursize = 1, wrank[40], wres;       /* size of the orbit of the current base; counts weighted by it */
static long long nbase, nproc, nrank[40], nres, ntest[2], ndead[2], nalive[2], ncap[2], totnodes[2], deep[2][11], totl[2][11], totc[2][10], npass[2], nplant, nplantok, nnoplant;
static void process(void) {
    nproc++;
    build_base(); int det = 0, rk = rank_and_inverse(&det), residue = (det == 1 || det == 2 || det == 4);
    nrank[rk]++; wrank[rk] += cursize; if (rk == 36 && residue) wres += cursize;
    if (rk < 35) { printf("LOW RANK %d base %lld:", rk, nbase); for (int k = 0; k < 15; k++) printf(" %d %d", E[k][0], E[k][1]); printf("\n"); return; }
    int z = 36 - rk;                                 /* 0: the base spans W; 1: a hyperplane */
    if (rk == 36 && residue) { nres++; if (!NODISC) return; }
    if (RANKONLY) return;
    for (int v = 0; v < NBASE; v++) pos[v] = -1;
    for (int c = 0; c < DIM; c++) pos[Isel[c]] = c;
    int nus[2], nnu = 1; nus[0] = 1;
    if (rk == 35) { if (NODISC) { nus[0] = 1; nus[1] = 3; nnu = 2; } else nus[0] = residue ? 3 : 1; }
    ntest[z]++; int alive = 0, capped = 0, dp = 0;
    for (int pass = 0; pass < nnu; pass++) {
        NU = nus[pass]; npass[z]++;
        candidates();
        int mx = 0; for (int m = 0; m < 10; m++) { if (nc[m] > mx) mx = nc[m]; totc[z][m] += nc[m]; }
        W = (mx + 63) / 64; if (W == 0) W = 1;
        for (int m = 0; m < 10; m++) ord[m] = m;
        for (int a = 1; a < 10; a++) { int v = ord[a], b = a; while (b > 0 && nc[ord[b - 1]] > nc[v]) { ord[b] = ord[b - 1]; b--; } ord[b] = v; }
        for (int m = 0; m < 10; m++) {
            for (int k = 0; k < 15; k++) memset(PTF[m][k], 0, W * sizeof(u64));
            for (int t = 0; t < 10; t++) memset(PTB[m][t], 0, W * sizeof(u64));
            for (int c = 0; c < nc[m]; c++) {
                for (unsigned f = ctm[m][c]; f; f &= f - 1) PTF[m][__builtin_ctz(f)][c >> 6] |= 1ULL << (c & 63);
                for (unsigned f = cpm[m][c]; f; f &= f - 1) PTB[m][__builtin_ctz(f)][c >> 6] |= 1ULL << (c & 63);
            }
        }
        for (int a = 0; a < 10; a++) for (int b = 0; b < 10; b++) WANT[a][b] = adj1[a][b] ? 6 : 1;
        if (PLANT) {                                 /* control: plant a cell found without the products */
            NOGRAM = 1; STOPFIRST = 1; search(); NOGRAM = 0; STOPFIRST = 0;
            if (!found) { nnoplant++; continue; }
            nplant++; int pl[10]; memcpy(pl, sol, sizeof pl);
            for (int a = 0; a < 10; a++) for (int b = 0; b < 10; b++) if (a != b) WANT[a][b] = product(a, pl[a], b, pl[b]);
        }
        search();
        if (PLANT && found) nplantok++;
        totnodes[z] += nodes; for (int d = 1; d <= 10; d++) { totl[z][d] += lvl[d]; if (lvl[d] && d > dp) dp = d; }
        if (nodes > NODECAP) capped = 1; else if (found) alive = 1;
        if (VERBOSE) {
            printf("rank %d, determinant %d, nu %d; candidates per member:", rk, det, NU); for (int m = 0; m < 10; m++) printf(" %d", nc[m]);
            printf("\nnodes %lld by depth:", nodes); for (int d = 1; d <= 10; d++) printf(" %lld", lvl[d]); printf("; complete cells %d\n", found);
        }
    }
    deep[z][dp]++;
    if (alive) { nalive[z]++; if (!PLANT && !NOGRAM) { printf("ALIVE base %lld (rank %d):", nbase, rk); for (int k = 0; k < 15; k++) printf(" %d %d", E[k][0], E[k][1]); printf("\n"); fflush(stdout); } }
    else if (capped) ncap[z]++; else ndead[z]++;
}

/* ---------- the symmetries: the 24 collineations of the Fano plane fixing the point 0, acting on the positions of B0 ---------- */
static int NG, GP[24][10], ORBIT; static long long norb, burn;
static void symmetries(void) {
    int hex[6][6], nh = 0, p[6];                     /* the permutations of the six flags preserving the twins and the lines among flags */
    for (p[0] = 0; p[0] < 6; p[0]++) for (p[1] = 0; p[1] < 6; p[1]++) for (p[2] = 0; p[2] < 6; p[2]++) for (p[3] = 0; p[3] < 6; p[3]++) for (p[4] = 0; p[4] < 6; p[4]++) for (p[5] = 0; p[5] < 6; p[5]++) {
        int seen = 0, ok = 1; for (int i = 0; i < 6; i++) seen |= 1 << p[i];
        if (seen != 63) continue;
        for (int i = 0; i < 6; i += 2) if (p[i] / 2 != p[i + 1] / 2) ok = 0;
        for (int l = 0; l < 3 && ok; l++) { int a = 4 + p[FLp[l][0] - 4], b = 4 + p[FLp[l][1] - 4]; if (!adj1[a][b]) ok = 0; }
        if (ok) { if (nh >= 6) { fprintf(stderr, "hexagon group too large\n"); exit(6); } memcpy(hex[nh++], p, sizeof p); }
    }
    if (nh != 6) { fprintf(stderr, "hexagon group of order %d\n", nh); exit(6); }
    int g[7]; g[0] = 0; NG = 0;
    for (g[1] = 1; g[1] < 7; g[1]++) for (g[2] = 1; g[2] < 7; g[2]++) for (g[3] = 1; g[3] < 7; g[3]++) for (g[4] = 1; g[4] < 7; g[4]++) for (g[5] = 1; g[5] < 7; g[5]++) for (g[6] = 1; g[6] < 7; g[6]++) {
        int seen = 0; for (int i = 0; i < 7; i++) seen |= 1 << g[i];
        if (seen != 127) continue;
        int gl[7], ok = 1;
        for (int j = 0; j < 7 && ok; j++) { gl[j] = -1; for (int l = 0; l < 7; l++) if (on(g[LINES[j][0]], l) && on(g[LINES[j][1]], l) && on(g[LINES[j][2]], l)) gl[j] = l; if (gl[j] < 0) ok = 0; }
        if (!ok) continue;
        if (NG >= 24) { fprintf(stderr, "too many collineations\n"); exit(6); }
        int *P = GP[NG], nf = 0;
        for (int t = 0; t < 4; t++) { P[t] = -1; for (int u = 0; u < 4; u++) if (B0lab[u] == gl[B0lab[t]]) P[t] = u; if (P[t] < 0) { fprintf(stderr, "label\n"); exit(6); } }
        for (int h = 0; h < 6; h++) { int good = 1; for (int i = 0; i < 6; i++) if (B0lab[4 + hex[h][i]] != gl[B0lab[4 + i]]) good = 0; if (good) { nf++; for (int i = 0; i < 6; i++) P[4 + i] = 4 + hex[h][i]; } }
        if (nf != 1) { fprintf(stderr, "lift not unique (%d)\n", nf); exit(6); }
        NG++;
    }
    if (NG != 24) { fprintf(stderr, "%d collineations\n", NG); exit(6); }
}
static int pairidx[10][10];
static int canonical(void) {                        /* is the current graph the least of its orbit? also adds the orbit size to the Burnside sum */
    u64 me = 0; for (int k = 0; k < 15; k++) me |= 1ULL << pairidx[E[k][0]][E[k][1]];
    int stab = 0;
    for (int g = 0; g < NG; g++) {
        u64 im = 0; for (int k = 0; k < 15; k++) im |= 1ULL << pairidx[GP[g][E[k][0]]][GP[g][E[k][1]]];
        if (im < me) return 0;
        if (im == me) stab++;
    }
    cursize = NG / stab; burn += cursize; return 1;
}

/* ---------- all the bases: simple cubic graphs on 10 vertices avoiding the six pairs ---------- */
static int deg[10], used[10][10], ne; static long long MOD = 1, RES = 0, MAXB = 1LL << 60, ngraphs;
static void gen(int v) {
    while (v < 10 && deg[v] == 3) v++;
    if (nproc >= MAXB) return;
    if (v == 10) { ngraphs++; if (ORBIT && !canonical()) return; if (ORBIT) norb++; if (nbase % MOD == RES) process(); nbase++; return; }
    int need = 3 - deg[v], cand[10], n = 0;
    for (int w = v + 1; w < 10; w++) if (deg[w] < 3 && !forb[v][w] && !used[v][w]) cand[n++] = w;
    if (n < need) return;
    int idx[3];
    for (idx[0] = 0; idx[0] < n; idx[0]++) for (idx[1] = (need > 1 ? idx[0] + 1 : 0); idx[1] < (need > 1 ? n : 1); idx[1]++) for (idx[2] = (need > 2 ? idx[1] + 1 : 0); idx[2] < (need > 2 ? n : 1); idx[2]++) {
        for (int e = 0; e < need; e++) { int w = cand[idx[e]]; deg[w]++; used[v][w] = 1; E[ne][0] = v; E[ne][1] = w; ne++; }
        int dv = deg[v]; deg[v] = 3;
        gen(v + 1);
        deg[v] = dv;
        for (int e = 0; e < need; e++) { int w = cand[idx[e]]; deg[w]--; used[v][w] = 0; ne--; }
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: fano37 all <mod> <res> [max bases] [fc]  |  fano37 base a0 b0 ... a14 b14 [fc]\n"); return 1; }
    cell(0, B0lab); cell(1, B1lab);
    for (int m = 0; m < 10; m++) { quota1[m] = 1 + on(0, B1lab[m]); quota0[m] = 1 + on(1, B0lab[m]); }
    for (int l = 0; l < 3; l++) { int a = FLp[l][0], b = FLp[l][1]; adj1[a][b] = adj1[b][a] = 1; forb[a][b] = forb[b][a] = 1; }
    forb[4][5] = forb[5][4] = forb[6][7] = forb[7][6] = forb[8][9] = forb[9][8] = 1;
    { int n = 0; for (int a = 0; a < 15; a++) for (int b = a + 1; b < 15; b++) for (int c = b + 1; c < 15; c++) { TR[n][0] = a; TR[n][1] = b; TR[n][2] = c; TRm[n] = (1 << a) | (1 << b) | (1 << c); n++; } }
    { int n = 0; for (int a = 0; a < 10; a++) for (int b = a + 1; b < 10; b++) { pairidx[a][b] = pairidx[b][a] = 44 - n; n++; } }
    symmetries();
    rowidx = calloc((size_t)10 * MAXC * 10, sizeof(int)); pool = malloc((size_t)POOLWORDS * sizeof(u64));
    if (!rowidx || !pool) { fprintf(stderr, "memory\n"); return 2; }
    if (getenv("FANO37_CAP")) NODECAP = atoll(getenv("FANO37_CAP"));
    NODISC = getenv("FANO37_NODISC") != NULL; RANKONLY = getenv("FANO37_RANKONLY") != NULL; ORBIT = getenv("FANO37_ORBIT") != NULL;
    PLANT = getenv("FANO37_PLANT") != NULL; NOGRAM = getenv("FANO37_NOGRAM") != NULL; if (NOGRAM) STOPFIRST = 1;
    double t0 = now();
    if (!strcmp(argv[1], "base")) {
        if (argc < 32) { fprintf(stderr, "30 integers expected\n"); return 1; }
        for (int k = 0; k < 15; k++) { E[k][0] = atoi(argv[2 + 2 * k]); E[k][1] = atoi(argv[3 + 2 * k]); }
        FCMODE = argc > 32; VERBOSE = 1; process();
        if (nrank[36] + nrank[35] == 0) printf("Seidel rank below 35\n"); else if (nres && !NODISC) printf("rank 36, determinant a residue: dead by the discriminant\n");
        else if (nrank[35]) printf("Seidel rank 35: %s\n", nalive[1] ? "ALIVE" : ncap[1] ? "capped" : "dead");
    } else {
        MOD = atoll(argv[2]); RES = atoll(argv[3]); if (argc > 4) MAXB = atoll(argv[4]); FCMODE = argc > 5;
        gen(0);
        printf("labelled bases enumerated %lld", ngraphs);
        if (ORBIT) printf("; orbits under the 24 collineations fixing the point 0: %lld (sum of the orbit sizes %lld)", norb, burn);
        printf("\nprocessed %lld (serial number = %lld modulo %lld); search %s%s%s%s\n", nproc, RES, MOD, FCMODE ? "with forward checking" : "lazy",
               NODISC ? "; discriminant of W NOT used" : "", NOGRAM ? "; CONTROL: products not tested" : "", PLANT ? "; CONTROL: planted cell" : "");
        printf("Seidel rank of the base:"); for (int r = 0; r < 40; r++) if (nrank[r]) printf("  %d: %lld", r, nrank[r]); printf("\n");
        if (ORBIT) { printf("the same counted with the orbit sizes (labelled bases):"); for (int r = 0; r < 40; r++) if (wrank[r]) printf("  %d: %lld", r, wrank[r]); printf(";  rank 36 with a residue determinant: %lld\n", wres); }
        printf("rank 36: determinant a residue %lld%s; candidates inconsistent on a dependent base vertex (must be 0): %lld\n", nres, NODISC ? " (searched too)" : " (dead by the discriminant)", nincons36);
        for (int z = 0; z < 2; z++) if (ntest[z]) {
            printf("rank %d: tested %lld (searches %lld): dead %lld, ALIVE %lld, stopped at the node cap %lld\n", 36 - z, ntest[z], npass[z], ndead[z], nalive[z], ncap[z]);
            printf("   mean candidates per member:"); for (int m = 0; m < 10; m++) printf(" %.0f", (double)totc[z][m] / npass[z]);
            printf("\n   mean nodes per search %.0f, by depth:", (double)totnodes[z] / npass[z]); for (int d = 1; d <= 10; d++) printf(" %.1f", (double)totl[z][d] / npass[z]);
            printf("\n   bases by deepest partial cell:"); for (int d = 0; d <= 10; d++) if (deep[z][d]) printf("  %d: %lld", d, deep[z][d]); printf("\n");
        }
        if (PLANT) printf("planted cells %lld, found again %lld; searches without any cell to plant %lld\n", nplant, nplantok, nnoplant);
    }
    printf("time %.1f s\n", now() - t0);
    return 0;
}
