"""Plain attachment problem (LAB 16/10/2026): is there ANY admissible four-star structure (stars 0..3) to which the labels
{4,6}, ..., {4,5+k} can be attached?  Model of ext_rows.py without base: stars 0..3 exact, every other letter as an upper
bound (letter 4 exact only with --exact4 and k = 8, which is then the plain five-star problem), C2 caps.
This is a relaxation of the five-star problem: INFEASIBLE for some k would exclude Conway's graph (after certification).
usage: python plain_rows.py <k> <seconds> <out json> [--exact4] [--K K]"""
import itertools
import json
import sys
import time

from ortools.sat.python import cp_model

K = int(sys.argv[sys.argv.index("--K") + 1]) if "--K" in sys.argv else 14
k, secs, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
exact = {0, 1, 2, 3} | ({4} if "--exact4" in sys.argv else set())
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


S4 = [l for l in LABELS if any(y in l for y in (0, 1, 2, 3))]
S = S4 + [frozenset((4, t)) for t in range(6, 6 + k)]
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
        if y in exact:
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
print("K = %d, k = %d labels {4,t}, exact letters %s: %d labels" % (K, k, sorted(exact), n), flush=True)
sv = cp_model.CpSolver()
sv.parameters.num_search_workers = 1
sv.parameters.max_time_in_seconds = secs
t0 = time.time()
st = sv.Solve(m)
res = {"K": K, "k": k, "exact": sorted(exact), "status": sv.StatusName(st), "seconds": time.time() - t0}
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    res["labels"] = [sorted(l) for l in S]
    res["edges"] = [[i, j] for i, j in itertools.combinations(range(n), 2) if sv.Value(e[(i, j)])]
json.dump(res, open(out, "w"))
print("status %s in %.1f s" % (res["status"], res["seconds"]), flush=True)
