/* rank17_z4.c (C1, 28/09 night): rank-17 pass 2 for one (V, y-pair), compiled.
   1. Exhaustive skeleton enumeration: port of rank17_skeleton.skeleton_exists(orbits=H-orbits, masks=None): 6-sets of
      usable classes (kmax-0 duals applied), pairwise odd, sums usable, independent, parity energy of the kmax 1/2 duals,
      unit rule; the first class is an H-orbit minimum (H = <reflections in the roots of K>, verdict-neutral).
   2. Per skeleton, the 21 cell signature sets Sigma_X (port of rank17_engine.Case.domains: in-class pairs with
      (w, w') in {0, +-4}, all 8 sign/order variants, M1 p(a) = eps_c, refined L1, sign normalisation of a_12, b_12, b_1d);
      sigma(q+) = ((s(w+), g_e))_e with s(q) = ((q - q mod 2) mod 4) / 2 (checked equal to sigma(q-) under M1).
   3. The exact mod-4 test (port of z4g.z4_test): rows M_d = phi(b_d), M_c[d] + M_d[c] = (b_c, b_d)/2,
      phi(d_1d) = M_d in Sigma_1d, phi(d_cd) = M_c + M_d + kappa_cd in Sigma_cd.
   Verdict per skeleton: EMPTY (some Sigma_X is empty), Z4 (mod-4 relaxation infeasible), SURVIVOR (goes to the full solver).
   Input: rank17_z4export.py file.  Usage: rank17_z4 <file> [run [survivor file] | list N | count | skel <file>]
   Env: Z4_PMIN (partial mod-4 test from this many chosen classes, default 3; 7 = off), Z4_CANON (H-canonical enumeration,
   default 1), Z4_SDEPTH, Z4_NSCH (stabilizer chain depth, Schreier generators), Z4_KEEP, Z4_FP (validation helpers).
   Build: gcc -O2 -march=native -o rank17_z4.exe rank17_z4.c  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define MAXB 24
static int nB, n, nd, nu;
static int Gv[MAXB][MAXB], GVK[MAXB][15];
static int KM[32];
static int *U, *orbmin, *Fm, *FK, *FU, *gvm;
static int cidx[1 << 15];

typedef struct {
    int m;
    int8_t *w;
    int *fsp, *fsm;
    int *voff, *fv;
    int np;
    int *pi, *pj, *fh1, *fh2;
    int8_t *s1, *s2;
} CD;
static CD *cd;

static int ngen0 = 0;
static int **gen0;

static FILE *fin;
static void rd(void *p, size_t sz, size_t k) {
    if (fread(p, sz, k, fin) != k) { fprintf(stderr, "read error\n"); exit(2); }
}
static int rdi(void) { int32_t x; rd(&x, 4, 1); return x; }

static int fmask(const int *h) {                       /* 15-bit functional (h G_V K_V^T) mod 2 */
    int f = 0;
    for (int k = 0; k < 15; k++) {
        long s = 0;
        for (int a = 0; a < nB; a++) s += (long)h[a] * GVK[a][k];
        if (s & 1) f |= 1 << k;
    }
    return f;
}
static int sgn1(const int *h) {
    for (int a = 0; a < nB; a++) if (h[a]) return h[a] > 0 ? 1 : -1;
    return 1;
}

