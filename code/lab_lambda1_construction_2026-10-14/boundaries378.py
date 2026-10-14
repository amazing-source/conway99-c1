"""Geometric kept sets R (|R| <= ~110) in the S3 hemisystem graph srg(378,52,1,8), compared with random kept sets of the
same size, through the concentration criterion of rigidity378.py (14/10/2026): for F = V - R, dimension of the
(-11)-eigenvectors supported in F and the best product P_ii P_jj (a trade needs >= 1/900). Kept sets:
  N[v]            closed neighbourhood of a vertex (53)
  N[v] u N[w]     two adjacent vertices (103) / two non-adjacent (98)
  X_m             H-lines meeting a GQ line m outside H (78; every outside vertex has 13 neighbours in it)
  T_P-star        the 3 H-lines through a GQ point P and all their neighbours (3 + 3*50 = 153: too big, skipped)
  X_m u N[v]      mixed
usage: python boundaries378.py <gq.json> <hemi.json> <edges>"""
import json
import random
import sys

import numpy as np

gqf, hf, ef = sys.argv[1], sys.argv[2], sys.argv[3]
G = json.load(open(gqf))
H = json.load(open(hf))
E = [tuple(map(int, l.split())) for l in open(ef) if l.strip()]
n = 1 + max(max(e) for e in E)
A = np.zeros((n, n))
for a, b in E:
    A[a, b] = A[b, a] = 1
w, V = np.linalg.eigh(A)
Q11 = V[:, np.abs(w + 11) < 1e-6]
adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]


def conc(R):
    R = sorted(R)
    M = Q11[R, :]
    u, sv, vt = np.linalg.svd(M, full_matrices=True)
    rank = int((sv > 1e-8).sum())
    N = vt[rank:].T
    Y = Q11 @ N
    if Y.shape[1] == 0:
        return 0, 0.0, 0.0
    d = (Y ** 2).sum(1)
    top = np.sort(d)[-2:]
    return Y.shape[1], float(d.max()), float(top[0] * top[1])


lines = [set(l) for l in G["lines"]]
Hs = set(H)
nonH = [i for i in range(len(lines)) if i not in Hs]
X = {m: {kk for kk, h in enumerate(H) if lines[h] & lines[m]} for m in nonH}
rng = random.Random(3)
cases = []
v = rng.randrange(n)
cases.append(("N[v]", {v} | adj[v]))
wv = next(iter(adj[v]))
cases.append(("N[v] u N[w], v ~ w", {v, wv} | adj[v] | adj[wv]))
wn = next(x for x in range(n) if x != v and x not in adj[v])
cases.append(("N[v] u N[w], v !~ w", {v, wn} | adj[v] | adj[wn]))
m = nonH[0]
cases.append(("X_m", set(X[m])))
cases.append(("X_m u N[v] (v in X_m)", set(X[m]) | {min(X[m])} | adj[min(X[m])]))
for label, R in cases:
    d, mx, pr = conc(R)
    dr, mxr, prr = conc(set(rng.sample(range(n), len(R))))
    print("%-28s |R| = %3d, |F| = %3d: geometric -> dim %3d, max P_ii %.4f, pair %.5f %s | random same size -> dim %3d, "
          "pair %.5f %s" % (label, len(R), n - len(R), d, mx, pr, "OK" if pr >= 1 / 900 else "rigid", dr, prr,
                            "OK" if prr >= 1 / 900 else "rigid"), flush=True)
