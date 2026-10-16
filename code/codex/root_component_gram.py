"""Exact necessary integer Gram feasibility for the root component templates.

For each template R is the Gram matrix of four-label rectangle sums.
Its diagonal is in {2,4,6,8}, its columns annihilate the component incidence,
and 0<=R<=28I. All PSD cuts have integer negative-direction witnesses.
SAT here means a feasible small Gram quotient, never a Conway graph.
"""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
import time

import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_ambient_upper import psd_or_witness
from root_rectangle_domains import rectangle_realizations


def solve(template, seconds, realize_rectangles=False, root_prism_budget=None):
    edges = [tuple(e) for e in template["nongrid_edges"]]
    m = len(edges)
    if root_prism_budget is not None and 4*(21-m)>root_prism_budget:
        return {"status":"ROOT_GRID_BUDGET_EXCLUDED","grid_prism_lower_bound":4*(21-m),"cuts":[]}
    if not m:
        return {"status": "QUOTIENT_FEASIBLE", "R": [], "R_rank": 0, "cuts": []}
    nodes = template["component_graph_nodes"]
    links = template["component_graph_edges"]
    incidence = sp.zeros(len(nodes), m)
    for i, (a, b) in enumerate(links):
        incidence[a, i] = incidence[b, i] = 1
    kernel = sp.Matrix.hstack(*incidence.nullspace())
    anchors = list(kernel.T.rref()[1])
    assert len(anchors) == template["kernel_dimension"] <= 4
    model = cp_model.CpModel()
    matrix = [[None] * m for _ in range(m)]
    for i in range(m):
        matrix[i][i] = model.new_int_var_from_domain(cp_model.Domain.from_values([2, 4, 6, 8]), f"r_{i}_{i}")
        for j in range(i):
            common = set(edges[i]).intersection(edges[j])
            upper = 0 if common else 4
            matrix[i][j] = matrix[j][i] = model.new_int_var(-8, upper, f"r_{j}_{i}")
            if common:
                root = next(iter(common))
                same_component = any(root == r and all((set(e) - {root}).issubset(part)
                                                       for e in (edges[i], edges[j]))
                                     for r, part in nodes)
                if not same_component:
                    model.add(matrix[i][j] == 0)
    for node in range(len(nodes)):
        incident = [i for i, ends in enumerate(links) if node in ends]
        for j in range(m):
            model.add(sum(matrix[i][j] for i in incident) == 0)
    model.add(sum(matrix[i][i] for i in range(m)) <= 28 * len(anchors))
    if root_prism_budget is not None:
        degree_three_rectangles=[]
        for i in range(m):
            flag=model.new_bool_var(f"three_corner_edges_{i}")
            model.add(matrix[i][i]==2).only_enforce_if(flag)
            model.add(matrix[i][i]!=2).only_enforce_if(flag.Not())
            degree_three_rectangles.append(flag)
        model.add(4*(21-m)+3*sum(degree_three_rectangles)<=root_prism_budget)
    allowed = [(a, b, c) for a in (2, 4, 6, 8) for b in (2, 4, 6, 8)
               for c in range(-8, 5) if c*c <= a*b]
    for i, j in combinations(range(m), 2):
        model.add_allowed_assignments([matrix[i][i], matrix[j][j], matrix[i][j]], allowed)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 0
    cuts = []
    started = time.monotonic()
    while True:
        remaining = seconds - (time.monotonic() - started)
        if remaining <= 0:
            return {"status": "UNKNOWN", "cuts": cuts}
        solver.parameters.max_time_in_seconds = remaining
        status = solver.solve(model)
        if status == cp_model.INFEASIBLE:
            return {"status": "QUOTIENT_INFEASIBLE", "cuts": cuts,
                    "solver": "CP-SAT integer model plus recorded exact PSD cuts"}
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return {"status": "UNKNOWN", "cuts": cuts, "solver_status": solver.status_name(status)}
        candidate = sp.Matrix([[solver.value(v) for v in row] for row in matrix])
        small = candidate.extract(anchors, anchors)
        lower = psd_or_witness(small)
        upper = psd_or_witness(28 * sp.eye(m) - candidate) if lower["psd"] else None
        if lower["psd"] and upper["psd"]:
            assert incidence * candidate == sp.zeros(len(nodes), m)
            realization = rectangle_realizations(edges, candidate.tolist(),root_prism_budget=root_prism_budget) if realize_rectangles else None
            if realization and not realization["feasible"]:
                anchor_pairs = [(i,j) for i in anchors for j in anchors if i <= j]
                variables = [matrix[i][j] for i,j in anchor_pairs]
                values = [int(candidate[i,j]) for i,j in anchor_pairs]
                model.add_forbidden_assignments(variables, [values])
                cuts.append({"kind": "no_corner_realization", "failed_rectangle": realization["failed_rectangle"],
                             "R": candidate.tolist(), "anchor_values": values})
                continue
            return {"status": "QUOTIENT_FEASIBLE", "R": candidate.tolist(),
                    "R_rank": len(candidate.rref()[1]), "anchors": anchors,
                    "cuts": cuts, "seconds": time.monotonic() - started,
                    "corner_realizations": realization}
        if not lower["psd"]:
            vector = [0] * m
            for i, value in zip(anchors, lower["integer_witness"]):
                vector[i] = value
            rhs, kind, failure = 0, "R_psd", lower
        else:
            vector = upper["integer_witness"]
            rhs, kind, failure = 28 * sum(x*x for x in vector), "28I_minus_R_psd", upper
        expression = sum(vector[i] * vector[j] * matrix[i][j] for i in range(m) for j in range(m)
                         if vector[i] and vector[j])
        model.add(expression >= 0 if kind == "R_psd" else expression <= rhs)
        cuts.append({"kind": kind, "vector": vector, "rhs": rhs,
                     "rejected_quadratic_value": failure["quadratic_value"]})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds-per-template", type=float, default=3)
    parser.add_argument("--realize-rectangles", action="store_true")
    parser.add_argument("--root-prism-budget",type=int)
    parser.add_argument("--prior-grams",type=Path)
    args = parser.parse_args()
    data = json.loads(args.source.read_text(encoding="utf-8"))
    prior = None
    if args.prior_grams:
        prior={r["template_index"]:r for r in json.loads(args.prior_grams.read_text(encoding="utf-8"))["records"]}
        assert all(r["status"] in ("QUOTIENT_FEASIBLE","QUOTIENT_INFEASIBLE") for r in prior.values())
    if args.root_prism_budget is not None:
        assert args.realize_rectangles
    counts, output = Counter(), []
    started = time.monotonic()
    for i, item in enumerate(data["survivors"]):
        if prior is not None and prior[i]["status"]=="QUOTIENT_INFEASIBLE":
            continue
        result = solve(item, args.seconds_per_template, args.realize_rectangles,args.root_prism_budget)
        counts[result["status"]] += 1
        output.append({"template_index": i, "graph_mask": item["graph_mask"],
                       "root_prism_budget":args.root_prism_budget, **result})
        if i % 25 == 0 or result["status"] == "UNKNOWN":
            print(json.dumps({"completed": i+1, "counts": dict(counts)}), flush=True)
    result = {"source": str(args.source),
              "scope": "Finite necessary Gram quotients only, not completed 44- or 99-vertex graphs.",
              "includes_corner_realization": args.realize_rectangles,
              "root_prism_budget":args.root_prism_budget,
              "prior_grams":str(args.prior_grams) if args.prior_grams else None,
              "counts": dict(counts), "elapsed_seconds": time.monotonic()-started,
              "records": output}
    args.output.write_text(json.dumps(result, indent=2, default=int)+"\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k != "records"}), flush=True)


if __name__ == "__main__":
    main()
