// J2 engine (R6, cell J2): exhaustive search of the two-star support W = star(0) u star(1) u {V}.
// Setting (notes/151 s2ter, notes/154): a = +-1 on the 20 cut labels (cells (0,x),(1,x), x=2..6), a = +2 on V = (5,6,+).
// Base = star(0) (structure S0 = (Q0, Pi0)) and P_sigma cap star(0).  Unknowns = the 10 cut1 labels' columns (their 2+2 root
// incidences into star(0)), their P_sigma status, and the star(1) relations T between cut1 labels.
// Every test is a necessary condition:
//  frame   : M = 12I - 4T - RR^T = 28 P_E has rank 15 on all 42 labels.  star(0) spans 11 dims, so the residuals (w.r.t.
//            span f_star0) of F = sum a_L f_L, V and the cut1 labels live in R^4: residual Gram PSD (float, robust margin)
//            and rank <= 4 (EXACT, mod p = 2^31-1: rank mod p <= rank over Q).
//  local   : pair design of O_0+ (each non-Q0 pair covered by exactly one outside root), mixed-pair capacities, cut0 cross
//            budgets (C/B edges), star(1) partner slots/types, h-profile, lambda/mu with v, sigma v and between cut1 roots,
//            Z roots' star(1) slots, P_sigma cap star(1) = 2+2.
// Usage: j2_engine <a: 42 ints> <symfile> <mode> [args]
//   mode "sample N seed" : run the search on N random star-level survivors (timing / census)
//   mode "full outfile nthreads" : exhaustive over all (Q0, Pi0, P_sigma0) canonical under the symmetry file
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#ifdef _OPENMP
#include <omp.h>
#endif
#define N 12
#define NY 10
#define PR 2147483647ULL
typedef unsigned long long u64;
static inline u64 mulm(u64 a, u64 b) { return (a * b) % PR; }
static inline u64 addm(u64 a, u64 b) { u64 s = a + b; return s >= PR ? s - PR : s; }
static inline u64 subm(u64 a, u64 b) { return a >= b ? a - b : a + PR - b; }
static inline u64 tom(long long x) { x %= (long long)PR; if (x < 0) x += PR; return (u64)x; }
static u64 powm(u64 a, u64 e) { u64 r = 1; while (e) { if (e & 1) r = mulm(r, a); a = mulm(a, a); e >>= 1; } return r; }
static u64 invm(u64 a) { return powm(a, PR - 2); }

static int inv[10395][N]; static int ninv = 0;
static void gen_inv(int *p, int *used) {
    int i = 0; while (i < N && used[i]) i++;
    if (i == N) { memcpy(inv[ninv++], p, sizeof(int) * N); return; }
    used[i] = 1;
    for (int j = i + 1; j < N; j++) if (!used[j]) { used[j] = 1; p[i] = j; p[j] = i; gen_inv(p, used); used[j] = 0; }
    used[i] = 0;
}
// ---------------- global pattern data ----------------
static int alpha[N], xof[N], sof[N];
static int aY[NY], xY[NY], sY[NY];
static int nsym = 0; static int symperm[4096][N];
static int withV = 1, asq = 24;   // J2: V present, |a|^2 = 24 ; R5: no V, |a|^2 = 20   // label permutations of star(0) induced by the pattern stabiliser (fixing star 0)
// ---------------- per-structure data ----------------
typedef struct {
    int L[4];              // L1<L2 (+ incidences), L3<L4 (- incidences)
    int m[N];
    double vd[N]; u64 vm[N];
    double sd, fd, v0d; u64 sm, fm, v0m;
    int psmask, zinc, zq, zp, so;
    int pairP, pairM;
    signed char needC[N], needB[N];
    int zroot[4];          // Z-root adjacency of p_Y: index 0..3 for +z1,-z1,+z2,-z2 (p_Y ~ root); -1 unused
    int nz;
    int dent;              // D-entry label or -1
} Cand;
typedef struct {
    int Q[N], P[N], mask;
    int cL[N], bL[N];
    int cap[N][N];         // mixed-pair capacities (outside roots adjacent to 0rep(L) and -0rep(L'))
    int qpair[N][N];       // 1 if {L,L'} is a Q0 pair
    int vpair_id, spair_id;
    double Ad[N][N]; u64 Am[N][N];   // (A0+J)^{-1}
    double vFd[N], vVd[N]; u64 vFm[N], vVm[N];
    double RFF, RFV, RVV; u64 RFFm, RFVm, RVVm;
    int mV[N];
    int zsQ[4], zsP[4];    // Z roots' remaining star(1) slots by 1-side after Z-Z edges (Q-type = same 1-side)
    int zh[4];             // h-sum of each Z root's star(0) neighbours
    Cand *cand[NY]; int ncand[NY];
} Str;
// Z roots: 0:+z1 (e0+e1), 1:-z1, 2:+z2 (e0-e1), 3:-z2.  1-sides: +1,-1,-1,+1
static const int zside[4] = {1, -1, -1, 1};
static int zroot_of(int L, int eps) { return (L == 0) ? (eps > 0 ? 0 : 1) : (eps > 0 ? 2 : 3); }

static int chol_inv_d(double A[N][N], double Ainv[N][N]) {
    double L[N][N]; memset(L, 0, sizeof L);
    for (int j = 0; j < N; j++) {
        double s = A[j][j]; for (int k = 0; k < j; k++) s -= L[j][k] * L[j][k];
        if (s <= 1e-12) return 0; L[j][j] = sqrt(s);
        for (int i = j + 1; i < N; i++) { double t = A[i][j]; for (int k = 0; k < j; k++) t -= L[i][k] * L[j][k]; L[i][j] = t / L[j][j]; }
    }
    for (int c = 0; c < N; c++) {
        double y[N], x[N];
        for (int i = 0; i < N; i++) { double s = (i == c); for (int k = 0; k < i; k++) s -= L[i][k] * y[k]; y[i] = s / L[i][i]; }
        for (int i = N - 1; i >= 0; i--) { double s = y[i]; for (int k = i + 1; k < N; k++) s -= L[k][i] * x[k]; x[i] = s / L[i][i]; }
        for (int i = 0; i < N; i++) Ainv[i][c] = x[i];
    }
    return 1;
}
static int inv_mod(long long A[N][N], u64 R[N][N]) {
    u64 M[N][2 * N];
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) { M[i][j] = tom(A[i][j]); M[i][N + j] = (i == j); }
    for (int c = 0; c < N; c++) {
        int piv = -1; for (int r = c; r < N; r++) if (M[r][c]) { piv = r; break; }
        if (piv < 0) return 0;
        if (piv != c) for (int j = 0; j < 2 * N; j++) { u64 t = M[c][j]; M[c][j] = M[piv][j]; M[piv][j] = t; }
        u64 iv = invm(M[c][c]);
        for (int j = 0; j < 2 * N; j++) M[c][j] = mulm(M[c][j], iv);
        for (int r = 0; r < N; r++) if (r != c && M[r][c]) { u64 f = M[r][c]; for (int j = 0; j < 2 * N; j++) M[r][j] = subm(M[r][j], mulm(f, M[c][j])); }
    }
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) R[i][j] = M[i][N + j];
    return 1;
}
static inline double dotd(const int *m, const double *v) { double s = 0; for (int i = 0; i < N; i++) s += m[i] * v[i]; return s; }
static inline u64 dotm(const int *m, const u64 *v) { u64 s = 0; for (int i = 0; i < N; i++) { if (m[i] > 0) s = addm(s, mulm((u64)m[i], v[i])); else if (m[i] < 0) s = subm(s, mulm((u64)(-m[i]), v[i])); } return s; }

