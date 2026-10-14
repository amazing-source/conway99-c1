"""Probe 2 (14/10/2026): for irregular kept sets R inside block 0 of a graph (random, trivial setwise stabiliser),
count the candidate rows of EVERY freed block vertex. If all are 1, the block is forced back, and the completions are
those of the full-block census (NOTE_SPREADFREE 6h: the seven graphs).
usage: python irregular_probe2.py <edge file> <size> <seed0> <seed1> <cap>   (environment PYLIB)"""
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

path, size, s0, s1, cap = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
A = T.load(path)
n = len(A)
adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
for seed in range(s0, s1 + 1):
    rng = random.Random(seed)
    R = sorted(rng.sample(range(81), size))
    M = np.zeros_like(A)
    M[np.ix_(R, R)] = 1
    np.fill_diagonal(M, 0)
    o, _ = FO.group_plain([A, M])
    Rs = set(R)
    F = [v for v in range(n) if v not in Rs]
    t = time.time()
    counts = []
    for f in range(81):
        if f in Rs:
            continue
        rows = BC.rows_of(adj, R, Rs, F, f, cap)
        counts.append(len(rows) if rows is not None else -1)
    hist = {}
    for c in counts:
        hist[c] = hist.get(c, 0) + 1
    print("%s, %d kept in block 0, seed %d: stabiliser %d; candidate rows of the %d freed block vertices: %s (%.0f s)"
          % (os.path.basename(path), size, seed, o, len(counts), dict(sorted(hist.items())), time.time() - t), flush=True)
