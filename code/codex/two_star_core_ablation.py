"""Remove pair filters BEFORE propagation; solve only the two-star core LP.

Unary pools and the common-apex filters stay unchanged. Every mode rebuilds
its own propagated domains. Only domain, marginal and pointwise star-sum
equalities are present in the LP. Numerical feasibility is not an exact
primal certificate; infeasibility is claimed only after integer Farkas replay.
"""
import argparse
from itertools import combinations
import json
import math
from pathlib import Path
import time

import highspy
import numpy as np
from scipy.sparse import coo_matrix
from ortools.sat.python import cp_model
from ortools.graph.python import max_flow

from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
from joint_star_propagation import setup, propagate, replay
from joint_star_pair_lp import find_bounded_dual, verify_farkas


MODES = ("green", "overlap", "capacity", "saturation", "within", "across", "full")


def filtered_system(prepared, u, v, apex, mode):
    system = setup(prepared, u, v, apex)
    if mode == "full":
        return system
    common, labels, arrays, sides, targets, full_compat = system
    g, green = prepared[:2]
    compat = {}
    for i, j in combinations(range(18), 2):
        ni, nj = arrays[i], arrays[j]
        edge = 3-(ni@green@nj.T) % 7
        good = (edge == 0) | (edge == 1)
        if MODES.index(mode) >= MODES.index("overlap"):
            good &= ni@nj.T <= 2-edge
        if MODES.index(mode) >= MODES.index("capacity"):
            si, sj = labels[i][0], labels[j][0]
            cap_i = (1 if si == sj else 2)-ni@g[(u, v)[sj]]
            cap_j = (1 if si == sj else 2)-nj@g[(u, v)[si]]
            good &= (edge <= cap_i[:, None]) & (edge <= cap_j[None, :])
        if MODES.index(mode) >= MODES.index("saturation"):
            sat_i, sat_j = (ni@g+ni == 2).astype(np.int64), (nj@g+nj == 2).astype(np.int64)
            good &= (edge == 0) | ((sat_i@nj.T == 0) & (ni@sat_j.T == 0))
        if ((mode == "within" and labels[i][0] == labels[j][0])
                or (mode == "across" and labels[i][0] != labels[j][0])):
            good &= full_compat[i, j]
        assert np.all(good | ~full_compat[i, j]), "weakened table must contain the full table"
        compat[i, j], compat[j, i] = good, good.T
    return common, labels, arrays, sides, targets, compat


def core_matrix(system, result):
    alive = replay(system, result)
    assert result["contradiction"] is None
    common, labels, arrays, sides, targets, compat = system
    kept = [sorted(a) for a in alive]
    arrays = [a[k] for a, k in zip(arrays, kept)]
    x, count = [], 0
    for arr in arrays:
        x.append(np.arange(count, count+len(arr)))
        count += len(arr)
    unary_count = count
    pairs = {}
    for i, j in combinations(range(18), 2):
        left, right = np.nonzero(compat[i, j][np.ix_(kept[i], kept[j])])
        pairs[i, j] = left, right, np.arange(count, count+len(left))
        count += len(left)
    rr, cc, vv, rhs, names = [], [], [], [], []

    def row(terms, target, name):
        for cols, values in terms:
            for col, value in zip(cols, values):
                if value:
                    rr.append(len(rhs)); cc.append(int(col)); vv.append(int(value))
        rhs.append(int(target)); names.append(name)

    for i, cols in enumerate(x):
        row([(cols, [1]*len(cols))], 1, f"domain:{i}")
    for (i, j), (left, right, cols) in pairs.items():
        for var, choices in ((i, left), (j, right)):
            for c, xc in enumerate(x[var]):
                selected = cols[choices == c]
                row([(selected, [1]*len(selected)), ([xc], [-1])], 0, f"marginal:{i}:{j}:{var}:{c}")
    for side, indices in enumerate(sides):
        for p in range(36):
            row([(x[i], arrays[i][:, p]) for i in indices], targets[side][p], f"star_sum:{side}:{p}")
    matrix = coo_matrix((vv, (rr, cc)), shape=(len(rhs), count), dtype=np.int64).tocsr()
    return matrix, np.array(rhs), names, {"unary_variables": unary_count,
        "pair_variables": count-unary_count, "constraints": len(rhs), "nonzero_coefficients": matrix.nnz,
        "remaining_domain_sizes": [len(a) for a in arrays]}


