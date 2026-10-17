"""Separate exact neighbourhood-capacity inequalities on exceptional stars.

If mask p is present, its neighbours among the remaining vertices have
incidences D z = t_p with 0 <= z_j <= x_j. Hence, for every integer y,
sum_j min(0, y D_j) x_j <= y t_p. Adjacency-impossible j are omitted.
LP duals only propose y; the violated inequality is checked in integers.
These cuts constrain all completions, not just one assignment of masks.
"""
import argparse
import json
from pathlib import Path
import time

import numpy as np
from ortools.sat.python import cp_model
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, eye, hstack

from transport_exception_star import CASES, ROOT, setup, extension_model


def separate(d, target, selected):
    """Return an exact violated coefficient inequality, or None."""
    active = d[:, selected]
    k = active.shape[1]
    # min y.t + sum s, with s >= -D_j.y and s >= 0.
    result = linprog(np.r_[target, np.ones(k)],
                     A_ub=hstack([-csr_matrix(active.T), -eye(k)]),
                     b_ub=np.zeros(k),
                     bounds=[(-1, 1)] * len(target) + [(0, None)] * k,
                     method="highs")
    if not result.success or result.fun >= -1e-7:
        return None
    for scale in (1, 10, 100, 1000, 10000, 1000000):
        y = np.rint(result.x[:len(target)] * scale).astype(np.int64)
        coeff = np.minimum(0, y @ d)
        rhs = int(y @ target)
        if int(coeff[selected].sum()) > rhs:
            return y, coeff, rhs
    raise RuntimeError("Floating separator not converted to exact inequality")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--case", type=int, choices=range(3), default=0)
    ap.add_argument("--orbit", type=int, default=0)
    ap.add_argument("--rounds", type=int, default=20)
    ap.add_argument("--seconds", type=float, default=10)
    ap.add_argument("--out", type=Path,
                    default=ROOT / "data/codex_transport_exception_capacity.json")
    args = ap.parse_args()
    core, near, cells, orbits, _ = setup(*CASES[args.case])
    matching = sorted(orbits)[args.orbit]
    for i, j in matching:
        core[i, j] = core[j, i] = 1
    b, m, rhs, _ = extension_model(core, near, cells, False)
    n = len(b)
    budget = 2 - b - b @ core
    can1 = ((b @ b.T <= 1) & (b @ (budget == 0).T == 0)
            & ((budget == 0) @ b.T == 0))
    np.fill_diagonal(can1, False)
    model = cp_model.CpModel()
    xs = [model.new_bool_var(f"x_{i}") for i in range(n)]
    for row, target in zip(m, rhs):
        model.add(sum(int(row[i]) * xs[i] for i in np.flatnonzero(row)) == int(target))
    for i, j in zip(*np.where(np.triu(b @ b.T > 2, 1))):
        model.add(xs[i] + xs[j] <= 1)
    report = {"case": args.case, "orbit": args.orbit, "matching": matching,
              "scope": "exact necessary neighbourhood-capacity cuts; not a graph",
              "rounds": [], "cuts": []}
    start = time.monotonic()
    for iteration in range(args.rounds):
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 2
        solver.parameters.max_time_in_seconds = args.seconds
        status = solver.solve(model)
        row = {"iteration": iteration, "status": solver.status_name(status),
               "solve_seconds": solver.wall_time}
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            report["rounds"].append(row)
            print(row, flush=True)
            break
        selected = np.array([i for i in range(n) if solver.value(xs[i])], dtype=int)
        assert len(selected) == 75 and np.array_equal(m[:, selected].sum(axis=1), rhs)
        cuts = 0
        for p in selected:
            available = np.flatnonzero(can1[p])
            chosen = np.flatnonzero(np.isin(available, selected))
            d = np.vstack([np.ones(len(available), dtype=np.int64), b[available].T])
            target = np.r_[14 - b[p].sum(), budget[p]]
            cut = separate(d, target, chosen)
            if cut is None:
                continue
            y, coeff, bound = cut
            model.add(sum(int(c) * xs[int(j)] for c, j in zip(coeff, available) if c)
                      <= bound).only_enforce_if(xs[int(p)])
            report["cuts"].append({"mask_index": int(p), "y": y.tolist(), "rhs": bound,
                                   "violating_selection": selected.tolist()})
            cuts += 1
        row["new_exact_cuts"] = cuts
        row["elapsed_seconds"] = time.monotonic() - start
        report["rounds"].append(row)
        report["last_selected_masks"] = b[selected].tolist()
        args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(row, flush=True)
        if not cuts:
            report["local_neighbourhood_capacities_feasible"] = True
            break
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
