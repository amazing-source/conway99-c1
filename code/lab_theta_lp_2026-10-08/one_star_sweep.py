"""C1, lab session, 2026-10-08. Is the obstruction of 17.59 a ONE-star obstruction? (question raised by Codex, 20:27 UTC)
  python one_star_sweep.py <codex code/codex dir (commit 96e7f23)> <ball json | cyclic> <out json> <max pivots per star> <apex> [<apex> ...]
Pair tables: Codex's mode "green" (Green value in {2,3}) INSIDE each star; every table BETWEEN the two stars is replaced by
"all compatible". The two stars then share only the fixed common apex w, so each star is an independent problem:
9 private shadows, exact pointwise sums K e_centre - w, Green value 3 and overlap <= 2 against w, Green value in {2,3}
between them. For each star and each pivot shadow (by increasing domain size, at most <max pivots>), every candidate
of the pivot is fixed in turn and Codex's exact propagation is run from the SAME fresh base domains; the star is
refuted with that pivot when every candidate ends in a contradiction. Integer, deterministic, no solver.
Output per apex branch: for each star, the first refuting pivot (or none within the limit) and the leaf count.
Not a certificate archive (Codex's audit format replays leaf traces); a classification of where the contradiction sits."""
import sys, json, time
sys.path.insert(0, sys.argv[1])
from itertools import combinations
import numpy as np
from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
from joint_star_propagation import propagate, replay
from two_star_core_ablation import filtered_system
g0 = cyclic_ball() if sys.argv[2] == "cyclic" else json.load(open(sys.argv[2]))["adjacency"]; maxp = int(sys.argv[4]); prepared = prepare(g0, 0, 12); out = {}; t00 = time.time()
def restrict(system, dom):
    common, labels, arrays, sides, targets, compat = system
    return common, labels, [a[d] for a, d in zip(arrays, dom)], sides, targets, {(i, j): compat[i, j][np.ix_(dom[i], dom[j])] for i in range(18) for j in range(18) if i != j}
for ap in [int(a) for a in sys.argv[5:]]:
    common, labels, arrays, sides, targets, compat = filtered_system(prepared, 0, 12, ap, "green")
    for i, j in combinations(range(18), 2):
        if labels[i][0] != labels[j][0]: compat[i, j] = np.ones_like(compat[i, j]); compat[j, i] = np.ones_like(compat[j, i])
    system = (common, labels, arrays, sides, targets, compat); dom = [list(range(len(a))) for a in arrays]; sub = restrict(system, dom); res = propagate(sub); rec = {"apex_index": ap, "common_apex_support": list(common)}
    if res["contradiction"] is not None: rec["plain_propagation"] = res["contradiction"]; out[ap] = rec; continue
    alive = replay(sub, res); dom = [[d[k] for k in sorted(a)] for d, a in zip(dom, alive)]; rec["base_domain_sizes"] = [len(d) for d in dom]
    for s in (0, 1):
        tried = []; hit = None
        for i in sorted(sides[s], key=lambda k: (len(dom[k]), k))[:maxp]:
            surv = [c for c in dom[i] if propagate(restrict(system, [d if j != i else [c] for j, d in enumerate(dom)]))["contradiction"] is None]
            tried.append([i, len(dom[i]), len(surv)])
            if not surv: hit = i; break
        rec["star%d" % s] = {"refuting_pivot": hit, "pivots_tried": tried}
    out[ap] = rec
json.dump(out, open(sys.argv[3], "w"))
n = len(out); pl = sum(1 for r in out.values() if "plain_propagation" in r); k0 = sum(1 for r in out.values() if r.get("star0", {}).get("refuting_pivot") is not None); k1 = sum(1 for r in out.values() if r.get("star1", {}).get("refuting_pivot") is not None)
both = sum(1 for r in out.values() if r.get("star0", {}).get("refuting_pivot") is not None and r.get("star1", {}).get("refuting_pivot") is not None)
none = [a for a, r in out.items() if "plain_propagation" not in r and r["star0"]["refuting_pivot"] is None and r["star1"]["refuting_pivot"] is None]
first = sum(1 for r in out.values() if "star0" in r and (len(r["star0"]["pivots_tried"]) == 1 and r["star0"]["refuting_pivot"] is not None or len(r["star1"]["pivots_tried"]) == 1 and r["star1"]["refuting_pivot"] is not None))
print("%d branches (max %d pivots per star): plain propagation %d; star u alone refuted %d; star v alone refuted %d; both %d; at least one star with its smallest pivot %d; NEITHER star within the limit: %d %s  [%.0f s]" % (
    n, maxp, pl, k0, k1, both, first, len(none), none[:20], time.time() - t00), flush=True)