static void load(const char *path) {
    fin = fopen(path, "rb");
    if (!fin) { fprintf(stderr, "cannot open %s\n", path); exit(2); }
    if (rdi() != 0x5A344B31) { fprintf(stderr, "bad magic\n"); exit(2); }
    nB = rdi(); n = rdi(); nd = rdi(); nu = rdi();
    for (int a = 0; a < nB; a++) for (int b = 0; b < nB; b++) Gv[a][b] = rdi();
    for (int a = 0; a < nB; a++) for (int k = 0; k < 15; k++) GVK[a][k] = rdi();
    for (int t = 0; t < nd; t++) KM[t] = rdi();
    U = malloc(n * sizeof(int)); orbmin = malloc(n * sizeof(int)); Fm = malloc(n * sizeof(int));
    FK = malloc(n * sizeof(int)); FU = malloc(n * sizeof(int)); gvm = malloc(n * sizeof(int));
    for (int x = 0; x < (1 << 15); x++) cidx[x] = -1;
    for (int i = 0; i < n; i++) {
        U[i] = rdi(); orbmin[i] = rdi(); Fm[i] = rdi(); FK[i] = rdi(); FU[i] = rdi(); gvm[i] = rdi();
        cidx[U[i]] = i;
    }
    cd = calloc(n, sizeof(CD));
    long totpairs = 0;
    int *wg = malloc(sizeof(int) * 4096 * MAXB);
    for (int i = 0; i < n; i++) {
        int C = rdi(), m = rdi();
        if (C != U[i]) { fprintf(stderr, "class order mismatch\n"); exit(2); }
        CD *c = &cd[i];
        c->m = m;
        c->w = malloc((size_t)m * nB + 1);
        rd(c->w, 1, (size_t)m * nB);
        c->fsp = malloc(sizeof(int) * (m + 1)); c->fsm = malloc(sizeof(int) * (m + 1));
        c->voff = malloc(sizeof(int) * (m + 1));
        int cap = 4 * m + 16, used = 0;
        c->fv = malloc(sizeof(int) * cap);
        for (int k = 0; k < m; k++) {
            c->fsp[k] = rdi(); c->fsm[k] = rdi();
            int nv = rdi();
            if (used + nv > cap) { cap = 2 * (used + nv) + 16; c->fv = realloc(c->fv, sizeof(int) * cap); }
            c->voff[k] = used;
            for (int t = 0; t < nv; t++) c->fv[used++] = rdi();
        }
        c->voff[m] = used;
        /* in-class pairs */
        if (m > 4096) { fprintf(stderr, "class too large %d\n", m); exit(2); }
        for (int k = 0; k < m; k++)
            for (int b = 0; b < nB; b++) {
                int s = 0;
                for (int a = 0; a < nB; a++) s += c->w[k * nB + a] * Gv[a][b];
                wg[k * MAXB + b] = s;
            }
        int pc = 16; c->np = 0;
        c->pi = malloc(sizeof(int) * pc); c->pj = malloc(sizeof(int) * pc);
        c->fh1 = malloc(sizeof(int) * pc); c->fh2 = malloc(sizeof(int) * pc);
        c->s1 = malloc(pc); c->s2 = malloc(pc);
        for (int a = 0; a < m; a++)
            for (int b2 = a + 1; b2 < m; b2++) {
                int ip = 0;
                for (int t = 0; t < nB; t++) ip += wg[a * MAXB + t] * c->w[b2 * nB + t];
                if (ip != 0 && ip != 4 && ip != -4) continue;
                if (c->np == pc) {
                    pc *= 2;
                    c->pi = realloc(c->pi, sizeof(int) * pc); c->pj = realloc(c->pj, sizeof(int) * pc);
                    c->fh1 = realloc(c->fh1, sizeof(int) * pc); c->fh2 = realloc(c->fh2, sizeof(int) * pc);
                    c->s1 = realloc(c->s1, pc); c->s2 = realloc(c->s2, pc);
                }
                int h1[MAXB], h2[MAXB];
                for (int t = 0; t < nB; t++) {
                    int x = c->w[a * nB + t], y = c->w[b2 * nB + t];
                    if ((x + y) & 1) { fprintf(stderr, "pair not in one class\n"); exit(2); }
                    h1[t] = (x + y) / 2; h2[t] = (x - y) / 2;
                }
                c->pi[c->np] = a; c->pj[c->np] = b2;
                c->fh1[c->np] = fmask(h1); c->fh2[c->np] = fmask(h2);
                c->s1[c->np] = (int8_t)sgn1(h1); c->s2[c->np] = (int8_t)sgn1(h2);
                c->np++;
            }
        totpairs += c->np;
    }
    free(wg);
    /* trailer: generators of H on the class indices */
    ngen0 = rdi();
    gen0 = malloc(sizeof(int *) * (ngen0 + 1));
    for (int k = 0; k < ngen0; k++) {
        gen0[k] = malloc(sizeof(int) * n);
        rd(gen0[k], 4, n);
        for (int x = 0; x < n; x++) if (gen0[k][x] < 0 || gen0[k][x] >= n) { fprintf(stderr, "bad generator\n"); exit(2); }
    }
    fclose(fin);
    fprintf(stderr, "loaded: classes %d, duals %d, units %d, in-class pairs %ld\n", n, nd, nu, totpairs);
}

/* ---------------- per skeleton ---------------- */
static int g[6];
static int Tlo[256], Thi[128];
static inline int pat(int f) { return Tlo[f & 255] ^ Thi[f >> 8]; }
static int CELLc[21], CELLd[21], cellidx[8][8];
static uint64_t SIG[21];
static int J[6][6], KAP[6][6], Mrow[6];
static long long zsol;
static int zcount_all = 0;
static long long mismatch = 0;
static unsigned char *badbuf;

static int ipmask(int a, int b) {
    int s = 0;
    for (int i = 0; i < nB; i++) if ((a >> i) & 1)
        for (int j = 0; j < nB; j++) if ((b >> j) & 1) s += Gv[i][j];
    return s;
}

/* KB = number of known skeleton classes (6 at a leaf; 3..5 in the partial test): patterns have KB bits, M1 and the
   signatures are read on those bits, refined L1 (which needs full patterns) only when KB = 6. With KB < 6 every Sigma is
   a superset of the projection of the true Sigma, so the partial mod-4 test is a necessary condition. */
static int KB = 6, ZK = 6;
static int weak_norm = 0;       /* 1: cell (1,2) normalised like the other star-1 cells (b only), for the edge test */
static void build_tables(int kb) {
    for (int x = 0; x < 256; x++) {
        int v = 0;
        for (int e = 0; e < kb; e++) v |= (__builtin_popcount(x & g[e] & 255) & 1) << e;
        Tlo[x] = v;
    }
    for (int x = 0; x < 128; x++) {
        int v = 0;
        for (int e = 0; e < kb; e++) v |= (__builtin_popcount((x << 8) & g[e]) & 1) << e;
        Thi[x] = v;
    }
}

