"""Exact real-projector filters on a generic two-star branch.

Q = 7 Pi = 3I + J/12 - A_F - N.T H_real^+ N is PSD of rank eight.
Apply its 1x1, 2x2, and common-apex 3x3 principal minor conditions
BEFORE propagation. This is an additional necessary condition, not a
uniform exclusion. Products and determinants use Python integers.
"""
import argparse
from itertools import combinations
import json
import math
from pathlib import Path

import highspy
import numpy as np
import sympy as sp

from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
from joint_star_propagation import propagate, replay
from joint_star_pair_lp import find_bounded_dual, verify_farkas
from two_star_core_ablation import (MODES, filtered_system, core_matrix,
    numerical_primal, rational_primal, verify_fractional)


LEVELS = ("diagonal", "apex", "pairs", "triples")


def exact_green(prepared):
    g, green, k = prepared[:3]
    h = 3*sp.eye(36)-sp.Matrix(g.tolist())
    j = sp.ones(36)
    hp = 36*(36*h+j).inv(method="DM")-j/36
    assert hp == hp.T and h*hp == sp.eye(36)-j/36
    assert hp*sp.ones(36, 1) == sp.zeros(36, 1)
    denominator = math.lcm(*(int(x.q) for x in hp))
    numerator = np.array([[int(hp[p, q]*denominator) for q in range(36)]
                          for p in range(36)], dtype=object)
    assert denominator % 7 != 0
    assert np.array_equal(np.asarray(numerator % 7, dtype=np.int64)*pow(denominator, -1, 7) % 7, green)
    assert sum(int((numerator@k)[p, p]) for p in range(36)) == 129*denominator
    return numerator, denominator


