"""Why does a template die once its Gram cover is imposed?  Ablation of the gram_cover_branch.py model (LAB, 18/10/2026).
Every variant is a sub-model of the full one (Codex's all-in-one complete-star model + the complete Gram table on all
entries), so INFEASIBLE in a variant is INFEASIBLE in the full model; the smallest dying variant names the reason.
  all       : budget s <= 51 + universal root cuts (E3, component cuts) + exact triangles + full Gram table
  nobudget  : all without the budget
  nouniv    : all without the universal root cuts (the table still forces R_ii in {4,6,8})
  notri     : all without the exact triangles
  core      : C1/C2 + component equations + Gram definitions + full Gram table only
  gram=g    : 'all' with the table reduced to the single listed Gram number g (per-Gram death)
  notable   : 'all' without the table (= the plain all-in-one model, baseline)
  crzero    : 'all' without the table but with the linear identities C R = 0 written on Codex's r
              (sum over the rectangles at one component node of r_ij = 0, audit item 5)
usage: python gram_cover_ablation.py <codex dir> <catalogue> <index> <cover json> <variant> <seconds> <out.json>"""
import json
import sys
from pathlib import Path

codex, cat, ti, cov_path, variant, secs, out = (Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4]),
                                                sys.argv[5], float(sys.argv[6]), Path(sys.argv[7]))
sys.path.insert(0, str(codex.resolve()))
import root_component_complete_star as CS                                  # noqa: E402
from root_component_global import build                                    # noqa: E402
from root_component_gram_table import add_gram_table                       # noqa: E402
from root_component_exact_triangles import add_exact_triangle_structure    # noqa: E402

template, source_hash, _ = CS.load_template(cat, ti)
cover = json.load(open(cov_path))
edges = [tuple(e) for e in template["nongrid_edges"]]
m = len(edges)
assert cover["template_index"] == ti and cover["status"] == "COMPLETE" and [tuple(e) for e in cover["edges"]] == edges
grams = cover["grams"]
if variant.startswith("gram="):
    grams = [grams[int(variant[5:])]]
budget = variant not in ("nobudget", "core")
univ = variant not in ("nouniv", "core")
tri = variant not in ("notri", "core")
model, graph, info = build(template, {"cuts": [], "root_prism_budget": 51} if budget else {"cuts": []})
res = {"template": ti, "variant": variant, "budget": budget, "universal_cuts": univ, "triangles": tri,
       "gram_rows": len(grams), "cover_gram_count": cover["gram_count"]}
if model is None:
    res.update(status="INFEASIBLE", method="exact_binary_propagation")
else:
    if univ:
        CS.add_universal_root_cuts(model, graph, template)
    if tri:
        add_exact_triangle_structure(model, graph, template)
    full = [(i, j) for i in range(m) for j in range(i, m)]
    if variant == "crzero":
        from itertools import combinations
        from root_component_propagation import RECTANGLES
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import cle3_gram as GR
        _, nodes, links = GR.template_graph(template)

        def rexpr(i, j):
            e, f = edges[i], edges[j]
            if i == j:
                return 8 - 2 * sum(graph[a][b] for a, b in combinations(RECTANGLES[e], 2))
            return (0 if set(e) & set(f) else 4) - sum(graph[a][b] for a in RECTANGLES[e] for b in RECTANGLES[f])
        n_eq = 0
        for node in range(len(nodes)):
            inc = [i for i, ends in enumerate(links) if node in ends]
            for j in range(m):
                model.add(sum(rexpr(i, j) for i in inc) == 0)
                n_eq += 1
        res["cr_zero_equations"] = n_eq
    if variant not in ("notable", "crzero"):
        add_gram_table(model, graph, template, {
            "exhaustive": True, "usable_as_gram_cover": True, "root_prism_budget": 51,
            "requires_separate_corner_realization": False, "anchors": list(range(m)), "anchor_pairs": full,
            "gram_anchor_values": [[R[i][j] for i, j in full] for R in grams], "gram_count": len(grams)})
    r = CS.solve_branch(model, graph, secs)
    r.pop("adjacency", None)
    res.update(r)
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: res.get(k) for k in ("template", "variant", "gram_rows", "status", "cpu_seconds", "branches", "conflicts")}))
