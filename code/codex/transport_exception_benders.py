"""Lift shared-edge contradictions to exact linear cuts on all mask choices.

This is a bounded exploration of one star, not a complete exclusion run.
"""
import argparse
import json
from pathlib import Path
import time

import numpy as np
from ortools.sat.python import cp_model

from transport_exception_star import CASES, ROOT, setup, extension_model
from transport_exception_shared_edges import matrix, solve


def lift(b, core, selected, certificate):
    n = len(b)
    target = np.column_stack([14 - b.sum(axis=1), 2 - b - b @ core])
    d = np.column_stack([np.ones(n, dtype=np.int64), b])
    potentials = np.zeros((n, 25), dtype=np.int64)
    potentials[selected] = np.array(certificate["row_multipliers"], dtype=np.int64).reshape(75, 25)
    coeff = np.sum(potentials * target, axis=1)
    budget = target[:, 1:]
    allowed = ((b @ b.T <= 1) & (b @ (budget == 0).T == 0)
               & ((budget == 0) @ b.T == 0))
    costs = potentials @ d.T
    costs += costs.T.copy()
    marked = np.zeros(n, dtype=bool)
    marked[selected] = True
    for p, q in zip(*np.where(np.triu(allowed & (costs < 0), 1))):
        # e_pq <= x_endpoint; choose the zero endpoint at the current point.
        endpoint = q if marked[p] and not marked[q] else p
        coeff[endpoint] -= costs[p, q]
    value = int(coeff[selected].sum())
    assert value == certificate["target"] - certificate["box_lower_bound"] < 0
    return coeff, value


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--check", action="store_true", help="check archived cuts in integers, without a solver")
    ap.add_argument("--input", type=Path,
                    default=ROOT / "data/codex_transport_exception_shared_edges.json")
    ap.add_argument("--out", type=Path,
                    default=ROOT / "data/codex_transport_exception_benders.json")
    args = ap.parse_args()
    previous = json.loads(args.input.read_text(encoding="utf-8"))
    case, orbit = previous["case"], previous["orbit"]
    core, near, cells, orbits, _ = setup(*CASES[case])
    for i, j in sorted(orbits)[orbit]:
        core[i, j] = core[j, i] = 1
    b, m, rhs, _ = extension_model(core, near, cells, False)
    if args.check:
        archived = json.loads(args.out.read_text(encoding="utf-8"))
        assert (archived["case"], archived["orbit"]) == (case, orbit)
        for cut in archived["cuts"]:
            selected = np.array(cut["excluded_selected_indices"], dtype=int)
            assert len(selected) == 75 and len(set(selected)) == 75
            assert np.array_equal(m[:, selected].sum(axis=1), rhs)
            a, r, _ = matrix(core, b[selected])
            cert = cut["certificate"]
            y = np.array(cert["row_multipliers"], dtype=np.int64)
            lower = int(np.minimum(0, a.T @ y).sum())
            target = int(y @ r)
            assert lower == cert["box_lower_bound"] > target == cert["target"]
            coeff, value = lift(b, core, selected, cert)
            assert coeff.tolist() == cut["coefficients"] and value == cut["violation"]
        print("Exact archived cuts checked:", len(archived["cuts"]), "without solving")
        return
    lookup = {tuple(row): i for i, row in enumerate(b.tolist())}
    selected = np.array([lookup[tuple(row)] for row in previous["selected_masks"]], dtype=int)
    cert = previous["certificate"]
    model = cp_model.CpModel()
    xs = [model.new_bool_var(f"x{i}") for i in range(len(b))]
    for row, t in zip(m, rhs):
        model.add(sum(int(row[i]) * xs[i] for i in np.flatnonzero(row)) == int(t))
    for i, j in zip(*np.where(np.triu(b @ b.T > 2, 1))):
        model.add(xs[i] + xs[j] <= 1)
    report = {"case": case, "orbit": orbit, "scope": "bounded exact cut separation, star remains open",
              "cuts": [], "iterations": []}
    start = time.monotonic()
    for iteration in range(args.rounds):
        coeff, value = lift(b, core, selected, cert)
        model.add(sum(int(c) * x for c, x in zip(coeff, xs) if c) >= 0)
        report["cuts"].append({"coefficients": coeff.tolist(), "excluded_selected_indices": selected.tolist(),
                               "violation": value, "certificate": cert})
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 2
        solver.parameters.max_time_in_seconds = 10
        status = solver.solve(model)
        row = {"iteration": iteration, "master_status": solver.status_name(status)}
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            report["iterations"].append(row)
            print(row, flush=True)
            break
        selected = np.array([i for i, x in enumerate(xs) if solver.value(x)], dtype=int)
        assert np.array_equal(m[:, selected].sum(axis=1), rhs)
        for old_cut in report["cuts"]:
            assert sum(old_cut["coefficients"][i] for i in selected) >= 0
        a, r, _ = matrix(core, b[selected])
        cert = solve(a, r)
        row["shared_edge_status"] = cert["status"]
        row["elapsed_seconds"] = time.monotonic() - start
        report["iterations"].append(row)
        report["last_selected_indices"] = selected.tolist()
        report["last_shared_edge_result"] = cert
        args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(row, flush=True)
        if cert["status"] != "excluded_exact_selected_boundary":
            break
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
