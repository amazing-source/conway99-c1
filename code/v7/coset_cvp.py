"""Exhaustive core-supported transfer search = CVP in the class of q.

For c in Z^core and j in Z, z = q + sum_v c_v q_v + j*1 has
  ||z||^2 = 37 + c^T G c + 99 j^2 + 2 sum_v c_v (6 - 7 q(v)) + 66 j + 22 j s,   G = 21I + 2J - 7A_core, s = sum c,
  level(z) = 3 + s + 9 j.
Only the core adjacency and q on the core enter.  We enumerate ALL (c, j) with ||z||^2 <= BOUND (Fincke-Pohst on
the exact integer Gram of {q_v (v in core), 1}), and report the norms found per level.
A level-0 vector of norm 26 is an integer -4 eigenvector of norm 26: it kills the core (residual hypothesis).
"""
import json, sys, itertools
import numpy as np
from fractions import Fraction

P13 = list(range(14, 27))


def gram_and_lin(A, qcore):
    n = A.shape[0]
    G = np.zeros((n + 1, n + 1), dtype=np.int64)
    G[:n, :n] = 21 * np.eye(n, dtype=np.int64) + 2 - 7 * A
    G[:n, n] = G[n, :n] = 11
    G[n, n] = 99
    lin = np.zeros(n + 1, dtype=np.int64)  # <q, basis vector>
    lin[:n] = 6 - 7 * np.array(qcore)
    lin[n] = 33
    return G, lin


def enumerate_short(G, lin, const, bound):
    """all integer x with x^T G x + 2 lin.x + const <= bound  (G positive definite)."""
    n = G.shape[0]
    Gf = G.astype(float)
    center = -np.linalg.solve(Gf, lin.astype(float))
    cmin = const - lin.astype(float) @ np.linalg.solve(Gf, lin.astype(float))
    R = np.linalg.cholesky(Gf).T  # G = R^T R, R upper triangular
    sols = []
    x = np.zeros(n, dtype=np.int64)
    budget = bound - cmin + 1e-6

    def rec(k, rem):
        # coordinates k..n-1 already fixed in x? we go from last to first
        if k < 0:
            val = int(x @ G @ x + 2 * lin @ x + const)
            if val <= bound:
                sols.append((val, x.copy()))
            return
        # y = R (x - center); y_k = R_kk (x_k - c_k) + sum_{l>k} R_kl (x_l - c_l)
        s = sum(R[k, l] * (x[l] - center[l]) for l in range(k + 1, n))
        ck = center[k] - s / R[k, k]
        r = np.sqrt(max(rem, 0)) / R[k, k]
        lo = int(np.ceil(ck - r - 1e-9)); hi = int(np.floor(ck + r + 1e-9))
        for v in range(lo, hi + 1):
            x[k] = v
            y = R[k, k] * (v - ck)
            rec(k - 1, rem - y * y)
        x[k] = 0

    rec(n - 1, budget)
    return sols


def run(core, holes, bound=40):
    A = np.array(core["adj"], dtype=np.int64)
    qcore = [-1, -1, 1, 1, 1, 1, 1, 1] + [0] * 6 + [0 if v in holes else 1 for v in P13]
    G, lin = gram_and_lin(A, qcore)
    # relation sum kappa_v q_v = -5*1 (kernel of K_core); drop q_26 (kappa=1) to get a basis
    keep = list(range(26)) + [27]
    G = G[np.ix_(keep, keep)]; lin = lin[keep]
    sols = enumerate_short(G, lin, 37, bound)
    res = {}
    for val, x in sols:
        lev = 3 + int(x[:-1].sum()) + 9 * int(x[-1])
        res.setdefault((lev, val), []).append(x)
    return res


if __name__ == "__main__":
    cores = json.load(open("cores27.json"))
    k = int(sys.argv[1])
    holes = [int(v) for v in sys.argv[2].split(",")]
    bound = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    res = run(cores[k], holes, bound)
    for key in sorted(res):
        print(key, len(res[key]))
