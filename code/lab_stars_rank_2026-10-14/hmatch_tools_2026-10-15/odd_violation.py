"""Why does U fail on broken structures? (LAB 15/10/2026, task T3).

For broken structures Gamma (not h-invariant), the h-odd block of U is C' = Q_-^T (7 Pi - T) Q_-, and it depends only on
the average Gamma_0 = (Gamma + h Gamma h)/2.  Here: enumerate the structures sharing a kernel (as kernel_sat_measure.py),
keep the broken ones whose C' is not PSD, and print the most negative eigenvector of C' in the natural h-odd basis
(e_y = 1_0y - 1_1y, f_y = 1_2y - 1_3y for y = 4..13, k1 = 1_02 - 1_13, k2 = 1_03 - 1_12), together with the broken
orbits of Gamma (pairs {p, h p} carrying exactly one edge).  usage: python odd_violation.py <structure json> [max shown]"""
import itertools
import json
import random
import sys
from collections import Counter

import numpy as np
from pycryptosat import Solver

sys.path.insert(0, '.')
from stars_rank import build, kval, LABELS
from cls_decomp import nullspace_int

f = sys.argv[1]
mshow = int(sys.argv[2]) if len(sys.argv) > 2 else 6
d = json.load(open(f))
S, idx, e, F = build([0, 1, 2, 3], random.Random(5))
n = len(S)
E0 = {tuple(sorted(x)) for x in d["edges"]}
K8 = [[int(round(8 * kval(a, b))) for b in S] for a in S]
G0 = [[1 if tuple(sorted((a, b))) in E0 else 0 for b in range(n)] for a in range(n)]
M = [[(24 if a == b else 0) - 8 * G0[a][b] - K8[a][b] for b in range(n)] for a in range(n)]
N = nullspace_int(M)
sol = Solver()
for c in F.clauses:
    sol.add_clause(c)
nv = F.n
for vec in N:
    for i in range(n):
        tot = sum((24 if i == j else 0) * vec[j] - K8[i][j] * vec[j] for j in range(n))
        r = tot // 8
        terms = [(e[(i, j)], vec[j]) for j in range(n) if j != i and vec[j]]
        if not terms:
            continue
        kk = len(terms)
        lo, hi = [0] * (kk + 1), [0] * (kk + 1)
        for t in range(kk - 1, -1, -1):
            lo[t] = lo[t + 1] + min(0, terms[t][1])
            hi[t] = hi[t + 1] + max(0, terms[t][1])
        layer = {0: None}
        for t, (x, c) in enumerate(terms):
            nxt = {}
            for v, yv in layer.items():
                for val, lit in ((v, -x), (v + c, x)):
                    if not (val + lo[t + 1] <= r <= val + hi[t + 1]):
                        sol.add_clause([-lit] if yv is None else [-yv, -lit])
                        continue
                    if val not in nxt:
                        nv += 1
                        nxt[val] = nv
                    sol.add_clause([-lit, nxt[val]] if yv is None else [-yv, -lit, nxt[val]])
            layer = nxt
Kf = np.array([[kval(a, b) for b in S] for a in S])
D84 = np.zeros((14, 84))
for jj, l in enumerate(LABELS):
    for y in l:
        D84[y, jj] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: ii for ii, l in enumerate(LABELS)}
P7 = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
L = lambda *x: idx[frozenset(x)]
basis, names = [], []
for y in range(4, 14):
    v = np.zeros(n); v[L(0, y)], v[L(1, y)] = 1, -1
    basis.append(v); names.append("e%d" % y)
for y in range(4, 14):
    v = np.zeros(n); v[L(2, y)], v[L(3, y)] = 1, -1
    basis.append(v); names.append("f%d" % y)
v = np.zeros(n); v[L(0, 2)], v[L(1, 3)] = 1, -1
basis.append(v); names.append("k1")
v = np.zeros(n); v[L(0, 3)], v[L(1, 2)] = 1, -1
basis.append(v); names.append("k2")
Bm = np.array(basis).T                         # n x 22, h-odd basis (not orthonormal)
pairs = list(itertools.combinations(range(n), 2))
shown = 0
stats = Counter()
while shown < mshow:
    ok, model = sol.solve()
    if not ok:
        break
    sol.add_clause([-e[p] if model[e[p]] else e[p] for p in pairs])
    G = np.zeros((n, n))
    for p in pairs:
        if model[e[p]]:
            G[p] = 1
            G[p[1], p[0]] = 1
    brk = [(i, j) for i, j in pairs if G[i, j] != G[hp[i], hp[j]] and (min(hp[i], hp[j]), max(hp[i], hp[j])) > (i, j)]
    if not brk:
        continue
    T = 3 * np.eye(n) - G - Kf
    Up = Bm.T @ (P7 - T) @ Bm                    # Gram of U on the h-odd basis
    Gm = Bm.T @ Bm
    # generalised eigenproblem Up x = mu Gm x (Gm > 0)
    Lc = np.linalg.cholesky(Gm)
    Li = np.linalg.inv(Lc)
    w, V = np.linalg.eigh(Li @ Up @ Li.T)
    if w[0] > -1e-9:
        stats["odd U block PSD"] += 1
        continue
    x = Li.T @ V[:, 0]
    x = x / np.abs(x).max()
    shown += 1
    stats["odd U block NOT PSD"] += 1
    print("broken orbits (%d): %s" % (len(brk), ", ".join("%s-%s" % ("".join(map(str, sorted(S[i]))), "".join(map(str, sorted(S[j]))))
                                                         for i, j in brk)))
    print("  min eigenvalue %.4f; eigenvector (|coef| > 0.05): %s" % (w[0], ", ".join("%s:%.2f" % (names[k], x[k]) for k in range(22) if abs(x[k]) > 0.05)))
print(stats)
