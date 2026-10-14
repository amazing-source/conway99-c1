"""Scan of trade regions in a hemisystem graph srg(378,52,1,8) (14/10/2026). For each region F (free pairs inside F),
census_general lists every srg completion (row cap and time limit per region). Regions: unions of j sets X_m (m GQ
lines outside the hemisystem) and random sets of a given size. Any completion different from the input is checked
(A^2 identity), written, and its exact |Aut| computed (prism colours + individualisation-refinement).
usage: python scan378.py <gq.json> <hemi.json> <edges> <out prefix> <seconds per region> <spec> [<spec> ...]
spec: X<j>:<count>  (count regions, each the union of j sets X_m)   or   R<size>:<count>  (random regions)
environment PYLIB"""
import json
import os
import random
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_general as CG
import pq_invariants as PQ
import srg_group2 as S

gqf, hf, ef, prefix, secs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5])
specs = sys.argv[6:]
G = json.load(open(gqf))
H = json.load(open(hf))
lines = [set(l) for l in G["lines"]]
A0 = PQ.load(ef)
n = len(A0)
Hs = set(H)
nonH = [i for i in range(len(lines)) if i not in Hs]
X = {m: {kk for kk, h in enumerate(H) if lines[h] & lines[m]} for m in nonH}
I = np.eye(n, dtype=np.int64)
J = np.ones((n, n), dtype=np.int64)
rng = random.Random(7)
found = 0
for spec in specs:
    kind, rest = spec[0], spec[1:]
    j, count = map(int, rest.split(":"))
    for c in range(count):
        if kind == "X":
            ms = rng.sample(nonH, j)
            F = set().union(*[X[m] for m in ms])
            label = "union of X_m for %d lines" % j
        else:
            F = set(rng.sample(range(n), j))
            label = "random"
        R = [v for v in range(n) if v not in F]
        t = time.time()
        sols, status, info = CG.completions(A0, R, secs, 52, 1, 8, maxsol=50, rowcap=3000)
        others = [X1 for X1 in sols if not np.array_equal(X1, A0)]
        print("%s (%s), |F| = %d: %d completions, %d new, status %s, rows max %s (%.0f s)"
              % (spec, label, len(F), len(sols), len(others), status, info.get("rows_max"), time.time() - t), flush=True)
        for X1 in others:
            found += 1
            ok = np.array_equal(X1 @ X1, 44 * I - 7 * X1 + 8 * J)
            C, _, _, _, _ = PQ.pair_colours(X1)
            o, sizes, gens = S.aut_group(X1, C)
            path = "%s_%d.edges" % (prefix, found)
            with open(path, "w") as fh:
                for a in range(n):
                    for b in range(a + 1, n):
                        if X1[a, b]:
                            fh.write("%d %d\n" % (a, b))
            print("   NEW completion: srg identity %s, %d pairs changed, |Aut| = %d -> %s"
                  % (ok, int(np.abs(X1 - A0).sum()) // 2, o, path), flush=True)
