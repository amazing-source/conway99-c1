// cut25.c (C1, 28/09 evening): exhaustive search for the 2|5 cut cells R5 (20 x +-1, no V) and J2 (+ one +2 on V=(5,6,+)).
// Optimised successor of j2_engine.c (same model and tests, notes/154), with:
//   - per-depth forward-checked candidate lists (combinatorial), label with the fewest candidates first;
//   - exact cut0 quotas per label L: C/B budgets (eigen-equation) AND the star(1) side split (L0 for star(1));
//   - side-sum identities: sum_{Y in side s} rho_Y = (F_perp - 2 rho_V)/2 (from sum_{star1} f = 0 and F = sum a f), used as a
//     knapsack bound on the F-component and checked exactly (mod p) at the end;
//   - residual Gram of F, V, cut1 labels over span f_star0: rank <= 4 EXACT mod p = 2^31-1, PSD float (robust margin).
// Every test is a necessary condition. Survivors (if any) are written for exact verification.
// Usage: cut25 <a: 42 ints> <symfile> <withV> list <outfile>            (canonical star-level survivors, OpenMP)
//        cut25 <a: 42 ints> <symfile> <withV> run <listfile> <outfile> <nthreads> [first last]
//        cut25 <a: 42 ints> <symfile> <withV> sample <N> <seed>
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
#define MAXC 2500
#define PR 2147483647ULL
typedef unsigned long long u64;
static inline u64 redm(u64 x) { x = (x & PR) + (x >> 31); x = (x & PR) + (x >> 31); return x >= PR ? x - PR : x; }  // Mersenne 2^31-1
static inline u64 mulm(u64 a, u64 b) { return redm(a * b); }
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
static int alpha[N], xof[N], sof[N], aY[NY], xY[NY], sY[NY];
static int withV = 0, asq = 20;
static int nsym = 0; static int symperm[4096][N];
static const int zside[4] = {1, -1, -1, 1};          // Z roots: 0:+z1(e0+e1) 1:-z1 2:+z2(e0-e1) 3:-z2 ; their 1-sides
static inline int zroot_of(int L, int eps) { return (L == 0) ? (eps > 0 ? 0 : 1) : (eps > 0 ? 2 : 3); }
static inline int pYdot(int y, int z) { return aY[y] * aY[z] * (1 + ((xY[y] == xY[z]) ? sY[y] * sY[z] : 0)); }
static inline int rVdot(int y) { return (xY[y] == 5 || xY[y] == 6) ? aY[y] * sY[y] : 0; }

