"""Is U >= 0 automatic on a two-mate-star base X_l = L_0 u L_1 (24 labels)?  (14/10/2026)
T_X >= 0 always (Codex's sum of squares). U_X = 7 Pi_X - T_X: if U_X can be indefinite, then 'U_X >= 0' is a genuine
condition that every line of a Conway graph must satisfy. Samples random admissible bases (stars 0, 1) and reports
lambda_min(U_X), lambda_max(T_X), together with t(l) (transversals) and c(l).
usage: python base_u.py <samples> <seed>"""
import random
import sys
from collections import defaultdict
import numpy as np
from pycryptosat import Solver
from stars_rank import build, kval, LABELS
from z5_enum import exact_rank

samples, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
S, idx, e, F = build([0, 1], rng)
n = len(S)
K = np.array([[kval(a, b) for b in S] for a in S])
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {l: i for i, l in enumerate(LABELS)}
ix = [pos[l] for l in S]
PiS = Pi[np.ix_(ix, ix)]
tpairs = [(idx[frozenset((0, x))], idx[frozenset((1, x))]) for x in range(2, 14)]
stats = defaultdict(list)
neg = 0
for t in range(samples):
    sol = Solver(options={"polar": "rnd", "seed": str(rng.randrange(1, 10 ** 9))})
    for c in F.clauses:
        sol.add_clause(c)
    ok, model = sol.solve()
    G = np.zeros((n, n))
    for (i, j), v in e.items():
        if i < j and model[v]:
            G[i, j] = G[j, i] = 1
    T = 3 * np.eye(n) - G - K
    U = 7 * PiS - T
    lu = float(np.linalg.eigvalsh(U)[0])
    lt = float(np.linalg.eigvalsh(T)[-1])
    tl = sum(1 for a, b in tpairs if G[a, b])
    stats[tl].append(lu)
    neg += lu < -1e-9
print("%d bases: U_X indefinite in %d" % (samples, neg))
for k in sorted(stats):
    v = stats[k]
    print("t(l) = %2d: %4d bases, lambda_min(U_X) min %.4f max %.4f" % (k, len(v), min(v), max(v)))
