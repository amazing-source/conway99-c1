"""C1, lab session, 2026-10-08. Comparison asked by Codex (20:07 UTC): capacity mode + internal collisions only.
  python capacity_collision.py <codex code/codex dir (commit 96e7f23)> <ball json | cyclic> <out dir> <base mode> <apex> [<apex> ...]
Pair tables: Codex's `filtered_system(<base mode>)` (green / overlap / capacity: NO saturation), then, for two shadows i, j
of the SAME star s only, forbid a common point p with t_s(p) = 1 (t_s = K e_centre - w): two shadows of one star cannot
both cover a coordinate whose residual star sum is one. This is the internal K filter of Codex's note 214, added directly
to the base mode. Propagation redone with these tables (Codex's propagate / replay); LP = domains + pair marginals +
pointwise star sums (Codex's core_matrix). Infeasible: exact integer Farkas (find_bounded_dual / verify_farkas).
Feasible: exact rational witness (Codex's rational_primal / verify_fractional). Everything archived in full."""
import sys, json, time
sys.path.insert(0, sys.argv[1])
from itertools import combinations
import numpy as np
import highspy
from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
from joint_star_propagation import propagate, replay
from joint_star_pair_lp import find_bounded_dual, verify_farkas
from two_star_core_ablation import filtered_system, core_matrix, numerical_primal, rational_primal
g0 = cyclic_ball() if sys.argv[2] == "cyclic" else json.load(open(sys.argv[2]))["adjacency"]; base = sys.argv[4]; prepared = prepare(g0, 0, 12)
tag = "cyclic241" if sys.argv[2] == "cyclic" else sys.argv[2].replace("\\", "/").split("/")[-1].replace(".json", "")
for ap in [int(a) for a in sys.argv[5:]]:
    t0 = time.time(); common, labels, arrays, sides, targets, compat = filtered_system(prepared, 0, 12, ap, base); removed = 0
    for s in (0, 1):
        P = np.flatnonzero(np.asarray(targets[s]) == 1)
        for i, j in combinations(sides[s], 2):
            good = compat[i, j] & (arrays[i][:, P] @ arrays[j][:, P].T == 0); removed += int(compat[i, j].sum() - good.sum()); compat[i, j], compat[j, i] = good, good.T
    system = (common, labels, arrays, sides, targets, compat); result = propagate(system); replay(system, result)
    rec = {"ball": tag, "adjacency": np.asarray(g0).tolist(), "centers": [0, 12], "apex_index": ap, "common_apex_support": list(common), "base_mode": base,
           "extra_filter": "same-star pairs: no common point p with t_s(p) = 1", "pairs_removed_by_extra_filter": removed, "propagation": result}
    if result["contradiction"] is not None: rec["conclusion"] = "EXACT_PROPAGATION_CONTRADICTION"
    else:
        matrix, rhs, names, meta = core_matrix(system, result); rec["matrix"] = meta
        status, secs, numerical = numerical_primal(matrix, rhs, 45); rec["primal_diagnostic"] = {"status": str(status), "seconds": secs}; rec["conclusion"] = "NUMERICAL_DIAGNOSTIC_ONLY"
        if status == highspy.HighsModelStatus.kInfeasible:
            cert, check, diag = find_bounded_dual(matrix, rhs, rhs, names, 45, False); rec["dual_diagnostic"] = diag
            if cert: rec.update({"farkas_certificate": cert, "exact_check": verify_farkas(matrix, rhs, rhs, names, cert), "conclusion": "EXACT_CORE_LP_CONTRADICTION"})
        elif status == highspy.HighsModelStatus.kOptimal:
            witness, check = rational_primal(system, result, matrix, rhs, names, numerical, 60)
            if witness: rec.update({"fractional_witness": witness, "exact_check": check, "conclusion": "EXACT_FRACTIONAL_CORE_WITNESS_NOT_A_GRAPH"})
    json.dump(rec, open("%s/core_%s_plus_internal_collision_%s_apex%d.json" % (sys.argv[3], base, tag, ap), "w"))
    print("apex %d, %s + internal collisions (pairs removed %d): %s %s %s  [%.0f s]" % (ap, base, removed, rec["conclusion"], rec.get("matrix", {}).get("remaining_domain_sizes", ""),
          {k: v for k, v in (rec.get("exact_check") or {}).items() if k in ("contradiction_gap", "denominator", "positive_variables", "equalities_verified")}, time.time() - t0), flush=True)