def real_system(prepared, u, v, apex, mode, level, green_data=None):
    system = filtered_system(prepared, u, v, apex, mode)
    common, labels, arrays, sides, targets, compat = system
    numerator, denominator = exact_green(prepared) if green_data is None else green_data
    w = np.array([int(p in common) for p in range(36)], dtype=object)
    qw = int(37*denominator-12*(w@numerator@w))
    metadata = {"green_denominator": denominator, "q_scale": 12*denominator,
                "scaled_apex_diagonal": qw, "original_domain_sizes": [len(a) for a in arrays]}
    if qw < 0:
        metadata["apex_contradiction"] = "negative projector diagonal"
        return None, metadata
    energy, toward_w, keep, rejected_norm, rejected_apex = [], [], [], [], []
    for arr in arrays:
        diag = [int(37*denominator-12*(n@numerator@n)) for n in arr]
        cross = [int(denominator-12*(n@numerator@w)) for n in arr]
        bad_diag = [c for c in range(len(arr)) if diag[c] < 0]
        bad_apex = [c for c in range(len(arr)) if diag[c] >= 0 and qw*diag[c]-cross[c]**2 < 0]
        good = [c for c in range(len(arr)) if diag[c] >= 0 and
                (level == "diagonal" or qw*diag[c]-cross[c]**2 >= 0)]
        keep.append(good)
        energy.append([diag[c] for c in good]); toward_w.append([cross[c] for c in good])
        rejected_norm.append(bad_diag); rejected_apex.append(bad_apex if level != "diagonal" else [])
    reduced = [a[indices] for a, indices in zip(arrays, keep)]
    new_compat, counts = {}, {"before_real_pair_filter": 0, "after_two_by_two": 0, "after_three_by_three": 0}
    for i, j in combinations(range(18), 2):
        good = compat[i, j][np.ix_(keep[i], keep[j])].copy()
        counts["before_real_pair_filter"] += int(good.sum())
        if LEVELS.index(level) >= LEVELS.index("pairs"):
            edge = 3-(reduced[i]@prepared[1]@reduced[j].T) % 7
            products = reduced[i]@numerator@reduced[j].T
            for c, d in zip(*np.nonzero(good)):
                qij = int(denominator*(1-12*int(edge[c, d]))-12*int(products[c, d]))
                if energy[i][c]*energy[j][d]-qij*qij < 0:
                    good[c, d] = False
        counts["after_two_by_two"] += int(good.sum())
        if level == "triples":
            for c, d in zip(*np.nonzero(good)):
                qi, qj, qiw, qjw = energy[i][c], energy[j][d], toward_w[i][c], toward_w[j][d]
                qij = int(denominator*(1-12*int(edge[c, d]))-12*int(products[c, d]))
                det = qw*qi*qj+2*qiw*qjw*qij-qw*qij*qij-qi*qjw*qjw-qj*qiw*qiw
                if det < 0:
                    good[c, d] = False
        counts["after_three_by_three"] += int(good.sum())
        new_compat[i, j], new_compat[j, i] = good, good.T
    metadata.update({"rejected_diagonal_indices": rejected_norm, "rejected_apex_pair_indices": rejected_apex,
                     "retained_original_indices": keep, "domain_sizes_before_propagation": [len(a) for a in reduced],
                     "pair_counts": counts})
    return (common, labels, reduced, sides, targets, new_compat), metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ball", type=Path)
    parser.add_argument("--u", type=int, default=0)
    parser.add_argument("--v", type=int, default=12)
    parser.add_argument("--apex", type=int, default=0)
    parser.add_argument("--mode", choices=MODES, default="green")
    parser.add_argument("--level", choices=LEVELS, default="triples")
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--rational-witness", action="store_true")
    parser.add_argument("--propagation-only", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.verify_only:
        report = json.loads(args.out.read_text(encoding="utf-8"))
        g, (u, v), apex, mode, level = (report["adjacency"], report["centers"], report["apex_index"],
                                      report["pair_mode"], report["real_level"])
    else:
        g = json.loads(args.ball.read_text(encoding="utf-8"))["adjacency"] if args.ball else cyclic_ball()
        u, v, apex, mode, level = args.u, args.v, args.apex, args.mode, args.level
    prepared = prepare(g, u, v)
    system, geometry = real_system(prepared, u, v, apex, mode, level)
    if args.verify_only:
        assert geometry == report["geometry"]
    else:
        report = {"ball": str(args.ball) if args.ball else "cyclic(2,4,1)", "adjacency": np.asarray(g).tolist(),
                  "centers": [u, v], "apex_index": apex, "common_apex_support": list(prepared[6][apex]),
                  "pair_mode": mode, "real_level": level, "geometry": geometry,
                  "scope": "one generic rank-37 branch; exact real PSD filters before propagation; no uniform exclusion"}
        print(json.dumps({"mode": mode, "level": level, "apex": apex,
                          "domains": geometry.get("domain_sizes_before_propagation"),
                          "pairs": geometry.get("pair_counts")}), flush=True)
    if system is None:
        report["conclusion"] = "EXACT_APEX_NORM_CONTRADICTION"
    else:
        reduction = report["propagation"] if args.verify_only else propagate(system)
        replay(system, reduction)
        report["propagation"] = reduction
        if reduction["contradiction"] is not None:
            report["conclusion"] = "EXACT_PROPAGATION_CONTRADICTION"
        elif args.propagation_only or (args.verify_only and report["conclusion"] == "PROPAGATION_SURVIVES"):
            report["conclusion"] = "PROPAGATION_SURVIVES"
        else:
            matrix, rhs, names, metadata = core_matrix(system, reduction)
            if args.verify_only:
                assert metadata == report["matrix"]
                if report.get("fractional_witness"):
                    check = verify_fractional(matrix, rhs, report["fractional_witness"])
                else:
                    check = verify_farkas(matrix, rhs, rhs, names, report["farkas_certificate"])
                assert check == report["exact_check"]
            else:
                report["matrix"] = metadata
                status, seconds, numerical = numerical_primal(matrix, rhs, args.seconds)
                report["primal_diagnostic"] = {"status": str(status), "seconds": seconds}
                report["conclusion"] = "NUMERICAL_DIAGNOSTIC_ONLY"
                if status == highspy.HighsModelStatus.kInfeasible:
                    cert, check, diagnostic = find_bounded_dual(matrix, rhs, rhs, names, args.seconds, False)
                    report["farkas_certificate"], report["exact_check"], report["dual_diagnostic"] = cert, check, diagnostic
                    if cert:
                        report["conclusion"] = "EXACT_CORE_LP_CONTRADICTION"
                elif status == highspy.HighsModelStatus.kOptimal and args.rational_witness:
                    witness, check = rational_primal(system, reduction, matrix, rhs, names, numerical, args.seconds)
                    report["fractional_witness"], report["exact_check"] = witness, check
                    if witness:
                        report["conclusion"] = "EXACT_FRACTIONAL_CORE_WITNESS_NOT_A_GRAPH"
    if not args.verify_only:
        args.out.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("apex_index", "pair_mode", "real_level", "conclusion", "exact_check") if k in report}), flush=True)


if __name__ == "__main__":
    main()
