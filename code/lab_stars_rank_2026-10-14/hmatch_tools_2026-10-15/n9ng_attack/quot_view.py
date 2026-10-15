"""V4-quotient of a four-star structure: N_l, N_m (10x10), N_x (10x10), e_C, e'_C, edges in C; A++ and the Schur
complement R++ (m over l), its rank and nonzero spectrum.  usage: python quot_view.py <json>"""
import json, sys
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
f = sys.argv[1]
d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
G = np.zeros((n, n))
for a, b in d["edges"]: G[a, b] = G[b, a] = 1
K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
OUT = list(range(4, 14))
o = [[idx[frozenset((0, y))], idx[frozenset((1, y))]] for y in OUT]
p = [[idx[frozenset((2, y))], idx[frozenset((3, y))]] for y in OUT]
C = [idx[frozenset(q)] for q in ((0, 2), (0, 3), (1, 2), (1, 3))]
cnt = lambda A, B: int(sum(G[i, j] for i in A for j in B))
Nl = np.array([[cnt(o[i], o[j]) for j in range(10)] for i in range(10)])
Nm = np.array([[cnt(p[i], p[j]) for j in range(10)] for i in range(10)])
Nx = np.array([[cnt(o[i], p[j]) for j in range(10)] for i in range(10)])
eC = [cnt(o[i], C) for i in range(10)]; eCm = [cnt(p[i], C) for i in range(10)]; eCC = cnt(C, C) // 2
print(f); print("outer letters", OUT)
print("N_l:\n", Nl); print("N_m:\n", Nm); print("N_x:\n", Nx)
print("e_C(l)", eC, " e_C(m)", eCm, " edges in C", eCC)
W = []
for grp in o + p:
    v = np.zeros(n); v[grp] = 1; W.append(v)
v = np.zeros(n); v[C] = 1; W.append(v)
W = np.array(W).T
A = W.T @ T @ W
L = list(range(10)) + [20]; M = list(range(10, 20))
ALL = A[np.ix_(L, L)]; ALM = A[np.ix_(L, M)]; AMM = A[np.ix_(M, M)]
R = AMM - ALM.T @ np.linalg.pinv(ALL, rcond=1e-10) @ ALM; R = (R + R.T) / 2
w = np.linalg.eigvalsh(R)
print("nu(A++) =", int(np.sum(np.abs(np.linalg.eigvalsh(A)) < 1e-7)), " rank R++ =", int(np.sum(np.abs(w) > 1e-7)), " nonzero spectrum", np.round(w[np.abs(w) > 1e-7], 4))