typedef struct {
    int L[4];
    int m[N]; double vd[N]; u64 vm[N];
    double sd, fd, v0d; u64 sm, fm, v0m;
    int psmask, zinc, zq, zp, so, dent;
    int pairP, pairM;
    int nq; int qL[4], qcb[4], qsd[4];
    int ma[8], mb[8];
    int nz; int zr[4];
    int inc_sg[4];
    int xc[2];
} Cand;
typedef struct {
    int Q[N], P[N], mask;
    int cL[N], bL[N], sP[N], sM[N];
    int cap[N][N];
    int vpair_id, spair_id;
    double Ad[N][N]; u64 Am[N][N];
    double vFd[N]; u64 vFm[N]; int mV[N]; double vVd[N]; u64 vVm[N];
    double RFF, RFV, RVV; u64 RFFm, RFVm, RVVm;
    int zsQ[4], zsP[4], zh[4];
    double phimin[NY], phimax[NY];
    int x0[N][2][2];
    int X0[N][2][5][2];
    Cand *cand[NY]; int ncand[NY];
} Str;
static int chol_inv_d(double A[N][N], double Ainv[N][N]) {
    double L[N][N]; memset(L, 0, sizeof L);
    for (int j = 0; j < N; j++) {
        double s = A[j][j]; for (int k = 0; k < j; k++) s -= L[j][k] * L[j][k];
        if (s <= 1e-12) return 0;
        L[j][j] = sqrt(s);
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
static inline u64 dotm(const int *m, const u64 *v) { u64 p = 0, q = 0; for (int i = 0; i < N; i++) { if (m[i] > 0) p += (u64)m[i] * v[i]; else if (m[i] < 0) q += (u64)(-m[i]) * v[i]; } return subm(redm(p), redm(q)); }
static void matvec(const Str *S, const int *m, double *vd, u64 *vm) {
    for (int i = 0; i < N; i++) { double s = 0; u64 t = 0;
        for (int j = 0; j < N; j++) { if (!m[j]) continue; s += S->Ad[i][j] * m[j];
            t = (m[j] > 0) ? addm(t, mulm(S->Am[i][j], (u64)m[j])) : subm(t, mulm(S->Am[i][j], (u64)(-m[j]))); }
        vd[i] = s; vm[i] = t; }
}
// ---------- star level ----------
static int profile_forced(const int *Q, const int *P, int *bad) {
    int forced = 0, fp = 0, fm = 0; *bad = 0;
    for (int L = 2; L < N; L++) {
        int zc = (Q[L] < 2) + (P[L] < 2);
        int s0 = (Q[L] == P[L]) ? 0 : alpha[L] * (alpha[Q[L]] - alpha[P[L]]);
        int f = (zc == 2) || (zc == 1 && s0 == 1) || (zc == 0 && s0 == 2);
        if (f) { forced |= 1 << L; if (alpha[L] == 1) fp++; else fm++; }
    }
    if (!withV) { if (forced) *bad = 1; }
    else if (fp > 2 || fm > 2) *bad = 1;
    return forced;
}
static int star_prepare(Str *S, const int *Q, const int *P) {
    memcpy(S->Q, Q, sizeof(int) * N); memcpy(S->P, P, sizeof(int) * N);
    int T[N][N]; memset(T, 0, sizeof T);
    for (int L = 0; L < N; L++) { T[L][Q[L]] += 1; T[L][P[L]] -= 1; }
    double A[N][N]; long long Ai[N][N];
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) { Ai[i][j] = (i == j ? 11 : 0) + ((xof[i] == xof[j] && i != j) ? 1 : 0) - 4 * T[i][j]; A[i][j] = (double)Ai[i][j]; }
    if (!chol_inv_d(A, S->Ad)) return 0;
    if (!inv_mod(Ai, S->Am)) return -1;
    int cF[N]; for (int i = 0; i < N; i++) cF[i] = 28 * alpha[i];
    matvec(S, cF, S->vFd, S->vFm);
    S->RFF = 28.0 * asq - dotd(cF, S->vFd); S->RFFm = subm((u64)(28 * asq), dotm(cF, S->vFm));
    return 1;
}
static double qval(const Str *S) { double q = 0; for (int i = 0; i < N; i++) q += alpha[i] * S->vFd[i]; return q / 28.0; }
static int psigma_ok(const Str *S, int mask, int forced) {
    const int *Q = S->Q, *P = S->P;
    if ((forced & mask) != forced) return 0;
    int vp[2], vm[2], a = 0, b = 0;
    for (int L = 2; L < N; L++) if ((mask >> L) & 1) { if (alpha[L] == -1) { if (a < 2) vp[a] = L; a++; } else { if (b < 2) vm[b] = L; b++; } }
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
static int v_odd_ok(Str *S, int mask) {
    for (int L = 0; L < N; L++) { int t = ((mask >> L) & 1) ? -alpha[L] : 0; int rr = (xof[L] == 5 || xof[L] == 6) ? sof[L] : 0; S->mV[L] = -4 * t - rr; }
    matvec(S, S->mV, S->vVd, S->vVm);
    int cF[N]; for (int i = 0; i < N; i++) cF[i] = 28 * alpha[i];
    S->RVV = 10.0 - dotd(S->mV, S->vVd); S->RVVm = subm(10, dotm(S->mV, S->vVm));
    S->RFV = 56.0 - dotd(cF, S->vVd); S->RFVm = subm(56, dotm(cF, S->vVm));
    return !(S->RVV < -1e-9 || S->RFV * S->RFV > S->RFF * S->RVV + 1e-7);
}
static int is_canonical(const int *Q, const int *P, int mask) {
    for (int g = 0; g < nsym; g++) {
        const int *pm = symperm[g]; int Q2[N], P2[N], m2 = 0;
        for (int L = 0; L < N; L++) { Q2[pm[L]] = pm[Q[L]]; P2[pm[L]] = pm[P[L]]; if ((mask >> L) & 1) m2 |= 1 << pm[L]; }
        int cmp = 0;
        for (int i = 0; i < N && !cmp; i++) if (Q2[i] != Q[i]) cmp = Q2[i] < Q[i] ? -1 : 1;
        for (int i = 0; i < N && !cmp; i++) if (P2[i] != P[i]) cmp = P2[i] < P[i] ? -1 : 1;
        if (!cmp && m2 != mask) cmp = m2 < mask ? -1 : 1;
        if (cmp < 0) return 0;
    }
    return 1;
}
// ---------- build the cut1 candidates ----------
static inline int shared_inner_root(int y, int L, int eps) {
    if (L < 2) return (eps * (L == 0 ? 1 : -1)) == aY[y];
    return (xof[L] == xY[y] && eps * sof[L] == aY[y] * sY[y]);
}
static int build(Str *S) {
    int *Q = S->Q, *P = S->P, mask = S->mask;
    for (int L = 0; L < N; L++) S->cL[L] = S->bL[L] = S->sP[L] = S->sM[L] = 0;
    for (int L = 2; L < N; L++) {
        int zc = (Q[L] < 2) + (P[L] < 2);
        int s0 = (Q[L] == P[L]) ? 0 : alpha[L] * (alpha[Q[L]] - alpha[P[L]]);
        int inPs = (mask >> L) & 1, so = -4 - s0 + 2 * inPs, n = 4 - zc;
        if (((n + so) & 1) || n + so < 0 || n - so < 0) return 0;
        S->cL[L] = (n + so) / 2; S->bL[L] = (n - so) / 2;
        // star(1) side split for 0rep(L): 2 nbrs in O_1+ and 2 in O_1-, minus its Z nbrs (via star(0)) on each side
        int zp = 0, zm = 0;
        if (Q[L] < 2) { int r = zroot_of(Q[L], +1); if (zside[r] > 0) zp++; else zm++; }
        if (P[L] < 2) { int r = zroot_of(P[L], -1); if (zside[r] > 0) zp++; else zm++; }
        S->sP[L] = 2 - zp; S->sM[L] = 2 - zm;
        if (S->sP[L] < 0 || S->sM[L] < 0) return 0;
    }
    for (int L = 0; L < N; L++) for (int M = 0; M < N; M++) {
        int cap;
        if (L == M) cap = (Q[L] != P[L]) ? 2 : 0;
        else if (P[L] == M) cap = 1 - ((M == (L ^ 1)) ? 1 : 0);
        else cap = 2 - ((M == (L ^ 1)) ? 1 : 0) - (P[Q[L]] == M) - (Q[P[L]] == M);
        S->cap[L][M] = cap;
    }
    S->vpair_id = S->spair_id = -1;
    if (withV) {
        int vplus[2], vminus[2], nvp = 0, nvm = 0;
        for (int L = 2; L < N; L++) if ((mask >> L) & 1) { if (alpha[L] == -1) vplus[nvp++] = L; else vminus[nvm++] = L; }
        for (int i = 0; i < 2; i++) for (int j = 0; j < 2; j++) { S->cap[vplus[i]][vminus[j]]--; S->cap[vminus[j]][vplus[i]]--; }
        S->vpair_id = (vplus[0] < vplus[1]) ? vplus[0] * N + vplus[1] : vplus[1] * N + vplus[0];
        S->spair_id = (vminus[0] < vminus[1]) ? vminus[0] * N + vminus[1] : vminus[1] * N + vminus[0];
    }
    for (int L = 0; L < N; L++) for (int M = 0; M < N; M++) if (S->cap[L][M] < 0) return 0;
    for (int r = 0; r < 4; r++) {
        int Lz = (r < 2) ? 0 : 1, sg = (r % 2 == 0) ? 1 : -1;
        int nb[2][2] = {{Q[Lz], sg}, {P[Lz], -sg}};
        S->zsQ[r] = 1; S->zsP[r] = 1; S->zh[r] = 0;
        for (int t = 0; t < 2; t++) { int L = nb[t][0], s = nb[t][1];
            if (L < 2) { int r2 = zroot_of(L, s); if (zside[r2] == zside[r]) S->zsQ[r]--; else S->zsP[r]--; }
            else S->zh[r] += s * alpha[L]; }
        if (S->zsQ[r] < 0 || S->zsP[r] < 0) return 0;
        { int freeS = S->zsQ[r] + S->zsP[r], d = -S->zh[r]; if (abs(d) > freeS || ((d - freeS) & 1)) return 0; }
    }
    memset(S->x0, 0, sizeof S->x0);
    memset(S->X0, 0, sizeof S->X0);
    for (int L = 2; L < N; L++) for (int e = 0; e < 2; e++) { int eps = e ? -1 : 1;
        int nbL[2] = {Q[L], P[L]}, nbs[2] = {eps, -eps};           // eps*0rep(L) ~ eps*0rep(Q L), ~ -eps*0rep(P L)
        for (int t = 0; t < 2; t++) { int M = nbL[t]; if (M < 2) continue; int xs = nbs[t] * sof[M]; S->X0[L][e][xof[M] - 2][xs > 0 ? 0 : 1]++; } }
    for (int L = 2; L < N; L++) {
        int M = L ^ 1;                                            // same-cell label
        for (int e = 0; e < 2; e++) { int eps = e ? -1 : 1;       // root eps*0rep(L)
            if (Q[L] == M) { int xs = eps * sof[M]; S->x0[L][e][xs > 0 ? 0 : 1]++; }       // eps*0rep(L) ~ eps*0rep(M)
            if (P[L] == M) { int xs = -eps * sof[M]; S->x0[L][e][xs > 0 ? 0 : 1]++; }      // eps*0rep(L) ~ -eps*0rep(M)
        }
    }
    int cF[N]; for (int i = 0; i < N; i++) cF[i] = 28 * alpha[i];
    for (int y = 0; y < NY; y++) {
        int n = 0; Cand *arr = S->cand[y];
        int innS = withV && (xY[y] == 5 || xY[y] == 6) && (aY[y] * sY[y] == -1), innV = withV && (xY[y] == 5 || xY[y] == 6) && (aY[y] * sY[y] == 1);
        int rY[N];
        for (int L = 0; L < N; L++) rY[L] = (L == 0) ? aY[y] : (L == 1) ? -aY[y] : ((xof[L] == xY[y]) ? aY[y] * sY[y] * sof[L] : 0);
        S->phimin[y] = 1e9; S->phimax[y] = -1e9;
        for (int L1 = 0; L1 < N; L1++) for (int L2 = L1 + 1; L2 < N; L2++) {
            if (Q[L1] == L2) continue;
            int pp = L1 * N + L2;
            if (pp == S->vpair_id || pp == S->spair_id) continue;
            for (int L3 = 0; L3 < N; L3++) for (int L4 = L3 + 1; L4 < N; L4++) {
                if (Q[L3] == L4) continue;
                int pm = L3 * N + L4;
                if (pm == S->vpair_id || pm == S->spair_id || pm == pp) continue;
                int inc[4] = {L1, L2, L3, L4}, sg[4] = {1, 1, -1, -1};
                int zinc = 0; for (int t = 0; t < 4; t++) zinc += inc[t] < 2;
                if (zinc > 2) continue;
                int so = alpha[L1] + alpha[L2] - alpha[L3] - alpha[L4];
                int zq = 0, zp = 0;
                for (int t = 0; t < 4; t++) if (inc[t] < 2) { int r = zroot_of(inc[t], sg[t]); if (zside[r] == aY[y]) zq++; else zp++; }
                if (zq > 1 || zp > 1) continue;
                int psm = 0;
                for (int ps = 0; ps < 1 + withV; ps++) {
                    int ok;
                    if (zinc == 2) ok = (so == -2 && ps);
                    else if (zinc == 1) ok = (so == -3) || (so == -1 && ps);
                    else ok = (so == -4) || (so == -2) || (so == 0 && ps);
                    if (ok) psm |= 1 << ps;
                }
                if (!psm) continue;
                // quotas: (C/B) budgets and star(1) side split at each cut0 label
                int nC[N], nB[N], nSp[N], nSm[N], bad = 0;
                memset(nC, 0, sizeof nC); memset(nB, 0, sizeof nB); memset(nSp, 0, sizeof nSp); memset(nSm, 0, sizeof nSm);
                for (int t = 0; t < 4; t++) { int L = inc[t]; if (L < 2) continue;
                    if (sg[t] * alpha[L] == 1) nC[L]++; else nB[L]++;
                    if (sg[t] * aY[y] > 0) nSp[L]++; else nSm[L]++; }
                for (int L = 2; L < N; L++) if (nC[L] > S->cL[L] || nB[L] > S->bL[L] || nSp[L] > S->sP[L] || nSm[L] > S->sM[L]) bad = 1;
                if (bad) continue;
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
                int add[N][N]; memset(add, 0, sizeof add);
                for (int i = 0; i < 2; i++) for (int j = 2; j < 4; j++) { add[inc[i]][inc[j]]++; add[inc[j]][inc[i]]++; }
                for (int i = 0; i < N && !bad; i++) for (int j = 0; j < N; j++) if (add[i][j] > S->cap[i][j]) { bad = 1; break; }
                if (bad) continue;
                int cs = 0, cv = 0;
                for (int t = 0; t < 4; t++) { int L = inc[t]; if (L < 2 || !((mask >> L) & 1)) continue; if (sg[t] * alpha[L] == 1) cs++; else cv++; }
                if (cv + innV > 2) continue;
                int psm2 = 0;
                for (int ps = 0; ps < 2; ps++) if ((psm >> ps) & 1) { if (ps) { if (cs + innS <= 1) psm2 |= 2; } else { if (cs + innS <= 2) psm2 |= 1; } }
                if (!psm2) continue;
                Cand c; memset(&c, 0, sizeof c);
                c.L[0] = L1; c.L[1] = L2; c.L[2] = L3; c.L[3] = L4;
                for (int t = 0; t < 4; t++) c.inc_sg[t] = sg[t];
                int t0[N]; memset(t0, 0, sizeof t0); t0[L1]++; t0[L2]++; t0[L3]--; t0[L4]--;
                for (int L = 0; L < N; L++) c.m[L] = -4 * t0[L] - rY[L];
                matvec(S, c.m, c.vd, c.vm);
                c.sd = 10.0 - dotd(c.m, c.vd); c.sm = subm(10, dotm(c.m, c.vm));
                if (c.sd < -1e-9) continue;
                c.fd = 28.0 - dotd(cF, c.vd); c.fm = subm(28, dotm(cF, c.vm));
                int rv = rVdot(y);
                if (withV) { c.v0d = -rv - dotd(S->mV, c.vd); c.v0m = subm(tom(-rv), dotm(S->mV, c.vm)); }
                int psm3 = 0;
                for (int ps = 0; ps < 2; ps++) if ((psm2 >> ps) & 1) {
                    if (!withV) { if (S->RFF * c.sd - c.fd * c.fd < -1e-6 * (1.0 + S->RFF * c.sd)) continue; psm3 |= 1; continue; }
                    double g = c.v0d + 4.0 * ps;
                    double G[3][3] = {{S->RFF, S->RFV, c.fd}, {S->RFV, S->RVV, g}, {c.fd, g, c.sd}};
                    double det = G[0][0] * (G[1][1] * G[2][2] - G[1][2] * G[2][1]) - G[0][1] * (G[1][0] * G[2][2] - G[1][2] * G[2][0]) + G[0][2] * (G[1][0] * G[2][1] - G[1][1] * G[2][0]);
                    double m2 = G[0][0] * G[1][1] - G[0][1] * G[0][1], m3 = G[0][0] * G[2][2] - G[0][2] * G[0][2], m4 = G[1][1] * G[2][2] - G[1][2] * G[1][2];
                    if (m2 < -1e-6 || m3 < -1e-6 || m4 < -1e-6 || det < -1e-4) continue;
                    psm3 |= 1 << ps;
                }
                if (!psm3) continue;
                c.psmask = psm3; c.zinc = zinc; c.zq = zq; c.zp = zp; c.so = so; c.pairP = pp; c.pairM = pm;
                c.xc[0] = c.xc[1] = 0;
                for (int t = 0; t < 4; t++) { int L = inc[t]; if (L < 2 || xof[L] != xY[y]) continue; int xs = sg[t] * sof[L]; c.xc[xs > 0 ? 0 : 1]++; }
                c.nq = 0;
                for (int t = 0; t < 4; t++) { int L = inc[t]; if (L < 2) continue; c.qL[c.nq] = L; c.qcb[c.nq] = (sg[t] * alpha[L] == 1) ? 0 : 1; c.qsd[c.nq] = (sg[t] * aY[y] > 0) ? 0 : 1; c.nq++; }
                int k = 0; for (int i = 0; i < 2; i++) for (int j = 2; j < 4; j++) { c.ma[k] = inc[i]; c.mb[k] = inc[j]; k++; c.ma[k] = inc[j]; c.mb[k] = inc[i]; k++; }
                c.nz = 0;
                for (int t = 0; t < 4; t++) if (inc[t] < 2) { c.zr[c.nz++] = zroot_of(inc[t], sg[t]); c.zr[c.nz++] = zroot_of(inc[t], -sg[t]) | 4; }
                c.dent = -1; for (int i = 0; i < 2; i++) for (int j = 2; j < 4; j++) if (inc[i] == inc[j]) c.dent = inc[i];
                double phi = 1.0 - c.fd / 28.0;
                if (phi < S->phimin[y]) S->phimin[y] = phi; if (phi > S->phimax[y]) S->phimax[y] = phi;
                if (n >= MAXC) { fprintf(stderr, "too many candidates\n"); exit(4); }
                arr[n++] = c;
            }
        }
        S->ncand[y] = n;
        if (n == 0) return 0;
    }
    return 1;
}
// ---------- search ----------
typedef struct { int ci, ps; } Opt;
typedef struct {
    int nas, order[NY], assigned[NY], ci[NY], ps[NY], T[NY][NY];
    int needQ[NY], needP[NY], sig[NY], target[NY];
    int uq[N][4];               // used: [0]=C, [1]=B, [2]=side+, [3]=side-
    unsigned char pairused[N * N];
    unsigned char mix[N][N];
    int zQ[4], zP[4], zhs[4], cntPs[2];
    int xq[N][2][2]; int yx[NY][2];
    int XC0[N][2][5][2]; int XC1[NY][2][5][2];
    int nside[2]; double phisum[2];
    int k, bid[4]; u64 Ginv[4][4]; double Lc[4][4]; int fl_ok;
    int ndep, did[NY + 2]; u64 dco[NY + 2][4];
} St;
typedef struct { long long nodes, surv, leaves, deadlist, sbcut; long long bydepth[NY + 2]; } Stat;
static int g_use_sidebound = 1;
static double phi_target[2]; static u64 sidevec_m[2][4];  // per structure (set in run_one); used only at the end via res
static inline void res_yy(int y, const Cand *a, int z, const Cand *b, int T, double *d, u64 *m) {
    int base = -4 * T - pYdot(y, z);
    *d = base - dotd(a->m, b->vd);
    *m = subm(tom(base), dotm(a->m, b->vm));
}
static void ip_basis(const Str *S, const St *st, int i1, int i2, double *d, u64 *m) {
    if (i1 > i2) { int t = i1; i1 = i2; i2 = t; }
    if (i1 == -2 && i2 == -2) { *d = S->RFF; *m = S->RFFm; return; }
    if (i1 == -2 && i2 == -1) { *d = S->RFV; *m = S->RFVm; return; }
    if (i1 == -1 && i2 == -1) { *d = S->RVV; *m = S->RVVm; return; }
    if (i1 < 0) {
        const Cand *c = &S->cand[i2][st->ci[i2]];
        if (i1 == -2) { *d = c->fd; *m = c->fm; return; }
        int TVY = -st->ps[i2]; *d = c->v0d - 4.0 * TVY; *m = subm(c->v0m, tom(4 * TVY)); return;
    }
    const Cand *a = &S->cand[i1][st->ci[i1]], *b = &S->cand[i2][st->ci[i2]];
    if (i1 == i2) { *d = a->sd; *m = a->sm; return; }
    res_yy(i1, a, i2, b, st->T[i1][i2], d, m);
}
static void ip_new(const Str *S, const St *st, int id, int y, const Cand *c, int ps, const int *Trow, double *d, u64 *m) {
    if (id == -2) { *d = c->fd; *m = c->fm; return; }
    if (id == -1) { int TVY = -ps; *d = c->v0d - 4.0 * TVY; *m = subm(c->v0m, tom(4 * TVY)); return; }
    res_yy(y, c, id, &S->cand[id][st->ci[id]], Trow[id], d, m);
}
static int basis_refresh(const Str *S, St *st) {
    int k = st->k; u64 G[4][8]; double Gd[4][4];
    for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) { double d; u64 m; ip_basis(S, st, st->bid[i], st->bid[j], &d, &m); G[i][j] = m; Gd[i][j] = d; }
    for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) G[i][k + j] = (i == j);
    for (int c = 0; c < k; c++) {
        int piv = -1; for (int r = c; r < k; r++) if (G[r][c]) { piv = r; break; }
        if (piv < 0) return 0;
        if (piv != c) for (int j = 0; j < 2 * k; j++) { u64 t = G[c][j]; G[c][j] = G[piv][j]; G[piv][j] = t; }
        u64 iv = invm(G[c][c]); for (int j = 0; j < 2 * k; j++) G[c][j] = mulm(G[c][j], iv);
        for (int r = 0; r < k; r++) if (r != c && G[r][c]) { u64 f = G[r][c]; for (int j = 0; j < 2 * k; j++) G[r][j] = subm(G[r][j], mulm(f, G[c][j])); }
    }
    for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) st->Ginv[i][j] = G[i][k + j];
    st->fl_ok = 1; memset(st->Lc, 0, sizeof st->Lc);
    for (int j = 0; j < k; j++) {
        double s = Gd[j][j]; for (int t = 0; t < j; t++) s -= st->Lc[j][t] * st->Lc[j][t];
        if (s < 1e-3) { st->fl_ok = 0; return 1; }
        st->Lc[j][j] = sqrt(s);
        for (int i = j + 1; i < k; i++) { double t = Gd[i][j]; for (int q = 0; q < j; q++) t -= st->Lc[i][q] * st->Lc[j][q]; st->Lc[i][j] = t / st->Lc[j][j]; }
    }
    return 1;
}
static int res_test(const St *st, const u64 *gm, const double *gd, u64 sm, double sd, u64 *coef) {
    int k = st->k; u64 c[4];
    for (int i = 0; i < k; i++) { u64 s = 0; for (int j = 0; j < k; j++) s = addm(s, mulm(st->Ginv[i][j], gm[j])); c[i] = s; }
    u64 q = 0; for (int i = 0; i < k; i++) q = addm(q, mulm(gm[i], c[i]));
    u64 schur = subm(sm, q);
    if (st->fl_ok) {
        double y[4]; for (int i = 0; i < k; i++) { double s = gd[i]; for (int j = 0; j < i; j++) s -= st->Lc[i][j] * y[j]; y[i] = s / st->Lc[i][i]; }
        double sch = sd; for (int i = 0; i < k; i++) sch -= y[i] * y[i];
        if (sch < -1e-6 * (1.0 + fabs(sd))) return 0;
    }
    if (schur == 0) { for (int i = 0; i < k; i++) coef[i] = c[i]; return 1; }
    if (k == 4) return 0;
    return 2;
}
static int xstar_col_ok(const Str *S, const St *st, int y, const Cand *c);
static void xstar_col_apply(St *st, int y, const Cand *c, int sgn);
// combinatorial compatibility with the current state
static inline int comb_ok(const Str *S, const St *st, int y, const Cand *c, int ps) {
    if (st->pairused[c->pairP] || st->pairused[c->pairM]) return 0;
    for (int t = 0; t < c->nq; t++) {
        int L = c->qL[t];
        int needCB = 0, needSd = 0;
        for (int u = 0; u < c->nq; u++) if (c->qL[u] == L) { if (c->qcb[u] == c->qcb[t]) needCB++; if (c->qsd[u] == c->qsd[t]) needSd++; }
        int capCB = c->qcb[t] == 0 ? S->cL[L] : S->bL[L], capSd = c->qsd[t] == 0 ? S->sP[L] : S->sM[L];
        if (st->uq[L][c->qcb[t]] + needCB > capCB || st->uq[L][2 + c->qsd[t]] + needSd > capSd) return 0;
    }
    for (int t = 0; t < 8; t++) {
        int a = c->ma[t], b = c->mb[t], cnt = 0;
        for (int u = 0; u < 8; u++) if (c->ma[u] == a && c->mb[u] == b) cnt++;
        if (st->mix[a][b] + cnt > S->cap[a][b]) return 0;
    }
    if (c->nz) {
        int nq[4] = {0, 0, 0, 0}, np_[4] = {0, 0, 0, 0};
        for (int t = 0; t < c->nz; t++) { int r = c->zr[t] & 3, rsg = (c->zr[t] >> 2) ? -1 : 1;
            if (rsg * aY[y] == zside[r]) nq[r]++; else np_[r]++; }
        for (int r = 0; r < 4; r++) if (st->zQ[r] < nq[r] || st->zP[r] < np_[r]) return 0;
        // eigen-equation at the Z roots (h = 0): the h-sum of their star(1) cut nbrs must stay completable
        int dh[4] = {0, 0, 0, 0};
        for (int t = 0; t < c->nz; t++) { int r = c->zr[t] & 3, rsg = (c->zr[t] >> 2) ? -1 : 1; dh[r] += rsg; }
        for (int r = 0; r < 4; r++) if (nq[r] + np_[r]) {
            int freeS = st->zQ[r] - nq[r] + st->zP[r] - np_[r];
            int d = -(S->zh[r] + st->zhs[r] + dh[r]);
            if (abs(d) > freeS || ((d - freeS) & 1)) return 0;
        }
    }
    if (withV && ps && st->cntPs[aY[y] > 0] >= 2) return 0;
    if (!xstar_col_ok(S, st, y, c)) return 0;
    // (L0) for star(x_Y) at the cut0 roots of cell (0,x_Y): each has exactly one nbr per x-side in star(x)
    for (int t = 0; t < 4; t++) { int L = c->L[t]; if (L < 2 || xof[L] != xY[y]) continue;
        int sg = c->inc_sg[t];
        // root sg*0rep(L) ~ p_Y (x-side aY*sY) ; root -sg*0rep(L) ~ -p_Y (x-side -aY*sY)
        int e1 = sg > 0 ? 0 : 1, s1 = (aY[y] * sY[y] > 0) ? 0 : 1;
        int add1 = 0, add2 = 0;
        for (int u = 0; u < 4; u++) { int L2 = c->L[u]; if (L2 != L) continue; if (c->inc_sg[u] == sg) add1++; else add2++; }
        (void)add2;
        if (S->x0[L][e1][s1] + st->xq[L][e1][s1] + add1 > 1) return 0;
        if (S->x0[L][1 - e1][1 - s1] + st->xq[L][1 - e1][1 - s1] + add1 > 1) return 0;
    }
    return 1;
}
static void apply_comb(St *st, int y, const Cand *c, int ps, int sgn) {
    st->pairused[c->pairP] += sgn; st->pairused[c->pairM] += sgn;
    for (int t = 0; t < c->nq; t++) { st->uq[c->qL[t]][c->qcb[t]] += sgn; st->uq[c->qL[t]][2 + c->qsd[t]] += sgn; }
    for (int t = 0; t < 8; t++) st->mix[c->ma[t]][c->mb[t]] += sgn;
    for (int t = 0; t < c->nz; t++) { int r = c->zr[t] & 3, rsg = (c->zr[t] >> 2) ? -1 : 1; int side1 = rsg * aY[y];
        if (side1 == zside[r]) st->zQ[r] -= sgn; else st->zP[r] -= sgn; st->zhs[r] += sgn * rsg; }
    if (withV && ps) st->cntPs[aY[y] > 0] += sgn;
    xstar_col_apply(st, y, c, sgn);
    for (int t = 0; t < 4; t++) { int L = c->L[t]; if (L < 2 || xof[L] != xY[y]) continue;
        int sg = c->inc_sg[t]; int e1 = sg > 0 ? 0 : 1, s1 = (aY[y] * sY[y] > 0) ? 0 : 1;
        st->xq[L][e1][s1] += sgn; st->xq[L][1 - e1][1 - s1] += sgn; }
    int sd = aY[y] > 0 ? 0 : 1; st->nside[sd] += sgn; st->phisum[sd] += sgn * (1.0 - c->fd / 28.0);
}
static int side_bound_ok(const Str *S, const St *st, const int *unassigned_side_min_max_dummy) {
    (void)unassigned_side_min_max_dummy;
    for (int sd = 0; sd < 2; sd++) {
        double lo = 0, hi = 0;
        for (int y = 0; y < NY; y++) if (!st->assigned[y] && ((aY[y] > 0 ? 0 : 1) == sd)) { lo += S->phimin[y]; hi += S->phimax[y]; }
        double need = phi_target[sd] - st->phisum[sd];
        if (need < lo - 1e-6 || need > hi + 1e-6) return 0;
    }
    return 1;
}
static int g_fastchk = 1;
static FILE *g_out; static FILE *g_kill;
static int final_check(const Str *S, St *st) {
    for (int L = 2; L < N; L++) if (st->uq[L][0] != S->cL[L] || st->uq[L][1] != S->bL[L] || st->uq[L][2] != S->sP[L] || st->uq[L][3] != S->sM[L]) return 0;
    if (withV && (st->cntPs[0] != 2 || st->cntPs[1] != 2)) return 0;
    for (int r = 0; r < 4; r++) if (st->zQ[r] != 0 || st->zP[r] != 0 || st->zhs[r] + S->zh[r] != 0) return 0;
    int nf = 0;
    for (int y = 0; y < NY; y++) {
        if (st->needQ[y] == 0 && st->needP[y] == 0) { if (st->sig[y] != st->target[y]) return 0; continue; }
        const Cand *c = &S->cand[y][st->ci[y]];
        if (st->needQ[y] == 1 && st->needP[y] == 1 && c->zinc == 0 && st->target[y] == 0 && c->dent < 0) { nf++; continue; }
        return 0;
    }
    if (nf & 1) return 0;
    if (withV) for (int sgn = -1; sgn <= 1; sgn += 2) {
        int ids[2], n = 0;
        for (int y = 0; y < NY; y++) if (st->ps[y] && aY[y] == sgn) ids[n++] = y;
        if (n == 2) { int y = ids[0], z = ids[1], T = st->T[y][z];
            if (T) { int qtype = (T == 1) ? (aY[y] == aY[z]) : (aY[y] == -aY[z]); if (qtype) return 0; } }
    }
    // full lambda/mu recount
    for (int y = 0; y < NY; y++) {
        const Cand *c = &S->cand[y][st->ci[y]];
        if (withV) {
            int innS = (xY[y] == 5 || xY[y] == 6) && (aY[y] * sY[y] == -1), innV = (xY[y] == 5 || xY[y] == 6) && (aY[y] * sY[y] == 1);
            int cs = 0, cv = 0;
            for (int t = 0; t < 4; t++) { int L = c->L[t], sg = c->inc_sg[t]; if (L < 2 || !((S->mask >> L) & 1)) continue; if (sg * alpha[L] == 1) cs++; else cv++; }
            for (int z = 0; z < NY; z++) if (z != y && st->ps[z]) { if (st->T[y][z] == 1) cs++; if (st->T[y][z] == -1) cv++; }
            if (cs + innS > (st->ps[y] ? 1 : 2)) return 0;
            if (cv + innV > 2) return 0;
        }
        for (int z = y + 1; z < NY; z++) {
            const Cand *b = &S->cand[z][st->ci[z]];
            for (int eps = -1; eps <= 1; eps += 2) {
                int cnt = 0;
                for (int i = 0; i < 4; i++) for (int j = 0; j < 4; j++) if (c->L[i] == b->L[j] && c->inc_sg[i] == eps * b->inc_sg[j]) cnt++;
                cnt += (aY[y] == eps * aY[z]) || (xY[y] == xY[z] && aY[y] * sY[y] == eps * aY[z] * sY[z]);
                for (int w = 0; w < NY; w++) if (w != y && w != z && st->T[y][w] && st->T[z][w] && st->T[y][w] * st->T[z][w] == eps) cnt++;
                if (withV && st->ps[y] && eps == 1 && st->ps[z]) cnt++;
                if (cnt > ((st->T[y][z] == eps) ? 1 : 2)) return 0;
            }
        }
    }
    // side-sum identities, exact mod p: for every basis vector b, sum_{side s} Res(b, Y) = (Res(b,F) - 2 Res(b,V)) / 2
    u64 inv2 = invm(2);
    for (int i = 0; i < st->k; i++) {
        int b = st->bid[i]; double dF, dV = 0; u64 mF, mV = 0;
        ip_basis(S, st, b, -2, &dF, &mF); if (withV) ip_basis(S, st, b, -1, &dV, &mV);
        u64 tgt = mulm(subm(mF, mulm(2, mV)), inv2);
        for (int sd = 0; sd < 2; sd++) {
            u64 s = 0;
            for (int y = 0; y < NY; y++) if ((aY[y] > 0 ? 0 : 1) == sd) { double d; u64 m; ip_basis(S, st, b, y, &d, &m); s = addm(s, m); }
            if (s != tgt) return 0;
        }
    }
    return 1;
}
static void emit(const Str *S, const St *st) {
    #pragma omp critical
    {
        fprintf(g_out, "Q"); for (int i = 0; i < N; i++) fprintf(g_out, " %d", S->Q[i]);
        fprintf(g_out, " P"); for (int i = 0; i < N; i++) fprintf(g_out, " %d", S->P[i]);
        fprintf(g_out, " mask %d cols", S->mask);
        for (int y = 0; y < NY; y++) { const Cand *c = &S->cand[y][st->ci[y]]; fprintf(g_out, " %d,%d,%d,%d,%d", c->L[0], c->L[1], c->L[2], c->L[3], st->ps[y]); }
        fprintf(g_out, " T"); for (int y = 0; y < NY; y++) for (int z = y + 1; z < NY; z++) if (st->T[y][z]) fprintf(g_out, " %d,%d,%d", y, z, st->T[y][z]);
        fprintf(g_out, "\n"); fflush(g_out);
    }
}
// per-thread list buffers
typedef struct { Opt *buf; size_t per; int *len[NY + 2]; Opt *lst[NY + 2][NY]; } Lists;

