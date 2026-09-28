/* J1a type (v): exhaustive PSD test of every support configuration (a, groups, Q, P).
 * For each configuration the 15x15 matrices (positive representatives; star labels 0..11, V labels 12..14)
 *   Mo = 12I + 4G - RR^T          (= 28 P_{-4} restricted to U, must be PSD)
 *   Me = 6I - 2G - |R||R|^T + J    (= 14 P+_{-4} restricted, sigma-even, must be PSD; D_UU = 0 in J1a)
 *   Mc = 8I + 2G + |R||R|^T - J    (= 14 (I - P+) restricted, must be PSD)
 * are tested with a shifted Cholesky: fail at shift 1e-3 => lambda_min < -1e-3 (robust kill);
 * pass at 1e-3 but fail at 1e-9 => marginal kill (listed for an exact check); pass at 1e-9 => test passed.
 * Usage: j1av_psd run base.bin out_prefix nthreads
 *        j1av_psd check base.bin b q p1 p2   (prints the edge list and the verdicts of one configuration) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <omp.h>
#ifdef _WIN32
#include <windows.h>
#endif
#define N 15
typedef struct { signed char a[6]; signed char g[12]; } Base;
static int perms[720][6];
static int match6[15][3][2];
static int nperm = 0, nmatch = 0;

static void gen_perms(int *arr, int k) {
    if (k == 6) { memcpy(perms[nperm++], arr, 6 * sizeof(int)); return; }
    for (int i = k; i < 6; i++) {
        int t = arr[k]; arr[k] = arr[i]; arr[i] = t;
        gen_perms(arr, k + 1);
        t = arr[k]; arr[k] = arr[i]; arr[i] = t;
    }
}

static void gen_match(void) {
    /* perfect matchings of {0..5}: pair 0 with j, then one of the 3 matchings of the other four */
    for (int j = 1; j < 6; j++) {
        int rest[4], r = 0;
        for (int x = 1; x < 6; x++) if (x != j) rest[r++] = x;
        int pm[3][2][2] = {{{rest[0], rest[1]}, {rest[2], rest[3]}},
                           {{rest[0], rest[2]}, {rest[1], rest[3]}},
                           {{rest[0], rest[3]}, {rest[1], rest[2]}}};
        for (int t = 0; t < 3; t++) {
            match6[nmatch][0][0] = 0;           match6[nmatch][0][1] = j;
            match6[nmatch][1][0] = pm[t][0][0]; match6[nmatch][1][1] = pm[t][0][1];
            match6[nmatch][2][0] = pm[t][1][0]; match6[nmatch][2][1] = pm[t][1][1];
            nmatch++;
        }
    }
}

static int chol_ok(const double *A, double shift) {
    double L[N * N];
    for (int j = 0; j < N; j++) {
        double d = A[j * N + j] + shift;
        for (int k = 0; k < j; k++) d -= L[j * N + k] * L[j * N + k];
        if (!(d > 0)) return 0;
        double ljj = sqrt(d);
        L[j * N + j] = ljj;
        for (int i = j + 1; i < N; i++) {
            double s = A[i * N + j];
            for (int k = 0; k < j; k++) s -= L[i * N + k] * L[j * N + k];
            L[i * N + j] = s / ljj;
        }
    }
    return 1;
}

/* 0 = passed, 1 = robust kill, 2 = marginal kill */
static int test(const double *A) {
    if (!chol_ok(A, 1e-3)) return 1;
    if (!chol_ok(A, 1e-9)) return 2;
    return 0;
}