static uint64_t cell_sigma(int X) {
    int c = CELLc[X], d = CELLd[X];
    int gam = (c == 1) ? g[d - 2] : (g[c - 2] ^ g[d - 2]);
    int ci = cidx[gam];
    if (ci < 0) { fprintf(stderr, "cell class not usable %d\n", gam); exit(3); }
    CD *C = &cd[ci];
    int full = (1 << KB) - 1;
    int ec = (c == 1) ? full : (1 << (c - 2)), ed = 1 << (d - 2);
    if (KB == 6) {
        uint64_t forb = 0;
        int q4[4] = {0, ec, ed, ec ^ ed};
        for (int t = 0; t < 4; t++) { forb |= 1ULL << q4[t]; forb |= 1ULL << (63 ^ q4[t]); }
        for (int k = 0; k < C->m; k++) {
            unsigned char b = 0;
            for (int t = C->voff[k]; t < C->voff[k + 1]; t++) if ((forb >> pat(C->fv[t])) & 1) { b = 1; break; }
            badbuf[k] = b;
        }
    } else
        memset(badbuf, 0, C->m);
    uint64_t S = 0;
    int star12 = (c == 1 && d == 2 && !weak_norm), star1 = (c == 1);
    for (int p = 0; p < C->np; p++) {
        int i = C->pi[p], j = C->pj[p];
        if (badbuf[i] || badbuf[j]) continue;
        int ph1 = pat(C->fh1[p]), ph2 = pat(C->fh2[p]);
        int s1 = C->s1[p], s2 = C->s2[p];
        for (int t = 0; t < 2; t++) {
            if (t == 0 && ph1 != ec) continue;
            if (t == 1 && ph2 != ec) continue;
            for (int sp = 1; sp >= -1; sp -= 2) {
                for (int ord = 0; ord < 2; ord++) {
                    /* variant: t = 0 (A = +-h1): ord 0: (sp w_i, sp w_j), ord 1: (sp w_j, sp w_i)
                                t = 1 (A = +-h2): ord 0: (sp w_i, -sp w_j), ord 1: (-sp w_j, sp w_i) */
                    int fpA, fpB, fsplus, fsminus;
                    if (t == 0) {
                        fpA = sp * s1 > 0;
                        fpB = (ord == 0) ? (sp * s2 > 0) : (-sp * s2 > 0);
                        if (ord == 0) { fsplus = sp > 0 ? C->fsp[i] : C->fsm[i]; fsminus = sp > 0 ? C->fsp[j] : C->fsm[j]; }
                        else { fsplus = sp > 0 ? C->fsp[j] : C->fsm[j]; fsminus = sp > 0 ? C->fsp[i] : C->fsm[i]; }
                    } else {
                        fpA = sp * s2 > 0;
                        fpB = (ord == 0) ? (sp * s1 > 0) : (-sp * s1 > 0);
                        if (ord == 0) { fsplus = sp > 0 ? C->fsp[i] : C->fsm[i]; fsminus = sp > 0 ? C->fsm[j] : C->fsp[j]; }
                        else { fsplus = sp > 0 ? C->fsm[j] : C->fsp[j]; fsminus = sp > 0 ? C->fsp[i] : C->fsm[i]; }
                    }
                    if (star12 && !(fpA && fpB)) continue;
                    if (star1 && !star12 && !fpB) continue;
                    int sig = pat(fsplus);
                    if ((pat(fsminus) ^ ed) != sig) mismatch++;
                    S |= 1ULL << sig;
                }
            }
        }
    }
    return S;
}

static int z4rec(int k) {
    if (k == ZK) { zsol++; return !zcount_all; }
    uint64_t S = SIG[cellidx[1][k + 2]];
    while (S) {
        int m = __builtin_ctzll(S); S &= S - 1;
        int ok = 1;
        for (int e = 0; e < k; e++) if ((((m >> e) & 1) ^ ((Mrow[e] >> k) & 1)) != J[k][e]) { ok = 0; break; }
        if (!ok) continue;
        for (int e = 0; e < k; e++) {
            int v = Mrow[e] ^ m ^ KAP[e][k];
            if (!((SIG[cellidx[e + 2][k + 2]] >> v) & 1)) { ok = 0; break; }
        }
        if (!ok) continue;
        Mrow[k] = m;
        if (z4rec(k + 1)) return 1;
    }
    return 0;
}

/* ---------------- enumeration ---------------- */
static int nw;
static uint64_t *nbr, *candbuf;
static long long nodes, leaves, n_empty, n_z4, n_surv, empty_by_cell[21];
static int chosen[6], span[64], nspan;
static int mode = 0;            /* 0 run, 1 list, 2 count */
static long long list_n = 0;
static int stopflag = 0;
static FILE *fsurv;
static const char *skelfile = 0;

static clock_t tstart;
static int topi = -1;
static long long pruned[7], tested[7], selftest_bad = 0;
static int PMIN = 3;            /* partial mod-4 test when >= PMIN classes are chosen (7 = off) */

static void build_JK(int kc) {
    for (int c = 0; c < kc; c++) {
        int gc = gvm[chosen[c]];
        int dd = 2 + ipmask(gc, gc);
        if (((dd % 4) + 4) % 4 != 0) { fprintf(stderr, "residue not doubly even\n"); exit(3); }
        for (int e = 0; e < kc; e++) if (e != c) {
            int tot = 1 + ipmask(gc, gvm[chosen[e]]);
            if (tot % 2) { fprintf(stderr, "residue not self-orthogonal\n"); exit(3); }
            J[c][e] = (((tot / 2) % 2) + 2) % 2;
        }
    }
    for (int c = 0; c < kc; c++) for (int d = c + 1; d < kc; d++) {
        int x = gvm[chosen[c]] & gvm[chosen[d]], v = 0;
        for (int e = 0; e < kc; e++) {
            int par = ((ipmask(x, gvm[chosen[e]]) % 2) + 2) % 2;
            v |= ((1 + par) & 1) << e;
        }
        KAP[c][d] = v;
    }
}

