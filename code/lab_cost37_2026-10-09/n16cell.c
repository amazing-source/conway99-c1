/* C1, lab session, 2026-10-10. Rank 37 against one world of norm 16 (core + D + Z, 35 vertices, Seidel rank 33):
   the test of n16_cell_test.py in C (same search, same node counts).

   Rank 37 <=> the vertices are isotropic vectors of a non-degenerate 36-dimensional space over F_7, product 6 on
   edges and 1 on non-edges. The base spans a non-degenerate subspace V of dimension 33, a new vertex a is v_a + r_a
   with r_a in the 3-dimensional complement, and for a set S of new vertices the matrix
       R[a][b] = t_ab - <v_a, v_b>     (t_aa = 0, t_ab = 6 if a ~ b, 1 otherwise)
   is the Gram matrix of the r_a: rank(R) <= 3 modulo 7.
   Cell of a core vertex c = its simple neighbours (8). With the core and D neighbours of c they are the whole
   neighbourhood of c: seven disjoint edges, and every other base vertex x has exactly
       (1 if x ~ c else 2) - |N(x) & N(c) & base|
   neighbours among the members. A member with no neighbour among the base neighbours of c is matched with another
   member. Two members share at most 2 - [adjacent] base neighbours (c included), exactly 2 inside one cell (p,q).
   A cell with no completion kills the world at rank 37. The discriminant of the space is not used.

   Input (text, from n16_world_to_text.py):  n ndom / n rows of 0,1 / for each domain: p q multiplicity nmasks masks...
   n16cell <world.txt> [node cap per cell] [rank|norank] [first]
     norank: control (rank not tested);  first: stop at the first dead cell.
   Output: one line per cell and a verdict.   gcc -O3 -march=native -o n16cell n16cell.c     One process, a few MB. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef unsigned long long u64;
#define NB 40
#define MAXD 64
#define MAXM 512
#define MAXS 12
static int n, ndom, A[NB][NB], K[NB][NB], I[NB], nI, Kinv[NB][NB];
static int dp[MAXD], dq[MAXD], dmult[MAXD], dn[MAXD]; static u64 dmask[MAXD][MAXM];
static u64 nbr[NB];
static const int inv7[7] = {0, 1, 4, 5, 2, 3, 6};
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static int rank7(int k, int M[MAXS][MAXS]) {
    int a[MAXS][MAXS], rk = 0;
    for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) a[i][j] = M[i][j];
    for (int c = 0; c < k; c++) {
        int p = -1; for (int r = rk; r < k; r++) if (a[r][c]) { p = r; break; }
        if (p < 0) continue;
        if (p != rk) for (int j = 0; j < k; j++) { int t = a[rk][j]; a[rk][j] = a[p][j]; a[p][j] = t; }
        int iv = inv7[a[rk][c]]; for (int j = 0; j < k; j++) a[rk][j] = a[rk][j] * iv % 7;
        for (int r = 0; r < k; r++) if (r != rk && a[r][c]) { int f = 7 - a[r][c]; for (int j = 0; j < k; j++) a[r][j] = (a[r][j] + f * a[rk][j]) % 7; }
        rk++;
    }
    return rk;
}

/* one cell */
typedef struct { u64 m; unsigned char s[36], c[36]; int npart; } cand_t;
static cand_t *cand[MAXD]; static int ncand[MAXD];
static int nslot, sdom[MAXS], need[NB]; static u64 need1, need2;
static long long nodes, CAP, lv[MAXS + 1], sols; static int stopped, NORANK;
static cand_t *chosen[MAXS]; static int chidx[MAXS], partner[MAXS], R[MAXS][MAXS];

static inline int prod(const cand_t *a, const cand_t *b) { int s = 0; for (int i = 0; i < nI; i++) s += a->s[i] * b->c[i]; return s % 7; }

