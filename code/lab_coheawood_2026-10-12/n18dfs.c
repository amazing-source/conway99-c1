/* C1, lab session, 2026-10-12. Norm 18, rank-free: complete sets of double vertices of a core, by positivity.

   World of an integral (-4)-eigenvector f = 1_P - 1_Q of norm 18 (P, Q independent 9-sets, B = incidence P x Q with
   row and column sums 4). Defect of a pair of P = 2 - (number of common neighbours in Q); the same for Q.
   A double vertex d has two neighbours T in P and two neighbours U in Q, at most a matching between T and U.
   In the branch WITHOUT triple vertex the doubles are a bijection between the 18 defect edges of P (with
   multiplicity) and the 18 defect edges of Q.

   Rank-free positivity (NOTE 17.97; 7 P = 3I - A + J/9 is 7 times the projector on E_-4, 7 E_3 = 4I + A - (2/11) J):
       S4(v,v') = 3 [v=v'] - A_vv' - k4(v,v'),   k4 = (a_v - 1/9)^t M4^-1 (a_v' - 1/9) - 1/9,   M4 = 3I - A_core + J/9
       S3(v,v') = 4 [v=v'] + A_vv' - k3(v,v'),   k3 = (a_v - 2/11)^t M3^+ (a_v' - 2/11) + 2/11,  M3 = 4I + A_core - (2/11) J
   must both be positive semidefinite on every set of outside vertices.

   Combinatorial rules between two doubles (T,U), (T',U') of the same world:
     * they have at most 2 common core neighbours, at most 1 if they are adjacent;
     * a core edge p ~ q lies in ONE triangle: p in T cap T' and q in U cap U' forces B[p][q] = 0;
     * the same pair T = T' only if its defect is 2 (then U, U' are disjoint).

   This program searches the complete sets of 18 doubles in the branch "D independent" (mode ind) or with the
   adjacencies inside D left free (mode adj: every pair of chosen doubles with at most one common core neighbour may
   be adjacent; a double has at most MAXDEG neighbours in D; two adjacent doubles have exactly one common neighbour,
   so they have no common neighbour in D unless ... see the rules in the code), by depth-first search on the defect
   edges of P with both positivity tests at every node (incremental Cholesky, double precision, tolerance 1e-9:
   EXPLORATION, not a certificate).

   n18dfs <core file: 9 lines of 9 digits> <ind|adj> [first_lo first_hi] [node cap]
   first_lo, first_hi: only the candidates number first_lo <= i < first_hi of the first defect edge (slices).
   gcc -O3 -march=native -o n18dfs n18dfs.c -lm          One process, a few MB. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define M 9
#define N 18
#define MAXC 400
#define MAXS 20
#define TOL 1e-9
static int B[M][M], defP[M][M], defQ[M][M];
static int nc, cT[MAXC][2], cU[MAXC][2], cmask[MAXC], cpP[MAXC], cpQ[MAXC];
static double K4[MAXC][MAXC], K3[MAXC][MAXC];
static unsigned char comp0[MAXC][MAXC], comp1[MAXC][MAXC];      /* compatible as non-adjacent / as adjacent */
static int npP, pairP[40][2], dP[40], npQ, pairQ[40][2], dQ[40], idxP[M][M], idxQ[M][M];
static int nslot, slotpair[MAXS], slotsecond[MAXS];
static int ncs[40], cs[40][MAXC];
static int ADJ, MAXDEG = 4;
static long long nodes[MAXS + 2], tests, CAP = 1LL << 62, nsol; static int stopped;
static int chosen[MAXS], usedQ[40], deg[MAXS], adjm[MAXS][MAXS];
static double L4[MAXS][MAXS], L3[MAXS][MAXS]; static int z4[MAXS], z3[MAXS];
static int FLO = 0, FHI = 1 << 30;
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static void invert(double A[N][N], double R[N][N]) {
    static double W[N][2 * N];
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) { W[i][j] = A[i][j]; W[i][N + j] = i == j; }
    for (int c = 0; c < N; c++) {
        int p = c; for (int r = c; r < N; r++) if (fabs(W[r][c]) > fabs(W[p][c])) p = r;
        if (fabs(W[p][c]) < 1e-12) { fprintf(stderr, "singular\n"); exit(2); }
        for (int j = 0; j < 2 * N; j++) { double t = W[c][j]; W[c][j] = W[p][j]; W[p][j] = t; }
        double iv = 1 / W[c][c]; for (int j = 0; j < 2 * N; j++) W[c][j] *= iv;
        for (int r = 0; r < N; r++) if (r != c) { double f = W[r][c]; if (f != 0) for (int j = 0; j < 2 * N; j++) W[r][j] -= f * W[c][j]; }
    }
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) R[i][j] = W[i][N + j];
}

