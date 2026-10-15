"""Which axioms does ODD9 need? (LAB 15/10/2026)
Random four-star structures satisfying only (C1) (exact star counts), or (C1) + (C1'), or the full model; for each,
the exact odd gains beyond X_l and X_m (odd9_check.gain) and c(l), c(m).
usage: python odd9_axioms.py <C1|C1p|full> <count> <seed>"""
import itertools
import random
import sys

import numpy as np
from pycryptosat import Solver

import stars_rank
from stars_rank import kval, CNF, count_needed, LABELS
from odd9_check import gain
from z5_enum import exact_rank

mode, cnt, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)
stars = [0, 1, 2, 3]
if mode == "full":
    S, idx, e, F = stars_rank.build(stars, rng)
else:
    S = [l for l in LABELS if any(y in l for y in stars)]
    idx = {l: i for i, l in enumerate(S)}
    F = CNF()
    pairs = list(itertools.combinations(range(len(S)), 2))
    rng.shuffle(pairs)
    e = {}
    for i, j in pairs:
        e[(i, j)] = e[(j, i)] = F.var()
    for l in S:
        i = idx[l]
        for y in stars:
            lits = [e[(i, idx[t])] for t in S if y in t and t != l]
            c = count_needed(l, y)
            for sub in itertools.combinations(lits, c + 1):
                F.add([-x for x in sub])
            if c == 1:
                F.add(list(lits))
            else:
                for x in lits:
                    F.add([z for z in lits if z != x])
    if mode == "C1p":
        for l in S:
            i = idx[l]
            for y in range(14):
                if y in stars:
                    continue
                lits = [e[(i, idx[t])] for t in S if y in t and t != l]
                c = count_needed(l, y)
                for sub in itertools.combinations(lits, c + 1):
                    F.add([-x for x in sub])
n = len(S)
K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
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
    res = []
    cs = []
    for (a, a2, b, b2) in ((0, 1, 2, 3), (2, 3, 0, 1)):
        Xl = [i for i in range(n) if S[i] & {a, a2}]
        cs.append(23 - exact_rank(M8[np.ix_(Xl, Xl)].tolist()))
        odd = []
        for y in range(4, 14):
            v = np.zeros(n, dtype=np.int64)
            v[idx[frozenset((b, y))]] = 1
            v[idx[frozenset((b2, y))]] = -1
            odd.append(v)
        res.append(gain(M8, Xl, odd))
    key = (res[0], res[1])
    hist[key] = hist.get(key, 0) + 1
    if res[0] != 9 or res[1] != 9:
        print("structure %d: odd gains %s, c %s" % (t, res, cs), flush=True)
print("%s: histogram of (odd gain beyond X_l, beyond X_m):" % mode, hist)
