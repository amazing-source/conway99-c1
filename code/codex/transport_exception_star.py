"""Necessary extension test for the full star of a transport exception.

This is a new 24-vertex core, not a rerun of the dossier's 12-vertex LP.
The 75 remaining vertices have distinct root labels. No conclusion
about a completed graph is drawn from feasible mask assignments.
"""
import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import time

import networkx as nx
import numpy as np
from scipy.optimize import linprog

from convergences_transfer import strip
from twisted_prism_extension import certify_infeasible, verify_certificate, spectral_masks

ROOT = Path(__file__).resolve().parents[2]
CASES = [(0, (0, 5, 10)), (1, (0, 2, 5)), (1, (0, 3, 9))]


def pairings(vertices):
    if not vertices:
        yield []
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        for rest in pairings(vertices[1:k] + vertices[k + 1:]):
            yield [(u, vertices[k])] + rest


def setup(twist, triple):
    h = np.array(strip(twist), dtype=np.int64)
    t = np.array([int(i in triple) for i in range(12)], dtype=np.int64)
    counts = 2 - t - h @ t
    assert counts.sum() == 9 and max(counts) == 1
    labels = [None, None] + [i for i in range(12) if counts[i]]
    a = np.zeros((24, 24), dtype=np.int64)
    a[:12, :12] = h
    a[12, :12] = a[:12, 12] = t
    for k, label in enumerate(labels, 13):
        a[12, k] = a[k, 12] = 1
        if label is not None:
            a[k, label] = a[label, k] = 1
    fixed = [(i, 13 + labels.index(i)) for i in triple]
    root_neighbours = sorted(list(triple) + list(range(13, 24)))
    used = {v for e in fixed for v in e}
    free = [i for i in root_neighbours if i not in used]
    assert len(free) == 8
    for i, j in fixed:
        a[i, j] = a[j, i] = 1
    # All allowed relabellings fix the marked exceptional triple setwise.
    graph = nx.from_numpy_array(h)
    nx.set_node_attributes(graph, {i: int(i in triple) for i in range(12)}, "marked")
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph, graph, node_match=lambda x, y: x["marked"] == y["marked"]
    )
    actions = []
    for p in matcher.isomorphisms_iter():
        for flip in (0, 1):
            q = [p[i] for i in range(12)] + [12, 13 + flip, 14 - flip]
            q.extend(13 + labels.index(p[label]) for label in labels[2:])
            assert len(q) == 24 and sorted(q) == list(range(24))
            assert np.array_equal(a, a[np.ix_(q, q)])
            actions.append(q)
    orbits = {}
    for matching in pairings(free):
        canonical = min(
            tuple(sorted(tuple(sorted((p[u], p[v]))) for u, v in matching))
            for p in actions
        )
        orbits[canonical] = orbits.get(canonical, 0) + 1
    assert sum(orbits.values()) == 105
    cells = []
    for i in range(12):
        cells.append(((i,), int(4 + t[i] - counts[i])))
    h2 = h @ h
    for i, j in combinations(range(12), 2):
        n = int(2 - h[i, j] - h2[i, j] - t[i] * t[j])
        if n:
            cells.append(((i, j), n))
    assert sum(n for _, n in cells) == 75
    return a, root_neighbours, cells, orbits, len(actions)


def extension_model(a, root_neighbours, cells, spectral=False):
    used_labels = {
        tuple(i for i in root_neighbours if a[v, i])
        for v in range(12) if v not in root_neighbours
    }
    assert len(used_labels) == 9 and all(len(p) == 2 for p in used_labels)
    root_labels = [p for p in combinations(root_neighbours, 2)
                   if not a[p[0], p[1]] and p not in used_labels]
    assert len(root_labels) == 75
    candidates = []
    for mask, _ in cells:
        intersection = tuple(i for i in mask if i in root_neighbours)
        for label in root_labels:
            if tuple(i for i in label if i < 12) != intersection:
                continue
            b = [int(i in mask) if i < 12 else int(i in label) for i in range(24)]
            candidates.append(b)
    candidates = np.array(candidates, dtype=np.int64)
    deficit = 2 - a - a @ a
    candidates = candidates[np.all(candidates @ a <= 2 - candidates, axis=1)]
    for u, v in combinations(range(24), 2):
        if deficit[u, v] == 0:
            candidates = candidates[candidates[:, u] * candidates[:, v] == 0]
    before_spectral = len(candidates)
    if spectral and len(candidates):
        # Exact rational Schur filtering, inherited from the existing local tool.
        # It is only a necessary condition on each new exterior vertex.
        candidates = spectral_masks(a, candidates, 14)
    pairs = list(combinations(range(24), 2))
    rows = [np.ones(len(candidates), dtype=np.int64)]
    rows += [candidates[:, i] for i in range(24)]
    rows += [candidates[:, i] * candidates[:, j] for i, j in pairs]
    rhs = [75] + (14 - a.sum(axis=1)).tolist() + [int(deficit[i, j]) for i, j in pairs]
    for mask, n in cells:
        b = np.array([int(i in mask) for i in range(12)])
        rows.append(np.all(candidates[:, :12] == b, axis=1).astype(np.int64))
        rhs.append(n)
    return candidates, np.array(rows), np.array(rhs, dtype=np.int64), before_spectral


def run_case(case_index, spectral=False, limit=None):
    twist, triple = CASES[case_index]
    base, neighbours, cells, orbits, action_count = setup(twist, triple)
    records = []
    for index, (matching, multiplicity) in enumerate(sorted(orbits.items())):
        if limit is not None and index >= limit:
            break
        start = time.monotonic()
        a = base.copy()
        for i, j in matching:
            a[i, j] = a[j, i] = 1
        assert np.all((a @ a + a)[~np.eye(24, dtype=bool)] <= 2)
        candidates, m, rhs, before = extension_model(a, neighbours, cells, spectral)
        upper = np.ones(len(candidates), dtype=np.int64)
        result = linprog(np.zeros(len(candidates)), A_eq=m, b_eq=rhs,
                         bounds=(0, 1), method="highs", options={"time_limit": 20})
        record = {"orbit": index, "matching": matching, "labelled_multiplicity": multiplicity,
                  "masks_before_spectral": before, "masks": len(candidates),
                  "status": "lp_feasible_unresolved" if result.success else "unresolved",
                  "solver_status": int(result.status)}
        if result.status == 2:
            cert = certify_infeasible(m, rhs, upper)
            if cert is not None:
                verify_certificate(m, rhs, upper, cert)
                record.update(status="excluded_integer_certificate", certificate=cert)
        record["seconds"] = round(time.monotonic() - start, 3)
        records.append(record)
        print(case_index, index, len(orbits), record["masks"], record["status"],
              record["seconds"], flush=True)
    return {"twist": twist, "triple": triple, "action_count": action_count,
            "total_orbits": len(orbits), "total_labelled_matchings": 105,
            "coverage_complete": len(records) == len(orbits), "records": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=int, choices=range(3))
    parser.add_argument("--spectral", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--out", type=Path,
                        default=ROOT / "data/codex_transport_exception_star.json")
    args = parser.parse_args()
    out = {"scope": "necessary 24-vertex core extension, not completed graphs",
           "spectral_masks": args.spectral, "cases": []}
    for case in range(3) if args.case is None else [args.case]:
        out["cases"].append(run_case(case, args.spectral, args.limit))
        args.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("Summary", [dict(Counter(x["status"] for x in c["records"])) for c in out["cases"]])


if __name__ == "__main__":
    main()