/* append row k to a Cholesky factor: s[i] = S(new, chosen_i) for i < k, diag = S(new,new). Returns 0 if not PSD. */
static int chol_add(double L[MAXS][MAXS], int *zero, int k, const double *s, double diag) {
    double y[MAXS], sum2 = 0;
    for (int i = 0; i < k; i++) {
        double t = s[i]; for (int l = 0; l < i; l++) t -= y[l] * L[i][l];
        if (zero[i]) { if (fabs(t) > 1e-7) return 0; y[i] = 0; }
        else y[i] = t / L[i][i];
        sum2 += y[i] * y[i];
    }
    double p2 = diag - sum2;
    if (p2 < -TOL) return 0;
    for (int i = 0; i < k; i++) L[k][i] = y[i];
    if (p2 < 1e-7) { zero[k] = 1; L[k][k] = 0; } else { zero[k] = 0; L[k][k] = sqrt(p2); }
    return 1;
}

static void rec(int depth);
static void try_adj(int depth, int c, int i, double *s4, double *s3, int d) {
    /* decide the adjacency of the new double (position depth) with the chosen doubles i, i+1, ...; d = its degree so far */
    if (stopped) return;
    if (i == depth) {
        tests++; if (tests > CAP) { stopped = 1; return; }
        if (!chol_add(L4, z4, depth, s4, 3 - K4[c][c])) return;
        if (!chol_add(L3, z3, depth, s3, 4 - K3[c][c])) return;
        chosen[depth] = c; usedQ[cpQ[c]]++; deg[depth] = d; nodes[depth + 1]++;
        for (int j = 0; j < depth; j++) if (adjm[depth][j]) deg[j]++;
        rec(depth + 1);
        for (int j = 0; j < depth; j++) if (adjm[depth][j]) deg[j]--;
        usedQ[cpQ[c]]--;
        return;
    }
    int w = chosen[i];
    /* non-adjacent */
    if (comp0[c][w]) {
        /* two common neighbours at most: the common core neighbours plus the chosen doubles adjacent to both */
        int cc = __builtin_popcount(cmask[c] & cmask[w]), com = 0;
        for (int j = 0; j < i; j++) if (adjm[depth][j] && adjm[i][j]) com++;
        if (cc + com <= 2) { adjm[depth][i] = adjm[i][depth] = 0; s4[i] = -K4[c][w]; s3[i] = -K3[c][w]; try_adj(depth, c, i + 1, s4, s3, d); }
    }
    if (ADJ && comp1[c][w] && d < MAXDEG && deg[i] < MAXDEG) {
        /* adjacent: exactly one common neighbour in the whole graph, so at most one among core + chosen doubles */
        int cc = __builtin_popcount(cmask[c] & cmask[w]), com = 0;
        for (int j = 0; j < i; j++) if (adjm[depth][j] && adjm[i][j]) com++;
        if (cc + com <= 1) { adjm[depth][i] = adjm[i][depth] = 1; s4[i] = -1 - K4[c][w]; s3[i] = 1 - K3[c][w]; try_adj(depth, c, i + 1, s4, s3, d + 1); adjm[depth][i] = adjm[i][depth] = 0; }
    }
}

