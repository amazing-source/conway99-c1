"""Shared-edge completion search for one exceptional transport star.

All 84 vertices far from the exception have fixed, distinct root labels.
The same adjacency variables occur in every degree/common-neighbour equation.
Initial common-neighbour equations cover all pairs involving the nine
known far vertices. Violated remaining pairs can be added lazily.
UNKNOWN means only that the configured search limit was reached.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time

import numpy as np
from ortools.sat.python import cp_model

from transport_exception_star import CASES, setup, extension_model

ROOT = Path(__file__).resolve().parents[2]


def build(case, orbit):
    core, near, cells, orbits, _ = setup(*CASES[case])
    matching = sorted(orbits)[orbit]
    for i, j in matching:
        core[i, j] = core[j, i] = 1
    candidates, _, _, _ = extension_model(core, near, cells, False)
    labels = [p for p in combinations(near, 2) if not core[p[0], p[1]]]
    assert len(labels) == 84
    seeds = {labels.index(tuple(i for i in near if core[v, i])): v
             for v in range(12) if v not in near}
    assert len(seeds) == 9
    mate = {u: next(v for v in near if core[u, v]) for u in near}
    model = cp_model.CpModel()
    edges = {}
    for p, q in combinations(range(84), 2):
        edges[p, q] = (int(core[seeds[p], seeds[q]]) if p in seeds and q in seeds
                       else model.new_bool_var(f"e_{p}_{q}"))

    def edge(p, q):
        return 0 if p == q else edges[min(p, q), max(p, q)]

    seed_order = sorted(seeds)
    for p, label in enumerate(labels):
        if p in seeds:
            continue
        selected = [b for b in candidates if tuple(u for u in near if b[u]) == label]
        patterns = sorted({tuple(int(b[seeds[q]]) for q in seed_order) for b in selected})
        assert patterns
        model.add_allowed_assignments([edge(p, q) for q in seed_order], patterns)
    for p, label in enumerate(labels):
        model.add(sum(edge(p, q) for q in range(84) if q != p) == 12)
        for u in near:
            target = (1 if u in label else 2) - int(mate[u] in label)
            model.add(sum(edge(p, q) for q, lab in enumerate(labels) if u in lab) == target)

    imposed = set()

    def add_pair(p, q):
        p, q = sorted((p, q))
        if (p, q) in imposed:
            return
        terms = []
        for k in range(84):
            if k in (p, q):
                continue
            a, b = edge(p, k), edge(q, k)
            if isinstance(a, int):
                if a:
                    terms.append(b)
            elif isinstance(b, int):
                if b:
                    terms.append(a)
            else:
                y = model.new_bool_var(f"c_{p}_{q}_{k}")
                model.add(y <= a)
                model.add(y <= b)
                model.add(y >= a + b - 1)
                terms.append(y)
        model.add(sum(terms) + edge(p, q) == 2 - len(set(labels[p]) & set(labels[q])))
        imposed.add((p, q))

    for p, q in combinations(range(84), 2):
        if p in seeds or q in seeds:
            add_pair(p, q)
    return model, edge, add_pair, imposed, core, near, labels, seeds, matching


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=int, choices=range(3), default=0)
    parser.add_argument("--orbit", type=int, default=0)
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--add-pairs", type=int, default=30)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--log", action="store_true")
    parser.add_argument("--out", type=Path,
                        default=ROOT / "data/codex_transport_exception_completion.json")
    args = parser.parse_args()
    start = time.monotonic()
    model, edge, add_pair, imposed, core, near, labels, seeds, matching = build(args.case, args.orbit)
    report = {"case": args.case, "orbit": args.orbit, "matching": matching,
              "scope": "one shared-edge completion instance, not all exceptional cases",
              "build_seconds": time.monotonic() - start, "rounds": []}
    print("BUILT", len(imposed), "far pair equations", "seconds", report["build_seconds"], flush=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for iteration in range(args.rounds):
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = args.seconds
        solver.parameters.num_search_workers = args.workers
        solver.parameters.log_search_progress = args.log
        status = solver.solve(model)
        row = {"round": iteration, "status": solver.status_name(status),
               "seconds": solver.wall_time, "imposed_far_pairs": len(imposed),
               "conflicts": solver.num_conflicts, "branches": solver.num_branches}
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            far = np.zeros((84, 84), dtype=np.int64)
            for p, q in combinations(range(84), 2):
                value = edge(p, q)
                far[p, q] = far[q, p] = value if isinstance(value, int) else solver.value(value)
            a = np.zeros((99, 99), dtype=np.int64)
            a[0, 1:15] = a[1:15, 0] = 1
            a[1:15, 1:15] = core[np.ix_(near, near)]
            for p, label in enumerate(labels):
                for u in label:
                    a[15 + p, 1 + near.index(u)] = a[1 + near.index(u), 15 + p] = 1
            a[15:, 15:] = far
            defect = a @ a + a - 12 * np.eye(99, dtype=np.int64) - 2
            assert np.all(a.sum(axis=1) == 14)
            assert np.all(defect[:15, :] == 0)
            assert all(not defect[15+p, 15+q] for p, q in imposed)
            bad = [(abs(int(defect[15+p, 15+q])), p, q)
                   for p, q in combinations(range(84), 2) if defect[15+p, 15+q]]
            row["violated_far_pairs"] = len(bad)
            row["max_common_neighbour_defect"] = max((v for v, _, _ in bad), default=0)
            row["far_adjacency"] = far.tolist()
            if not bad:
                row["full_srg_identity_checked"] = True
            else:
                for _, p, q in sorted(bad, reverse=True)[:args.add_pairs]:
                    add_pair(p, q)
        report["rounds"].append(row)
        args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print({k: v for k, v in row.items() if k != "far_adjacency"}, flush=True)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE) or row.get("full_srg_identity_checked"):
            break


if __name__ == "__main__":
    main()
