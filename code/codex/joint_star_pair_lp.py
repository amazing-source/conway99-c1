"""Pair-marginal LP relaxation of a fixed two-star common-apex branch.

Candidate pairs retain their exact mod-7 compatibility tables. Floating
solver outcomes are diagnostic; only the integer Farkas verifier certifies
infeasibility. This script makes no uniform or full-ball exclusion claim.
"""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
import math
from pathlib import Path

import highspy
import numpy as np
from scipy.sparse import coo_matrix, eye, hstack

from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
from joint_star_propagation import setup, propagate, replay


def build(prepared, u, v, apex, lift_sums=False):
    system = setup(prepared, u, v, apex)
    reduction = propagate(system)
    alive = replay(system, reduction)
    assert reduction["contradiction"] is None, "branch already has a propagation certificate"
    common, labels, all_arrays, sides, targets, compat = system
    g, green, k, c4, *_ = prepared
    kept = [sorted(a) for a in alive]
    arrays = [a[indices] for a, indices in zip(all_arrays, kept)]
    gn = [a@g for a in arrays]
    w = np.array([int(p in common) for p in range(36)], dtype=np.int64)
    x, count = [], 0
    for arr in arrays:
        x.append(np.arange(count, count+len(arr)))
        count += len(arr)
    unary_count = count
    pairs = {}
    for i, j in combinations(range(18), 2):
        good = compat[i, j][np.ix_(kept[i], kept[j])]
        left, right = np.nonzero(good)
        edge = 3-(arrays[i]@green@arrays[j].T)[left, right] % 7
        cols = np.arange(count, count+len(left))
        pairs[i, j] = (left, right, edge, cols)
        count += len(cols)
    rr, cc, vv, lower, upper, names = [], [], [], [], [], []

    def row(terms, rhs, name, equality=True):
        combined = {}
        for cols, values in terms:
            for col, value in zip(cols, values):
                if value:
                    c = int(col)
                    combined[c] = combined.get(c, 0)+int(value)
        for col, value in combined.items():
            if value:
                rr.append(len(names)); cc.append(col); vv.append(value)
        lower.append(int(rhs) if equality else -math.inf)
        upper.append(int(rhs))
        names.append(name)

    for i, cols in enumerate(x):
        row([(cols, np.ones(len(cols), dtype=np.int64))], 1, f"domain:{i}")
    for (i, j), (left, right, edge, cols) in pairs.items():
        for var, choices in ((i, left), (j, right)):
            for c, xc in enumerate(x[var]):
                selected = cols[choices == c]
                row([(selected, np.ones(len(selected), dtype=np.int64)), ([xc], [-1])],
                    0, f"marginal:{i}:{j}:{var}:{c}")
    for side, indices in enumerate(sides):
        for p in range(36):
            row([(x[i], arrays[i][:, p]) for i in indices], targets[side][p], f"star_sum:{side}:{p}")
    for p, q in combinations(range(36), 2):
        row([(x[i], a[:, p]*a[:, q]) for i, a in enumerate(arrays)],
            k[p, q]-w[p]*w[q], f"near_pair:{p}:{q}", False)
    for i in range(18):
        side = labels[i][0]
        for other_side in (0, 1):
            terms = []
            for j in sides[other_side]:
                if i != j:
                    left, right, edge, cols = pairs[min(i, j), max(i, j)]
                    terms.append((cols, edge))
            capacity = (1 if side == other_side else 2)-gn[i][:, (u, v)[other_side]]
            row(terms+[(x[i], -capacity)], 0, f"degree:{i}:{other_side}")
        for p in range(36):
            terms = [(x[i], arrays[i][:, p]+gn[i][:, p])]
            for j in range(18):
                if j == i:
                    continue
                left, right, edge, cols = pairs[min(i, j), max(i, j)]
                other_choice = right if i < j else left
                terms.append((cols, edge*arrays[j][other_choice, p]))
            row(terms, 2, f"near_far:{i}:{p}", False)
    for a, b in combinations(sides[0], 2):
        for c, d in combinations(sides[1], 2):
            for ac, bd in (((a, c), (b, d)), ((a, d), (b, c))):
                terms = [(pairs[i, j][3], pairs[i, j][2]) for i, j in ((a, b), (c, d), ac, bd)]
                row(terms, 3, f"no_prism:{a}:{b}:{ac[1]}:{bd[1]}", False)
    if lift_sums:
        # Multiply each exact star-sum equation by the indicator that
        # variable i chooses c, then replace products by pair marginals.
        for i in range(18):
            for c, xc in enumerate(x[i]):
                for side, indices in enumerate(sides):
                    for p in range(36):
                        terms = [([xc], [int(arrays[i][c, p])*(i in indices)-targets[side][p]])]
                        for j in indices:
                            if j == i:
                                continue
                            left, right, edge, cols = pairs[min(i, j), max(i, j)]
                            own, other = (left, right) if i < j else (right, left)
                            mask = own == c
                            terms.append((cols[mask], arrays[j][other[mask], p]))
                        row(terms, 0, f"lifted_star:{i}:{c}:{side}:{p}")
    matrix = coo_matrix((vv, (rr, cc)), shape=(len(names), count), dtype=np.int64).tocsr()
    return matrix, np.array(lower), np.array(upper), names, {
        "common_apex_support": list(common), "unary_variables": unary_count,
        "pair_variables": count-unary_count, "constraints": len(names),
        "nonzero_coefficients": matrix.nnz, "lifted_star_sums": lift_sums,
        "variable_bounds": [0, 1],
        "propagated_domain_sizes": [len(a) for a in arrays]}


