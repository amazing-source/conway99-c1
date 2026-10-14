"""Stage 2 for the alternative block family found by irregular_stage1.py (14/10/2026): rebuild the 81 block rows with
the alternative choice, keep the block (all its pairs), list every strongly regular completion of the 162 outside
vertices (boundary_census.completions, exhaustive within the time limit), identify each completion against the eight
known graphs and compute its automorphism group.
usage: python irregular_stage2.py <edge file> <size> <seed> <cap> <seconds> <known graphs ...>   (environment PYLIB)"""
import itertools
import os
import random
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T
import boundary_census as BC

path, size, seed, cap, secs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
known = [(os.path.basename(p), T.load(p)) for p in sys.argv[6:]]
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


def compatible(f, Nf, g, Ng):
    if (g in Nf) != (f in Ng):
        return False
    need = (1 if g in Nf else 2) - len(adj[f] & adj[g] & Rs)
    return len(Nf & Ng) == need


multi = [f for f in freed if len(rows[f]) > 1]
alts = []
for choice in itertools.product(*[range(len(rows[f])) for f in multi]):
    pick = {f: own[f] for f in freed}
    for f, c in zip(multi, choice):
        pick[f] = rows[f][c]
    if all(compatible(f, pick[f], g, pick[g]) for f, g in itertools.combinations(freed, 2)) and \
            any(pick[f] != own[f] for f in freed):
        alts.append(pick)
print("alternative families: %d" % len(alts), flush=True)
for pick in alts:
    changed = [f for f in freed if pick[f] != own[f]]
    print("  changed freed vertices: %s" % changed, flush=True)
    B = A.copy()
    for f in freed:
        B[f, :] = 0
        B[:, f] = 0
    for f in freed:
        for g in adj[f] & Rs:
            B[f, g] = B[g, f] = 1
        for g in pick[f]:
            B[f, g] = B[g, f] = 1
    # consistency inside the block (pairs among freed vertices must agree both ways)
    sym = all(B[f, g] == B[g, f] for f in range(81) for g in range(81))
    t = time.time()
    sols, status, info = BC.completions(B, list(range(81)), secs, 5000)
    print("  block rebuilt (symmetric: %s); completions of the outside: %d, status %s, %s (%.0f s)"
          % (sym, len(sols), status, info, time.time() - t), flush=True)
    for X in sols:
        name = next((nm for nm, K in known if T.find_iso(X, K) is not None), "NEW")
        o = T.aut_group(X)[0]
        print("    completion: isomorphic to %s, |Aut| = %d" % (name, o), flush=True)
