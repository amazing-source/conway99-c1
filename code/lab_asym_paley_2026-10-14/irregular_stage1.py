"""Stage 1 for an irregular kept set R inside block 0 (14/10/2026): all families of candidate rows of the freed block
vertices that are pairwise compatible (symmetry + exact number of common neighbours), exhaustive. If the only family
is the input's, the block is forced back and the completions are those of the full-block census (NOTE_SPREADFREE 6h).
usage: python irregular_stage1.py <edge file> <size> <seed> <cap>   (environment PYLIB)"""
import itertools
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T
import boundary_census as BC

path, size, seed, cap = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
A = T.load(path)
n = len(A)
adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
rng = random.Random(seed)
R = sorted(rng.sample(range(81), size))
Rs = set(R)
F = [v for v in range(n) if v not in Rs]
freed = [v for v in range(81) if v not in Rs]
rows = {f: [frozenset(N) for N in BC.rows_of(adj, R, Rs, F, f, cap)] for f in freed}
own = {f: frozenset(adj[f] - Rs) for f in freed}
assert all(own[f] in rows[f] for f in freed)


def compatible(f, Nf, g, Ng):
    if (g in Nf) != (f in Ng):
        return False
    need = (1 if g in Nf else 2) - len(adj[f] & adj[g] & Rs)
    return len(Nf & Ng) == need


multi = [f for f in freed if len(rows[f]) > 1]
print("freed block vertices: %d; with more than one candidate row: %d %s" % (len(freed), len(multi),
      [len(rows[f]) for f in multi]), flush=True)
fams = 0
other = 0
for choice in itertools.product(*[range(len(rows[f])) for f in multi]):
    pick = {f: own[f] for f in freed}
    for f, c in zip(multi, choice):
        pick[f] = rows[f][c]
    if all(compatible(f, pick[f], g, pick[g]) for f, g in itertools.combinations(freed, 2)):
        fams += 1
        if any(pick[f] != own[f] for f in freed):
            other += 1
print("pairwise compatible families: %d, of which different from the input: %d" % (fams, other), flush=True)
