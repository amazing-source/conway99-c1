"""Locate obstructions by imposing only selected common-neighbour equations.

This is a relaxation, never a construction of a Conway graph unless all C2
equations are checked. No Gram witness or Gram cuts are imposed. Components
and C1 are imposed exactly; C2 is added in nested geometrically defined layers.
"""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_propagation import LABELS, PAIRS, RECTANGLES, constraints, propagate
from root_component_c2_layers import label_pair_layer


def pair_layer(a, b):
    return label_pair_layer(LABELS[a], LABELS[b])


def solve(template, layer, seconds, minimize_prisms=False, gram_cover=None):
    propagation = propagate(template, use_c2=False)
    if propagation["status"] == "PROPAGATION_CONTRADICTION":
        return {"status": propagation["status"], "conflict": propagation["conflict"]}
    fixed = {i: v for i, v, _ in propagation["assignments"]}
    model = cp_model.CpModel()
    edges = [fixed[i] if i in fixed else model.new_bool_var(f"e{i}") for i in range(len(PAIRS))]
    graph = [[0] * 84 for _ in range(84)]
    for (a, b), value in zip(PAIRS, edges):
        graph[a][b] = graph[b][a] = value
    equations, bounds, _ = constraints(template)
    for indices, target, _ in equations:
        model.add(sum(edges[i] for i in indices) == target)
    for indices, upper, _ in bounds:
        model.add(sum(edges[i] for i in indices) <= upper)
    prism_sum = sum(graph[a][b] for corners in RECTANGLES.values()
                    for a, b in combinations(corners, 2) if set(LABELS[a]) & set(LABELS[b]))
    if minimize_prisms:
        model.minimize(prism_sum)
    else:
        model.add(prism_sum <= 51)
    gram_info = None
    if gram_cover is not None:
        assert not minimize_prisms, "This Gram cover used the root budget51."
        from root_component_gram_table import add_gram_table
        gram_info = add_gram_table(model, graph, template, gram_cover)
    products = {}

    def product(a, b):
        if isinstance(a, int):
            return b if a else 0
        if isinstance(b, int):
            return a if b else 0
        key = tuple(sorted((a.index, b.index)))
        if key not in products:
            p = model.new_bool_var(f"p{len(products)}")
            model.add(p <= a)
            model.add(p <= b)
            model.add(p >= a + b - 1)
            products[key] = p
        return products[key]

    c2_count = 0
    for a, b in PAIRS:
        if pair_layer(a, b) <= layer:
            model.add(graph[a][b] + sum(product(graph[a][z], graph[b][z]) for z in range(84))
                      == 2 - len(set(LABELS[a]) & set(LABELS[b])))
            c2_count += 1
    assert not model.validate(), model.validate()
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.cp_model_probing_level = 0
    solver.parameters.symmetry_level = 0
    solver.parameters.linearization_level = 0
    status = solver.solve(model)
    result = {"status": solver.status_name(status), "solver_seconds": solver.wall_time,
              "branches": solver.num_branches, "conflicts": solver.num_conflicts,
              "c2_equations": c2_count, "product_variables": len(products),
              "complete_gram_cover": gram_info,
              "is_full_conway_model": layer == 4}
    if minimize_prisms:
        result["prism_lower_bound"] = solver.best_objective_bound
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result["root_prism_sum"] = solver.value(prism_sum)
        gamma = [[solver.value(x) for x in row] for row in graph]
        errors = Counter()
        for a, b in PAIRS:
            value = gamma[a][b] + sum(gamma[a][z] * gamma[b][z] for z in range(84))
            if value != 2 - len(set(LABELS[a]) & set(LABELS[b])):
                errors[pair_layer(a, b)] += 1
        result["violated_C2_by_layer"] = dict(sorted(errors.items()))
        result["all_C2_satisfied"] = not errors
        result["relaxation_edges"] = [[a, b] for a, b in PAIRS if gamma[a][b]]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--layer", choices=range(5), type=int, default=0)
    parser.add_argument("--seconds", type=float, default=2)
    parser.add_argument("--indices", type=int, nargs="*")
    parser.add_argument("--minimize-prisms", action="store_true")
    parser.add_argument("--gram-cover", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    templates = json.loads((args.directory / "root_component_templates.json").read_text(encoding="utf-8"))["survivors"]
    cover = json.loads((args.directory / "root_component_cover79.json").read_text(encoding="utf-8"))
    indices = args.indices if args.indices is not None else [r["template_index"] for r in cover["templates"]]
    gram_covers = None if args.gram_cover is None else {r["template_index"]: r for r in json.loads(args.gram_cover.read_text(encoding="utf-8"))["records"]}
    records = []
    for index in indices:
        result = {"template_index": index, **solve(templates[index], args.layer, args.seconds, args.minimize_prisms,
                    None if gram_covers is None else gram_covers[index])}
        records.append(result)
        summary = {"scope": "Necessary component/C1 relaxation; only the selected C2 layer is imposed.",
                   "layer": args.layer, "layer_meaning": ["no_C2", "same_rectangle", "same_rectangle_or_letter", "shared_root_line", "all_pairs"][args.layer],
                   "root_prism_budget": None if args.minimize_prisms else 51,
                   "minimizes_root_prisms": args.minimize_prisms, "no_Gram_cuts": gram_covers is None,
                   "complete_gram_cover_source": str(args.gram_cover) if args.gram_cover else None,
                   "counts": dict(Counter(r["status"] for r in records)), "records": records}
        args.output.write_text(json.dumps(summary, separators=(",", ":")) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in result.items() if k != "relaxation_edges"}), flush=True)
    print(json.dumps({"counts": summary["counts"]}), flush=True)


if __name__ == "__main__":
    main()
