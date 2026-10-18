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
parser.add_argument("--ablate", type=str, default="", help="comma list among budget,univ,tri: parts of the base model to drop")
parser.add_argument("--codex-moments", type=Path, default=None,
                    help="second encoding: Codex's root_component_neighbor_moments.add_neighbor_moments (52d7d465) on the "
                         "21 rectangles, instead of the LAB products")
parser.add_argument("--mixed", action="store_true", help="with --codex-moments: also the mixed identities")
parser.add_argument("--combine", type=str, default=None,
                    help="with --codex-moments: also add, for these non-grid edge indices f (e.g. 0), the LINEAR combination "
                         "sum_w [base^2 + (1 - 2 base) z_w + 2 binom(z_w,2)] = 7 r_ff of Codex's own variables "
                         "(a linear consequence of his three identities; it adds no logical content)")
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
ablate = set(x for x in args.ablate.split(",") if x)
model, graph, info = build(template, {"cuts": []} if "budget" in ablate else {"cuts": [], "root_prism_budget": 51})
result = {"scope": __doc__, "template_index": args.index, "source_sha256": source_hash, "m": m,
          "kernel_dimension": template["kernel_dimension"], "crzero": not args.no_crzero,
          "diagonal_only": args.diagonal_only, "seconds": args.seconds, "resources": resources, "status": "NOT_RUN"}
if model is None:
    result.update(status="INFEASIBLE", method="exact_binary_propagation")
else:
    if "univ" not in ablate:
        CS.add_universal_root_cuts(model, graph, template)
    if "tri" not in ablate:
        add_exact_triangle_structure(model, graph, template)
    result["ablate"] = sorted(ablate)

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
    if args.codex_moments is not None:
        sys.path.append(str(args.codex_moments.resolve()))
        from root_component_neighbor_moments import add_neighbor_moments
        from root_component_propagation import LABELS
        nm = add_neighbor_moments(model, LABELS, graph, mixed=args.mixed)
        result["codex_moments"] = nm["info"]
        if args.combine:
            for f in (int(x) for x in args.combine.split(",")):
                q = edges[f]
                zs, cs = nm["columns"][q], nm["costs"][q]
                expr = []
                for w, lab in enumerate(LABELS):
                    rect = tuple(sorted(a // 2 for a in lab))
                    base = 2 if rect == q else (0 if set(rect) & set(q) else 1)
                    expr.append(base * base + (1 - 2 * base) * zs[w] + 2 * cs[w])
                model.add(sum(expr) == 7 * rexpr(f, f))
            result["combined"] = args.combine
        result["products"] = 0
        result["build_cpu_seconds"] = time.process_time() - t0
        if args.debug_solver == "lp":
            from ortools.sat.python import cp_model
            solver = cp_model.CpSolver()
            solver.parameters.num_search_workers = 1
            solver.parameters.max_time_in_seconds = args.seconds
            solver.parameters.linearization_level = 2
            st = solver.solve(model)
            r = {"status": solver.status_name(st), "branches": solver.num_branches, "conflicts": solver.num_conflicts,
                 "cpu_seconds": solver.user_time}
        else:
            r = CS.solve_branch(model, graph, args.seconds)
        result.update(r)
        result["process_peak_rss_bytes"] = CS.peak_memory_bytes()
        atomic_json_write(args.output, result)
        print(json.dumps({k: result.get(k) for k in ("template_index", "kernel_dimension", "status", "cpu_seconds",
                                                     "branches", "conflicts", "build_cpu_seconds")} | {"encoding": "codex"}))
        sys.exit(0)
    h, hdom = {}, {}
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
                hdom[w, f] = (lo, hi)        # 18/10 fix: bounds kept in Python, never read back from the CP proto (unreliable in OR-Tools 9.15)
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
                (alo, ahi), (blo, bhi) = hdom[w, e], hdom[w, f]
                lo = min(x * y for x in (alo, ahi) for y in (blo, bhi))
                hi = max(x * y for x in (alo, ahi) for y in (blo, bhi))
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
