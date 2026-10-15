"""ODD9 on random admissible four-star structures, PSD or not (LAB 15/10/2026).
Random SAT solutions of the admissibility model (C1, C1', C2) with random polarities; for each: exact odd and even
rank gains beyond X_l and X_m (Gram ranks of 8T), lambda_min of T and U on the complement of the stars.
usage: python odd9_random.py <count> <seed>"""
import random
import sys

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS
from odd9_check import gain

cnt, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
S, idx, e, F = build([0, 1, 2, 3], rng)
n = len(S)
K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {l: i for i, l in enumerate(LABELS)}
ix = [pos[l] for l in S]
PiS = Pi[np.ix_(ix, ix)]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
hist = {}
for t in range(cnt):
    sol = Solver(options={"polar": "rnd", "seed": str(seed * 1000 + t)})
    for c in F.clauses:
        sol.add_clause(c)
    ok, model = sol.solve()
    if not ok:
        print("UNSAT")
        break
    G = np.zeros((n, n), dtype=np.int64)
    for (i, j), v in e.items():
        if i < j and model[v]:
            G[i, j] = G[j, i] = 1
    M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    T = M8 / 8.0
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
    res = []
    for (a, a2, b, b2) in ((0, 1, 2, 3), (2, 3, 0, 1)):
        Xl = [i for i in range(n) if S[i] & {a, a2}]
        odd = []
        for y in range(4, 14):
            v = np.zeros(n, dtype=np.int64)
            v[idx[frozenset((b, y))]] = 1
            v[idx[frozenset((b2, y))]] = -1
            odd.append(v)
        res.append(gain(M8, Xl, odd))
    key = (res[0], res[1], "PSD" if min(lt, lu) > -1e-9 else "notPSD")
    hist[key] = hist.get(key, 0) + 1
    if res[0] != 9 or res[1] != 9:
        print("structure %d: odd gains %s, lambda_T %.3f, lambda_U %.3f" % (t, res, lt, lu), flush=True)
print("histogram (odd gain beyond X_l, beyond X_m, PSD?):", hist)
