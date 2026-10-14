"""Validation of (DISC) on a real srg(243,22,1,2) (15/10/2026).
T' = Schur complement of (4I - A) on N[v] (the analogue of T, r = 4, s = -5); expected T'^2 = 9 T', rank 110 - 22 = 88.
Then disc(lattice of all 220 label vectors, Gram c T') may contain only the primes of 9c, and every full-rank subset
has disc = that x a square.  usage: python disc243_check.py <edges file> [v] [subset size] [seed]"""
import sys, random
from fractions import Fraction as Fr
import numpy as np
import latdisc
E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
n = 1 + max(max(e) for e in E)
A = np.zeros((n, n), dtype=np.int64)
for a, b in E: A[a, b] = A[b, a] = 1
assert np.all(A.sum(1) == 22)
A2 = A @ A
assert np.all(A2[A == 1] == 1) and np.all(A2[(A == 0) & ~np.eye(n, dtype=bool)] == 2)
v = int(sys.argv[2]) if len(sys.argv) > 2 else 0
Nv = [v] + [int(x) for x in np.nonzero(A[v])[0]]
L = [x for x in range(n) if x not in Nv]
print("srg(243,22,1,2) checked; |N[v]| = %d, labels %d" % (len(Nv), len(L)))
# exact inverse of 4I - A on N[v]
m = len(Nv)
M = [[Fr((4 if i == j else 0) - int(A[Nv[i], Nv[j]])) for j in range(m)] for i in range(m)]
Aug = [row[:] + [Fr(1 if i == j else 0) for j in range(m)] for i, row in enumerate(M)]
for c in range(m):
    p = next(i for i in range(c, m) if Aug[i][c] != 0)
    Aug[c], Aug[p] = Aug[p], Aug[c]
    pv = Aug[c][c]; Aug[c] = [x / pv for x in Aug[c]]
    for i in range(m):
        if i != c and Aug[i][c] != 0:
            f = Aug[i][c]; Aug[i] = [x - f * y for x, y in zip(Aug[i], Aug[c])]
Minv = [row[m:] for row in Aug]
# T' = (4I - A)_LL - A_LN Minv A_NL ; A_LN has entries 0/1
ALN = [[int(A[x, y]) for y in Nv] for x in L]
nb = [[k for k in range(m) if ALN[i][k]] for i in range(len(L))]
T = []
for i in range(len(L)):
    row = []
    for j in range(len(L)):
        s = sum(Minv[a][b] for a in nb[i] for b in nb[j])
        row.append(Fr((4 if i == j else 0) - int(A[L[i], L[j]])) - s)
    T.append(row)
import math
c = 1
for row in T:
    for x in row: c = c * x.denominator // math.gcd(c, x.denominator)
Tf = np.array([[float(x) for x in row] for row in T])
print("scale c = %d; ||T'^2 - 9T'|| = %.2e; numerical rank %d" % (c, np.abs(Tf @ Tf - 9 * Tf).max(), np.linalg.matrix_rank(Tf, 1e-8)))
G = [[int(x * c) for x in row] for row in T]
r, disc = latdisc.lattice_disc(G)
f, cof = latdisc.factor_small(disc)
print("ALL labels: rank %d, disc = %s, cofactor %d" % (r, f, cof))
size = int(sys.argv[3]) if len(sys.argv) > 3 else 120
rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
for t in range(3):
    S = sorted(rng.sample(range(len(L)), size))
    GS = [[G[a][b] for b in S] for a in S]
    rS, dS = latdisc.lattice_disc(GS)
    fS, cofS = latdisc.factor_small(dS)
    q = dS // disc if dS % disc == 0 else None
    sq = (q is not None) and math.isqrt(q) ** 2 == q
    print("random subset %d: rank %d, disc = %s cof %d; disc_S / disc_all = %s, perfect square: %s" % (size, rS, fS, cofS, q if q is None or q < 10**30 else "big", sq))
