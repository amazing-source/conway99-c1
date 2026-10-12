/* Lab session, 2026-10-12. Parity skeletons of S3-covers of the Brouwer-Haemers graph: exhaustive depth-first search
   with unit propagation, in the edge order that solved the Z3 case (work/audit_v7_2026-10-12/z3_classify.py).

   BH: V = F_3^4, x ~ y iff q(y - x) = 0, q = x0^2 + x1^2 + x2 x3. Unknown eps : 810 edges -> {0,1} with
     (T) eps even on each of the 270 lines;
     (L) for each of the 2430 non-adjacent pairs the six path parities eps(PZ) + eps(ZR) have weight 0, 3 or 6;
     gauge: vertices are placed one at a time (each time the vertex with most placed neighbours); the edge from a new
     vertex to its first placed neighbour is 0 (tree gauge: one representative per switching class).
   Solutions = switching classes of parity skeletons; the all-zero assignment is the trivial class.
   Propagation: a line with two known edges forces the third; a pair forces its unknown path parities when only one
   final weight is still possible (and an unknown parity with one known edge forces the other edge).
   Search: the edges in the order of placement; an unassigned edge is a decision (0 then 1).

   paritydfs [node cap] [mode]      mode 0: plain search from the root (prints the profile and every solution)
                                    mode 1 <dives> <seed>: Knuth estimate of the tree size by random dives
   gcc -O3 -march=native -o paritydfs paritydfs.c          One process, a few MB. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define NV 81
#define NE 810
#define NP 2430
static int adj[NV][NV], nbr[NV][20], eid[NV][NV], eu[NE], ev[NE];
static int line_other[NE][2];                        /* the two other edges of the line of an edge */
static int pslot[NP][6][2];                          /* edges of the six paths of a pair */
static int emem[NE][36], nmem[NE];                   /* pairs containing an edge */
static signed char val[NE]; static int trail[NE], ntrail, order[NE], gauge[NE];
static long long nodes, CAP = 1LL << 62, alive[NE + 1], nsol; static int stopped;
static unsigned long long rng = 88172645463325252ULL;
static unsigned long long rnd(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static int qf(const int *x) { return (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3; }

static int queue[NE * 4], qh, qt;
static int set(int e, int v) {                       /* returns 0 on conflict */
    if (val[e] >= 0) return val[e] == v;
    val[e] = (signed char)v; trail[ntrail++] = e; queue[qt++] = e; return 1;
}
static int propagate(void) {
    while (qh < qt) {
        int e = queue[qh++];
        int a = line_other[e][0], b = line_other[e][1];
        if (val[a] >= 0 && val[b] >= 0) { if ((val[a] ^ val[b] ^ val[e]) != 0) return 0; }
        else if (val[a] >= 0) { if (!set(b, val[a] ^ val[e])) return 0; }
        else if (val[b] >= 0) { if (!set(a, val[b] ^ val[e])) return 0; }
        for (int m = 0; m < nmem[e]; m++) {
            int p = emem[e][m], ones = 0, zeros = 0;
            for (int s = 0; s < 6; s++) {
                int x = val[pslot[p][s][0]], y = val[pslot[p][s][1]];
                if (x >= 0 && y >= 0) { if (x ^ y) ones++; else zeros++; }
            }
            int u = 6 - ones - zeros;
            int f0 = ones == 0, f3 = ones <= 3 && zeros <= 3, f6 = zeros == 0;
            if (!f0 && !f3 && !f6) return 0;
            if (!u) continue;
            int force = -1;                          /* value forced on every unknown path parity, if any */
            if (f0 && !f3 && !f6) force = 0;
            else if (f6 && !f0 && !f3) force = 1;
            else if (f3 && !f0 && !f6) { if (ones == 3) force = 0; else if (zeros == 3) force = 1; }
            else if (f0 && f3 && !f6) { if (3 > ones + u) force = 0; }      /* weight 3 not reachable */
            else if (f6 && f3 && !f0) { if (3 > zeros + u) force = 1; }
            if (force < 0) continue;
            for (int s = 0; s < 6; s++) {
                int e1 = pslot[p][s][0], e2 = pslot[p][s][1], x = val[e1], y = val[e2];
                if (x >= 0 && y < 0) { if (!set(e2, x ^ force)) return 0; }
                else if (y >= 0 && x < 0) { if (!set(e1, y ^ force)) return 0; }
            }
        }
    }
    return 1;
}
static void undo(int mark) { while (ntrail > mark) val[trail[--ntrail]] = -1; }

static void rec(int k, int depth) {
    if (stopped) return;
    while (k < NE && val[order[k]] >= 0) k++;
    if (k == NE) {
        nsol++; int w = 0; for (int e = 0; e < NE; e++) w += val[e];
        printf("SOLUTION %lld: %d negative edges%s\n", nsol, w, w ? "  ** NON-TRIVIAL **" : " (trivial class)");
        if (w) { for (int e = 0; e < NE; e++) putchar('0' + val[e]); putchar('\n'); }
        fflush(stdout); return;
    }
    int e = order[k];
    for (int v = 0; v < 2; v++) {
        if (++nodes > CAP) { stopped = 1; return; }
        int mark = ntrail; qh = qt = 0;
        if (set(e, v) && propagate()) { alive[depth + 1]++; rec(k + 1, depth + 1); }
        undo(mark);
        if (stopped) return;
    }
}

int main(int argc, char **argv) {
    if (argc > 1) CAP = atoll(argv[1]);
    int mode = argc > 2 ? atoi(argv[2]) : 0;
    int X[NV][4]; for (int i = 0; i < NV; i++) { int t = i; for (int j = 3; j >= 0; j--) { X[i][j] = t % 3; t /= 3; } }
    int ne = 0; memset(eid, -1, sizeof eid);
    for (int i = 0; i < NV; i++) { int d = 0; for (int j = 0; j < NV; j++) { int df[4]; for (int c = 0; c < 4; c++) df[c] = (X[j][c] - X[i][c] + 3) % 3; adj[i][j] = (i != j && qf(df) == 0); if (adj[i][j]) nbr[i][d++] = j; } if (d != 20) return 2; }
    /* vertex order, edges in order of placement, gauge */
    int pos[NV], placed[NV], np = 0; memset(pos, -1, sizeof pos);
    /* PARITY_ORDER=line: the line {0, e, 2e} first (vertices 0, 3, 6), then its three layers, then the far vertices
       (line gauge of parity_line.py); inside a class, the vertex with most placed neighbours first */
    int cls[NV], useline = getenv("PARITY_ORDER") != NULL;
    for (int v = 0; v < NV; v++) { cls[v] = 0; if (useline) { if (v == 0 || v == 3 || v == 6) cls[v] = 0; else if (adj[v][0]) cls[v] = 1; else if (adj[v][3]) cls[v] = 2; else if (adj[v][6]) cls[v] = 3; else cls[v] = 4; } }
    placed[np] = 0; pos[0] = np++;
    while (np < NV) {
        int best = -1, bc = -1, bcl = 99;
        for (int v = 0; v < NV; v++) if (pos[v] < 0) { int c = 0; for (int d = 0; d < 20; d++) if (pos[nbr[v][d]] >= 0) c++; if (cls[v] < bcl || (cls[v] == bcl && c > bc)) { bcl = cls[v]; bc = c; best = v; } }
        int first = 1;
        for (int i = 0; i < np; i++) if (adj[best][placed[i]]) { eu[ne] = placed[i]; ev[ne] = best; eid[best][placed[i]] = eid[placed[i]][best] = ne; gauge[ne] = first; first = 0; order[ne] = ne; ne++; }
        placed[np] = best; pos[best] = np++;
    }
    if (ne != NE) return 2;
    for (int e = 0; e < NE; e++) { int a = eu[e], b = ev[e], c = -1; for (int d = 0; d < 20; d++) if (adj[b][nbr[a][d]]) c = nbr[a][d]; line_other[e][0] = eid[a][c]; line_other[e][1] = eid[b][c]; }
    int npair = 0;
    for (int a = 0; a < NV; a++) for (int b = a + 1; b < NV; b++) if (!adj[a][b]) {
        int s = 0; for (int d = 0; d < 20; d++) { int z = nbr[a][d]; if (adj[z][b]) { pslot[npair][s][0] = eid[a][z]; pslot[npair][s][1] = eid[z][b]; s++; } }
        if (s != 6) return 2;
        for (int t = 0; t < 6; t++) for (int h = 0; h < 2; h++) { int e = pslot[npair][t][h]; emem[e][nmem[e]++] = npair; }
        npair++;
    }
    if (npair != NP) return 2;
    memset(val, -1, sizeof val); ntrail = 0; qh = qt = 0;
    int ok = 1; for (int e = 0; e < NE && ok; e++) if (gauge[e]) ok = set(e, 0);
    ok = ok && propagate();
    int nfree = 0; for (int e = 0; e < NE; e++) if (val[e] < 0) nfree++;
    printf("BH built; gauge edges 80; after propagation of the gauge: %d edges assigned, %d unassigned; consistent: %d\n", NE - nfree, nfree, ok);
    double t0 = now();
    if (mode == 0) {
        rec(0, 0);
        printf("search %s: %lld nodes, %lld solutions  [%.1f s]\n", stopped ? "STOPPED at the node cap" : "exhaustive", nodes, nsol, now() - t0);
        printf("assignments alive after each decision:"); for (int d = 1; d <= NE && alive[d]; d++) printf(" %lld", alive[d]); printf("\n");
    } else {
        long long dives = argc > 3 ? atoll(argv[3]) : 1000; if (argc > 4) rng ^= (unsigned long long)atoll(argv[4]) * 0x9E3779B97F4A7C15ULL;
        static double sumw[NE + 1]; int base = ntrail, maxd = 0; double tot = 0;
        for (long long dv = 0; dv < dives; dv++) {
            double w = 1; int k = 0, depth = 0;
            for (;;) {
                while (k < NE && val[order[k]] >= 0) k++;
                if (k == NE) { printf("dive %lld reached a full assignment\n", dv); break; }
                int e = order[k], okv[2], nok = 0;
                for (int v = 0; v < 2; v++) { int mark = ntrail; qh = qt = 0; if (set(e, v) && propagate()) okv[nok++] = v; undo(mark); }
                if (!nok) break;
                w *= nok; depth++; sumw[depth] += w; if (depth > maxd) maxd = depth;
                int v = okv[rnd() % nok]; qh = qt = 0; set(e, v); propagate();
            }
            undo(base);
        }
        printf("Knuth estimate from %lld dives: alive assignments after each decision:", dives);
        for (int d = 1; d <= maxd; d++) { printf(" %.3g", sumw[d] / dives); tot += sumw[d] / dives; }
        printf("\nestimated total number of alive nodes %.3g; deepest decision level reached %d  [%.1f s]\n", tot, maxd, now() - t0);
    }
    return 0;
}