static void build_base(const Base *B, double *Mo, double *Me, double *Mc, int *Ap, int *Am) {
    double R[N][7];
    memset(R, 0, sizeof R);
    int np = 0, nm = 0;
    for (int K = 1; K <= 6; K++)
        for (int si = 0; si < 2; si++) {
            int L = 2 * (K - 1) + si;
            int s = si == 0 ? 1 : -1;
            int a = B->a[K - 1];
            R[L][0] = a; R[L][K] = a * s;
            if (a == 1) Ap[np++] = L; else Am[nm++] = L;
        }
    /* v1 = e1 - e2, v2 = e2 - e3, v3 = e3 - e1 */
    R[12][1] = 1; R[12][2] = -1; R[13][2] = 1; R[13][3] = -1; R[14][3] = 1; R[14][1] = -1;
    double G[N][N];
    memset(G, 0, sizeof G);
    for (int L = 0; L < 12; L++) { int w = 12 + B->g[L]; G[L][w] = G[w][L] = 1; }
    G[12][13] = G[13][12] = G[13][14] = G[14][13] = G[12][14] = G[14][12] = 1;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            double rr = 0, aa = 0;
            for (int c = 0; c < 7; c++) { rr += R[i][c] * R[j][c]; aa += fabs(R[i][c]) * fabs(R[j][c]); }
            double I = (i == j);
            Mo[i * N + j] = 12 * I + 4 * G[i][j] - rr;
            Me[i * N + j] = 6 * I - 2 * G[i][j] - aa + 1;
            Mc[i * N + j] = 8 * I + 2 * G[i][j] + aa - 1;
        }
}

static inline void add_edge(double *M, int x, int y, double w) { M[x * N + y] += w; M[y * N + x] += w; }

typedef struct { int b, q, p1, p2, kind; } Rec;  /* kind: 0 survivor; 11/12/13 marginal kill in odd/even/comp */

