"""Joint binary realization of a fixed Gram from a complete finite cover.

Necessary constraints beyond separate signatures: exact H^t H=7R, B H=0,
all row-to-rectangle counts H=T P, and all two-vertex conditional PSD tests.
Optional C2 layers remain relaxations unless the entire C2 system is used.
Each fixed Gram is a branch, never a stand-alone exclusion of its template.
"""

import argparse
from collections import Counter
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_propagation import LABELS, PAIRS, RECTANGLES, constraints, propagate
from root_component_signature_moments import gram_matrix
from root_rectangle_domains import signature_domains
from root_component_obstruction_layers import pair_layer


def build(template, matrix, layer=0, pair_psd=True):
    edges = [tuple(e) for e in template["nongrid_edges"]]
    raw = [[int(x) for x in row] for row in matrix.tolist()]
    domains = {tuple(r["rectangle"]): r for r in signature_domains(edges, raw)}
    anchors = list(matrix.rref()[1])
    small = matrix.extract(anchors, anchors)
    det = int(small.det())
    adj = [[int(x) for x in row] for row in (small.inv() * det).tolist()]
    propagation = propagate(template)
    if propagation["conflict"]:
        raise ValueError(propagation["conflict"])
    fixed = {i: v for i, v, _ in propagation["assignments"]}
    model = cp_model.CpModel()
    variables = [fixed[i] if i in fixed else model.new_bool_var(f"e{i}") for i in range(len(PAIRS))]
    graph = [[0] * 84 for _ in range(84)]
    for (a, b), value in zip(PAIRS, variables):
        graph[a][b] = graph[b][a] = value
    equations, bounds, _ = constraints(template)
    for ids, target, _ in equations:
        model.add(sum(variables[i] for i in ids) == target)
    for ids, upper, _ in bounds:
        model.add(sum(variables[i] for i in ids) <= upper)
    model.add(sum(graph[a][b] for corners in RECTANGLES.values() for a, b in combinations(corners, 2)
                  if set(LABELS[a]) & set(LABELS[b])) <= 51)
    selectors, indicators, hs, hfull = [None] * 84, [None] * 84, [None] * 84, [None] * 84
    for rectangle, corners in RECTANGLES.items():
        signatures = domains[rectangle]["signatures"]
        reduced = [tuple(h[i] for i in anchors) for h in signatures]
        if not signatures:
            model.add(False)
            return model, graph, {"empty_domain": list(rectangle)}
        for w in corners:
            hs[w], hfull[w] = reduced, signatures
            selectors[w] = model.new_int_var(0, len(signatures) - 1, f"signature_{w}")
            if len(signatures) == 1:
                flags = [1]
            else:
                flags = [model.new_bool_var(f"signature_{w}_{i}") for i in range(len(signatures))]
                model.add_exactly_one(flags)
                model.add_map_domain(selectors[w], flags)
            indicators[w] = flags
            for ci, coordinate in enumerate(edges):
                base = 2 if rectangle == coordinate else (0 if set(rectangle) & set(coordinate) else 1)
                model.add(sum(graph[w][q] for q in RECTANGLES[coordinate]) +
                          sum(flag * h[ci] for flag, h in zip(flags, signatures)) == base)
    for i, j in combinations_with_replacement(range(len(anchors)), 2):
        model.add(sum(flag * h[i] * h[j] for w in range(84) for flag, h in zip(indicators[w], hs[w]))
                  == 7 * int(matrix[anchors[i], anchors[j]]))
    for letter in range(14):
        for i in range(len(anchors)):
            model.add(sum(flag * h[i] for w in range(84) if letter in LABELS[w]
                          for flag, h in zip(indicators[w], hs[w])) == 0)
    pair_tables, pair_rows = 0, 0
    if pair_psd:
        def inner(a, b):
            return sum(a[i] * adj[i][j] * b[j] for i in range(len(anchors)) for j in range(len(anchors)))
        norms = [[20 * det - 8 * inner(h, h) for h in hs[w]] for w in range(84)]
        for u, v in PAIRS:
            common = len(set(LABELS[u]) & set(LABELS[v]))
            mate_common = sum((a ^ 1) in LABELS[v] for a in LABELS[u])
            base8 = 2 - 3 * common - mate_common
            edge = graph[u][v]
            possible_edges = [edge] if isinstance(edge, int) else [0, 1]
            allowed = []
            for a, hu in enumerate(hs[u]):
                for b, hv in enumerate(hs[v]):
                    ip = inner(hu, hv)
                    for e in possible_edges:
                        off = (base8 - 8 * e) * det - 8 * ip
                        if off * off <= norms[u][a] * norms[v][b]:
                            allowed.append([a, b] if isinstance(edge, int) else [a, b, e])
            if len(allowed) < len(hs[u]) * len(hs[v]) * len(possible_edges):
                columns = [selectors[u], selectors[v]] + ([] if isinstance(edge, int) else [edge])
                model.add_allowed_assignments(columns, allowed)
                pair_tables += 1
                pair_rows += len(allowed)
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
    for u, v in PAIRS:
        if pair_layer(u, v) <= layer:
            model.add(graph[u][v] + sum(product(graph[u][z], graph[v][z]) for z in range(84))
                      == 2 - len(set(LABELS[u]) & set(LABELS[v])))
            c2_count += 1
    info = {"pair_psd_tables": pair_tables, "pair_psd_rows": pair_rows, "c2_equations": c2_count,
            "moment_equations": len(anchors) * (len(anchors) + 1) // 2,
            "signature_flags": sum(len(x) for x in indicators), "full_C2": layer == 4}
    return model, graph, info