/* necessary condition on kc chosen classes: the mod-4 test restricted to the cells among labels 1..kc+1, read on kc bits */
static int partial_ok(int kc) {
    for (int e = 0; e < kc; e++) g[e] = U[chosen[e]];
    KB = kc; ZK = kc;
    build_tables(kc);
    for (int X = 0; X < 21; X++) {
        if (CELLd[X] > kc + 1) continue;
        SIG[X] = cell_sigma(X);
        if (!SIG[X]) { KB = ZK = 6; return 0; }
    }
    build_JK(kc);
    zsol = 0; zcount_all = 0;
    z4rec(0);
    KB = ZK = 6;
    return zsol > 0;
}

/* edge test: two classes x = U_i, y = U_j (i < j) that sit in one skeleton get labels c < d; the cells (1,c), (1,d), (c,d)
   read on the bits of g_c, g_d, with the rows M_c, M_d restricted to those bits, must pass the mod-4 test. This is the
   partial test for labels 2, 3 with the weaker sign normalisation (b only on (1,2)), valid whatever the labels are. */
static int edge_ok(int i, int j) {
    chosen[0] = i; chosen[1] = j;
    weak_norm = 1;
    int r = partial_ok(2);
    weak_norm = 0;
    return r;
}

static const char *fpfile = 0;
static unsigned long long *fps = 0;
static long long nfp = 0, capfp = 0;
static int *orb0 = 0;
static int cmpull(const void *a, const void *b) {
    unsigned long long x = *(const unsigned long long *)a, y = *(const unsigned long long *)b;
    return x < y ? -1 : x > y;
}

static void leaf(void) {
    leaves++;
    if ((leaves & ((1 << 20) - 1)) == 0) {
        fprintf(stderr, "progress %.0fs top %d/%d leaves %lld empty %lld z4 %lld surv %lld nodes %lld\n",
                (double)(clock() - tstart) / CLOCKS_PER_SEC, topi, n, leaves, n_empty, n_z4, n_surv, nodes);
        fflush(stderr);
    }
    for (int e = 0; e < 6; e++) g[e] = U[chosen[e]];
    if (mode == 2) {
        if (fpfile) {                                      /* H-invariant fingerprint of the set (validation) */
            long long a6[6], a15[15], a20[20]; int t = 0;
            for (int e = 0; e < 6; e++) a6[e] = orb0[chosen[e]];
            for (int e = 0; e < 6; e++) for (int f2 = e + 1; f2 < 6; f2++) {
                long long p = orb0[chosen[e]], q = orb0[chosen[f2]];
                int si = cidx[U[chosen[e]] ^ U[chosen[f2]]];
                long long r = si >= 0 ? orb0[si] : -1;
                a15[t++] = ((p < q ? p : q) << 28) | ((p < q ? q : p) << 14) | (r + 1);
            }
            t = 0;
            for (int e = 0; e < 6; e++) for (int f2 = e + 1; f2 < 6; f2++) for (int h = f2 + 1; h < 6; h++) {
                int si = cidx[U[chosen[e]] ^ U[chosen[f2]] ^ U[chosen[h]]];
                a20[t++] = si >= 0 ? orb0[si] : -1;
            }
            #define SORTLL(arr, len) for (int u1 = 1; u1 < len; u1++) for (int u2 = u1; u2 > 0 && arr[u2 - 1] > arr[u2]; u2--) { long long tt = arr[u2]; arr[u2] = arr[u2 - 1]; arr[u2 - 1] = tt; }
            SORTLL(a6, 6) SORTLL(a15, 15) SORTLL(a20, 20)
            unsigned long long hsh = 1469598103934665603ULL;
            for (int e = 0; e < 6; e++) { hsh ^= (unsigned long long)a6[e]; hsh *= 1099511628211ULL; }
            for (int e = 0; e < 15; e++) { hsh ^= (unsigned long long)a15[e]; hsh *= 1099511628211ULL; }
            for (int e = 0; e < 20; e++) { hsh ^= (unsigned long long)(a20[e] + 7); hsh *= 1099511628211ULL; }
            if (nfp == capfp) { capfp = capfp ? 2 * capfp : 1 << 20; fps = realloc(fps, sizeof(unsigned long long) * capfp); }
            fps[nfp++] = hsh;
        }
        return;
    }
    KB = ZK = 6;
    build_tables(6);
    int firstempty = -1;
    for (int X = 0; X < 21; X++) {
        SIG[X] = cell_sigma(X);
        if (!SIG[X] && firstempty < 0) { firstempty = X; if (mode == 0) break; }
    }
    const char *verdict;
    if (firstempty >= 0) {
        n_empty++; empty_by_cell[firstempty]++; verdict = "EMPTY";
    } else {
        build_JK(6);
        zsol = 0;
        zcount_all = (mode == 1);
        z4rec(0);
        if (zsol == 0) { n_z4++; verdict = "Z4"; }
        else {
            n_surv++; verdict = "SURVIVOR";
            if (fsurv) {
                fprintf(fsurv, "%d %d %d %d %d %d\n", g[0], g[1], g[2], g[3], g[4], g[5]);
                fflush(fsurv);
            }
        }
    }
    if (mode == 1) {
        printf("SK %d %d %d %d %d %d |", g[0], g[1], g[2], g[3], g[4], g[5]);
        for (int X = 0; X < 21; X++) printf(" %llx", (unsigned long long)SIG[X]);
        printf(" | %s %lld\n", verdict, zsol);
        if (leaves >= list_n) stopflag = 1;
    }
}

