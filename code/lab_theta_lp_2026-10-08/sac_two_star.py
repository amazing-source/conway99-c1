"""C1, lab session, 2026-10-08. Solver-free "assign one shadow, then propagate" certificates for a two-star branch.
  python sac_two_star.py <codex code/codex dir (commit 96e7f23)> <ball json | cyclic> <out json> <mode> <seconds per branch> <apex> [<apex> ...]
Motivation: with Codex's pair tables WITHOUT saturation (modes green / overlap / capacity) the pair-marginal LP is exactly
feasible, but adding the conditioned star sums makes it infeasible with every candidate individually excluded
(lifted_core.py). The discrete counterpart needs no LP: for a shadow i and a candidate c, fix i = c and run Codex's exact
propagation (pointwise star-sum bounds + pair supports) on the remaining domains; a contradiction deletes c. Repeat to
a fixed point. A branch is excluded when a domain becomes empty. Everything is integer and deterministic: the replay
is the recomputation (the deletion list is archived and compared). Pair tables: Codex's filtered_system(mode); nothing
is inherited from a stronger mode. One process, below 2 GB.
Positive control: PLANT=<seed> draws one candidate per shadow, redefines the star-sum targets as their sums and declares the
drawn pairs compatible; the procedure must then end alive with every drawn candidate still present."""
import sys, json, time, os
sys.path.insert(0, sys.argv[1])
from itertools import combinations
import numpy as np
from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
from joint_star_propagation import propagate, replay
from two_star_core_ablation import filtered_system
g0 = cyclic_ball() if sys.argv[2] == "cyclic" else json.load(open(sys.argv[2]))["adjacency"]; mode = sys.argv[4]; budget = float(sys.argv[5]); prepared = prepare(g0, 0, 12); out = {}
def restrict(system, dom):
    common, labels, arrays, sides, targets, compat = system
    return common, labels, [a[d] for a, d in zip(arrays, dom)], sides, targets, {(i, j): compat[i, j][np.ix_(dom[i], dom[j])] for i in range(18) for j in range(18) if i != j}
def close(system, dom):
    """Codex's propagation on the current domains; returns (new domains | None, contradiction)."""
    sub = restrict(system, dom); res = propagate(sub)
    if res["contradiction"] is not None: return None, res["contradiction"]
    alive = replay(sub, res); return [[d[k] for k in sorted(a)] for d, a in zip(dom, alive)], None
for ap in [int(a) for a in sys.argv[6:]]:
    t0 = time.time(); system = filtered_system(prepared, 0, 12, ap, mode); planted = None
    if os.environ.get("PLANT"):                                           # POSITIVE CONTROL: a planted integer solution must survive
        common, labels, arrays, sides, targets, compat = system; rng = np.random.default_rng(int(os.environ["PLANT"])); planted = [int(rng.integers(len(a))) for a in arrays]
        if os.environ.get("PLANT_TARGETS", "1") == "1": targets = [sum(arrays[i][planted[i]] for i in sides[s_]) for s_ in (0, 1)]
        for i, j in combinations(range(18), 2): compat[i, j][planted[i], planted[j]] = True; compat[j, i][planted[j], planted[i]] = True
        system = (common, labels, arrays, sides, targets, compat)
    dom = [list(range(len(a))) for a in system[2]]; dom, contra = close(system, dom); log = []; rounds = 0; status = None
    sizes0 = [len(d) for d in dom] if dom else None
    while dom is not None and status is None:
        rounds += 1; deleted = 0
        for i in sorted(range(18), key=lambda k: len(dom[k])):
            for c in list(dom[i]):
                if time.time() - t0 > budget: status = "BUDGET_REACHED"; break
                trial = [d if j != i else [c] for j, d in enumerate(dom)]; sub, why = close(system, trial)
                if sub is None: dom[i].remove(c); log.append([i, c]); deleted += 1
                if not dom[i]: break
            if status or not dom[i]: break
        if status: break
        if any(not d for d in dom): status = "EXCLUDED: empty domain of shadow %d after assign-and-propagate deletions" % [k for k, d in enumerate(dom) if not d][0]; break
        if deleted == 0: status = "FIXED_POINT_ALIVE"; break
        dom, contra = close(system, dom)
        if dom is None: status = "EXCLUDED: propagation contradiction after deletions (%s)" % contra.get("kind")
    if dom is None and status is None: status = "EXCLUDED: plain propagation (%s)" % contra.get("kind")
    out[ap] = {"mode": mode, "apex_index": ap, "common_apex_support": list(system[0]), "domain_sizes_after_plain_propagation": sizes0, "rounds": rounds, "deletions": log,
               "status": status, "final_domain_sizes": [len(d) for d in dom] if dom else None, "seconds": round(time.time() - t0, 1)}
    if planted is not None: print("   positive control: planted candidates still present: %s" % (dom is not None and all(planted[i] in dom[i] for i in range(18))))
    print("apex %d, mode %s: %s; plain propagation leaves %s candidates; %d assign-and-propagate deletions in %d round(s); final sizes %s  [%.0f s]" % (
        ap, mode, status, sum(sizes0) if sizes0 else 0, len(log), rounds, out[ap]["final_domain_sizes"], time.time() - t0), flush=True)
json.dump(out, open(sys.argv[3], "w"))
