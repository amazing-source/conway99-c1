"""Search for an exact failure of ODD9 at c(l) = 1, in the E3-free regime (exploration, LAB 17/10/2026).
Setting (archive, AUDIT_EXCLUSIONS 15/10 03:30): four-star block, l = {v,0,1}, m = {v,2,3}; X_l = the 24 labels of l
(rank T_{X_l} = 23 - c(l) = 22 at c = 1), Q = the 20 labels 2y, 3y (y = 4..13); odd vectors f_y = 1_{2y} - 1_{3y},
even g_y = 1_{2y} + 1_{3y}.  With S_Q the Schur complement of T_S on Q (rank additivity holds without positivity:
range T_{lQ} lies in range T_l), nullity(T_S) = 22 - o - e where o = rank(F^t S_Q F) (odd gain, <= 9 since the sum of
the f_y comes from z_2 - z_3) and e = the even gain.  ODD9 (o = 9) gives nullity <= 13 at c = 1; Conway needs 14.
Walk: CNF of stars_rank.build (local axioms) + no rectangle with exactly 3 internal edges at both roots + c(l) = 1
(every proper cut of the six rectangles of l is crossed).  Moves free NFREE labels and re-solve (pycryptosat).
Score = odd gap = second smallest eigenvalue of S_f = F^t S_Q F (smallest is 0, eigenvector 1); Metropolis on -gap.
When the gap is < 1e-6 the exact odd gain is computed (sympy ranks).  Positivity and nullity are recorded.
usage: python c1_odd9_walk.py <seed> <seconds> [NFREE] [T0]"""
import itertools
import json
import math
import os
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
from stars_rank import build, kval  # noqa: E402

seed, secs = int(sys.argv[1]), float(sys.argv[2])
NFREE = int(sys.argv[3]) if len(sys.argv) > 3 else 4
temp = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05
rng = random.Random(seed)
S, idx, e, F = build([0, 1, 2, 3], rng)
n = len(S)
sol = Solver(options={"polar": "rnd", "seed": str(seed)})
for c in F.clauses:
    sol.add_clause(c)
# E3 at both roots
for (a0, a1) in ((0, 1), (2, 3)):
    for x in range(0, 14, 2):
        if {x, x + 1} & {a0, a1}:
            continue
        q = [idx[frozenset((r, t))] for r in (a0, a1) for t in (x, x + 1)]
        prs = [e[(q[i], q[j])] for i, j in itertools.combinations(range(4), 2)]
        for sub in itertools.combinations(range(6), 3):
            sol.add_clause([-prs[k] if k in sub else prs[k] for k in range(6)])
# c(l) = 1
rect = [[idx[frozenset((r, t))] for r in (0, 1) for t in (2 * j, 2 * j + 1)] for j in range(1, 7)]
for size in range(1, 6):
    for sub in itertools.combinations(range(6), size):
        if 0 not in sub:
            continue
        ins = [p for k in sub for p in rect[k]]
        out = [p for k in range(6) if k not in sub for p in rect[k]]
        sol.add_clause([e[(p, r)] for p in ins for r in out])
K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
XL = [i for i, l in enumerate(S) if l & {0, 1}]
QQ = [i for i, l in enumerate(S) if not (l & {0, 1})]
assert len(XL) == 24 and len(QQ) == 20
Fm = np.zeros((20, 10))
Gm = np.zeros((20, 10))
for k, y in enumerate(range(4, 14)):
    Fm[QQ.index(idx[frozenset((2, y))]), k] = 1
    Fm[QQ.index(idx[frozenset((3, y))]), k] = -1
    Gm[QQ.index(idx[frozenset((2, y))]), k] = 1
    Gm[QQ.index(idx[frozenset((3, y))]), k] = 1


def graph_of(model):
    G = np.zeros((n, n), dtype=np.int64)
    for (i, j), v in e.items():
        if i < j and model[v]:
            G[i, j] = G[j, i] = 1
    return G


B9 = np.linalg.qr(np.hstack([np.ones((10, 1)), np.eye(10)[:, :9]]))[0][:, 1:]      # orthonormal basis of 1^perp


def analyse(G):
    """returns T, S_Q, S_f and the sorted |eigenvalues| of S_f on 1^perp (rank 9 <=> all nonzero)."""
    T = (24 * np.eye(n) - 8 * G - K8) / 8.0
    Tl = T[np.ix_(XL, XL)]
    TlQ = T[np.ix_(XL, QQ)]
    SQ = T[np.ix_(QQ, QQ)] - TlQ.T @ np.linalg.pinv(Tl, rcond=1e-9) @ TlQ
    Sf = Fm.T @ SQ @ Fm
    ev = np.sort(np.abs(np.linalg.eigvalsh(B9.T @ Sf @ B9)))
    return T, SQ, Sf, np.concatenate([[0.0], ev])


def exact_gains(G):
    import sympy as sp
    T8 = sp.Matrix((24 * np.eye(n, dtype=np.int64) - 8 * G - K8).tolist())
    rl = T8.extract(XL, XL).rank()
    # odd gain: rank of the Gram of [X_l unit columns, odd columns] minus rank T_l
    P = sp.zeros(n, 34)
    for a, i in enumerate(XL):
        P[i, a] = 1
    for k in range(10):
        for b, q in enumerate(QQ):
            if Fm[b, k]:
                P[q, 24 + k] = int(Fm[b, k])
    r_odd = (P.T * T8 * P).rank()
    return rl, r_odd - rl, n - T8.rank()


ok, model = sol.solve()
assert ok
G = graph_of(model)
T, SQ, Sf, ev = analyse(G)
cur = ev[1]
best = cur
t0 = time.time()
moves = 0
log = []
while time.time() - t0 < secs:
    moves += 1
    freed = set(rng.sample(range(n), NFREE))
    assum = [(e[(i, j)] if model[e[(i, j)]] else -e[(i, j)]) for i, j in itertools.combinations(range(n), 2)
             if i not in freed and j not in freed]
    ok2, m2 = sol.solve(assum)
    if not ok2:
        continue
    G2 = graph_of(m2)
    T2, SQ2, Sf2, ev2 = analyse(G2)
    g2 = ev2[1]
    if g2 <= cur or rng.random() < math.exp(-(g2 - cur) / temp):
        model, cur, G = m2, g2, G2
    if cur < best:
        best = cur
        lam = float(np.linalg.eigvalsh(T2)[0]) if model is m2 else float(np.linalg.eigvalsh((24 * np.eye(n) - 8 * G - K8) / 8.0)[0])
        log.append((moves, round(best, 6)))
        fn = os.path.join(HERE, "unbiased_walks", "odd9_best_seed%d.json" % seed)
        json.dump({"labels": [sorted(l) for l in S], "gap": best,
                   "edges": [[i, j] for i, j in itertools.combinations(range(n), 2) if G[i, j]]}, open(fn, "w"))
        if best < 1e-6:
            rl, o, nu = exact_gains(G)
            print("move %d: gap %.2e -> EXACT: rank T_l %d, odd gain %d, nullity %d" % (moves, best, rl, o, nu), flush=True)
            if o <= 8:
                print("  EXACT ODD9 FAILURE at c(l) = 1, E3-free; saved", fn, flush=True)
                break
    temp = max(0.002, temp * 0.9995)
    if moves % 400 == 0:
        print("move %d: gap %.5f best %.6f (%.0f s)" % (moves, cur, best, time.time() - t0), flush=True)
print("end: %d moves, best odd gap %.6g ; improvements %s" % (moves, best, log[-8:]), flush=True)
