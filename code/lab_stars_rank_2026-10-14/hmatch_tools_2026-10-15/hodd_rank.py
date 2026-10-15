"""Rank of the h-odd compression C = T|E_- of four-star structures (LAB 15/10/2026).  On all 331 rank-30 objects
nullity(C) = 2 (only the star differences).  Here: random admissible structures from cryptominisat (no positivity)
and saved files.  usage: python hodd_rank.py <samples> <seed> [json glob]"""
import glob
import json
import random
import sys
from collections import Counter

import numpy as np
from pycryptosat import Solver

sys.path.insert(0, '.')
from stars_rank import build, kval

samples, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
S, idx, e, F = build([0, 1, 2, 3], rng)
n = len(S)
K = np.array([[kval(a, b) for b in S] for a in S])
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
H = np.zeros((n, n))
for i in range(n):
    H[hp[i], i] = 1
Qm = np.linalg.svd((np.eye(n) - H) / 2)[0][:, :22]
Qp = np.linalg.svd((np.eye(n) + H) / 2)[0][:, :22]


def stats(G):
    T = 3 * np.eye(n) - G - K
    nC = int(np.sum(np.abs(np.linalg.eigvalsh(Qm.T @ T @ Qm)) < 1e-8))
    nA = int(np.sum(np.abs(np.linalg.eigvalsh(Qp.T @ T @ Qp)) < 1e-8))
    nT = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    return nC, nA, nT


cnt = Counter()
sol = Solver(options={"polar": "rnd", "seed": str(seed)})
for c in F.clauses:
    sol.add_clause(c)
for t in range(samples):
    ok, model = sol.solve()
    if not ok:
        break
    G = np.zeros((n, n))
    lits = []
    for (i, j), v in e.items():
        if i < j:
            if model[v]:
                G[i, j] = G[j, i] = 1
            lits.append(-v if model[v] else v)
    sol.add_clause(rng.sample(lits, 40))       # push the solver elsewhere (not a full no-good)
    cnt[("random", stats(G)[0])] += 1
for pat in sys.argv[3:]:
    for f in glob.glob(pat):
        d = json.load(open(f))
        if "edges" not in d:
            continue
        G = np.zeros((n, n))
        for i, j in d["edges"]:
            G[i, j] = G[j, i] = 1
        nC, nA, nT = stats(G)
        cnt[("file", nC, "nullity", nT)] += 1
for k, v in sorted(cnt.items(), key=str):
    print(k, v)