def solve(template, matrix, seconds, layer=0, workers=1):
    started = time.monotonic()
    model, graph, info = build(template, matrix, layer)
    assert not model.validate(), model.validate()
    info.update(build_seconds=time.monotonic() - started, variables=len(model.proto.variables), constraints=len(model.proto.constraints))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.cp_model_probing_level = 0
    solver.parameters.symmetry_level = 0
    solver.parameters.linearization_level = 0
    status = solver.solve(model)
    info.update(status=solver.status_name(status), solver_seconds=solver.wall_time,
                branches=solver.num_branches, conflicts=solver.num_conflicts)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        gamma = [[solver.value(x) for x in row] for row in graph]
        errors = Counter()
        for u, v in PAIRS:
            actual = gamma[u][v] + sum(gamma[u][z] * gamma[v][z] for z in range(84))
            if actual != 2 - len(set(LABELS[u]) & set(LABELS[v])):
                errors[pair_layer(u, v)] += 1
        info["violated_C2_by_layer"] = dict(errors)
        info["relaxation_edges"] = [[u, v] for u, v in PAIRS if gamma[u][v]]
    return info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--indices", type=int, nargs="+", required=True)
    parser.add_argument("--seconds", type=float, default=5)
    parser.add_argument("--layer", type=int, choices=range(5), default=0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--moments", type=Path)
    parser.add_argument("--prior", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    covers = {r["template_index"]: r for r in json.loads((args.directory / "root_component_gram_orbits20.json").read_text())["records"]}
    templates = json.loads((args.directory / "root_component_templates.json").read_text())["survivors"]
    earlier = {}
    if args.moments:
        earlier = {(r["template_index"], c["gram_index"]): c for r in json.loads(args.moments.read_text())["records"] for c in r["cases"]}
    if args.prior:
        for r in json.loads(args.prior.read_text())["records"]:
            for c in r["cases"]:
                if c["status"] == "INFEASIBLE":
                    earlier[r["template_index"], c["gram_index"]] = dict(c, inherited_source=str(args.prior))
    records = []
    for index in args.indices:
        cover = covers[index]
        assert cover["exhaustive"] and cover["usable_as_gram_cover"]
        cases = []
        record = {"template_index": index, "complete_source_gram_count": cover["gram_count"], "cases": cases}
        records.append(record)
        for gi, values in enumerate(cover["gram_anchor_values"]):
            prev = earlier.get((index, gi), {})
            if prev.get("status") == "INFEASIBLE":
                assert prev["gram_anchor_values"] == values
                result = {"status": "INFEASIBLE", "source": prev.get("inherited_source", str(args.moments))}
            else:
                result = solve(templates[index], gram_matrix(cover, values), args.seconds, args.layer, args.workers)
            result.update(gram_index=gi, gram_anchor_values=values)
            cases.append(result)
            print(json.dumps({"template": index, **{k: v for k, v in result.items() if k != "relaxation_edges"}}), flush=True)
            record.update(counts=dict(Counter(r["status"] for r in cases)),
                          all_source_grams_processed=len(cases) == cover["gram_count"],
                          excluded=len(cases) == cover["gram_count"] and all(r["status"] == "INFEASIBLE" for r in cases))
            args.output.write_text(json.dumps({"scope": __doc__, "layer": args.layer, "records": records}, separators=(",", ":")) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in record.items() if k != "cases"}), flush=True)


if __name__ == "__main__":
    main()
