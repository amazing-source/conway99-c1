"""Transversals versus positivity on random admissible four-star structures, NO symmetry (14/10/2026).
For each sample: t(l), t(m) (fixed points of sigma_l, sigma_m), c(l), c(m), lambda_min of T and U off the stars.
usage: python tsample.py <samples> <seed>"""
import random
import sys
from collections import defaultdict
import numpy as np
from pycryptosat import Solver
from stars_rank import build, kval, LABELS

samples, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
stars = [0, 1, 2, 3]
S, idx, e, F = build(stars, rng)
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
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
tl_pairs = [(idx[frozenset((0, x))], idx[frozenset((1, x))]) for x in range(2, 14)]
tm_pairs = [(idx[frozenset((2, x))], idx[frozenset((3, x))]) for x in [0, 1] + list(range(4, 14))]


def pm(M):
    ev, V = np.linalg.eigh(Pp @ M @ Pp)
    keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
    return float(ev[keep].min())


stats = defaultdict(list)
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
    tl = sum(1 for a, b in tl_pairs if G[a, b])
    tm = sum(1 for a, b in tm_pairs if G[a, b])
    s = min(pm(T), pm(7 * PiS - T))
    stats[tl + tm].append(s)
for k in sorted(stats):
    v = stats[k]
    print("t(l) + t(m) = %2d: %4d samples, best min(lambda_T, lambda_U) %.4f, mean %.4f" % (k, len(v), max(v), np.mean(v)))