static inline int col_has(const Cand *c, int L, int sgn) { for (int t = 0; t < 4; t++) if (c->L[t] == L && c->inc_sg[t] == sgn) return 1; return 0; }
// lambda/mu for (star(0) root, cut1 root) pairs whose common neighbours include cut1 roots (via partner edges).
// y is being assigned with column c and partner row Trow (Trow[z] != 0 only for partners).
static int lm_star0_cut1_ok(const Str *S, const St *st, int y, const Cand *c, const int *Trow) {
    for (int t = 0; t < st->nas; t++) {
        int z = st->order[t]; int dz = Trow[z]; if (!dz) continue;
        const Cand *bz = &S->cand[z][st->ci[z]];
        // (a) pairs (p_Y, r), r = dz * (a star(0) incidence root of p_Z) = label L, sign dz*sg
        for (int j = 0; j < 4; j++) {
            int L = bz->L[j], sr = dz * bz->inc_sg[j];
            int cnt = 0;
            if (col_has(c, S->Q[L], sr)) cnt++;
            if (col_has(c, S->P[L], -sr)) cnt++;
            cnt += (L < 2) ? ((sr * (L == 0 ? 1 : -1)) == aY[y]) : (xof[L] == xY[y] && sr * sof[L] == aY[y] * sY[y]);
            for (int u = 0; u < st->nas; u++) { int w = st->order[u]; int dw = Trow[w]; if (!dw) continue;
                if (col_has(&S->cand[w][st->ci[w]], L, dw * sr)) cnt++; }
            int adj = col_has(c, L, sr);
            if (cnt > (adj ? 1 : 2)) return 0;
        }
        // (b) pairs (dz p_Z, r), r = a star(0) incidence root of p_Y (label L, sign sg)
        for (int i = 0; i < 4; i++) {
            int L = c->L[i], sg = c->inc_sg[i];
            int cnt = 1;                                  // p_Y itself
            if (col_has(bz, S->Q[L], dz * sg)) cnt++;
            if (col_has(bz, S->P[L], -dz * sg)) cnt++;
            { int e = dz * sg; cnt += (L < 2) ? ((e * (L == 0 ? 1 : -1)) == aY[z]) : (xof[L] == xY[z] && e * sof[L] == aY[z] * sY[z]); }
            for (int u = 0; u < st->nas; u++) { int w = st->order[u]; if (w == z) continue;
                int Tzw = st->T[z][w]; if (!Tzw) continue;
                int dw = dz * Tzw;                         // dw p_W ~ dz p_Z  <=>  T_zw = dz*dw
                if (col_has(&S->cand[w][st->ci[w]], L, dw * sg)) cnt++; }
            int adj = col_has(bz, L, dz * sg);
            if (cnt > (adj ? 1 : 2)) return 0;
        }
    }
    return 1;
}