static void rec(int pos, u64 c1, u64 c2) {          /* c1: base vertices with at least one member neighbour, c2: with two */
    if (stopped) return;
    if (pos == nslot) {
        if ((c1 & (need1 | need2)) != (need1 | need2) || (c2 & need2) != need2) return;
        for (int i = 0; i < nslot; i++) if (partner[i] == -1) return;
        sols++; return;
    }
    int di = sdom[pos], start = (pos > 0 && sdom[pos - 1] == di) ? chidx[pos - 1] + 1 : 0;
    u64 sat = (c1 & need1) | (c2 & need2);            /* saturated base vertices */
    for (int ci = start; ci < ncand[di]; ci++) {
        cand_t *cd = &cand[di][ci]; u64 m = cd->m;
        if (m & sat) continue;
        int nopt = 0, opts[MAXS + 1];
        if (cd->npart == 1) opts[nopt++] = -2;
        else { opts[nopt++] = -1; for (int j = 0; j < pos; j++) if (partner[j] == -1) opts[nopt++] = j; }
        int pr[MAXS], share[MAXS], okshare = 1;
        for (int j = 0; j < pos; j++) {
            share[j] = __builtin_popcountll(m & chosen[j]->m);
            if (share[j] > 2 || (sdom[j] == di && share[j] != 2)) { okshare = 0; break; }
        }
        if (!okshare) continue;
        int have = 0, self = 0;
        for (int o = 0; o < nopt; o++) {
            int op = opts[o];
            if (op >= 0 && share[op] > 1) continue;
            nodes++;
            if (nodes > CAP) { stopped = 1; return; }
            if (!have) { for (int j = 0; j < pos; j++) pr[j] = prod(cd, chosen[j]); self = prod(cd, cd); have = 1; }
            for (int j = 0; j < pos; j++) { int v = ((op == j ? 6 : 1) - pr[j] + 7) % 7; R[pos][j] = R[j][pos] = v; }
            R[pos][pos] = (7 - self) % 7;
            if (!NORANK && rank7(pos + 1, R) > 3) continue;
            lv[pos + 1]++;
            chosen[pos] = cd; chidx[pos] = ci; partner[pos] = op; if (op >= 0) partner[op] = pos;
            rec(pos + 1, c1 | m, c2 | (c1 & m));
            if (op >= 0) partner[op] = -1;
            if (stopped) return;
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: n16cell <world.txt> [node cap per cell] [rank|norank] [first]\n"); return 1; }
    FILE *f = fopen(argv[1], "r"); if (!f) { fprintf(stderr, "cannot open\n"); return 1; }
    CAP = argc > 2 ? atoll(argv[2]) : 2000000000LL; NORANK = argc > 3 && !strcmp(argv[3], "norank"); int FIRST = argc > 4 && !strcmp(argv[4], "first");
    if (fscanf(f, "%d %d", &n, &ndom) != 2 || n > 36 || ndom > MAXD) { fprintf(stderr, "bad header\n"); return 1; }
    for (int i = 0; i < n; i++) { char row[64]; if (fscanf(f, "%63s", row) != 1) return 1; for (int j = 0; j < n; j++) A[i][j] = row[j] == '1'; }
    for (int d = 0; d < ndom; d++) {
        if (fscanf(f, "%d %d %d %d", &dp[d], &dq[d], &dmult[d], &dn[d]) != 4 || dn[d] > MAXM) { fprintf(stderr, "bad domain\n"); return 1; }
        for (int k = 0; k < dn[d]; k++) if (fscanf(f, "%llu", &dmask[d][k]) != 1) return 1;
    }
    fclose(f);
    for (int i = 0; i < n; i++) { nbr[i] = 0; for (int j = 0; j < n; j++) { K[i][j] = i == j ? 0 : (A[i][j] ? 6 : 1); if (A[i][j]) nbr[i] |= 1ULL << j; } }
    /* independent rows and inverse */
    { static int bas[NB][NB]; int piv[NB]; nI = 0;
      for (int i = 0; i < n; i++) {
          int v[NB]; for (int j = 0; j < n; j++) v[j] = K[i][j];
          for (int b = 0; b < nI; b++) if (v[piv[b]]) { int fct = 7 - v[piv[b]]; for (int j = 0; j < n; j++) v[j] = (v[j] + fct * bas[b][j]) % 7; }
          int p = -1; for (int j = 0; j < n; j++) if (v[j]) { p = j; break; }
          if (p < 0) continue;
          int iv = inv7[v[p]]; for (int j = 0; j < n; j++) bas[nI][j] = v[j] * iv % 7;
          piv[nI] = p; I[nI++] = i;
      }
      static int M[NB][2 * NB];
      for (int i = 0; i < nI; i++) for (int j = 0; j < nI; j++) { M[i][j] = K[I[i]][I[j]]; M[i][nI + j] = i == j; }
      for (int c = 0; c < nI; c++) {
          int p = -1; for (int r = c; r < nI; r++) if (M[r][c]) { p = r; break; }
          if (p < 0) { fprintf(stderr, "singular\n"); return 2; }
          if (p != c) for (int j = 0; j < 2 * nI; j++) { int t = M[c][j]; M[c][j] = M[p][j]; M[p][j] = t; }
          int iv = inv7[M[c][c]]; for (int j = 0; j < 2 * nI; j++) M[c][j] = M[c][j] * iv % 7;
          for (int r = 0; r < nI; r++) if (r != c && M[r][c]) { int fct = 7 - M[r][c]; for (int j = 0; j < 2 * nI; j++) M[r][j] = (M[r][j] + fct * M[c][j]) % 7; }
      }
      for (int i = 0; i < nI; i++) for (int j = 0; j < nI; j++) Kinv[i][j] = M[i][nI + j];
    }
    printf("base %d vertices, Seidel rank %d, residual dimension %d; %s\n", n, nI, 36 - nI, NORANK ? "CONTROL: rank not tested" : "rank of the residual Gram matrix <= residual dimension tested");
    if (nI != 33) { printf("this program treats bases of rank 33 only\n"); return 3; }
    for (int d = 0; d < ndom; d++) cand[d] = malloc(sizeof(cand_t) * (dn[d] + 1));
    int dead = 0, ncell = 0; double tall = now();
    for (int side = 0; side < 2 && !(FIRST && dead); side++) for (int idx = 0; idx < 8 && !(FIRST && dead); idx++) {
        int c0 = side * 8 + idx; double t0 = now(); long long bad = 0;
        need1 = need2 = 0; int oversat = 0;
        for (int x = 0; x < n; x++) { need[x] = 0; if (x == c0) continue; need[x] = (A[x][c0] ? 1 : 2) - __builtin_popcountll(nbr[x] & nbr[c0]); if (need[x] < 0) oversat = 1; if (need[x] == 1) need1 |= 1ULL << x; if (need[x] == 2) need2 |= 1ULL << x; }
        if (oversat) { printf("  cell of %c%d: base over-saturated\n", side ? 'Q' : 'P', idx); continue; }
        u64 zero = 0; for (int x = 0; x < n; x++) if (x != c0 && need[x] == 0) zero |= 1ULL << x;
        int cd_list[MAXD], nd = 0;
        for (int d = 0; d < ndom; d++) if ((side ? dq[d] : dp[d]) == idx) {
            ncand[d] = 0;
            for (int k = 0; k < dn[d]; k++) {
                u64 m = dmask[d][k]; cand_t *c = &cand[d][ncand[d]];
                if (!((m >> c0) & 1)) { fprintf(stderr, "mask without the cell vertex\n"); return 4; }
                int s[NB]; for (int j = 0; j < n; j++) s[j] = ((m >> j) & 1) ? 6 : 1;
                for (int a = 0; a < nI; a++) { int t = 0; for (int b = 0; b < nI; b++) t += Kinv[a][b] * s[I[b]]; c->c[a] = t % 7; c->s[a] = s[I[a]]; }
                int ok = 1; for (int x = 0; x < n && ok; x++) { int t = 0; for (int a = 0; a < nI; a++) t += K[x][I[a]] * c->c[a]; if (t % 7 != s[x]) ok = 0; }
                if (!ok) { bad++; continue; }
                if (m & zero) continue;
                c->npart = __builtin_popcountll(m & nbr[c0]); if (c->npart > 1) continue;
                c->m = m; ncand[d]++;
            }
            cd_list[nd++] = d;
        }
        for (int a = 1; a < nd; a++) { int v = cd_list[a], b = a; while (b > 0 && ncand[cd_list[b - 1]] > ncand[v]) { cd_list[b] = cd_list[b - 1]; b--; } cd_list[b] = v; }
        nslot = 0; for (int a = 0; a < nd; a++) for (int k = 0; k < dmult[cd_list[a]]; k++) sdom[nslot++] = cd_list[a];
        nodes = 0; sols = 0; stopped = 0; memset(lv, 0, sizeof lv); for (int i = 0; i < MAXS; i++) partner[i] = -1;
        rec(0, 0, 0);
        ncell++;
        printf("  cell of %c%d: %d members, candidates per domain [", side ? 'Q' : 'P', idx, nslot); for (int a = 0; a < nd; a++) printf("%s%d", a ? ", " : "", ncand[cd_list[a]]);
        printf("] (masks contradicting the relations: %lld); nodes %lld, kept by depth [", bad, nodes); for (int d = 1; d <= nslot; d++) printf("%s%lld", d > 1 ? ", " : "", lv[d]);
        if (stopped) printf("]; STOPPED at the node cap (%lld complete cells so far)", sols); else if (sols == 0) { printf("]; DEAD"); dead++; } else printf("]; %lld complete cells", sols);
        printf("  [%.1f s]\n", now() - t0); fflush(stdout);
    }
    printf("cells without any admissible completion: %d of %d searched%s  [%.1f s]\n", dead, ncell, NORANK ? "" : (dead ? "  => WORLD DEAD at rank 37" : "  => not decided"), now() - tall);
    return 0;
}
