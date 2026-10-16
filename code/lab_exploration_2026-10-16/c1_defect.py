"""c = 1: bound on the number delta of exact odd saturations by the defect energy (exploration, LAB 17/10/2026).
Odd profiles g (sum 0): D(g) = g^T (6I - A_sig) g - (Cg)^T L^+ (Cg), with C_us = [u ~ {2,s}] - [u ~ {3,s}] (u in L_0 u L_1).
Saturated g satisfy (Cg)^T L^+ (Cg) = g^T(6I - A_sig)g >= 2|g|^2, so delta <= #{eigenvalues of C^T L^+ C >= 2}
<= tr(L^+ C C^T)/2 = (1/2) sum_s E_s, E_s = c_s^T L^+ c_s (energy of the defect pattern of the outer letter s).
Also the sharper count #{eig(C^T L^+ C) >= 2} and, sharper still, #{generalized eigenvalues of (C^T L^+ C, 6I - A_sig) >= 1}.
usage: python c1_defect.py <distinct cache.jsonl> <cle3_sides.jsonl>"""
import json, sys, collections
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from c1_network import build
from c1_signed import signed_graph

want = {json.loads(x)["src"] for x in open(sys.argv[2]) if json.loads(x)["c"] == 1}
rows = []
for line in open(sys.argv[1]):
    d = json.loads(line)
    if d["src"] not in want:
        continue
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
    S, Gv, Y, AG, B, AY = build(L, E)
    Lg = 3 * np.eye(36) - AG
    el, Vl = np.linalg.eigh(Lg)
    if np.sum(el < 1e-9) != 1:
        continue
    Lp = (Vl[:, el > 1e-9] / el[el > 1e-9]) @ Vl[:, el > 1e-9].T
    SG, Bo, Asig, outer = signed_graph(Gv, Y, AG, B, AY)
    C = Bo.copy()
    hubs = [Gv.index(("L", 2)), Gv.index(("L", 3))]
    C[hubs, :] = 0                       # hub rows vanish on sum-zero g
    Es = np.array([C[:, j] @ Lp @ C[:, j] for j in range(10)])
    M = C.T @ Lp @ C
    P = np.eye(10) - np.ones((10, 10)) / 10
    Mp = P @ M @ P
    em = np.linalg.eigvalsh(Mp)
    N6 = P @ (6 * np.eye(10) - Asig) @ P
    # generalized eigenvalues on 1^perp
    U = np.linalg.svd(P)[0][:, :9]
    gen = np.sort(np.linalg.eigvals(np.linalg.solve(U.T @ N6 @ U, U.T @ Mp @ U)).real)[::-1]
    nnz = int(np.sum(np.abs(C) > 0))
    rows.append((Es.sum(), int(np.sum(em >= 2 - 1e-9)), gen[0], int(np.linalg.matrix_rank(C)), nnz, d["src"]))
print("c = 1 sides:", len(rows))
for k, name in ((0, "sum_s E_s (delta <= half of it)"), (2, "top generalized eigenvalue (delta = #{=1})")):
    v = np.array([r[k] for r in rows])
    print("%-45s: min %.3f  median %.3f  max %.3f" % (name, v.min(), np.median(v), v.max()))
print("#{eig(C^T L^+ C) >= 2} distribution:", dict(sorted(collections.Counter(r[1] for r in rows).items())))
print("rank C distribution:", dict(sorted(collections.Counter(r[3] for r in rows).items())))
print("nonzeros of C distribution (defect incidences):", dict(sorted(collections.Counter(r[4] for r in rows).items())))
