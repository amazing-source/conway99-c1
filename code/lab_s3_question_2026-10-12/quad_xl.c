/* Lab session, 2026-10-12. Linearisation at degree 2 of the parity skeleton problem on BH.

   Input (from quad_setup.py): for each of the 2430 non-adjacent pairs, five linear forms rho_1..rho_5 on F_2^460.
   The skeletons are the common zeros of the quadrics
        rho_i (1 + L) = 0  (i = 1..5),      e_2(rho) + L = 0,        L = rho_1 + ... + rho_5.
   Every F_2-linear combination of these quadrics vanishes on every skeleton. This program eliminates the quadratic
   monomials x_a x_b (a < b; x_a^2 = x_a) by Gaussian elimination; the combinations whose quadratic part vanishes are
   AFFINE-LINEAR equations satisfied by every skeleton. It prints their number, the rank of their linear parts, and the
   dimension of the space they leave (460 - rank). If that dimension is 0, every parity skeleton is trivial.
   The linear consequences are written to a file (one per line: constant, then the 460 coefficients as 0/1).

   Memory: 14 580 rows x 1 657 words x 8 bytes = 193 MB, plus the same for the combination tracker if TRACK is set
   (not set here). One thread. Build: gcc -O3 -march=native -o quad_xl quad_xl.c
   Usage: quad_xl <rho file> <out file for the linear consequences> */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define NV 460
#define NQ (NV * (NV - 1) / 2)          /* quadratic monomials */
#define NB (NQ + NV + 1)                /* then the linear monomials, then the constant */
#define NW ((NB + 63) / 64)
#define VW ((NV + 63) / 64)
typedef uint64_t u64;

static int nrows;
static u64 *M;                           /* nrows x NW */
static inline int qidx(int a, int b) { return b * (b - 1) / 2 + a; }      /* a < b */
static inline void flip(u64 *row, int bit) { row[bit >> 6] ^= 1ULL << (bit & 63); }
static inline int get(const u64 *row, int bit) { return (row[bit >> 6] >> (bit & 63)) & 1; }

static void parse_hex(const char *s, u64 *v) {
    int len = (int)strlen(s), i; memset(v, 0, VW * sizeof(u64));
    for (i = 0; i < len; i++) {
        char c = s[len - 1 - i]; int d = (c >= '0' && c <= '9') ? c - '0' : (c >= 'a' && c <= 'f') ? c - 'a' + 10 : c - 'A' + 10;
        v[(4 * i) >> 6] |= (u64)d << ((4 * i) & 63);
    }
}
/* row ^= u * w (product of two linear forms without constant) */
static void add_product(u64 *row, const u64 *u, const u64 *w) {
    int a, b;
    for (a = 0; a < NV; a++) {
        int ua = (u[a >> 6] >> (a & 63)) & 1, wa = (w[a >> 6] >> (a & 63)) & 1;
        if (ua && wa) flip(row, NQ + a);
        if (!ua && !wa) continue;
        for (b = a + 1; b < NV; b++) {
            int ub = (u[b >> 6] >> (b & 63)) & 1, wb = (w[b >> 6] >> (b & 63)) & 1;
            if ((ua & wb) ^ (ub & wa)) flip(row, qidx(a, b));
        }
    }
}
static void add_linear(u64 *row, const u64 *u) { int a; for (a = 0; a < NV; a++) if ((u[a >> 6] >> (a & 63)) & 1) flip(row, NQ + a); }

