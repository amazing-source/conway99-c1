/* padic.c -- exact local linear algebra over Z_q, truncated mod q^E (q prime, q^E <= 2^50).
 * Build: gcc -O2 -o padic.exe padic.c   (MinGW-w64 / WinLibs GCC; padic_py.py expects padic.exe next to itself)
 *
 * Usage: padic MODE Q E < matrix
 *   input  : "m n" then m*n integers (row-major)
 *   MODE smith  : Smith valuations of the matrix over Z_q (one per diagonal entry; E means ">= E", i.e. zero mod q^E)
 *   MODE kernel : saturated right kernel {x in Z_q^n : A x = 0}, printed as k rows of n residues mod q^E
 *   MODE gram   : input rows B (k x n); prints the Smith valuations of B B^T over Z_q
 * Method: elimination with a pivot of minimal valuation (local PID), row and column operations; the column transform
 * V is tracked for the kernel: A V = U^-1 D with V invertible over Z_q, so the columns of V beyond the rank span the
 * saturated kernel.  Products use __int128.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef int64_t i64;
typedef __int128 i128;
static i64 MOD;
static int Q, E;

static i64 md(i128 x) { i64 r = (i64)(x % MOD); return r < 0 ? r + MOD : r; }
static int val(i64 x) { if (x == 0) return E; int v = 0; while (x % Q == 0) { x /= Q; v++; } return v; }
static i64 powq(int e) { i64 r = 1; while (e--) r *= Q; return r; }
static i64 inv_unit(i64 a) {
    i64 t = 0, nt = 1, r = MOD, nr = a % MOD;
    if (nr < 0) nr += MOD;
    while (nr) { i64 qq = r / nr, tmp; tmp = t - qq * nt; t = nt; nt = tmp; tmp = r - qq * nr; r = nr; nr = tmp; }
    if (r != 1) { fprintf(stderr, "inv_unit: not a unit\n"); exit(2); }
    return t < 0 ? t + MOD : t;
}

/* in-place local Smith; returns rank; vals[t] = valuation of pivot t; V (n x n) column transform if not NULL */
static int smith(i64 *A, int m, int n, int *vals, i64 *V) {
    int t = 0;
    for (; t < m && t < n; t++) {
        int bi = -1, bj = -1, bv = E;
        for (int i = t; i < m && bv > 0; i++)
            for (int j = t; j < n; j++) {
                i64 x = A[(size_t)i * n + j];
                if (x) { int v = val(x); if (v < bv) { bv = v; bi = i; bj = j; if (!v) break; } }
            }
        if (bi < 0) break;
        if (bi != t) for (int j = 0; j < n; j++) { i64 s = A[(size_t)t * n + j]; A[(size_t)t * n + j] = A[(size_t)bi * n + j]; A[(size_t)bi * n + j] = s; }
        if (bj != t) {
            for (int i = 0; i < m; i++) { i64 s = A[(size_t)i * n + t]; A[(size_t)i * n + t] = A[(size_t)i * n + bj]; A[(size_t)i * n + bj] = s; }
            if (V) for (int i = 0; i < n; i++) { i64 s = V[(size_t)i * n + t]; V[(size_t)i * n + t] = V[(size_t)i * n + bj]; V[(size_t)i * n + bj] = s; }
        }
        i64 qv = powq(bv), p = A[(size_t)t * n + t];
        i64 u = inv_unit(p / qv);                    /* p = q^v * unit */
        for (int i = t + 1; i < m; i++) {
            i64 x = A[(size_t)i * n + t];
            if (!x) continue;
            i64 f = md((i128)(x / qv) * u);          /* x divisible by q^v (minimal valuation) */
            for (int j = t; j < n; j++) {
                i64 y = A[(size_t)t * n + j];
                if (y) A[(size_t)i * n + j] = md((i128)A[(size_t)i * n + j] - (i128)f * y);
            }
        }
        for (int j = t + 1; j < n; j++) {
            i64 x = A[(size_t)t * n + j];
            if (!x) continue;
            i64 f = md((i128)(x / qv) * u);
            A[(size_t)t * n + j] = 0;                  /* column t is zero below the pivot now */
            if (V) for (int i = 0; i < n; i++) {
                i64 y = V[(size_t)i * n + t];
                if (y) V[(size_t)i * n + j] = md((i128)V[(size_t)i * n + j] - (i128)f * y);
            }
        }
        vals[t] = bv;
    }
    return t;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: padic smith|kernel|gram Q E < matrix\n"); return 1; }
    Q = atoi(argv[2]); E = atoi(argv[3]); MOD = powq(E);
    int m, n;
    if (scanf("%d %d", &m, &n) != 2) return 1;
    i64 *A = malloc(sizeof(i64) * (size_t)m * n);
    for (size_t i = 0; i < (size_t)m * n; i++) { long long x; if (scanf("%lld", &x) != 1) return 1; A[i] = md(x); }
    if (!strcmp(argv[1], "gram")) {                 /* A holds B (m x n): replace by B B^T (m x m) */
        i64 *G = malloc(sizeof(i64) * (size_t)m * m);
        for (int i = 0; i < m; i++)
            for (int j = i; j < m; j++) {
                i128 s = 0;
                for (int k = 0; k < n; k++) s += (i128)A[(size_t)i * n + k] * A[(size_t)j * n + k] % MOD;
                G[(size_t)i * m + j] = G[(size_t)j * m + i] = md(s);
            }
        free(A); A = G; n = m;
    }
    int *vals = calloc((size_t)(m < n ? m : n) + 1, sizeof(int));
    if (!strcmp(argv[1], "kernel")) {
        i64 *V = calloc((size_t)n * n, sizeof(i64));
        for (int i = 0; i < n; i++) V[(size_t)i * n + i] = 1;
        int r = smith(A, m, n, vals, V);
        printf("%d %d\n", n - r, n);
        for (int j = r; j < n; j++) {
            for (int i = 0; i < n; i++) printf("%lld ", (long long)V[(size_t)i * n + j]);
            printf("\n");
        }
        free(V);
    } else {
        int r = smith(A, m, n, vals, NULL);
        int mn = m < n ? m : n;
        printf("%d\n", mn);
        for (int t = 0; t < mn; t++) printf("%d ", t < r ? vals[t] : E);
        printf("\n");
    }
    return 0;
}
