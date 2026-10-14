"""Stage 1 by depth-first search (14/10/2026): irregular kept set R (random, inside block 0), all families of candidate
rows of the freed block vertices that are pairwise compatible; vertices ordered by number of candidates, forward
checking. Prints the number of families and how many differ from the input.
usage: python irregular_dfs1.py <edge file> <size> <seed> <cap> <seconds>   (environment PYLIB)"""
import os
import random
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T
import boundary_census as BC

path, size, seed, cap, secs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
A = T.load(path)
n = len(A)
adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
rng = random.Random(seed)
R = sorted(rng.sample(range(81), size))
Rs = set(R)
F = [v for v in range(n) if v not in Rs]
freed = [v for v in range(81) if v not in Rs]
t0 = time.time()
rows = {f: [frozenset(N) for N in BC.rows_of(adj, R, Rs, F, f, cap)] for f in freed}
own = {f: frozenset(adj[f] - Rs) for f in freed}
print("rows listed in %.0f s: %s" % (time.time() - t0, sorted(len(rows[f]) for f in freed)), flush=True)


def compatible(f, Nf, g, Ng):
    if (g in Nf) != (f in Ng):
        return False
    need = (1 if g in Nf else 2) - len(adj[f] & adj[g] & Rs)
    return len(Nf & Ng) == need


order = sorted(freed, key=lambda f: len(rows[f]))
dom = {f: list(range(len(rows[f]))) for f in freed}
fams = []
nodes = [0]
t1 = time.time()
timed_out = [False]


def rec(i, pick, dom):
    if time.time() - t1 > secs:
        timed_out[0] = True
        return
    nodes[0] += 1
    if i == len(order):
        fams.append(dict(pick))
        return
    f = order[i]
    for c in dom[f]:
        Nf = rows[f][c]
        newdom = {}
        ok = True
        for g in order[i + 1:]:
            d = [e for e in dom[g] if compatible(f, Nf, g, rows[g][e])]
            if not d:
                ok = False
                break
            newdom[g] = d
        if not ok:
            continue
        pick[f] = Nf
        rec(i + 1, pick, {**dom, **newdom})
        del pick[f]
        if timed_out[0]:
            return


rec(0, {}, dom)
other = sum(1 for p in fams if any(p[f] != own[f] for f in freed))
print("stage 1 %s: %d families, %d different from the input, %d nodes (%.0f s)"
      % ("INTERRUPTED" if timed_out[0] else "complete", len(fams), other, nodes[0], time.time() - t1), flush=True)
for p in fams[:12]:
    ch = [f for f in freed if p[f] != own[f]]
    if ch:
        print("  family changing %d freed vertices: %s" % (len(ch), ch), flush=True)