def numerical_primal(matrix, rhs, seconds):
    lp = highspy.HighsLp()
    lp.num_row_, lp.num_col_ = matrix.shape
    lp.col_cost_, lp.col_lower_, lp.col_upper_ = np.zeros(matrix.shape[1]), np.zeros(matrix.shape[1]), np.ones(matrix.shape[1])
    lp.row_lower_, lp.row_upper_ = rhs, rhs
    lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
    lp.a_matrix_.start_, lp.a_matrix_.index_, lp.a_matrix_.value_ = matrix.indptr, matrix.indices, matrix.data
    solver = highspy.Highs()
    for key, value in (("output_flag", False), ("solver", "ipm"), ("run_crossover", "off"), ("threads", 1), ("time_limit", seconds)):
        solver.setOptionValue(key, value)
    solver.passModel(lp); solver.run()
    return solver.getModelStatus(), solver.getRunTime(), solver.getSolution().col_value


def verify_fractional(matrix, rhs, witness):
    denominator = witness["denominator"]
    assert type(denominator) is int and denominator > 0
    mass = [0]*matrix.shape[1]
    seen = set()
    for col, value in witness["positive_masses"]:
        assert type(col) is int and 0 <= col < len(mass) and col not in seen
        assert type(value) is int and 0 < value <= denominator
        mass[col] = value; seen.add(col)
    for r in range(matrix.shape[0]):
        total = sum(int(matrix.data[o])*mass[int(matrix.indices[o])]
                    for o in range(matrix.indptr[r], matrix.indptr[r+1]))
        assert total == denominator*int(rhs[r])
    return {"denominator": denominator, "positive_variables": len(seen),
            "equalities_verified": matrix.shape[0]}


