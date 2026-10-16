"""Finite integral column signatures in a root rectangle Gram quotient.

For rank r<=4, every individual vertex has an integer signature h in im(R),
with h^t R^+ h<=5/2. At most 5^r anchor assignments need testing per root
rectangle. Four such signatures must add to the corresponding column of R.
This is a necessary realization test, not a binary adjacency completion.
"""

import argparse
from collections import Counter
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_quotient import EDGES
from three_star_ambient_upper import psd_or_witness


RECTANGLE_LABELS = ((0, 2), (0, 3), (1, 2), (1, 3))


def corner_graphs(edge_count):
    pairs = list(combinations_with_replacement(range(4), 2))
    pairs = [(i, j) for i, j in pairs if i != j]
    result = []
    for mask in range(1 << 6):
        if mask.bit_count() != edge_count:
            continue
        adjacency = [[0] * 4 for _ in range(4)]
        for k, (i, j) in enumerate(pairs):
            adjacency[i][j] = adjacency[j][i] = int(bool(mask & (1 << k)))
        if any(sum(adjacency[i][j] for j in range(4) if a in RECTANGLE_LABELS[j]) > 1
               for i in range(4) for a in range(4)):
            continue
        t4 = [[10 if i == j else -4*adjacency[i][j]-int(bool(set(RECTANGLE_LABELS[i]) & set(RECTANGLE_LABELS[j])))
               for j in range(4)] for i in range(4)]
        result.append((adjacency, t4, [2-sum(row) for row in adjacency]))
    return result


def rectangle_realizations(edges, raw, domains=None):
    """Four genuine binary corner rows and their conditional T Gram."""
    domains = signature_domains(edges, raw) if domains is None else domains
    if not edges:
        return {"feasible": True, "witnesses": [], "scope": "Empty nongrid quotient only."}
    matrix = sp.Matrix(raw)
    anchors = list(matrix.rref()[1])
    small = matrix.extract(anchors, anchors)
    denominator = int(small.det())
    adjugate = (small.inv(method="DM") * denominator).applyfunc(int)
    witnesses = []
    for item in domains:
        rectangle = tuple(item["rectangle"])
        signatures = [tuple(v) for v in item["signatures"]]
        coordinate = edges.index(rectangle) if rectangle in edges else None
        energy = int(matrix[coordinate, coordinate]) if coordinate is not None else 0
        patterns = corner_graphs(4-energy//2)
        vectors = [sp.Matrix([h[i] for i in anchors]) for h in signatures]
        gram = [[int((a.T*adjugate*b)[0]) for b in vectors] for a in vectors]
        target = tuple(item["target"])
        found = None
        for adjacency, t4, degrees in patterns:
            choices = [[i for i,h in enumerate(signatures) if coordinate is None or h[coordinate] == value]
                       for value in degrees]
            pair_sums = {}
            for i, j in product(choices[2], choices[3]):
                key = tuple(a+b for a,b in zip(signatures[i], signatures[j]))
                pair_sums.setdefault(key, []).append((i, j))
            for i, j in product(choices[0], choices[1]):
                needed = tuple(t-a-b for t,a,b in zip(target, signatures[i], signatures[j]))
                for k,l in pair_sums.get(needed, []):
                    indices = (i,j,k,l)
                    residual = sp.Matrix(4, 4, lambda a,b:
                        denominator*t4[int(a)][int(b)]-4*gram[indices[int(a)]][indices[int(b)]])
                    if psd_or_witness(residual)["psd"]:
                        found = {"rectangle": rectangle, "signature_indices": indices,
                                 "corner_adjacency": adjacency}
                        break
                if found is not None:
                    break
            if found is not None:
                break
        if found is None:
            return {"feasible": False, "failed_rectangle": rectangle,
                    "reason": "No binary corner graph and four signatures satisfy the conditional Gram."}
        witnesses.append(found)
    return {"feasible": True, "witnesses": witnesses}


def bounds(rectangle, coordinate):
    if rectangle == coordinate:
        return 0, 2
    return (-2, 0) if set(rectangle).intersection(coordinate) else (-3, 1)


def signature_domains(edges, raw):
    matrix = sp.Matrix(raw)
    m = len(edges)
    if not m:
        return [{"rectangle": e, "signatures": [[]], "four_sum": [0, 0, 0, 0]} for e in EDGES]
    anchors = list(matrix.rref()[1])
    small = matrix.extract(anchors, anchors)
    denominator = int(small.det())
    assert denominator > 0 and len(anchors) <= 4
    inverse_scaled = (small.inv(method="DM") * denominator).applyfunc(int)
    lift = matrix[:, anchors] * inverse_scaled
    inverse_scaled = [[int(x) for x in row] for row in inverse_scaled.tolist()]
    lift = [[int(x) for x in row] for row in lift.tolist()]
    results = []
    for rectangle in EDGES:
        intervals = [bounds(rectangle, edge) for edge in edges]
        domains = []
        for coordinates in product(*(range(intervals[i][0], intervals[i][1]+1) for i in anchors)):
            norm = sum(coordinates[i]*inverse_scaled[i][j]*coordinates[j]
                       for i in range(len(anchors)) for j in range(len(anchors)))
            if 2*norm > 5*denominator:
                continue
            numerator = [sum(a*b for a,b in zip(row, coordinates)) for row in lift]
            if any(x % denominator for x in numerator):
                continue
            h = tuple(x // denominator for x in numerator)
            if all(lo <= x <= hi for x, (lo, hi) in zip(h, intervals)):
                domains.append(h)
        target = tuple(int(matrix[i, edges.index(rectangle)]) for i in range(m)) if rectangle in edges else (0,) * m
        pairs = {}
        for i, j in combinations_with_replacement(range(len(domains)), 2):
            key = tuple(a+b for a,b in zip(domains[i], domains[j]))
            pairs.setdefault(key, (i, j))
        witness = None
        for key, first in pairs.items():
            second = pairs.get(tuple(a-b for a,b in zip(target, key)))
            if second is not None:
                witness = list(first+second)
                break
        results.append({"rectangle": rectangle, "signatures": domains,
                        "four_sum": witness, "target": target})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("templates", type=Path)
    parser.add_argument("grams", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    templates = json.loads(args.templates.read_text(encoding="utf-8"))["survivors"]
    grams = json.loads(args.grams.read_text(encoding="utf-8"))["records"]
    counts, records = Counter(), []
    started = time.monotonic()
    for item in grams:
        if item["status"] != "QUOTIENT_FEASIBLE":
            continue
        edges = [tuple(e) for e in templates[item["template_index"]]["nongrid_edges"]]
        domains = signature_domains(edges, item["R"])
        bad = [d["rectangle"] for d in domains if d["four_sum"] is None]
        realization = rectangle_realizations(edges, item["R"], domains) if not bad else None
        counts["R_has_all_four_sums" if not bad else "R_fails_four_sum"] += 1
        if realization:
            counts["R_has_all_corner_realizations" if realization["feasible"] else "R_fails_corner_realization"] += 1
        records.append({"template_index": item["template_index"], "bad_rectangles": bad,
                        "maximum_domain_size": max(len(d["signatures"]) for d in domains),
                        "domains": domains, "corner_realization": realization})
    output = {"scope": "Tests the saved Gram witness for each template, not all feasible Grams.",
              "counts": dict(counts), "elapsed_seconds": time.monotonic()-started,
              "records": records}
    args.output.write_text(json.dumps(output, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k != "records"}), flush=True)
    print(json.dumps({"maximum_domain_size": max(r["maximum_domain_size"] for r in records)}), flush=True)


if __name__ == "__main__":
    main()
