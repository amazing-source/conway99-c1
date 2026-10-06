/* Fincke-Pohst enumeration of all integer x with  x^T G x + 2 lin.x + c0 <= bound  (G positive definite).
   Input (stdin): n, then G (n*n ints), lin (n ints), c0, bound.
   Output (stdout, binary): for each solution, int32 value followed by n int32 coordinates.
   Exact integer evaluation at the leaves; floating point only for the pruning radii (with slack). */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

static int n; static long long *G, *lin, c0, bnd;
static double *R, *ctr; static long long *x; static long long count = 0;
static int mode = 0; static long long *levc, lev0; static long long mins[64]; static int nmins = 0; static int stopfirst = 1;

static void leaf(void) {
    long long v = c0;
    for (int i = 0; i < n; i++) {
        long long s = 0;
        for (int j = 0; j < n; j++) s += G[i * n + j] * x[j];
        v += x[i] * s + 2 * lin[i] * x[i];
    }
    if (v <= bnd && mode == 1) {
        long long lev = lev0;
        for (int i = 0; i < n; i++) lev += levc[i] * x[i];
        long long al = lev < 0 ? -lev : lev;
        if (al < nmins && v < mins[al]) {
            printf("%lld %lld\n", lev, v); fflush(stdout); count++;
            if (stopfirst) exit(0);
        }
        return;
    }
    if (v <= bnd) {
        int buf[64]; buf[0] = (int)v;
        for (int i = 0; i < n; i++) buf[i + 1] = (int)x[i];
        fwrite(buf, sizeof(int), n + 1, stdout); count++;
    }
}

static void rec(int k, double rem) {
    if (k < 0) { leaf(); return; }
    double s = 0;
    for (int l = k + 1; l < n; l++) s += R[k * n + l] * (x[l] - ctr[l]);
    double ck = ctr[k] - s / R[k * n + k];
    double r = sqrt(rem > 0 ? rem : 0) / R[k * n + k];
    long long lo = (long long)ceil(ck - r - 1e-7), hi = (long long)floor(ck + r + 1e-7);
    for (long long v = lo; v <= hi; v++) {
        x[k] = v;
        double y = R[k * n + k] * (v - ck);
        rec(k - 1, rem - y * y);
    }
    x[k] = 0;
}

int main(void) {
    if (scanf("%d", &n) != 1) return 1;
    G = malloc(sizeof(long long) * n * n); lin = malloc(sizeof(long long) * n);
    for (int i = 0; i < n * n; i++) scanf("%lld", &G[i]);
    for (int i = 0; i < n; i++) scanf("%lld", &lin[i]);
    scanf("%lld %lld", &c0, &bnd);
    if (scanf("%d", &mode) != 1) mode = 0;
    if (mode == 1) {
        levc = malloc(sizeof(long long) * n);
        for (int i = 0; i < n; i++) scanf("%lld", &levc[i]);
        scanf("%lld %d %d", &lev0, &nmins, &stopfirst);
        for (int i = 0; i < nmins; i++) scanf("%lld", &mins[i]);
    }
    /* centre = -G^{-1} lin, cmin = c0 - lin.G^{-1}lin ; Cholesky G = R^T R */
    double *Gf = malloc(sizeof(double) * n * n); R = calloc(n * n, sizeof(double));
    for (int i = 0; i < n * n; i++) Gf[i] = (double)G[i];
    for (int j = 0; j < n; j++) {
        double d = Gf[j * n + j];
        for (int k = 0; k < j; k++) d -= R[k * n + j] * R[k * n + j];
        if (d <= 0) { fprintf(stderr, "not PD\n"); return 2; }
        R[j * n + j] = sqrt(d);
        for (int i = j + 1; i < n; i++) {
            double s = Gf[j * n + i];
            for (int k = 0; k < j; k++) s -= R[k * n + j] * R[k * n + i];
            R[j * n + i] = s / R[j * n + j];
        }
    }
    /* solve G c = -lin via R^T y = -lin, R c = y */
    double *y = malloc(sizeof(double) * n); ctr = malloc(sizeof(double) * n);
    for (int i = 0; i < n; i++) {
        double s = -(double)lin[i];
        for (int k = 0; k < i; k++) s -= R[k * n + i] * y[k];
        y[i] = s / R[i * n + i];
    }
    for (int i = n - 1; i >= 0; i--) {
        double s = y[i];
        for (int k = i + 1; k < n; k++) s -= R[i * n + k] * ctr[k];
        ctr[i] = s / R[i * n + i];
    }
    double cmin = (double)c0;
    for (int i = 0; i < n; i++) cmin += (double)lin[i] * ctr[i];
    x = calloc(n, sizeof(long long));
    rec(n - 1, (double)bnd - cmin + 1e-6);
    fprintf(stderr, "solutions %lld\n", count);
    return 0;
}