static inline int xcap(int xr, int x) { return xr == x ? 1 : 2; }
// (L0) for the X-stars: adding the column of y (p_Y ~ sg*0rep(L)) must keep every endpoint within its star(x) bounds
static int xstar_col_ok(const Str *S, const St *st, int y, const Cand *c) {
    int add0[N][2][5][2]; int add1[2][5][2];
    memset(add0, 0, sizeof add0); memset(add1, 0, sizeof add1);
    for (int t = 0; t < 4; t++) { int L = c->L[t]; if (L < 2) continue; int sg = c->inc_sg[t];
        // p_Y gets nbr sg*0rep(L): star(x_L), side sg*s_L ; -p_Y gets -sg*0rep(L): side -sg*s_L
        int xs = sg * sof[L]; add1[0][xof[L] - 2][xs > 0 ? 0 : 1]++; add1[1][xof[L] - 2][xs > 0 ? 1 : 0]++;
        // root sg*0rep(L) (e index) gets nbr p_Y: star(x_Y), side aY*sY ; root -sg*0rep(L) gets -p_Y
        int e1 = sg > 0 ? 0 : 1, ys = aY[y] * sY[y];
        add0[L][e1][xY[y] - 2][ys > 0 ? 0 : 1]++; add0[L][1 - e1][xY[y] - 2][ys > 0 ? 1 : 0]++; }
    for (int x = 2; x < 7; x++) for (int sd = 0; sd < 2; sd++) for (int e = 0; e < 2; e++) {
        if (add1[e][x - 2][sd] > xcap(xY[y], x)) return 0; }
    for (int t = 0; t < 4; t++) { int L = c->L[t]; if (L < 2) continue;
        for (int e = 0; e < 2; e++) { int x = xY[y];
            for (int sd = 0; sd < 2; sd++) if (add0[L][e][x - 2][sd] && S->X0[L][e][x - 2][sd] + st->XC0[L][e][x - 2][sd] + add0[L][e][x - 2][sd] > xcap(xof[L], x)) return 0; } }
    return 1;
}
static void xstar_col_apply(St *st, int y, const Cand *c, int sgn) {
    for (int t = 0; t < 4; t++) { int L = c->L[t]; if (L < 2) continue; int sg = c->inc_sg[t];
        int xs = sg * sof[L]; st->XC1[y][0][xof[L] - 2][xs > 0 ? 0 : 1] += sgn; st->XC1[y][1][xof[L] - 2][xs > 0 ? 1 : 0] += sgn;
        int e1 = sg > 0 ? 0 : 1, ys = aY[y] * sY[y];
        st->XC0[L][e1][xY[y] - 2][ys > 0 ? 0 : 1] += sgn; st->XC0[L][1 - e1][xY[y] - 2][ys > 0 ? 1 : 0] += sgn; }
}
// partner edge p_Y ~ d p_Z (and -p_Y ~ -d p_Z): p_Y gets a nbr in star(x_Z) with side d*aZ*sZ; root d p_Z gets p_Y
static int xstar_partner_ok(const St *st, int y, int z, int d, const int *extra_y) {
    int sz = d * aY[z] * sY[z], sy = aY[y] * sY[y];
    int ez = d > 0 ? 0 : 1;
    // p_Y (e=0) and -p_Y (e=1)
    int v0 = st->XC1[y][0][xY[z] - 2][sz > 0 ? 0 : 1] + extra_y[(xY[z] - 2) * 4 + 0 * 2 + (sz > 0 ? 0 : 1)] + 1;
    if (v0 > xcap(xY[y], xY[z])) return 0;
    int v1 = st->XC1[z][ez][xY[y] - 2][sy > 0 ? 0 : 1] + 1;
    if (v1 > xcap(xY[z], xY[y])) return 0;
    return 1;
}
static void dfs(const Str *S, St *st, Lists *LS, int depth, Stat *sta);

