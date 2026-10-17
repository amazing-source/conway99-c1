"""Enumerate every integer rectangle Gram in one component template.

The CP model is a necessary superset. Every solution is tested exactly for
0<=R<=28I on at most four anchor coordinates. A time limit gives a PARTIAL
list; only exhaustive lists may be used as a cover of possible Grams.
"""

import argparse
from collections import Counter
from functools import reduce
from itertools import combinations
import json
from math import gcd, lcm
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_rectangle_domains import rectangle_realizations


def integer_psd(matrix):
    """Exact Schur elimination, including singular pivots; order at most4."""
    a = matrix
    while a:
        pivot = a[0][0]
        if pivot < 0 or (pivot == 0 and any(a[0][1:])):
            return False
        if pivot == 0:
            a = [row[1:] for row in a[1:]]
        else:
            a = [[pivot * a[i][j] - a[i][0] * a[0][j]
                  for j in range(1, len(a))] for i in range(1, len(a))]
            divisor = reduce(gcd, (abs(x) for row in a for x in row), 0)
            if divisor > 1:
                a = [[x // divisor for x in row] for row in a]
    return True


def enumerate_grams(template, seconds, realize):
    edges = [tuple(e) for e in template["nongrid_edges"]]
    nodes = template["component_graph_nodes"]
    links = template["component_graph_edges"]
    m = len(edges)
    incidence = sp.zeros(len(nodes), m)
    for i, (a, b) in enumerate(links):
        incidence[a, i] = incidence[b, i] = 1
    kernel = sp.Matrix.hstack(*incidence.nullspace())
    anchors = list(kernel.T.rref()[1])
    d = len(anchors)
    lift = kernel * kernel.extract(anchors, range(d)).inv()
    assert lift.extract(anchors, range(d)) == sp.eye(d)
    upper = 28 * (lift.T * lift).inv()
    upper_scale = lcm(*(int(x.q) for x in upper))
    upper_base = [[int(upper_scale * upper[i, j]) for j in range(d)] for i in range(d)]
    model = cp_model.CpModel()
    r = [[None] * m for _ in range(m)]
    for i in range(m):
        r[i][i] = model.new_int_var_from_domain(cp_model.Domain.from_values([2, 4, 6, 8]), f"r{i}_{i}")
        for j in range(i):
            common = set(edges[i]) & set(edges[j])
            r[i][j] = r[j][i] = model.new_int_var(-8, 0 if common else 4, f"r{j}_{i}")
            if common:
                root = next(iter(common))
                same = any(root == node_root and all((set(e) - {root}).issubset(part)
                           for e in (edges[i], edges[j])) for node_root, part in nodes)
                if not same:
                    model.add(r[i][j] == 0)
    for node in range(len(nodes)):
        indices = [i for i, ends in enumerate(links) if node in ends]
        for j in range(m):
            model.add(sum(r[i][j] for i in indices) == 0)
    model.add(sum(r[i][i] for i in range(m)) <= 28 * d)
    flags = []
    for i in range(m):
        flag = model.new_bool_var(f"three_edges{i}")
        model.add(r[i][i] == 2).only_enforce_if(flag)
        model.add(r[i][i] != 2).only_enforce_if(flag.Not())
        flags.append(flag)
    model.add(4 * (21 - m) + 3 * sum(flags) <= 51)
    allowed = [(a, b, c) for a in (2, 4, 6, 8) for b in (2, 4, 6, 8)
               for c in range(-8, 5) if c * c <= a * b]
    for i, j in combinations(range(m), 2):
        model.add_allowed_assignments([r[i][i], r[j][j], r[i][j]], allowed)
    assert not model.validate(), model.validate()
    anchor_pairs = [(i, j) for i in range(d) for j in range(i, d)]

    class Collector(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
            self.counts = Counter()
            self.grams = []

        def on_solution_callback(self):
            self.counts["integer_candidates"] += 1
            small = [[self.value(r[i][j]) for j in anchors] for i in anchors]
            if not integer_psd(small):
                self.counts["not_psd"] += 1
                return
            complement = [[upper_base[i][j] - upper_scale * small[i][j] for j in range(d)] for i in range(d)]
            if not integer_psd(complement):
                self.counts["exceeds_28I"] += 1
                return
            self.counts["psd_grams"] += 1
            if realize:
                matrix = [[self.value(x) for x in row] for row in r]
                corners = rectangle_realizations(edges, matrix, root_prism_budget=51)
                if not corners["feasible"]:
                    self.counts["no_separate_corner_realization"] += 1
                    return
            self.grams.append([small[i][j] for i, j in anchor_pairs])

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.enumerate_all_solutions = True
    collector = Collector()
    started = time.monotonic()
    status = solver.solve(model, collector)
    assert len({tuple(values) for values in collector.grams}) == len(collector.grams)
    exhaustive = status in (cp_model.OPTIMAL, cp_model.INFEASIBLE)
    return {"status": solver.status_name(status), "exhaustive": exhaustive,
            "usable_as_gram_cover": exhaustive, "root_prism_budget": 51,
            "requires_separate_corner_realization": realize,
            "seconds": time.monotonic() - started, "counts": dict(collector.counts),
            "gram_count": len(collector.grams), "anchors": anchors,
            "anchor_pairs": anchor_pairs,
            "lift_matrix": [[[int(x.p), int(x.q)] for x in lift.row(i)] for i in range(m)],
            "upper_test_scale": upper_scale, "upper_test_base": upper_base,
            "gram_anchor_values": collector.grams}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--indices", type=int, nargs="+", required=True)
    parser.add_argument("--seconds", type=float, default=10)
    parser.add_argument("--realize-rectangles", action="store_true")
    parser.add_argument("--prior", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    templates = json.loads((args.directory / "root_component_templates.json").read_text(encoding="utf-8"))["survivors"]
    prior = {} if args.prior is None else {r["template_index"]: r for r in json.loads(args.prior.read_text(encoding="utf-8"))["records"]}
    records = []
    for index in args.indices:
        if index in prior and prior[index]["exhaustive"] and prior[index]["requires_separate_corner_realization"] == args.realize_rectangles:
            result = prior[index]
        else:
            result = {"template_index": index, **enumerate_grams(templates[index], args.seconds, args.realize_rectangles)}
        records.append(result)
        args.output.write_text(json.dumps({"scope": "Finite necessary Gram covers; no full graph completion.",
                                          "records": records}, separators=(",", ":")) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in result.items() if k not in (
            "gram_anchor_values", "lift_matrix", "upper_test_base", "anchor_pairs")}), flush=True)


if __name__ == "__main__":
    main()
