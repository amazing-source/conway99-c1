"""Anatomy of a near-saturation of ODD-PURE (exploration, LAB 16/10/2026).
For one structure and orientation (iota = (2 3) by default): top generalized eigenvector u of (C Phi^+ C^t, K) on
range(K), its odd partner z = -Phi^+ C^t u, lambda_max, plus: corner adjacency (is C = {02,03,12,13} a 4-cycle?), the
components of the two line neighbourhoods, and the labels carrying most of u and of the odd profile.
usage: python near_saturation.py <structure json> [01|23]"""
import itertools
import json
import sys

import numpy as np

MATE = lambda i: i ^ 1


def kval(a, b):
    s = len(a & b)
    m = sum(1 for p in a for q in b if q == MATE(p))
    return (3 * s + m - 2) / 8.0


d = json.load(open(sys.argv[1]))
swap = (2, 3) if (len(sys.argv) < 3 or sys.argv[2] == "23") else (0, 1)
L = [frozenset(x) for x in d["labels"]]
E = set(frozenset((L[i], L[j])) for i, j in d["edges"])
S = [l for l in L if l & {0, 1, 2, 3}]
idx = {l: i for i, l in enumerate(S)}
G = np.zeros((44, 44))
for a, b in itertools.combinations(S, 2):
    if frozenset((a, b)) in E:
        G[idx[a], idx[b]] = G[idx[b], idx[a]] = 1
T = 3 * np.eye(44) - G - np.array([[kval(a, b) for b in S] for a in S])
r1, r2 = swap
U = [l for l in S if not (l & {r1, r2})]
others = [a for a in range(14) if a not in (r1, r2) and frozenset((r1, a)) in idx]
B = np.zeros((44, 44))
col = 0
for l in U:
    B[idx[l], col] = 1
    col += 1
for a in others:
    B[idx[frozenset((r1, a))], col] = B[idx[frozenset((r2, a))], col] = 1 / np.sqrt(2)
    col += 1
for a in others:
    B[idx[frozenset((r1, a))], col] = 1 / np.sqrt(2)
    B[idx[frozenset((r2, a))], col] = -1 / np.sqrt(2)
    col += 1
Tb = B.T @ T @ B
nU, nP = len(U), len(others)
K = Tb[:nU, :nU]
C = Tb[:nU, nU + nP:]
Phi = Tb[nU + nP:, nU + nP:]
ep, Vp = np.linalg.eigh(Phi)
Phip = (Vp[:, ep > 1e-9] / ep[ep > 1e-9]) @ Vp[:, ep > 1e-9].T
ek, Vk = np.linalg.eigh(K)
Kh = Vk[:, ek > 1e-9] / np.sqrt(ek[ek > 1e-9])
Mr = Kh.T @ C @ Phip @ C.T @ Kh
em, Vm = np.linalg.eigh(Mr)
u = Kh @ Vm[:, -1]
z = -Phip @ C.T @ u
print("orientation swap %s: lambda_max = %.6f (next %.6f)" % (swap, em[-1], em[-2]))
print("u (fixed labels), largest entries:")
for i in np.argsort(-np.abs(u))[:10]:
    print("   %s  %+.4f" % ("".join(str(t) for t in sorted(U[i])), u[i]))
print("odd profile delta_a = z_a*sqrt2 (pair {%d a}/{%d a}):" % (r1, r2))
for k, a in enumerate(others):
    print("   a=%2d  %+.4f" % (a, z[k] * np.sqrt(2)))
corners = [frozenset(p) for p in ((0, 2), (0, 3), (1, 2), (1, 3))]
ce = [(sorted(a), sorted(b)) for a, b in itertools.combinations(corners, 2) if frozenset((a, b)) in E]
print("corner edges:", ce)
