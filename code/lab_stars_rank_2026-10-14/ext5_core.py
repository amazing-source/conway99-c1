"""Minimal obstruction to adding the fifth star (LAB 16/10/2026).

Model: CP-SAT version of the admissibility constraints (cp6.py) on the labels meeting the given stars.  The adjacency of
a base four-star structure is imposed pair by pair, each pair (a, b) only under the two assumption literals g_a, g_b
(one per base label).  An INFEASIBLE answer returns a sufficient set of base labels; it is then shrunk by deletion
(each label removed in turn, kept out if the rest is still infeasible).  The result is a set A of base labels such that
the induced base adjacency on A alone cannot be completed: a forbidden local configuration.
usage: python ext5_core.py <stars> <base json> <out json> [seconds per solve]"""
import itertools
import json
import sys
import time

from ortools.sat.python import cp_model

MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(14), 2) if w != MATE(u)]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


stars = [int(t) for t in sys.argv[1].split(",")]
base, out = sys.argv[2], sys.argv[3]
secs = float(sys.argv[4]) if len(sys.argv) > 4 else 60.0
S = [l for l in LABELS if any(y in l for y in stars)]
idx = {l: i for i, l in enumerate(S)}
n = len(S)
bd = json.load(open(base))
bl = [frozenset(x) for x in bd["labels"]]
bE = set(tuple(sorted(x)) for x in bd["edges"])
bidx = [idx[l] for l in bl]


def solve(active):
    m = cp_model.CpModel()
    e = {}
    for i, j in itertools.combinations(range(n), 2):
        e[(i, j)] = e[(j, i)] = m.NewBoolVar("")
    for l in S:
        i = idx[l]
        for y in range(14):
            lits = [e[(i, idx[t])] for t in S if y in t and t != l]
            if lits:
                c = count_needed(l, y)
                m.Add(sum(lits) == c) if y in stars else m.Add(sum(lits) <= c)
    for i, j in itertools.combinations(range(n), 2):
        s = len(S[i] & S[j])
        prods = []
        for t in range(n):
            if t not in (i, j):
                p = m.NewBoolVar("")
                m.Add(p >= e[(i, t)] + e[(j, t)] - 1)
                prods.append(p)
        m.Add(sum(prods) + s + e[(i, j)] <= 2)
    act = set(active)
    for a, b in itertools.combinations(range(len(bl)), 2):
        if a in act and b in act:
            m.Add(e[(bidx[a], bidx[b])] == (1 if (a, b) in bE else 0))
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 1
    sv.parameters.max_time_in_seconds = secs
    return sv.StatusName(sv.Solve(m))


t0 = time.time()
full = list(range(len(bl)))
st = solve(full)
print("full base: %s" % st, flush=True)
core = full if st == "INFEASIBLE" else None
log = []
if core:
    for a in list(core):
        trial = [x for x in core if x != a]
        r = solve(trial)
        log.append((sorted(bl[a]), r))
        if r == "INFEASIBLE":
            core = trial
        print("  drop %s -> %s (core %d)" % (sorted(bl[a]), r, len(core)), flush=True)
res = {"stars": stars, "base": base, "full": st,
       "core_labels": [sorted(bl[a]) for a in core] if core else None,
       "core_edges": [[sorted(bl[a]), sorted(bl[b])] for a, b in itertools.combinations(core, 2) if (a, b) in bE]
       if core else None, "log": log, "seconds": time.time() - t0}
json.dump(res, open(out, "w"), indent=1)
print("minimal core: %d labels" % (len(core) if core else -1), res["core_labels"], flush=True)
print("core edges:", res["core_edges"], flush=True)
