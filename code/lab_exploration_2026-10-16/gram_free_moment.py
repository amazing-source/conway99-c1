"""Gram-free moment model (LAB, 18/10/2026): Codex's exact all-in-one complete-star model + C R = 0 + the exact
quadratic identity H^T H = 7R written on the edges, with no Gram cover.
For each of the 84 labels w and each non-grid rectangle f: h_{w,f} = base - |N(w) cap Q_f| (base 2 / 0 / 1, bounds
[0,2] / [-2,0] / [-3,1]); for each pair e <= f: sum over w of h_{w,e} h_{w,f} = 7 r_ef (products by CP-SAT
multiplication equalities).  H = T P and T^2 = 7T give the identity exactly (audit section 3; C3_GRAM_COVER note).
Intended for templates whose Gram cover is too large to enumerate (dim ker C = 6, 7).
usage: python gram_free_moment.py <codex dir> <catalogue> --index i --seconds S [--no-crzero] [--diagonal-only]
       --output <out.json>"""
import argparse
import json
import sys
import time
from itertools import combinations
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("codex", type=Path)
parser.add_argument("templates", type=Path)
parser.add_argument("--index", type=int, required=True)
parser.add_argument("--seconds", type=float, default=600)
parser.add_argument("--no-crzero", action="store_true")
parser.add_argument("--diagonal-only", action="store_true", help="only the pairs e = f of the identity")
parser.add_argument("--core", action="store_true",
                    help="put each pair equation behind an assumption literal and report CP-SAT's sufficient subset")
parser.add_argument("--pairs", type=str, default=None, help="only these pairs, e.g. 0-3,0-4 (indices of non-grid edges)")
parser.add_argument("--no-bounds", action="store_true", help="debug: h domains [-12, 12] instead of the proved bounds")
parser.add_argument("--debug-solver", type=str, default=None, help="debug: 'nopresolve' or 'log' (plain CP-SAT solve)")
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.codex.resolve()))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import root_component_complete_star as CS                                  # noqa: E402
from root_component_global import build                                    # noqa: E402
from root_component_exact_triangles import add_exact_triangle_structure    # noqa: E402
from root_component_propagation import RECTANGLES                          # noqa: E402
from root_component_resources import atomic_json_write, limit_research_process  # noqa: E402
import cle3_gram as GR                                                     # noqa: E402

if args.output.exists():
    raise FileExistsError("Use a fresh report, never overwrite a previous verdict.")
resources = limit_research_process(1)
template, source_hash, _ = CS.load_template(args.templates, args.index)
edges = [tuple(e) for e in template["nongrid_edges"]]
m = len(edges)
t0 = time.process_time()
model, graph, info = build(template, {"cuts": [], "root_prism_budget": 51})
result = {"scope": __doc__, "template_index": args.index, "source_sha256": source_hash, "m": m,
          "kernel_dimension": template["kernel_dimension"], "crzero": not args.no_crzero,
          "diagonal_only": args.diagonal_only, "seconds": args.seconds, "resources": resources, "status": "NOT_RUN"}
if model is None:
    result.update(status="INFEASIBLE", method="exact_binary_propagation")
else:
    CS.add_universal_root_cuts(model, graph, template)
    add_exact_triangle_structure(model, graph, template)

    def rexpr(i, j):
        e, f = edges[i], edges[j]
        if i == j:
            return 8 - 2 * sum(graph[a][b] for a, b in combinations(RECTANGLES[e], 2))
        return (0 if set(e) & set(f) else 4) - sum(graph[a][b] for a in RECTANGLES[e] for b in RECTANGLES[f])

    if not args.no_crzero:
        _, nodes, links = GR.template_graph(template)
        for node in range(len(nodes)):
            inc = [i for i, ends in enumerate(links) if node in ends]
            for j in range(m):
                model.add(sum(rexpr(i, j) for i in inc) == 0)
    h = {}
    for rect, corners in RECTANGLES.items():
        for w in corners:
            for f in range(m):
                target = edges[f]
                if rect == target:
                    base, lo, hi = 2, 0, 2
                elif set(rect) & set(target):
                    base, lo, hi = 0, -2, 0
                else:
                    base, lo, hi = 1, -3, 1
                if args.no_bounds:
                    lo, hi = -12, 12
                v = model.new_int_var(lo, hi, "h_%d_%d" % (w, f))
                model.add(v == base - sum(graph[w][q] for q in RECTANGLES[target]))
                h[w, f] = v
    labels = sorted({w for corners in RECTANGLES.values() for w in corners})
    assert len(labels) == 84
    products = 0
    assumptions = {}
    only = None if args.pairs is None else {tuple(int(x) for x in q.split("-")) for q in args.pairs.split(",")}
    for e in range(m):
        for f in range(e, m):
            if args.diagonal_only and f != e:
                continue
            if only is not None and (e, f) not in only:
                continue
            terms = []
            for w in labels:
                a, b = h[w, e], h[w, f]
                lo = min(x * y for x in (a.proto.domain[0], a.proto.domain[-1]) for y in (b.proto.domain[0], b.proto.domain[-1]))
                hi = max(x * y for x in (a.proto.domain[0], a.proto.domain[-1]) for y in (b.proto.domain[0], b.proto.domain[-1]))
                p = model.new_int_var(lo, hi, "p")
                model.add_multiplication_equality(p, [a, b])
                terms.append(p)
                products += 1
            if args.core:
                lit = model.new_bool_var("pair_%d_%d" % (e, f))
                model.add(sum(terms) == 7 * rexpr(e, f)).only_enforce_if(lit)
                assumptions[lit.index] = (e, f)
            else:
                model.add(sum(terms) == 7 * rexpr(e, f))
    if args.core:
        model.add_assumptions([model.get_bool_var_from_proto_index(i) for i in assumptions])
    result["products"] = products
    result["build_cpu_seconds"] = time.process_time() - t0
    if args.debug_solver:
        from ortools.sat.python import cp_model
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = args.seconds
        if args.debug_solver == "nopresolve":
            solver.parameters.cp_model_presolve = False
        solver.parameters.log_search_progress = args.debug_solver == "log"
        st = solver.solve(model)
        result["status"] = solver.status_name(st)
        result["branches"], result["conflicts"] = solver.num_branches, solver.num_conflicts
        r = {}
    elif args.core:
        from ortools.sat.python import cp_model
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = args.seconds
        st = solver.solve(model)
        result["status"] = solver.status_name(st)
        if st == cp_model.INFEASIBLE:
            core = [assumptions[i] for i in solver.sufficient_assumptions_for_infeasibility()]
            result["core_pairs"] = [[list(edges[e]), list(edges[f])] for e, f in core]
            result["core_pair_indices"] = core
        r = {}
    else:
        r = CS.solve_branch(model, graph, args.seconds)
    result.update(r)
    if r.get("exact_all_pair_check"):
        result["status"] = "CONWAY_GRAPH_FOUND"
result["process_peak_rss_bytes"] = CS.peak_memory_bytes()
atomic_json_write(args.output, result)
print(json.dumps({k: result.get(k) for k in ("template_index", "kernel_dimension", "status", "cpu_seconds", "products",
                                             "branches", "conflicts", "build_cpu_seconds", "core_pair_indices")}))