// ---------------- star-level tests (same as star0_count.c), returns 1 if (Q,P,mask) passes ----------------
static int star_prepare(Str *S, int *Q, int *P) {
    memcpy(S->Q, Q, sizeof(int) * N); memcpy(S->P, P, sizeof(int) * N);
    int T[N][N]; memset(T, 0, sizeof T);
    for (int L = 0; L < N; L++) { T[L][Q[L]] += 1; T[L][P[L]] -= 1; }
    double A[N][N]; long long Ai[N][N];
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) {
        Ai[i][j] = (i == j ? 11 : 0) + ((xof[i] == xof[j] && i != j) ? 1 : 0) - 4 * T[i][j];
        A[i][j] = (double)Ai[i][j];
    }
    if (!chol_inv_d(A, S->Ad)) return 0;
    if (!inv_mod(Ai, S->Am)) return -1;   // singular mod p: caller falls back
    double al[N]; int cF[N]; for (int i = 0; i < N; i++) { al[i] = alpha[i]; cF[i] = 28 * alpha[i]; }
    for (int i = 0; i < N; i++) { S->vFd[i] = 0; for (int j = 0; j < N; j++) S->vFd[i] += S->Ad[i][j] * cF[j]; }
    for (int i = 0; i < N; i++) { u64 s = 0; for (int j = 0; j < N; j++) s = (cF[j] >= 0) ? addm(s, mulm(S->Am[i][j], (u64)cF[j])) : subm(s, mulm(S->Am[i][j], (u64)(-cF[j]))); S->vFm[i] = s; }
    S->RFF = 28.0 * asq - dotd(cF, S->vFd); S->RFFm = subm((u64)(28 * asq), dotm(cF, S->vFm));
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) S->qpair[i][j] = (Q[i] == j);
    return 1;
}
// ---------------- the search ----------------
typedef struct {
    int nas; int order[NY]; int ci[NY]; int ps[NY];
    int T[NY][NY];
    int needQ[NY], needP[NY], sig[NY], target[NY];
    int usedC[N], usedB[N];
    unsigned char pairused[N * N];
    unsigned char mix[N][N];
    int cntPs[2];
    int zQ[4], zP[4], zhs[4];
    // residual basis: ids -2 = F, -1 = V, >=0 = label
    int k; int bid[4]; u64 Ginv[4][4]; u64 Gb[4][4];
    double Lc[4][4]; int fl_ok;   // float Cholesky of the basis Gram
    int ndep; int did[NY]; u64 dco[NY][4];
    int assigned[NY];
} St;
static long long g_surv;
static long long g_nodes;
#pragma omp threadprivate(g_nodes)
typedef struct { FILE *fp; } Out;

static inline int shared_inner_root(int y, int L, int eps) {   // p_Y and root eps*0rep(L)
    if (L < 2) return (eps * (L == 0 ? 1 : -1)) == aY[y];
    return (xof[L] == xY[y] && eps * sof[L] == aY[y] * sY[y]);
}
static inline int pYdot(int y, int z) { return aY[y] * aY[z] * (1 + ((xY[y] == xY[z]) ? sY[y] * sY[z] : 0)); }
static inline int rVdot(int y) { return (xY[y] == 5 || xY[y] == 6) ? aY[y] * sY[y] : 0; }

