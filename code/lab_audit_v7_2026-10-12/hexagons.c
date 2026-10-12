/* Lab session, 2026-10-12. Independent count of the induced hexagons (6-cycles without chord) of a graph on 243
   vertices given as an edge list; check of the column "hexagones" of note 165 (branch claude/v7-simultaneous).
   For every induced path a-b-c-d (a not adjacent to c, d; b not adjacent to d; counted once, a < d) the pairs (e, f)
   with e ~ d, f ~ a, e ~ f, e adjacent to none of a, b, c and f adjacent to none of b, c, d close it into an induced
   hexagon; every hexagon is obtained from its 6 paths.     gcc -O2 -o hexagons hexagons.c ;  hexagons file.edges */
#include <stdio.h>
#include <string.h>
typedef unsigned long long u64;
#define N 243
static u64 adj[N][4];
static int A[N][N];
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); int i, j; long long m = 0;
    if (!f) return 1;
    while (fscanf(f, "%d %d", &i, &j) == 2) { A[i][j] = A[j][i] = 1; adj[i][j >> 6] |= 1ULL << (j & 63); adj[j][i >> 6] |= 1ULL << (i & 63); m++; }
    long long total = 0, paths = 0;
    for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) if (A[a][b])
        for (int c = 0; c < N; c++) if (A[b][c] && c != a && !A[a][c])
            for (int d = a + 1; d < N; d++) if (A[c][d] && d != b && !A[b][d] && !A[a][d]) {
                paths++;
                u64 E[4], F[4];
                for (int w = 0; w < 4; w++) { E[w] = adj[d][w] & ~(adj[a][w] | adj[b][w] | adj[c][w]); F[w] = adj[a][w] & ~(adj[b][w] | adj[c][w] | adj[d][w]); }
                E[c >> 6] &= ~(1ULL << (c & 63)); F[b >> 6] &= ~(1ULL << (b & 63));
                for (int w = 0; w < 4; w++) for (u64 bits = E[w]; bits; bits &= bits - 1) {
                    int e = 64 * w + __builtin_ctzll(bits);
                    for (int x = 0; x < 4; x++) total += __builtin_popcountll(adj[e][x] & F[x]);
                }
            }
    printf("%s: %lld edges, induced paths on 4 vertices %lld, induced hexagons %lld%s\n", argv[1], m, paths, total / 6, total % 6 ? " (NOT divisible by 6!)" : "");
    return 0;
}
