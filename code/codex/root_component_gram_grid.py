"""Exhaustive finite-grid Gram enumeration, without SAT search.

Choose independent entries of the linear space CR=0 with component
orthogonality. Every other entry is a rational linear function of these.
Enumerate the finite entry domains, then test integrality, bounds and PSD.
"""

import argparse
from itertools import combinations
import json
from math import lcm, prod
from pathlib import Path
import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_gram_enumeration import integer_psd


def enumerate_grid(template):
    started = time.monotonic()
    edges = [set(e) for e in template["nongrid_edges"]]
    nodes, links = template["component_graph_nodes"], template["component_graph_edges"]
    m = len(edges)
    incidence = sp.zeros(len(nodes), m)
    for j, (a, b) in enumerate(links):
        incidence[a, j] = incidence[b, j] = 1
    kernel = sp.Matrix.hstack(*incidence.nullspace())
    d = kernel.cols
    anchors = list(kernel.T.rref()[1])
    symmetric_pairs = [(i, j) for i in range(d) for j in range(i, d)]
    entries = [(i, j) for i in range(m) for j in range(i, m)]
    entry_index = {pair: i for i, pair in enumerate(entries)}
    forms = {pair: sp.Matrix(1, len(symmetric_pairs), [
        kernel[pair[0], i] * kernel[pair[1], j] +
        (kernel[pair[0], j] * kernel[pair[1], i] if i != j else 0)
        for i, j in symmetric_pairs]) for pair in entries}
    zero_forms = []
    for (a, b), form in forms.items():
        common = edges[a] & edges[b]
        if a != b and common:
            root = next(iter(common))
            if not any(r == root and (edges[a] - {root}).issubset(part)
                       and (edges[b] - {root}).issubset(part) for r, part in nodes):
                zero_forms.append(form)
    zero_matrix = sp.Matrix.vstack(*zero_forms) if zero_forms else sp.zeros(0, len(symmetric_pairs))
    free = sp.Matrix.hstack(*zero_matrix.nullspace())
    dimension = free.cols
    selected, rows = [], sp.zeros(0, dimension)
    order = sorted(entries, key=lambda pair: (pair[0] != pair[1], not bool(edges[pair[0]] & edges[pair[1]]), pair))
    for pair in order:
        row = forms[pair] * free
        if rows.col_join(row).rank() > rows.rows:
            selected.append(pair)
            rows = rows.col_join(row)
            if rows.rows == dimension:
                break
    assert rows.rows == dimension
    inverse = rows.inv()
    coefficient_rows, denominators = [], []
    for pair in entries:
        row = forms[pair] * free * inverse
        denominator = lcm(*(int(x.q) for x in row))
        denominators.append(denominator)
        coefficient_rows.append([int(x * denominator) for x in row])
    coefficients = np.array(coefficient_rows, dtype=np.int64)
    denominators_np = np.array(denominators, dtype=np.int64)
    assert max(sum(abs(x) for x in row) for row in coefficient_rows) * 8 < 2 ** 60
    domains = [list((2, 4, 6, 8) if a == b else range(-8, 1 if edges[a] & edges[b] else 5)) for a, b in selected]
    total = prod(map(len, domains))
    diagonal = [entry_index[i, i] for i in range(m)]
    off_diagonal = [entry_index[i, j] for i, j in combinations(range(m), 2)]
    upper_bounds = np.array([8 if a == b else (0 if edges[a] & edges[b] else 4) for a, b in entries])
    lower_bounds = np.array([2 if a == b else -8 for a, b in entries])
    lift = kernel * kernel.extract(anchors, range(d)).inv()
    upper = 28 * (lift.T * lift).inv()
    upper_scale = lcm(*(int(x.q) for x in upper))
    upper_base = [[int(x * upper_scale) for x in upper.row(i)] for i in range(d)]
    anchor_entry_indices = [entry_index[anchors[i], anchors[j]] for i, j in symmetric_pairs]
    counts = {"finite_parameter_grid": total, "integral_matrices": 0, "entry_domains": 0,
              "trace_and_prism_budget": 0, "two_by_two_minors": 0,
              "not_psd": 0, "exceeds_28I": 0, "psd_grams": 0}
    grams = []
    last_report = started
    for start in range(0, total, 32768):
        stop = min(start + 32768, total)
        ids = np.arange(start, stop, dtype=np.int64)
        values = np.empty((stop - start, dimension), dtype=np.int64)
        for j in range(dimension - 1, -1, -1):
            values[:, j] = np.array(domains[j], dtype=np.int64)[ids % len(domains[j])]
            ids //= len(domains[j])
        numerators = values @ coefficients.T
        integral = np.all(numerators % denominators_np == 0, axis=1)
        flat = numerators[integral] // denominators_np
        counts["integral_matrices"] += len(flat)
        legal = (np.all(flat >= lower_bounds, axis=1) & np.all(flat <= upper_bounds, axis=1)
                 & np.all(flat[:, diagonal] % 2 == 0, axis=1))
        flat = flat[legal]
        counts["entry_domains"] += len(flat)
        keep = ((np.sum(flat[:, diagonal], axis=1) <= 28 * d)
                & (4 * (21 - m) + 3 * np.count_nonzero(flat[:, diagonal] == 2, axis=1) <= 51))
        flat = flat[keep]
        counts["trace_and_prism_budget"] += len(flat)
        for i, j in combinations(range(m), 2):
            flat = flat[flat[:, entry_index[i, j]] ** 2 <= flat[:, diagonal[i]] * flat[:, diagonal[j]]]
        counts["two_by_two_minors"] += len(flat)
        for anchor_values in flat[:, anchor_entry_indices].tolist():
            small = [[0] * d for _ in range(d)]
            for (i, j), value in zip(symmetric_pairs, anchor_values):
                small[i][j] = small[j][i] = value
            if not integer_psd(small):
                counts["not_psd"] += 1
                continue
            complement = [[upper_base[i][j] - upper_scale * small[i][j] for j in range(d)] for i in range(d)]
            if not integer_psd(complement):
                counts["exceeds_28I"] += 1
                continue
            grams.append(anchor_values)
        if time.monotonic() - last_report >= 10:
            print(json.dumps({"grid_examined": stop, "grid_total": total, "gram_count": len(grams)}), flush=True)
            last_report = time.monotonic()
    assert len({tuple(row) for row in grams}) == len(grams)
    counts["psd_grams"] = len(grams)
    return {"status": "EXHAUSTIVE_FINITE_GRID", "exhaustive": True, "usable_as_gram_cover": True,
            "root_prism_budget": 51, "requires_separate_corner_realization": False,
            "seconds": time.monotonic() - started, "counts": counts,
            "gram_count": len(grams), "anchors": anchors, "anchor_pairs": symmetric_pairs,
            "lift_matrix": [[[int(x.p), int(x.q)] for x in lift.row(i)] for i in range(m)],
            "upper_test_scale": upper_scale, "upper_test_base": upper_base,
            "finite_grid_certificate": {"dimension": dimension, "independent_entries": selected,
                 "parameter_domains": domains, "all_entries_order": entries,
                 "entry_numerators": coefficient_rows, "entry_denominators": denominators},
            "gram_anchor_values": grams}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--prior", type=Path, required=True)
    parser.add_argument("--indices", type=int, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    templates = json.loads((args.directory / "root_component_templates.json").read_text(encoding="utf-8"))["survivors"]
    data = json.loads(args.prior.read_text(encoding="utf-8"))
    records = {r["template_index"]: r for r in data["records"]}
    for index in args.indices:
        assert not records[index]["exhaustive"], "Already covered; do not repeat the enumeration."
        record = {"template_index": index, **enumerate_grid(templates[index])}
        records[index] = record
        data["records"] = [records[i] for i in sorted(records)]
        args.output.write_text(json.dumps(data, separators=(",", ":")) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in record.items() if k not in (
            "gram_anchor_values", "lift_matrix", "upper_test_base", "anchor_pairs", "finite_grid_certificate")}), flush=True)


if __name__ == "__main__":
    main()