static int g_prefilter = 1;
// per-parent cache of (candidate, option) residual data w.r.t. the 3-basis; rebuilt when the parent tag changes
typedef struct { int w, ci; u64 g3[3], S3; } PEnt;
static __thread PEnt *pc_buf = 0; static __thread int pc_n = 0, pc_cap = 0; static __thread long long pc_tag = -1, g_ptag = 0;
static __thread int pc_lab[3], pc_nlab = 0, pc_off[4];
static void pc_build(const Str *S, const St *st, Lists *LS, int depth, int y) {
    int ord[NY], no = 0;
    for (int w = 0; w < NY; w++) if (!st->assigned[w] && w != y) ord[no++] = w;
    for (int i = 1; i < no; i++) for (int j = i; j > 0 && LS->len[depth][ord[j - 1]] > LS->len[depth][ord[j]]; j--) { int t = ord[j]; ord[j] = ord[j - 1]; ord[j - 1] = t; }
    pc_nlab = no < 3 ? no : 3; pc_n = 0;
    if (!pc_buf) { pc_cap = 1 << 16; pc_buf = malloc(sizeof(PEnt) * pc_cap); }
    for (int oi = 0; oi < pc_nlab; oi++) {
        int w = ord[oi], plen = LS->len[depth][w]; Opt *src = LS->lst[depth][w];
        pc_lab[oi] = w; pc_off[oi] = pc_n;
        for (int i = 0; i < plen; i++) {
            const Cand *c = &S->cand[w][src[i].ci]; int ps = src[i].ps;
            int need_q = 1 - c->zq, need_p = 1 - c->zp;
            if (need_q < 0 || need_p < 0) continue;
            u64 bm[NY];
            int candQ[NY][2], nQ = 0, candP[NY][2], nP = 0;
            for (int t = 0; t < st->nas; t++) {
                int z = st->order[t]; int Tq = (aY[w] == aY[z]) ? 1 : -1, Tp = -Tq;
                if (need_q && st->needQ[z] > 0) { candQ[nQ][0] = z; candQ[nQ][1] = Tq; nQ++; }
                if (need_p && st->needP[z] > 0) { candP[nP][0] = z; candP[nP][1] = Tp; nP++; }
                bm[z] = subm(tom(-pYdot(w, z)), dotm(c->m, S->cand[z][st->ci[z]].vm));
            }
            for (int a = -1; a < nQ; a++) for (int b = -1; b < nP; b++) {
                if (a >= 0 && b >= 0 && candQ[a][0] == candP[b][0]) continue;
                int za = a >= 0 ? candQ[a][0] : -9, ta = a >= 0 ? candQ[a][1] : 0, zb = b >= 0 ? candP[b][0] : -9, tb = b >= 0 ? candP[b][1] : 0;
                if (pc_n == pc_cap) { pc_cap *= 2; pc_buf = realloc(pc_buf, sizeof(PEnt) * pc_cap); }
                PEnt *e = &pc_buf[pc_n++]; e->w = w; e->ci = src[i].ci;
                for (int i2 = 0; i2 < 3; i2++) { int id = st->bid[i2];
                    if (id == -2) e->g3[i2] = c->fm; else if (id == -1) e->g3[i2] = subm(c->v0m, tom(-4 * ps));
                    else { int T = (id == za) ? ta : (id == zb) ? tb : 0; e->g3[i2] = subm(bm[id], tom(4 * T)); } }
                u64 u[3]; for (int i2 = 0; i2 < 3; i2++) { u64 x = 0; for (int j2 = 0; j2 < 3; j2++) x = addm(x, mulm(st->Ginv[i2][j2], e->g3[j2])); u[i2] = x; }
                u64 S3 = c->sm; for (int i2 = 0; i2 < 3; i2++) S3 = subm(S3, mulm(e->g3[i2], u[i2]));
                e->S3 = S3;
            }
        }
    }
    pc_off[pc_nlab] = pc_n;
}
static int child_dead(const Str *S, const St *st, Lists *LS, int depth, int y, const Cand *ce, const u64 *ge, u64 Se) {
    if (pc_tag != g_ptag) { pc_build(S, st, LS, depth, y); pc_tag = g_ptag; }
    u64 ue[3]; for (int i = 0; i < 3; i++) { u64 a = 0; for (int j = 0; j < 3; j++) a = addm(a, mulm(st->Ginv[i][j], ge[j])); ue[i] = a; }
    for (int oi = 0; oi < pc_nlab; oi++) {
        int hit = 0, lastci = -1; u64 r0 = 0; int w = pc_lab[oi];
        for (int k = pc_off[oi]; k < pc_off[oi + 1] && !hit; k++) {
            PEnt *e = &pc_buf[k];
            if (e->ci != lastci) { r0 = subm(tom(-pYdot(w, y)), dotm(S->cand[w][e->ci].m, ce->vm)); lastci = e->ci; }
            u64 pr = addm(addm(mulm(e->g3[0], ue[0]), mulm(e->g3[1], ue[1])), mulm(e->g3[2], ue[2]));
            u64 lhs = mulm(e->S3, Se), b = subm(r0, pr);
            for (int T = -1; T <= 1; T++) { u64 t = subm(b, tom(4 * T)); if (mulm(t, t) == lhs) { hit = 1; break; } }
        }
        if (!hit) return 1;
    }
    return 0;
}
static void assign_try(const Str *S, St *st, Lists *LS, int depth, int y, int ci, int ps, Stat *sta) {
    const Cand *c = &S->cand[y][ci];
    int need_q = 1 - c->zq, need_p = 1 - c->zp;
    if (need_q < 0 || need_p < 0) return;
    int target = -4 - c->so + 2 * ps;
    int candQ[NY][2], nQ = 0, candP[NY][2], nP = 0;
    for (int t = 0; t < st->nas; t++) {
        int z = st->order[t]; int Tq = (aY[y] == aY[z]) ? 1 : -1, Tp = -Tq;
        if (need_q && st->needQ[z] > 0) { candQ[nQ][0] = z; candQ[nQ][1] = Tq; nQ++; }
        if (need_p && st->needP[z] > 0) { candP[nP][0] = z; candP[nP][1] = Tp; nP++; }
    }
    for (int a = -1; a < nQ; a++) for (int b = -1; b < nP; b++) {
        if (a >= 0 && b >= 0 && candQ[a][0] == candP[b][0]) continue;
        int sig = (a >= 0 ? candQ[a][1] : 0) + (b >= 0 ? candP[b][1] : 0);
        int remaining = (need_q - (a >= 0)) + (need_p - (b >= 0));
        int dpos = (a < 0 && b < 0 && need_q == 1 && need_p == 1 && c->zinc == 0 && target == 0);
        if (!dpos && (abs(target - sig) > remaining || ((target - sig - remaining) & 1))) continue;
        int Trow[NY]; memset(Trow, 0, sizeof Trow);
        if (a >= 0) Trow[candQ[a][0]] = candQ[a][1];
        if (b >= 0) Trow[candP[b][0]] = candP[b][1];
        // lambda/mu with assigned cut1 roots
        int bad = 0;
        for (int t = 0; t < st->nas && !bad; t++) {
            int z = st->order[t]; const Cand *bz = &S->cand[z][st->ci[z]];
            for (int eps = -1; eps <= 1 && !bad; eps += 2) {
                int cnt = 0;
                for (int i = 0; i < 4; i++) for (int j = 0; j < 4; j++) if (c->L[i] == bz->L[j] && c->inc_sg[i] == eps * bz->inc_sg[j]) cnt++;
                cnt += (aY[y] == eps * aY[z]) || (xY[y] == xY[z] && aY[y] * sY[y] == eps * aY[z] * sY[z]);
                for (int u = 0; u < st->nas; u++) { int w = st->order[u]; if (w == z) continue; if (Trow[w] && st->T[z][w] && Trow[w] * st->T[z][w] == eps) cnt++; }
                if (withV && ps && eps == 1 && st->ps[z]) cnt++;
                if (cnt > ((Trow[z] == eps) ? 1 : 2)) bad = 1;
            }
        }
        if (bad) continue;
        if (!lm_star0_cut1_ok(S, st, y, c, Trow)) continue;
        if (a >= 0 && b >= 0) {        // the two partners of y gain the common neighbour p_Y: recount their pair
            int z1 = candQ[a][0], d1 = candQ[a][1], z2 = candP[b][0], d2 = candP[b][1], eps = d1 * d2;
            const Cand *c1 = &S->cand[z1][st->ci[z1]], *c2 = &S->cand[z2][st->ci[z2]];
            int cnt = 1;                                                                   // p_Y
            for (int i = 0; i < 4; i++) for (int j = 0; j < 4; j++) if (c1->L[i] == c2->L[j] && c1->inc_sg[i] == eps * c2->inc_sg[j]) cnt++;
            cnt += (aY[z1] == eps * aY[z2]) || (xY[z1] == xY[z2] && aY[z1] * sY[z1] == eps * aY[z2] * sY[z2]);
            for (int u = 0; u < st->nas; u++) { int w = st->order[u]; if (w == z1 || w == z2) continue;
                if (st->T[z1][w] && st->T[z2][w] && st->T[z1][w] * st->T[z2][w] == eps) cnt++; }
            if (withV && eps == 1 && st->ps[z1] && st->ps[z2]) cnt++;
            if (cnt > ((st->T[z1][z2] == eps) ? 1 : 2)) continue;
        }
        { int extra[20]; memset(extra, 0, sizeof extra); int okx = 1;
          for (int t = 0; t < st->nas && okx; t++) { int z = st->order[t]; int d = Trow[z]; if (!d) continue;
              if (!xstar_partner_ok(st, y, z, d, extra)) okx = 0;
              int sz = d * aY[z] * sY[z]; extra[(xY[z] - 2) * 4 + 0 * 2 + (sz > 0 ? 0 : 1)]++; }
          if (!okx) continue; }
        { int z = y ^ 1;
          if (st->assigned[z] && Trow[z]) {
              int T = Trow[z]; const Cand *bz = &S->cand[z][st->ci[z]];
              int sy = (T * aY[z] * sY[z] > 0) ? 0 : 1;             // x-side of T p_Z (nbr of p_Y)
              int sz = (T * aY[y] * sY[y] > 0) ? 0 : 1;             // x-side of T p_Y (nbr of p_Z)
              if (c->xc[sy] + 1 > 1 || bz->xc[sz] + 1 > 1) continue;
          } }
        u64 gm[4]; double gd[4]; u64 coef[4];
        for (int i = 0; i < st->k; i++) ip_new(S, st, st->bid[i], y, c, ps, Trow, &gd[i], &gm[i]);
        int r = res_test(st, gm, gd, c->sm, c->sd, coef);
        if (!r) continue;
        if (g_prefilter && r == 2 && st->k == 3 && st->ndep == 0) {
            u64 u3[3]; for (int i = 0; i < 3; i++) { u64 a = 0; for (int j = 0; j < 3; j++) a = addm(a, mulm(st->Ginv[i][j], gm[j])); u3[i] = a; }
            u64 Se = c->sm; for (int i = 0; i < 3; i++) Se = subm(Se, mulm(gm[i], u3[i]));
            if (child_dead(S, st, LS, depth, y, c, gm, Se)) { sta->nodes++; sta->bydepth[st->nas + 1]++; sta->deadlist++; continue; }
        }
        int okd = 1;
        for (int t = 0; t < st->ndep && okd; t++) {
            double dd; u64 mm; ip_new(S, st, st->did[t], y, c, ps, Trow, &dd, &mm);
            u64 pred = 0; for (int i = 0; i < st->k; i++) pred = addm(pred, mulm(st->dco[t][i], gm[i]));
            if (pred != mm) okd = 0;
        }
        if (!okd) continue;
        St sv = *st;
        st->assigned[y] = 1; st->order[st->nas++] = y; st->ci[y] = ci; st->ps[y] = ps;
        for (int t = 0; t < st->nas - 1; t++) { int z = st->order[t]; st->T[y][z] = st->T[z][y] = Trow[z];
            int d = Trow[z]; if (d) { int sz = d * aY[z] * sY[z], sy = aY[y] * sY[y];
                st->XC1[y][0][xY[z] - 2][sz > 0 ? 0 : 1]++; st->XC1[y][1][xY[z] - 2][sz > 0 ? 1 : 0]++;
                int ez = d > 0 ? 0 : 1; st->XC1[z][ez][xY[y] - 2][sy > 0 ? 0 : 1]++; st->XC1[z][1 - ez][xY[y] - 2][sy > 0 ? 1 : 0]++; } }
        st->needQ[y] = need_q; st->needP[y] = need_p; st->sig[y] = 0; st->target[y] = target;
        if (a >= 0) { int z = candQ[a][0]; st->needQ[y]--; st->needQ[z]--; st->sig[y] += candQ[a][1]; st->sig[z] += candQ[a][1]; }
        if (b >= 0) { int z = candP[b][0]; st->needP[y]--; st->needP[z]--; st->sig[y] += candP[b][1]; st->sig[z] += candP[b][1]; }
        int feas = 1;
        for (int t = 0; t < st->nas && feas; t++) { int z = st->order[t]; int rem = st->needQ[z] + st->needP[z];
            if (rem > 0 && abs(st->target[z] - st->sig[z]) > rem) feas = 0;
            if (rem == 0 && st->target[z] != st->sig[z]) feas = 0; }
        if (feas) {
            if (r == 2) { st->bid[st->k++] = y; if (!basis_refresh(S, st)) feas = 0; for (int t = 0; t < st->ndep; t++) st->dco[t][st->k - 1] = 0; }
            else { st->did[st->ndep] = y; for (int i = 0; i < st->k; i++) st->dco[st->ndep][i] = coef[i]; st->ndep++; }
            if (feas) dfs(S, st, LS, depth, sta);     // depth = the child's depth (dfs passed depth + 1)
        }
        *st = sv;
    }
}

