/* Lab session, 2026-10-12. The depth-first search of z3_classify.py in C: all the Z3-gain functions b on the edges of
   the Brouwer-Haemers graph such that the cover is a srg(243,22,1,2), in the gauge and edge order of the model file
   written by z3_classify.py (environment variable Z3_EXPORT).

   Along the edge order an edge is free (3 values) or determined by earlier edges (linear relation over F_3). When an
   edge is set, some values c_Z = c1 b_e1 + c2 b_e2 of non-adjacent pairs become known; a pair must end with the values
   0, 1, 2 twice each, so a value met three times is a dead end.
   Symmetry used: b -> -b maps solutions to solutions and keeps the gauge, so the first non-zero FREE value is taken
   equal to 1 (option "half"); every solution found then stands for itself and its opposite.

   z3cov <model.txt> <solutions.txt> [half|full] [L [first last]]
   L: report on stderr every finished top-level branch (= alive assignment of the first L free edges); first, last:
   search only the branches first <= id < last (to cut the run into pieces; the pieces partition the search).
   Output: the solutions (one line of digits each) and the number of nodes.   gcc -O3 -march=native -o z3cov z3cov.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define MAXE 900
#define MAXP 2600
static int E, NP, isfree[MAXE], nd[MAXE], *de[MAXE], *dc[MAXE], nr[MAXE], *rp[MAXE], *rs[MAXE];
static int pt[MAXP][6][4];
static signed char x[MAXE]; static unsigned char cnt[MAXP][3];
static long long nodes, nsol, alive[MAXE + 1]; static FILE *fo; static int HALF, freerank[MAXE], PROG = 0, BR_LO = 0, BR_HI = 1 << 30, branch_id; static double T0;
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static void rec(int k, int nonzero) {
    if (k == E) { nsol++; for (int e = 0; e < E; e++) fputc('0' + x[e], fo); fputc('\n', fo); return; }
    int lo = 0, hi = 2;
    if (!isfree[k]) { int s = 0; for (int i = 0; i < nd[k]; i++) s += dc[k][i] * x[de[k][i]]; lo = hi = ((3 - s % 3) % 3); }
    else if (HALF && !nonzero) hi = 1;
    for (int val = lo; val <= hi; val++) {
        nodes++;
        x[k] = (signed char)val; int ok = 1, done = 0;
        for (int i = 0; i < nr[k]; i++) {
            int pi = rp[k][i], s = rs[k][i], c = (pt[pi][s][1] * x[pt[pi][s][0]] + pt[pi][s][3] * x[pt[pi][s][2]]) % 3;
            done = i + 1;
            if (++cnt[pi][c] > 2) { ok = 0; break; }
        }
        if (ok) {
            alive[k + 1]++;
            if (isfree[k] && freerank[k] == PROG - 1) {            /* one top-level branch = the values of the first PROG free edges */
                int id = branch_id++;
                if (id >= BR_LO && id < BR_HI) {
                    long long n0 = nodes, s0 = nsol; rec(k + 1, nonzero || val != 0);
                    fprintf(stderr, "branch %d done: %lld nodes, %lld solutions, %.1f s\n", id, nodes - n0, nsol - s0, now() - T0); fflush(stderr); fflush(fo);
                }
            } else rec(k + 1, nonzero || (isfree[k] && val != 0));
        }
        for (int i = 0; i < done; i++) {
            int pi = rp[k][i], s = rs[k][i], c = (pt[pi][s][1] * x[pt[pi][s][0]] + pt[pi][s][3] * x[pt[pi][s][2]]) % 3;
            cnt[pi][c]--;
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: z3cov <model.txt> <solutions.txt> [half|full]\n"); return 1; }
    FILE *f = fopen(argv[1], "r"); if (!f) return 1;
    HALF = !(argc > 3 && !strcmp(argv[3], "full"));
    if (fscanf(f, "%d %d", &E, &NP) != 2 || E > MAXE || NP > MAXP) return 2;
    int nfree = 0;
    for (int k = 0; k < E; k++) {
        char t[4]; if (fscanf(f, "%3s", t) != 1) return 2;
        if (t[0] == 'F') { isfree[k] = 1; nfree++; continue; }
        if (fscanf(f, "%d", &nd[k]) != 1) return 2;
        de[k] = malloc(sizeof(int) * (nd[k] + 1)); dc[k] = malloc(sizeof(int) * (nd[k] + 1));
        for (int i = 0; i < nd[k]; i++) if (fscanf(f, "%d %d", &de[k][i], &dc[k][i]) != 2) return 2;
    }
    for (int k = 0; k < E; k++) {
        if (fscanf(f, "%d", &nr[k]) != 1) return 2;
        rp[k] = malloc(sizeof(int) * (nr[k] + 1)); rs[k] = malloc(sizeof(int) * (nr[k] + 1));
        for (int i = 0; i < nr[k]; i++) if (fscanf(f, "%d %d", &rp[k][i], &rs[k][i]) != 2) return 2;
    }
    for (int p = 0; p < NP; p++) for (int s = 0; s < 6; s++) for (int j = 0; j < 4; j++) if (fscanf(f, "%d", &pt[p][s][j]) != 1) return 2;
    fclose(f);
    fo = fopen(argv[2], "w"); if (!fo) return 3;
    { int r = 0; for (int k = 0; k < E; k++) freerank[k] = isfree[k] ? r++ : -1; }
    if (argc > 4) PROG = atoi(argv[4]);
    if (argc > 6) { BR_LO = atoi(argv[5]); BR_HI = atoi(argv[6]); }
    double t0 = now(); T0 = t0;
    rec(0, 0);
    fclose(fo);
    printf("model: %d edges (%d free), %d pairs; symmetry b -> -b %s\n", E, nfree, NP, HALF ? "used (first non-zero free value = 1)" : "not used");
    printf("search %s: %lld nodes, %lld solutions written%s  [%.1f s]\n", (BR_LO == 0 && BR_HI == (1 << 30)) ? "exhaustive" : "of the requested branches", nodes, nsol, HALF ? " (each stands for itself and its opposite)" : "", now() - t0);
    if (PROG) printf("top-level branches (alive assignments of the first %d free edges): %d; searched: %d .. %d\n", PROG, branch_id, BR_LO, BR_HI < branch_id ? BR_HI - 1 : branch_id - 1);
    printf("partial assignments alive after each free edge:");
    for (int k = 0; k < E; k++) if (isfree[k]) printf(" %lld", alive[k + 1]);
    printf("\n");
    return 0;
}
