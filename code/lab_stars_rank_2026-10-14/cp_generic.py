"""Calibration of the plain k-star search on other lambda = 1, mu = 2 parameter sets (LAB 16/10/2026).
Same CP-SAT model as cp6.py (C1 exact for the star letters, C1' bounds for the other letters, C2 caps inside S), for a
root with K letters (K = 14 for Conway, K = 22 for srg(243,22,1,2); mates 2i, 2i+1).  No adjacency is fixed: the
solver must FIND an admissible structure.  For K = 22 real structures exist (the eight known srg(243)), so the time
to find one tells how informative an UNKNOWN at K = 14 is.
usage: python cp_generic.py <K> <stars> <seconds> <out json>"""
import itertools
import json
import sys
import time

from ortools.sat.python import cp_model

K = int(sys.argv[1])
stars = [int(t) for t in sys.argv[2].split(",")]
secs = float(sys.argv[3])
out = sys.argv[4]
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


S = [l for l in LABELS if any(y in l for y in stars)]
idx = {l: i for i, l in enumerate(S)}
n = len(S)
m = cp_model.CpModel()
e = {}
for i, j in itertools.combinations(range(n), 2):
    e[(i, j)] = e[(j, i)] = m.NewBoolVar("")
for l in S:
    i = idx[l]
    for y in range(K):
        lits = [e[(i, idx[t])] for t in S if y in t and t != l]
        if not lits:
            continue
        c = count_needed(l, y)
        if y in stars:
            m.Add(sum(lits) == c)
        else:
            m.Add(sum(lits) <= c)
for i, j in itertools.combinations(range(n), 2):
    s = len(S[i] & S[j])
    prods = []
    for t in range(n):
        if t in (i, j):
            continue
        p = m.NewBoolVar("")
        m.Add(p >= e[(i, t)] + e[(j, t)] - 1)
        prods.append(p)
    m.Add(sum(prods) + s + e[(i, j)] <= 2)
# BASE (env): fix the adjacency among the labels of a given structure (keys "labels" or "label_list", and "edges")
import os
nfix = 0
base = os.environ.get("BASE", "")
if base:
    bd = json.load(open(base))
    bl = [frozenset(x) for x in bd.get("labels") if isinstance(x, list)] if isinstance(bd.get("labels"), list) \
        else [frozenset(x) for x in bd["label_list"]]
    bE = set(tuple(sorted(x)) for x in bd["edges"])
    for a, b in itertools.combinations(range(len(bl)), 2):
        if bl[a] in idx and bl[b] in idx:
            m.Add(e[(idx[bl[a]], idx[bl[b]])] == (1 if (a, b) in bE else 0))
            nfix += 1
print("K = %d, stars %s: %d labels, BASE %s (%d fixed pairs)" % (K, stars, n, base, nfix), flush=True)
solver = cp_model.CpSolver()
solver.parameters.num_search_workers = 1
solver.parameters.max_time_in_seconds = secs
t0 = time.time()
st = solver.Solve(m)
name = solver.StatusName(st)
res = {"K": K, "stars": stars, "labels": n, "status": name, "seconds": time.time() - t0}
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    res["label_list"] = [sorted(l) for l in S]
    res["edges"] = [[i, j] for i, j in itertools.combinations(range(n), 2) if solver.Value(e[(i, j)])]
json.dump(res, open(out, "w"))
print("status %s in %.1f s" % (name, res["seconds"]), flush=True)
