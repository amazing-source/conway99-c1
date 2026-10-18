"""Faster complete enumeration of the integer Grams R allowed for one template (LAB, 18/10/2026).
Same model as gram_cover_enum.py (same constraints, same anchors), in two phases:
  1. lazy exact PSD cuts as in gram_cover_enum.py (each cut v^T R v >= 0 or <= 28 |v|^2 is valid for every allowed
     R); each PSD solution is recorded and forbidden on its anchor block;
  2. after a few seconds, one CP-SAT run with enumerate_all_solutions on the model with all these cuts: every
     solution is tested exactly (rational elimination, d x d with d = dim ker C) for X >= 0 and 28 (L^T L)^-1 - X >= 0,
     where X is the anchor block and L the lift (R = L X L^T, L = identity on the anchors).  The second test is
     equivalent to 28 I - R >= 0 (congruence on im L, and R vanishes on (im L)^perp).
The list is complete iff phase 1 ends INFEASIBLE or the phase-2 enumeration ends OPTIMAL/INFEASIBLE.
usage: python gram_cover_enum2.py <catalogue> <template index> <max seconds> <out.json> [phase-1 seconds]"""
import gzip
import json
import sys
import time
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cle3_gram as GR                                   # noqa: E402
from three_star_ambient_upper import psd_or_witness      # noqa: E402

cat, ti, secs, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
phase1 = float(sys.argv[5]) if len(sys.argv) > 5 else 10.0
data = json.load(gzip.open(cat, "rt") if cat.endswith(".gz") else open(cat))
t = data["open"][ti]["template"] if "open" in data else data["templates"][ti]
edges, nodes, links = GR.template_graph(t)
m = len(edges)
incidence = sp.zeros(len(nodes), m)
for i, (a, b) in enumerate(links):
    incidence[a, i] = incidence[b, i] = 1
kernel = sp.Matrix.hstack(*incidence.nullspace())
anchors = list(kernel.T.rref()[1])
d = len(anchors)
lift = kernel * kernel.extract(anchors, list(range(d))).inv()
assert lift.extract(anchors, list(range(d))) == sp.eye(d)
upper = 28 * (lift.T * lift).inv()
upper_q = [[Fraction(int(sp.fraction(upper[i, j])[0]), int(sp.fraction(upper[i, j])[1])) for j in range(d)] for i in range(d)]


def psd(a):
    """Exact test for a symmetric rational matrix: pivot on the first diagonal entry (zero pivot needs a zero row)."""
    a = [row[:] for row in a]
    while a:
        p = a[0][0]
        if p < 0 or (p == 0 and any(a[0][1:])):
            return False
        if p == 0:
            a = [row[1:] for row in a[1:]]
        else:
            a = [[a[i][j] - a[i][0] * a[0][j] / p for j in range(1, len(a))] for i in range(1, len(a))]
    return True


model = cp_model.CpModel()
R = [[None] * m for _ in range(m)]
for i in range(m):
    R[i][i] = model.new_int_var_from_domain(cp_model.Domain.from_values([4, 6, 8]), "r%d_%d" % (i, i))
    for j in range(i):
        common = set(edges[i]) & set(edges[j])
        R[i][j] = R[j][i] = model.new_int_var(-8, 0 if common else 4, "r%d_%d" % (j, i))
        if common:
            root = next(iter(common))
            same = any(r == root and all((set(e) - {root}) <= set(part) for e in (edges[i], edges[j])) for r, part in nodes)
            if not same:
                model.add(R[i][j] == 0)
for node in range(len(nodes)):
    inc = [i for i, ends in enumerate(links) if node in ends]
    for j in range(m):
        model.add(sum(R[i][j] for i in inc) == 0)
    if len(inc) >= 3:
        for size in range(1, len(inc)):
            for U in combinations(inc, size):
                if inc[0] in U:
                    rest = [f for f in inc if f not in U]
                    model.add(sum(R[e][f] for e in U for f in rest) <= -2)
