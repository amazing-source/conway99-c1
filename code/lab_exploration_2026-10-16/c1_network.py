"""c = 1, rigorous network form (exploration, LAB 16/10/2026 night).
For a pair (l, m) at v, l = {v,0,1}, m = {v,2,3}: G_l = cubic graph induced on the 36 neighbours of l (12 letters of
N(v) minus l, and L_0 u L_1); Y = the 20 labels {2,s},{3,s} (s outer).  Derived by hand (notebook): when G_l is connected
(c = 1), the 3-eigenvectors of the 59-ball are exactly  (two universal vectors) + {profiles eta in ker F}, with
     F = 3I - A_YY + J/12 - B^T L^+ B ,   L = 3I - A_G (Laplacian of G_l),  B = adjacency G_l x Y,
so nu(T_S) = 2 + dim ker F.  Conway needs dim ker F >= 12.  With M = 3I - A_YY + J/12 (positive definite) and
R = B^T L^+ B >= 0, F >= 0 means X = M^{-1/2} R M^{-1/2} has spectrum in [0, 1] and dim ker F = mult of 1 in X; for any k,
dim ker F <= tr X^k.  This script checks the identity nu = 2 + dim ker F on c = 1 sides and prints tr X, tr X^2, tr X^4.
usage: python c1_network.py <distinct cache.jsonl> <cle3_sides.jsonl> [max]"""
import itertools
import json
import sys

import numpy as np

MATE = lambda i: i ^ 1


def build(L, E):
    S = [l for l in L if l & {0, 1, 2, 3}]
    letters = [("L", s) for s in range(14) if s not in (0, 1)]
    Gv = letters + [l for l in S if l & {0, 1}]            # 12 + 24 = 36
    Y = [l for l in S if (l & {2, 3}) and not (l & {0, 1})]  # 20
    def adj(a, b):
        if isinstance(a, tuple) and isinstance(b, tuple):
            return MATE(a[1]) == b[1]
        if isinstance(a, tuple):
            return a[1] in b
        if isinstance(b, tuple):
            return b[1] in a
        return frozenset((a, b)) in E
    AG = np.array([[1.0 if i != j and adj(a, b) else 0.0 for j, b in enumerate(Gv)] for i, a in enumerate(Gv)])
    B = np.array([[1.0 if adj(a, y) else 0.0 for y in Y] for a in Gv])
    AY = np.array([[1.0 if i != j and adj(a, b) else 0.0 for j, b in enumerate(Y)] for i, a in enumerate(Y)])
    return S, Gv, Y, AG, B, AY


if __name__ == "__main__":
    cache, sides = sys.argv[1], sys.argv[2]
    mx = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
    want = {}
    for x in open(sides):
        s = json.loads(x)
        if s["c"] == 1:
            want.setdefault(s["src"], []).append(s)
    n = 0
    bad = 0
    rows = []
    for line in open(cache):
        d = json.loads(line)
        if d["src"] not in want or n >= mx:
            continue
        L = [frozenset(x) for x in d["labels"]]
        E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
        S, Gv, Y, AG, B, AY = build(L, E)
        deg = AG.sum(1)
        if not np.allclose(deg, 3):
            continue                      # orientation (0,1) not cubic: skip (should not happen)
        Lg = 3 * np.eye(36) - AG
        ncomp = int(np.sum(np.linalg.eigvalsh(Lg) < 1e-9))
        if ncomp != 1:
            continue                      # this side's c(l) for l = (0,1) is not 1 (the c=1 record is the other orientation)
        el, Vl = np.linalg.eigh(Lg)
        keep = el > 1e-9
        Lp = (Vl[:, keep] / el[keep]) @ Vl[:, keep].T     # exact pseudo-inverse (pinv with default rcond inverts the numerical zero)
        M = 3 * np.eye(20) - AY + np.ones((20, 20)) / 12
        R = B.T @ Lp @ B
        F = M - R
        ef = np.linalg.eigvalsh((F + F.T) / 2)
        kerF = int(np.sum(np.abs(ef) < 1e-7))
        # nu from T_S
        idx = {l: i for i, l in enumerate(S)}
        G = np.zeros((44, 44))
        for a, b in itertools.combinations(S, 2):
            if frozenset((a, b)) in E:
                G[idx[a], idx[b]] = G[idx[b], idx[a]] = 1
        def kval(a, b):
            s_ = len(a & b); m_ = sum(1 for p in a for q in b if q == MATE(p)); return (3 * s_ + m_ - 2) / 8.0
        T = 3 * np.eye(44) - G - np.array([[kval(a, b) for b in S] for a in S])
        nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
        bad += 0 if nu == 2 + kerF else 1
        em, Vm = np.linalg.eigh(M)
        Mi = Vm @ np.diag(em ** -0.5) @ Vm.T
        X = Mi @ R @ Mi
        ex = np.clip(np.linalg.eigvalsh((X + X.T) / 2), 0, 1)
        rows.append((kerF, nu, float(ex.sum()), float((ex ** 2).sum()), float((ex ** 4).sum()), float(min(ef)),
                     sorted(ex)[::-1][:12]))
        n += 1
    print("c = 1 sides (orientation l = (0,1)) checked: %d ; identity nu = 2 + dim ker F fails on %d" % (n, bad))
    import collections
    print("dim ker F distribution:", dict(sorted(collections.Counter(r[0] for r in rows).items())))
    print("min eigenvalue of F (should be >= 0):", min(r[5] for r in rows))
    for k, name in ((2, "tr X"), (3, "tr X^2"), (4, "tr X^4")):
        v = [r[k] for r in rows]
        print("%s: min %.3f  max %.3f" % (name, min(v), max(v)))
    r = max(rows, key=lambda r: r[2])
    print("largest tr X side: dim ker F %d, top eigenvalues of X:" % r[0], [round(x, 4) for x in r[6]])