// does some partner option of candidate (y, c, ps) pass the exact residual tests against the current basis and dependents?
static int res_ok_any(const Str *S, const St *st, int y, const Cand *c, int ps) {
    int need_q = 1 - c->zq, need_p = 1 - c->zp;
    if (need_q < 0 || need_p < 0) return 0;
    int target = -4 - c->so + 2 * ps;
    int candQ[NY][2], nQ = 0, candP[NY][2], nP = 0;
    double bd[NY]; u64 bm[NY];
    for (int t = 0; t < st->nas; t++) {
        int z = st->order[t]; int Tq = (aY[y] == aY[z]) ? 1 : -1, Tp = -Tq;
        if (need_q && st->needQ[z] > 0) { candQ[nQ][0] = z; candQ[nQ][1] = Tq; nQ++; }
        if (need_p && st->needP[z] > 0) { candP[nP][0] = z; candP[nP][1] = Tp; nP++; }
        res_yy(y, c, z, &S->cand[z][st->ci[z]], 0, &bd[z], &bm[z]);
    }
    for (int a = -1; a < nQ; a++) for (int b = -1; b < nP; b++) {
        if (a >= 0 && b >= 0 && candQ[a][0] == candP[b][0]) continue;
        int sig = (a >= 0 ? candQ[a][1] : 0) + (b >= 0 ? candP[b][1] : 0);
        int remaining = (need_q - (a >= 0)) + (need_p - (b >= 0));
        int dpos = (a < 0 && b < 0 && need_q == 1 && need_p == 1 && c->zinc == 0 && target == 0);
        if (!dpos && (abs(target - sig) > remaining || ((target - sig - remaining) & 1))) continue;
        int za = a >= 0 ? candQ[a][0] : -9, ta = a >= 0 ? candQ[a][1] : 0, zb = b >= 0 ? candP[b][0] : -9, tb = b >= 0 ? candP[b][1] : 0;
        u64 gm[4]; double gd[4];
        for (int i = 0; i < st->k; i++) {
            int id = st->bid[i];
            if (id == -2) { gd[i] = c->fd; gm[i] = c->fm; }
            else if (id == -1) { int TVY = -ps; gd[i] = c->v0d - 4.0 * TVY; gm[i] = subm(c->v0m, tom(4 * TVY)); }
            else { int T = (id == za) ? ta : (id == zb) ? tb : 0; gd[i] = bd[id] - 4.0 * T; gm[i] = subm(bm[id], tom(4 * T)); }
        }
        u64 coef[4];
        int r = res_test(st, gm, gd, c->sm, c->sd, coef);
        if (!r) continue;
        int okd = 1;
        for (int t = 0; t < st->ndep && okd; t++) {
            int id = st->did[t]; u64 mm;
            if (id == -2) mm = c->fm;
            else if (id == -1) { int TVY = -ps; mm = subm(c->v0m, tom(4 * TVY)); }
            else { int T = (id == za) ? ta : (id == zb) ? tb : 0; mm = subm(bm[id], tom(4 * T)); }
            u64 pred = 0; for (int i = 0; i < st->k; i++) pred = addm(pred, mulm(st->dco[t][i], gm[i]));
            if (pred != mm) okd = 0;
        }
        if (okd) return 1;
    }
    return 0;
}


