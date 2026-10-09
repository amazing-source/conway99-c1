"""Exact shared-edge capacity obstruction for a selected exceptional boundary.

The output excludes a selected boundary assignment only. It does not
exclude an exceptional star or one of the five dossier boundary cases.
"""
import argparse
import json
from pathlib import Path
import time

import highspy
import numpy as np
from scipy.sparse import coo_matrix

from transport_exception_star import CASES, ROOT, setup


def matrix(core, b):
    budget = 2 - b - b @ core
    can1 = ((b @ b.T <= 1) & (b @ (budget == 0).T == 0)
            & ((budget == 0) @ b.T == 0))
    edges = list(zip(*np.where(np.triu(can1, 1))))
    rows, columns = [], []
    for k, (i, j) in enumerate(edges):
        rows.extend([25 * i, 25 * j])
        columns.extend([k, k])
        for h in np.flatnonzero(b[j]):
            rows.append(25 * i + 1 + h)
            columns.append(k)
        for h in np.flatnonzero(b[i]):
            rows.append(25 * j + 1 + h)
            columns.append(k)
    m = coo_matrix((np.ones(len(rows), dtype=np.int64), (rows, columns)),
                   shape=(75 * 25, len(edges))).tocsr()
    rhs = np.column_stack([14 - b.sum(axis=1), budget]).ravel()
    return m, rhs, edges


def solve(m, rhs):
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("threads", 2)
    h.setOptionValue("solver", "simplex")
    h.setOptionValue("time_limit", 60.0)
    n = m.shape[1]
    h.addCols(n, np.zeros(n), np.zeros(n), np.ones(n), 0,
              np.zeros(n + 1, dtype=np.int32), np.array([], dtype=np.int32), np.array([]))
    h.addRows(len(rhs), rhs, rhs, m.nnz, m.indptr, m.indices, m.data)
    h.run()
    status = h.getModelStatus()
    if status != highspy.HighsModelStatus.kInfeasible:
        return {"status": h.modelStatusToString(status)}
    _, exists, ray = h.getDualRay()
    assert exists
    for sign in (1, -1):
        for scale in (1, 10, 100, 1000, 10000, 1000000):
            y = np.rint(sign * scale * ray).astype(np.int64)
            coeff = np.asarray(m.T @ y).ravel()
            lower = int(np.minimum(0, coeff).sum())
            target = int(y @ rhs)
            if lower > target:
                # With 0 <= e <= 1, y.M.e >= sum min(0,y.M), contradicting y.rhs.
                return {"status": "excluded_exact_selected_boundary",
                        "row_multipliers": y.tolist(), "box_lower_bound": lower,
                        "target": target, "nonzero_multipliers": int(np.count_nonzero(y)),
                        "max_multiplier": int(np.max(abs(y)))}
    raise RuntimeError("No exact integer certificate extracted from numerical ray")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path,
                    default=ROOT / "data/codex_transport_exception_capacity.json")
    ap.add_argument("--out", type=Path,
                    default=ROOT / "data/codex_transport_exception_shared_edges.json")
    args = ap.parse_args()
    selected = json.loads(args.input.read_text(encoding="utf-8"))
    case, orbit = selected["case"], selected["orbit"]
    core, _, _, orbits, _ = setup(*CASES[case])
    for i, j in sorted(orbits)[orbit]:
        core[i, j] = core[j, i] = 1
    b = np.array(selected["last_selected_masks"], dtype=np.int64)
    m, rhs, edges = matrix(core, b)
    start = time.monotonic()
    report = {"case": case, "orbit": orbit, "selected_masks": b.tolist(),
              "scope": "one selected boundary, not all assignments to this star",
              "possible_shared_edges": len(edges), "certificate": solve(m, rhs),
              "seconds": time.monotonic() - start}
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print({k: v for k, v in report.items() if k not in ("selected_masks", "certificate")})
    print({k: v for k, v in report["certificate"].items() if k != "row_multipliers"})


if __name__ == "__main__":
    main()
