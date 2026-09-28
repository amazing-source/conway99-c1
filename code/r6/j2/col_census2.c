// J2 census: for sampled star-level survivors (S0, P_sigma cap star(0)), count the admissible columns of each cut1 label.
// A column of Y (label (1,x,s), positive rep p_Y) = its 2 incidences in O_0+ (labels L1,L2 -> roots 0rep(L)) and 2 in O_0-
// (labels L3,L4 -> roots -0rep(L)).  Filters (all necessary):
//   pair design : {L1,L2}, {L3,L4} distinct, not Q0 pairs, not v's / sigma v's O_0+ pairs
//   h-profile   : (zinc, sigma_other, P_sigma status) in the allowed table (notes/151 s2ter); zinc=2 -> one Z root in O_1+, one in O_1-
//   lambda/mu   : common neighbours with sigma v / v inside star(0) u inner vertices <= 1 or 2
//   odd         : Gram{F_perp, rho_V, rho_Y} PSD   (second residual s'_Y >= 0)
//   even        : m+_Y orthogonal to each component of Q u Pi u S; Gram{V,Y} even residual PSD
// Usage: col_census <a: 42 ints> <nsamples> <seed>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define N 12
static int inv[10395][N]; static int ninv = 0;
static void gen_inv(int *p, int *used) {
    int i = 0; while (i < N && used[i]) i++;
    if (i == N) { memcpy(inv[ninv++], p, sizeof(int) * N); return; }
    used[i] = 1;
    for (int j = i + 1; j < N; j++) if (!used[j]) { used[j] = 1; p[i] = j; p[j] = i; gen_inv(p, used); used[j] = 0; }
    used[i] = 0;
}
static void chol_inv(double A[N][N], double Ainv[N][N]) {
    double L[N][N]; memset(L, 0, sizeof L);
    for (int j = 0; j < N; j++) {
        double s = A[j][j]; for (int k = 0; k < j; k++) s -= L[j][k] * L[j][k];
        L[j][j] = sqrt(s);
        for (int i = j + 1; i < N; i++) { double t = A[i][j]; for (int k = 0; k < j; k++) t -= L[i][k] * L[j][k]; L[i][j] = t / L[j][j]; }
    }
    for (int c = 0; c < N; c++) {
        double y[N], x[N];
        for (int i = 0; i < N; i++) { double s = (i == c); for (int k = 0; k < i; k++) s -= L[i][k] * y[k]; y[i] = s / L[i][i]; }
        for (int i = N - 1; i >= 0; i--) { double s = y[i]; for (int k = i + 1; k < N; k++) s -= L[k][i] * x[k]; x[i] = s / L[i][i]; }
        for (int i = 0; i < N; i++) Ainv[i][c] = x[i];
    }
}
static unsigned long long rs;
static unsigned rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static double quad(double P[N][N], double *u, double *v) { double s = 0; for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) s += u[i] * P[i][j] * v[j]; return s; }
int main(int argc, char **argv) {
    int a42[42]; for (int i = 0; i < 42; i++) a42[i] = atoi(argv[1 + i]);
    int nsamp = atoi(argv[43]); rs = 0x9E3779B97F4A7C15ULL ^ (unsigned long long)atoll(argv[44]);
    // label index in the global 42 list: cells (i,j) i<j lexicographic, sign +1 then -1
    int gidx[7][7]; int k = 0; for (int i = 0; i < 7; i++) for (int j = i + 1; j < 7; j++) { gidx[i][j] = k; k += 2; }
    int alpha[N], xof[N], sof[N];
    for (int L = 0; L < N; L++) { xof[L] = (L < 2) ? 1 : 2 + (L - 2) / 2; sof[L] = (L % 2 == 0) ? 1 : -1;
        alpha[L] = (L < 2) ? 0 : a42[gidx[0][xof[L]] + (sof[L] == 1 ? 0 : 1)]; }
    int aY[10], xY[10], sY[10];
    for (int y = 0; y < 10; y++) { xY[y] = 2 + y / 2; sY[y] = (y % 2 == 0) ? 1 : -1; aY[y] = a42[gidx[1][xY[y]] + (sY[y] == 1 ? 0 : 1)]; }
    int p[N], used[N]; memset(used, 0, sizeof used); gen_inv(p, used);
    int plus[5], minus[5], np = 0, nm = 0;
    for (int L = 2; L < N; L++) { if (alpha[L] == 1) plus[np++] = L; else minus[nm++] = L; }
    double al[N]; for (int i = 0; i < N; i++) al[i] = alpha[i];
    int got = 0; long long tries = 0;
    long long hist[10][6]; memset(hist, 0, sizeof hist);
    double logsum = 0; int dead = 0;
    while (got < nsamp) {
        tries++;
        int *Q = inv[rnd() % ninv], *P = inv[rnd() % ninv];
        int forced = 0, fp = 0, fm = 0;
        for (int L = 2; L < N; L++) {
            int zc = (Q[L] < 2) + (P[L] < 2);
            int s0 = (Q[L] == P[L]) ? 0 : alpha[L] * (alpha[Q[L]] - alpha[P[L]]);
            if ((zc == 2) || (zc == 1 && s0 == 1) || (zc == 0 && s0 == 2)) { forced |= 1 << L; if (alpha[L] == 1) fp++; else fm++; }
        }
        if (fp > 2 || fm > 2) continue;
        int T[N][N]; memset(T, 0, sizeof T);
        for (int L = 0; L < N; L++) { T[L][Q[L]] += 1; T[L][P[L]] -= 1; }
        double A[N][N], Ap[N][N];
        for (int i = 0; i < N; i++) for (int j = 0; j < N; j++)
            A[i][j] = (i == j ? 11.0 : 0.0) + ((xof[i] == xof[j] && i != j) ? 1.0 : 0.0) - 4.0 * T[i][j];   // A0 + J
        chol_inv(A, Ap);           // (A0+J)^{-1}: acts as A0^+ on 1-perp vectors
        double xa[N]; for (int i = 0; i < N; i++) { xa[i] = 0; for (int j = 0; j < N; j++) xa[i] += Ap[i][j] * al[j]; }
        double q = 0; for (int i = 0; i < N; i++) q += al[i] * xa[i];
        if (q > 6.0 / 7.0 + 1e-9) continue;
        // even
        int comp[N]; for (int i = 0; i < N; i++) comp[i] = -1; int nc = 0;
        for (int s = 0; s < N; s++) if (comp[s] < 0) { int st[N], sp = 0; st[sp++] = s; comp[s] = nc;
            while (sp) { int u = st[--sp]; int nb[3] = {Q[u], P[u], u ^ 1}; for (int t = 0; t < 3; t++) if (comp[nb[t]] < 0) { comp[nb[t]] = nc; st[sp++] = nb[t]; } } nc++; }
        double Ae[N][N], Aep[N][N];
        for (int i = 0; i < N; i++) for (int j = 0; j < N; j++)
            Ae[i][j] = (i == j ? 5.0 : 0.0) - ((xof[i] == xof[j] && i != j) ? 1.0 : 0.0) - 2.0 * ((Q[i] == j) + (P[i] == j)) + (comp[i] == comp[j] ? 1.0 : 0.0);
        chol_inv(Ae, Aep);
        // pick a random admissible P_sigma (same filters as star0_count)
        int cand[100][4], nca = 0;
        for (int a1 = 0; a1 < 5; a1++) for (int a2 = a1 + 1; a2 < 5; a2++) for (int b1 = 0; b1 < 5; b1++) for (int b2 = b1 + 1; b2 < 5; b2++) {
            int S4[4] = {plus[a1], plus[a2], minus[b1], minus[b2]}; int mask = 0; for (int t = 0; t < 4; t++) mask |= 1 << S4[t];
            if ((forced & mask) != forced) continue;
            if (Q[minus[b1]] == minus[b2] || Q[plus[a1]] == plus[a2]) continue;
            int ok = 1;
            for (int L = 2; L < N && ok; L++) {
                int inPs = (mask >> L) & 1, cs = 0, cv = 0, ql = Q[L], pl = P[L];
                if (ql >= 2 && ((mask >> ql) & 1)) { if (alpha[ql] == alpha[L]) cs++; else cv++; }
                if (pl >= 2 && ((mask >> pl) & 1)) { if (alpha[pl] == -alpha[L]) cs++; else cv++; }
                int x = xof[L], s = sof[L];
                int innS = (x == 5 || x == 6) && (alpha[L] * s == -1), innV = (x == 5 || x == 6) && (alpha[L] * s == 1);
                if (inPs) { if (cs + innS > 1) ok = 0; } else { if (cs + innS > 2) ok = 0; }
                if (cv + innV > 2) ok = 0;
            }
            if (!ok) continue;
            double mV[N]; for (int L = 0; L < N; L++) mV[L] = -4.0 * (((mask >> L) & 1) ? -alpha[L] : 0.0) - ((xof[L] == 5 || xof[L] == 6) ? sof[L] : 0.0);
            double sV = 10.0 - quad(Ap, mV, mV), aVy = quad(Ap, al, mV);
            double phi = 672.0 - 784.0 * q, fV = 56.0 - 28.0 * aVy;
            if (sV < -1e-9 || fV * fV > phi * sV + 1e-7) continue;
            double mE[N]; for (int L = 0; L < N; L++) mE[L] = -2.0 * ((mask >> L) & 1) - ((xof[L] == 5 || xof[L] == 6) ? 1.0 : 0.0) + 1.0;
            int kok = 1; for (int c = 0; c < nc && kok; c++) { double s = 0; for (int L = 0; L < N; L++) if (comp[L] == c) s += mE[L]; if (fabs(s) > 1e-9) kok = 0; }
            if (!kok) continue;
            if (5.0 - quad(Aep, mE, mE) < -1e-9) continue;
            memcpy(cand[nca++], S4, sizeof S4);
        }
        if (!nca) continue;
        int *S4 = cand[rnd() % nca]; int mask = 0; for (int t = 0; t < 4; t++) mask |= 1 << S4[t];
        got++;
        double mV[N]; for (int L = 0; L < N; L++) mV[L] = -4.0 * (((mask >> L) & 1) ? -alpha[L] : 0.0) - ((xof[L] == 5 || xof[L] == 6) ? sof[L] : 0.0);
        double sV = 10.0 - quad(Ap, mV, mV), aVy = quad(Ap, al, mV), phi = 672.0 - 784.0 * q, fV = 56.0 - 28.0 * aVy;
        double mE[N]; for (int L = 0; L < N; L++) mE[L] = -2.0 * ((mask >> L) & 1) - ((xof[L] == 5 || xof[L] == 6) ? 1.0 : 0.0) + 1.0;
        double sEV = 5.0 - quad(Aep, mE, mE);
        int vpair[2], spair[2], nv = 0, ns = 0;
        for (int t = 0; t < 4; t++) { if (alpha[S4[t]] == -1) vpair[nv++] = S4[t]; else spair[ns++] = S4[t]; }
        int cL[N], bL[N];
        for (int L = 0; L < N; L++) { cL[L] = bL[L] = 0; }
        for (int L = 2; L < N; L++) {
            int zc = (Q[L] < 2) + (P[L] < 2);
            int s0 = (Q[L] == P[L]) ? 0 : alpha[L] * (alpha[Q[L]] - alpha[P[L]]);
            int inPs = (mask >> L) & 1;
            int so = -4 - s0 + 2 * inPs, n = 4 - zc;
            cL[L] = (n + so) / 2; bL[L] = (n - so) / 2;
            if (cL[L] < 0 || bL[L] < 0 || ((n + so) & 1)) { cL[L] = -99; }
        }
        double lp = 0; int anyzero = 0;
        for (int y = 0; y < 10; y++) {
            long long cnt = 0;
            double rY[N];   // R_0 p_Y
            for (int L = 0; L < N; L++) {
                if (L == 0) rY[L] = aY[y]; else if (L == 1) rY[L] = -aY[y];
                else rY[L] = (xof[L] == xY[y]) ? (double)(aY[y] * sY[y] * sof[L]) : 0.0;
            }
            int innS = (xY[y] == 5 || xY[y] == 6) && (aY[y] * sY[y] == -1), innV = (xY[y] == 5 || xY[y] == 6) && (aY[y] * sY[y] == 1);
            for (int L1 = 0; L1 < N; L1++) for (int L2 = L1 + 1; L2 < N; L2++) {
                if (Q[L1] == L2) continue;
                if ((L1 == vpair[0] && L2 == vpair[1]) || (L1 == vpair[1] && L2 == vpair[0])) continue;
                if ((L1 == spair[0] && L2 == spair[1]) || (L1 == spair[1] && L2 == spair[0])) continue;
                for (int L3 = 0; L3 < N; L3++) for (int L4 = L3 + 1; L4 < N; L4++) {
                    if (Q[L3] == L4) continue;
                    if ((L3 == vpair[0] && L4 == vpair[1]) || (L3 == vpair[1] && L4 == vpair[0])) continue;
                    if ((L3 == spair[0] && L4 == spair[1]) || (L3 == spair[1] && L4 == spair[0])) continue;
                    if (L1 == L3 && L2 == L4) continue;
                    int zinc = (L1 < 2) + (L2 < 2) + (L3 < 2) + (L4 < 2);
                    int so = alpha[L1] + alpha[L2] - alpha[L3] - alpha[L4];
                    if (zinc > 2) continue;
                    if (zinc == 2) {   // one Z root in O_1+ (+z1 or -z2) and one in O_1- (-z1 or +z2)
                        int up = (L1 == 0) + (L2 == 0) + (L3 == 1) + (L4 == 1), dn = (L3 == 0) + (L4 == 0) + (L1 == 1) + (L2 == 1);
                        if (!(up == 1 && dn == 1)) continue;
                    }
                    {   int inc2[4] = {L1, L2, L3, L4}, sg2[4] = {1, 1, -1, -1}, bad = 0;
                        int needC[N], needB[N]; memset(needC, 0, sizeof needC); memset(needB, 0, sizeof needB);
                        for (int t = 0; t < 4; t++) { int L = inc2[t]; if (L < 2) continue;
                            if (sg2[t] * alpha[L] == 1) needC[L]++; else needB[L]++; }
                        for (int L = 2; L < N && !bad; L++) if (needC[L] > cL[L] || needB[L] > bL[L]) bad = 1;
                        // shared inner vertex of p_Y with root eps*0rep(L)
                        #define SHARED(L, eps) ( ((L) < 2) ? (((eps) * ((L) == 0 ? 1 : -1)) == aY[y]) : (xof[L] == xY[y] && (eps) * sof[L] == aY[y] * sY[y]) )
                        // for every root r of star(0) (label L, sign eps): count Y's incidences among r's star(0) nbrs
                        for (int L = 0; L < N && !bad; L++) for (int eps = -1; eps <= 1 && !bad; eps += 2) {
                            int isinc = 0; for (int t = 0; t < 4; t++) if (inc2[t] == L && sg2[t] == eps) isinc = 1;
                            int c = 0; int qn = Q[L], pn = P[L];
                            for (int t = 0; t < 4; t++) { if (inc2[t] == qn && sg2[t] == eps) c++; if (inc2[t] == pn && sg2[t] == -eps) c++; }
                            int sh = SHARED(L, eps);
                            if (isinc) { if (c + sh > 1) bad = 1; } else { if (c + sh > 2) bad = 1; }
                        }
                        // at most one incidence in cell (0,x_Y) on each x-side
                        { int side[2] = {0, 0};
                          for (int t = 0; t < 4; t++) { int L = inc2[t]; if (L < 2 || xof[L] != xY[y]) continue; int xs = sg2[t] * sof[L]; side[xs > 0]++; }
                          if (side[0] > 1 || side[1] > 1) bad = 1; }
                        if (bad) continue;
                    }
                    // lambda/mu with sigma v and v inside star(0)
                    int inc[4] = {L1, L2, L3, L4}, sg[4] = {1, 1, -1, -1}, cs = 0, cv = 0;
                    for (int t = 0; t < 4; t++) { int L = inc[t]; if (L < 2 || !((mask >> L) & 1)) continue;
                        if (sg[t] * alpha[L] == 1) cs++; else cv++; }
                    if (cv + innV > 2) continue;
                    double t0[N]; memset(t0, 0, sizeof t0); t0[L1] += 1; t0[L2] += 1; t0[L3] -= 1; t0[L4] -= 1;
                    double m[N]; for (int L = 0; L < N; L++) m[L] = -4.0 * t0[L] - rY[L];
                    double sYv = 10.0 - quad(Ap, m, m);
                    if (sYv < -1e-9) continue;
                    double fY = 28.0 * (1.0 - quad(Ap, al, m));
                    double gVY0 = quad(Ap, mV, m);
                    // even column
                    double me[N]; for (int L = 0; L < N; L++) { int incn = (L == L1) + (L == L2) + (L == L3) + (L == L4);
                        me[L] = -2.0 * incn - (L < 2 ? 1.0 : 0.0) - (xof[L] == xY[y] ? 1.0 : 0.0) + 1.0; }
                    int kok = 1; for (int c = 0; c < nc && kok; c++) { double s = 0; for (int L = 0; L < N; L++) if (comp[L] == c) s += me[L]; if (fabs(s) > 1e-9) kok = 0; }
                    if (!kok) continue;
                    double sEY = 5.0 - quad(Aep, me, me);
                    if (sEY < -1e-9) continue;
                    double gE0 = quad(Aep, mE, me);
                    int ok = 0;
                    for (int ps = 0; ps < 2 && !ok; ps++) {     // ps = 1: Y in P_sigma (T_VY = -1)
                        // profile table
                        int allowed = 0;
                        if (zinc == 2) allowed = (so == -2 && ps);
                        else if (zinc == 1) allowed = (so == -3) || (so == -1 && ps);
                        else allowed = (so == -4) || (so == -2) || (so == 0 && ps);
                        if (!allowed) continue;
                        if (ps) { if (cs + innS > 1) continue; } else { if (cs + innS > 2) continue; }
                        double TVY = ps ? -1.0 : 0.0;
                        double rVrY = (xY[y] == 5 || xY[y] == 6) ? (double)(aY[y] * sY[y]) : 0.0;   // r_V . p_Y
                        double g = -4.0 * TVY - rVrY - gVY0;
                        double G[3][3] = {{phi, fV, fY}, {fV, sV, g}, {fY, g, sYv}};
                        // PSD of 3x3 via Cholesky with tolerance
                        double l00 = G[0][0]; if (l00 < -1e-9) continue;
                        double d1, d2;
                        if (l00 > 1e-9) {
                            double a10 = G[1][0] / l00, a20 = G[2][0] / l00;
                            d1 = G[1][1] - a10 * G[1][0]; double e12 = G[2][1] - a20 * G[1][0]; d2 = G[2][2] - a20 * G[2][0];
                            if (d1 < -1e-7) continue;
                            if (d1 > 1e-9) { if (d2 - e12 * e12 / d1 < -1e-7) continue; } else { if (fabs(e12) > 1e-6 || d2 < -1e-7) continue; }
                        } else { if (fabs(fV) > 1e-6 || fabs(fY) > 1e-6) continue; if (sV * sYv - g * g < -1e-7) continue; }
                        double gE = -2.0 * ps - ((xY[y] == 5 || xY[y] == 6) ? 1.0 : 0.0) + 1.0 - gE0;
                        if (sEV * sEY - gE * gE < -1e-7) continue;
                        ok = 1;
                    }
                    if (ok) cnt++;
                }
            }
            int b = cnt == 0 ? 0 : cnt < 10 ? 1 : cnt < 50 ? 2 : cnt < 200 ? 3 : cnt < 1000 ? 4 : 5;
            hist[y][b]++;
            if (cnt == 0) anyzero = 1; else lp += log((double)cnt);
        }
        if (anyzero) dead++; else logsum += lp;
    }
    printf("samples %d (tries %lld)  dead (some cut1 label has no column): %d\n", got, tries, dead);
    printf("per-label column-count histogram [0, 1-9, 10-49, 50-199, 200-999, 1000+]:\n");
    for (int y = 0; y < 10; y++) { printf("  Y=(1,%d,%+d): ", xY[y], sY[y]); for (int b = 0; b < 6; b++) printf("%lld ", hist[y][b]); printf("\n"); }
    if (got > dead) printf("mean log10 prod N_Y over live samples: %.2f\n", logsum / (got - dead) / log(10.0));
    return 0;
}
