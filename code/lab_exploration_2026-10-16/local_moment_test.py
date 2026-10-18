"""Local moment test (LAB, 18/10/2026): only two root lines i, j are described.
A partial template in Codex's own schema (root_component_propagation.constraints: 'partial', 'known_grid_edges',
None for an unknown line): the partitions of lines i and j into components are given, the other five lines are
unknown.  Model: Codex's build on this partial template (C1/C2 on the 84 labels, letter quotas, degrees, the
component equations of lines i and j only, Gram definitions), no budget, no universal cuts, no triangles, no C R = 0;
plus the moment identities sum_w h_{w,e} h_{w,f} = 7 r_ef for the rectangles e, f known to be non-grid (by default
only the diagonal of Q_ij).  INFEASIBLE means: no Conway graph has a root with two lines whose component partitions
are these (whatever the five other lines).
usage: python local_moment_test.py <codex dir> --i I --j J --part-i '3,4,6' --part-j '0,2,5,6' [--all-pairs]
       [--budget] --seconds S --output out.json        (blocks separated by '/', e.g. '1,2/3,4,5,6')"""
import argparse
import json
import sys
import time
from itertools import combinations
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("codex", type=Path)
parser.add_argument("--i", type=int, required=True)
parser.add_argument("--j", type=int, required=True)
parser.add_argument("--part-i", type=str, required=True)
parser.add_argument("--part-j", type=str, required=True)
parser.add_argument("--all-pairs", action="store_true", help="all pairs of known non-grid rectangles, not only Q_ij")
parser.add_argument("--budget", action="store_true", help="add the root prism budget s <= 51")
parser.add_argument("--seconds", type=float, default=60)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.codex.resolve()))
from root_component_global import build                                    # noqa: E402
from root_component_propagation import RECTANGLES                          # noqa: E402
import root_component_complete_star as CS                                  # noqa: E402

i, j = args.i, args.j
assert i != j


def blocks(text):
    return [sorted(int(x) for x in b.split(",")) for b in text.split("/") if b]


parts = {i: blocks(args.part_i), j: blocks(args.part_j)}
for r, bl in parts.items():
    flat = [x for b in bl for x in b]
    assert len(flat) == len(set(flat)) and r not in flat and all(len(b) >= 2 for b in bl)
assert any(j in b for b in parts[i]) and any(i in b for b in parts[j]), "Q_ij must be non-grid from both sides"
nongrid, grids = set(), set()
for r, bl in parts.items():
    inblock = {x for b in bl for x in b}
    for x in range(7):
        if x == r:
            continue
        e = tuple(sorted((r, x)))
        (nongrid if x in inblock else grids).add(e)
assert not nongrid & grids, "inconsistent grid status between the two lines"
groups = [None] * 7
groups[i], groups[j] = parts[i], parts[j]
counts = [0] * 7                                  # metadata only in build (info['root_minimum_components'])
for r, bl in parts.items():
    counts[r] = len(bl) + sum(1 for x in range(7) if x != r and not any(x in b for b in bl))
template = {"partial": True, "nongrid_edges": sorted(nongrid), "known_grid_edges": sorted(grids),
            "nontrivial_component_groups": groups, "kernel_dimension": 21, "component_count_by_root_line": counts}
t0 = time.process_time()
model, graph, info = build(template, {"cuts": [], "root_prism_budget": 51} if args.budget else {"cuts": []})
edges = [tuple(e) for e in template["nongrid_edges"]]
m = len(edges)
q0 = edges.index(tuple(sorted((i, j))))
result = {"scope": __doc__, "i": i, "j": j, "part_i": parts[i], "part_j": parts[j], "nongrid": edges,
          "grids": sorted(grids), "all_pairs": args.all_pairs, "budget": args.budget, "status": "NOT_RUN"}
if model is None:
    result.update(status="INFEASIBLE", method="exact_binary_propagation")
else:
    def rexpr(a, b):
        e, f = edges[a], edges[b]
        if a == b:
            return 8 - 2 * sum(graph[u][v] for u, v in combinations(RECTANGLES[e], 2))
        return (0 if set(e) & set(f) else 4) - sum(graph[u][v] for u in RECTANGLES[e] for v in RECTANGLES[f])

    use = range(m) if args.all_pairs else [q0]
    h, hdom = {}, {}
    for rect, corners in RECTANGLES.items():
        for w in corners:
            for f in use:
                target = edges[f]
                if rect == target:
                    base, lo, hi = 2, 0, 2
                elif set(rect) & set(target):
                    base, lo, hi = 0, -2, 0
                else:
                    base, lo, hi = 1, -3, 1
                v = model.new_int_var(lo, hi, "h")
                model.add(v == base - sum(graph[w][q] for q in RECTANGLES[target]))
                h[w, f] = v
                hdom[w, f] = (lo, hi)        # 18/10 fix: bounds kept in Python, never read back from the CP proto (unreliable in OR-Tools 9.15)
    labels = sorted({w for c in RECTANGLES.values() for w in c})
    pairs = [(a, b) for a in use for b in use if a <= b]
    for a, b in pairs:
        terms = []
        for w in labels:
            x, y = h[w, a], h[w, b]
            ends = [hdom[w, a], hdom[w, b]]
            prods = [p * q for p in ends[0] for q in ends[1]]
            pv = model.new_int_var(min(prods), max(prods), "p")
            model.add_multiplication_equality(pv, [x, y])
            terms.append(pv)
        model.add(sum(terms) == 7 * rexpr(a, b))
    result["pairs"] = len(pairs)
    result["build_cpu_seconds"] = time.process_time() - t0
    r = CS.solve_branch(model, graph, args.seconds)
    r.pop("adjacency", None)
    result.update(r)
json.dump(result, open(args.output, "w"), indent=1)
print(json.dumps({k: result.get(k) for k in ("i", "j", "part_i", "part_j", "status", "cpu_seconds", "branches",
                                             "conflicts", "pairs", "method")}))