def rational_primal(system, result, matrix, rhs, names, numerical, seconds):
    """Round unary masses subject to exact sums, then lift by integer flows.

    A failed flow supplies a Hall inequality to the unary rounding model.
    The final certificate is independently checked by integer matrix sums.
    """
    started = time.monotonic()
    alive = replay(system, result)
    kept = [sorted(a) for a in alive]
    offsets = np.cumsum([0]+[len(a) for a in kept]).tolist()
    unary_count = offsets[-1]
    compat = system[-1]
    for denominator, padding in ((100000, 2), (1000000, 5), (10000000, 10)):
        model = cp_model.CpModel()
        variables = [model.NewIntVar(max(0, math.floor(numerical[c]*denominator)-padding),
                         min(denominator, math.ceil(numerical[c]*denominator)+padding), f"mass_{c}")
                     for c in range(unary_count)]
        for r, name in enumerate(names):
            if name.startswith(("domain:", "star_sum:")):
                model.Add(sum(int(matrix.data[o])*variables[int(matrix.indices[o])]
                              for o in range(matrix.indptr[r], matrix.indptr[r+1])) == denominator*int(rhs[r]))
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = min(10, seconds)
        for iteration in range(20):
            remaining = seconds-(time.monotonic()-started)
            if remaining <= 0:
                return None, None
            solver.parameters.max_time_in_seconds = min(10, remaining)
            status = solver.Solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                break
            mass = [solver.Value(var) for var in variables]+[0]*(matrix.shape[1]-unary_count)
            col_offset, failed = unary_count, False
            for i, j in combinations(range(18), 2):
                good = compat[i, j][np.ix_(kept[i], kept[j])]
                left, right = np.nonzero(good)
                ni, nj = good.shape
                src, dst = 0, ni+nj+1
                flow = max_flow.SimpleMaxFlow()
                for c in range(ni):
                    flow.add_arc_with_capacity(src, 1+c, mass[offsets[i]+c])
                arcs = [flow.add_arc_with_capacity(1+int(c), 1+ni+int(d), denominator)
                        for c, d in zip(left, right)]
                for d in range(nj):
                    flow.add_arc_with_capacity(1+ni+d, dst, mass[offsets[j]+d])
                flow_status = flow.solve(src, dst)
                assert flow_status == flow.OPTIMAL
                if flow.optimal_flow() != denominator:
                    reachable = set(map(int, flow.get_source_side_min_cut()))
                    ls = [c for c in range(ni) if 1+c in reachable]
                    rs = [d for d in range(nj) if 1+ni+d in reachable]
                    assert all(not good[c, d] or d in rs for c in ls for d in range(nj))
                    model.Add(sum(variables[offsets[i]+c] for c in ls)
                              <= sum(variables[offsets[j]+d] for d in rs))
                    failed = True
                    break
                for k, arc in enumerate(arcs):
                    mass[col_offset+k] = int(flow.flow(arc))
                col_offset += len(arcs)
            if not failed:
                assert col_offset == matrix.shape[1]
                witness = {"denominator": denominator,
                           "positive_masses": [[c, int(value)] for c, value in enumerate(mass) if value]}
                return witness, verify_fractional(matrix, rhs, witness)
    return None, None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ball", type=Path)
    parser.add_argument("--u", type=int, default=0)
    parser.add_argument("--v", type=int, default=12)
    parser.add_argument("--apex", type=int, default=0)
    parser.add_argument("--mode", choices=MODES, default="green")
    parser.add_argument("--seconds", type=float, default=45)
    parser.add_argument("--rational-witness", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        report = json.loads(args.out.read_text(encoding="utf-8"))
        g, (u, v), apex, mode = report["adjacency"], report["centers"], report["apex_index"], report["pair_mode"]
    else:
        g = json.loads(args.ball.read_text(encoding="utf-8"))["adjacency"] if args.ball else cyclic_ball()
        u, v, apex, mode = args.u, args.v, args.apex, args.mode
    system = filtered_system(prepare(g, u, v), u, v, apex, mode)
    if args.verify_only:
        result = report["propagation"]
        replay(system, result)
    else:
        result = propagate(system)
        replay(system, result)
        report = {"ball": str(args.ball) if args.ball else "cyclic(2,4,1)",
            "adjacency": np.asarray(g).tolist(), "centers": [u, v], "apex_index": apex,
            "common_apex_support": list(system[0]), "pair_mode": mode,
            "initial_domain_sizes": [len(a) for a in system[2]], "propagation": result,
            "scope": "one branch; unchanged unary and common-apex filters; propagation uses this pair mode"}
    assert report["common_apex_support"] == list(system[0])
    if result["contradiction"] is not None:
        report["conclusion"] = "EXACT_PROPAGATION_CONTRADICTION"
    else:
        matrix, rhs, names, metadata = core_matrix(system, result)
        if args.verify_only:
            assert report["matrix"] == metadata
            if report.get("fractional_witness"):
                check = verify_fractional(matrix, rhs, report["fractional_witness"])
            else:
                check = verify_farkas(matrix, rhs, rhs, names, report["farkas_certificate"])
            assert check == report["exact_check"]
        else:
            report["matrix"] = metadata
            print(json.dumps({"mode": mode, "apex": apex, **metadata}), flush=True)
            status, seconds, numerical = numerical_primal(matrix, rhs, args.seconds)
            report["solver_version"] = highspy.Highs().version()
            report["primal_diagnostic"] = {"status": str(status), "seconds": seconds}
            report["conclusion"] = "NUMERICAL_DIAGNOSTIC_ONLY"
            if status == highspy.HighsModelStatus.kInfeasible:
                certificate, check, diagnostic = find_bounded_dual(matrix, rhs, rhs, names, args.seconds, False)
                report["farkas_certificate"], report["exact_check"], report["dual_diagnostic"] = certificate, check, diagnostic
                if certificate:
                    report["conclusion"] = "EXACT_CORE_LP_CONTRADICTION"
            elif status == highspy.HighsModelStatus.kOptimal and args.rational_witness:
                witness, check = rational_primal(system, result, matrix, rhs, names, numerical, args.seconds)
                report["fractional_witness"], report["exact_check"] = witness, check
                if witness:
                    report["conclusion"] = "EXACT_FRACTIONAL_CORE_WITNESS_NOT_A_GRAPH"
    if not args.verify_only:
        args.out.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("pair_mode", "apex_index", "conclusion", "primal_diagnostic", "exact_check") if k in report}), flush=True)


if __name__ == "__main__":
    main()