static clock_t tlastp = 0;
static void rec(int depth, const uint64_t *cand, const int *o, const int *ou) {
    nodes++;
    if ((nodes & 0x3FF) == 0 && clock() - tlastp > 20 * CLOCKS_PER_SEC) {
        tlastp = clock();
        fprintf(stderr, "progress %.0fs top %d/%d leaves %lld empty %lld z4 %lld surv %lld nodes %lld tested %lld %lld %lld pruned %lld %lld %lld\n",
                (double)(clock() - tstart) / CLOCKS_PER_SEC, topi, n, leaves, n_empty, n_z4, n_surv, nodes,
                tested[3], tested[4], tested[5], pruned[3], pruned[4], pruned[5]);
        fflush(stderr);
    }
    int need = 5 - depth;
    for (int wi = 0; wi < nw && !stopflag; wi++) {
        uint64_t c = cand[wi];
        while (c) {
            int b = __builtin_ctzll(c); c &= c - 1;
            int i = wi * 64 + b;
            int x = U[i], in = 0;
            for (int s = 0; s < nspan; s++) if (span[s] == x) { in = 1; break; }
            if (in) continue;
            if (depth == 0 && !orbmin[i]) continue;
            if (depth == 0) topi = i;
            int o2[32], bad = 0;
            for (int t = 0; t < nd; t++) {
                int oo = o[t] + ((FK[i] >> t) & 1), zz = depth + 1 - oo;
                o2[t] = oo;
                if (KM[t] == 1) { if (oo > 1 && zz > 0) { bad = 1; break; } }
                else { if (oo > 2 && zz > 1) { bad = 1; break; } }
            }
            if (bad) continue;
            int ou2[32];
            for (int t = 0; t < nu; t++) ou2[t] = ou[t] + ((FU[i] >> t) & 1);
            if (depth + 1 == 6) {
                int okk = 1;
                for (int t = 0; t < nu; t++) if (ou2[t] < 1) { okk = 0; break; }
                if (!okk) continue;
                chosen[5] = i;
                leaf();
                if (stopflag) return;
                continue;
            }
            uint64_t *c2 = candbuf + (size_t)(depth + 1) * nw;
            const uint64_t *nb = nbr + (size_t)i * nw;
            int cnt = 0;
            for (int k = 0; k < nw; k++) { c2[k] = cand[k] & nb[k]; cnt += __builtin_popcountll(c2[k]); }
            if (cnt < need) continue;
            chosen[depth] = i;
            if (depth + 1 >= PMIN && mode != 2) {
                tested[depth + 1]++;
                if (!partial_ok(depth + 1)) { pruned[depth + 1]++; continue; }
            }
            int old = nspan;
            for (int s = 0; s < old; s++) span[old + s] = span[s] ^ x;
            nspan = 2 * old;
            rec(depth + 1, c2, o2, ou2);
            nspan = old;
            if (stopflag) return;
        }
    }
}

/* ---------------- canonical enumeration under H (pointwise stabilizer chain) ----------------
   Level j (x_1..x_j chosen) carries a group G_j <= H fixing x_1..x_j pointwise (G_0 = H); G_{j+1} is generated by random
   Schreier generators of Stab_{G_j}(x_{j+1}) (a subgroup of it: the chain stays descending, the reduction stays valid);
   orbit ids orb_j = orbit minimum. A set S is enumerated as (x_1, ..., x_6), x_{j+1} = the minimum of S - {x_1..x_j} in
   the order (orb_j, index), and x_{j+1} must be a G_j-orbit minimum. Every H-orbit of skeletons has such a set: apply
   elements of G_0, G_1, ... level by level (each fixes the earlier x's and preserves the earlier orbit ids).
   Levels >= SDEPTH use the trivial group. Labels: x_1 -> 2, ..., x_6 -> 7 (any labelling is valid: S_6 symmetry). */
#define MAXGEN 64
static uint64_t *nbrs;
static int *orbl[7];
static int **genl[7];
static int ngenl[7];
static int *genbuf[7][MAXGEN];
static int *genptr[7][MAXGEN];
static int SDEPTH = 4, NSCHREIER = 24;
static uint64_t *candl;
static int *bfs_par, *bfs_gen, *bfs_q, *tA, *tB, *tC, *tD;
static unsigned rngs = 12345u;
static unsigned rnd32(void) { rngs = rngs * 1664525u + 1013904223u; return rngs >> 8; }
static long long orbit_calls = 0, schreier_made = 0;

static void orbits_of(int **gens, int ng, int *orb) {
    for (int x = 0; x < n; x++) orb[x] = -1;
    for (int s = 0; s < n; s++) {
        if (orb[s] >= 0) continue;
        int qh = 0, qt = 0;
        bfs_q[qt++] = s; orb[s] = s;
        while (qh < qt) {
            int x = bfs_q[qh++];
            for (int k = 0; k < ng; k++) {
                int y = gens[k][x];
                if (orb[y] < 0) { orb[y] = s; bfs_q[qt++] = y; }
            }
        }
    }
    orbit_calls++;
}

