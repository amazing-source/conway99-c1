/* Branch 18 (t = 0), level 1: count the X-configurations of a support (constraint list in xlevel.py).
   stdin: 9 lines of 9 chars '0'/'1' (rows = P, columns = N).
   An X vertex is a pair (P-pair, N-pair); the P-pair multiset and N-pair multiset are forced by D.
   Constraints: (a) for p in pi, |nu & row_p| <= 1 and for v in nu, |pi & col_v| <= 1;
                (c) x(p,v) <= 2 - D[p][v];  (d) |pi & pi'| + |nu & nu'| <= 2 for two X vertices.
   Identical P-slots get strictly increasing N-pair indices (identical (pi,nu) twice is excluded by (d)).
   stdout: count (and, with argument "dump", every configuration as 18 lines "p1 p2 v1 v2" + blank line). */
#include <stdio.h>
#include <string.h>
#include <math.h>
static int D[9][9];
static int Pa[18], Pb[18], nP = 0;
static int Na[36], Nb[36], Ncnt[36], nN = 0;
static int okp[18][36];
static int x[9][9];
static int chN[18];
static long long cnt = 0;
static int dump = 0;
#include <stdlib.h>
static int knuth = 0;
static int inter(int a1, int b1, int a2, int b2) { return (a1 == a2) + (a1 == b2) + (b1 == a2) + (b1 == b2); }
static void rec(int i, int lastN) {
    if (i == 18) {
        cnt++;
        if (dump) {
            for (int k = 0; k < 18; k++) printf("%d %d %d %d\n", Pa[k], Pb[k], Na[chN[k]], Nb[chN[k]]);
            printf("\n");
        }
        return;
    }
    int lo = 0;
    if (i > 0 && Pa[i] == Pa[i - 1] && Pb[i] == Pb[i - 1]) lo = lastN + 1;
    for (int j = lo; j < nN; j++) {
        if (!Ncnt[j] || !okp[i][j]) continue;
        int p1 = Pa[i], p2 = Pb[i], v1 = Na[j], v2 = Nb[j];
        if (x[p1][v1] + 1 > 2 - D[p1][v1] || x[p1][v2] + 1 > 2 - D[p1][v2] ||
            x[p2][v1] + 1 > 2 - D[p2][v1] || x[p2][v2] + 1 > 2 - D[p2][v2]) continue;
        int bad = 0;
        for (int k = 0; k < i; k++)
            if (inter(p1, p2, Pa[k], Pb[k]) + inter(v1, v2, Na[chN[k]], Nb[chN[k]]) > 2) { bad = 1; break; }
        if (bad) continue;
        Ncnt[j]--; chN[i] = j;
        x[p1][v1]++; x[p1][v2]++; x[p2][v1]++; x[p2][v2]++;
        rec(i + 1, j);
        x[p1][v1]--; x[p1][v2]--; x[p2][v1]--; x[p2][v2]--;
        Ncnt[j]++;
    }
}
int main(int argc, char **argv) {
    char line[64];
    dump = (argc > 1 && strcmp(argv[1], "dump") == 0);
    knuth = (argc > 3 && strcmp(argv[1], "knuth") == 0);
    for (int p = 0; p < 9; p++) {
        if (scanf("%63s", line) != 1) return 1;
        for (int v = 0; v < 9; v++) D[p][v] = line[v] - '0';
    }
    for (int a = 0; a < 9; a++) for (int b = a + 1; b < 9; b++) {
        int c = 0; for (int v = 0; v < 9; v++) c += D[a][v] & D[b][v];
        for (int m = 0; m < 2 - c; m++) { Pa[nP] = a; Pb[nP] = b; nP++; }
    }
    for (int a = 0; a < 9; a++) for (int b = a + 1; b < 9; b++) {
        int c = 0; for (int p = 0; p < 9; p++) c += D[p][a] & D[p][b];
        if (2 - c > 0) { Na[nN] = a; Nb[nN] = b; Ncnt[nN] = 2 - c; nN++; }
    }
    if (nP != 18) { fprintf(stderr, "nP=%d\n", nP); return 2; }
    for (int i = 0; i < 18; i++) for (int j = 0; j < nN; j++) {
        int p1 = Pa[i], p2 = Pb[i], v1 = Na[j], v2 = Nb[j];
        okp[i][j] = (D[p1][v1] + D[p1][v2] <= 1) && (D[p2][v1] + D[p2][v2] <= 1) &&
                    (D[p1][v1] + D[p2][v1] <= 1) && (D[p1][v2] + D[p2][v2] <= 1);
    }
    if (knuth) {
        int trials = atoi(argv[2]); srand(atoi(argv[3]));
        double sum = 0, sum2 = 0; long long zero = 0;
        for (int t = 0; t < trials; t++) {
            double w = 1; int i = 0, lastN = -1;
            int stackj[18];
            while (i < 18) {
                int cand[36], nc = 0;
                int lo = 0;
                if (i > 0 && Pa[i] == Pa[i - 1] && Pb[i] == Pb[i - 1]) lo = lastN + 1;
                for (int j = lo; j < nN; j++) {
                    if (!Ncnt[j] || !okp[i][j]) continue;
                    int p1 = Pa[i], p2 = Pb[i], v1 = Na[j], v2 = Nb[j];
                    if (x[p1][v1] + 1 > 2 - D[p1][v1] || x[p1][v2] + 1 > 2 - D[p1][v2] ||
                        x[p2][v1] + 1 > 2 - D[p2][v1] || x[p2][v2] + 1 > 2 - D[p2][v2]) continue;
                    int bad = 0;
                    for (int k = 0; k < i; k++)
                        if (inter(p1, p2, Pa[k], Pb[k]) + inter(v1, v2, Na[chN[k]], Nb[chN[k]]) > 2) { bad = 1; break; }
                    if (!bad) cand[nc++] = j;
                }
                if (nc == 0) { w = 0; break; }
                int j = cand[rand() % nc]; w *= nc;
                int p1 = Pa[i], p2 = Pb[i], v1 = Na[j], v2 = Nb[j];
                Ncnt[j]--; chN[i] = j; stackj[i] = j;
                x[p1][v1]++; x[p1][v2]++; x[p2][v1]++; x[p2][v2]++;
                lastN = j; i++;
            }
            for (int k = i - 1; k >= 0; k--) {
                int j = stackj[k], p1 = Pa[k], p2 = Pb[k], v1 = Na[j], v2 = Nb[j];
                Ncnt[j]++; x[p1][v1]--; x[p1][v2]--; x[p2][v1]--; x[p2][v2]--;
            }
            if (w == 0) zero++;
            sum += w; sum2 += w * w;
        }
        double mean = sum / trials, sd = sqrt(sum2 / trials - mean * mean) / sqrt(trials);
        printf("%.4g %.3g %lld\n", mean, sd, zero);
        return 0;
    }
    rec(0, -1);
    if (!dump) printf("%lld\n", cnt);
    else fprintf(stderr, "%lld\n", cnt);
    return 0;
}
