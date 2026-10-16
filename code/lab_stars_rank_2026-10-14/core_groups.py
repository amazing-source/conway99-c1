"""Which admissibility constraints make a symmetric five-star structure impossible? (LAB 16/10/2026)

CP-SAT model of cp6.py, with every constraint row behind its own enforcement literal:
  C1[l,y] (exact count of l towards a star letter y), C1p[l,y] (upper count towards a non-star letter),
  C2[i,j] (common-neighbour cap of a pair).
Symmetry ties (GENS) are hard.  INFEASIBLE returns a sufficient set of rows (SufficientAssumptionsForInfeasibility);
it is then shrunk by deletion within a time budget.  Prints the surviving rows.
usage: python core_groups.py <stars> <gens or none> <out json> [seconds per solve] [deletion budget seconds]"""
import itertools
import json
import sys
import time

from ortools.sat.python import cp_model

MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(14), 2) if w != MATE(u)]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


def parse(cyc):
    h = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    return h


stars = [int(t) for t in sys.argv[1].split(",")]
gens = [] if sys.argv[2] == "none" else [parse(c) for c in sys.argv[2].split("|")]
out = sys.argv[3]
secs = float(sys.argv[4]) if len(sys.argv) > 4 else 30.0
budget = float(sys.argv[5]) if len(sys.argv) > 5 else 600.0
S = [l for l in LABELS if any(y in l for y in stars)]
idx = {l: i for i, l in enumerate(S)}
n = len(S)
rows = []  # (name, builder)
for l in S:
    for y in range(14):
        lits_idx = [idx[t] for t in S if y in t and t != l]
        if lits_idx:
            rows.append((("C1" if y in stars else "C1p", tuple(sorted(l)), y), (idx[l], lits_idx, count_needed(l, y), y in stars)))
for i, j in itertools.combinations(range(n), 2):
    rows.append((("C2", tuple(sorted(S[i])), tuple(sorted(S[j]))), (i, j)))


def solve(active):
    m = cp_model.CpModel()
    e = {}
    for i, j in itertools.combinations(range(n), 2):
        e[(i, j)] = e[(j, i)] = m.NewBoolVar("")
    for h in gens:
        for i, j in itertools.combinations(range(n), 2):
            a = idx[frozenset(h[y] for y in S[i])]
            b = idx[frozenset(h[y] for y in S[j])]
            m.Add(e[(i, j)] == e[(a, b)])
    lits = []
    for r in active:
        name, data = rows[r]
        g = m.NewBoolVar("g%d" % r)
        lits.append(g)
        if name[0] in ("C1", "C1p"):
            i, li, c, exact = data
            s = sum(e[(i, t)] for t in li)
            (m.Add(s == c) if exact else m.Add(s <= c)).OnlyEnforceIf(g)
        else:
            i, j = data
            sh = len(S[i] & S[j])
            prods = []
            for t in range(n):
                if t not in (i, j):
                    p = m.NewBoolVar("")
                    m.Add(p >= e[(i, t)] + e[(j, t)] - 1)
                    prods.append(p)
            m.Add(sum(prods) + sh + e[(i, j)] <= 2).OnlyEnforceIf(g)
    m.AddAssumptions(lits)
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 1
    sv.parameters.max_time_in_seconds = secs
    st = sv.Solve(m)
    core = None
    if st == cp_model.INFEASIBLE:
        core = [active[k] for k, g in enumerate(lits) if g.Index() in set(sv.SufficientAssumptionsForInfeasibility())]
    return sv.StatusName(st), core


t0 = time.time()
st, core = solve(list(range(len(rows))))
print("all %d rows: %s, sufficient core %s rows (%.1f s)" % (len(rows), st, len(core) if core else None, time.time() - t0),
      flush=True)
if core:
    t1 = time.time()
    for r in list(core):
        if time.time() - t1 > budget:
            break
        trial = [x for x in core if x != r]
        s2, c2 = solve(trial)
        if s2 == "INFEASIBLE":
            core = c2 if c2 and len(c2) < len(trial) else trial
    print("after deletion: %d rows (%.1f s)" % (len(core), time.time() - t0), flush=True)
    names = [rows[r][0] for r in core]
    from collections import Counter
    print(Counter(nm[0] for nm in names), flush=True)
    for nm in sorted(names):
        print("  ", nm, flush=True)
    json.dump({"stars": stars, "gens": sys.argv[2], "core": [list(map(str, nm)) for nm in names]}, open(out, "w"), indent=1)
