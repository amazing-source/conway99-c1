"""Two-star refinement of Codex's complete-star branch (LAB, 18/10/2026), no-transport model.
For a template, its star line r0 = {v, a, a*} and the matching M of the star of a (as in Codex's cover), the internal
matching M' of the OPPOSITE star (letter a*, 12 labels, one perfect matching per component) is free in Codex's model.
Here M' is fixed as well: the branches (M, M') for all M' cover the branch M exactly (the opposite star has one of
these matchings in any realisation), so the branch M is excluded iff every (M, M') is.  The model is Codex's
build(template, ..., extra_initial = both stars) + universal root cuts + exact triangles, i.e. his --no-transport model
with more initial values; solved by his solve_branch.
usage: python two_star_branch.py <package dir> <catalogue> <template index> <matching index> <seconds> <out.json>
       [--opposite i,j,...]  (default: all opposite matchings)"""
import json
import sys
import time
from itertools import combinations, product
from pathlib import Path

pkg, cat, ti, mi, secs, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
sys.path.insert(0, str(Path(pkg) / "code" / "codex"))
import root_component_complete_star as CS                # noqa: E402
from root_component_propagation import LABELS, variable  # noqa: E402

template, _, _ = CS.load_template(Path(cat), ti)
root, parts, counts, cover = CS.matching_cover(template)
M = cover[mi]
lookup = {tuple(p): w for w, p in enumerate(LABELS)}
opp_vertices = [[lookup[tuple(sorted((2 * root + 1, a)))] for j in p for a in (2 * j, 2 * j + 1)] for p in parts]
opp_cover = [tuple(sorted(e for m in sel for e in m)) for sel in product(*(tuple(CS.perfect_matchings(vs)) for vs in opp_vertices))]
opp_star = sorted({w for vs in opp_vertices for w in vs})
assert len(opp_star) == 12
selected = list(range(len(opp_cover)))
if "--opposite" in sys.argv:
    selected = [int(x) for x in sys.argv[sys.argv.index("--opposite") + 1].split(",")]
from root_component_global import build                  # noqa: E402
from root_component_exact_triangles import add_exact_triangle_structure  # noqa: E402
results = []
for oi in selected:
    Mp = set(opp_cover[oi])
    init = dict(CS.matching_assignments(root, M))
    init.update({variable(u, v): int((u, v) in Mp) for u, v in combinations(opp_star, 2)})
    t0 = time.process_time()
    model, graph, info = build(template, {"cuts": [], "root_prism_budget": 51}, extra_initial=init)
    if model is None:
        r = {"opposite_index": oi, "status": "INFEASIBLE", "method": info.get("status")}
    else:
        CS.add_universal_root_cuts(model, graph, template)
        add_exact_triangle_structure(model, graph, template)
        build_cpu = time.process_time() - t0
        r = dict(opposite_index=oi, build_cpu=build_cpu, **CS.solve_branch(model, graph, secs))
        r.pop("adjacency", None)
    results.append(r)
    print(json.dumps({k: r[k] for k in r if k in ("opposite_index", "status", "cpu_seconds", "build_cpu", "method")}), flush=True)
    json.dump({"template": ti, "root": root, "parts": [len(p) for p in parts], "matching": mi,
               "opposite_count": len(opp_cover), "results": results}, open(out, "w"), indent=1)