static int edges_of(const int *Ap, const int *Am, int q, int p1, int p2, int ex[12][2]) {
    int ne = 0;
    for (int i = 0; i < 6; i++) { ex[ne][0] = Ap[i]; ex[ne][1] = Am[perms[q][i]]; ne++; }
    for (int t = 0; t < 3; t++) { ex[ne][0] = Ap[match6[p1][t][0]]; ex[ne][1] = Ap[match6[p1][t][1]]; ne++; }
    for (int t = 0; t < 3; t++) { ex[ne][0] = Am[match6[p2][t][0]]; ex[ne][1] = Am[match6[p2][t][1]]; ne++; }
    return ne;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: run base.bin prefix nthreads | check base.bin b q p1 p2\n"); return 1; }
    int arr[6] = {0, 1, 2, 3, 4, 5};
    gen_perms(arr, 0);
    gen_match();
    if (nperm != 720 || nmatch != 15) { fprintf(stderr, "gen error %d %d\n", nperm, nmatch); return 1; }
    FILE *f = fopen(argv[2], "rb");
    if (!f) { fprintf(stderr, "cannot open %s\n", argv[2]); return 1; }
    int nb;
    if (fread(&nb, 4, 1, f) != 1) return 1;
    Base *bases = malloc(sizeof(Base) * nb);
    for (int i = 0; i < nb; i++)
        if (fread(bases[i].a, 1, 6, f) != 6 || fread(bases[i].g, 1, 12, f) != 12) return 1;
    fclose(f);

    if (strcmp(argv[1], "check") == 0) {
        int b = atoi(argv[3]), q = atoi(argv[4]), p1 = atoi(argv[5]), p2 = atoi(argv[6]);
        double Mo[N * N], Me[N * N], Mc[N * N];
        int Ap[6], Am[6], ex[12][2];
        build_base(&bases[b], Mo, Me, Mc, Ap, Am);
        printf("a");
        for (int k = 0; k < 6; k++) printf(" %d", bases[b].a[k]);
        printf(" | g");
        for (int k = 0; k < 12; k++) printf(" %d", bases[b].g[k]);
        printf(" | edges");
        edges_of(Ap, Am, q, p1, p2, ex);
        for (int e = 0; e < 12; e++) {
            printf(" %d-%d", ex[e][0], ex[e][1]);
            add_edge(Mo, ex[e][0], ex[e][1], 4); add_edge(Me, ex[e][0], ex[e][1], -2); add_edge(Mc, ex[e][0], ex[e][1], 2);
        }
        printf(" | odd %d even %d comp %d\n", test(Mo), test(Me), test(Mc));
        return 0;
    }

    char *prefix = argv[3];
    int nth = atoi(argv[4]);
#ifdef _WIN32
    SetPriorityClass(GetCurrentProcess(), BELOW_NORMAL_PRIORITY_CLASS);
#endif
    omp_set_num_threads(nth);
    long long cnt[8] = {0};  /* total, odd robust, odd marg, even robust, even marg, comp robust, comp marg, survivors */
    Rec *all = NULL;
    long long nall = 0, capall = 0, done = 0;
    double t0 = omp_get_wtime();
    #pragma omp parallel
    {
        long long c[8] = {0};
        Rec *loc = NULL;
        long long nloc = 0, caploc = 0;
        #pragma omp for schedule(dynamic, 4)
        for (int b = 0; b < nb; b++) {
            double Mo0[N * N], Me0[N * N], Mc0[N * N];
            int Ap[6], Am[6];
            build_base(&bases[b], Mo0, Me0, Mc0, Ap, Am);
            for (int q = 0; q < 720; q++) {
                double MoQ[N * N];
                memcpy(MoQ, Mo0, sizeof MoQ);
                for (int i = 0; i < 6; i++) add_edge(MoQ, Ap[i], Am[perms[q][i]], 4);
                for (int p1 = 0; p1 < 15; p1++) {
                    double MoP[N * N];
                    memcpy(MoP, MoQ, sizeof MoP);
                    for (int t = 0; t < 3; t++) add_edge(MoP, Ap[match6[p1][t][0]], Ap[match6[p1][t][1]], 4);
                    for (int p2 = 0; p2 < 15; p2++) {
                        double Mo[N * N];
                        memcpy(Mo, MoP, sizeof Mo);
                        for (int t = 0; t < 3; t++) add_edge(Mo, Am[match6[p2][t][0]], Am[match6[p2][t][1]], 4);
                        c[0]++;
                        int r = test(Mo), kind = -1;
                        if (r == 1) { c[1]++; continue; }
                        if (r == 2) { c[2]++; kind = 11; }
                        else {
                            double Me[N * N], Mc[N * N];
                            int ex[12][2];
                            memcpy(Me, Me0, sizeof Me);
                            memcpy(Mc, Mc0, sizeof Mc);
                            edges_of(Ap, Am, q, p1, p2, ex);
                            for (int e = 0; e < 12; e++) { add_edge(Me, ex[e][0], ex[e][1], -2); add_edge(Mc, ex[e][0], ex[e][1], 2); }
                            int r2 = test(Me);
                            if (r2 == 1) { c[3]++; continue; }
                            if (r2 == 2) { c[4]++; kind = 12; }
                            else {
                                int r3 = test(Mc);
                                if (r3 == 1) { c[5]++; continue; }
                                if (r3 == 2) { c[6]++; kind = 13; }
                                else { c[7]++; kind = 0; }
                            }
                        }
                        if (nloc == caploc) { caploc = caploc ? 2 * caploc : 1024; loc = realloc(loc, caploc * sizeof(Rec)); }
                        loc[nloc].b = b; loc[nloc].q = q; loc[nloc].p1 = p1; loc[nloc].p2 = p2; loc[nloc].kind = kind;
                        nloc++;
                    }
                }
            }
            long long dn;
            #pragma omp atomic capture
            dn = ++done;
            if (dn % 500 == 0) {
                double el = omp_get_wtime() - t0;
                fprintf(stderr, "progress %lld/%d bases, %.0f s elapsed, eta %.0f s\n", dn, nb, el, el / dn * (nb - dn));
            }
        }
        #pragma omp critical
        {
            for (int k = 0; k < 8; k++) cnt[k] += c[k];
            if (nloc) {
                if (nall + nloc > capall) { capall = (nall + nloc) * 2; all = realloc(all, capall * sizeof(Rec)); }
                memcpy(all + nall, loc, nloc * sizeof(Rec));
                nall += nloc;
            }
            free(loc);
        }
    }
    double el = omp_get_wtime() - t0;
    printf("J1a(v) exhaustive PSD run: %lld configurations in %.1f s with %d threads\n", cnt[0], el, nth);
    printf("  odd robust kills   %lld\n  odd marginal kills %lld\n  even robust kills  %lld\n  even marginal      %lld\n"
           "  comp robust kills  %lld\n  comp marginal      %lld\n  SURVIVORS (pass all three) %lld\n",
           cnt[1], cnt[2], cnt[3], cnt[4], cnt[5], cnt[6], cnt[7]);
    char fn[512];
    snprintf(fn, sizeof fn, "%s_records.txt", prefix);
    FILE *o = fopen(fn, "w");
    for (long long i = 0; i < nall; i++) fprintf(o, "%d %d %d %d %d\n", all[i].b, all[i].q, all[i].p1, all[i].p2, all[i].kind);
    fclose(o);
    printf("records (survivors + marginal kills): %lld -> %s\n", nall, fn);
    return 0;
}
