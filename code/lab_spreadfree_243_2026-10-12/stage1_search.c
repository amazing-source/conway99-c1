/* Lab session, 2026-10-13. Stage 1 of the staged census in C: all pairwise compatible families of rows for the freed
   vertices of the block (see staged_census.py). Two rows N (vertex p) and M (vertex q) are compatible when
   [q in N] = [p in M] and popcount(N & M) = T[p][q] - [q in N].
   Depth-first search, smallest list first, forward checking. The first vertex runs over the given representatives.
   Input: file written by stage1_export.py. Output: one line per family (the row index of each vertex), flag ORIGINAL / NEW.
   gcc -O3 -march=native -o stage1_search stage1_search.c ;  stage1_search <file.bin> <max seconds> <out file>   */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#define MAXV 60
static int NV, NF, W, NREP, pbit[MAXV], cnt[MAXV], T[MAXV][MAXV], origidx[MAXV], *reps;
static uint64_t *rows[MAXV];
static int *lists[MAXV + 1][MAXV], llen[MAXV + 1][MAXV], fixedrow[MAXV], isfixed[MAXV];
static long long nodes = 0, nfam = 0, nnew = 0; static time_t t0; static double tmax; static int stop = 0; static FILE *out;
static inline int bit(const uint64_t *r, int b) { return (int)((r[b >> 6] >> (b & 63)) & 1); }
static inline int compat(int p, int i, int q, int j) {
    const uint64_t *N = rows[p] + (size_t)i * W, *M = rows[q] + (size_t)j * W;
    int a = bit(N, pbit[q]); if (a != bit(M, pbit[p])) return 0;
    int c = 0; for (int k = 0; k < W; k++) c += __builtin_popcountll(N[k] & M[k]);
    return c == T[p][q] - a;
}
static void search(int depth) {
    if (stop) return;
    if ((nodes & 1023) == 0 && difftime(time(NULL), t0) > tmax) { stop = 1; return; }
    int best = -1;
    for (int v = 0; v < NV; v++) if (!isfixed[v] && (best < 0 || llen[depth][v] < llen[depth][best])) best = v;
    if (best < 0) {
        nfam++; int same = 1; for (int v = 0; v < NV; v++) if (fixedrow[v] != origidx[v]) same = 0;
        if (!same) nnew++;
        for (int v = 0; v < NV; v++) fprintf(out, "%d ", fixedrow[v]);
        fprintf(out, "%s\n", same ? "ORIGINAL" : "NEW"); fflush(out);
        return;
    }
    nodes++;
    for (int a = 0; a < llen[depth][best]; a++) {
        int i = lists[depth][best][a], ok = 1;
        for (int v = 0; v < NV && ok; v++) {
            if (isfixed[v] || v == best) continue;
            int m = 0, *src = lists[depth][v], *dst = lists[depth + 1][v];
            for (int b = 0; b < llen[depth][v]; b++) if (compat(best, i, v, src[b])) dst[m++] = src[b];
            llen[depth + 1][v] = m; if (m == 0) ok = 0;
        }
        if (!ok) continue;
        isfixed[best] = 1; fixedrow[best] = i; search(depth + 1); isfixed[best] = 0;
        if (stop) return;
    }
}
int main(int argc, char **argv) {
    if (argc < 4) return 2;
    FILE *f = fopen(argv[1], "rb"); tmax = atof(argv[2]); out = fopen(argv[3], "w"); int hdr[5];
    if (!f || !out || fread(hdr, 4, 5, f) != 5) return 1;
    NV = hdr[0]; NF = hdr[1]; W = hdr[2]; NREP = hdr[3];
    for (int v = 0; v < NV; v++) { int a[2]; if (fread(a, 4, 2, f) != 2) return 1; pbit[v] = a[0]; cnt[v] = a[1]; }
    for (int v = 0; v < NV; v++) for (int w = 0; w < NV; w++) if (fread(&T[v][w], 4, 1, f) != 1) return 1;
    reps = malloc(4 * (size_t)NREP); if (fread(reps, 4, NREP, f) != (size_t)NREP) return 1;
    for (int v = 0; v < NV; v++) if (fread(&origidx[v], 4, 1, f) != 1) return 1;
    for (int v = 0; v < NV; v++) { rows[v] = malloc((size_t)cnt[v] * W * 8); if (fread(rows[v], 8, (size_t)cnt[v] * W, f) != (size_t)cnt[v] * W) return 1; }
    for (int d = 0; d <= NV; d++) for (int v = 0; v < NV; v++) lists[d][v] = malloc(4 * (size_t)cnt[v]);
    t0 = time(NULL);
    for (int r = 0; r < NREP && !stop; r++) {
        int i = reps[r], ok = 1;
        for (int v = 1; v < NV && ok; v++) { int m = 0; for (int b = 0; b < cnt[v]; b++) if (compat(0, i, v, b)) lists[1][v][m++] = b; llen[1][v] = m; if (!m) ok = 0; }
        if (ok) { for (int v = 0; v < NV; v++) isfixed[v] = 0; isfixed[0] = 1; fixedrow[0] = i; search(1); }
        if (r % 200 == 0) { printf("first row %d / %d: %lld families (%lld new), %lld nodes, %.0f s\n", r + 1, NREP, nfam, nnew, nodes, difftime(time(NULL), t0)); fflush(stdout); }
    }
    printf("stage 1 %s: %lld compatible families, %lld different from the input, %lld nodes, %.0f s\n", stop ? "NOT FINISHED" : "complete", nfam, nnew, nodes, difftime(time(NULL), t0));
    return 0;
}