def verify_farkas(matrix, lower, upper, names, certificate):
    """Integer-only Farkas check including the explicit bounds 0<=x<=1.

    A weighted row sum Cx<=rhs contradicts Cx>=sum(min(C_j,0)).
    All candidate and pair weights are probabilities, so these upper
    bounds also follow from domain normalization and pair marginals.
    """
    total = {}
    rhs = 0
    seen = set()
    for entry in certificate:
        r, multiplier = entry["row"], entry["multiplier"]
        assert isinstance(r, int) and isinstance(multiplier, int) and multiplier != 0
        assert 0 <= r < len(names) and r not in seen and names[r] == entry["name"]
        seen.add(r)
        assert math.isfinite(float(upper[r]))
        assert lower[r] == upper[r] or multiplier >= 0
        rhs += multiplier*int(upper[r])
        for offset in range(matrix.indptr[r], matrix.indptr[r+1]):
            col, value = int(matrix.indices[offset]), int(matrix.data[offset])
            total[col] = total.get(col, 0)+multiplier*value
    bound = sum(min(value, 0) for value in total.values())
    assert rhs < bound
    return {"weighted_rhs": rhs, "nonzero_rows": len(certificate),
            "box_lower_bound": bound, "contradiction_gap": bound-rhs,
            "positive_columns": sum(value > 0 for value in total.values()),
            "negative_columns": sum(value < 0 for value in total.values())}