model.add(sum(R[i][i] for i in range(m)) <= 28 * len(anchors))
allowed = [(a, b, c) for a in (4, 6, 8) for b in (4, 6, 8) for c in range(-8, 5) if c * c <= a * b]
for i, j in combinations(range(m), 2):
    model.add_allowed_assignments([R[i][i], R[j][j], R[i][j]], allowed)
pairs = [(i, j) for i in anchors for j in anchors if i <= j]
found, seen, cuts, t0, status = [], set(), 0, time.monotonic(), None
solver = cp_model.CpSolver()
solver.parameters.num_search_workers = 1
solver.parameters.random_seed = 0
while time.monotonic() - t0 < min(phase1, secs):
    solver.parameters.max_time_in_seconds = max(0.1, min(phase1, secs) - (time.monotonic() - t0))
    st = solver.solve(model)
    if st == cp_model.INFEASIBLE:
        status = "COMPLETE"
        break
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        break
    cand = sp.Matrix([[solver.value(v) for v in row] for row in R])
    low = psd_or_witness(cand.extract(anchors, anchors))
    if not low["psd"]:
        vec = [0] * m
        for i, x in zip(anchors, low["integer_witness"]):
            vec[i] = x
        model.add(sum(vec[i] * vec[j] * R[i][j] for i in range(m) for j in range(m) if vec[i] and vec[j]) >= 0)
        cuts += 1
        continue
    up = psd_or_witness(28 * sp.eye(m) - cand)
    if not up["psd"]:
        vec = up["integer_witness"]
        model.add(sum(vec[i] * vec[j] * R[i][j] for i in range(m) for j in range(m) if vec[i] and vec[j]) <= 28 * sum(x * x for x in vec))
        cuts += 1
        continue
    key = tuple(int(cand[i, j]) for i, j in pairs)
    assert key not in seen
    seen.add(key)
    found.append([[int(x) for x in row] for row in cand.tolist()])
    model.add_forbidden_assignments([R[i][j] for i, j in pairs], [list(key)])
phase1_found, counts = len(found), {"candidates": 0, "not_psd": 0, "exceeds_28I": 0}
if status is None:
    class Collector(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            counts["candidates"] += 1
            X = [[Fraction(self.value(R[i][j])) for j in anchors] for i in anchors]
            if not psd(X):
                counts["not_psd"] += 1
                return
            if not psd([[upper_q[a][b] - X[a][b] for b in range(d)] for a in range(d)]):
                counts["exceeds_28I"] += 1
                return
            key = tuple(self.value(R[i][j]) for i, j in pairs)
            assert key not in seen
            seen.add(key)
            found.append([[self.value(R[i][j]) for j in range(m)] for i in range(m)])
    rem = secs - (time.monotonic() - t0)
    if rem > 0:
        s2 = cp_model.CpSolver()
        s2.parameters.num_search_workers = 1
        s2.parameters.enumerate_all_solutions = True
        s2.parameters.max_time_in_seconds = rem
        st2 = s2.solve(model, Collector())
        status = "COMPLETE" if st2 in (cp_model.OPTIMAL, cp_model.INFEASIBLE) else "TIME_LIMIT"
    else:
        status = "TIME_LIMIT"
json.dump({"template_index": ti, "edges": edges, "anchors": anchors, "status": status, "psd_cuts": cuts,
           "phase1_found": phase1_found, "phase2_counts": counts, "gram_count": len(found), "grams": found,
           "seconds": round(time.monotonic() - t0, 1)}, open(out, "w"), default=int)
print(json.dumps({"template_index": ti, "status": status, "gram_count": len(found), "psd_cuts": cuts,
                  "phase1_found": phase1_found, "phase2": counts, "seconds": round(time.monotonic() - t0, 1),
                  "dim_ker_C": d}))
