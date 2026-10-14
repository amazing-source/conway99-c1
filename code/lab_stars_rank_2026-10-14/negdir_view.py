"""Negative directions of T_S for a saved three-star structure with an extra relation (14/10/2026).
Prints the negative eigenvalues of T_S, the composition of the most negative eigenvector by region (X, C4, B),
its overlap with the extra relation, and the Rayleigh quotients of simple test vectors built from the relation
(positive part, negative part, level sets).  usage: python negdir_view.py <found json> [index]"""
import json
import sys
import numpy as np
from stars_rank import kval

d = json.load(open(sys.argv[1]))
k = int(sys.argv[2]) if len(sys.argv) > 2 else 0
S = [frozenset(l) for l in d["labels"]]
n = len(S)
G = np.zeros((n, n))
for i, j in d["found"][k]["edges"]:
    G[i, j] = G[j, i] = 1
T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
ev, V = np.linalg.eigh(T)
print("eigenvalues of T_S below 1e-9:", ["%.4f" % x for x in ev if x < 1e-9])
reg = {"X only": [i for i in range(n) if (0 in S[i] or 1 in S[i]) and 2 not in S[i] and 3 not in S[i]],
       "C4": [i for i in range(n) if (0 in S[i] or 1 in S[i]) and (2 in S[i] or 3 in S[i])],
       "B (L2 minus X)": [i for i in range(n) if 2 in S[i] and not (0 in S[i] or 1 in S[i])]}
u = V[:, 0]
for name, ids in reg.items():
    print("   most negative eigenvector: mass on %-14s %.3f" % (name, float(np.sum(u[ids] ** 2))))
# kernel of T (numerical) and the extra relation: orthogonal complement of stars inside the kernel
ker = V[:, np.abs(ev) < 1e-9]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2)]).T
Qz, _ = np.linalg.qr(Z)
Pk = ker - Qz @ (Qz.T @ ker)
U_, s_, _ = np.linalg.svd(Pk)
z = U_[:, 0]
print("extra relation (unit, orthogonal to stars): overlap with most negative eigenvector %.3f" % abs(z @ u))
for name, ids in reg.items():
    print("   relation mass on %-14s %.3f" % (name, float(np.sum(z[ids] ** 2))))
for name, y in (("positive part", np.maximum(z, 0)), ("negative part", np.maximum(-z, 0))):
    y = y - Qz @ (Qz.T @ y)
    print("Rayleigh quotient of the %s of the relation (stars removed): %.4f" % (name, y @ T @ y / (y @ y)))
