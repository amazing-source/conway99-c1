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
#include <math.h>

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
    uint16_t *pi, *pj, *fh1, *fh2;         /* compact: class size <= 4096, functionals are 15-bit */
    int8_t *s1, *s2;
    int *wgv;                              /* w G_V per vector (integer phi test) */
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
        c->wgv = malloc(sizeof(int) * ((size_t)m * nB + 1));
        for (int k = 0; k < m; k++)
            for (int b = 0; b < nB; b++) {
                int s = 0;
                for (int a = 0; a < nB; a++) s += c->w[k * nB + a] * Gv[a][b];
                wg[k * MAXB + b] = s;
                c->wgv[k * nB + b] = s;
            }
        int pc = 16; c->np = 0;
        c->pi = malloc(sizeof(uint16_t) * pc); c->pj = malloc(sizeof(uint16_t) * pc);
        c->fh1 = malloc(sizeof(uint16_t) * pc); c->fh2 = malloc(sizeof(uint16_t) * pc);
        c->s1 = malloc(pc); c->s2 = malloc(pc);
        for (int a = 0; a < m; a++)
            for (int b2 = a + 1; b2 < m; b2++) {
                int ip = 0;
                for (int t = 0; t < nB; t++) ip += wg[a * MAXB + t] * c->w[b2 * nB + t];
                if (ip != 0 && ip != 4 && ip != -4) continue;
                if (c->np == pc) {
                    pc *= 2;
                    c->pi = realloc(c->pi, sizeof(uint16_t) * pc); c->pj = realloc(c->pj, sizeof(uint16_t) * pc);
                    c->fh1 = realloc(c->fh1, sizeof(uint16_t) * pc); c->fh2 = realloc(c->fh2, sizeof(uint16_t) * pc);
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
        if (c->np) {                                       /* trim the doubling slack (memory) */
            c->pi = realloc(c->pi, sizeof(uint16_t) * c->np); c->pj = realloc(c->pj, sizeof(uint16_t) * c->np);
            c->fh1 = realloc(c->fh1, sizeof(uint16_t) * c->np); c->fh2 = realloc(c->fh2, sizeof(uint16_t) * c->np);
            c->s1 = realloc(c->s1, c->np); c->s2 = realloc(c->s2, c->np);
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

/* entries recorded at a leaf for the integer phi test: (w+, w-) = (s+ w_vp, s- w_vm) in the cell's class, signature */
typedef struct { uint16_t vp, vm; int8_t sp, sm; uint8_t sig; } IEnt;
static IEnt *ients[21];
static int nient[21], capient[21];
static CD *cellcd[21];
static int record_entries = 0;
static void push_ient(int X, int vp, int sp, int vm, int sm, int sig) {
    if (nient[X] == capient[X]) {
        capient[X] = capient[X] ? 2 * capient[X] : 256;
        ients[X] = realloc(ients[X], sizeof(IEnt) * capient[X]);
    }
    IEnt *e = &ients[X][nient[X]++];
    e->vp = (uint16_t)vp; e->vm = (uint16_t)vm; e->sp = (int8_t)sp; e->sm = (int8_t)sm; e->sig = (uint8_t)sig;
}

static uint64_t cell_sigma(int X) {
    int c = CELLc[X], d = CELLd[X];
    int gam = (c == 1) ? g[d - 2] : (g[c - 2] ^ g[d - 2]);
    int ci = cidx[gam];
    if (ci < 0) { fprintf(stderr, "cell class not usable %d\n", gam); exit(3); }
    CD *C = &cd[ci];
    if (record_entries) { nient[X] = 0; cellcd[X] = C; }
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
                    if (record_entries) {                  /* (w+, w-) as (vector index, sign) pairs, and sigma */
                        int vp, vm, sgp, sgm;
                        if (t == 0) { if (ord == 0) { vp = i; vm = j; } else { vp = j; vm = i; } sgp = sgm = sp; }
                        else if (ord == 0) { vp = i; sgp = sp; vm = j; sgm = -sp; }
                        else { vp = j; sgp = -sp; vm = i; sgm = sp; }
                        push_ient(X, vp, sgp, vm, sgm, sig);
                    }
                }
            }
        }
    }
    return S;
}

/* ---- integer phi test (Z4_INTPHI=1): at a mod-4-feasible leaf, redo the phi search with, for every cell X determined by
   the rows chosen so far, the restricted domain R_X = {recorded entries with signature phi(d_X)} (every entry of a frame
   lies in the one self-dual code, so its signature is phi(d_X)), and forward checking under the integer rule
   (w_X^s, w_Y^t) + r_X^s . r_Y^t in {0, +-4}. A phi that dies has no frame; a skeleton all of whose phi die is excluded. */
