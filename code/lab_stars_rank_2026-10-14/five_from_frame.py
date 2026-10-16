"""Five-star completion of one of Codex's star frames (LAB 16/10/2026).
The frame gives complete rows on the 84 labels for some labels (all of L_4, possibly more).  We fix every entry of
those rows towards the 52 labels of the stars 0..4 and ask CP-SAT for the rest of the five-star structure, with the
constraints of cp6.py:
  (C1)  exact counts towards the star letters 0..4, (C1') upper bounds towards the other letters;
  (C2)  common label neighbours inside S + shared letters + [l ~ l'] <= 2.
FEASIBLE gives the first admissible five-star structure (saved); INFEASIBLE means this frame has no five-star
completion (CP-SAT proof, no certificate).
usage: python five_from_frame.py <frame json> <seconds> <out json> [--rows-only-L4]"""
import itertools
import json
import sys
import time

from ortools.sat.python import cp_model

MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(14), 2) if w != MATE(u)]
stars = [0, 1, 2, 3, 4]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


frame = json.load(open(sys.argv[1], encoding="utf-8"))["global_new_rows"]
secs = float(sys.argv[2])
out = sys.argv[3]
only4 = "--rows-only-L4" in sys.argv
lab84 = [frozenset(x) for x in frame["labels"]]
pos84 = {l: i for i, l in enumerate(lab84)}
rows = {frozenset(r): frame["rows"][k] for k, r in enumerate(frame["row_labels"])}
if only4:
    rows = {r: v for r, v in rows.items() if 4 in r}
S = [l for l in LABELS if any(y in l for y in stars)]
idx = {l: i for i, l in enumerate(S)}
n = len(S)
m = cp_model.CpModel()
e = {}
for i, j in itertools.combinations(range(n), 2):
    e[(i, j)] = e[(j, i)] = m.NewBoolVar("e%d_%d" % (i, j))
for l in S:
    i = idx[l]
    for y in range(14):
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
nfix = 0
conflict = 0
seen = set()
for r, v in rows.items():
    for t in S:
        if t == r:
            continue
        key = frozenset((r, t))
        val = v[pos84[t]]
        if key in seen:
            # both rows given: they must agree
            other = rows[t][pos84[r]]
            if other != val:
                conflict += 1
            continue
        seen.add(key)
        m.Add(e[(idx[r], idx[t])] == val)
        nfix += 1
print("frame %s: %d fixed rows (%s), %d fixed pairs, %d row conflicts"
      % (sys.argv[1].split("/")[-1], len(rows), sorted(sorted(r) for r in rows), nfix, conflict), flush=True)
solver = cp_model.CpSolver()
solver.parameters.num_search_workers = 1
solver.parameters.max_time_in_seconds = secs
t0 = time.time()
st = solver.Solve(m)
name = solver.StatusName(st)
res = {"frame": sys.argv[1], "rows_fixed": [sorted(r) for r in rows], "status": name, "seconds": time.time() - t0}
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    res["labels"] = [sorted(l) for l in S]
    res["edges"] = [[i, j] for i, j in itertools.combinations(range(n), 2) if solver.Value(e[(i, j)])]
json.dump(res, open(out, "w"))
print("status %s in %.1f s" % (name, res["seconds"]), flush=True)
