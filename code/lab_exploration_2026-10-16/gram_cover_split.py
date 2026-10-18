"""Gram-by-Gram split of the exact all-in-one model (LAB, 18/10/2026).
The template is covered by its COMPLETE Gram list (gram_cover_enum*.py): a Conway graph realizing the template has its
rectangle Gram R equal to one listed R_k.  So the template is excluded iff, for every k, the model with R = R_k is
INFEASIBLE.  The base model is Codex's all-in-one complete-star model (build with budget 51, universal root cuts,
exact triangles, no transport) plus the identities C R = 0 written on Codex's r (audit item 5; optional); it is built
once and cloned for each k, where all the entries r_ij (i <= j) are fixed to R_k.
(gc2a, 18/10: on template 4192, the 79 single-Gram models die in 10-13 s each, while one table of all 79 rows stays
UNKNOWN at 600 s.)
Optional necessary conditions per Gram (cle3_corner.py = Codex's root_rectangle_domains without its rank <= 4 assert:
h_w = (T 1_Q)_w, [[T_ww, h_w^T], [h_w, R]] >= 0 with T_ww = 5/2, so h_w in im R and h_w^T R^+ h_w <= 5/2 in any rank):
  --corner-filter     : the Gram needs, for each of the 21 rectangles, a binary corner graph and four signatures with
                        [[T_QQ, H_Q], [H_Q^T, R]] >= 0, and the minimal prism sum <= 51; else the Gram is excluded;
  --signature-tables  : every one of the 84 labels w has its signature vector h_w (on the m non-grid rectangles) in
                        the finite domain of its rectangle (table constraint).
usage: python gram_cover_split.py <codex dir> <catalogue> --index i --cover <cover json(.gz)> --per-gram S
       --budget B [--no-crzero] [--keep-going] --output <out.json>"""
import argparse
import gzip
import json
import sys
import time
from itertools import combinations
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("codex", type=Path)
parser.add_argument("templates", type=Path)
parser.add_argument("--index", type=int, required=True)
parser.add_argument("--cover", type=Path, required=True)
parser.add_argument("--per-gram", type=float, default=60)
parser.add_argument("--budget", type=float, default=3600, help="total CPU seconds for all the Grams of the template")
parser.add_argument("--no-crzero", action="store_true")
parser.add_argument("--keep-going", action="store_true", help="continue after an UNKNOWN Gram (statistics)")
parser.add_argument("--only", type=str, default=None, help="comma-separated Gram numbers (a test; no template verdict)")
parser.add_argument("--slice", type=str, default=None,
                    help="i/n: only the Grams order[i::n] of the trace-sorted order; the record says which Grams it covers, "
                         "and the template is excluded iff the n slices are all ALL_INFEASIBLE (checked by the analysis)")
parser.add_argument("--moment-filter", action="store_true",
                    help="moment_bounds.analyse (LAB, from scratch) before any SAT: corner realizations + H^T H = 7R bounds")
parser.add_argument("--moment-design", type=float, default=0.0,
                    help="seconds for the exact moment design of moment_bounds (one corner realization per rectangle, "
                         "sum of the moments = 7R on every pair), after the bounds")
parser.add_argument("--codex-moment", type=Path, default=None,
                    help="directory of Codex's root_component_corner_moment_bounds (cross-check, ranks <= 5)")
parser.add_argument("--corner-filter", action="store_true")
parser.add_argument("--signature-tables", action="store_true")
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
import cle3_corner as CC                                                   # noqa: E402
import moment_bounds as MB                                                 # noqa: E402

if args.output.exists():
    raise FileExistsError("Use a fresh report, never overwrite a previous verdict.")
resources = limit_research_process(1)
template, source_hash, _ = CS.load_template(args.templates, args.index)
raw = args.cover.read_bytes()
cover = json.loads(gzip.decompress(raw) if args.cover.suffix == ".gz" else raw)
edges = [tuple(e) for e in template["nongrid_edges"]]
m = len(edges)
assert cover["template_index"] == args.index and cover["status"] == "COMPLETE", "only a complete list is a cover"
assert [tuple(e) for e in cover["edges"]] == edges
grams = cover["grams"]
t0 = time.process_time()
model, graph, info = build(template, {"cuts": [], "root_prism_budget": 51})
result = {"scope": __doc__, "template_index": args.index, "source_sha256": source_hash, "gram_count": len(grams),
          "per_gram_seconds": args.per_gram, "budget_seconds": args.budget, "crzero": not args.no_crzero,
          "corner_filter": args.corner_filter, "signature_tables": args.signature_tables,
          "resources": resources, "grams": [], "status": "NOT_RUN"}
if model is None:
    result.update(status="INFEASIBLE", method="exact_binary_propagation")
    atomic_json_write(args.output, result)
    print(json.dumps({"template_index": args.index, "status": "INFEASIBLE", "method": "exact_binary_propagation"}))
    sys.exit(0)
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
result["build_cpu_seconds"] = time.process_time() - t0
spent = 0.0
order = sorted(range(len(grams)), key=lambda k: sum(grams[k][i][i] for i in range(m)))
if args.only is not None:
    order = [int(x) for x in args.only.split(",")]
