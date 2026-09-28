/* fp_short.c (C1, 28/09 night): the Fincke-Pohst recursion of rank17_ypairs.short_vectors_chunked, compiled.
   Same floating-point operations in the same order (compile with -ffp-contract=off), same output order (the recursion
   order), same filter (x != 0, first non-zero coordinate positive). Input file: int32 n, double bound, double d[n],
   double Q[n][n] (the Python Cholesky data). Output file: int32 count, then count rows of n int8.
   Usage: fp_short <in> <out> */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

static int n;
static double d[64], Q[64][64];
static int x[64];
static const double eps = 1e-7;
static FILE *fo;
static long long cnt = 0;
static int8_t row[64];

static void emit(void) {
    int f = -1;
    for (int i = 0; i < n; i++) if (x[i]) { f = i; break; }
    if (f < 0 || x[f] < 0) return;
    for (int i = 0; i < n; i++) {
        if (x[i] > 127 || x[i] < -128) { fprintf(stderr, "coordinate out of int8 range\n"); exit(3); }
        row[i] = (int8_t)x[i];
    }
    fwrite(row, 1, n, fo);
    cnt++;
}

static void rec(int k, double rem) {
    double s_ = 0.0;
    for (int j = k + 1; j < n; j++) if (x[j]) s_ += Q[k][j] * (double)x[j];
    double c = -s_;
    double r0 = rem > 0.0 ? rem : 0.0;
    double sp = sqrt(r0 / d[k]) + eps;
    int lo = (int)ceil(c - sp), hi = (int)floor(c + sp);
    double dk = d[k];
    for (int xi = lo; xi <= hi; xi++) {
        double t = (double)xi - c;
        double r2 = rem - dk * t * t;
        if (r2 < -eps) continue;
        x[k] = xi;
        if (k == 0) emit();
        else rec(k - 1, r2);
    }
    x[k] = 0;
}

int main(int argc, char **argv) {
    if (argc < 3) return 1;
    FILE *fi = fopen(argv[1], "rb");
    int32_t nn; double bound;
    if (!fi || fread(&nn, 4, 1, fi) != 1 || fread(&bound, 8, 1, fi) != 1) return 2;
    n = nn;
    if (n > 64) return 2;
    if (fread(d, 8, n, fi) != (size_t)n) return 2;
    for (int i = 0; i < n; i++) if (fread(Q[i], 8, n, fi) != (size_t)n) return 2;
    fclose(fi);
    fo = fopen(argv[2], "wb");
    int32_t z = 0;
    fwrite(&z, 4, 1, fo);
    rec(n - 1, bound + eps);
    fseek(fo, 0, SEEK_SET);
    int32_t c32 = (int32_t)cnt;
    fwrite(&c32, 4, 1, fo);
    fclose(fo);
    return 0;
}
