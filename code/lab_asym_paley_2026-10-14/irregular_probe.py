"""Feasibility probe for Codex's variant (14/10/2026): keep an IRREGULAR set R of 54 vertices inside block 0 (0..80) of
the sixth graph, with trivial setwise stabiliser in Aut(G); everything else free. Measures the number of candidate rows
of one freed block vertex and one outside vertex (boundary_census.rows_of, CryptoMiniSat, exact), with a cap.
No census is run. usage: python irregular_probe.py <edge file> <seed> <cap>   (environment PYLIB)"""
import os
import random
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firstorder as FO
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T
import boundary_census as BC

path, seed, cap = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
A = T.load(path)
n = len(A)
rng = random.Random(seed)
R = sorted(rng.sample(range(81), 54))
M = np.zeros_like(A)
M[np.ix_(R, R)] = 1
np.fill_diagonal(M, 0)
t = time.time()
o, _ = FO.group_plain([A, M])
print("R = %d random vertices of block 0 (seed %d); setwise stabiliser in Aut(G): order %d (%.0f s)" % (len(R), seed, o, time.time() - t), flush=True)
Rs = set(R)
F = [v for v in range(n) if v not in Rs]
adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
for f in (next(v for v in range(81) if v not in Rs), 100):
    t = time.time()
    rows = BC.rows_of(adj, R, Rs, F, f, cap)
    print("vertex %d (%s): %s candidate rows (%.0f s)" % (f, "freed block vertex" if f < 81 else "outside vertex",
          len(rows) if rows is not None else "more than %d" % cap, time.time() - t), flush=True)