def rational_certificate(ray, matrix, lower, upper, names):
    if len(ray) != len(names) or not np.all(np.isfinite(ray)) or not np.any(ray):
        return None, None
    # Rounded dual weights plus exact variable bounds absorb tiny floating
    # residuals. The returned proof is checked entirely with Python ints.
    for scale in (10**3, 10**6, 10**9, 10**12):
        for sign in (1, -1):
            normalized = sign*np.asarray(ray)/np.max(np.abs(ray))*scale
            ints = [round(float(value)) for value in normalized]
            ints = [value if lower[r] == upper[r] else max(0, value) for r, value in enumerate(ints)]
            divisor = math.gcd(*ints)
            if not divisor:
                continue
            cert = [{"row": r, "name": names[r], "multiplier": value//divisor}
                    for r, value in enumerate(ints) if value]
            try:
                return cert, verify_farkas(matrix, lower, upper, names, cert)
            except AssertionError:
                pass
    for max_denominator in (1, 10, 100, 1000, 10000, 1000000):
        fractions = [Fraction(float(value)).limit_denominator(max_denominator) for value in ray]
        scale = math.lcm(*(f.denominator for f in fractions))
        ints = [int(f*scale) for f in fractions]
        divisor = math.gcd(*ints)
        if not divisor:
            continue
        for sign in (1, -1):
            cert = [{"row": r, "name": names[r], "multiplier": sign*value//divisor}
                    for r, value in enumerate(ints) if value]
            try:
                check = verify_farkas(matrix, lower, upper, names, cert)
                return cert, check
            except AssertionError:
                pass
    return None, None


def find_bounded_dual(matrix, lower, upper, names, seconds, log):
    """Explicit dual search; even a non-optimal vector can yield an exact proof.

    Minimize b.lambda + sum(z), subject to A.T lambda + z >= 0,
    |lambda_eq|<=1, 0<=lambda_ineq<=1, z>=0. A negative value is a
    separating certificate for the primal box. No optimality is needed.
    """
    nr, nc = matrix.shape
    dual_matrix = hstack((matrix.T, eye(nc, format="csr")), format="csr")
    lp = highspy.HighsLp()
    lp.num_row_, lp.num_col_ = nc, nr+nc
    lp.col_cost_ = np.concatenate((upper, np.ones(nc)))
    lp.col_lower_ = np.concatenate((np.where(lower == upper, -1, 0), np.zeros(nc)))
    lp.col_upper_ = np.concatenate((np.ones(nr), np.full(nc, math.inf)))
    lp.row_lower_, lp.row_upper_ = np.zeros(nc), np.full(nc, math.inf)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_, lp.a_matrix_.index_, lp.a_matrix_.value_ = dual_matrix.indptr, dual_matrix.indices, dual_matrix.data
    solver = highspy.Highs()
    solver.setOptionValue("output_flag", log)
    solver.setOptionValue("solver", "ipm")
    solver.setOptionValue("run_crossover", "off")
    solver.setOptionValue("time_limit", seconds)
    solver.setOptionValue("threads", 1)
    solver.passModel(lp)
    solver.run()
    weights = solver.getSolution().col_value[:nr]
    cert, check = rational_certificate(weights, matrix, lower, upper, names)
    return cert, check, {"status": str(solver.getModelStatus()),
                         "seconds": solver.getRunTime(), "objective": solver.getObjectiveValue()}


def simplify_center_rows(certificate, names, u, v):
    """Replace redundant center inequalities by their exact equality rows.

    near_pair(center,p) is precisely star_sum(side,p).
    near_far(i,center) = degree(i,side) + 2*domain(i), with RHS 2.
    """
    index = {name: r for r, name in enumerate(names)}
    weights = Counter()
    for entry in certificate:
        name, value = entry["name"], entry["multiplier"]
        parts = name.split(":")
        if parts[0] == "near_far" and int(parts[2]) in (u, v):
            i, side = int(parts[1]), (u, v).index(int(parts[2]))
            weights[index[f"degree:{i}:{side}"]] += value
            weights[index[f"domain:{i}"]] += 2*value
        elif parts[0] == "near_pair" and any(int(p) in (u, v) for p in parts[1:]):
            p, q = map(int, parts[1:])
            center, other = (p, q) if p in (u, v) else (q, p)
            weights[index[f"star_sum:{(u, v).index(center)}:{other}"]] += value
        else:
            weights[entry["row"]] += value
    return [{"row": r, "name": names[r], "multiplier": value}
            for r, value in sorted(weights.items()) if value]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ball", type=Path)
    parser.add_argument("--u", type=int, default=0)
    parser.add_argument("--v", type=int, default=12)
    parser.add_argument("--apex", type=int, default=0)
    parser.add_argument("--lift-sums", action="store_true")
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--solver", choices=("simplex", "ipm"), default="ipm")
    parser.add_argument("--log", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    g0 = json.loads(args.ball.read_text(encoding="utf-8"))["adjacency"] if args.ball else cyclic_ball()
    prepared = prepare(g0, args.u, args.v)
    matrix, lower, upper, names, metadata = build(prepared, args.u, args.v, args.apex, args.lift_sums)
    report = {"ball": str(args.ball) if args.ball else "cyclic(2,4,1)", "centers": [args.u, args.v], "apex_index": args.apex,
              **metadata, "scope": "one fixed common-apex branch; no uniform exclusion"}
    print(json.dumps(report), flush=True)
    if args.verify_only:
        old = json.loads(args.out.read_text(encoding="utf-8"))
        assert all(old[key] == value for key, value in report.items())
        check = verify_farkas(matrix, lower, upper, names, old["farkas_certificate"])
        assert check == old["exact_check"]
        print(json.dumps({"verified": check}), flush=True)
        return
    lp = highspy.HighsLp()
    lp.num_col_, lp.num_row_ = matrix.shape[1], matrix.shape[0]
    lp.col_cost_ = np.zeros(matrix.shape[1])
    lp.col_lower_ = np.zeros(matrix.shape[1])
    lp.col_upper_ = np.ones(matrix.shape[1])
    lp.row_lower_, lp.row_upper_ = lower, upper
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_, lp.a_matrix_.index_, lp.a_matrix_.value_ = matrix.indptr, matrix.indices, matrix.data
    solver = highspy.Highs()
    solver.setOptionValue("output_flag", args.log)
    solver.setOptionValue("solver", args.solver)
    solver.setOptionValue("time_limit", args.seconds)
    solver.setOptionValue("threads", 1)
    solver.passModel(lp)
    run_status = solver.run()
    status = solver.getModelStatus()
    report["solver_status"] = str(status)
    report["solver_algorithm"] = args.solver
    report["run_status"] = str(run_status)
    report["solver_version"] = solver.version()
    report["solver_seconds"] = solver.getRunTime()
    if status == highspy.HighsModelStatus.kInfeasible:
        dual = solver.getSolution().row_dual
        cert, check = rational_certificate(dual, matrix, lower, upper, names)
        report["certificate_source"] = "row_dual"
        if cert is None:
            cert, check, diagnostic = find_bounded_dual(matrix, lower, upper, names, args.seconds, args.log)
            report["dual_search"] = diagnostic
            report["certificate_source"] = "bounded_dual_search"
        if cert is not None:
            cert = simplify_center_rows(cert, names, args.u, args.v)
            check = verify_farkas(matrix, lower, upper, names, cert)
            report["certificate_families"] = dict(Counter(e["name"].split(":")[0] for e in cert))
        report["farkas_certificate"], report["exact_check"] = cert, check
    report["conclusion"] = ("EXACT_BRANCH_CERTIFICATE" if report.get("exact_check")
                            else "NUMERICAL_DIAGNOSTIC_ONLY")
    args.out.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "farkas_certificate"}), flush=True)


if __name__ == "__main__":
    main()