// residual inner product between two cut1 vectors (label y cand a, label z cand b) with T
static inline void res_yy(const Str *S, int y, const Cand *a, int z, const Cand *b, int T, double *d, u64 *m) {
    int base = -4 * T - pYdot(y, z);
    *d = base - dotd(a->m, b->vd);
    *m = subm(tom(base), dotm(a->m, b->vm));
}
// get inner products (d,m) of vector id with a new label vector (y, c, ps, T row)
static void ip_with(const Str *S, const St *st, int id, int y, const Cand *c, int ps, const int *Trow, double *d, u64 *m) {
    if (id == -2) { *d = c->fd; *m = c->fm; return; }
    if (id == -1) { int TVY = -ps; *d = c->v0d - 4.0 * TVY; *m = subm(c->v0m, tom(4 * TVY)); return; }
    const Cand *b = &S->cand[id][st->ci[id]];
    res_yy(S, y, c, id, b, Trow[id], d, m);
}
// basis vectors' mutual inner products (for F, V, labels)
static void ip_basis(const Str *S, const St *st, int i1, int i2, double *d, u64 *m) {
    if (i1 > i2) { int t = i1; i1 = i2; i2 = t; }
    if (i1 == -2 && i2 == -2) { *d = S->RFF; *m = S->RFFm; return; }
    if (i1 == -2 && i2 == -1) { *d = S->RFV; *m = S->RFVm; return; }
    if (i1 == -1 && i2 == -1) { *d = S->RVV; *m = S->RVVm; return; }
    if (i1 < 0) {   // i2 is a label
        const Cand *c = &S->cand[i2][st->ci[i2]];
        if (i1 == -2) { *d = c->fd; *m = c->fm; return; }
        int TVY = -st->ps[i2]; *d = c->v0d - 4.0 * TVY; *m = subm(c->v0m, tom(4 * TVY)); return;
    }
    const Cand *a = &S->cand[i1][st->ci[i1]], *b = &S->cand[i2][st->ci[i2]];
    if (i1 == i2) { *d = a->sd; *m = a->sm; return; }
    res_yy(S, i1, a, i2, b, st->T[i1][i2], d, m);
}
// recompute basis inverse (mod p) and float Cholesky
static void basis_refresh(const Str *S, St *st) {
    int k = st->k; u64 G[4][8]; double Gd[4][4];
    for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) { double d; u64 m; ip_basis(S, st, st->bid[i], st->bid[j], &d, &m); G[i][j] = m; st->Gb[i][j] = m; Gd[i][j] = d; }
    for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) G[i][k + j] = (i == j);
    for (int c = 0; c < k; c++) {
        int piv = -1; for (int r = c; r < k; r++) if (G[r][c]) { piv = r; break; }
        if (piv < 0) { fprintf(stderr, "basis singular mod p\n"); exit(3); }
        if (piv != c) for (int j = 0; j < 2 * k; j++) { u64 t = G[c][j]; G[c][j] = G[piv][j]; G[piv][j] = t; }
        u64 iv = invm(G[c][c]); for (int j = 0; j < 2 * k; j++) G[c][j] = mulm(G[c][j], iv);
        for (int r = 0; r < k; r++) if (r != c && G[r][c]) { u64 f = G[r][c]; for (int j = 0; j < 2 * k; j++) G[r][j] = subm(G[r][j], mulm(f, G[c][j])); }
    }
    for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) st->Ginv[i][j] = G[i][k + j];
    // float Cholesky with conditioning guard
    st->fl_ok = 1; memset(st->Lc, 0, sizeof st->Lc);
    for (int j = 0; j < k; j++) {
        double s = Gd[j][j]; for (int t = 0; t < j; t++) s -= st->Lc[j][t] * st->Lc[j][t];
        if (s < 1e-3) { st->fl_ok = 0; return; }
        st->Lc[j][j] = sqrt(s);
        for (int i = j + 1; i < k; i++) { double t = Gd[i][j]; for (int q = 0; q < j; q++) t -= st->Lc[i][q] * st->Lc[j][q]; st->Lc[i][j] = t / st->Lc[j][j]; }
    }
}
// test a new vector: g (mod p, float) inner products with basis, s = its norm; returns 0 reject, 1 dependent, 2 independent
static int res_test(const St *st, const u64 *gm, const double *gd, u64 sm, double sd, u64 *coef) {
    int k = st->k;
    u64 c[4]; for (int i = 0; i < k; i++) { u64 s = 0; for (int j = 0; j < k; j++) s = addm(s, mulm(st->Ginv[i][j], gm[j])); c[i] = s; }
    u64 q = 0; for (int i = 0; i < k; i++) q = addm(q, mulm(gm[i], c[i]));
    u64 schur = subm(sm, q);
    if (st->fl_ok) {
        double y[4]; for (int i = 0; i < k; i++) { double s = gd[i]; for (int j = 0; j < i; j++) s -= st->Lc[i][j] * y[j]; y[i] = s / st->Lc[i][i]; }
        double sch = sd; for (int i = 0; i < k; i++) sch -= y[i] * y[i];
        if (sch < -1e-6 * (1.0 + fabs(sd))) return 0;          // PSD violation (robust)
    }
    if (schur == 0) { for (int i = 0; i < k; i++) coef[i] = c[i]; return 1; }
    if (k == 4) return 0;                                        // rank would exceed 4: exact kill
    return 2;
}
static Out g_out;
static void emit(const Str *S, const St *st, FILE *fp) {
    if (!fp) return;
    fprintf(fp, "Q");
    for (int i = 0; i < N; i++) fprintf(fp, " %d", S->Q[i]);
    fprintf(fp, " P"); for (int i = 0; i < N; i++) fprintf(fp, " %d", S->P[i]);
    fprintf(fp, " mask %d cols", S->mask);
    for (int y = 0; y < NY; y++) { const Cand *c = &S->cand[y][st->ci[y]]; fprintf(fp, " %d,%d,%d,%d,%d", c->L[0], c->L[1], c->L[2], c->L[3], st->ps[y]); }
    fprintf(fp, " T");
    for (int y = 0; y < NY; y++) for (int z = y + 1; z < NY; z++) if (st->T[y][z]) fprintf(fp, " %d,%d,%d", y, z, st->T[y][z]);
    fprintf(fp, "\n");
}
static int final_check(const Str *S, St *st) {
    for (int L = 2; L < N; L++) if (st->usedC[L] != S->cL[L] || st->usedB[L] != S->bL[L]) return 0;
    if (withV && (st->cntPs[0] != 2 || st->cntPs[1] != 2)) return 0;
    for (int r = 0; r < 4; r++) if (st->zQ[r] != 0 || st->zP[r] != 0) return 0;
    for (int r = 0; r < 4; r++) if (st->zhs[r] + S->zh[r] != 0) return 0;
    // partner slots: every label full, or empty and D-pairable (zinc=0, target 0, no D-entry)
    int free_[NY], nf = 0;
    for (int y = 0; y < NY; y++) {
        if (st->needQ[y] == 0 && st->needP[y] == 0) { if (st->sig[y] != st->target[y]) return 0; continue; }
        const Cand *c = &S->cand[y][st->ci[y]];
        if (st->needQ[y] == 1 && st->needP[y] == 1 && c->zinc == 0 && st->target[y] == 0 && c->dent < 0) { free_[nf++] = y; continue; }
        return 0;
    }
    if (nf & 1) return 0;
    // full lambda/mu recount among cut1 roots and with v, sigma v (star(0) incidences + inner + cut1 via T + v/sigma v)
    for (int y = 0; y < NY; y++) {
        const Cand *c = &S->cand[y][st->ci[y]];
        int innS = withV && (xY[y] == 5 || xY[y] == 6) && (aY[y] * sY[y] == -1), innV = withV && (xY[y] == 5 || xY[y] == 6) && (aY[y] * sY[y] == 1);
        int cs = 0, cv = 0;
        for (int t = 0; t < 4; t++) { int L = c->L[t], sg = (t < 2) ? 1 : -1; if (L < 2 || !((S->mask >> L) & 1)) continue; if (sg * alpha[L] == 1) cs++; else cv++; }
        for (int z = 0; z < NY; z++) if (z != y && st->ps[z]) { if (st->T[y][z] == 1) cs++; if (st->T[y][z] == -1) cv++; }
        if (cs + innS > (st->ps[y] ? 1 : 2)) return 0;
        if (cv + innV > 2) return 0;
        for (int z = y + 1; z < NY; z++) {
            const Cand *b = &S->cand[z][st->ci[z]];
            for (int eps = -1; eps <= 1; eps += 2) {
                int cnt = 0;
                for (int i = 0; i < 4; i++) { int Li = c->L[i], si = (i < 2) ? 1 : -1;
                    for (int j = 0; j < 4; j++) { int Lj = b->L[j], sj = ((j < 2) ? 1 : -1) * eps; if (Li == Lj && si == sj) cnt++; } }
                cnt += (aY[y] == eps * aY[z]) || (xY[y] == xY[z] && aY[y] * sY[y] == eps * aY[z] * sY[z]);
                for (int w = 0; w < NY; w++) if (w != y && w != z && st->T[y][w] && st->T[z][w] && st->T[y][w] * st->T[z][w] == eps) cnt++;
                if (st->ps[y] && eps == 1 && st->ps[z]) cnt++;
                if (cnt > ((st->T[y][z] == eps) ? 1 : 2)) return 0;
            }
        }
    }
    // v's star(1) pairs must not be Q1 pairs: labels in P_sigma with a_Y = -1 (v's O_1+ pair) / +1
    for (int sgn = -1; sgn <= 1 && withV; sgn += 2) {
        int ids[2], n = 0;
        for (int y = 0; y < NY; y++) if (st->ps[y] && aY[y] == sgn) ids[n++] = y;
        if (n == 2) { int y = ids[0], z = ids[1], T = st->T[y][z];
            if (T) { int qtype = (T == 1) ? (aY[y] == aY[z]) : (aY[y] == -aY[z]); if (qtype) return 0; } }
    }
    return 1;
}
static void dfs(const Str *S, St *st, FILE *fp);
// try assigning label y with candidate index ci, status ps, partner choice (up to 2 partners among assigned labels)
static void try_assign(const Str *S, St *st, int y, int ci, int ps, FILE *fp) {
    const Cand *c = &S->cand[y][ci];
    // partner candidates among assigned labels with open slot of the right type
    int need_q = 1 - (c->zq), need_p = 1 - (c->zp);
    if (need_q < 0 || need_p < 0) return;
    int target = -4 - c->so + 2 * ps;
    // enumerate partner sets: none, one (type Q or P), two (one Q + one P)
    int opts[64][2][2]; int nopt = 0;   // up to two (label, T)
    int candQ[NY][2], nQ = 0, candP[NY][2], nP = 0;
    for (int t = 0; t < st->nas; t++) {
        int z = st->order[t];
        // Q-type relation between y and z: T = +1 if aY equal, else -1
        int Tq = (aY[y] == aY[z]) ? 1 : -1, Tp = -Tq;
        if (need_q && st->needQ[z] > 0) { candQ[nQ][0] = z; candQ[nQ][1] = Tq; nQ++; }
        if (need_p && st->needP[z] > 0) { candP[nP][0] = z; candP[nP][1] = Tp; nP++; }
    }
    // option list: (qchoice, pchoice) with -1 = none
    for (int a = -1; a < nQ; a++) for (int b = -1; b < nP; b++) {
        if (a >= 0 && b >= 0 && candQ[a][0] == candP[b][0]) continue;   // same label cannot be both (that would be a D-pair: T=0)
        int sig = (a >= 0 ? candQ[a][1] : 0) + (b >= 0 ? candP[b][1] : 0);
        int remaining = (need_q - (a >= 0)) + (need_p - (b >= 0));
        // D-pair completion possible only if no partner at all
        int dpos = (a < 0 && b < 0 && need_q == 1 && need_p == 1 && c->zinc == 0 && target == 0);
        if (abs(target - sig) > remaining && !dpos) continue;
        if (((target - sig - remaining) & 1) && !dpos) continue;
        if (nopt < 64) { opts[nopt][0][0] = a >= 0 ? candQ[a][0] : -1; opts[nopt][0][1] = a >= 0 ? candQ[a][1] : 0;
                         opts[nopt][1][0] = b >= 0 ? candP[b][0] : -1; opts[nopt][1][1] = b >= 0 ? candP[b][1] : 0; nopt++; }
    }
    for (int o = 0; o < nopt; o++) {
        int Trow[NY]; memset(Trow, 0, sizeof Trow);
        for (int h = 0; h < 2; h++) if (opts[o][h][0] >= 0) Trow[opts[o][h][0]] = opts[o][h][1];
        // lambda/mu between p_Y and assigned cut1 roots (star(0) incidences + inner + cut1 via T + sigma v)
        int bad = 0;
        for (int t = 0; t < st->nas && !bad; t++) {
            int z = st->order[t]; const Cand *b = &S->cand[z][st->ci[z]];
            for (int eps = -1; eps <= 1 && !bad; eps += 2) {
                int cnt = 0;
                for (int i = 0; i < 4; i++) { int Li = c->L[i], si = (i < 2) ? 1 : -1;
                    for (int j = 0; j < 4; j++) { int Lj = b->L[j], sj = ((j < 2) ? 1 : -1) * eps; if (Li == Lj && si == sj) cnt++; } }
                int sh = (aY[y] == eps * aY[z]) || (xY[y] == xY[z] && aY[y] * sY[y] == eps * aY[z] * sY[z]);
                cnt += sh;
                for (int u = 0; u < st->nas; u++) { int w = st->order[u]; if (w == z) continue;
                    if (Trow[w] && st->T[z][w] && Trow[w] * st->T[z][w] == eps) cnt++; }
                if (ps && eps == 1 && st->ps[z]) cnt++;
                int adj = (Trow[z] == eps);
                if (cnt > (adj ? 1 : 2)) bad = 1;
            }
        }
        if (bad) continue;
        // residual test against basis and dependent vectors
        u64 gm[4]; double gd[4];
        for (int i = 0; i < st->k; i++) ip_with(S, st, st->bid[i], y, c, ps, Trow, &gd[i], &gm[i]);
        u64 coef[4];
        int r = res_test(st, gm, gd, c->sm, c->sd, coef);
        if (!r) continue;
        // consistency with dependent vectors
        int okd = 1;
        for (int t = 0; t < st->ndep && okd; t++) {
            int z = st->did[t]; double dd; u64 mm; ip_with(S, st, z, y, c, ps, Trow, &dd, &mm);
            u64 pred = 0; for (int i = 0; i < st->k; i++) pred = addm(pred, mulm(st->dco[t][i], gm[i]));
            if (pred != mm) okd = 0;
        }
        if (!okd) continue;
        // commit
        St sv = *st;
        st->assigned[y] = 1; st->order[st->nas++] = y; st->ci[y] = ci; st->ps[y] = ps;
        for (int z = 0; z < NY; z++) if (st->assigned[z] && z != y) { st->T[y][z] = st->T[z][y] = Trow[z]; }
        st->needQ[y] = need_q; st->needP[y] = need_p; st->sig[y] = 0; st->target[y] = target;
        for (int h = 0; h < 2; h++) { int z = opts[o][h][0]; if (z < 0) continue; int T = opts[o][h][1];
            if (h == 0) { st->needQ[y]--; st->needQ[z]--; } else { st->needP[y]--; st->needP[z]--; }
            st->sig[y] += T; st->sig[z] += T; }
        // partners' sigma feasibility
        int feas = 1;
        for (int t = 0; t < st->nas && feas; t++) { int z = st->order[t]; int rem = st->needQ[z] + st->needP[z];
            if (abs(st->target[z] - st->sig[z]) > rem) feas = 0; }
        if (feas) {
            if (r == 2) { st->bid[st->k++] = y; basis_refresh(S, st);
                // dependent vectors: coefficients get a zero on the new basis vector
                for (int t = 0; t < st->ndep; t++) st->dco[t][st->k - 1] = 0; }
            else { st->did[st->ndep] = y; for (int i = 0; i < st->k; i++) st->dco[st->ndep][i] = coef[i]; st->ndep++; }
            dfs(S, st, fp);
        }
        *st = sv;
    }
}
// combinatorial compatibility of candidate (y, ci, ps) with the current state
static int comb_ok(const Str *S, const St *st, int y, const Cand *c, int ps) {
    if (st->pairused[c->pairP] || st->pairused[c->pairM]) return 0;
    for (int L = 2; L < N; L++) if (st->usedC[L] + c->needC[L] > S->cL[L] || st->usedB[L] + c->needB[L] > S->bL[L]) return 0;
    int side = aY[y] > 0; if (ps && st->cntPs[side] >= 2) return 0;
    // mixed pairs: p_Y uses (L1|L2, L3|L4); -p_Y uses (L3|L4, L1|L2)
    unsigned char add[N][N]; memset(add, 0, sizeof add);
    for (int i = 0; i < 2; i++) for (int j = 2; j < 4; j++) { add[c->L[i]][c->L[j]]++; add[c->L[j]][c->L[i]]++; }
    for (int i = 0; i < 2; i++) for (int j = 2; j < 4; j++) {
        int a = c->L[i], b = c->L[j];
        if (st->mix[a][b] + add[a][b] > S->cap[a][b]) return 0;
        if (st->mix[b][a] + add[b][a] > S->cap[b][a]) return 0;
    }
    // Z roots' star(1) slots
    int dq[4] = {0, 0, 0, 0}, dp[4] = {0, 0, 0, 0};
    for (int t = 0; t < c->nz; t++) { int r = c->zroot[t] & 3, root_sign = (c->zroot[t] >> 2) ? -1 : 1;
        // the cut1 root adjacent to Z root r is root_sign * p_Y: its 1-side = root_sign * aY
        int side1 = root_sign * aY[y]; if (side1 == zside[r]) dq[r]++; else dp[r]++; }
    for (int r = 0; r < 4; r++) if (st->zQ[r] - dq[r] < 0 || st->zP[r] - dp[r] < 0) return 0;
    return 1;
}
static void apply_comb(const Str *S, St *st, int y, const Cand *c, int ps, int sign) {
    st->pairused[c->pairP] += sign; st->pairused[c->pairM] += sign;
    for (int L = 2; L < N; L++) { st->usedC[L] += sign * c->needC[L]; st->usedB[L] += sign * c->needB[L]; }
    if (ps) st->cntPs[aY[y] > 0] += sign;
    for (int i = 0; i < 2; i++) for (int j = 2; j < 4; j++) { st->mix[c->L[i]][c->L[j]] += sign; st->mix[c->L[j]][c->L[i]] += sign; }
    for (int t = 0; t < c->nz; t++) { int r = c->zroot[t] & 3, root_sign = (c->zroot[t] >> 2) ? -1 : 1;
        int side1 = root_sign * aY[y]; if (side1 == zside[r]) st->zQ[r] -= sign; else st->zP[r] -= sign;
        st->zhs[r] += sign * root_sign; }
}
static void dfs(const Str *S, St *st, FILE *fp) {
    g_nodes++;
    if (st->nas == NY) { if (final_check(S, st)) {
        #pragma omp atomic
        g_surv++;
        #pragma omp critical
        emit(S, st, fp); }
        return; }
    // choose unassigned label with fewest combinatorially compatible (cand, ps)
    int besty = -1, bestn = 1 << 30;
    for (int y = 0; y < NY; y++) if (!st->assigned[y]) {
        int n = 0;
        for (int i = 0; i < S->ncand[y] && n < bestn; i++) { const Cand *c = &S->cand[y][i];
            for (int ps = 0; ps < 2; ps++) if ((c->psmask >> ps) & 1) if (comb_ok(S, st, y, c, ps)) n++; }
        if (n < bestn) { bestn = n; besty = y; }
        if (n == 0) return;
    }
    int y = besty;
    for (int i = 0; i < S->ncand[y]; i++) { const Cand *c = &S->cand[y][i];
        for (int ps = 0; ps < 2; ps++) if ((c->psmask >> ps) & 1) {
            if (!comb_ok(S, st, y, c, ps)) continue;
            apply_comb(S, st, y, c, ps, +1);
            try_assign(S, st, y, i, ps, fp);
            apply_comb(S, st, y, c, ps, -1);
        } }
}
// build candidates for all cut1 labels given S (Q,P,mask prepared); returns 0 if some label has none
static int build(Str *S) {
    int *Q = S->Q, *P = S->P, mask = S->mask;
    // cross budgets
    for (int L = 0; L < N; L++) S->cL[L] = S->bL[L] = 0;
    for (int L = 2; L < N; L++) {
        int zc = (Q[L] < 2) + (P[L] < 2);
        int s0 = (Q[L] == P[L]) ? 0 : alpha[L] * (alpha[Q[L]] - alpha[P[L]]);
        int inPs = (mask >> L) & 1, so = -4 - s0 + 2 * inPs, n = 4 - zc;
        if (((n + so) & 1) || n + so < 0 || n - so < 0) return 0;
        S->cL[L] = (n + so) / 2; S->bL[L] = (n - so) / 2;
    }
    // mixed-pair capacities
    for (int L = 0; L < N; L++) for (int M = 0; M < N; M++) {
        int cap;
        if (L == M) cap = (Q[L] != P[L]) ? 2 : 0;
        else if (P[L] == M) cap = 1 - ((M == (L ^ 1)) ? 1 : 0);
        else cap = 2 - ((M == (L ^ 1)) ? 1 : 0) - (P[Q[L]] == M) - (Q[P[L]] == M);
        S->cap[L][M] = cap;
    }
    // V's usage of mixed pairs and O_0+ pairs
    S->vpair_id = S->spair_id = -1;
    if (withV) {
    int vplus[2], vminus[2], nvp = 0, nvm = 0;   // v's + incidences (alpha=-1 labels), - incidences (alpha=+1)
    for (int L = 2; L < N; L++) if ((mask >> L) & 1) { if (alpha[L] == -1) vplus[nvp++] = L; else vminus[nvm++] = L; }
    if (nvp != 2 || nvm != 2) return 0;
    for (int i = 0; i < 2; i++) for (int j = 0; j < 2; j++) { S->cap[vplus[i]][vminus[j]]--; S->cap[vminus[j]][vplus[i]]--; }
    S->vpair_id = (vplus[0] < vplus[1]) ? vplus[0] * N + vplus[1] : vplus[1] * N + vplus[0];
    S->spair_id = (vminus[0] < vminus[1]) ? vminus[0] * N + vminus[1] : vminus[1] * N + vminus[0];
    }
    for (int L = 0; L < N; L++) for (int M = 0; M < N; M++) if (S->cap[L][M] < 0) return 0;
    // V column
    for (int L = 0; L < N; L++) { int t = ((mask >> L) & 1) ? -alpha[L] : 0; int rr = (xof[L] == 5 || xof[L] == 6) ? sof[L] : 0; S->mV[L] = -4 * t - rr; }
    for (int i = 0; i < N; i++) { S->vVd[i] = 0; u64 s = 0; for (int j = 0; j < N; j++) { S->vVd[i] += S->Ad[i][j] * S->mV[j];
        s = (S->mV[j] >= 0) ? addm(s, mulm(S->Am[i][j], (u64)S->mV[j])) : subm(s, mulm(S->Am[i][j], (u64)(-S->mV[j]))); } S->vVm[i] = s; }
    int cF[N]; for (int i = 0; i < N; i++) cF[i] = 28 * alpha[i];
    S->RVV = 10.0 - dotd(S->mV, S->vVd); S->RVVm = subm(10, dotm(S->mV, S->vVm));
    S->RFV = 56.0 - dotd(cF, S->vVd); S->RFVm = subm(56, dotm(cF, S->vVm));
    if (withV && (S->RVV < -1e-9 || S->RFV * S->RFV > S->RFF * S->RVV + 1e-7)) return 0;
    // Z roots: star(1) slots left after Z-Z edges, and star(0) h-sums
    // Z root r (0:+z1 1:-z1 2:+z2 3:-z2) = sign*0rep(Lz); its star(0) nbrs: sign*0rep(Q[Lz]) and -sign*0rep(P[Lz])
    for (int r = 0; r < 4; r++) {
        int Lz = (r < 2) ? 0 : 1, sg = (r % 2 == 0) ? 1 : -1;
        int nb[2][2] = {{Q[Lz], sg}, {P[Lz], -sg}};
        S->zsQ[r] = 1; S->zsP[r] = 1; S->zh[r] = 0;
        for (int t = 0; t < 2; t++) { int L = nb[t][0], s = nb[t][1];
            if (L < 2) { int r2 = zroot_of(L, s); if (zside[r2] == zside[r]) S->zsQ[r]--; else S->zsP[r]--; }
            else S->zh[r] += s * alpha[L]; }
        if (S->zsQ[r] < 0 || S->zsP[r] < 0) return 0;
    }
    // candidates
    for (int y = 0; y < NY; y++) {
        int n = 0; Cand *arr = S->cand[y];
        int innS = withV && (xY[y] == 5 || xY[y] == 6) && (aY[y] * sY[y] == -1), innV = withV && (xY[y] == 5 || xY[y] == 6) && (aY[y] * sY[y] == 1);
        int rY[N];
        for (int L = 0; L < N; L++) rY[L] = (L == 0) ? aY[y] : (L == 1) ? -aY[y] : ((xof[L] == xY[y]) ? aY[y] * sY[y] * sof[L] : 0);
        for (int L1 = 0; L1 < N; L1++) for (int L2 = L1 + 1; L2 < N; L2++) {
            if (Q[L1] == L2) continue; int pp = L1 * N + L2; if (pp == S->vpair_id || pp == S->spair_id) continue;
            for (int L3 = 0; L3 < N; L3++) for (int L4 = L3 + 1; L4 < N; L4++) {
                if (Q[L3] == L4) continue; int pm = L3 * N + L4; if (pm == S->vpair_id || pm == S->spair_id || pm == pp) continue;
                int inc[4] = {L1, L2, L3, L4}, sg[4] = {1, 1, -1, -1};
                int zinc = 0; for (int t = 0; t < 4; t++) zinc += inc[t] < 2;
                if (zinc > 2) continue;
                int so = alpha[L1] + alpha[L2] - alpha[L3] - alpha[L4];
                // Z partners of Y: Z root adjacent to p_Y = sg*0rep(L); its 1-side vs aY decides Q/Pi type
                int zq = 0, zp = 0, zr[4], nz = 0;
                for (int t = 0; t < 4; t++) if (inc[t] < 2) { int r = zroot_of(inc[t], sg[t]); if (zside[r] == aY[y]) zq++; else zp++; zr[nz++] = r; }
                if (zq > 1 || zp > 1) continue;
                int psm = 0;
                for (int ps = 0; ps < 1 + withV; ps++) {
                    int ok = 0;
                    if (zinc == 2) ok = (so == -2 && ps);
                    else if (zinc == 1) ok = (so == -3) || (so == -1 && ps);
                    else ok = (so == -4) || (so == -2) || (so == 0 && ps);
                    if (ok) psm |= 1 << ps;
                }
                if (!psm) continue;
                // budgets
                signed char nC[N], nB[N]; memset(nC, 0, sizeof nC); memset(nB, 0, sizeof nB); int bad = 0;
                for (int t = 0; t < 4; t++) { int L = inc[t]; if (L < 2) continue; if (sg[t] * alpha[L] == 1) nC[L]++; else nB[L]++; }
                for (int L = 2; L < N; L++) if (nC[L] > S->cL[L] || nB[L] > S->bL[L]) bad = 1;
                if (bad) continue;
                // star(0) lambda/mu
                for (int L = 0; L < N && !bad; L++) for (int eps = -1; eps <= 1 && !bad; eps += 2) {
                    int isinc = 0; for (int t = 0; t < 4; t++) if (inc[t] == L && sg[t] == eps) isinc = 1;
                    int cc = 0; for (int t = 0; t < 4; t++) { if (inc[t] == Q[L] && sg[t] == eps) cc++; if (inc[t] == P[L] && sg[t] == -eps) cc++; }
                    int sh = shared_inner_root(y, L, eps);
                    if (isinc) { if (cc + sh > 1) bad = 1; } else { if (cc + sh > 2) bad = 1; }
                }
                if (bad) continue;
                { int side[2] = {0, 0};
                  for (int t = 0; t < 4; t++) { int L = inc[t]; if (L < 2 || xof[L] != xY[y]) continue; int xs = sg[t] * sof[L]; side[xs > 0]++; }
                  if (side[0] > 1 || side[1] > 1) continue; }
                // mixed-pair capacities (own use)
                unsigned char add[N][N]; memset(add, 0, sizeof add);
                for (int i = 0; i < 2; i++) for (int j = 2; j < 4; j++) { add[inc[i]][inc[j]]++; add[inc[j]][inc[i]]++; }
                for (int i = 0; i < N && !bad; i++) for (int j = 0; j < N; j++) if (add[i][j] > S->cap[i][j]) { bad = 1; break; }
                if (bad) continue;
                // lambda/mu with sigma v, v in star(0)
                int cs = 0, cv = 0;
                for (int t = 0; t < 4; t++) { int L = inc[t]; if (L < 2 || !((mask >> L) & 1)) continue; if (sg[t] * alpha[L] == 1) cs++; else cv++; }
                if (cv + innV > 2) continue;
                int psm2 = 0;
                for (int ps = 0; ps < 2; ps++) if ((psm >> ps) & 1) { if (ps) { if (cs + innS <= 1) psm2 |= 2; } else { if (cs + innS <= 2) psm2 |= 1; } }
                if (!psm2) continue;
                // residual quantities
                Cand c; memset(&c, 0, sizeof c);
                c.L[0] = L1; c.L[1] = L2; c.L[2] = L3; c.L[3] = L4;
                int t0[N]; memset(t0, 0, sizeof t0); t0[L1]++; t0[L2]++; t0[L3]--; t0[L4]--;
                for (int L = 0; L < N; L++) c.m[L] = -4 * t0[L] - rY[L];
                for (int i = 0; i < N; i++) { double s = 0; u64 sm_ = 0;
                    for (int j = 0; j < N; j++) { s += S->Ad[i][j] * c.m[j];
                        sm_ = (c.m[j] >= 0) ? addm(sm_, mulm(S->Am[i][j], (u64)c.m[j])) : subm(sm_, mulm(S->Am[i][j], (u64)(-c.m[j]))); }
                    c.vd[i] = s; c.vm[i] = sm_; }
                c.sd = 10.0 - dotd(c.m, c.vd); c.sm = subm(10, dotm(c.m, c.vm));
                if (c.sd < -1e-9) continue;
                c.fd = 28.0 - dotd(cF, c.vd); c.fm = subm(28, dotm(cF, c.vm));
                int rv = rVdot(y);
                c.v0d = -rv - dotd(S->mV, c.vd); c.v0m = subm(tom(-rv), dotm(S->mV, c.vm));
                // 3x3 {F, V, Y} PSD per ps
                int psm3 = 0;
                for (int ps = 0; ps < 2; ps++) if ((psm2 >> ps) & 1) {
                    if (!withV) { if (S->RFF * c.sd - c.fd * c.fd < -1e-6 * (1.0 + S->RFF * c.sd)) continue; psm3 |= 1; continue; }
                    double g = c.v0d + 4.0 * ps;   // -4*T_VY with T_VY = -ps
                    double G[3][3] = {{S->RFF, S->RFV, c.fd}, {S->RFV, S->RVV, g}, {c.fd, g, c.sd}};
                    double det = G[0][0] * (G[1][1] * G[2][2] - G[1][2] * G[2][1]) - G[0][1] * (G[1][0] * G[2][2] - G[1][2] * G[2][0]) + G[0][2] * (G[1][0] * G[2][1] - G[1][1] * G[2][0]);
                    double m2 = G[0][0] * G[1][1] - G[0][1] * G[0][1], m3 = G[0][0] * G[2][2] - G[0][2] * G[0][2], m4 = G[1][1] * G[2][2] - G[1][2] * G[1][2];
                    if (m2 < -1e-6 || m3 < -1e-6 || m4 < -1e-6 || det < -1e-4) continue;
                    psm3 |= 1 << ps;
                }
                if (!psm3) continue;
                c.psmask = psm3; c.zinc = zinc; c.zq = zq; c.zp = zp; c.so = so;
                c.pairP = pp; c.pairM = pm;
                for (int L = 0; L < N; L++) { c.needC[L] = nC[L]; c.needB[L] = nB[L]; }
                // Z root adjacency: p_Y ~ sg*0rep(L): Z root index r, root_sign +1 (p_Y) ; -p_Y ~ -sg*0rep(L): root -r, root sign -1
                c.nz = 0;
                for (int t = 0; t < 4; t++) if (inc[t] < 2) {
                    int r = zroot_of(inc[t], sg[t]); c.zroot[c.nz++] = r;               // p_Y adjacent to Z root r
                    int r2 = zroot_of(inc[t], -sg[t]); c.zroot[c.nz++] = r2 | 4;        // -p_Y adjacent to Z root r2
                }
                c.dent = -1; for (int i = 0; i < 2; i++) for (int j = 2; j < 4; j++) if (inc[i] == inc[j]) c.dent = inc[i];
                if (n >= 2000) { fprintf(stderr, "too many candidates\n"); exit(4); }
                arr[n++] = c;
            }
        }
        S->ncand[y] = n;
        if (n == 0) return 0;
    }
    return 1;
}
static int run_search(Str *S, FILE *fp, long long *nodes) {
    St st; memset(&st, 0, sizeof st);
    for (int r = 0; r < 4; r++) { st.zQ[r] = S->zsQ[r]; st.zP[r] = S->zsP[r]; }
    if (withV) { st.pairused[S->vpair_id] = 1; st.pairused[S->spair_id] = 1; }
    // V's mixed-pair usage already subtracted from capacities in build()
    st.k = 0; st.ndep = 0; st.fl_ok = 1;
    for (int sid = -2; sid <= (withV ? -1 : -2); sid++) {
        u64 gm[4]; double gd[4]; u64 coef[4];
        for (int i = 0; i < st.k; i++) ip_basis(S, &st, sid, st.bid[i], &gd[i], &gm[i]);
        double sd; u64 sm; ip_basis(S, &st, sid, sid, &sd, &sm);
        int r = res_test(&st, gm, gd, sm, sd, coef);
        if (!r) { *nodes = 0; return 0; }
        if (r == 1) {
            for (int t = 0; t < st.ndep; t++) { double dd; u64 mm; ip_basis(S, &st, sid, st.did[t], &dd, &mm);
                u64 pred = 0; for (int i = 0; i < st.k; i++) pred = addm(pred, mulm(st.dco[t][i], gm[i]));
                if (pred != mm) { *nodes = 0; return 0; } }
            st.did[st.ndep] = sid; for (int i = 0; i < st.k; i++) st.dco[st.ndep][i] = coef[i]; st.ndep++;
        } else { st.bid[st.k++] = sid; basis_refresh(S, &st); for (int t = 0; t < st.ndep; t++) st.dco[t][st.k - 1] = 0; }
    }
    long long before = g_nodes;
    dfs(S, &st, fp);
    *nodes = g_nodes - before;
    return 0;
}
static unsigned long long rs = 88172645463325252ULL;
static unsigned rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
// star-level P_sigma admissibility (same as star0_count.c)
static int psigma_ok(const Str *S, int mask, int forced) {
    const int *Q = S->Q, *P = S->P;
    if ((forced & mask) != forced) return 0;
    int vp[2], vm[2], a = 0, b = 0;
    for (int L = 2; L < N; L++) if ((mask >> L) & 1) { if (alpha[L] == -1) vp[a++] = L; else vm[b++] = L; }
    if (a != 2 || b != 2) return 0;
    if (Q[vp[0]] == vp[1] || Q[vm[0]] == vm[1]) return 0;
    for (int L = 2; L < N; L++) {
        int inPs = (mask >> L) & 1, cs = 0, cv = 0, ql = Q[L], pl = P[L];
        if (ql >= 2 && ((mask >> ql) & 1)) { if (alpha[ql] == alpha[L]) cs++; else cv++; }
        if (pl >= 2 && ((mask >> pl) & 1)) { if (alpha[pl] == -alpha[L]) cs++; else cv++; }
        int x = xof[L], s = sof[L];
        int innS = (x == 5 || x == 6) && (alpha[L] * s == -1), innV = (x == 5 || x == 6) && (alpha[L] * s == 1);
        if (inPs) { if (cs + innS > 1) return 0; } else { if (cs + innS > 2) return 0; }
        if (cv + innV > 2) return 0;
    }
    return 1;
}
static int forced_of(const int *Q, const int *P, int *bad) {
    int forced = 0, fp = 0, fm = 0;
    for (int L = 2; L < N; L++) {
        int zc = (Q[L] < 2) + (P[L] < 2);
        int s0 = (Q[L] == P[L]) ? 0 : alpha[L] * (alpha[Q[L]] - alpha[P[L]]);
        if ((zc == 2) || (zc == 1 && s0 == 1) || (zc == 0 && s0 == 2)) { forced |= 1 << L; if (alpha[L] == 1) fp++; else fm++; }
    }
    *bad = (fp > 2 || fm > 2);
    return forced;
}
static double q_of(const Str *S) { double q = 0; for (int i = 0; i < N; i++) q += alpha[i] * S->vFd[i] / 28.0; return q; }
// even V-test (star level)
static int even_v_ok(const Str *S, int mask) {
    const int *Q = S->Q, *P = S->P;
    int comp[N]; for (int i = 0; i < N; i++) comp[i] = -1; int nc = 0;
    for (int s = 0; s < N; s++) if (comp[s] < 0) { int stk[N], sp = 0; stk[sp++] = s; comp[s] = nc;
        while (sp) { int u = stk[--sp]; int nb[3] = {Q[u], P[u], u ^ 1}; for (int t = 0; t < 3; t++) if (comp[nb[t]] < 0) { comp[nb[t]] = nc; stk[sp++] = nb[t]; } } nc++; }
    double mE[N]; for (int L = 0; L < N; L++) mE[L] = -2.0 * ((mask >> L) & 1) - ((xof[L] == 5 || xof[L] == 6) ? 1.0 : 0.0) + 1.0;
    for (int c = 0; c < nc; c++) { double s = 0; for (int L = 0; L < N; L++) if (comp[L] == c) s += mE[L]; if (fabs(s) > 1e-9) return 0; }
    double Ae[N][N], Aep[N][N];
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++)
        Ae[i][j] = (i == j ? 5.0 : 0.0) - ((xof[i] == xof[j] && i != j) ? 1.0 : 0.0) - 2.0 * ((Q[i] == j) + (P[i] == j)) + (comp[i] == comp[j] ? 1.0 : 0.0);
    if (!chol_inv_d(Ae, Aep)) return 1;
    double q = 0; for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) q += mE[i] * Aep[i][j] * mE[j];
    return 5.0 - q >= -1e-9;
}
// canonical under the symmetry permutations (each perm maps star(0) labels; Q,P conjugated, mask mapped)
static int is_canonical(const int *Q, const int *P, int mask) {
    for (int g = 0; g < nsym; g++) {
        const int *pm = symperm[g];
        int Q2[N], P2[N], m2 = 0;
        for (int L = 0; L < N; L++) { Q2[pm[L]] = pm[Q[L]]; P2[pm[L]] = pm[P[L]]; if ((mask >> L) & 1) m2 |= 1 << pm[L]; }
        // lexicographic compare (Q, P, mask)
        int cmp = 0;
        for (int i = 0; i < N && !cmp; i++) if (Q2[i] != Q[i]) cmp = Q2[i] < Q[i] ? -1 : 1;
        for (int i = 0; i < N && !cmp; i++) if (P2[i] != P[i]) cmp = P2[i] < P[i] ? -1 : 1;
        if (!cmp && m2 != mask) cmp = m2 < mask ? -1 : 1;
        if (cmp < 0) return 0;
    }
    return 1;
}
int main(int argc, char **argv) {
    int a42[42]; for (int i = 0; i < 42; i++) a42[i] = atoi(argv[1 + i]);
    const char *symf = argv[43]; withV = atoi(argv[44]); asq = withV ? 24 : 20; const char *mode = argv[45]; argv += 1;
    int gidx[7][7]; int k = 0; for (int i = 0; i < 7; i++) for (int j = i + 1; j < 7; j++) { gidx[i][j] = k; k += 2; }
    for (int L = 0; L < N; L++) { xof[L] = (L < 2) ? 1 : 2 + (L - 2) / 2; sof[L] = (L % 2 == 0) ? 1 : -1;
        alpha[L] = (L < 2) ? 0 : a42[gidx[0][xof[L]] + (sof[L] == 1 ? 0 : 1)]; }
    for (int y = 0; y < NY; y++) { xY[y] = 2 + y / 2; sY[y] = (y % 2 == 0) ? 1 : -1; aY[y] = a42[gidx[1][xY[y]] + (sY[y] == 1 ? 0 : 1)]; }
    { FILE *f = fopen(symf, "r"); if (f) { while (nsym < 256) { int ok = 1; for (int i = 0; i < N; i++) if (fscanf(f, "%d", &symperm[nsym][i]) != 1) { ok = 0; break; } if (!ok) break; nsym++; } fclose(f); } }
    int p[N], used[N]; memset(used, 0, sizeof used); gen_inv(p, used);
    if (!strcmp(mode, "sample")) {
        int ns = atoi(argv[45]); rs ^= (unsigned long long)atoll(argv[46]) * 2654435761ULL;
        Str *S = (Str *)calloc(1, sizeof(Str)); for (int y = 0; y < NY; y++) S->cand[y] = (Cand *)malloc(2000 * sizeof(Cand));
        int got = 0; double tsum = 0; long long nsum = 0, tot_surv = 0; long long zerocand = 0;
        while (got < ns) {
            int *Q = inv[rnd() % ninv], *P = inv[rnd() % ninv]; int bad; int forced = forced_of(Q, P, &bad); if (bad) continue;
            int r = star_prepare(S, Q, P); if (r != 1) continue;
            if (q_of(S) > asq / 28.0 + 1e-9) continue;
            int masks[100], nm = 0;
            if (!withV) { if (forced == 0) masks[nm++] = 0; }
            else {
            int pl[5], mi[5], a = 0, b = 0; for (int L = 2; L < N; L++) { if (alpha[L] == 1) pl[a++] = L; else mi[b++] = L; }
            for (int a1 = 0; a1 < 5; a1++) for (int a2 = a1 + 1; a2 < 5; a2++) for (int b1 = 0; b1 < 5; b1++) for (int b2 = b1 + 1; b2 < 5; b2++) {
                int mask = (1 << pl[a1]) | (1 << pl[a2]) | (1 << mi[b1]) | (1 << mi[b2]);
                if (psigma_ok(S, mask, forced) && even_v_ok(S, mask)) masks[nm++] = mask; } }
            if (!nm) continue;
            S->mask = masks[rnd() % nm];
            clock_t t0 = clock();
            if (!build(S)) { zerocand++; continue; }
            long long nodes; long long sb = g_surv; run_search(S, stdout, &nodes);
            double dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
            tsum += dt; nsum += nodes; tot_surv += g_surv - sb; got++;
            if (got <= 20 || got % 50 == 0) { printf("sample %d: ncand", got); for (int y = 0; y < NY; y++) printf(" %d", S->ncand[y]); printf("  nodes %lld  time %.3f s  surv %lld\n", nodes, dt, g_surv - sb); fflush(stdout); }
        }
        printf("SUMMARY samples %d  build-dead %lld  mean time %.4f s  mean nodes %.0f  survivors %lld\n", got, zerocand, tsum / got, (double)nsum / got, tot_surv);
        return 0;
    }
    if (!strcmp(mode, "full")) {
        const char *outf = argv[45]; int nth = atoi(argv[46]);
        FILE *fo = fopen(outf, "w");
#ifdef _OPENMP
        omp_set_num_threads(nth);
#endif
        long long cnt_s0 = 0, cnt_pairs = 0, cnt_searched = 0, cnt_build_dead = 0; long long done = 0;
        time_t t0 = time(NULL);
        #pragma omp parallel reduction(+:cnt_s0,cnt_pairs,cnt_searched,cnt_build_dead)
        {
            Str *S = (Str *)calloc(1, sizeof(Str)); for (int y = 0; y < NY; y++) S->cand[y] = (Cand *)malloc(2000 * sizeof(Cand));
            #pragma omp for schedule(dynamic, 1)
            for (int qi = 0; qi < ninv; qi++) {
                for (int pi = 0; pi < ninv; pi++) {
                    int *Q = inv[qi], *P = inv[pi]; int bad; int forced = forced_of(Q, P, &bad); if (bad) continue;
                    int r = star_prepare(S, Q, P);
                    if (r == -1) { fprintf(stderr, "SINGULAR MOD P at qi=%d pi=%d\n", qi, pi); exit(5); }
                    if (r != 1) continue;
                    if (q_of(S) > asq / 28.0 + 1e-9) continue;
                    cnt_s0++;
                    int pl[5], mi[5], a = 0, b = 0; for (int L = 2; L < N; L++) { if (alpha[L] == 1) pl[a++] = L; else mi[b++] = L; }
                    int nmask = withV ? 100 : 1;
                    for (int mi_ = 0; mi_ < nmask; mi_++) {
                        int mask = 0;
                        if (withV) { int a1, a2, b1, b2, t = mi_; int ab = t / 10, bb = t % 10; int cnt = 0;
                            a1 = a2 = b1 = b2 = -1;
                            for (int u = 0; u < 5; u++) for (int v = u + 1; v < 5; v++) { if (cnt == ab) { a1 = u; a2 = v; } if (cnt == bb) { b1 = u; b2 = v; } cnt++; }
                            mask = (1 << pl[a1]) | (1 << pl[a2]) | (1 << mi[b1]) | (1 << mi[b2]);
                            if (!psigma_ok(S, mask, forced)) continue;
                            if (!even_v_ok(S, mask)) continue; }
                        else { if (forced) continue; }
                        if (!is_canonical(Q, P, mask)) continue;
                        cnt_pairs++;
                        S->mask = mask;
                        if (!build(S)) { cnt_build_dead++; continue; }
                        long long nodes; run_search(S, fo, &nodes); cnt_searched++;
                    }
                }
                #pragma omp atomic
                done++;
                if (omp_get_thread_num() == 0) { fprintf(stderr, "\rQ0 done %lld/%d  elapsed %ld s  surv %lld   ", done, ninv, (long)(time(NULL) - t0), g_surv); fflush(stderr); }
            }
        }
        fclose(fo);
        printf("DONE  S0 (a-test) %lld  canonical (S0,Psigma) %lld  build-dead %lld  searched %lld  survivors %lld  nodes %lld  time %ld s\n",
               cnt_s0, cnt_pairs, cnt_build_dead, cnt_searched, g_surv, g_nodes, (long)(time(NULL) - t0));
        return 0;
    }
    return 0;
}
