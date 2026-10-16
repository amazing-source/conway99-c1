"""Split of ker Q into antisymmetric and symmetric parts across the two rows of Y (exploration, LAB 16/10/2026).
For each PSD four-star structure and each side: ker Q (numerical, tolerance 1e-8), rank of the antisymmetric parts
x_{r s} - x_{r' s} (ODDCONST predicts 1: only the trivial vector chi_r - chi_r' of the other line) and rank of the
symmetric parts x_{r s} + x_{r' s} (SYM6 predicts <= 6 for non-grid sides).  Aggregates by grid / non-grid.
usage: python q_split_scan.py <root dir>"""
import collections
import itertools
import json
import os
import sys

import numpy as np

MATE = lambda i: i ^ 1


def kval(a, b):
    s = len(a & b)
    m = sum(1 for p in a for q in b if q == MATE(p))
    return (3 * s + m - 2) / 8.0


def rank(M, tol=1e-7):
    if M.size == 0:
        return 0
    s = np.linalg.svd(M, compute_uv=False)
    return int(np.sum(s > tol * max(1.0, s[0])))


def sides(L, E):
    S = [l for l in L if l & {0, 1, 2, 3}]
    if len(S) != 44:
        return None
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
    iS = [pos[l] for l in S]
    T = 3 * np.eye(44) - A[np.ix_(iS, iS)] - np.array([[kval(a, b) for b in S] for a in S])
    if np.linalg.eigvalsh(T)[0] < -1e-8:
        return None
    res = []
    for (p, q), (r1, r2) in (((0, 1), (2, 3)), ((2, 3), (0, 1))):
        Nset = [("L", s) for s in range(14) if s not in (p, q)] + [l for l in S if l & {p, q}]
        Yset = [frozenset((r, s)) for r in (r1, r2) for s in range(14) if s not in (0, 1, 2, 3)]
        iN = [pos[x] for x in Nset]
        iY = [pos[x] for x in Yset]
        ANN = A[np.ix_(iN, iN)]
        ev, V = np.linalg.eigh(3 * np.eye(len(iN)) - ANN)
        c = int(np.sum(ev < 1e-9))
        inv = (V[:, ev > 1e-9] / ev[ev > 1e-9]) @ V[:, ev > 1e-9].T
        AYN = A[np.ix_(iY, iN)]
        Q = 3 * np.eye(20) - A[np.ix_(iY, iY)] - AYN @ inv @ AYN.T
        eq, VQ = np.linalg.eigh(Q)
        K = VQ[:, np.abs(eq) < 1e-8]               # 20 x corank
        anti = K[:10, :] - K[10:, :]
        symm = K[:10, :] + K[10:, :]
        # grid on (l, m): the component of the letter r1 has size 6
        null = V[:, ev < 1e-9]
        i0 = Nset.index(("L", r1))
        same = [j for j in range(len(Nset)) if np.allclose(null[j], null[i0], atol=1e-8)]
        res.append({"c": c, "cor": K.shape[1], "anti": rank(anti), "sym": rank(symm), "grid": len(same) == 6})
    g = res[0]["grid"] or res[1]["grid"]
    for r in res:
        r["grid"] = g
    return res


root = sys.argv[1]
seen = set()
agg = collections.Counter()
viol = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(".json"):
            continue
        try:
            d = json.load(open(os.path.join(dp, f)))
            L = [frozenset(x) for x in d["labels"]]
            E = set(frozenset((L[i], L[j])) for i, j in d["edges"])
        except Exception:
            continue
        key = frozenset(E)
        if key in seen:
            continue
        seen.add(key)
        rs = sides(L, E)
        if rs is None:
            continue
        for r in rs:
            agg[("G" if r["grid"] else "NG", r["c"], r["cor"], r["anti"], r["sym"])] += 1
            if not r["grid"] and (r["anti"] > 1 or r["sym"] > 6) and len(viol) < 10:
                viol.append((os.path.join(dp, f), r))
print("(grid?, c, corank Q, rank antisym, rank sym): count")
for k, v in sorted(agg.items()):
    print("  ", k, v)
print("non-grid sides with antisym rank > 1 or sym rank > 6:", sum(v for k, v in agg.items() if k[0] == "NG" and
      (k[3] > 1 or k[4] > 6)), viol[:5])
