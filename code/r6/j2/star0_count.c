// J2, star level: count star(0) structures (Q0, Pi0) + P_sigma cap star(0) that pass every star-level test.
// Labels of star(0) in 0-reps: 0 = e0+e1, 1 = e0-e1 (Z, h=0), 2+2(x-2)+(s<0) = e0 + s e_x (x=2..6).
// Tests (all necessary, see notes/154):
//   profile  : forced-P_sigma labels (z=2, or z=1 & s0=+1, or z=0 & s0=+2) at most 2 per alpha sign
//   a-test   : q = alpha^T A0^+ alpha <= 6/7                         (F = sum a_L f_L, |F|^2 = 672)
//   P_sigma  : 2 labels of each alpha sign, containing the forced ones;
//              v's O_0+ pair and O_0- pair are not Q0 pairs (lambda = 1 at 0+ / 0-);
//              lambda(sigma v, p) = 1 for p in P_sigma, mu <= 2 for the others; mu(v, p) <= 2
//   V odd    : Gram{star(0), V, F} PSD  <=>  s_V >= 0 and f_V^2 <= phi s_V
//   V even   : m+_V orthogonal to every component of Q u Pi u S, and 5 - m+_V (A0+)^+ m+_V >= 0
//   V P3     : 12I + 3T - RR^T on star(0) u V PSD ; V P3+ : 15Q + 60I - 3MM^T - 4J on star(0) u V PSD
// Usage: star0_count <alpha: 12 ints>   (alpha[0] = alpha[1] = 0)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define N 12
static int inv[10395][N];
static int ninv = 0;
static void gen_inv(int *p, int *used, int k) {
    int i = 0; while (i < N && used[i]) i++;
    if (i == N) { memcpy(inv[ninv++], p, sizeof(int) * N); return; }
    used[i] = 1;
    for (int j = i + 1; j < N; j++) if (!used[j]) { used[j] = 1; p[i] = j; p[j] = i; gen_inv(p, used, k + 1); used[j] = 0; }
    used[i] = 0;
}
static int cholsolve(double A[N][N], int n, double *b, double *x) {   // A SPD, overwritten
    double L[N][N]; memset(L, 0, sizeof L);
    for (int j = 0; j < n; j++) {
        double s = A[j][j]; for (int k = 0; k < j; k++) s -= L[j][k] * L[j][k];
        if (s <= 1e-12) return 0; L[j][j] = sqrt(s);
        for (int i = j + 1; i < n; i++) { double t = A[i][j]; for (int k = 0; k < j; k++) t -= L[i][k] * L[j][k]; L[i][j] = t / L[j][j]; }
    }
    double y[N];
    for (int i = 0; i < n; i++) { double s = b[i]; for (int k = 0; k < i; k++) s -= L[i][k] * y[k]; y[i] = s / L[i][i]; }
    for (int i = n - 1; i >= 0; i--) { double s = y[i]; for (int k = i + 1; k < n; k++) s -= L[k][i] * x[k]; x[i] = s / L[i][i]; }
    return 1;
}
// smallest eigenvalue check of a symmetric matrix via Cholesky with shift
static int psd_shift(double *M, int n, double shift) {
    double L[16][16]; memset(L, 0, sizeof L);
    for (int j = 0; j < n; j++) {
        double s = M[j * n + j] + shift; for (int k = 0; k < j; k++) s -= L[j][k] * L[j][k];
        if (s <= 0) return 0; L[j][j] = sqrt(s);
        for (int i = j + 1; i < n; i++) { double t = M[i * n + j]; for (int k = 0; k < j; k++) t -= L[i][k] * L[j][k]; L[i][j] = t / L[j][j]; }
    }
    return 1;
}
int main(int argc, char **argv) {
    int alpha[N]; for (int i = 0; i < N; i++) alpha[i] = atoi(argv[1 + i]);
    int xof[N], sof[N];
    for (int L = 0; L < N; L++) { xof[L] = (L < 2) ? 1 : 2 + (L - 2) / 2; sof[L] = (L % 2 == 0) ? 1 : -1; }
    int p[N], used[N]; memset(used, 0, sizeof used); gen_inv(p, used, 0);
    long long cnt_all = 0, cnt_prof = 0, cnt_a = 0, cnt_pairs = 0, cnt_lam = 0, cnt_odd = 0, cnt_even = 0, cnt_p3 = 0, cnt_s0 = 0;
    int plus[5], minus[5], np = 0, nm = 0;
    for (int L = 2; L < N; L++) { if (alpha[L] == 1) plus[np++] = L; else minus[nm++] = L; }
    double al[N]; for (int i = 0; i < N; i++) al[i] = alpha[i];
    for (int qi = 0; qi < ninv; qi++) {
        int *Q = inv[qi];
        for (int pi = 0; pi < ninv; pi++) {
            int *P = inv[pi]; cnt_all++;
            int forced = 0, fp = 0, fm = 0;   // bitmask of forced labels
            int bad = 0;
            for (int L = 2; L < N && !bad; L++) {
                int zc = (Q[L] < 2) + (P[L] < 2);
                int s0 = (Q[L] == P[L]) ? 0 : alpha[L] * (alpha[Q[L]] - alpha[P[L]]);
                int f = (zc == 2) || (zc == 1 && s0 == 1) || (zc == 0 && s0 == 2);
                if (f) { forced |= 1 << L; if (alpha[L] == 1) fp++; else fm++; }
            }
            if (fp > 2 || fm > 2) continue;
            cnt_prof++;
            // T in 0-reps
            int T[N][N]; memset(T, 0, sizeof T);
            for (int L = 0; L < N; L++) { T[L][Q[L]] += 1; T[L][P[L]] -= 1; }
            double A[N][N];
            for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) {
                double s = (i == j ? 11.0 : 0.0) + ((xof[i] == xof[j] && i != j) ? 1.0 : 0.0) - 1.0 - 4.0 * T[i][j];
                A[i][j] = s + 1.0;   // A0 + J (positive definite)
            }
            double Ac[N][N]; memcpy(Ac, A, sizeof A);
            double xa[N];
            if (!cholsolve(Ac, N, al, xa)) { fprintf(stderr, "chol fail\n"); continue; }
            double q = 0; for (int i = 0; i < N; i++) q += al[i] * xa[i];
            if (q > 6.0 / 7.0 + 1e-9) continue;
            cnt_a++;
            // even star Gram 5I - S - 2(Q+Pi): components of Q u Pi u S
            int comp[N]; for (int i = 0; i < N; i++) comp[i] = -1;
            int nc = 0;
            for (int s = 0; s < N; s++) if (comp[s] < 0) {
                int st[N], sp = 0; st[sp++] = s; comp[s] = nc;
                while (sp) { int u = st[--sp]; int nb[3] = {Q[u], P[u], (u ^ 1)};
                    for (int k = 0; k < 3; k++) if (comp[nb[k]] < 0) { comp[nb[k]] = nc; st[sp++] = nb[k]; } }
                nc++;
            }
            double Ae[N][N];
            for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) {
                double s = (i == j ? 5.0 : 0.0) - ((xof[i] == xof[j] && i != j) ? 1.0 : 0.0) - 2.0 * ((Q[i] == j) + (P[i] == j));
                Ae[i][j] = s;
            }
            // regularise the even Gram on its kernel: add sum over components of 1_K 1_K^T
            for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) if (comp[i] == comp[j]) Ae[i][j] += 1.0;
            int any = 0;
            for (int a1 = 0; a1 < 5; a1++) for (int a2 = a1 + 1; a2 < 5; a2++) for (int b1 = 0; b1 < 5; b1++) for (int b2 = b1 + 1; b2 < 5; b2++) {
                int S4[4] = {plus[a1], plus[a2], minus[b1], minus[b2]};
                int mask = 0; for (int k = 0; k < 4; k++) mask |= 1 << S4[k];
                if ((forced & mask) != forced) continue;
                cnt_pairs++;
                // v ~ -p for p in P_sigma: incidence at 0rep(L) with sign -alpha_L. O_0+ pair = minus labels, O_0- pair = plus labels.
                if (Q[minus[b1]] == minus[b2] || Q[plus[a1]] == plus[a2]) continue;
                int ok = 1;
                for (int L = 2; L < N && ok; L++) {
                    int inPs = (mask >> L) & 1;
                    int cs = 0, cv = 0;
                    int ql = Q[L], pl = P[L];
                    if (ql >= 2 && ((mask >> ql) & 1)) { if (alpha[ql] == alpha[L]) cs++; else cv++; }
                    if (pl >= 2 && ((mask >> pl) & 1)) { if (alpha[pl] == -alpha[L]) cs++; else cv++; }
                    int x = xof[L], s = sof[L];
                    int innS = (x == 5 || x == 6) && (alpha[L] * s == -1);
                    int innV = (x == 5 || x == 6) && (alpha[L] * s == 1);
                    if (inPs) { if (cs + innS > 1) ok = 0; } else { if (cs + innS > 2) ok = 0; }
                    if (cv + innV > 2) ok = 0;
                }
                if (!ok) continue;
                cnt_lam++;
                // odd V-test with F
                double mV[N];
                for (int L = 0; L < N; L++) {
                    double t = ((mask >> L) & 1) ? -alpha[L] : 0.0;
                    double rr = (xof[L] == 5 || xof[L] == 6) ? sof[L] : 0.0;
                    mV[L] = -4.0 * t - rr;
                }
                double Ac2[N][N]; memcpy(Ac2, A, sizeof A);
                double y[N]; cholsolve(Ac2, N, mV, y);
                double sV = 10.0, aVy = 0;
                for (int i = 0; i < N; i++) { sV -= mV[i] * y[i]; aVy += al[i] * y[i]; }
                double phi = 672.0 - 784.0 * q, fV = 56.0 - 28.0 * aVy;
                if (sV < -1e-9 || fV * fV > phi * sV + 1e-7) continue;
                cnt_odd++;
                // even V-test
                double mE[N];
                for (int L = 0; L < N; L++) mE[L] = -2.0 * ((mask >> L) & 1) - ((xof[L] == 5 || xof[L] == 6) ? 1.0 : 0.0) + 1.0;
                int kok = 1;
                for (int c = 0; c < nc && kok; c++) { double s = 0; for (int L = 0; L < N; L++) if (comp[L] == c) s += mE[L]; if (fabs(s) > 1e-9) kok = 0; }
                if (!kok) continue;
                double Ae2[N][N]; memcpy(Ae2, Ae, sizeof Ae);
                double ye[N]; cholsolve(Ae2, N, mE, ye);
                double sE = 5.0; for (int i = 0; i < N; i++) sE -= mE[i] * ye[i];
                if (sE < -1e-9) continue;
                cnt_even++;
                // P3 and P3+ tests on star(0) u V (13 x 13)
                double M3[13 * 13], M3p[13 * 13];
                for (int i = 0; i < 13; i++) for (int j = 0; j < 13; j++) {
                    double t, rr, tabs, mm;
                    if (i < 12 && j < 12) {
                        t = T[i][j]; tabs = (Q[i] == j) + (P[i] == j);
                        rr = (i == j) ? 2.0 : ((xof[i] == xof[j]) ? 0.0 : 1.0);
                        mm = (i == j) ? 2.0 : ((xof[i] == xof[j]) ? 2.0 : 1.0);
                    } else if (i == 12 && j == 12) { t = 0; tabs = 0; rr = 2; mm = 2; }
                    else { int L = (i < 12) ? i : j; t = ((mask >> L) & 1) ? -alpha[L] : 0.0; tabs = ((mask >> L) & 1);
                        rr = (xof[L] == 5 || xof[L] == 6) ? sof[L] : 0.0; mm = (xof[L] == 5 || xof[L] == 6) ? 1.0 : 0.0; }
                    M3[i * 13 + j] = (i == j ? 12.0 : 0.0) + 3.0 * t - rr;
                    M3p[i * 13 + j] = 15.0 * tabs + (i == j ? 60.0 : 0.0) - 3.0 * mm - 4.0;
                }
                if (!psd_shift(M3, 13, 1e-7) || !psd_shift(M3p, 13, 1e-6)) continue;
                cnt_p3++;
                any = 1;
            }
            if (any) cnt_s0++;
        }
    }
    printf("all %lld profile %lld a-test %lld | (S0,Psigma) pairs %lld lambda/mu %lld odd-V %lld even-V %lld P3 %lld | S0 with >=1 Psigma: %lld\n",
           cnt_all, cnt_prof, cnt_a, cnt_pairs, cnt_lam, cnt_odd, cnt_even, cnt_p3, cnt_s0);
    return 0;
}
