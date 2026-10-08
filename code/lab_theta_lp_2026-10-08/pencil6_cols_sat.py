"""C1, lab session, 2026-10-08. A line in six grids with the CANONICAL column structure: is there a graph on the 60 names?
  python pencil6_cols_sat.py [seconds] [workers]
NEW FACT USED: the column part of the 60 names can be fixed (the 60 labelled synthemes outside a total = ordered stars
of the Petersen graph), so the unknown is only the 8-regular graph H on these names (and the rows, relaxed away here).
Necessary conditions kept (NOTE 17.46), all implied by "srg(99,14,1,2) with a line in six grids and these columns":
  (a) H is 8-regular;
  (b) for every name b and grid k: exactly 2 neighbours with the same column at k, and 3 in each other column;
  (c) for b != b': common(b,b') + agree(b,b') = 2 - h(b,b'), where 0 <= agree <= number of grids where the columns agree
      (agree = coordinates where column AND row agree; rows are not modelled): so
      common <= 2 - h  and  common >= 2 - h - (column agreements).
UNSAT would exclude a line in six grids with this column structure (other column structures exist: W = 4 + kernel).
SAT proves nothing (rows relaxed). CP-SAT, one process, memory below 3 GB, time limit given (default 280 s)."""
import sys, time
from itertools import combinations, permutations
from ortools.sat.python import cp_model
T0 = time.time(); limit = float(sys.argv[1]) if len(sys.argv) > 1 else 280.0; workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
pts = range(6); duads = [frozenset(d) for d in combinations(pts, 2)]
synth = [frozenset(a) for a in combinations(duads, 3) if len(frozenset().union(*a)) == 6]
totals = [t for t in combinations(synth, 5) if len(frozenset().union(*t)) == 15]
out = [s for s in synth if s not in totals[0]]
names = [(x, lam) for x in range(10) for lam in permutations(range(3))]
def col(nm, k):
    x, lam = nm; ds = sorted(out[x], key=sorted)
    return next(lam[t] for t in range(3) if k in ds[t])
C = [[col(nm, k) for k in pts] for nm in names]; n = len(names)
m = cp_model.CpModel(); h = {}
for i, j in combinations(range(n), 2): h[i, j] = h[j, i] = m.NewBoolVar("h%d_%d" % (i, j))
for i in range(n):
    m.Add(sum(h[i, j] for j in range(n) if j != i) == 8)
    for k in pts:
        for c in range(3):
            m.Add(sum(h[i, j] for j in range(n) if j != i and C[j][k] == c) == (2 if c == C[i][k] else 3))
nprod = 0
for i, j in combinations(range(n), 2):
    ag = sum(C[i][k] == C[j][k] for k in pts); cm = []
    for l in range(n):
        if l in (i, j): continue
        p = m.NewBoolVar(""); m.AddBoolAnd([h[i, l], h[j, l]]).OnlyEnforceIf(p); m.AddBoolOr([h[i, l].Not(), h[j, l].Not(), p]); cm.append(p); nprod += 1
    s = sum(cm)
    m.Add(s <= 2 - h[i, j]); m.Add(s >= 2 - h[i, j] - ag) if ag < 2 else (m.Add(s >= 1 - ag).OnlyEnforceIf(h[i, j]) if ag < 1 else None)
    if ag == 1: m.Add(s >= 1).OnlyEnforceIf(h[i, j].Not())
print("model: %d names, %d edge variables, %d products  [%.0f s]" % (n, n * (n - 1) // 2, nprod, time.time() - T0), flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = limit; sol.parameters.num_workers = workers; sol.parameters.max_memory_in_mb = 3000
st = sol.Solve(m)
print("status %s after %.0f s (conflicts %d, branches %d)" % (sol.StatusName(st), sol.WallTime(), sol.NumConflicts(), sol.NumBranches()), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    E = [(i, j) for i, j in combinations(range(n), 2) if sol.Value(h[i, j])]
    import json; json.dump({"names": [[x, list(l)] for x, l in names], "edges": E}, open("pencil6_cols_sat_solution.json", "w"))
    tri = sum(1 for i, j, l in combinations(range(n), 3) if sol.Value(h[i, j]) and sol.Value(h[i, l]) and sol.Value(h[j, l]))
    print("a graph satisfying the column-level conditions exists: %d edges, %d triangles (saved); rows not checked" % (len(E), tri))