/* t_p (maps y -> p) from the Schreier vector of the BFS rooted at y */
static void transversal(int p, int **gens, int *out) {
    int path[4096], len = 0;
    while (bfs_par[p] != -1) {
        if (len >= 4096) { fprintf(stderr, "transversal path too long\n"); exit(3); }
        path[len++] = bfs_gen[p]; p = bfs_par[p];
    }
    for (int x = 0; x < n; x++) out[x] = x;
    for (int t = len - 1; t >= 0; t--) {
        int *g = gens[path[t]];
        for (int x = 0; x < n; x++) out[x] = g[out[x]];
    }
}

/* generators of (a subgroup of) Stab_{G_j}(y) into level j + 1, and its orbits */
static void stabilizer(int j, int y) {
    int **gs = genl[j], ng = ngenl[j];
    for (int x = 0; x < n; x++) bfs_par[x] = -2;
    int qh = 0, qt = 0;
    bfs_q[qt++] = y; bfs_par[y] = -1; bfs_gen[y] = -1;
    while (qh < qt) {
        int x = bfs_q[qh++];
        for (int k = 0; k < ng; k++) {
            int z = gs[k][x];
            if (bfs_par[z] == -2) { bfs_par[z] = x; bfs_gen[z] = k; bfs_q[qt++] = z; }
        }
    }
    int osz = qt;
    if (osz == 1) {                                        /* G_j fixes y: same group */
        genl[j + 1] = gs; ngenl[j + 1] = ng;
        memcpy(orbl[j + 1], orbl[j], sizeof(int) * n);
        return;
    }
    int *orbitpts = malloc(sizeof(int) * osz);
    memcpy(orbitpts, bfs_q, sizeof(int) * osz);
    int made = 0;
    for (int tries = 0; tries < 4 * NSCHREIER && made < NSCHREIER && made < MAXGEN; tries++) {
        int p = orbitpts[rnd32() % osz], k = rnd32() % ng;
        int sp = gs[k][p];
        transversal(p, gs, tA);                            /* tA: y -> p */
        transversal(sp, gs, tC);                           /* tC: y -> s(p) */
        for (int x = 0; x < n; x++) tD[tC[x]] = x;         /* tD = tC^-1 */
        int *out = genbuf[j + 1][made];
        int ident = 1;
        for (int x = 0; x < n; x++) { out[x] = tD[gs[k][tA[x]]]; if (out[x] != x) ident = 0; }
        if (out[y] != y) { fprintf(stderr, "Schreier generator does not fix the point\n"); exit(3); }
        if (!ident) made++;
    }
    free(orbitpts);
    genl[j + 1] = genptr[j + 1];
    for (int m = 0; m < made; m++) genptr[j + 1][m] = genbuf[j + 1][m];
    ngenl[j + 1] = made;
    schreier_made += made;
    orbits_of(genl[j + 1], made, orbl[j + 1]);
}

static void trivial_level(int L) {
    ngenl[L] = 0;
    for (int x = 0; x < n; x++) orbl[L][x] = x;
}

