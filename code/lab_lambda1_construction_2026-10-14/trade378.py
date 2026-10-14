"""Trades in a hemisystem graph srg(378,52,1,8) (14/10/2026): free the pairs inside F = X_m u X_m' (m, m' two GQ lines
outside the hemisystem; X_m = hemisystem lines meeting m), keep every pair meeting R = V - F, list all srg completions
(census_general.completions), check each one (A^2 identity), compare with the input, compute |Aut| of new ones.
usage: python trade378.py <gq.json> <hemi.json> <edges> <kind: opposite|concurrent> <pair index> <seconds> <out prefix>
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
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T

gqf, hf, ef, kind, idx, secs, prefix = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), float(sys.argv[6]), sys.argv[7]
G = json.load(open(gqf))
H = json.load(open(hf))
lines = [set(l) for l in G["lines"]]
A0 = PQ.load(ef)
n = len(A0)
Hs = set(H)
nonH = [i for i in range(len(lines)) if i not in Hs]
X = {m: {kk for kk, h in enumerate(H) if lines[h] & lines[m]} for m in nonH}
rng = random.Random(1)
if kind == "opposite":
    pairs = [(a, b) for a, b in ((rng.choice(nonH), rng.choice(nonH)) for _ in range(4000)) if a != b and not (lines[a] & lines[b])]
else:
    pairs = [(a, b) for a, b in ((rng.choice(nonH), rng.choice(nonH)) for _ in range(40000)) if a != b and (lines[a] & lines[b])]
m1, m2 = pairs[idx]
F = sorted(X[m1] | X[m2])
R = [v for v in range(n) if v not in set(F)]
print("%s pair %d: lines %d, %d; |F| = %d free vertices, %d kept" % (kind, idx, m1, m2, len(F), len(R)), flush=True)
t = time.time()
sols, status, info = CG.completions(A0, R, secs, 52, 1, 8, maxsol=200, rowcap=4000)
print("census: %d completions, status %s, info %s (%.0f s)" % (len(sols), status, info, time.time() - t), flush=True)
I = np.eye(n, dtype=np.int64)
J = np.ones((n, n), dtype=np.int64)
new = 0
for X1 in sols:
    ok = np.array_equal(X1 @ X1, 44 * I - 7 * X1 + 8 * J)
    same = np.array_equal(X1, A0)
    diff = int(np.abs(X1 - A0).sum()) // 2
    if same:
        continue
    new += 1
    C, _, _, _, _ = PQ.pair_colours(X1)
    o, sizes, gens = S.aut_group(X1, C)
    path = "%s_%d.edges" % (prefix, new)
    with open(path, "w") as fh:
        for a in range(n):
            for b in range(a + 1, n):
                if X1[a, b]:
                    fh.write("%d %d\n" % (a, b))
    print("  completion %d: srg identity %s; %d pairs changed; |Aut| = %d; written %s" % (new, ok, diff, o, path), flush=True)
