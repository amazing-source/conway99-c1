/* Exact solver for the Route-Omega column stage in 3-layer form (notes/163).
   Input (stdin): m ; then 3 lines with the layer matchings (m ints each: mate of i in layer 0, 1, 2) ;
   then three m x m matrices N01, N02, N12 (row-major).  Finds sets of triples (p0,p1,p2), p_i an edge of the
   cocktail-party graph of layer i, every edge of every layer used exactly once, with
   #{t : u in p_i(t), u' in p_j(t)} = Nij[u][u'].  Generalised exact cover with cell capacities, dancing via
   alive flags + trail.  Usage: colsolve MAXSOL MAXNODES [print] < instance
   Output: "solutions S nodes N complete C" (C=1 iff the search finished, i.e. S is the exact count when S < MAXSOL). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define MAXM 24
static int m, mate[3][MAXM], N[3][MAXM][MAXM];   /* N[0]=01, N[1]=02, N[2]=12 */
static int nE[3], eu[3][400], ev[3][400], eid[3][MAXM][MAXM];
static int nopt; static int *opt_e;     /* 3 per option: item index (layer*400 + edge) */
static int *opt_c;                      /* 12 per option: cell index */
static int nitem, ncell;
static int *item_cnt, *item_cov, **item_opts, *item_nopts;
static int *cell_cap, *cell_cnt, **cell_opts, *cell_nopts;
static char *alive;
static int *trail, trail_top;
static long long nodes, maxnodes, nsol, maxsol; static int print_sol, *chosen, depth;
static int item_of(int L, int e) { return L * 400 + e; }
static int cell_of(int k, int u, int w) { return k * MAXM * MAXM + u * MAXM + w; }

static void kill(int o) {
    alive[o] = 0; trail[trail_top++] = o;
    for (int t = 0; t < 3; t++) item_cnt[opt_e[3 * o + t]]--;
    for (int t = 0; t < 12; t++) cell_cnt[opt_c[12 * o + t]]--;
}
static void undo_to(int mark) {
    while (trail_top > mark) {
        int o = trail[--trail_top]; alive[o] = 1;
        for (int t = 0; t < 3; t++) item_cnt[opt_e[3 * o + t]]++;
        for (int t = 0; t < 12; t++) cell_cnt[opt_c[12 * o + t]]++;
    }
}
static int all_items[1200], n_all_items;

static int consistent(void) {
    for (int i = 0; i < n_all_items; i++) { int it = all_items[i]; if (!item_cov[it] && item_cnt[it] == 0) return 0; }
    return 1;
}
static int cells_ok(int o) {   /* after choosing o: check its cells' remaining capacity vs supply */
    for (int t = 0; t < 12; t++) { int c = opt_c[12 * o + t]; if (cell_cap[c] > cell_cnt[c]) return 0; }
    return 1;
}

static void search(void) {
    if (nsol >= maxsol || nodes >= maxnodes) return;
    nodes++;
    int best = -1, bc = 1 << 30;
    for (int i = 0; i < n_all_items; i++) {
        int it = all_items[i];
        if (!item_cov[it] && item_cnt[it] < bc) { bc = item_cnt[it]; best = it; if (bc <= 1) break; }
    }
    if (best < 0) {
        nsol++;
        if (print_sol) { printf("SOL"); for (int d = 0; d < depth; d++) printf(" %d", chosen[d]); printf("\n"); }
        return;
    }
    if (bc == 0) return;
    for (int k = 0; k < item_nopts[best]; k++) {
        int o = item_opts[best][k]; if (!alive[o]) continue;
        int mark = trail_top;
        /* choose o: cover its items, decrement caps */
        for (int t = 0; t < 3; t++) item_cov[opt_e[3 * o + t]] = 1;
        kill(o);
        for (int t = 0; t < 3; t++) {
            int it = opt_e[3 * o + t];
            for (int q = 0; q < item_nopts[it]; q++) { int o2 = item_opts[it][q]; if (alive[o2]) kill(o2); }
        }
        int ok = 1;
        for (int t = 0; t < 12; t++) {
            int c = opt_c[12 * o + t]; cell_cap[c]--;
            if (cell_cap[c] == 0)
                for (int q = 0; q < cell_nopts[c]; q++) { int o2 = cell_opts[c][q]; if (alive[o2]) kill(o2); }
        }
        /* capacity feasibility on all cells touched by killed options is expensive; check cells of o and items */
        if (!consistent()) ok = 0;
        if (ok) {
            for (int t = 0; t < 12 && ok; t++) { int c = opt_c[12 * o + t]; if (cell_cap[c] > cell_cnt[c]) ok = 0; }
        }
        if (ok) { chosen[depth++] = o; search(); depth--; }
        for (int t = 0; t < 12; t++) cell_cap[opt_c[12 * o + t]]++;
        for (int t = 0; t < 3; t++) item_cov[opt_e[3 * o + t]] = 0;
        undo_to(mark);
        if (nsol >= maxsol || nodes >= maxnodes) return;
    }
}