static int INTPHI = 0;
static int *rdom[8][21], rlen[8][21], rcap[21];
static int detd[21];
static long long iphi_nodes = 0, iphi_alive = 0, n_int_killed = 0, n_int_surv = 0;
static inline int rr_dot(int X, int s, int Y, int t) {
    int c = CELLc[X], d = CELLd[X], c2 = CELLc[Y], d2 = CELLd[Y];
    return (c == c2) + (c == d2) * t + (d == c2) * s + (d == d2) * s * t;
}
static inline int wdot(const CD *A, int ia, const CD *B, int ib) {
    const int *x = A->wgv + ia * nB; const int8_t *y = B->w + ib * nB;
    int s = 0;
    for (int k = 0; k < nB; k++) s += x[k] * y[k];
    return s;
}
static inline int ok4(int v) { return !(v & 3) && v <= 4 && v >= -4; }
static int ent_compat(int X, const IEnt *e, int Y, const IEnt *f) {
    const CD *A = cellcd[X], *B = cellcd[Y];
    if (!ok4(e->sp * f->sp * wdot(A, e->vp, B, f->vp) + rr_dot(X, 1, Y, 1))) return 0;
    if (!ok4(e->sp * f->sm * wdot(A, e->vp, B, f->vm) + rr_dot(X, 1, Y, -1))) return 0;
    if (!ok4(e->sm * f->sp * wdot(A, e->vm, B, f->vp) + rr_dot(X, -1, Y, 1))) return 0;
    if (!ok4(e->sm * f->sm * wdot(A, e->vm, B, f->vm) + rr_dot(X, -1, Y, -1))) return 0;
    return 1;
}
/* keep the entries of X (level L list) that have a compatible entry in Y; returns the new length */
static int fc_filter(int L, int X, int Y) {
    int n0 = rlen[L][X], out = 0;
    for (int a = 0; a < n0; a++) {
        const IEnt *e = &ients[X][rdom[L][X][a]];
        int ok = 0;
        for (int b = 0; b < rlen[L][Y] && !ok; b++) ok = ent_compat(X, e, Y, &ients[Y][rdom[L][Y][b]]);
        if (ok) rdom[L][X][out++] = rdom[L][X][a];
    }
    rlen[L][X] = out;
    return out;
}
static int intphi_rec(int k) {
    iphi_nodes++;
    if (k == 6) { iphi_alive++; return 1; }
    uint64_t S = SIG[cellidx[1][k + 2]];
    while (S) {
        int m = __builtin_ctzll(S); S &= S - 1;
        int ok = 1;
        for (int e = 0; e < k; e++) if ((((m >> e) & 1) ^ ((Mrow[e] >> k) & 1)) != J[k][e]) { ok = 0; break; }
        if (!ok) continue;
        int tgt[8], newc[8], nn = 0;
        newc[nn] = cellidx[1][k + 2]; tgt[nn++] = m;
        for (int e = 0; e < k; e++) {
            int v = Mrow[e] ^ m ^ KAP[e][k];
            if (!((SIG[cellidx[e + 2][k + 2]] >> v) & 1)) { ok = 0; break; }
            newc[nn] = cellidx[e + 2][k + 2]; tgt[nn++] = v;
        }
        if (!ok) continue;
        /* level k+1 domains: copy the determined ones, build the new ones */
        for (int X = 0; X < 21; X++) if (detd[X]) {
            rlen[k + 1][X] = rlen[k][X];
            memcpy(rdom[k + 1][X], rdom[k][X], sizeof(int) * rlen[k][X]);
        }
        for (int q = 0; q < nn; q++) {
            int X = newc[q]; rlen[k + 1][X] = 0;
            for (int a = 0; a < nient[X]; a++) if (ients[X][a].sig == tgt[q]) rdom[k + 1][X][rlen[k + 1][X]++] = a;
            if (!rlen[k + 1][X]) ok = 0;
        }
        if (!ok) continue;
        for (int q = 0; q < nn; q++) detd[newc[q]] = 1;
        /* forward checking: new cells against every determined cell, then the old ones against the new ones */
        for (int q = 0; q < nn && ok; q++)
            for (int Y = 0; Y < 21 && ok; Y++)
                if (detd[Y] && Y != newc[q] && !fc_filter(k + 1, newc[q], Y)) ok = 0;
        for (int Y = 0; Y < 21 && ok; Y++) {
            int isnew = 0;
            for (int q = 0; q < nn; q++) if (newc[q] == Y) isnew = 1;
            if (!detd[Y] || isnew) continue;
            for (int q = 0; q < nn && ok; q++) if (!fc_filter(k + 1, Y, newc[q])) ok = 0;
        }
        if (ok) {
            Mrow[k] = m;
            if (intphi_rec(k + 1)) { for (int q = 0; q < nn; q++) detd[newc[q]] = 0; return 1; }
        }
        for (int q = 0; q < nn; q++) detd[newc[q]] = 0;
    }
    return 0;
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
static long long fail_empty[7], fail_z4[7];
static int partial_ok(int kc) {
    for (int e = 0; e < kc; e++) g[e] = U[chosen[e]];
    KB = kc; ZK = kc;
    build_tables(kc);
    for (int pass = 0; pass < 2; pass++)                  /* the cells of the newest label first: early exit */
        for (int X = 0; X < 21; X++) {
            if (CELLd[X] > kc + 1 || (CELLd[X] == kc + 1) != (pass == 0)) continue;
            SIG[X] = cell_sigma(X);
            if (!SIG[X]) { KB = ZK = 6; fail_empty[kc]++; return 0; }
        }
    build_JK(kc);
    zsol = 0; zcount_all = 0;
    z4rec(0);
    KB = ZK = 6;
    if (!zsol) fail_z4[kc]++;
    return zsol > 0;
}

/* ---- incremental partial test (same verdicts as partial_ok): per level L (L chosen classes, labels 2..L+1) and active
   cell X (d <= L+1), the list of cell entries passing the sign normalisation and M1 on the L known bits, stored as
   (f_a, f_s(w+)). An old cell's list at level L is its level-(L-1) list filtered by the new bit (eps_c has bit L-1 = 1 for
   c = 1 and 0 otherwise, since c - 2 < L - 1); a new cell (d = L+1) is built from its class. */
typedef struct { uint16_t fA, fs; } Ent;
static Ent *arena[7];
static long long arcap[7], arlen[7], cst[7][21], cln[7][21];
static int INC = 1;
/* S7 base rule (valid): relabelling the base vertex is a symmetry, the 21 cell classes are the differences of the 7-point
   set {0, g_2..g_7}. Take a difference of minimal H-orbit id, make one of its endpoints the base, then canonicalise:
   x_1 has that orbit id and is its orbit minimum, so every cell class is >= x_1 in the order (H-orbit id, index). */
static int BASE = 0;                                                    /* off until validated */
static int FP7 = 0;
static int STAB2 = 1;
static int LEAFPRE = 1;
static long long leaf_pre_killed = 0;
static inline void push_ent(int L, int fA, int fs) {
    if (arlen[L] == arcap[L]) {
        arcap[L] = arcap[L] ? 2 * arcap[L] : (1 << 16);
        arena[L] = realloc(arena[L], sizeof(Ent) * arcap[L]);
    }
    arena[L][arlen[L]].fA = (uint16_t)fA; arena[L][arlen[L]].fs = (uint16_t)fs; arlen[L]++;
}

static void cell_full_list(int L, int X) {
    int c = CELLc[X], d = CELLd[X];
    int gam = (c == 1) ? g[d - 2] : (g[c - 2] ^ g[d - 2]);
    CD *C = &cd[cidx[gam]];
    int full = (1 << L) - 1, ec = (c == 1) ? full : (1 << (c - 2));
    int star12 = (c == 1 && d == 2), star1 = (c == 1);
    cst[L][X] = arlen[L];
    for (int p = 0; p < C->np; p++) {
        int i = C->pi[p], j = C->pj[p];
        int ph1 = pat(C->fh1[p]), ph2 = pat(C->fh2[p]);
        int s1 = C->s1[p], s2 = C->s2[p];
        for (int t = 0; t < 2; t++) {
            if (t == 0 && ph1 != ec) continue;
            if (t == 1 && ph2 != ec) continue;
            int fA = t == 0 ? C->fh1[p] : C->fh2[p];
            for (int sp = 1; sp >= -1; sp -= 2)
                for (int ord = 0; ord < 2; ord++) {
                    int fpA, fpB, fsplus;
                    if (t == 0) {
                        fpA = sp * s1 > 0;
                        fpB = (ord == 0) ? (sp * s2 > 0) : (-sp * s2 > 0);
                        fsplus = (ord == 0) ? (sp > 0 ? C->fsp[i] : C->fsm[i]) : (sp > 0 ? C->fsp[j] : C->fsm[j]);
                    } else {
                        fpA = sp * s2 > 0;
                        fpB = (ord == 0) ? (sp * s1 > 0) : (-sp * s1 > 0);
                        fsplus = (ord == 0) ? (sp > 0 ? C->fsp[i] : C->fsm[i]) : (sp > 0 ? C->fsm[j] : C->fsp[j]);
                    }
                    if (star12 && !(fpA && fpB)) continue;
                    if (star1 && !star12 && !fpB) continue;
                    push_ent(L, fA, fsplus);
                }
        }
    }
    cln[L][X] = arlen[L] - cst[L][X];
}

static void cell_filter_list(int L, int X) {
    int ebit = (CELLc[X] == 1) ? 1 : 0, gnew = g[L - 1];
    cst[L][X] = arlen[L];
    Ent *src = arena[L - 1] + cst[L - 1][X];
    long long n0 = cln[L - 1][X];
    for (long long k = 0; k < n0; k++) {
        Ent e = src[k];                                    /* copy: push_ent may move arena[L], never arena[L-1] */
        if ((__builtin_popcount(e.fA & gnew) & 1) == ebit) push_ent(L, e.fA, e.fs);
    }
    cln[L][X] = arlen[L] - cst[L][X];
}

/* level L lists (chosen[0..L-1] set); returns 0 if the partial test at L fails (only tested when L >= PMIN) */
static int inc_level(int L, int test) {
    for (int e = 0; e < L; e++) g[e] = U[chosen[e]];
    KB = L; ZK = L;
    build_tables(L);
    arlen[L] = 0;
    int anyempty = 0;
    for (int X = 0; X < 21; X++) {                        /* all active lists are built (the next level reads them) */
        if (CELLd[X] > L + 1) continue;
        if (CELLd[X] == L + 1) cell_full_list(L, X); else cell_filter_list(L, X);
        if (!cln[L][X]) { anyempty = 1; if (test) break; }
    }
    if (!test) { KB = ZK = 6; return 1; }
    if (anyempty) { KB = ZK = 6; fail_empty[L]++; return 0; }
    for (int X = 0; X < 21; X++) {
        if (CELLd[X] > L + 1) continue;
        uint64_t S = 0;
        Ent *a = arena[L] + cst[L][X];
        for (long long k = 0; k < cln[L][X]; k++) S |= 1ULL << pat(a[k].fs);
        SIG[X] = S;
    }
    build_JK(L);
    zsol = 0; zcount_all = 0;
    z4rec(0);
    KB = ZK = 6;
    if (!zsol) fail_z4[L]++;
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
static unsigned long long *fpset = 0;                  /* open addressing, 2^22 slots: distinct fingerprints only */
static void fp_add(unsigned long long h) {
    if (!fpset) fpset = calloc(1 << 22, sizeof(unsigned long long));
    if (!h) h = 1;
    unsigned long long k = h & ((1 << 22) - 1);
    while (fpset[k] && fpset[k] != h) k = (k + 1) & ((1 << 22) - 1);
    if (!fpset[k]) {
        fpset[k] = h;
        if (nfp == capfp) { capfp = capfp ? 2 * capfp : 1 << 16; fps = realloc(fps, sizeof(unsigned long long) * capfp); }
        fps[nfp++] = h;
        if (nfp > (1 << 21)) { fprintf(stderr, "too many distinct fingerprints\n"); exit(6); }
    }
}
static int cmpull(const void *a, const void *b) {
    unsigned long long x = *(const unsigned long long *)a, y = *(const unsigned long long *)b;
    return x < y ? -1 : x > y;
}

static long long maxleaves = 0, maxsurv = 0;                        /* Z4_MAXLEAVES: stop after this many (diagnostics; incomplete) */
static void leaf(void) {
    leaves++;
    if (maxleaves && leaves >= maxleaves) stopflag = 1;
    if ((leaves & ((1 << 20) - 1)) == 0) {
        fprintf(stderr, "progress %.0fs top %d/%d leaves %lld empty %lld z4 %lld surv %lld nodes %lld\n",
                (double)(clock() - tstart) / CLOCKS_PER_SEC, topi, n, leaves, n_empty, n_z4, n_surv, nodes);
        fflush(stderr);
    }
    for (int e = 0; e < 6; e++) g[e] = U[chosen[e]];
    if (mode == 2) {
        if (fpfile && FP7) {                               /* S7 x H invariant: the 7-point set {0, g_2..g_7} */
            int P[7]; P[0] = 0;
            for (int e = 0; e < 6; e++) P[e + 1] = U[chosen[e]];
            long long od[7][7], a21[21], a35[35]; int t = 0;
            for (int a = 0; a < 7; a++) for (int b2 = a + 1; b2 < 7; b2++) {
                int si = cidx[P[a] ^ P[b2]];
                od[a][b2] = od[b2][a] = si >= 0 ? orb0[si] : -1;
                a21[t++] = od[a][b2];
            }
            t = 0;
            for (int a = 0; a < 7; a++) for (int b2 = a + 1; b2 < 7; b2++) for (int h = b2 + 1; h < 7; h++) {
                long long x = od[a][b2] + 1, y = od[a][h] + 1, z = od[b2][h] + 1, tt;
                if (x > y) { tt = x; x = y; y = tt; }
                if (y > z) { tt = y; y = z; z = tt; }
                if (x > y) { tt = x; x = y; y = tt; }
                a35[t++] = (x << 28) | (y << 14) | z;
            }
            #define SORTL2(arr, len) for (int u1 = 1; u1 < len; u1++) for (int u2 = u1; u2 > 0 && arr[u2 - 1] > arr[u2]; u2--) { long long tt2 = arr[u2]; arr[u2] = arr[u2 - 1]; arr[u2 - 1] = tt2; }
            SORTL2(a21, 21) SORTL2(a35, 35)
            unsigned long long hsh = 1469598103934665603ULL;
            for (int e = 0; e < 21; e++) { hsh ^= (unsigned long long)(a21[e] + 3); hsh *= 1099511628211ULL; }
            for (int e = 0; e < 35; e++) { hsh ^= (unsigned long long)a35[e]; hsh *= 1099511628211ULL; }
            fp_add(hsh);
        } else if (fpfile) {                               /* H-invariant fingerprint of the set (validation) */
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
            fp_add(hsh);
        }
        return;
    }
    KB = ZK = 6;
    build_tables(6);
    int firstempty = -1;
    record_entries = INTPHI;
    for (int X = 0; X < 21; X++) {
        SIG[X] = cell_sigma(X);
        if (!SIG[X] && firstempty < 0) { firstempty = X; if (mode == 0) break; }
    }
    record_entries = 0;
    const char *verdict;
    if (firstempty >= 0) {
        n_empty++; empty_by_cell[firstempty]++; verdict = "EMPTY";
    } else {
        build_JK(6);
        zsol = 0;
        zcount_all = (mode == 1);
        z4rec(0);
        int intkilled = 0;
        if (zsol > 0 && INTPHI) {                          /* integer phi test on the mod-4 survivor */
            for (int X = 0; X < 21; X++) {
                if (rcap[X] < nient[X] + 1) {
                    rcap[X] = nient[X] + 1;
                    for (int L = 0; L < 8; L++) rdom[L][X] = realloc(rdom[L][X], sizeof(int) * rcap[X]);
                }
                detd[X] = 0;
            }
            int r = intphi_rec(0);
            if (!r) { intkilled = 1; n_int_killed++; }
            else n_int_surv++;
        }
        if (zsol == 0) { n_z4++; verdict = "Z4"; }
        else if (intkilled) { verdict = "INT"; }
        else {
            n_surv++; verdict = "SURVIVOR";
            if (maxsurv && n_surv >= maxsurv) stopflag = 1;
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
static int SDEPTH = 6, NSCHREIER = 24;
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

/* stabilizer restricted to candidates (same group chain, cheaper): Cand_j (the level-j candidate bitset) is G_j-invariant
   (it is cut out by adjacency to fixed points and by the (orbit id, index) order of earlier levels, all preserved), so the
   generators of G_j are only needed on Cand_j. G_{j+1}'s Schreier generators are evaluated on Cand_{j+1} only, through the
   transversal words (inverse generators for t^-1), and its orbits are computed on Cand_{j+1}. */
static int **invl[7];
static int *invbuf[7][MAXGEN];
static int *invptr[7][MAXGEN];
static int *inv0buf[MAXGEN * 4];
static int *clist, *pathbuf;
static long long stab2_calls = 0;

static void stabilizer2(int j, int y) {
    int **gs = genl[j], **gi = invl[j], ng = ngenl[j];
    const uint64_t *cj = candl + (size_t)j * nw, *cj1 = candl + (size_t)(j + 1) * nw;
    /* orbit of y under G_j (inside Cand_j), Schreier vector */
    int qh = 0, qt = 0;
    bfs_q[qt++] = y; bfs_par[y] = -1; bfs_gen[y] = -1;
    tB[y] = 1;                                              /* tB: visited mark for this BFS */
    while (qh < qt) {
        int x = bfs_q[qh++];
        for (int k = 0; k < ng; k++) {
            int z = gs[k][x];
            if (!tB[z]) { tB[z] = 1; bfs_par[z] = x; bfs_gen[z] = k; bfs_q[qt++] = z; }
        }
    }
    int osz = qt;
    for (int t = 0; t < osz; t++) tB[bfs_q[t]] = 0;
    /* the list of Cand_{j+1} points */
    int nc = 0;
    for (int k = 0; k < nw; k++) {
        uint64_t c = cj1[k];
        while (c) { int b = __builtin_ctzll(c); c &= c - 1; clist[nc++] = k * 64 + b; }
    }
    (void)cj;
    if (osz == 1) {                                         /* G_j fixes y: G_{j+1} = G_j */
        genl[j + 1] = gs; invl[j + 1] = gi; ngenl[j + 1] = ng;
        for (int t = 0; t < nc; t++) orbl[j + 1][clist[t]] = orbl[j][clist[t]];
        stab2_calls++;
        return;
    }
    int *orbitpts = malloc(sizeof(int) * osz);
    memcpy(orbitpts, bfs_q, sizeof(int) * osz);
    int made = 0;
    for (int tries = 0; tries < 4 * NSCHREIER && made < NSCHREIER && made < MAXGEN; tries++) {
        int p = orbitpts[rnd32() % osz], k = rnd32() % ng;
        int sp = gs[k][p];
        /* words: t_p = path(p), t_sp = path(sp) (generator indices from y outwards) */
        int lp = 0, x = p;
        while (bfs_par[x] != -1) { pathbuf[lp++] = bfs_gen[x]; x = bfs_par[x]; }
        int *wp = pathbuf;                                  /* reversed: wp[lp-1] is applied first */
        int ls = 0; x = sp;
        int *ws = pathbuf + 4096;
        while (bfs_par[x] != -1) { ws[ls++] = bfs_gen[x]; x = bfs_par[x]; }
        if (lp >= 4096 || ls >= 4096) { fprintf(stderr, "path too long\n"); exit(3); }
        int *out = genbuf[j + 1][made];
        int ident = 1;
        for (int t = 0; t < nc; t++) {
            int z = clist[t], v = z;
            for (int q = lp - 1; q >= 0; q--) v = gs[wp[q]][v];            /* t_p(z) */
            v = gs[k][v];                                                  /* s(t_p(z)) */
            for (int q = 0; q < ls; q++) v = gi[ws[q]][v];                 /* t_sp^-1: inverses in reverse order */
            out[z] = v;
            if (v != z) ident = 0;
        }
        if (!ident) {
            int *iv = invbuf[j + 1][made];
            for (int t = 0; t < nc; t++) iv[out[clist[t]]] = clist[t];
            made++;
        }
    }
    free(orbitpts);
    genl[j + 1] = genptr[j + 1]; invl[j + 1] = invptr[j + 1];
    for (int m = 0; m < made; m++) { genptr[j + 1][m] = genbuf[j + 1][m]; invptr[j + 1][m] = invbuf[j + 1][m]; }
    ngenl[j + 1] = made;
    schreier_made += made;
    /* orbits of G_{j+1} on Cand_{j+1}: orbit id = minimum index */
    for (int t = 0; t < nc; t++) orbl[j + 1][clist[t]] = -1;
    for (int t = 0; t < nc; t++) {
        int s = clist[t];
        if (orbl[j + 1][s] >= 0) continue;
        int h0 = 0, h1 = 0;
        bfs_q[h1++] = s; orbl[j + 1][s] = s;
        while (h0 < h1) {
            int x2 = bfs_q[h0++];
            for (int k = 0; k < made; k++) {
                int z = genptr[j + 1][k][x2];
                if (!((cj1[z / 64] >> (z % 64)) & 1)) { fprintf(stderr, "stabilizer left the candidate set\n"); exit(7); }
                if (orbl[j + 1][z] < 0) { orbl[j + 1][z] = s; bfs_q[h1++] = z; }
            }
        }
    }
    stab2_calls++;
}

static void trivial_level(int L) {
    ngenl[L] = 0;
    for (int x = 0; x < n; x++) orbl[L][x] = x;
}

static double t_stab = 0, t_inc = 0, t_cand = 0;
static long long nodes_at[7];
static void rec2(int j, const int *o, const int *ou) {
    nodes++;
    nodes_at[j]++;
    if (clock() - tlastp > 20 * CLOCKS_PER_SEC) {
        tlastp = clock();
        fprintf(stderr, "progress %.0fs top %d/%d leaves %lld nodes %lld by depth %lld %lld %lld %lld %lld %lld tested %lld %lld %lld pruned %lld %lld %lld | time stab %.1f inc %.1f cand %.1f\n",
                (double)(clock() - tstart) / CLOCKS_PER_SEC, topi, n, leaves, nodes, nodes_at[0], nodes_at[1], nodes_at[2],
                nodes_at[3], nodes_at[4], nodes_at[5], tested[3], tested[4], tested[5], pruned[3], pruned[4], pruned[5],
                t_stab, t_inc, t_cand);
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
                if (INC && LEAFPRE && mode != 2) {         /* incremental leaf pre-test (no L1: a relaxation) */
                    if (!inc_level(6, 1)) { leaves++; leaf_pre_killed++; continue; }
                }
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
                    if (orb[z] < i || (orb[z] == i && z <= i)) { w &= ~(1ULL << bb); continue; }
                    if (BASE) {                            /* S7 base rule: every cell class >= x_1 in (H-orbit, index) */
                        int x1 = j == 0 ? i : chosen[0];
                        int ci = cidx[U[i] ^ U[z]];
                        if (orb0[ci] < orb0[x1] || (orb0[ci] == orb0[x1] && ci < x1)) w &= ~(1ULL << bb);
                    }
                }
                c2[k] = w; cnt += __builtin_popcountll(w);
            }
            if (cnt < need) continue;
            chosen[j] = i;
            if (INC) {
                int test = (j + 1 >= PMIN);
                if (test) tested[j + 1]++;
                clock_t q0 = clock(); int okl = inc_level(j + 1, test); t_inc += (double)(clock() - q0) / CLOCKS_PER_SEC;
                if (!okl) { pruned[j + 1]++; continue; }
            } else if (j + 1 >= PMIN) {
                tested[j + 1]++;
                if (!partial_ok(j + 1)) { pruned[j + 1]++; continue; }
            }
            { clock_t q0 = clock(); if (j + 1 < SDEPTH) { if (STAB2) stabilizer2(j, i); else stabilizer(j, i); } else trivial_level(j + 1); t_stab += (double)(clock() - q0) / CLOCKS_PER_SEC; }
            int old = nspan;
            for (int s = 0; s < old; s++) span[old + s] = span[s] ^ x;
            nspan = 2 * old;
            rec2(j + 1, o2, ou2);
            nspan = old;
            if (stopflag) return;
        }
    }
}

/* ---- Knuth estimator (Z4_KNUTH = number of random walks): each walk descends the H-canonical tree, at every level
   enumerating the valid children exactly as rec2 does (orbit minimum, independence, duals, units, adjacency and order,
   partial mod-4 test from PMIN on), multiplying the branching factors; E[product at a leaf] = number of leaves reached
   by rec2 (before the leaf tests), E[sum of partial products] = number of nodes. */
static int kchild[1 << 15];
static void knuth(int walks) {
    double sumL = 0, sumL2 = 0, sumN = 0, maxL = 0;
    long long zero = 0;
    for (int w = 0; w < walks; w++) {
        double prod = 1, nodes_est = 1;
        int o[32] = {0}, ou[32] = {0};
        span[0] = 0; nspan = 1;
        int j = 0;
        double leafest = 0;
        while (1) {
            const uint64_t *cand = candl + (size_t)j * nw;
            const int *orb = orbl[j];
            int need = 5 - j, nk = 0;
            for (int wi = 0; wi < nw; wi++) {
                uint64_t c = cand[wi];
                while (c) {
                    int b = __builtin_ctzll(c); c &= c - 1;
                    int i = wi * 64 + b;
                    if (orb[i] != i) continue;
                    int x = U[i], in = 0;
                    for (int s = 0; s < nspan; s++) if (span[s] == x) { in = 1; break; }
                    if (in) continue;
                    int bad = 0;
                    for (int t = 0; t < nd; t++) {
                        int oo = o[t] + ((FK[i] >> t) & 1), zz = j + 1 - oo;
                        if (KM[t] == 1) { if (oo > 1 && zz > 0) { bad = 1; break; } }
                        else { if (oo > 2 && zz > 1) { bad = 1; break; } }
                    }
                    if (bad) continue;
                    if (j + 1 == 6) {
                        int okk = 1;
                        for (int t = 0; t < nu; t++) if (ou[t] + ((FU[i] >> t) & 1) < 1) { okk = 0; break; }
                        if (okk) kchild[nk++] = i;
                        continue;
                    }
                    uint64_t *c2 = candl + (size_t)(j + 1) * nw;
                    const uint64_t *nb = nbrs + (size_t)i * nw;
                    int cnt = 0;
                    for (int k = 0; k < nw; k++) {
                        uint64_t w2 = cand[k] & nb[k], ww = w2;
                        while (ww) {
                            int bb = __builtin_ctzll(ww); ww &= ww - 1;
                            int z = k * 64 + bb;
                            if (orb[z] < i || (orb[z] == i && z <= i)) w2 &= ~(1ULL << bb);
                        }
                        c2[k] = w2; cnt += __builtin_popcountll(w2);
                    }
                    if (cnt < need) continue;
                    chosen[j] = i;
                    if (INC && !inc_level(j + 1, j + 1 >= PMIN)) continue;
                    kchild[nk++] = i;
                }
            }
            if (nk == 0) break;
            if (j + 1 == 6) { leafest = prod * nk; break; }
            int i = kchild[rnd32() % nk];
            prod *= nk;
            nodes_est += prod;
            /* rebuild the state of the chosen child */
            uint64_t *c2 = candl + (size_t)(j + 1) * nw;
            const uint64_t *nb = nbrs + (size_t)i * nw;
            for (int k = 0; k < nw; k++) {
                uint64_t w2 = cand[k] & nb[k], ww = w2;
                while (ww) {
                    int bb = __builtin_ctzll(ww); ww &= ww - 1;
                    int z = k * 64 + bb;
                    if (orb[z] < i || (orb[z] == i && z <= i)) w2 &= ~(1ULL << bb);
                }
                c2[k] = w2;
            }
            chosen[j] = i;
            if (INC) inc_level(j + 1, 0);
            if (j + 1 < SDEPTH) { if (STAB2) stabilizer2(j, i); else stabilizer(j, i); } else trivial_level(j + 1);
            for (int t = 0; t < nd; t++) o[t] += (FK[i] >> t) & 1;
            for (int t = 0; t < nu; t++) ou[t] += (FU[i] >> t) & 1;
            int x = U[i], old = nspan;
            for (int s = 0; s < old; s++) span[old + s] = span[s] ^ x;
            nspan = 2 * old;
            j++;
        }
        sumL += leafest; sumL2 += leafest * leafest; sumN += nodes_est;
        if (leafest > maxL) maxL = leafest;
        if (leafest == 0) zero++;
    }
    double mL = sumL / walks, sd = sqrt(sumL2 / walks - mL * mL);
    printf("{\"knuth_walks\": %d, \"leaves_est\": %.4g, \"leaves_sd_of_mean\": %.3g, \"nodes_est\": %.4g, "
           "\"max_walk\": %.4g, \"dead_walks\": %lld, \"s\": %.1f}\n", walks, mL, sd / sqrt((double)walks),
           sumN / walks, maxL, zero, (double)(clock() - tstart) / CLOCKS_PER_SEC);
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
        long long ecut = 0;
        if (getenv("Z4_KEEPSUMS"))                         /* all 21 differences in the kept orbits: S7-invariant */
            for (int i = 0; i < n; i++)
                for (int wi = 0; wi < nw; wi++) {
                    uint64_t c = nbr[(size_t)i * nw + wi];
                    while (c) {
                        int b = __builtin_ctzll(c); c &= c - 1;
                        int j = wi * 64 + b, si = cidx[U[i] ^ U[j]];
                        if (!((keepm[si / 64] >> (si % 64)) & 1)) { nbr[(size_t)i * nw + wi] &= ~(1ULL << b); ecut++; }
                    }
                }
        fprintf(stderr, "restricted to %lld classes (%d orbits in all), edges cut for sums %lld\n", kept, nr, ecut);
    }
    int o0[32] = {0}, ou0[32] = {0};
    span[0] = 0; nspan = 1;
    const char *cv = getenv("Z4_CANON");
    int canon = (cv ? atoi(cv) : 1) && mode != 1 && !skelfile;
    if (getenv("Z4_SDEPTH")) SDEPTH = atoi(getenv("Z4_SDEPTH"));
    if (getenv("Z4_NSCH")) NSCHREIER = atoi(getenv("Z4_NSCH"));
    if (getenv("Z4_INC")) INC = atoi(getenv("Z4_INC"));
    if (getenv("Z4_BASE")) BASE = atoi(getenv("Z4_BASE"));
    if (getenv("Z4_FP7")) FP7 = atoi(getenv("Z4_FP7"));
    if (getenv("Z4_STAB2")) STAB2 = atoi(getenv("Z4_STAB2"));
    if (getenv("Z4_LEAFPRE")) LEAFPRE = atoi(getenv("Z4_LEAFPRE"));
    if (getenv("Z4_MAXLEAVES")) maxleaves = atoll(getenv("Z4_MAXLEAVES"));
    if (getenv("Z4_MAXSURV")) maxsurv = atoll(getenv("Z4_MAXSURV"));
    if (getenv("Z4_INTPHI")) INTPHI = atoi(getenv("Z4_INTPHI"));
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
        tA = malloc(sizeof(int) * n); tB = calloc(n, sizeof(int)); tC = malloc(sizeof(int) * n); tD = malloc(sizeof(int) * n);
        clist = malloc(sizeof(int) * n); pathbuf = malloc(sizeof(int) * 8192);
        for (int L = 1; L < 7; L++) for (int m = 0; m < MAXGEN; m++) invbuf[L][m] = malloc(sizeof(int) * n);
        candl = calloc((size_t)7 * nw, sizeof(uint64_t));
        genl[0] = gen0; ngenl[0] = ngen0;
        if (ngen0 > MAXGEN * 4) { fprintf(stderr, "too many H generators\n"); return 5; }
        for (int k = 0; k < ngen0; k++) { inv0buf[k] = malloc(sizeof(int) * n); for (int x = 0; x < n; x++) inv0buf[k][gen0[k][x]] = x; }
        invl[0] = inv0buf;
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
    } else if (canon && getenv("Z4_KNUTH")) {
        knuth(atoi(getenv("Z4_KNUTH")));
        return 0;
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
    printf("], \"pmin\": %d, \"partial_tested\": [%lld, %lld, %lld], \"partial_pruned\": [%lld, %lld, %lld], "
           "\"fail_empty\": [%lld, %lld, %lld], \"fail_z4\": [%lld, %lld, %lld], \"leaf_pre_killed\": %lld, "
           "\"sdepth\": %d, \"stab2\": %d, \"schreier_gens\": %d, \"intphi\": %d, \"int_killed\": %lld, "
           "\"int_survivors\": %lld, \"intphi_nodes\": %lld}\n", PMIN,
           tested[3], tested[4], tested[5], pruned[3], pruned[4], pruned[5],
           fail_empty[3], fail_empty[4], fail_empty[5], fail_z4[3], fail_z4[4], fail_z4[5], leaf_pre_killed,
           SDEPTH, STAB2, NSCHREIER, INTPHI, n_int_killed, n_int_surv, iphi_nodes);
    if (fsurv) fclose(fsurv);
    return mismatch ? 4 : 0;
}
