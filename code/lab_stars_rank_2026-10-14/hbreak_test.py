"""Do random local re-solves around an h-invariant PSD four-star structure break h, and are the PSD ones h-invariant?
(LAB 15/10/2026, SQ30 / h-invariance question).  Free the pairs touching k random labels, re-solve (random polarity),
record h-asymmetry, PSD (numerical, on the star complement for T and U), numerical nullity.
usage: python hbreak_test.py <start json> <trials> <k> <seed>"""
import itertools
import json
import random
import sys
from collections import Counter

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS

start, trials, kfree, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed)
S, idx, e, F = build([0, 1, 2, 3], rng)
n = len(S)
sol = Solver(options={"polar": "rnd", "seed": str(seed)})
for c in F.clauses:
    sol.add_clause(c)
d = json.load(open(start))
assert [sorted(l) for l in S] == d["labels"]
E0 = {tuple(x) for x in d["edges"]}
K = np.array([[kval(a, b) for b in S] for a in S])
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {l: i for i, l in enumerate(LABELS)}
PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
stats = Counter()
for t in range(trials):
    R = set(rng.sample(range(n), kfree))
    assum = [e[(i, j)] if (i, j) in E0 else -e[(i, j)] for i, j in itertools.combinations(range(n), 2)
             if i not in R and j not in R]
    ok, model = sol.solve(assum)
    if not ok:
        stats["unsat"] += 1
        continue
    G = np.zeros((n, n))
    for (i, j), v in e.items():
        if i < j and model[v]:
            G[i, j] = G[j, i] = 1
    changed = int(sum(1 for i, j in itertools.combinations(range(n), 2) if (G[i, j] == 1) != ((i, j) in E0)))
    hasym = int(np.abs(G[np.ix_(hp, hp)] - G).sum()) // 2
    T = 3 * np.eye(n) - G - K
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
    psd = min(lt, lu) > -1e-9
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    stats[("changed" if changed else "same", "h-inv" if hasym == 0 else "h-broken", "PSD" if psd else "notPSD")] += 1
    if psd and hasym:
        stats["PSD h-broken nullity %d" % nul] += 1
    if psd and not hasym and changed:
        stats["PSD h-inv changed nullity %d" % nul] += 1
for k, v in sorted(stats.items(), key=lambda x: str(x[0])):
    print(k, v)