if args.slice is not None:
    si, sn = (int(x) for x in args.slice.split("/"))
    assert 0 <= si < sn
    order = order[si::sn]
    result["slice"] = [si, sn]
    result["slice_grams"] = order
codex_verdicts = None
if args.codex_moment is not None:
    import subprocess
    tmp = str(args.output) + ".codex_moments.json"
    subprocess.run([sys.executable, "-I", "-X", "utf8", str(Path(__file__).resolve().parent / "codex_moment_batch.py"),
                    str(args.codex_moment), str(args.cover), ",".join(str(k) for k in order), tmp], check=False)
    try:
        codex_verdicts = json.load(open(tmp))
    except Exception:
        codex_verdicts = {}
    result["codex_moment_dir"] = str(args.codex_moment)
all_infeasible = True
for k in order:
    if spent >= args.budget:
        all_infeasible = False
        result["stopped"] = "budget"
        break
    R = grams[k]
    if args.moment_filter or args.codex_moment is not None:
        verdicts = {}
        if args.moment_filter:
            t1 = time.process_time()
            mb = MB.analyse(edges, R, args.moment_design)
            verdicts["lab"] = {k2: mb.get(k2) for k2 in ("status", "reason", "rectangle", "pair", "target_7R", "sum_min", "sum_max", "design")}
            verdicts["lab"]["cpu"] = round(time.process_time() - t1, 2)
        if codex_verdicts is not None:
            verdicts["codex"] = codex_verdicts.get(str(k), {"status": "MISSING"})
        stats = {v["status"] for v in verdicts.values()}
        if "EXCLUDED" in stats:
            row = {"gram": k, "status": "INFEASIBLE", "method": "moment_bounds", "verdicts": verdicts, "cpu_seconds": 0}
            known = {v["status"] for v in verdicts.values() if v["status"] in ("EXCLUDED", "PASSES", "PASSES_BOUNDS")}
            if len(verdicts) == 2 and "EXCLUDED" in known and len(known) == 2:
                row["moment_disagreement"] = True
                result["moment_disagreements"] = result.get("moment_disagreements", 0) + 1
            result["grams"].append(row)
            atomic_json_write(args.output, result)
            continue
    if args.corner_filter:
        cf = CC.rectangle_realizations(edges, R)
        if not cf["feasible"]:
            result["grams"].append({"gram": k, "status": "INFEASIBLE", "method": "corner_realization",
                                    "failed": str(cf.get("failed_rectangle")), "cpu_seconds": 0})
            atomic_json_write(args.output, result)
            continue
    clone = model.clone()
    for i in range(m):
        for j in range(i, m):
            clone.add(rexpr(i, j) == R[i][j])
    if args.signature_tables:
        for item in CC.signature_domains(edges, R):
            rect = tuple(item["rectangle"])
            rows = [list(h) for h in item["signatures"]]
            for w in RECTANGLES[rect]:
                hv = []
                for f in range(m):
                    target = edges[f]
                    base = 2 if rect == target else (0 if set(rect) & set(target) else 1)
                    v = clone.new_int_var(-3, 2, "h_%d_%d" % (w, f))
                    clone.add(v == base - sum(graph[w][q] for q in RECTANGLES[target]))
                    hv.append(v)
                if rows:
                    clone.add_allowed_assignments(hv, rows)
                else:
                    clone.add(False)
    r = CS.solve_branch(clone, graph, min(args.per_gram, args.budget - spent))
    spent += r["cpu_seconds"]
    row = {"gram": k, "status": r["status"], "cpu_seconds": round(r["cpu_seconds"], 2),
           "branches": r["branches"], "conflicts": r["conflicts"]}
    if r.get("exact_all_pair_check"):
        row["adjacency"] = r["adjacency"]
        result["grams"].append(row)
        result["status"] = "CONWAY_GRAPH_FOUND"
        break
    result["grams"].append(row)
    if r["status"] != "INFEASIBLE":
        all_infeasible = False
        if not args.keep_going:
            result["stopped"] = "unknown_gram"
            break
    atomic_json_write(args.output, result)
if result["status"] != "CONWAY_GRAPH_FOUND":
    if args.slice is not None:
        ok = all_infeasible and sorted(g["gram"] for g in result["grams"]) == sorted(order)
        result["status"] = "SLICE_ALL_INFEASIBLE" if ok else "UNKNOWN"
    else:
        done = len(result["grams"]) == len(grams) and args.only is None
        result["status"] = "INFEASIBLE" if all_infeasible and done else "UNKNOWN"
result["total_solve_cpu_seconds"] = round(spent, 1)
result["process_peak_rss_bytes"] = CS.peak_memory_bytes()
atomic_json_write(args.output, result)
st = [g["status"] for g in result["grams"]]
print(json.dumps({"template_index": args.index, "status": result["status"], "grams_done": len(st), "of": len(grams),
                  "infeasible": st.count("INFEASIBLE"), "cpu": round(spent, 1)}))
