"""Variable-Gram projector constraints for an entire component template.

H=T P on a fixed basis of rectangle columns. Impose H^tH=7R and
Gamma H=-4H, without choosing a Gram or a local binary seed.
"""

import argparse
from collections import Counter
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_propagation import LABELS, PAIRS, RECTANGLES, constraints, propagate
from root_component_obstruction_layers import pair_layer
from root_component_gram_table import add_gram_table


def add_projector(model, graph, template, anchors):
    edges = [tuple(e) for e in template["nongrid_edges"]]
    h, bounds = [], []
    label_rect = [tuple(a // 2 for a in p) for p in LABELS]
    for w in range(84):
        row, intervals = [], []
        for i, anchor in enumerate(anchors):
            f = edges[anchor]
            e = label_rect[w]
            base = 2 if e == f else (0 if set(e) & set(f) else 1)
            terms = [graph[w][v] for v in RECTANGLES[f]]
            forced = sum(x for x in terms if isinstance(x, int))
            unknown = sum(not isinstance(x, int) for x in terms)
            lo, hi = base - forced - unknown, base - forced
            if lo == hi:
                value = lo
            else:
                value = model.new_int_var(lo, hi, f"H_{w}_{i}")
                model.add(value + sum(terms) == base)
            row.append(value)
            intervals.append((lo, hi))
        h.append(row)
        bounds.append(intervals)
    moment_products = 0
    for i, j in combinations_with_replacement(range(len(anchors)), 2):
        terms = []
        for w in range(84):
            a, b = h[w][i], h[w][j]
            if isinstance(a, int):
                terms.append(a * b)
            elif isinstance(b, int):
                terms.append(b * a)
            else:
                products = [a0 * b0 for a0 in bounds[w][i] for b0 in bounds[w][j]]
                lo = 0 if i == j else min(products)
                hi = max(products)
                value = model.new_int_var(lo, hi, f"HH_{w}_{i}_{j}")
                model.add_multiplication_equality(value, [a, b])
                terms.append(value)
                moment_products += 1
        # R_ij is the sum of column j of H on the i-th anchor rectangle.
        model.add(sum(terms) == 7 * sum(h[w][j] for w in RECTANGLES[edges[anchors[i]]]))
    eigen_products = 0
    for u in range(84):
        for i in range(len(anchors)):
            terms = []
            for v in range(84):
                edge, value = graph[u][v], h[v][i]
                if isinstance(edge, int):
                    if edge:
                        terms.append(value)
                elif isinstance(value, int):
                    if value:
                        terms.append(value * edge)
                else:
                    lo, hi = bounds[v][i]
                    term = model.new_int_var(min(0, lo), max(0, hi), f"GH_{u}_{v}_{i}")
                    model.add(term == value).only_enforce_if(edge)
                    model.add(term == 0).only_enforce_if(edge.Not())
                    terms.append(term)
                    eigen_products += 1
            model.add(sum(terms) == -4 * h[u][i])
    return {"anchor_count": len(anchors), "moment_products": moment_products, "eigen_products": eigen_products,
            "identities": ["H=T P", "H^t H=7R", "Gamma H=-4H"]}


def build(template, cover, layer=2, projector=True, local_tables=None, normalize_component=False):
    prop = propagate(template)
    assert not prop["conflict"], prop["conflict"]
    fixed = {i: v for i, v, _ in prop["assignments"]}
    model = cp_model.CpModel()
    variables = [fixed[i] if i in fixed else model.new_bool_var(f"e{i}") for i in range(len(PAIRS))]
    graph = [[0] * 84 for _ in range(84)]
    for (u, v), value in zip(PAIRS, variables):
        graph[u][v] = graph[v][u] = value
    equations, upper_bounds, _ = constraints(template)
    for ids, target, _ in equations:
        model.add(sum(variables[i] for i in ids) == target)
    for ids, upper, _ in upper_bounds:
        model.add(sum(variables[i] for i in ids) <= upper)
    model.add(sum(graph[a][b] for corners in RECTANGLES.values() for a, b in combinations(corners, 2)
                  if set(LABELS[a]) & set(LABELS[b])) <= 51)
    gram_info = add_gram_table(model, graph, template, cover)
    projector_info = add_projector(model, graph, template, cover["anchors"]) if projector else None
    local_info = None
    if local_tables is not None:
        from root_component_local_tables import add_local_component_tables
        local_info = add_local_component_tables(model,graph,template,local_tables,normalize_component)
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
            model.add(p >= a+b-1)
            products[key] = p
        return products[key]
    c2_count = 0
    for u, v in PAIRS:
        if pair_layer(u, v) <= layer:
            model.add(graph[u][v] + sum(product(graph[u][z], graph[v][z]) for z in range(84))
                      == 2 - len(set(LABELS[u]) & set(LABELS[v])))
            c2_count += 1
    return model, graph, {"complete_gram_cover": gram_info, "projector": projector_info,
                          "C2_count": c2_count, "C2_products": len(products), "full_C2": layer == 4,
                          "local_component_tables": local_info}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--layer", type=int, choices=range(5), default=2)
    parser.add_argument("--seconds", type=float, default=300)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--grams", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--local-tables", type=Path)
    parser.add_argument("--normalize-component",action="store_true")
    parser.add_argument("--log-search",action="store_true")
    args = parser.parse_args()
    templates = json.loads((args.directory / "root_component_templates.json").read_text())["survivors"]
    source = args.grams or args.directory / "root_component_gram_orbits20.json"
    cover = next(r for r in json.loads(source.read_text())["records"] if r["template_index"] == args.index)
    started = time.monotonic()
    local_tables = None if args.local_tables is None else json.loads(args.local_tables.read_text())
    model, graph, info = build(templates[args.index], cover, args.layer, local_tables=local_tables,
                              normalize_component=args.normalize_component)
    assert not model.validate(), model.validate()
    info.update(template_index=args.index, status="MODEL_BUILT", build_seconds=time.monotonic()-started,
                variables=len(model.proto.variables), constraints=len(model.proto.constraints), source=str(source),
                scope="Whole template with variable Gram; no graph automorphism or fixed local seed.")
    args.output.write_text(json.dumps(info, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(info), flush=True)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.cp_model_probing_level = 0
    solver.parameters.symmetry_level = 0
    solver.parameters.linearization_level = 0
    solver.parameters.log_search_progress = args.log_search
    status = solver.solve(model)
    info.update(status=solver.status_name(status), solver_seconds=solver.wall_time,
                branches=solver.num_branches, conflicts=solver.num_conflicts)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        gamma = [[solver.value(x) for x in row] for row in graph]
        errors = Counter()
        for u,v in PAIRS:
            if gamma[u][v]+sum(gamma[u][z]*gamma[v][z] for z in range(84)) != 2-len(set(LABELS[u])&set(LABELS[v])):
                errors[pair_layer(u,v)] += 1
        info["violated_C2_by_layer"] = dict(errors)
        info["relaxation_edges"] = [[u,v] for u,v in PAIRS if gamma[u][v]]
    args.output.write_text(json.dumps(info, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in info.items() if k != "relaxation_edges"}), flush=True)


if __name__ == "__main__":
    main()
