"""Where does positivity fail in the best constrained c = 1 blocks? (exploration, LAB 17/10/2026)
For a saved four-star structure: lambda_min of T_S and U_S = 7 Pi_S - T_S on the complement of the four stars, the
weight of the extreme eigenvector on L_0 u L_1 / labels of m only / the four cross labels, its share in the span of the
12 root rectangles, and c(l), gap(G_l).
usage: python c1_negdir.py <structure.json> [...]"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
from stars_rank import kval, LABELS  # noqa: E402
from gg_test import orient, line_graph, components  # noqa: E402

for fn in sys.argv[1:]:
    d = json.load(open(fn))
    S = [frozenset(x) for x in d["labels"]]
    n = len(S)
    G = np.zeros((n, n))
    for i, j in d["edges"]:
        G[i, j] = G[j, i] = 1
    T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
    D = np.zeros((14, 84))
    for j, l in enumerate(LABELS):
        for t in l:
            D[t, j] = 1
    Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
    posL = {l: i for i, l in enumerate(LABELS)}
    ix = [posL[l] for l in S]
    U = 7 * Pi[np.ix_(ix, ix)] - T
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in range(4)]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T
    rects = [[frozenset((r, x)) for r in (a0, a1) for x in (2 * j, 2 * j + 1)]
             for (a0, a1) in ((0, 1), (2, 3)) for j in range(7) if {2 * j, 2 * j + 1} != {a0, a1}]
    P = np.array([[1.0 if S[i] in q else 0.0 for q in rects] for i in range(n)])
    Qr, _ = np.linalg.qr(P)
    for name, M in (("T", T), ("U", U)):
        ev, V = np.linalg.eigh(Pp @ M @ Pp)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        k0 = keep[int(np.argmin(ev[keep]))]
        v = V[:, k0]
        w = v ** 2
        parts = {"L01": sum(w[i] for i in range(n) if S[i] & {0, 1} and not S[i] & {2, 3}),
                 "m only": sum(w[i] for i in range(n) if S[i] & {2, 3} and not S[i] & {0, 1}),
                 "cross": sum(w[i] for i in range(n) if S[i] & {0, 1} and S[i] & {2, 3})}
        print("%s %s: lambda_min %.4f ; weight %s ; share in span of root rectangles %.3f" % (
            os.path.basename(fn), name, ev[k0], {k: round(float(x), 3) for k, x in parts.items()},
            float(np.linalg.norm(Qr.T @ v) ** 2)))
    L, EE = orient(S, [[sorted(S[i]), sorted(S[j])] for i, j in d["edges"]], 0)
    V2, pos, A = line_graph(L, EE)
    print("   c(l) = %d, gap(G_l) %.3f" % (components(A), np.sort(np.linalg.eigvalsh(3 * np.eye(36) - np.array(A, dtype=float)))[1]))
