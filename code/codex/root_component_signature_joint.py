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
import threading

from ortools.sat.python import cp_model
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_propagation import LABELS, PAIRS, RECTANGLES, constraints, propagate
from root_component_signature_moments import gram_matrix
from root_rectangle_domains import signature_domains
from root_component_obstruction_layers import pair_layer


def build(template, matrix, layer=0, pair_psd=True, eigen=False, mate_normalize=False, four_corners=False, local_tables=None, minc_lines=0, six_prism_profiles=False, line_profiles=0, profile_triples=False, triangle_cuts=False, exact_triangles=False, short_vectors=False):
    edges = [tuple(e) for e in template["nongrid_edges"]]
    raw = [[int(x) for x in row] for row in matrix.tolist()]
    domains = {tuple(r["rectangle"]): r for r in signature_domains(edges, raw)}
    short_data, short_info = None, None
    if short_vectors:
        from root_component_short_vectors import short_directions, filter_domains, evaluations
        short_data = short_directions(matrix)
        short_info = filter_domains(domains, short_data)
    anchors = list(matrix.rref()[1])
    small = matrix.extract(anchors, anchors)
    det = int(small.det())
    adj = [[int(x) for x in row] for row in (small.inv() * det).tolist()]
    corner_tables = None
    if four_corners:
        from root_component_corner_tables import enumerate_corner_rows
        corner_tables = enumerate_corner_rows(edges, matrix, domains, anchors, det, adj)
        for table in corner_tables:
            item = domains[table["rectangle"]]
            if short_data is not None:
                from root_rectangle_domains import RECTANGLE_LABELS
                values = [evaluations(h, short_data, roots_only=True) for h in item["signatures"]]
                table["rows"] = [row for row in table["rows"] if all(
                    not (edge or set(RECTANGLE_LABELS[i]) & set(RECTANGLE_LABELS[j])) or
                    not any(a == b != 0 for a, b in zip(values[row[i]], values[row[j]]))
                    for edge, (i, j) in zip(row[4:], combinations(range(4), 2)))]
            used = sorted({i for row in table["rows"] for i in row[:4]})
            remap = {old: new for new, old in enumerate(used)}
            item["signatures"] = [item["signatures"][i] for i in used]
            table["rows"] = [[remap[i] for i in row[:4]] + row[4:] for row in table["rows"]]
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
    triangle_info=None
    if triangle_cuts:
        # An adjacent pair sharing a label already has its unique common
        # neighbour in N(o); it cannot belong to a triangle in Gamma.
        seen=set()
        histogram=Counter()
        for u,v,w in combinations(range(84),3):
            if len(set(LABELS[u]+LABELS[v]+LABELS[w]))==6:
                continue
            edges3=[graph[u][v],graph[u][w],graph[v][w]]
            if any(isinstance(e,int) and e==0 for e in edges3):
                continue
            unknown=[e for e in edges3 if not isinstance(e,int)]
            key=tuple(sorted(e.index for e in unknown))
            if key not in seen:
                model.add_bool_or([e.Not() for e in unknown])
                histogram[len(key)]+=1
                seen.add(key)
        triangle_info=dict(histogram)
    local_info = None
    model.add(sum(graph[a][b] for corners in RECTANGLES.values() for a, b in combinations(corners, 2)
                  if set(LABELS[a]) & set(LABELS[b])) <= 51)
    selectors, indicators, hs, hfull = [None] * 84, [None] * 84, [None] * 84, [None] * 84
    for rectangle, corners in RECTANGLES.items():
        signatures = domains[rectangle]["signatures"]
        reduced = [tuple(h[i] for i in anchors) for h in signatures]
        if not signatures:
            model.add(False)
            return model, graph, {"empty_domain": list(rectangle), "short_vector_filter": short_info}
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
    for rectangle,vertices in RECTANGLES.items():
        target=domains[rectangle]["target"]
        for ci,anchor in enumerate(anchors):
            model.add(sum(flag*h[ci] for w in vertices for flag,h in zip(indicators[w],hs[w]))==target[anchor])
    corner_info=None
    if four_corners:
        for table in corner_tables:
            vertices = RECTANGLES[table["rectangle"]]
            model.add_allowed_assignments([selectors[w] for w in vertices] +
                                          [graph[u][v] for u,v in combinations(vertices,2)], table["rows"])
        corner_info = {"tables": len(corner_tables), "rows": sum(len(t["rows"]) for t in corner_tables),
                       "test": "Exact four-corner conditional PSD and four-signature sums.",
                       "domain_support_pruned": True}
    if local_tables is not None:
        from root_component_local_tables import add_local_component_tables
        corner_patterns = None if corner_tables is None else {
            t["rectangle"]: {sum(bit << i for i,bit in enumerate(row[4:])) for row in t["rows"]}
            for t in corner_tables}
        signature_data = None if corner_tables is None else (edges,domains,corner_tables,selectors)
        local_info = add_local_component_tables(model, graph, template, local_tables,
                                                corner_patterns=corner_patterns,signature_data=signature_data)
    for i, j in combinations_with_replacement(range(len(anchors)), 2):
        model.add(sum(flag * h[i] * h[j] for w in range(84) for flag, h in zip(indicators[w], hs[w]))
                  == 7 * int(matrix[anchors[i], anchors[j]]))
    if mate_normalize:
        label_index = {p: i for i, p in enumerate(LABELS)}
        for root in range(7):
            permutation = [label_index[tuple(sorted(a ^ int(a // 2 == root) for a in p))] for p in LABELS]
            prefix = 1
            for u, v in enumerate(permutation):
                if u >= v:
                    continue
                model.add(selectors[u] <= selectors[v]).only_enforce_if(prefix)
                equal = model.new_bool_var(f"mate_eq_{root}_{u}")
                model.add(selectors[u] == selectors[v]).only_enforce_if(equal)
                model.add(selectors[u] != selectors[v]).only_enforce_if(equal.Not())
                if isinstance(prefix, int):
                    prefix = equal
                else:
                    both = model.new_bool_var(f"mate_prefix_{root}_{u}")
                    model.add(both <= prefix)
                    model.add(both <= equal)
                    model.add(both >= prefix + equal - 1)
                    prefix = both
    for letter in range(14):
        for i in range(len(anchors)):
            model.add(sum(flag * h[i] for w in range(84) if letter in LABELS[w]
                          for flag, h in zip(indicators[w], hs[w])) == 0)
    eigen_products = 0
    if eigen:
        coordinates = []
        intervals = []
        for w in range(84):
            row, row_bounds = [], []
            for i in range(len(anchors)):
                lo, hi = min(h[i] for h in hs[w]), max(h[i] for h in hs[w])
                if lo == hi:
                    row.append(lo)
                else:
                    v = model.new_int_var(lo, hi, f"h_{w}_{i}")
                    model.add(v == sum(flag * h[i] for flag, h in zip(indicators[w], hs[w])))
                    row.append(v)
                row_bounds.append((lo, hi))
            coordinates.append(row)
            intervals.append(row_bounds)
        for u in range(84):
            for i in range(len(anchors)):
                terms = []
                for v in range(84):
                    edge, h = graph[u][v], coordinates[v][i]
                    if isinstance(edge, int):
                        if edge:
                            terms.append(h)
                    elif isinstance(h, int):
                        if h:
                            terms.append(h * edge)
                    else:
                        lo, hi = intervals[v][i]
                        term = model.new_int_var(min(lo, 0), max(hi, 0), f"eh_{u}_{v}_{i}")
                        model.add(term == h).only_enforce_if(edge)
                        model.add(term == 0).only_enforce_if(edge.Not())
                        terms.append(term)
                        eigen_products += 1
                model.add(sum(terms) == -4 * coordinates[u][i])
    pair_tables, pair_rows = 0, 0
    short_masks = None
    if short_data is not None:
        short_masks = [[(
            sum(1 << i for i, x in enumerate(values) if x == 1),
            sum(1 << i for i, x in enumerate(values) if x == -1))
            for values in [evaluations(h, short_data, roots_only=True) for h in hfull[w]]]
            for w in range(84)]
        root_count = sum(d['norm'] == 2 for d in short_data['directions'])
        for root_id in range(root_count):
            for letter in range(14):
                for sign in (0, 1):
                    model.add(sum(flag for w in range(84) if letter in LABELS[w]
                                  for flag, mask in zip(indicators[w], short_masks[w])
                                  if mask[sign] & (1 << root_id)) == 1)
        short_info['root_label_matching_equations'] = 28 * root_count
    if pair_psd or short_data is not None:
        def inner(a, b):
            return sum(a[i] * adj[i][j] * b[j] for i in range(len(anchors)) for j in range(len(anchors)))
        norms = [[20 * det - 8 * inner(h, h) for h in hs[w]] for w in range(84)]
        pair_cache = {}
        for u, v in PAIRS:
            common = len(set(LABELS[u]) & set(LABELS[v]))
            mate_common = sum((a ^ 1) in LABELS[v] for a in LABELS[u])
            base8 = 2 - 3 * common - mate_common
            edge = graph[u][v]
            possible_edges = [edge] if isinstance(edge, int) else [0, 1]
            cache_key = (id(hs[u]), id(hs[v]), base8, tuple(possible_edges))
            allowed = pair_cache.get(cache_key)
            if allowed is None:
                allowed = []
                for a, hu in enumerate(hs[u]):
                    for b, hv in enumerate(hs[v]):
                        ip = inner(hu, hv)
                        for e in possible_edges:
                            if (e or common) and short_masks is not None and (
                                short_masks[u][a][0] & short_masks[v][b][0] or
                                short_masks[u][a][1] & short_masks[v][b][1]):
                                continue
                            off = (base8 - 8 * e) * det - 8 * ip
                            if not pair_psd or off * off <= norms[u][a] * norms[v][b]:
                                allowed.append([a, b] if isinstance(edge, int) else [a, b, e])
                pair_cache[cache_key] = allowed
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
    minc_info=None
    if minc_lines:
        from root_component_minimum_partition import add_minimum_partitions
        minc_info=add_minimum_partitions(model,graph,minc_lines)
    profile_info=None
    if six_prism_profiles:
        from root_component_six_prism_profiles import add_six_prism_profiles
        profile_info=add_six_prism_profiles(model,graph,template,triple_packing=profile_triples)
    general_profiles=None
    if line_profiles:
        from root_component_line_profiles import add_line_profiles
        general_profiles=add_line_profiles(model,graph,template,line_profiles,triple_packing=profile_triples,
                                          signature_data=(edges,hfull,indicators))
    exact_triangle_info=None
    if exact_triangles:
        from root_component_exact_triangles import add_exact_triangle_structure
        exact_triangle_info=add_exact_triangle_structure(model,graph,template)
    info = {"pair_psd_tables": pair_tables, "pair_psd_rows": pair_rows, "c2_equations": c2_count,
            "moment_equations": len(anchors) * (len(anchors) + 1) // 2,
            "signature_flags": sum(len(x) for x in indicators), "full_C2": layer == 4,
            "eigen_equations": eigen, "eigen_products": eigen_products,
            "mate_flip_signature_normalization": mate_normalize,"explicit_four_sums":True,
            "four_corner_tables":corner_info, "local_component_tables": local_info,
            "nonroot_minimum_component_partitions":minc_info,"six_prism_profiles":profile_info,
            "line_profiles":general_profiles,"shared_label_triangle_clauses":triangle_info,
            "exact_triangle_structure":exact_triangle_info,"short_vector_filter":short_info}
    return model, graph, info


def solve(template, matrix, seconds, layer=0, workers=1, eigen=False, mate_normalize=False, corners=False, local_tables=None, cpu_time=False, minc_lines=0, six_prism_profiles=False, line_profiles=0, profile_triples=False, triangle_cuts=False, exact_triangles=False, short_vectors=False, linearization=0):
    started = time.monotonic()
    model, graph, info = build(template, matrix, layer, eigen=eigen, mate_normalize=mate_normalize,four_corners=corners,local_tables=local_tables,minc_lines=minc_lines,six_prism_profiles=six_prism_profiles,line_profiles=line_profiles,profile_triples=profile_triples,triangle_cuts=triangle_cuts,exact_triangles=exact_triangles,short_vectors=short_vectors)
    assert not model.validate(), model.validate()
    info.update(build_seconds=time.monotonic() - started, variables=len(model.proto.variables), constraints=len(model.proto.constraints))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.max_time_in_seconds = max(600,100*seconds) if cpu_time else seconds
    solver.parameters.cp_model_probing_level = 0
    solver.parameters.symmetry_level = 0
    solver.parameters.linearization_level = linearization
    info['linearization_level'] = linearization
    search_cpu_start = time.process_time()
    timer_done = threading.Event()
    timer = None
    if cpu_time:
        def stop_after_cpu_budget():
            while not timer_done.wait(.1):
                if time.process_time() - search_cpu_start >= seconds:
                    solver.stop_search()
                    return
        timer = threading.Thread(target=stop_after_cpu_budget, daemon=True)
        timer.start()
    try:
        status = solver.solve(model)
    finally:
        timer_done.set()
        if timer is not None:
            timer.join()
    info.update(status=solver.status_name(status), solver_seconds=solver.wall_time,
                branches=solver.num_branches, conflicts=solver.num_conflicts,
                solver_cpu_seconds=time.process_time()-search_cpu_start,
                budget_kind="process_cpu_seconds" if cpu_time else "wall_seconds")
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
    parser.add_argument("--eigen", action="store_true")
    parser.add_argument("--cpu-time", action="store_true")
    parser.add_argument("--minc-lines",type=int,default=0)
    parser.add_argument("--six-prism-profiles",action="store_true")
    parser.add_argument("--line-profiles",type=int,default=0)
    parser.add_argument("--profile-triples",action="store_true")
    parser.add_argument("--triangle-cuts",action="store_true")
    parser.add_argument("--exact-triangles",action="store_true")
    parser.add_argument("--short-vectors",action="store_true")
    parser.add_argument("--linearization",type=int,choices=range(3),default=0)
    parser.add_argument("--limit-grams", type=int)
    parser.add_argument("--mate-normalize", action="store_true")
    parser.add_argument("--corners",action="store_true")
    parser.add_argument("--gram-indices", type=int, nargs="+")
    parser.add_argument("--local-tables", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    from root_component_resources import limit_research_process
    resources=limit_research_process(4)
    local_tables = json.loads(args.local_tables.read_text()) if args.local_tables else None
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
            if args.gram_indices is not None and gi not in args.gram_indices:
                continue
            if args.limit_grams is not None and gi >= args.limit_grams:
                break
            prev = earlier.get((index, gi), {})
            if prev.get("status") == "INFEASIBLE":
                assert prev["gram_anchor_values"] == values
                result = {"status": "INFEASIBLE", "source": prev.get("inherited_source", str(args.moments))}
            else:
                result = solve(templates[index], gram_matrix(cover, values), args.seconds, args.layer, args.workers, args.eigen, args.mate_normalize,args.corners,local_tables,cpu_time=args.cpu_time,minc_lines=args.minc_lines,six_prism_profiles=args.six_prism_profiles,line_profiles=args.line_profiles,profile_triples=args.profile_triples,triangle_cuts=args.triangle_cuts,exact_triangles=args.exact_triangles,short_vectors=args.short_vectors,linearization=args.linearization)
            result.update(gram_index=gi, gram_anchor_values=values)
            cases.append(result)
            print(json.dumps({"template": index, **{k: v for k, v in result.items() if k != "relaxation_edges"}}), flush=True)
            record.update(counts=dict(Counter(r["status"] for r in cases)),
                          all_source_grams_processed=len(cases) == cover["gram_count"],
                          excluded=len(cases) == cover["gram_count"] and all(r["status"] == "INFEASIBLE" for r in cases))
            temporary=args.output.with_suffix('.json.tmp')
            temporary.write_text(json.dumps({"scope": __doc__, "layer": args.layer,"resources":resources, "records": records}, separators=(",", ":")) + "\n", encoding="utf-8")
            temporary.replace(args.output)
        print(json.dumps({k: v for k, v in record.items() if k != "cases"}), flush=True)


if __name__ == "__main__":
    main()
