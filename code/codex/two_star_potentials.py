"""Exact local-potential certificates for a fixed two-star branch.

Convert the equality-only Farkas certificate into potentials on 18
domains and 153 pair tables. Verify without the LP matrix or any solver.
Domains and compatibility still come from the shared exact generator.
"""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations
import json
from pathlib import Path

import numpy as np

from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
from joint_star_propagation import setup, propagate, replay


def context(g, u, v, apex):
    prepared = prepare(g, u, v)
    system = setup(prepared, u, v, apex)
    propagation = propagate(system)
    alive = replay(system, propagation)
    assert propagation["contradiction"] is None
    common, labels, arrays, sides, targets, compat = system
    kept = [sorted(a) for a in alive]
    arrays = [a[k] for a, k in zip(arrays, kept)]
    tables = {}
    for i, j in combinations(range(18), 2):
        rows, cols = np.nonzero(compat[i, j][np.ix_(kept[i], kept[j])])
        edge = 3-(arrays[i]@prepared[1]@arrays[j].T) % 7
        tables[i, j] = [(int(c), int(d), int(edge[c, d])) for c, d in zip(rows, cols)]
        assert tables[i, j]
    caps = [[[int((1 if labels[i][0] == side else 2)-arr[c]@prepared[0][center])
              for side, center in enumerate((u, v))] for c in range(len(arr))]
            for i, arr in enumerate(arrays)]
    return {"common": list(common), "labels": [list(t) for t in labels],
            "arrays": arrays, "kept": kept, "targets": [a.tolist() for a in targets],
            "tables": tables, "caps": caps, "sides": sides}


def extract(source, ctx):
    beta = [[0]*36 for _ in range(2)]
    gamma = [[0, 0] for _ in range(18)]
    eta = {(i, j): [[0]*len(ctx["arrays"][i]), [0]*len(ctx["arrays"][j])]
           for i, j in combinations(range(18), 2)}
    for entry in source["farkas_certificate"]:
        parts, value = entry["name"].split(":"), entry["multiplier"]
        if parts[0] == "domain":
            continue  # Cancels between the lower bound and the RHS.
        if parts[0] == "star_sum":
            beta[int(parts[1])][int(parts[2])] = value
        elif parts[0] == "degree":
            gamma[int(parts[1])][int(parts[2])] = value
        else:
            assert parts[0] == "marginal", "requires the simplified equality-only certificate"
            i, j, var, c = map(int, parts[1:])
            assert var in (i, j)
            eta[i, j][0 if var == i else 1][c] = value
    return beta, gamma, eta


def normalize(beta, gamma, eta, ctx):
    """Remove constant gauges; exact evaluation below is authoritative."""
    beta, gamma, eta = copy.deepcopy((beta, gamma, eta))
    for side in (0, 1):
        for layer in range(3):
            indices = range(12*layer, 12*layer+12)
            shift = sorted(beta[side][p] for p in indices)[6]
            for p in indices:
                beta[side][p] -= shift
        for p in range(36):
            values = [set(map(int, ctx["arrays"][i][:, p])) for i in ctx["sides"][side]]
            if all(len(v) == 1 for v in values) and sum(next(iter(v)) for v in values) == ctx["targets"][side][p]:
                beta[side][p] = 0
    for pair in eta.values():
        for values in pair:
            shift = Counter(values).most_common(1)[0][0]
            for c in range(len(values)):
                values[c] -= shift
    return beta, gamma, eta


def evaluate(beta, gamma, eta, ctx):
    """All score arithmetic uses arbitrary-precision Python integers."""
    unary = []
    for i, arr in enumerate(ctx["arrays"]):
        side = ctx["labels"][i][0]
        scores = []
        for c, n in enumerate(arr):
            score = sum(beta[side][p] for p in np.flatnonzero(n))
            score -= sum(gamma[i][t]*ctx["caps"][i][c][t] for t in (0, 1))
            scores.append(score)
        unary.append(scores)
    pair_bounds = []
    for (i, j), (left, right) in sorted(eta.items()):
        assert len(left) == len(unary[i]) and len(right) == len(unary[j])
        unary[i] = [a-b for a, b in zip(unary[i], left)]
        unary[j] = [a-b for a, b in zip(unary[j], right)]
        weight = gamma[i][ctx["labels"][j][0]]+gamma[j][ctx["labels"][i][0]]
        bound = min(left[c]+right[d]+weight*edge for c, d, edge in ctx["tables"][i, j])
        pair_bounds.append({"pair": [i, j], "minimum": bound})
    unary_bounds = [min(values) for values in unary]
    rhs = sum(beta[s][p]*ctx["targets"][s][p] for s in (0, 1) for p in range(36))
    lower = sum(unary_bounds)+sum(b["minimum"] for b in pair_bounds)
    return {"unary_minima": unary_bounds, "pair_minima": pair_bounds,
            "unary_minima_sum": sum(unary_bounds),
            "pair_minima_sum": sum(b["minimum"] for b in pair_bounds),
            "lower_bound": lower, "weighted_target": rhs, "contradiction_gap": lower-rhs}


