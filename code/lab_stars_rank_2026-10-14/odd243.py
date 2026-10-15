"""ODD-type law in REAL srg(243,22,1,2) graphs (LAB 15/10/2026).
For a vertex v and two lines l = {v,a,a'}, m = {v,b,b'}: labels = far vertices (each is z_xy, the second common
neighbour of two non-mate letters x, y); T = Schur complement of 4I - A after N[v] on the labels (PSD, T^2 = 9T).
X_l = labels adjacent to a or a'; f_y = e(z_by) - e(z_b'y) for the 18 letters y off l and m.  The odd gain beyond X_l
is rank T on X_l + span(f_y) minus rank T on X_l; it is at most 17 (sum of the f_y is a star difference modulo X_l).
The 99 analogue (gain 9 = ODD9) is open.  Ranks numerically (eigenvalues of T are 0 and 9).
usage: python odd243.py <edges file> [vertices to test, default 3] [line pairs per vertex, default all]"""
import itertools
import sys

import numpy as np

E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
nv = 1 + max(max(e) for e in E)
A = np.zeros((nv, nv))
for i, j in E:
    A[i, j] = A[j, i] = 1
assert set(A.sum(1)) == {22.0}
nverts = int(sys.argv[2]) if len(sys.argv) > 2 else 3
maxpairs = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9


def rank(M, tol=1e-7):
    return int(np.sum(np.abs(np.linalg.eigvalsh((M + M.T) / 2)) > tol))


hist = {}
for v in range(nverts):
    Nv = [u for u in range(nv) if A[v, u]]
    mate = {}
    for x in Nv:
        mate[x] = [y for y in Nv if A[x, y]][0]
    far = [u for u in range(nv) if u != v and not A[v, u]]
    NN = [v] + Nv
    M = 4 * np.eye(nv) - A
    T = M[np.ix_(far, far)] - M[np.ix_(far, NN)] @ np.linalg.solve(M[np.ix_(NN, NN)], M[np.ix_(NN, far)])
    fpos = {u: i for i, u in enumerate(far)}
    lab = {}
    for x, y in itertools.combinations(Nv, 2):
        if mate[x] == y:
            continue
        z = [u for u in far if A[u, x] and A[u, y]]
        assert len(z) == 1
        lab[frozenset((x, y))] = fpos[z[0]]
    lines = []
    for x in Nv:
        if x < mate[x]:
            lines.append((x, mate[x]))
    pairs = list(itertools.permutations(lines, 2))[:maxpairs]
    for (a, a2), (b, b2) in pairs:
        Xl = sorted({lab[frozenset((s, x))] for s in (a, a2) for x in Nv if x not in (s, mate[s])})
        outer = [y for y in Nv if y not in (a, a2, b, b2)]
        F = np.zeros((len(far), len(outer)))
        for k, y in enumerate(outer):
            F[lab[frozenset((b, y))], k] = 1
            F[lab[frozenset((b2, y))], k] = -1
        B = np.zeros((len(far), len(Xl)))
        for k, i in enumerate(Xl):
            B[i, k] = 1
        B2 = np.hstack([B, F])
        g = rank(B2.T @ T @ B2) - rank(B.T @ T @ B)
        cl = 2 * 20 - 1 - rank(B.T @ T @ B)
        hist[(g, cl)] = hist.get((g, cl), 0) + 1
print(sys.argv[1], "histogram (odd gain beyond X_l, c(l) = 39 - rank T_X):", dict(sorted(hist.items())))
