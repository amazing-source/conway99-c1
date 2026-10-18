"""All-in-one complete-star model of Codex + an exhaustive Gram cover of the template (LAB, 18/10/2026).
The model is Codex's build_branch(template, root, None, transport=False) (both internal stars free, budget s <= 51,
universal root cuts, exact triangles), with one extra necessary constraint: the matrix R of the 21-rectangle Gram,
written through the graph edges (Codex's r), takes one of the values of a COMPLETE list of the integer R allowed by
the quotient system (gram_cover_enum.py: C R = 0, E3, signs and bounds, zeros between components, connectivity cuts,
trace <= 28 dim ker C, R >= 0, 28 I - R >= 0; each is a proved consequence, audit 18/10 section 3, items 4-8).
The complete-star model alone does not impose R >= 0, which is why the table can cut.
  --table anchors : Codex's add_gram_table on the anchor block (R is determined by it inside ker C);
  --table full    : the same plus a table on every entry R_ij, i <= j (still exact: each listed R is complete).
INFEASIBLE here excludes the template (all matchings of the star at once); UNKNOWN means nothing.
usage: python gram_cover_branch.py <codex dir> <catalogue> --index i --cover <gram_cover_enum output> --seconds S
       [--table anchors|full] --output <out.json>"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("codex", type=Path)
parser.add_argument("templates", type=Path)
parser.add_argument("--index", type=int, required=True)
parser.add_argument("--cover", type=Path, required=True)
parser.add_argument("--seconds", type=float, default=600)
parser.add_argument("--table", choices=("anchors", "full"), default="anchors")
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.codex.resolve()))
import root_component_complete_star as CS                                  # noqa: E402
from root_component_global import build                                    # noqa: E402
from root_component_gram_table import add_gram_table                       # noqa: E402
from root_component_exact_triangles import add_exact_triangle_structure    # noqa: E402
from root_component_resources import atomic_json_write, limit_research_process  # noqa: E402

if args.output.exists():
    raise FileExistsError("Use a fresh report, never overwrite a previous verdict.")
resources = limit_research_process(1)
template, source_hash, metadata = CS.load_template(args.templates, args.index)
raw = args.cover.read_bytes()
cover = json.loads(raw)
edges = [tuple(e) for e in template["nongrid_edges"]]
m = len(edges)
assert cover["template_index"] == args.index and cover["status"] == "COMPLETE", "only a complete list is a cover"
assert [tuple(e) for e in cover["edges"]] == edges, "edge order of the cover differs from the template"
anchors = cover["anchors"]
d = len(anchors)
assert d == template["kernel_dimension"]
grams = cover["grams"]
assert all(len(R) == m and all(len(row) == m for row in R) for R in grams)
assert all(R[i][j] == R[j][i] for R in grams for i in range(m) for j in range(m))
pairs = [(a, b) for a in range(d) for b in range(a, d)]
values = [[R[anchors[a]][anchors[b]] for a, b in pairs] for R in grams]
assert len({tuple(v) for v in values}) == len(values), "two listed R with the same anchor block"
record = {"exhaustive": True, "usable_as_gram_cover": True, "root_prism_budget": 51,
          "requires_separate_corner_realization": False, "anchors": anchors, "anchor_pairs": pairs,
          "gram_anchor_values": values, "gram_count": len(grams)}
root, parts, counts, matchings = CS.matching_cover(template)
result = {"scope": __doc__, "source_file": args.templates.as_posix(), "source_sha256": source_hash,
          "template_index": args.index, "template": template, "root_line": root, "component_parts": parts,
          "matching_count": len(matchings), "matching_partition": "all_in_one", "transport": False,
          "root_prism_budget": 51, "gram_cover_file": args.cover.as_posix(),
          "gram_cover_sha256": hashlib.sha256(raw).hexdigest(), "gram_count": len(grams), "table": args.table,
          "seconds": args.seconds, "resources": resources, "status": "NOT_RUN"}
args.output.parent.mkdir(parents=True, exist_ok=True)
atomic_json_write(args.output, result)
t0 = time.process_time()
model, graph, info = build(template, {"cuts": [], "root_prism_budget": 51}, gram_cover=record)
if model is not None:
    info["universal_root_cuts"] = CS.add_universal_root_cuts(model, graph, template)
    info["triangles"] = add_exact_triangle_structure(model, graph, template)
    if args.table == "full":
        full = [(i, j) for i in range(m) for j in range(i, m)]
        info["full_table"] = add_gram_table(model, graph, template, {
            "exhaustive": True, "usable_as_gram_cover": True, "root_prism_budget": 51,
            "requires_separate_corner_realization": False, "anchors": list(range(m)), "anchor_pairs": full,
            "gram_anchor_values": [[R[i][j] for i, j in full] for R in grams], "gram_count": len(grams)})
    info["model_variables"] = len(model.proto.variables)
    info["model_constraints"] = len(model.proto.constraints)
result["build_cpu_seconds"] = time.process_time() - t0
result["model"] = info
if model is None:
    assert info["status"] == "PROPAGATION_CONTRADICTION"
    result.update(status="INFEASIBLE", method="exact_binary_propagation")
else:
    branch = CS.solve_branch(model, graph, args.seconds)
    result.update(branch)
    if branch.get("exact_all_pair_check"):
        result["status"] = "CONWAY_GRAPH_FOUND"
result["process_peak_rss_bytes"] = CS.peak_memory_bytes()
atomic_json_write(args.output, result)
print(json.dumps({k: result.get(k) for k in ("template_index", "table", "gram_count", "status", "cpu_seconds",
                                             "branches", "conflicts", "build_cpu_seconds")}), flush=True)
