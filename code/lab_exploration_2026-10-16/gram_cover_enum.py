"""Enumerate ALL integer Gram matrices R allowed by the quotient system of cle3_gram.py for one template (LAB, 18/10).
Same constraints as cle3_gram.solve (C R = 0, domains, zeros across components, connectivity cuts, trace, 2x2 minors,
exact lazy PSD cuts for R >= 0 and 28 I - R >= 0); each R found PSD is recorded and forbidden on its anchor block
(R is determined by its anchor block since im R lies in ker C), until the model is infeasible: the list is complete.
Purpose: a 'Gram cover' of the template, to be imposed on the exact complete-star model as a table (Codex's gram_cover
mechanism), since the complete-star model does not itself impose R >= 0.
usage: python gram_cover_enum.py <catalogue json(.gz) with 'open'> <template index> <max seconds> <out.json>"""
import gzip
import json
import sys
import time
from itertools import combinations
from pathlib import Path

import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cle3_gram as GR                                   # noqa: E402
from three_star_ambient_upper import psd_or_witness      # noqa: E402

cat, ti, secs, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
data = json.load(gzip.open(cat, "rt") if cat.endswith(".gz") else open(cat))
t = data["open"][ti]["template"] if "open" in data else data["templates"][ti]
edges, nodes, links = GR.template_graph(t)
m = len(edges)
incidence = sp.zeros(len(nodes), m)
for i, (a, b) in enumerate(links):
    incidence[a, i] = incidence[b, i] = 1
kernel = sp.Matrix.hstack(*incidence.nullspace())
anchors = list(kernel.T.rref()[1])
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
solver = cp_model.CpSolver()
solver.parameters.num_search_workers = 1
solver.parameters.random_seed = 0
found, cuts, t0, status = [], 0, time.monotonic(), "COMPLETE"
pairs = [(i, j) for i in anchors for j in anchors if i <= j]
while True:
    rem = secs - (time.monotonic() - t0)
    if rem <= 0:
        status = "TIME_LIMIT"
        break
    solver.parameters.max_time_in_seconds = rem
    st = solver.solve(model)
    if st == cp_model.INFEASIBLE:
        break
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        status = "UNKNOWN"
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
    found.append(cand.tolist())
    model.add_forbidden_assignments([R[i][j] for i, j in pairs], [[int(cand[i, j]) for i, j in pairs]])
json.dump({"template_index": ti, "edges": edges, "anchors": anchors, "status": status, "psd_cuts": cuts,
           "gram_count": len(found), "grams": found, "seconds": round(time.monotonic() - t0, 1)}, open(out, "w"), default=int)
print(json.dumps({"template_index": ti, "status": status, "gram_count": len(found), "psd_cuts": cuts,
                  "seconds": round(time.monotonic() - t0, 1), "dim_ker_C": len(anchors)}))
