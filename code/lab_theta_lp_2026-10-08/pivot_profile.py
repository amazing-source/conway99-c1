"""C1, lab session, 2026-10-08. What does a refuting pivot force that a surviving pivot does not? (Codex's question, 20:40 UTC)
  python pivot_profile.py <codex code/codex dir (commit 96e7f23)> <ball json | cyclic> <out json> <star 0|1> <max pivots> <apex> [<apex> ...]
Setting of one_star_sweep.py: Green-only tables inside each star, no table between the stars, fresh base domains from Codex's
plain propagation. For the chosen star and each pivot (by increasing domain size) and each candidate c of the pivot:
  * the domains of the 8 other private shadows of the star are cut to the candidates Green-compatible with c (one step);
  * for every point p outside the layer of the centre:  need(p) = t(p) - c(p),  cap(p) = number of those shadows that still
    have a candidate through p,  low(p) = number of those shadows all of whose candidates go through p;
  * "immediate" contradiction: need > cap or need < low at some point (no further propagation needed);
  * tight points: need = cap (every able shadow must cover p) and need = low;
  * outcome of Codex's full propagation (contradiction kind / survive), number of events.
Features of the candidate: does it contain the other transversal neighbour of the centre (then it is the star's second
isolated member), how many of its points have t = 1, its G-distances to the centre.
Then, for the star and each apex, a small exact search (branch on the smallest domain, Codex's propagation at every node)
counts the assignments of the nine private shadows satisfying the Green-only tables and the exact sums (cap 20), and tests
each one against Codex's FULL pair tables. Integer and deterministic. OBSERVATIONS only: nothing here is a general implication."""
import sys, json, time
sys.path.insert(0, sys.argv[1])
from itertools import combinations
from collections import Counter
import numpy as np
from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
from joint_star_propagation import propagate, replay, setup
from two_star_core_ablation import filtered_system
g0 = cyclic_ball() if sys.argv[2] == "cyclic" else json.load(open(sys.argv[2]))["adjacency"]; S = int(sys.argv[4]); maxp = int(sys.argv[5]); prepared = prepare(g0, 0, 12); g = np.asarray(prepared[0]); out = {}
centre = (0, 12)[S]; other = (12, 0)[S]; third = [int(q) for q in np.flatnonzero(g[centre]) if q // 12 not in (centre // 12, other // 12)][0]
def dist(src):
    d = {src: 0}; q = [src]
    for x in q:
        for y in range(36):
            if g[x][y] and y not in d: d[y] = d[x] + 1; q.append(y)
    return d
DC = dist(centre)
def restrict(system, dom):
    common, labels, arrays, sides, targets, compat = system
    return common, labels, [a[d] for a, d in zip(arrays, dom)], sides, targets, {(i, j): compat[i, j][np.ix_(dom[i], dom[j])] for i in range(18) for j in range(18) if i != j}
def close(system, dom):
    sub = restrict(system, dom); res = propagate(sub)
    if res["contradiction"] is not None: return None, res
    alive = replay(sub, res); return [[d[k] for k in sorted(a)] for d, a in zip(dom, alive)], res
for ap in [int(a) for a in sys.argv[6:]]:
    t0 = time.time(); common, labels, arrays, sides, targets, compat = filtered_system(prepared, 0, 12, ap, "green"); full = setup(prepared, 0, 12, ap)[5]
    for i, j in combinations(range(18), 2):
        if labels[i][0] != labels[j][0]: compat[i, j] = np.ones_like(compat[i, j]); compat[j, i] = np.ones_like(compat[j, i])
    system = (common, labels, arrays, sides, targets, compat); dom, res = close(system, [list(range(len(a))) for a in arrays]); star = sides[S]; t = np.asarray(targets[S]); pts = [p for p in range(36) if p // 12 != centre // 12]
    rec = {"apex_index": ap, "common_apex_support": list(common), "star": S, "centre": centre, "third_neighbour": third, "pivots": []}
    for i in sorted(star, key=lambda k: (len(dom[k]), k))[:maxp]:
        rows = []
        for c in dom[i]:
            cv = arrays[i][c]; cut = {j: [d for d in dom[j] if compat[i, j][c, d]] for j in star if j != i}
            need = {p: int(t[p] - cv[p]) for p in pts}; cap = {p: sum(1 for j in cut if any(arrays[j][d][p] for d in cut[j])) for p in pts}
            low = {p: sum(1 for j in cut if cut[j] and all(arrays[j][d][p] for d in cut[j])) for p in pts}
            imm = [p for p in pts if need[p] > cap[p] or need[p] < low[p]] + (["empty"] if any(not v for v in cut.values()) else [])
            sub, r = close(system, [d if j != i else [c] for j, d in enumerate(dom)])
            rows.append({"candidate": int(c), "support": [int(p) for p in np.flatnonzero(cv)], "has_third_neighbour": bool(cv[third]), "points_with_target_1": int(sum(1 for p in pts if cv[p] and t[p] == 1)),
                         "distances": sorted(DC[int(p)] for p in np.flatnonzero(cv)), "cut_sizes": sorted(len(v) for v in cut.values()), "immediate": [str(x) for x in imm],
                         "tight_cap": int(sum(1 for p in pts if need[p] == cap[p] and need[p] > 0)), "tight_low": int(sum(1 for p in pts if need[p] == low[p] and low[p] > 0)),
                         "survives": sub is not None, "end": None if sub is not None else r["contradiction"]["kind"], "events": len(r["trace"])})
        rec["pivots"].append({"shadow": int(i), "label": list(labels[i]), "domain": len(dom[i]), "survivors": sum(1 for x in rows if x["survives"]), "leaves": rows})
        if not any(x["survives"] for x in rows): break
    sols = []; nodes = [0]                                                          # exact count for this star (Green-only tables + sums)
    def dfs(d):
        nodes[0] += 1
        if len(sols) >= 20 or nodes[0] > 4000: return
        open_ = [k for k in star if len(d[k]) > 1]
        if not open_: sols.append([int(d[k][0]) for k in star]); return
        k = min(open_, key=lambda z: (len(d[z]), z))
        for c in d[k]:
            sub, _ = close(system, [x if j != k else [c] for j, x in enumerate(d)])
            if sub is not None: dfs(sub)
    dfs(dom); okfull = [bool(all(full[a, b][sa, sb] for (a, sa), (b, sb) in combinations(list(zip(star, s_)), 2))) for s_ in sols]
    rec["star_search"] = {"solutions_found": len(sols), "nodes": nodes[0], "cap_reached": len(sols) >= 20 or nodes[0] > 4000, "solutions": sols,
                          "solution_supports": [[[int(p) for p in np.flatnonzero(arrays[k][c])] for k, c in zip(star, s_)] for s_ in sols], "pass_full_pair_tables": okfull}
    out[ap] = rec; pv = rec["pivots"]
    print("apex %d, star %d: pivots [shadow, domain, survivors] %s | first pivot: immediate contradictions %d of %d, mean tight(cap) refuted %.1f / surviving %s | star search: %d assignment(s) with Green + sums, %d nodes%s; passing the FULL pair tables: %d  [%.0f s]" % (
        ap, S, [[p["shadow"], p["domain"], p["survivors"]] for p in pv], sum(1 for x in pv[0]["leaves"] if x["immediate"]), pv[0]["domain"],
        np.mean([x["tight_cap"] for x in pv[0]["leaves"] if not x["survives"]] or [0]), [x["tight_cap"] for x in pv[0]["leaves"] if x["survives"]],
        len(sols), nodes[0], " (cap reached)" if rec["star_search"]["cap_reached"] else "", sum(okfull), time.time() - t0), flush=True)
json.dump(out, open(sys.argv[3], "w"))
