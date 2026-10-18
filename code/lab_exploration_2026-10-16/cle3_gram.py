"""Integer Gram feasibility for root templates with any kernel dimension (LAB, 18/10/2026).

Adapted from Codex's code/codex/root_component_gram.py (read only, imported for psd_or_witness):
  * no assert on dim ker C (Codex's file assumes <= 4, valid only for c >= 4);
  * E3 (Codex, PROVED): R_ee in {4, 6, 8} on non-grid rectangles (2 = three corner edges is excluded);
  * connectivity of every component (its rectangle multigraph is connected and R restricted to it is its Laplacian
    with even degrees): every proper cut U of a component has sum_{e in U, f not in U} R_ef <= -2.
Everything else is Codex's necessary system: C R = 0, -8 <= R_ef <= 4, R_ef <= 0 on a shared line and = 0 across two
components of one line, 2x2 minors, trace <= 28 dim ker C, lazy exact PSD cuts for R >= 0 and 28 I - R >= 0.
QUOTIENT_FEASIBLE means a small Gram quotient exists, never a Conway graph.
usage: python cle3_gram.py <survivors.json from cle3_by_grids.py> <seconds per template> <output.json> [start end]"""
import json
import sys
import time
from collections import Counter
from itertools import combinations
from pathlib import Path

import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-asymmetry-audit\code\codex")
sys.path.insert(0, str(Path(__file__).resolve().parent))      # copy of Codex's module next to this file (AWS runs)
from three_star_ambient_upper import psd_or_witness  # noqa: E402


def template_graph(t):
    edges = [tuple(e) for e in t["nongrid_edges"]]
    nodes, lookup = [], {}
    for r, parts in enumerate(t["nontrivial_component_groups"]):
        for part in parts:
            lookup.update({(r, j): len(nodes) for j in part})
            nodes.append((r, tuple(part)))
    links = [(lookup[(a, b)], lookup[(b, a)]) for a, b in edges]
    return edges, nodes, links


def solve(t, seconds):
    edges, nodes, links = template_graph(t)
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
                same = any(r == root and all((set(e) - {root}) <= set(part) for e in (edges[i], edges[j]))
                           for r, part in nodes)
                if not same:
                    model.add(R[i][j] == 0)
    for node in range(len(nodes)):
        inc = [i for i, ends in enumerate(links) if node in ends]
        for j in range(m):
            model.add(sum(R[i][j] for i in inc) == 0)
        if len(inc) >= 3:                                     # connectivity of the component's rectangle multigraph
            for size in range(1, len(inc)):
                for U in combinations(inc, size):
                    if inc[0] not in U:
                        continue
                    rest = [f for f in inc if f not in U]
                    model.add(sum(R[e][f] for e in U for f in rest) <= -2)
    model.add(sum(R[i][i] for i in range(m)) <= 28 * len(anchors))
    allowed = [(a, b, c) for a in (4, 6, 8) for b in (4, 6, 8) for c in range(-8, 5) if c * c <= a * b]
    for i, j in combinations(range(m), 2):
        model.add_allowed_assignments([R[i][i], R[j][j], R[i][j]], allowed)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 0
    cuts, t0 = 0, time.monotonic()
    while True:
        rem = seconds - (time.monotonic() - t0)
        if rem <= 0:
            return {"status": "UNKNOWN", "cuts": cuts}
        solver.parameters.max_time_in_seconds = rem
        st = solver.solve(model)
        if st == cp_model.INFEASIBLE:
            return {"status": "QUOTIENT_INFEASIBLE", "cuts": cuts}
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return {"status": "UNKNOWN", "cuts": cuts}
        cand = sp.Matrix([[solver.value(v) for v in row] for row in R])
        low = psd_or_witness(cand.extract(anchors, anchors))
        up = psd_or_witness(28 * sp.eye(m) - cand) if low["psd"] else None
        if low["psd"] and up["psd"]:
            assert incidence * cand == sp.zeros(len(nodes), m)
            return {"status": "QUOTIENT_FEASIBLE", "R": cand.tolist(), "R_rank": len(cand.rref()[1]), "cuts": cuts}
        if not low["psd"]:
            vec = [0] * m
            for i, x in zip(anchors, low["integer_witness"]):
                vec[i] = x
            model.add(sum(vec[i] * vec[j] * R[i][j] for i in range(m) for j in range(m) if vec[i] and vec[j]) >= 0)
        else:
            vec = up["integer_witness"]
            model.add(sum(vec[i] * vec[j] * R[i][j] for i in range(m) for j in range(m) if vec[i] and vec[j])
                      <= 28 * sum(x * x for x in vec))
        cuts += 1


if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    secs = float(sys.argv[2])
    start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    end = int(sys.argv[5]) if len(sys.argv) > 5 else len(data["survivors"])
    counts, recs, t0 = Counter(), [], time.time()
    for k in range(start, end):
        r = solve(data["survivors"][k], secs)
        counts[r["status"]] += 1
        recs.append({"index": k, "kernel_dimension": data["survivors"][k]["kernel_dimension"], **r})
    json.dump({"source": sys.argv[1], "c_min_at_root": data["c_min_at_root"], "grids_at_root": data["grids_at_root"],
               "range": [start, end], "counts": dict(counts), "records": recs}, open(sys.argv[3], "w"), default=int)
    print(json.dumps({"range": [start, end], "counts": dict(counts), "seconds": round(time.time() - t0, 1)}))
