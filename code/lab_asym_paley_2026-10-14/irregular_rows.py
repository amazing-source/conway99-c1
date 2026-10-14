"""Row-list sizes of the freed block vertices for an irregular kept set R inside block 0 (14/10/2026); a vertex above
the cap is reported as '>cap'. usage: python irregular_rows.py <edge file> <size> <seed> <cap>   (environment PYLIB)"""
import os
import random
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T
import boundary_census as BC

path, size, seed, cap = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
A = T.load(path)
n = len(A)
adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
R = sorted(random.Random(seed).sample(range(81), size))
Rs = set(R)
F = [v for v in range(n) if v not in Rs]
t = time.time()
out = []
for f in range(81):
    if f in Rs:
        continue
    r = BC.rows_of(adj, R, Rs, F, f, cap)
    out.append(len(r) if r is not None else ">%d" % cap)
print("%d kept (seed %d): row counts of the %d freed block vertices: %s (%.0f s)" % (size, seed, len(out), out, time.time() - t), flush=True)