static void rec(int depth) {
    if (stopped) return;
    if (depth == nslot) {
        /* later conflicts between a new adjacency and the common-neighbour counts of earlier pairs are re-checked here */
        for (int a = 0; a < nslot; a++) for (int b = a + 1; b < nslot; b++) {
            int cc = __builtin_popcount(cmask[chosen[a]] & cmask[chosen[b]]), com = 0;
            for (int j = 0; j < nslot; j++) if (j != a && j != b && adjm[a][j] && adjm[b][j]) com++;
            if (cc + com > (adjm[a][b] ? 1 : 2)) return;
        }
        nsol++;
        if (nsol <= 5) {
            printf("complete set:"); for (int i = 0; i < nslot; i++) printf(" (%d%d|%d%d)", cT[chosen[i]][0], cT[chosen[i]][1], cU[chosen[i]][0], cU[chosen[i]][1]);
            int e = 0; for (int a = 0; a < nslot; a++) for (int b = a + 1; b < nslot; b++) e += adjm[a][b];
            printf("  edges in D: %d\n", e); fflush(stdout);
        }
        return;
    }
    int pp = slotpair[depth];
    double s4[MAXS], s3[MAXS];
    for (int x = 0; x < ncs[pp]; x++) {
        if (depth == 0 && (x < FLO || x >= FHI)) continue;
        int c = cs[pp][x];
        if (slotsecond[depth] && c <= chosen[depth - 1]) continue;       /* the two doubles of a pair of defect 2: increasing */
        if (usedQ[cpQ[c]] >= dQ[cpQ[c]]) continue;
        int ok = 1;
        for (int i = 0; i < depth && ok; i++) if (!comp0[c][chosen[i]] && !(ADJ && comp1[c][chosen[i]])) ok = 0;
        if (!ok) continue;
        try_adj(depth, c, 0, s4, s3, 0);
        if (stopped) return;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: n18dfs <core file> <ind|adj> [first_lo first_hi] [node cap]\n"); return 1; }
    FILE *f = fopen(argv[1], "r"); if (!f) return 1;
    for (int i = 0; i < M; i++) { char line[64]; if (fscanf(f, "%63s", line) != 1) return 1; for (int j = 0; j < M; j++) B[i][j] = line[j] - '0'; }
    fclose(f);
    ADJ = !strcmp(argv[2], "adj");
    if (argc > 4) { FLO = atoi(argv[3]); FHI = atoi(argv[4]); }
    if (argc > 5) CAP = atoll(argv[5]);
    if (getenv("N18_MAXDEG")) MAXDEG = atoi(getenv("N18_MAXDEG"));
    static double A[N][N], M4[N][N], M3[N][N], I4[N][N], I3[N][N];
    for (int i = 0; i < M; i++) for (int j = 0; j < M; j++) if (B[i][j]) A[i][M + j] = A[M + j][i] = 1;
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) {
        double fi = i < M ? 1 : -1, fj = j < M ? 1 : -1;
        M4[i][j] = 3 * (i == j) - A[i][j] + 1.0 / 9; M3[i][j] = 4 * (i == j) + A[i][j] - 2.0 / 11 + fi * fj / 18;   /* + projector on f */
    }
    invert(M4, I4); invert(M3, I3);
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) { double fi = i < M ? 1 : -1, fj = j < M ? 1 : -1; I3[i][j] -= fi * fj / 18; }   /* pseudo-inverse */
    for (int a = 0; a < M; a++) for (int b = 0; b < M; b++) {
        int s = 0, t = 0; for (int k = 0; k < M; k++) { s += B[a][k] * B[b][k]; t += B[k][a] * B[k][b]; }
        defP[a][b] = 2 - s; defQ[a][b] = 2 - t;
    }
    for (int a = 0; a < M; a++) for (int b = a + 1; b < M; b++) {
        if (defP[a][b] < 0 || defQ[a][b] < 0) { fprintf(stderr, "not a core\n"); return 1; }
        idxP[a][b] = idxP[b][a] = -1; idxQ[a][b] = idxQ[b][a] = -1;
        if (defP[a][b] > 0) { idxP[a][b] = idxP[b][a] = npP; pairP[npP][0] = a; pairP[npP][1] = b; dP[npP] = defP[a][b]; npP++; }
        if (defQ[a][b] > 0) { idxQ[a][b] = idxQ[b][a] = npQ; pairQ[npQ][0] = a; pairQ[npQ][1] = b; dQ[npQ] = defQ[a][b]; npQ++; }
    }
    for (int p = 0; p < npP; p++) for (int q = 0; q < npQ; q++) {
        int *T = pairP[p], *U = pairQ[q];
        if (B[T[0]][U[0]] + B[T[0]][U[1]] > 1 || B[T[1]][U[0]] + B[T[1]][U[1]] > 1 || B[T[0]][U[0]] + B[T[1]][U[0]] > 1 || B[T[0]][U[1]] + B[T[1]][U[1]] > 1) continue;
        cT[nc][0] = T[0]; cT[nc][1] = T[1]; cU[nc][0] = U[0]; cU[nc][1] = U[1]; cpP[nc] = p; cpQ[nc] = q;
        cmask[nc] = (1 << T[0]) | (1 << T[1]) | (1 << (M + U[0])) | (1 << (M + U[1])); nc++;
    }
    static double col[MAXC][N];
    for (int c = 0; c < nc; c++) for (int i = 0; i < N; i++) col[c][i] = (cmask[c] >> i) & 1;
    for (int c = 0; c < nc; c++) {
        double v4[N], v3[N];
        for (int i = 0; i < N; i++) { double s = 0, t = 0; for (int j = 0; j < N; j++) { s += I4[i][j] * (col[c][j] - 1.0 / 9); t += I3[i][j] * (col[c][j] - 2.0 / 11); } v4[i] = s; v3[i] = t; }
        for (int e = 0; e < nc; e++) { double s = 0, t = 0; for (int i = 0; i < N; i++) { s += (col[e][i] - 1.0 / 9) * v4[i]; t += (col[e][i] - 2.0 / 11) * v3[i]; } K4[e][c] = s - 1.0 / 9; K3[e][c] = t + 2.0 / 11; }
    }
    long long n0 = 0, n1 = 0;
    for (int c = 0; c < nc; c++) for (int e = 0; e < nc; e++) {
        if (c == e) continue;
        int cc = __builtin_popcount(cmask[c] & cmask[e]), ok = cc <= 2;
        /* a core edge in two triangles */
        for (int a = 0; a < 2 && ok; a++) for (int b = 0; b < 2 && ok; b++) { int p = cT[c][a], q = cU[c][b]; if (B[p][q] && ((cmask[e] >> p) & 1) && ((cmask[e] >> (M + q)) & 1)) ok = 0; }
        if (cpP[c] == cpP[e] && dP[cpP[c]] < 2) ok = 0;
        if (cpQ[c] == cpQ[e] && dQ[cpQ[c]] < 2) ok = 0;
        double a4 = 3 - K4[c][c], b4 = 3 - K4[e][e], a3 = 4 - K3[c][c], b3 = 4 - K3[e][e];
        comp0[c][e] = ok && a4 * b4 - K4[c][e] * K4[c][e] > -TOL && a3 * b3 - K3[c][e] * K3[c][e] > -TOL;
        comp1[c][e] = ok && cc <= 1 && a4 * b4 - (1 + K4[c][e]) * (1 + K4[c][e]) > -TOL && a3 * b3 - (1 - K3[c][e]) * (1 - K3[c][e]) > -TOL;
        n0 += comp0[c][e]; n1 += comp1[c][e];
    }
    for (int c = 0; c < nc; c++) cs[cpP[c]][ncs[cpP[c]]++] = c;
    /* order of the defect pairs of P: fewest candidates first; a pair of defect 2 gives two consecutive slots */
    int ordp[40]; for (int p = 0; p < npP; p++) ordp[p] = p;
    for (int a = 1; a < npP; a++) { int v = ordp[a], b = a; while (b > 0 && ncs[ordp[b - 1]] > ncs[v]) { ordp[b] = ordp[b - 1]; b--; } ordp[b] = v; }
    for (int a = 0; a < npP; a++) for (int k = 0; k < dP[ordp[a]]; k++) { slotpair[nslot] = ordp[a]; slotsecond[nslot] = k; nslot++; }
    int tq = 0; for (int q = 0; q < npQ; q++) tq += dQ[q];
    printf("core: %d defect pairs on P, %d on Q; slots %d / %d; candidate doubles %d; ordered pairs compatible as non-adjacent %lld, as adjacent %lld\n", npP, npQ, nslot, tq, nc, n0, n1);
    printf("mode %s%s; candidates of the first defect pair: %d (searched %d .. %d)\n", ADJ ? "adj (adjacencies inside D free, degree in D at most " : "ind (D independent)", ADJ ? (MAXDEG == 4 ? "4)" : "N18_MAXDEG)") : "", ncs[slotpair[0]], FLO, FHI < ncs[slotpair[0]] ? FHI - 1 : ncs[slotpair[0]] - 1);
    if (nslot != 18 || tq != 18) { printf("defect totals are not 18: no bijection\n"); return 0; }
    double t0 = now();
    rec(0);
    printf("nodes passing both positivity tests by depth:"); for (int d = 1; d <= nslot; d++) printf(" %lld", nodes[d]);
    printf("\ncomplete sets of 18 doubles: %lld%s  [%lld tests, %.1f s]\n", nsol, stopped ? " (STOPPED at the node cap)" : " (exhaustive on the slice)", tests, now() - t0);
    return 0;
}