def rounded(weights, unit):
    def one(value):
        return (1 if value >= 0 else -1)*((abs(value)+unit//2)//unit)
    beta, gamma, eta = weights
    return ([[one(v) for v in row] for row in beta],
            [[one(v) for v in row] for row in gamma],
            {ij: [[one(v) for v in row] for row in pair] for ij, pair in eta.items()})


def pack(beta, gamma, eta):
    return {"star_weights": beta, "degree_weights": gamma,
            "pair_potentials": [{"pair": list(ij),
                "left": [[c, v] for c, v in enumerate(pair[0]) if v],
                "right": [[c, v] for c, v in enumerate(pair[1]) if v]}
                for ij, pair in sorted(eta.items())]}


def unpack(data, ctx):
    beta, gamma = data["star_weights"], data["degree_weights"]
    assert len(beta) == 2 and all(len(row) == 36 for row in beta)
    assert len(gamma) == 18 and all(len(row) == 2 for row in gamma)
    assert all(type(v) is int for row in beta+gamma for v in row)
    eta = {}
    for item in data["pair_potentials"]:
        i, j = item["pair"]
        assert 0 <= i < j < 18 and (i, j) not in eta
        pair = []
        for variable, key in ((i, "left"), (j, "right")):
            values, seen = [0]*len(ctx["arrays"][variable]), set()
            for c, value in item[key]:
                assert type(c) is int and 0 <= c < len(values) and c not in seen
                assert type(value) is int and value != 0
                seen.add(c); values[c] = value
            pair.append(values)
        eta[i, j] = pair
    assert set(eta) == set(combinations(range(18), 2))
    return beta, gamma, eta


def verify(report):
    u, v = report["centers"]
    ctx = context(report["adjacency"], u, v, report["apex_index"])
    assert ctx["common"] == report["common_apex_support"]
    assert ctx["labels"] == report["variable_labels"] and ctx["kept"] == report["candidate_indices"]
    weights = unpack(report, ctx)
    if report["drop_degree_equations"]:
        assert all(v == 0 for row in weights[1] for v in row)
    result = evaluate(*weights, ctx)
    assert result == report["exact_check"] and result["contradiction_gap"] > 0
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--ball", type=Path)
    parser.add_argument("--drop-degrees", action="store_true")
    parser.add_argument("--search-rounding", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        result = verify(json.loads(args.out.read_text(encoding="utf-8")))
    else:
        assert args.source is not None
        source = json.loads(args.source.read_text(encoding="utf-8"))
        if args.ball:
            g = json.loads(args.ball.read_text(encoding="utf-8"))["adjacency"]
        elif source["ball"] == "cyclic(2,4,1)":
            g = cyclic_ball()
        else:
            g = json.loads(Path(source["ball"]).read_text(encoding="utf-8"))["adjacency"]
        u, v = source["centers"]
        ctx = context(g, u, v, source["apex_index"])
        weights = extract(source, ctx)
        original = evaluate(*weights, ctx)
        normalized = normalize(*weights, ctx)
        assert evaluate(*normalized, ctx)["contradiction_gap"] == original["contradiction_gap"]
        if args.drop_degrees:
            normalized = (normalized[0], [[0, 0] for _ in range(18)], normalized[2])
        diagnostics, chosen = [], None
        for unit in ((1, 2, 5, 10, 20, 50, 100, 200, 500, 1000) if args.search_rounding else (1,)):
            candidate = rounded(normalized, unit)
            result = evaluate(*candidate, ctx)
            diagnostics.append({"unit": unit, "gap": result["contradiction_gap"]})
            if result["contradiction_gap"] > 0:
                chosen = unit, candidate, result
        assert chosen is not None, "no exact potential certificate found"
        unit, candidate, result = chosen
        report = {"source": str(args.source), "source_sha256": hashlib.sha256(args.source.read_bytes()).hexdigest(),
                  "ball": source["ball"], "adjacency": np.asarray(g).tolist(), "centers": [u, v],
                  "apex_index": source["apex_index"], "common_apex_support": ctx["common"],
                  "variable_labels": ctx["labels"], "candidate_indices": ctx["kept"],
                  "drop_degree_equations": args.drop_degrees, "rounding_unit": unit,
                  "rounding_diagnostics": diagnostics, **pack(*candidate), "exact_check": result,
                  "scope": "one branch on the exactly filtered domains; not a uniform exclusion"}
        verify(report)
        args.out.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
        print(json.dumps({"rounding": diagnostics, "chosen_unit": unit}), flush=True)
    print(json.dumps({k: v for k, v in result.items() if k not in ("unary_minima", "pair_minima")}), flush=True)


if __name__ == "__main__":
    main()