int main(int argc, char **argv) {
    maxsol = atoll(argv[1]); maxnodes = atoll(argv[2]); print_sol = argc > 3;
    if (scanf("%d", &m) != 1) return 1;
    for (int L = 0; L < 3; L++) for (int i = 0; i < m; i++) scanf("%d", &mate[L][i]);
    for (int k = 0; k < 3; k++) for (int i = 0; i < m; i++) for (int j = 0; j < m; j++) scanf("%d", &N[k][i][j]);
    for (int L = 0; L < 3; L++) {
        nE[L] = 0;
        for (int i = 0; i < m; i++) for (int j = i + 1; j < m; j++)
            if (mate[L][i] != j) { eu[L][nE[L]] = i; ev[L][nE[L]] = j; eid[L][i][j] = eid[L][j][i] = nE[L]++; }
    }
    /* options */
    long cap = (long)nE[0] * nE[1] * nE[2];
    opt_e = malloc(sizeof(int) * 3 * cap); opt_c = malloc(sizeof(int) * 12 * cap);
    nopt = 0;
    for (int a = 0; a < nE[0]; a++) for (int b = 0; b < nE[1]; b++) {
        int x[2] = {eu[0][a], ev[0][a]}, z[2] = {eu[1][b], ev[1][b]}, ok = 1;
        for (int i = 0; i < 2 && ok; i++) for (int j = 0; j < 2; j++) if (N[0][x[i]][z[j]] <= 0) ok = 0;
        if (!ok) continue;
        for (int c = 0; c < nE[2]; c++) {
            int y[2] = {eu[2][c], ev[2][c]}, ok2 = 1;
            for (int i = 0; i < 2 && ok2; i++) for (int j = 0; j < 2; j++)
                if (N[1][x[i]][y[j]] <= 0 || N[2][z[i]][y[j]] <= 0) ok2 = 0;
            if (!ok2) continue;
            opt_e[3 * nopt] = item_of(0, a); opt_e[3 * nopt + 1] = item_of(1, b); opt_e[3 * nopt + 2] = item_of(2, c);
            int q = 0;
            for (int i = 0; i < 2; i++) for (int j = 0; j < 2; j++) {
                opt_c[12 * nopt + q++] = cell_of(0, x[i], z[j]);
                opt_c[12 * nopt + q++] = cell_of(1, x[i], y[j]);
                opt_c[12 * nopt + q++] = cell_of(2, z[i], y[j]);
            }
            nopt++;
        }
    }
    nitem = 3 * 400; ncell = 3 * MAXM * MAXM;
    item_cnt = calloc(nitem, sizeof(int)); item_cov = calloc(nitem, sizeof(int)); item_nopts = calloc(nitem, sizeof(int));
    item_opts = calloc(nitem, sizeof(int *));
    cell_cap = calloc(ncell, sizeof(int)); cell_cnt = calloc(ncell, sizeof(int)); cell_nopts = calloc(ncell, sizeof(int));
    cell_opts = calloc(ncell, sizeof(int *));
    for (int o = 0; o < nopt; o++) {
        for (int t = 0; t < 3; t++) item_nopts[opt_e[3 * o + t]]++;
        for (int t = 0; t < 12; t++) cell_nopts[opt_c[12 * o + t]]++;
    }
    for (int i = 0; i < nitem; i++) { item_opts[i] = malloc(sizeof(int) * (item_nopts[i] + 1)); item_cnt[i] = 0; }
    for (int c = 0; c < ncell; c++) { cell_opts[c] = malloc(sizeof(int) * (cell_nopts[c] + 1)); cell_cnt[c] = 0; }
    for (int o = 0; o < nopt; o++) {
        for (int t = 0; t < 3; t++) { int it = opt_e[3 * o + t]; item_opts[it][item_cnt[it]++] = o; }
        for (int t = 0; t < 12; t++) { int c = opt_c[12 * o + t]; cell_opts[c][cell_cnt[c]++] = o; }
    }
    for (int k = 0; k < 3; k++) for (int i = 0; i < m; i++) for (int j = 0; j < m; j++) cell_cap[cell_of(k, i, j)] = N[k][i][j];
    n_all_items = 0;
    for (int L = 0; L < 3; L++) for (int e = 0; e < nE[L]; e++) all_items[n_all_items++] = item_of(L, e);
    alive = malloc(nopt); memset(alive, 1, nopt);
    trail = malloc(sizeof(int) * (nopt + 16)); trail_top = 0;
    chosen = malloc(sizeof(int) * 1200); depth = 0;
    int bad = 0;
    for (int k = 0; k < 3; k++) for (int i = 0; i < m; i++) for (int j = 0; j < m; j++)
        if (N[k][i][j] < 0) bad = 1;
    clock_t t0 = clock();
    if (!bad && consistent()) search();
    int complete = (nsol < maxsol && nodes < maxnodes);
    printf("options %d solutions %lld nodes %lld complete %d time %.3f\n", nopt, nsol, nodes, complete,
           (double)(clock() - t0) / CLOCKS_PER_SEC);
    if (print_sol) {   /* decode option ids */
        printf("OPTDECODE");
        for (int d = 0; d < 0; d++) ;
        printf("\n");
    }
    return 0;
}
