"""C1, lab session, 2026-10-12. Checks on Codex's matrix H of the co-Heawood branch (its note of 12/10, formula (1)):
  H_rr = 36 - 6 B_st,   H_rr' = 12 - 21 e - 9 ([s=u] + [t=v]) - 7 q - 3 (B_sv + B_ut)
for boundary vertices r in cell (s,t), r' in cell (u,v); e = adjacency, q = number of common far neighbours.
 1. modulo 7, H depends only on the cells; rank of the 49 x 49 cell matrix modulo 7 (hand: 5);
 2. one row (the ten boundary neighbours of a core point, far vertices = edges of a cubic graph G on them):
    H_row = F - 7 A(G), F fixed; for every base orbit of the catalogue read: kernel contains 1, rank, least and
    largest eigenvalue (must lie in [0, 147]), squared Frobenius norm (hand: 15 024 whatever G).
python h_structure_check.py <bases_orbits.txt> [number of bases, default all]      One process, numpy, < 1 minute."""
import sys
import numpy as np
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
B = [[1 if x not in LINES[y] else 0 for y in range(7)] for x in range(7)]

def rank7(M):
    M = [[int(v) % 7 for v in r] for r in M]; n = len(M); m = len(M[0]); r = 0
    for c in range(m):
        p = next((i for i in range(r, n) if M[i][c]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; iv = pow(M[r][c], 5, 7); M[r] = [x * iv % 7 for x in M[r]]
        for i in range(n):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(x - f * y) % 7 for x, y in zip(M[i], M[r])]
        r += 1
    return r

cells = [(s, t) for s in range(7) for t in range(7)]
h = [[(12 - 9 * ((s == u) + (t == v)) - 3 * (B[s][v] + B[u][t])) % 7 for (u, v) in cells] for (s, t) in cells]
# same cell: single: diagonal 36 - 6 = 30 = 2; double: 36 = 1 on the diagonal and 12 - 18 - 0 = -6 = 1 between twins
ok = all(h[i][i] == ((30 if B[s][t] else 36) % 7) for i, (s, t) in enumerate(cells))
print("1. H modulo 7 is the blow-up of the cell matrix (diagonal and twins consistent: %s); its rank modulo 7: %d" % (ok, rank7(h)))

# one row: positions 0..3 singles (lines not through 0: 3,4,5,6), 4,5 twins of line 0, 6,7 line 1, 8,9 line 2; matching (4,6),(5,8),(7,9)
lab = [3, 4, 5, 6, 0, 0, 1, 1, 2, 2]; match = {(4, 6), (5, 8), (7, 9)}
def Hrow(edges):
    A = np.zeros((10, 10), dtype=np.int64)
    for a, b in edges: A[a, b] = A[b, a] = 1
    H = np.zeros((10, 10), dtype=np.int64)
    for i in range(10):
        for j in range(10):
            if i == j: H[i, j] = 36 - 6 * B[0][lab[i]]
            else:
                e = 1 if (min(i, j), max(i, j)) in match else 0
                H[i, j] = 12 - 21 * e - 9 * (1 + (lab[i] == lab[j])) - 7 * A[i, j] - 3 * (B[0][lab[j]] + B[0][lab[i]])
    return H
lines = [l for l in open(sys.argv[1]).read().split("\n") if l.strip()]
nb = int(sys.argv[2]) if len(sys.argv) > 2 else len(lines)
ranks = {}; fro = set(); lo = 1e9; hi = -1e9; bad = 0; ker1 = True
for l in lines[:nb]:
    w = [int(t) for t in l.split()]; edges = [(w[1 + 2 * k], w[2 + 2 * k]) for k in range(15)]
    H = Hrow(edges)
    if (H.sum(0) != 0).any(): ker1 = False
    ev = np.linalg.eigvalsh(H.astype(float)); r = int((ev > 1e-7).sum()) + int((ev < -1e-7).sum())
    ranks[r] = ranks.get(r, 0) + 1; fro.add(int((H * H).sum())); lo = min(lo, ev[0]); hi = max(hi, ev[-1])
    if ev[0] < -1e-7 or ev[-1] > 147 + 1e-7: bad += 1
print("2. %d base orbits: kernel contains 1: %s; ranks %s; squared Frobenius norms %s; eigenvalues in [%.4f, %.4f]; bases with an eigenvalue outside [0, 147]: %d"
      % (min(nb, len(lines)), ker1, sorted(ranks.items()), sorted(fro), lo, hi, bad))
