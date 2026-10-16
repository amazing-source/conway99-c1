"""Normalize complete Gram covers under template-preserving root relabelings.

This chooses labels, not automorphisms of a completed graph. The action keeps
the component template, root prism budget and every C1/C2 equation invariant.
"""

import argparse
from collections import Counter
import json
from math import lcm
from pathlib import Path
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_quotient import graph_automorphisms


def normalized_groups(groups):
    return tuple(tuple(sorted(tuple(sorted(part)) for part in row)) for row in groups)


def quotient(template, record):
    assert record["exhaustive"] and record["usable_as_gram_cover"]
    started = time.monotonic()
    groups = normalized_groups(template["nontrivial_component_groups"])
    automorphisms = []
    for permutation in graph_automorphisms(template["graph_mask"]):
        image = [[] for _ in range(7)]
        for i, row in enumerate(groups):
            image[permutation[i]] = [[permutation[j] for j in part] for part in row]
        if normalized_groups(image) == groups:
            automorphisms.append(permutation)
    edges = [tuple(e) for e in template["nongrid_edges"]]
    edge_index = {edge: i for i, edge in enumerate(edges)}
    lift = sp.Matrix([[sp.Rational(*x) for x in row] for row in record["lift_matrix"]])
    anchors = record["anchors"]
    pairs = [tuple(p) for p in record["anchor_pairs"]]
    transforms = []
    for permutation in automorphisms:
        edge_permutation = [edge_index[tuple(sorted((permutation[a], permutation[b])))] for a, b in edges]
        inverse = [edge_permutation.index(i) for i in range(len(edges))]
        rows = []
        for i, j in pairs:
            a, b = inverse[anchors[i]], inverse[anchors[j]]
            rows.append([lift[a, u] * lift[b, v] + (lift[a, v] * lift[b, u] if u != v else 0)
                         for u, v in pairs])
        denominator = lcm(*(int(x.q) for row in rows for x in row))
        transforms.append(([[int(x * denominator) for x in row] for row in rows], denominator))
    all_values = {tuple(values) for values in record["gram_anchor_values"]}
    assert len(all_values) == record["gram_count"]
    unseen = set(all_values)
    representatives, sizes = [], []
    for representative in sorted(all_values):
        if representative not in unseen:
            continue
        orbit = set()
        for matrix, denominator in transforms:
            numerator = [sum(c * x for c, x in zip(row, representative)) for row in matrix]
            assert all(x % denominator == 0 for x in numerator)
            orbit.add(tuple(x // denominator for x in numerator))
        assert orbit.issubset(all_values)
        assert orbit.issubset(unseen)
        assert representative == min(orbit)
        unseen.difference_update(orbit)
        representatives.append(list(representative))
        sizes.append(len(orbit))
    assert not unseen and sum(sizes) == record["gram_count"]
    result = dict(record)
    result.update(status="EXHAUSTIVE_UP_TO_ROOT_RELABELING", exhaustive=True,
                  usable_as_gram_cover=True, coverage_up_to_template_relabeling=True,
                  input_gram_count=record["gram_count"], root_automorphisms=automorphisms,
                  gram_count=len(representatives), gram_anchor_values=representatives,
                  gram_orbit_sizes=sizes, orbit_size_histogram=dict(Counter(sizes)),
                  quotient_seconds=time.monotonic() - started)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("templates", type=Path)
    parser.add_argument("grams", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    templates = json.loads(args.templates.read_text(encoding="utf-8"))["survivors"]
    data = json.loads(args.grams.read_text(encoding="utf-8"))
    records = []
    for original in data["records"]:
        index = original["template_index"]
        record = quotient(templates[index], original)
        records.append(record)
        print(json.dumps({"template_index": index, "root_relabelings": len(record["root_automorphisms"]),
                          "input_grams": record["input_gram_count"], "gram_orbits": record["gram_count"],
                          "seconds": record["quotient_seconds"]}), flush=True)
    data.update(scope="Complete necessary Gram cover up to component-template-preserving root relabeling; no graph automorphism assumed.", records=records)
    args.output.write_text(json.dumps(data, separators=(",", ":")) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
