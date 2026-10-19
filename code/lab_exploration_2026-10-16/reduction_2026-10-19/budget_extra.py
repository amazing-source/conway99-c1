"""Extra numbers for NOTE_REDUCTION (LAB 19/10/2026), heuristic: (1) L1 budget of the PLANTED instances (expected number
of solutions other than the planted one, margins of a random 3D matching), n = 8, 10, 12; (2) the L4 factor, i.e. the
probability that a random admissible name triple has exactly k_i names in each component, for c = 3 (2,2,2) and c = 6,
estimated exactly by enumeration of the 60^2 (q-pair, s-pair) choices for each p-pair.
usage: python budget_extra.py"""
import math
import random
import numpy as np
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from budget import class_gram, lg_fact, pair_logp
from ll_test import pairs_of
out = {}
for n in (8, 10, 12):
    A, m = class_gram(n)
    P = pairs_of(n)
    vals = []
    for seed in range(5):
        rng = random.Random(seed)
        q, s = rng.sample(range(m), m), rng.sample(range(m), m)
        E = np.zeros((3 * n, m), dtype=np.int64)
        for f in range(m):
            for c, pr in enumerate((P[f], P[q[f]], P[s[f]])):
                for i in pr:
                    E[c * n + i, f] = 1
        K = E @ E.T
        lp = sum(pair_logp(n, B, A, m)[0] for B in (K[0:n, n:2*n], K[0:n, 2*n:], K[n:2*n, 2*n:]))
        vals.append(round(2 * lg_fact(m) + lp, 1))
    out["planted_n%d_L1_budget" % n] = vals
# L4 factor: lines 0..5 of each class; component of a line = block index
for name, blocks in (("c3_222", [0, 0, 1, 1, 2, 2]), ("c6", [0, 1, 2, 3, 4, 5]), ("c2_33", [0, 0, 0, 1, 1, 1]), ("c2_15", [0, 1, 1, 1, 1, 1])):
    sizes = {}
    for b in blocks:
        sizes[b] = sizes.get(b, 0) + 1          # lines per class in the block = k_i
    P = pairs_of(12)
    ok = tot = 0
    for pp in P:
        for qq in P:
            for ss in P:
                cnt = {}
                for pr in (pp, qq, ss):
                    for i in pr:
                        b = blocks[i // 2]
                        cnt[b] = cnt.get(b, 0) + 1
                tot += 1
                ok += all(cnt.get(b, 0) == k for b, k in sizes.items())
    p = ok / tot
    out["L4_" + name] = dict(p_per_far=round(p, 5), log10_factor_60=round(60 * math.log10(p), 1))
import json
print(json.dumps(out, indent=1))