static void rec2(int j, const int *o, const int *ou) {
    nodes++;
    if ((nodes & 0x3FF) == 0 && clock() - tlastp > 20 * CLOCKS_PER_SEC) {
        tlastp = clock();
        fprintf(stderr, "progress %.0fs top %d/%d leaves %lld empty %lld z4 %lld surv %lld nodes %lld tested %lld %lld %lld pruned %lld %lld %lld\n",
                (double)(clock() - tstart) / CLOCKS_PER_SEC, topi, n, leaves, n_empty, n_z4, n_surv, nodes,
                tested[3], tested[4], tested[5], pruned[3], pruned[4], pruned[5]);
        fflush(stderr);
    }
    int need = 5 - j;
    const uint64_t *cand = candl + (size_t)j * nw;
    const int *orb = orbl[j];
    for (int wi = 0; wi < nw && !stopflag; wi++) {
        uint64_t c = cand[wi];
        while (c) {
            int b = __builtin_ctzll(c); c &= c - 1;
            int i = wi * 64 + b;
            if (orb[i] != i) continue;
            if (j == 0) topi = i;
            int x = U[i], in = 0;
            for (int s = 0; s < nspan; s++) if (span[s] == x) { in = 1; break; }
            if (in) continue;
            int o2[32], bad = 0;
            for (int t = 0; t < nd; t++) {
                int oo = o[t] + ((FK[i] >> t) & 1), zz = j + 1 - oo;
                o2[t] = oo;
                if (KM[t] == 1) { if (oo > 1 && zz > 0) { bad = 1; break; } }
                else { if (oo > 2 && zz > 1) { bad = 1; break; } }
            }
            if (bad) continue;
            int ou2[32];
            for (int t = 0; t < nu; t++) ou2[t] = ou[t] + ((FU[i] >> t) & 1);
            if (j + 1 == 6) {
                int okk = 1;
                for (int t = 0; t < nu; t++) if (ou2[t] < 1) { okk = 0; break; }
                if (!okk) continue;
                chosen[5] = i;
                leaf();
                if (stopflag) return;
                continue;
            }
            uint64_t *c2 = candl + (size_t)(j + 1) * nw;
            const uint64_t *nb = nbrs + (size_t)i * nw;
            int cnt = 0;
            for (int k = 0; k < nw; k++) {
                uint64_t w = cand[k] & nb[k], ww = w;
                while (ww) {
                    int bb = __builtin_ctzll(ww); ww &= ww - 1;
                    int z = k * 64 + bb;
                    if (orb[z] < i || (orb[z] == i && z <= i)) w &= ~(1ULL << bb);
                }
                c2[k] = w; cnt += __builtin_popcountll(w);
            }
            if (cnt < need) continue;
            chosen[j] = i;
            if (j + 1 >= PMIN) {
                tested[j + 1]++;
                if (!partial_ok(j + 1)) { pruned[j + 1]++; continue; }
            }
            if (j + 1 < SDEPTH) stabilizer(j, i); else trivial_level(j + 1);
            int old = nspan;
            for (int s = 0; s < old; s++) span[old + s] = span[s] ^ x;
            nspan = 2 * old;
            rec2(j + 1, o2, ou2);
            nspan = old;
            if (stopflag) return;
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: rank17_z4 <file> [run|list N|count] [survivor file]\n"); return 1; }
    if (argc > 2 && !strcmp(argv[2], "list")) { mode = 1; list_n = argc > 3 ? atoll(argv[3]) : 50; }
    if (argc > 2 && !strcmp(argv[2], "count")) mode = 2;
    if (argc > 3 && !strcmp(argv[2], "skel")) skelfile = argv[3];
    if (mode == 0 && !skelfile && argc > 3 && !strcmp(argv[2], "run")) fsurv = fopen(argv[3], "w");
    const char *pm = getenv("Z4_PMIN");
    if (pm) PMIN = atoi(pm);
    if (mode == 1) PMIN = 7;                       /* list mode: the plain enumeration (compared with Python) */
    clock_t t0 = clock();
    tstart = t0;
    load(argv[1]);
    int X = 0;
    for (int c = 1; c <= 7; c++) for (int d = c + 1; d <= 7; d++) { CELLc[X] = c; CELLd[X] = d; cellidx[c][d] = X; X++; }
    int maxm = 1;
    for (int i = 0; i < n; i++) if (cd[i].m > maxm) maxm = cd[i].m;
    badbuf = malloc(maxm + 1);
    nw = (n + 63) / 64;
    nbr = calloc((size_t)n * nw, sizeof(uint64_t));
    candbuf = calloc((size_t)7 * nw, sizeof(uint64_t));
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {
            if (!(__builtin_popcount(Fm[i] & U[j]) & 1)) continue;
            if (cidx[U[i] ^ U[j]] < 0) continue;
            nbr[(size_t)i * nw + j / 64] |= 1ULL << (j % 64);
        }
    const char *ev = getenv("Z4_EDGE");
    int use_edge = (ev ? atoi(ev) : 0) && mode != 1 && !skelfile;
    long long edges = 0, edges_cut = 0;
    for (int i = 0; i < n; i++)
        for (int wi = 0; wi < nw; wi++) {
            uint64_t c = nbr[(size_t)i * nw + wi];
            while (c) {
                int b = __builtin_ctzll(c); c &= c - 1;
                int j = wi * 64 + b;
                edges++;
                if (use_edge && !edge_ok(i, j)) {
                    nbr[(size_t)i * nw + wi] &= ~(1ULL << b);
                    edges_cut++;
                }
            }
        }
    fprintf(stderr, "edges %lld, cut by the edge test %lld (%s)\n", edges, edges_cut, use_edge ? "on" : "off");
    double tl = (double)(clock() - t0) / CLOCKS_PER_SEC;
    uint64_t *all = calloc(nw, sizeof(uint64_t));
    for (int i = 0; i < n; i++) all[i / 64] |= 1ULL << (i % 64);
    /* validation helpers: level-0 orbits, fingerprints, restriction to a union of H-orbits (Z4_KEEP = orbit ranks) */
    fpfile = getenv("Z4_FP");
    if (!bfs_q) bfs_q = malloc(sizeof(int) * n);
    orb0 = malloc(sizeof(int) * n);
    orbits_of(gen0, ngen0, orb0);
    const char *keep = getenv("Z4_KEEP");
    if (keep) {
        int rankof[1 << 13], nr = 0;
        for (int i = 0; i < n; i++) if (orb0[i] == i) rankof[nr++] = i;
        char *ks = strdup(keep), *tok = strtok(ks, ",");
        uint64_t *keepm = calloc(nw, sizeof(uint64_t));
        long long kept = 0;
        while (tok) {
            int r = atoi(tok);
            if (r >= 0 && r < nr)
                for (int i = 0; i < n; i++) if (orb0[i] == rankof[r]) { keepm[i / 64] |= 1ULL << (i % 64); kept++; }
            tok = strtok(0, ",");
        }
        for (int k = 0; k < nw; k++) all[k] &= keepm[k];
        fprintf(stderr, "restricted to %lld classes (%d orbits in all)\n", kept, nr);
    }
    int o0[32] = {0}, ou0[32] = {0};
    span[0] = 0; nspan = 1;
    const char *cv = getenv("Z4_CANON");
    int canon = (cv ? atoi(cv) : 1) && mode != 1 && !skelfile;
    if (getenv("Z4_SDEPTH")) SDEPTH = atoi(getenv("Z4_SDEPTH"));
    if (getenv("Z4_NSCH")) NSCHREIER = atoi(getenv("Z4_NSCH"));
    if (canon) {
        nbrs = calloc((size_t)n * nw, sizeof(uint64_t));
        for (int i = 0; i < n; i++)
            for (int wi = 0; wi < nw; wi++) {
                uint64_t c = nbr[(size_t)i * nw + wi];
                while (c) {
                    int b = __builtin_ctzll(c); c &= c - 1;
                    int j = wi * 64 + b;
                    nbrs[(size_t)i * nw + wi] |= 1ULL << b;
                    nbrs[(size_t)j * nw + i / 64] |= 1ULL << (i % 64);
                }
            }
        for (int L = 0; L < 7; L++) orbl[L] = malloc(sizeof(int) * n);
        for (int L = 1; L < 7; L++) for (int m = 0; m < MAXGEN; m++) genbuf[L][m] = malloc(sizeof(int) * n);
        bfs_par = malloc(sizeof(int) * n); bfs_gen = malloc(sizeof(int) * n); bfs_q = malloc(sizeof(int) * n);
        tA = malloc(sizeof(int) * n); tB = malloc(sizeof(int) * n); tC = malloc(sizeof(int) * n); tD = malloc(sizeof(int) * n);
        candl = calloc((size_t)7 * nw, sizeof(uint64_t));
        genl[0] = gen0; ngenl[0] = ngen0;
        orbits_of(gen0, ngen0, orbl[0]);
        long long mism = 0;
        for (int i = 0; i < n; i++) if ((orbl[0][i] == i) != (orbmin[i] != 0)) mism++;
        if (mism) { fprintf(stderr, "H orbit minima disagree with the export (%lld)\n", mism); return 5; }
        memcpy(candl, all, sizeof(uint64_t) * nw);
        fprintf(stderr, "canonical enumeration: H generators %d, SDEPTH %d, Schreier gens %d\n", ngen0, SDEPTH, NSCHREIER);
    }
    if (skelfile) {                                /* mode 3: given skeletons (6 classes per line), list output */
        FILE *fs = fopen(skelfile, "r");
        int a[6];
        mode = 1; list_n = 1LL << 60;
        while (fs && fscanf(fs, "%d %d %d %d %d %d", &a[0], &a[1], &a[2], &a[3], &a[4], &a[5]) == 6) {
            for (int e = 0; e < 6; e++) {
                chosen[e] = cidx[a[e]];
                if (chosen[e] < 0) { fprintf(stderr, "skeleton class not usable\n"); return 3; }
            }
            leaf();
            /* self-test of the partial test: the k-bit projection of every full Sigma_X (X among labels 1..k+1) must lie in
               the partial Sigma_X, for k = 3, 4, 5 */
            uint64_t full[21];
            memcpy(full, SIG, sizeof(full));
            for (int k = 3; k <= 5; k++) {
                for (int e = 0; e < k; e++) g[e] = U[chosen[e]];
                KB = ZK = k;
                build_tables(k);
                for (int X2 = 0; X2 < 21; X2++) {
                    if (CELLd[X2] > k + 1) continue;
                    uint64_t P = cell_sigma(X2), F = full[X2];
                    while (F) {
                        int s = __builtin_ctzll(F); F &= F - 1;
                        if (!((P >> (s & ((1 << k) - 1))) & 1)) selftest_bad++;
                    }
                }
                KB = ZK = 6;
            }
        }
        if (fs) fclose(fs);
        fprintf(stderr, "partial-test self-check violations: %lld\n", selftest_bad);
    } else if (canon)
        rec2(0, o0, ou0);
    else
        rec(0, all, o0, ou0);
    if (fpfile) {
        qsort(fps, nfp, sizeof(unsigned long long), cmpull);
        long long u = 0;
        for (long long k = 0; k < nfp; k++) if (k == 0 || fps[k] != fps[k - 1]) fps[u++] = fps[k];
        FILE *ff = fopen(fpfile, "w");
        for (long long k = 0; k < u; k++) fprintf(ff, "%016llx\n", fps[k]);
        fclose(ff);
        fprintf(stderr, "fingerprints: %lld leaves, %lld distinct\n", nfp, u);
    }
    double ts = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("{\"skeletons\": %lld, \"empty\": %lld, \"z4_killed\": %lld, \"survivors\": %lld, \"nodes\": %lld, "
           "\"sigma_mismatch\": %lld, \"complete\": %s, \"load_s\": %.1f, \"s\": %.1f, \"empty_by_cell\": [",
           leaves, n_empty, n_z4, n_surv, nodes, mismatch, stopflag ? "false" : "true", tl, ts);
    for (int k = 0; k < 21; k++) printf("%lld%s", empty_by_cell[k], k < 20 ? ", " : "");
    printf("], \"pmin\": %d, \"partial_tested\": [%lld, %lld, %lld], \"partial_pruned\": [%lld, %lld, %lld]}\n", PMIN,
           tested[3], tested[4], tested[5], pruned[3], pruned[4], pruned[5]);
    if (fsurv) fclose(fsurv);
    return mismatch ? 4 : 0;
}
