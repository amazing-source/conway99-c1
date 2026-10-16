"""Compute the new 20x20 line-resonance invariant proposed in LAB925.

Uses accepted 44-label four-star objects; it does not rerun their validity
or automorphism certificates. All new ranks and nullspaces are exact over Q.
Both choices of the distinguished line are computed. Output includes a
scaled integer Q, an integer kernel, and a full-rank principal minor.
"""

from __future__ import annotations

import argparse
from functools import reduce
import glob
import hashlib
from itertools import combinations
import json
from math import gcd, lcm
from pathlib import Path
import time

import sympy as sp


LABELS = [(a, b) for a, b in combinations(range(14), 2)
          if a < 4 and b != (a ^ 1)]
INDEX = {p: i for i, p in enumerate(LABELS)}
B = sp.Matrix([[int(r in p) for p in LABELS] for r in range(14)])


def records(value, name=""):
    if isinstance(value, dict) and "labels" in value:
        if len(value["labels"]) == 44:
            yield name or "object", value
        else:
            raise ValueError("Only complete 44-label four-star inputs are supported.")
    elif isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, dict) and "labels" in item:
                yield from records(item, str(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from records(item, str(index))


def adjacency(record):
    labels = [tuple(p) for p in record["labels"]]
    if set(labels) != set(LABELS):
        raise ValueError("Input uses a different four-star geometry.")
    if "gamma" in record:
        raw = sp.Matrix(record["gamma"])
    elif "adjacency" in record:
        raw = sp.Matrix(record["adjacency"])
    else:
        raw = sp.zeros(44)
        for i, j in record["edges"]:
            raw[i, j] = raw[j, i] = 1
    order = [labels.index(p) for p in LABELS]
    gamma = raw.extract(order, order)
    if gamma != gamma.T or any(gamma[i, i] for i in range(44)):
        raise ValueError("The input adjacency is not a simple undirected matrix.")
    if any(x not in (0, 1) for x in gamma):
        raise ValueError("The input adjacency is not binary.")
    return gamma


def root_block(gamma):
    a = sp.zeros(59)
    for r in range(14):
        a[0, r + 1] = a[r + 1, 0] = 1
        a[r + 1, (r ^ 1) + 1] = 1
    for i, label in enumerate(LABELS):
        for r in label:
            a[r + 1, 15 + i] = a[15 + i, r + 1] = 1
    a[15:, 15:] = gamma
    return a


def components(adjacency_matrix):
    pending = set(range(adjacency_matrix.rows))
    result = []
    while pending:
        seed = min(pending)
        pending.remove(seed)
        stack, component = [seed], [seed]
        while stack:
            v = stack.pop()
            neighbors = {u for u in pending if adjacency_matrix[v, u]}
            pending.difference_update(neighbors)
            stack.extend(sorted(neighbors))
            component.extend(sorted(neighbors))
        result.append(sorted(component))
    return result


def integer_vector(vector):
    denominator = lcm(*(int(x.q) for x in vector))
    values = [int(x * denominator) for x in vector]
    divisor = reduce(gcd, map(abs, values))
    values = [x // divisor for x in values]
    if next(x for x in values if x) < 0:
        values = [-x for x in values]
    return values


def rank_certificate(matrix):
    denominator = lcm(*(int(x.q) for x in matrix))
    integer = matrix * denominator
    pivots = list(integer.rref()[1])
    minor = integer.extract(pivots, pivots).det(method="domain-ge")
    assert minor != 0
    kernel = [integer_vector(v) for v in integer.nullspace()]
    assert len(kernel) == matrix.cols - len(pivots)
    for vector in kernel:
        assert integer * sp.Matrix(vector) == sp.zeros(matrix.rows, 1)
    return {
        "rank": len(pivots),
        "corank": len(kernel),
        "denominator": int(denominator),
        "integer_matrix": [[int(x) for x in row] for row in integer.tolist()],
        "principal_minor_indices": pivots,
        "principal_minor_determinant": str(minor),
        "integer_kernel_basis": kernel,
    }


def one_line(a, root_letter):
    line = [0, root_letter + 1, (root_letter ^ 1) + 1]
    near = [i for i in range(59) if i not in line and any(a[i, j] for j in line)]
    far = [i for i in range(59) if i not in line and i not in near]
    assert len(near) == 36 and len(far) == 20
    local = a.extract(near, near)
    if local * sp.ones(36, 1) != 3 * sp.ones(36, 1):
        raise ValueError("The selected line-neighborhood is not the complete cubic block.")
    groups = components(local)
    projector = sp.zeros(36)
    for group in groups:
        for i in group:
            for j in group:
                projector[i, j] = sp.Rational(1, len(group))
    laplacian = 3 * sp.eye(36) - local
    inverse = (laplacian + projector).inv(method="DM") - projector
    assert laplacian * inverse == sp.eye(36) - projector
    assert inverse * projector == sp.zeros(36)
    incidence = a.extract(far, near)
    component_balances = [
        list(incidence[:, group] * sp.ones(len(group), 1)) for group in groups
    ]
    if any(any(x != sp.Rational(len(group), 6) for x in values)
           for group, values in zip(groups, component_balances)):
        raise ValueError("The new elimination requires exact component balance.")
    q = 3 * sp.eye(20) - a.extract(far, far) - incidence * inverse * incidence.T
    v = incidence * inverse * a.extract(near, line)
    certificate = rank_certificate(q)
    joined = q.row_join(sp.ones(20, 1)).row_join(v)
    extended_rank = len(joined.rref()[1])
    # Effective dimension of RHS span(1,V), and obstructions to its range in Q.
    rhs_rank = len(sp.ones(20, 1).row_join(v).rref()[1])
    effective_rhs = rhs_rank - (extended_rank - certificate["rank"])
    shifted = q + sp.ones(20) / 12
    shifted_corank = 20 - len(shifted.rref()[1])
    trace = sp.trace(shifted)
    squared_trace = sp.trace(shifted * shifted)
    return {
        "line_root_letters": [root_letter, root_letter ^ 1],
        "near_vertices_in_rooted59": near,
        "far_labels": [list(LABELS[i - 15]) for i in far],
        "component_sizes": [len(group) for group in groups],
        "component_count": len(groups),
        "Q": certificate,
        "V": [[str(x) for x in row] for row in v.tolist()],
        "V_is_zero": v == sp.zeros(20, 3),
        "Q_row_sums": sorted(set(str(x) for x in q * sp.ones(20, 1))),
        "Q_plus_J_over_12_corank": shifted_corank,
        "F_trace": str(trace),
        "F_trace_square": str(squared_trace),
        "F_effective_rank": str(trace**2 / squared_trace) if squared_trace else None,
        "nullity_from_exact_elimination": len(groups) + 1 + shifted_corank,
        "rhs_span_dimension": rhs_rank,
        "rhs_span_intersection_image_Q_dimension": effective_rhs,
        "solution_projection_dimension": certificate["corank"] + effective_rhs,
        "proposed_corank_at_most_4_holds": certificate["corank"] <= 4,
    }


def analyze(record):
    gamma = adjacency(record)
    a = root_block(gamma)
    corners = [INDEX[p] for p in ((0, 2), (0, 3), (1, 2), (1, 3))]
    corner_edges = sum(gamma[i, j] for i, j in combinations(corners, 2))
    results = [one_line(a, r) for r in (0, 2)]
    mate_gram = B.T * B[[r ^ 1 for r in range(14)], :]
    t8 = 24 * sp.eye(44) - 8 * gamma - 3 * (B.T * B) - mate_gram + 2 * sp.ones(44)
    nullity = 44 - len(t8.rref()[1])
    counts = [result["component_count"] for result in results]
    for result in results:
        assert result["V_is_zero"]
        assert result["Q_row_sums"] == ["-5/3"]
        assert result["nullity_from_exact_elimination"] == nullity
        assert result["Q_plus_J_over_12_corank"] == result["Q"]["corank"] + 1
    return {
        "corner_edge_count": int(corner_edges),
        "grid_overlap": corner_edges == 4,
        "T_nullity": nullity,
        "line_component_counts": counts,
        "nongrid_mixed_dimension_formula": nullity - 2 - sum(counts) if corner_edges != 4 else None,
        "N9_bound": 9 + min(counts),
        "N9_inequality_holds": nullity <= 9 + min(counts),
        "minimum_component_line_F_rank": 19 - results[counts.index(min(counts))]["Q"]["corank"],
        "lines": results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", help="JSON files or quoted glob patterns")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    result = {"origin": "LAB925, new line-resonance Q invariant",
              "scope": "Accepted local blocks only; no exhaustive classification or Conway exclusion.",
              "records": []}
    files = sorted({str(Path(path).resolve()) for source in args.sources for path in glob.glob(source)})
    if not files:
        raise ValueError("No source files matched.")
    for filename in files:
        content = Path(filename).read_bytes()
        value = json.loads(content.decode("utf-8-sig"))
        for name, record in records(value):
            item = {"source_file": filename, "source_sha256": hashlib.sha256(content).hexdigest(),
                    "record": name, **analyze(record)}
            result["records"].append(item)
            print(json.dumps({"file": Path(filename).name, "record": name,
                              "grid": item["grid_overlap"], "c": item["line_component_counts"],
                              "nu": item["T_nullity"],
                              "Q_coranks": [x["Q"]["corank"] for x in item["lines"]],
                              "rhs_dimensions": [x["rhs_span_dimension"] for x in item["lines"]],
                              "V_zero": [x["V_is_zero"] for x in item["lines"]],
                              "Q_shifted_coranks": [x["Q_plus_J_over_12_corank"] for x in item["lines"]],
                              "Q_row_sums": [x["Q_row_sums"] for x in item["lines"]],
                              "F_effective_ranks": [x["F_effective_rank"] for x in item["lines"]],
                              "projection_dimensions": [x["solution_projection_dimension"] for x in item["lines"]]}), flush=True)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            result["seconds"] = time.monotonic() - started
            args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"objects": len(result["records"]), "seconds": result.get("seconds", 0)}), flush=True)


if __name__ == "__main__":
    main()
