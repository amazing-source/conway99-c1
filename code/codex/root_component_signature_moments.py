"""Necessary integral moments of all vertex signatures in a rectangle Gram.

For a Conway completion, T^2=7T and H=T P for the rectangle incidence P.
Thus H^t H=7R, in addition to the four-row sums P^t H=R. The variables
here count four signatures per rectangle. They are a relaxation: no
adjacency completion or ordering of the four corners is assumed.
"""

import argparse
from collections import Counter
from itertools import combinations_with_replacement
import json
from pathlib import Path
import sys
import time

import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_rectangle_domains import signature_domains


def gram_matrix(record, values):
    lift = sp.Matrix([[sp.Rational(*x) for x in row] for row in record["lift_matrix"]])
    small = sp.zeros(lift.cols)
    for (i, j), value in zip(record["anchor_pairs"], values):
        small[i, j] = small[j, i] = value
    matrix = lift * small * lift.T
    assert all(x.q == 1 for x in matrix)
    return matrix


def solve_moments(edges, matrix, seconds=2):
    started = time.monotonic()
    raw = [[int(x) for x in row] for row in matrix.tolist()]
    domains = signature_domains(edges, raw)
    anchors = list(matrix.rref()[1])
    model = cp_model.CpModel()
    variables, signatures = [], []
    for ri, item in enumerate(domains):
        hs = [tuple(h[i] for i in anchors) for h in item["signatures"]]
        counts = [model.new_int_var(0, 4, f"n_{ri}_{j}") for j in range(len(hs))]
        model.add(sum(counts) == 4)
        for ai, a in enumerate(anchors):
            model.add(sum(v * h[ai] for v, h in zip(counts, hs)) == item["target"][a])
        variables.append(counts)
        signatures.append(hs)
    for i, j in combinations_with_replacement(range(len(anchors)), 2):
        model.add(sum(v * h[i] * h[j] for counts, hs in zip(variables, signatures)
                      for v, h in zip(counts, hs)) == 7 * int(matrix[anchors[i], anchors[j]]))
    assert not model.validate(), model.validate()
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = seconds
    status = solver.solve(model)
    result = {"status": solver.status_name(status), "seconds": time.monotonic() - started,
              "solver_seconds": solver.wall_time, "variables": len(model.proto.variables),
              "branches": solver.num_branches, "conflicts": solver.num_conflicts}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result["signature_multisets"] = [
            {"rectangle": item["rectangle"], "signatures": [list(h) for v, h in zip(counts, hs)
                                                            for _ in range(solver.value(v))]}
            for item, counts, hs in zip(domains, variables, signatures)]
        # Check the newly derived necessary equations exactly on its witness.
        for i, j in combinations_with_replacement(range(len(anchors)), 2):
            assert sum(h[i] * h[j] for r in result["signature_multisets"] for h in r["signatures"]) == 7 * matrix[anchors[i], anchors[j]]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--grams", type=Path)
    parser.add_argument("--indices", type=int, nargs="+", required=True)
    parser.add_argument("--seconds", type=float, default=2)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.grams or args.directory / "root_component_gram_orbits20.json"
    covers = {r["template_index"]: r for r in json.loads(source.read_text(encoding="utf-8"))["records"]}
    templates = json.loads((args.directory / "root_component_templates.json").read_text(encoding="utf-8"))["survivors"]
    records = []
    for index in args.indices:
        cover = covers[index]
        assert cover["exhaustive"] and cover["usable_as_gram_cover"]
        edges = [tuple(e) for e in templates[index]["nongrid_edges"]]
        cases = []
        for gi, values in enumerate(cover["gram_anchor_values"]):
            result = solve_moments(edges, gram_matrix(cover, values), args.seconds)
            result.update(gram_index=gi, gram_anchor_values=values)
            cases.append(result)
            if (gi + 1) % 100 == 0:
                print(json.dumps({"template": index, "done": gi + 1, "counts": dict(Counter(r["status"] for r in cases))}), flush=True)
        record = {"template_index": index, "complete_source_gram_count": cover["gram_count"],
                  "counts": dict(Counter(r["status"] for r in cases)), "cases": cases,
                  "excluded": all(r["status"] == "INFEASIBLE" for r in cases)}
        records.append(record)
        args.output.write_text(json.dumps({"source": str(source),
            "scope": "Necessary four-signature sums and exact H^t H=7R; feasible is not a graph.",
            "records": records}, separators=(",", ":")) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in record.items() if k != "cases"}), flush=True)


if __name__ == "__main__":
    main()
