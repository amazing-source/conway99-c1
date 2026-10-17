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
import threading

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


def build(template, cover, layer=2, projector=True, local_tables=None, normalize_component=False,
          line_profiles=0,profile_triples=False,exact_triangles=False,minc_lines=0):
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
    profile_info=None
    if line_profiles:
        from root_component_line_profiles import add_line_profiles
        profile_info=add_line_profiles(model,graph,template,line_profiles,triple_packing=profile_triples)
    triangle_info=None
    if exact_triangles:
        from root_component_exact_triangles import add_exact_triangle_structure
        triangle_info=add_exact_triangle_structure(model,graph,template)
    minc_info=None
    if minc_lines:
        from root_component_minimum_partition import add_minimum_partitions
        minc_info=add_minimum_partitions(model,graph,minc_lines)
    return model, graph, {"complete_gram_cover": gram_info, "projector": projector_info,
                          "C2_count": c2_count, "C2_products": len(products), "full_C2": layer == 4,
                          "local_component_tables": local_info,"line_profiles":profile_info,
                          "exact_triangle_structure":triangle_info,"nonroot_minimum_component_partitions":minc_info}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--layer", type=int, choices=range(5), default=2)
    parser.add_argument("--seconds", type=float, default=300)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--grams", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--local-tables", type=Path)
    parser.add_argument("--normalize-component",action="store_true")
    parser.add_argument("--log-search",action="store_true")
    parser.add_argument("--cpu-time",action="store_true")
    parser.add_argument("--signature-domains",action="store_true")
    parser.add_argument("--coupled-corners",action="store_true")
    parser.add_argument("--minc-lines",type=int,default=0)
    parser.add_argument("--line-profiles",type=int,default=0)
    parser.add_argument("--profile-triples",action="store_true")
    parser.add_argument("--exact-triangles",action="store_true")
    args = parser.parse_args()
    from root_component_resources import limit_research_process
    resources=limit_research_process(4)
    templates = json.loads((args.directory / "root_component_templates.json").read_text())["survivors"]
    source = args.grams or args.directory / "root_component_gram_orbits20.json"
    cover = next(r for r in json.loads(source.read_text())["records"] if r["template_index"] == args.index)
    started = time.monotonic()
    if args.coupled_corners:
        import hashlib
        from root_component_coupled_cover import prepare
        from root_component_resources import atomic_json_write
        cache=args.output.with_suffix('.prepared.json')
        digest=hashlib.sha256(json.dumps(cover,sort_keys=True).encode()).hexdigest()
        if cache.exists():
            prepared=json.loads(cache.read_text())
            assert prepared['source_sha256']==digest
            cover=prepared['cover']
        else:
            cover=prepare(templates[args.index],cover,lambda i,b:print(json.dumps({'prepared_gram':i,'empty_corner_domain':b}),flush=True))
            atomic_json_write(cache,{'source_sha256':digest,'cover':cover})
    elif args.signature_domains:
        from root_component_signature_moments import gram_matrix
        from root_rectangle_domains import signature_domains
        rows={q:[] for q in RECTANGLES}
        edges=[tuple(e) for e in templates[args.index]['nongrid_edges']]
        for gi,values in enumerate(cover['gram_anchor_values']):
            matrix=gram_matrix(cover,values)
            domains=signature_domains(edges,[[int(x) for x in row] for row in matrix.tolist()])
            for domain in domains:
                rows[tuple(domain['rectangle'])]+=[[gi]+[h[a] for a in cover['anchors']] for h in domain['signatures']]
        cover=dict(cover,row_signature_tables=[{'rectangle':list(q),'rows':rs} for q,rs in rows.items()])
    local_tables = None if args.local_tables is None else json.loads(args.local_tables.read_text())
    model, graph, info = build(templates[args.index], cover, args.layer, local_tables=local_tables,
                              normalize_component=args.normalize_component,line_profiles=args.line_profiles,
                              profile_triples=args.profile_triples,exact_triangles=args.exact_triangles,minc_lines=args.minc_lines)
    assert not model.validate(), model.validate()
    info.update(template_index=args.index, status="MODEL_BUILT", build_seconds=time.monotonic()-started,
                variables=len(model.proto.variables), constraints=len(model.proto.constraints), source=str(source),
                resources=resources,root_prism_budget=51,fixed_gram_witness=False,fixed_local_seed=False,
                scope="Whole template with variable Gram; no graph automorphism or fixed local seed.")
    def checkpoint():
        temporary=args.output.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
        temporary.replace(args.output)
    checkpoint()
    print(json.dumps(info), flush=True)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_time_in_seconds = max(600,100*args.seconds) if args.cpu_time else args.seconds
    solver.parameters.cp_model_probing_level = 0
    solver.parameters.symmetry_level = 0
    solver.parameters.linearization_level = 0
    solver.parameters.log_search_progress = args.log_search
    cpu_started=time.process_time()
    done=threading.Event()
    timer=None
    if args.cpu_time:
        def interrupt():
            while not done.wait(.1):
                if time.process_time()-cpu_started>=args.seconds:
                    solver.stop_search()
                    return
        timer=threading.Thread(target=interrupt,daemon=True)
        timer.start()
    try:
        status = solver.solve(model)
    finally:
        done.set()
        if timer is not None:timer.join()
    info.update(status=solver.status_name(status), solver_seconds=solver.wall_time,
                branches=solver.num_branches, conflicts=solver.num_conflicts,
                solver_cpu_seconds=time.process_time()-cpu_started,
                budget_kind='process_cpu_seconds' if args.cpu_time else 'wall_seconds')
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        gamma = [[solver.value(x) for x in row] for row in graph]
        errors = Counter()
        for u,v in PAIRS:
            if gamma[u][v]+sum(gamma[u][z]*gamma[v][z] for z in range(84)) != 2-len(set(LABELS[u])&set(LABELS[v])):
                errors[pair_layer(u,v)] += 1
        info["violated_C2_by_layer"] = dict(errors)
        info["relaxation_edges"] = [[u,v] for u,v in PAIRS if gamma[u][v]]
    checkpoint()
    print(json.dumps({k:v for k,v in info.items() if k != "relaxation_edges"}), flush=True)


if __name__ == "__main__":
    main()