int main(int argc, char **argv) {
    FILE *f; char buf[5][256]; int a, b, i, j, r, npair = 0, rank = 0, col, nlin = 0;
    u64 rho[5][VW], L[VW];
    if (argc < 3) { printf("usage: quad_xl <rho file> <out file>\n"); return 1; }
    M = calloc((size_t)2430 * 6 * NW, sizeof(u64)); if (!M) { printf("no memory\n"); return 1; }
    f = fopen(argv[1], "r"); if (!f) { printf("cannot open %s\n", argv[1]); return 1; }
    while (fscanf(f, "%d %d %255s %255s %255s %255s %255s", &a, &b, buf[0], buf[1], buf[2], buf[3], buf[4]) == 7) {
        memset(L, 0, sizeof L);
        for (i = 0; i < 5; i++) { parse_hex(buf[i], rho[i]); for (j = 0; j < VW; j++) L[j] ^= rho[i][j]; }
        for (i = 0; i < 5; i++) {                                /* rho_i (1 + L) = rho_i + rho_i L */
            u64 *row = M + (size_t)nrows * NW; nrows++;
            add_product(row, rho[i], L); add_linear(row, rho[i]);
        }
        {                                                        /* e_2(rho) + L */
            u64 *row = M + (size_t)nrows * NW; nrows++;
            for (i = 0; i < 5; i++) for (j = i + 1; j < 5; j++) add_product(row, rho[i], rho[j]);
            add_linear(row, L);
        }
        npair++;
    }
    fclose(f);
    printf("%d pairs, %d quadrics in %d variables (%d quadratic monomials)\n", npair, nrows, NV, NQ); fflush(stdout);
    /* elimination of the quadratic columns */
    {
        int *used = calloc(nrows, sizeof(int));
        for (col = 0; col < NQ; col++) {
            int p = -1;
            for (r = 0; r < nrows; r++) if (!used[r] && get(M + (size_t)r * NW, col)) { p = r; break; }
            if (p < 0) continue;
            used[p] = 1; rank++;
            {
                u64 *pr = M + (size_t)p * NW; int w0 = col >> 6;
                for (r = 0; r < nrows; r++) if (r != p && !used[r] && get(M + (size_t)r * NW, col)) {
                    u64 *rr = M + (size_t)r * NW; int w;
                    for (w = w0; w < NW; w++) rr[w] ^= pr[w];
                }
            }
            if (rank == nrows) break;
        }
        printf("rank of the quadratic parts: %d of %d quadrics\n", rank, nrows); fflush(stdout);
        /* the unused rows have zero quadratic part: affine-linear consequences */
        {
            FILE *g = fopen(argv[2], "w"); int lrank = 0, incons = 0; u64 (*piv)[VW + 1] = calloc(NV, sizeof *piv); int *has = calloc(NV, sizeof(int));
            for (r = 0; r < nrows; r++) if (!used[r]) {
                u64 *rr = M + (size_t)r * NW, v[VW + 1]; int zero = 1, c0 = get(rr, NQ + NV), k;
                memset(v, 0, sizeof v);
                for (k = 0; k < NV; k++) if (get(rr, NQ + k)) { v[k >> 6] |= 1ULL << (k & 63); zero = 0; }
                v[VW] = (u64)c0;
                if (zero && !c0) continue;                       /* dependency among the quadrics themselves */
                nlin++;
                fprintf(g, "%d ", c0); for (k = 0; k < NV; k++) fputc(get(rr, NQ + k) ? '1' : '0', g); fputc('\n', g);
                for (;;) {                                       /* rank of the linear parts */
                    int top = -1;
                    for (k = NV - 1; k >= 0; k--) if ((v[k >> 6] >> (k & 63)) & 1) { top = k; break; }
                    if (top < 0) { if (v[VW]) incons = 1; break; }
                    if (!has[top]) { has[top] = 1; memcpy(piv[top], v, sizeof v); lrank++; break; }
                    for (k = 0; k <= VW; k++) v[k] ^= piv[top][k];
                }
            }
            fclose(g);
            printf("affine-linear consequences found: %d; rank of their linear parts: %d of %d; inconsistent (0 = 1): %s\n", nlin, lrank, NV, incons ? "YES" : "no");
            printf("dimension of the space left for a parity skeleton class: %d\n", NV - lrank);
        }
    }
    return 0;
}