// Fast exact test once the basis is complete (k == 4): same option enumeration and verdict as res_ok_any restricted to the
// mod-p part.  g = g0 - 4*delta (delta = partner T's at basis labels); Schur(delta) = S0 + 8 delta.v - 16 delta^T Ginv delta,
// v = Ginv g0.  Dependents: pred(delta) = pred0 - 4 dco.delta, mm(delta) = mm0 - 4 T_dep.  (No float PSD: dropping it can
// only weaken pruning, never kill a valid candidate.)
static int res_ok_fast4(const Str *S, const St *st, int y, const Cand *c, int ps) {
    int need_q = 1 - c->zq, need_p = 1 - c->zp;
    if (need_q < 0 || need_p < 0) return 0;
    int target = -4 - c->so + 2 * ps;
    int candQ[NY][2], nQ = 0, candP[NY][2], nP = 0;
    u64 bm[NY];
    for (int t = 0; t < st->nas; t++) {
        int z = st->order[t]; int Tq = (aY[y] == aY[z]) ? 1 : -1, Tp = -Tq;
        if (need_q && st->needQ[z] > 0) { candQ[nQ][0] = z; candQ[nQ][1] = Tq; nQ++; }
        if (need_p && st->needP[z] > 0) { candP[nP][0] = z; candP[nP][1] = Tp; nP++; }
        const Cand *b = &S->cand[z][st->ci[z]];
        bm[z] = subm(tom(-pYdot(y, z)), dotm(c->m, b->vm));
    }
    u64 g0[4]; int pos[NY]; for (int z = 0; z < NY; z++) pos[z] = -1;
    for (int i = 0; i < 4; i++) {
        int id = st->bid[i];
        if (id == -2) g0[i] = c->fm;
        else if (id == -1) g0[i] = subm(c->v0m, tom(-4 * ps));
        else { g0[i] = bm[id]; pos[id] = i; }
    }
    u64 v[4]; for (int i = 0; i < 4; i++) { u64 a = 0; for (int j = 0; j < 4; j++) a = addm(a, mulm(st->Ginv[i][j], g0[j])); v[i] = a; }
    u64 S0 = c->sm; for (int i = 0; i < 4; i++) S0 = subm(S0, mulm(g0[i], v[i]));
    u64 pred0[NY + 2], mm0[NY + 2]; int dpos[NY + 2];
    for (int t = 0; t < st->ndep; t++) {
        u64 a = 0; for (int i = 0; i < 4; i++) a = addm(a, mulm(st->dco[t][i], g0[i])); pred0[t] = a;
        int id = st->did[t]; dpos[t] = id;
        if (id == -2) mm0[t] = c->fm; else if (id == -1) mm0[t] = subm(c->v0m, tom(-4 * ps)); else mm0[t] = bm[id];
    }
    for (int a = -1; a < nQ; a++) for (int b = -1; b < nP; b++) {
        if (a >= 0 && b >= 0 && candQ[a][0] == candP[b][0]) continue;
        int sig = (a >= 0 ? candQ[a][1] : 0) + (b >= 0 ? candP[b][1] : 0);
        int remaining = (need_q - (a >= 0)) + (need_p - (b >= 0));
        int dpos_ = (a < 0 && b < 0 && need_q == 1 && need_p == 1 && c->zinc == 0 && target == 0);
        if (!dpos_ && (abs(target - sig) > remaining || ((target - sig - remaining) & 1))) continue;
        int zz[2] = {a >= 0 ? candQ[a][0] : -9, b >= 0 ? candP[b][0] : -9}, tt[2] = {a >= 0 ? candQ[a][1] : 0, b >= 0 ? candP[b][1] : 0};
        // delta at basis positions
        u64 Sv = S0; int bi[2], bt[2], nb = 0;
        for (int h = 0; h < 2; h++) if (zz[h] >= 0 && pos[zz[h]] >= 0) { bi[nb] = pos[zz[h]]; bt[nb] = tt[h]; nb++; }
        for (int h = 0; h < nb; h++) Sv = addm(Sv, mulm(8, bt[h] > 0 ? v[bi[h]] : subm(0, v[bi[h]])));
        for (int h = 0; h < nb; h++) for (int h2 = 0; h2 < nb; h2++) {
            u64 q = mulm(16, st->Ginv[bi[h]][bi[h2]]); if (bt[h] * bt[h2] < 0) q = subm(0, q); Sv = subm(Sv, q); }
        if (Sv != 0) continue;
        int okd = 1;
        for (int t = 0; t < st->ndep && okd; t++) {
            u64 pred = pred0[t];
            for (int h = 0; h < nb; h++) { u64 q = mulm(4, st->dco[t][bi[h]]); pred = (bt[h] > 0) ? subm(pred, q) : addm(pred, q); }
            u64 mm = mm0[t]; int id = dpos[t];
            for (int h = 0; h < 2; h++) if (zz[h] >= 0 && zz[h] == id) mm = subm(mm, tom(4 * tt[h]));
            if (pred != mm) okd = 0;
        }
        if (okd) return 1;
    }
    return 0;
}
static void dfs(const Str *S, St *st, Lists *LS, int depth, Stat *sta) {
    sta->nodes++; sta->bydepth[st->nas]++;
    if (st->nas == NY) { sta->leaves++; if (final_check(S, st)) { sta->surv++; emit(S, st); } return; }
    if (g_use_sidebound && !side_bound_ok(S, st, 0)) { sta->sbcut++; return; }
    // forward-check lists of unassigned labels (from the parent's lists)
    int best = -1, bestn = 1 << 30;
    Opt *base = LS->buf + LS->per * (depth + 1);
    int off = 0;
    int ord[NY], no = 0;
    for (int y = 0; y < NY; y++) { LS->len[depth + 1][y] = 0; if (!st->assigned[y]) ord[no++] = y; }
    for (int i = 1; i < no; i++) for (int j = i; j > 0 && LS->len[depth][ord[j - 1]] > LS->len[depth][ord[j]]; j--) { int t = ord[j]; ord[j] = ord[j - 1]; ord[j - 1] = t; }
    int full = (st->k == 4);
    if (full) {                      // existence pass: a label with no fitting candidate kills the node (same verdict as below)
        for (int oi = 0; oi < no; oi++) {
            int y = ord[oi], plen = LS->len[depth][y], hit = 0; Opt *src = LS->lst[depth][y];
            for (int i = 0; i < plen && !hit; i++) { const Cand *c = &S->cand[y][src[i].ci];
                if (res_ok_fast4(S, st, y, c, src[i].ps) && comb_ok(S, st, y, c, src[i].ps)) hit = 1; }
            if (!hit) { sta->deadlist++; return; }
        }
    }
    for (int oi = 0; oi < no; oi++) {
        int y = ord[oi];
        Opt *dst = base + off; int n = 0;
        int plen = LS->len[depth][y]; Opt *src = LS->lst[depth][y];
        for (int i = 0; i < plen; i++) { const Cand *c = &S->cand[y][src[i].ci];
            if (full && !(g_fastchk ? res_ok_fast4(S, st, y, c, src[i].ps) : res_ok_any(S, st, y, c, src[i].ps))) continue;
            if (comb_ok(S, st, y, c, src[i].ps)) dst[n++] = src[i]; }
        LS->lst[depth + 1][y] = dst; LS->len[depth + 1][y] = n; off += n;
        if (n == 0) { sta->deadlist++; return; }
        if (n < bestn) { bestn = n; best = y; }
    }
    int y = best;
    Opt *L = LS->lst[depth + 1][y]; int n = LS->len[depth + 1][y];
    static __thread long long tagctr = 0; long long mytag = ++tagctr;
    for (int i = 0; i < n; i++) {
        g_ptag = mytag;
        const Cand *c = &S->cand[y][L[i].ci];
        if (!comb_ok(S, st, y, c, L[i].ps)) continue;
        apply_comb(st, y, c, L[i].ps, +1);
        assign_try(S, st, LS, depth + 1, y, L[i].ci, L[i].ps, sta);
        apply_comb(st, y, c, L[i].ps, -1);
    }
}
static Lists *lists_alloc(void) {
    Lists *LS = calloc(1, sizeof(Lists));
    size_t per = (size_t)NY * MAXC * 2;
    LS->per = per;
    LS->buf = malloc(sizeof(Opt) * per * (NY + 2));
    for (int d = 0; d <= NY + 1; d++) { LS->len[d] = calloc(NY, sizeof(int)); LS->lst[d][0] = LS->buf + per * d; }
    return LS;
}
static void run_one(Str *S, Lists *LS, Stat *sta) {
    St st; memset(&st, 0, sizeof st);
    for (int r = 0; r < 4; r++) { st.zQ[r] = S->zsQ[r]; st.zP[r] = S->zsP[r]; }
    if (withV) { st.pairused[S->vpair_id] = 1; st.pairused[S->spair_id] = 1; }
    st.k = 0; st.ndep = 0; st.fl_ok = 1;
    for (int sid = -2; sid <= (withV ? -1 : -2); sid++) {
        u64 gm[4]; double gd[4]; u64 coef[4];
        for (int i = 0; i < st.k; i++) ip_basis(S, &st, sid, st.bid[i], &gd[i], &gm[i]);
        double sd; u64 sm; ip_basis(S, &st, sid, sid, &sd, &sm);
        int r = res_test(&st, gm, gd, sm, sd, coef);
        if (!r) return;
        if (r == 1) { st.did[st.ndep] = sid; for (int i = 0; i < st.k; i++) st.dco[st.ndep][i] = coef[i]; st.ndep++; }
        else { st.bid[st.k++] = sid; basis_refresh(S, &st); for (int t = 0; t < st.ndep; t++) st.dco[t][st.k - 1] = 0; }
    }
    // side-sum targets for the F component: sum_{side} phi = nside - (RFF - 2 RFV) / 56   (phi = 1 - Res(F,Y)/28)
    double tgt = (S->RFF - 2.0 * (withV ? S->RFV : 0.0)) / 2.0;
    for (int sd = 0; sd < 2; sd++) { int ns = 0; for (int y = 0; y < NY; y++) if ((aY[y] > 0 ? 0 : 1) == sd) ns++; phi_target[sd] = ns - tgt / 28.0; }
    // initial lists
    int off = 0;
    for (int y = 0; y < NY; y++) {
        Opt *dst = LS->lst[0][0] + off; int n = 0;
        for (int i = 0; i < S->ncand[y]; i++) for (int ps = 0; ps < 2; ps++) if ((S->cand[y][i].psmask >> ps) & 1) { dst[n].ci = i; dst[n].ps = ps; n++; }
        LS->lst[0][y] = dst; LS->len[0][y] = n; off += n;
    }
    // lists for depth d are stored from LS->buf + per*d: fix the next-level base pointers
    dfs(S, &st, LS, 0, sta);
}
static unsigned long long rs = 88172645463325252ULL;
static unsigned rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static int structure_masks(Str *S, int forced, int *masks) {
    int nm = 0;
    if (!withV) { masks[nm++] = 0; return nm; }
    int pl[5], mi[5], a = 0, b = 0; for (int L = 2; L < N; L++) { if (alpha[L] == 1) pl[a++] = L; else mi[b++] = L; }
    for (int a1 = 0; a1 < 5; a1++) for (int a2 = a1 + 1; a2 < 5; a2++) for (int b1 = 0; b1 < 5; b1++) for (int b2 = b1 + 1; b2 < 5; b2++) {
        int mask = (1 << pl[a1]) | (1 << pl[a2]) | (1 << mi[b1]) | (1 << mi[b2]);
        if (!psigma_ok(S, mask, forced) || !even_v_ok(S, mask) || !v_odd_ok(S, mask)) continue;
        masks[nm++] = mask;
    }
    return nm;
}
int main(int argc, char **argv) {
    int a42[42]; for (int i = 0; i < 42; i++) a42[i] = atoi(argv[1 + i]);
    if (getenv("NO_SIDEBOUND")) g_use_sidebound = 0;
    if (getenv("SLOWCHK")) g_fastchk = 0;
    if (getenv("NOPRE")) g_prefilter = 0;
    const char *symf = argv[43]; withV = atoi(argv[44]); asq = withV ? 24 : 20; const char *mode = argv[45];
    int gidx[7][7]; int k = 0; for (int i = 0; i < 7; i++) for (int j = i + 1; j < 7; j++) { gidx[i][j] = k; k += 2; }
    for (int L = 0; L < N; L++) { xof[L] = (L < 2) ? 1 : 2 + (L - 2) / 2; sof[L] = (L % 2 == 0) ? 1 : -1;
        alpha[L] = (L < 2) ? 0 : a42[gidx[0][xof[L]] + (sof[L] == 1 ? 0 : 1)]; }
    for (int y = 0; y < NY; y++) { xY[y] = 2 + y / 2; sY[y] = (y % 2 == 0) ? 1 : -1; aY[y] = a42[gidx[1][xY[y]] + (sY[y] == 1 ? 0 : 1)]; }
    { FILE *f = fopen(symf, "r"); if (f) { while (nsym < 4096) { int ok = 1; for (int i = 0; i < N; i++) if (fscanf(f, "%d", &symperm[nsym][i]) != 1) { ok = 0; break; } if (!ok) break; nsym++; } fclose(f); } }
    int p[N], used[N]; memset(used, 0, sizeof used); gen_inv(p, used);
    if (!strcmp(mode, "list")) {     // canonical star-level survivors -> file of (qi, pi, mask)
        FILE *fo = fopen(argv[46], "w"); int nth = argc > 47 ? atoi(argv[47]) : 1;
#ifdef _OPENMP
        omp_set_num_threads(nth);
#endif
        long long tot = 0;
        #pragma omp parallel reduction(+:tot)
        {
            Str *S = calloc(1, sizeof(Str));
            #pragma omp for schedule(dynamic, 16)
            for (int qi = 0; qi < ninv; qi++) for (int pi = 0; pi < ninv; pi++) {
                int bad; int forced = profile_forced(inv[qi], inv[pi], &bad); if (bad) continue;
                int r = star_prepare(S, inv[qi], inv[pi]); if (r == -1) { fprintf(stderr, "singular mod p\n"); exit(5); } if (r != 1) continue;
                if (qval(S) > asq / 28.0 + 1e-9) continue;
                int masks[100]; int nm = structure_masks(S, forced, masks);
                for (int t = 0; t < nm; t++) if (is_canonical(inv[qi], inv[pi], masks[t])) {
                    tot++;
                    #pragma omp critical
                    fprintf(fo, "%d %d %d\n", qi, pi, masks[t]);
                }
            }
        }
        fclose(fo); printf("LIST %lld canonical (S0, mask)\n", tot); return 0;
    }
    if (!strcmp(mode, "run") || !strcmp(mode, "sample")) {
        int issample = !strcmp(mode, "sample");
        int (*items)[3] = NULL; long long nit = 0;
        const char *outf = issample ? "NUL" : argv[47]; int nth = issample ? 1 : atoi(argv[48]);
        if (!issample) {
            FILE *fl = fopen(argv[46], "r"); long long cap = 1 << 16; items = malloc(sizeof(int[3]) * cap);
            int a, b, c; while (fscanf(fl, "%d %d %d", &a, &b, &c) == 3) { if (nit == cap) { cap *= 2; items = realloc(items, sizeof(int[3]) * cap); } items[nit][0] = a; items[nit][1] = b; items[nit][2] = c; nit++; }
            fclose(fl);
        } else {
            int ns = atoi(argv[46]); rs ^= (unsigned long long)atoll(argv[47]) * 2654435761ULL;
            items = malloc(sizeof(int[3]) * ns); Str *S = calloc(1, sizeof(Str));
            while (nit < ns) {
                int qi = rnd() % ninv, pi = rnd() % ninv; int bad; int forced = profile_forced(inv[qi], inv[pi], &bad); if (bad) continue;
                if (star_prepare(S, inv[qi], inv[pi]) != 1) continue; if (qval(S) > asq / 28.0 + 1e-9) continue;
                int masks[100]; int nm = structure_masks(S, forced, masks); if (!nm) continue;
                items[nit][0] = qi; items[nit][1] = pi; items[nit][2] = masks[rnd() % nm]; nit++;
            }
        }
        long long first = 0, last = nit;
        if (!issample && argc > 50) { first = atoll(argv[49]); last = atoll(argv[50]); if (last > nit) last = nit; }
        g_out = fopen(outf, "a");
        { char kf[512]; snprintf(kf, sizeof kf, "%s.kills", outf); g_kill = issample ? NULL : fopen(kf, "a"); }
#ifdef _OPENMP
        omp_set_num_threads(nth);
#endif
        long long tnodes = 0, tsurv = 0, tbuild = 0, done = 0; time_t t0 = time(NULL); double maxt = 0;
        #pragma omp parallel reduction(+:tnodes,tsurv,tbuild)
        {
            Str *S = calloc(1, sizeof(Str)); for (int y = 0; y < NY; y++) S->cand[y] = malloc(MAXC * sizeof(Cand));
            Lists *LS = lists_alloc();
            #pragma omp for schedule(dynamic, 1)
            for (long long it = first; it < last; it++) {
                clock_t c0 = clock();
                int qi = items[it][0], pi = items[it][1];
                if (star_prepare(S, inv[qi], inv[pi]) != 1) { fprintf(stderr, "prepare failed\n"); exit(6); }
                S->mask = items[it][2];
                if (withV) v_odd_ok(S, S->mask);
                if (!build(S)) { tbuild++; if (g_kill) {
                    #pragma omp critical
                    { fprintf(g_kill, "%lld %d %d %d 0 -1 0 0\n", it, qi, pi, S->mask); fflush(g_kill); } } }
                else { Stat sta; memset(&sta, 0, sizeof sta); run_one(S, LS, &sta); tnodes += sta.nodes; tsurv += sta.surv;
                       if (g_kill) { int md = 0; for (int d = 0; d <= NY; d++) if (sta.bydepth[d]) md = d;
                           #pragma omp critical
                           { fprintf(g_kill, "%lld %d %d %d %lld %d %lld %.2f\n", it, qi, pi, S->mask, sta.nodes, md, sta.surv, (double)(clock() - c0) / CLOCKS_PER_SEC);  fflush(g_kill); } }
                       double dt = (double)(clock() - c0) / CLOCKS_PER_SEC;
                       if (issample) { printf("item %lld: ncand", it); for (int y = 0; y < NY; y++) printf(" %d", S->ncand[y]); printf("  nodes %lld leaves %lld surv %lld  %.3f s  deadlist %lld sbcut %lld  by depth", sta.nodes, sta.leaves, sta.surv, dt, sta.deadlist, sta.sbcut); for (int d = 0; d <= NY; d++) printf(" %lld", sta.bydepth[d]); puts(""); fflush(stdout); }
                       #pragma omp critical
                       { if (dt > maxt) maxt = dt; } }
                #pragma omp atomic
                done++;
                if (!issample && (done % 200 == 0)) {
                    #pragma omp critical
                    { fprintf(stderr, "\rdone %lld/%lld  elapsed %ld s  survivors so far (this thread-sum approx)   ", done, last - first, (long)(time(NULL) - t0)); fflush(stderr); }
                }
            }
        }
        fclose(g_out); if (g_kill) fclose(g_kill);
        printf("RUN items %lld..%lld  build-dead %lld  nodes %lld  survivors %lld  time %ld s  max item time %.2f s\n", first, last, tbuild, tnodes, tsurv, (long)(time(NULL) - t0), maxt);
        return 0;
    }
    return 0;
}
