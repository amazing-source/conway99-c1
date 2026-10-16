"""Corank of the 20x20 matrix Q of the resonance elimination on a four-star block (exploration, LAB 16/10/2026).
U = l u N(l) u Y with l = {v,0,1}, N(l) = letters 2..13 + L_0 + L_1 (cubic), Y = the 20 labels of L_2 u L_3 avoiding 0, 1.
Q = 3I - A_YY - A_YN (3I - A_NN)^+ A_NY  ((.)^+ = pseudo-inverse, i.e. inverse on the complement of the component
indicators of the cubic graph).  Predicted (proved elimination): nu <= c(l) + 5 + corank(Q).  Also prints nu = nullity of
T_S and c(l).
usage: python q_corank.py <block json> [...]"""
import itertools
import json
import sys

import numpy as np

MATE = lambda i: i ^ 1
for path in sys.argv[1:]:
    d = json.load(open(path))
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((L[i], L[j])) for i, j in d["edges"])
    S = [l for l in L if l & {0, 1, 2, 3}]
    verts = ["v"] + [("L", s) for s in range(14)] + S
    pos = {x: i for i, x in enumerate(verts)}
    n = len(verts)
    A = np.zeros((n, n))
    for s in range(14):
        A[pos["v"], pos[("L", s)]] = A[pos[("L", s)], pos["v"]] = 1
        A[pos[("L", s)], pos[("L", MATE(s))]] = 1
    for l in S:
        for s in l:
            A[pos[l], pos[("L", s)]] = A[pos[("L", s)], pos[l]] = 1
    for a, b in itertools.combinations(S, 2):
        if frozenset((a, b)) in E:
            A[pos[a], pos[b]] = A[pos[b], pos[a]] = 1
    lset = ["v", ("L", 0), ("L", 1)]
    Nset = [("L", s) for s in range(2, 14)] + [l for l in S if l & {0, 1}]
    Yset = [l for l in S if not (l & {0, 1})]
    il = [pos[x] for x in lset]
    iN = [pos[x] for x in Nset]
    iY = [pos[x] for x in Yset]
    ANN = A[np.ix_(iN, iN)]
    assert np.allclose(ANN.sum(1), 3), "N(l) not cubic"
    ev, V = np.linalg.eigh(3 * np.eye(len(iN)) - ANN)
    inv = np.zeros_like(ANN)
    for k in range(len(ev)):
        if ev[k] > 1e-9:
            inv += np.outer(V[:, k], V[:, k]) / ev[k]
    c_l = int(np.sum(ev < 1e-9))
    AYN = A[np.ix_(iY, iN)]
    Q = 3 * np.eye(len(iY)) - A[np.ix_(iY, iY)] - AYN @ inv @ AYN.T
    eq = np.linalg.eigvalsh(Q)
    cor = int(np.sum(np.abs(eq) < 1e-8))
    # nullity of T_S via the Schur complement: 3I - A_UU on 1-perp; use the 3-eigenspace of A_UU orthogonal to 1
    ea, Va = np.linalg.eigh(A)
    W = Va[:, np.abs(ea - 3) < 1e-8]
    one = np.ones(n) / np.sqrt(n)
    if W.shape[1]:
        proj = W.T @ one
        nu = W.shape[1] - (1 if np.linalg.norm(proj) > 1e-8 else 0)
    else:
        nu = 0
    print("%s: c(l) = %d, corank(Q) = %d, nu (mult of 3 in A_UU, orthogonal to 1) = %d, bound c + 5 + corank = %d; "
          "lambda_min(Q) = %.4f" % (path.replace("\\", "/").split("/")[-1], c_l, cor, nu, c_l + 5 + cor, eq[0]))
