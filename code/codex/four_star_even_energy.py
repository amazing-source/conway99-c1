"""Compute the new one-fifth lower bound after eliminating a full odd sector.

The proof uses the 2-regular graph on two stars, not an empirical census.
This script records exact matrices for the previously available examples.
"""

import argparse
import json
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_line_resonance import B, INDEX, adjacency, records
from four_star_sym6_reduction import integer_matrix, pseudoinverse, rank


def positive_pivots(matrix):
    """Exact congruence pivots for the new inequality, with a zero remainder."""
    work = matrix.copy()
    pivots = []
    while work.rows:
        assert all(work[i, i] >= 0 for i in range(work.rows))
        candidates = [i for i in range(work.rows) if work[i, i] > 0]
        if not candidates:
            assert work == sp.zeros(work.rows)
            break
        i = candidates[0]
        work.row_swap(0, i)
        work.col_swap(0, i)
        pivot = work[0, 0]
        pivots.append(str(pivot))
        work = work[1:, 1:] - work[1:, :1] * work[:1, 1:] / pivot
    return pivots


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    original = json.loads(args.source.read_text(encoding="utf-8"))
    result = {"source": str(args.source), "bound": "even_schur >= G/5 + (2/5)(I-M)", "records": []}
    cache = {}
    for item in original["records"]:
        filename = item["source_file"]
        if filename not in cache:
            cache[filename] = dict(records(json.loads(Path(filename).read_text(encoding="utf-8"))))
        gamma = adjacency(cache[filename][item["record"]])
        t = (24 * sp.eye(44) - 8 * gamma - 3 * B.T * B
             - B.T * B[[j ^ 1 for j in range(14)], :] + 2 * sp.ones(44)) / 8
        entry = {"source_file": filename, "source_record": item["record"], "stars": []}
        for side_number, roots in enumerate(((0, 1), (2, 3))):
            letters = [s for s in range(14) if s not in roots]
            idx = [INDEX[tuple(sorted((a, s)))] for a in roots for s in letters]
            mate = sp.Matrix(12, 12, lambda i, j: int(letters[int(j)] == (letters[int(i)] ^ 1)))
            p = sp.eye(12).col_join(sp.eye(12))
            r = sp.eye(12).col_join(-sp.eye(12))
            block = t.extract(idx, idx)
            g, h, phi = p.T * block * p, p.T * block * r, r.T * block * r
            even = g - h * pseudoinverse(phi) * h.T
            margin = even - g / 5 - sp.Rational(2, 5) * (sp.eye(12) - mate)
            pivots = positive_pivots(margin)
            c = item["lines"][side_number]["component_count"]
            assert rank(even) == rank(g) == 12 - c
            data = {"roots": roots, "component_count": c, "G_rank": rank(g),
                    "even_schur_rank": rank(even), "margin_rank": len(pivots),
                    "margin_positive_congruence_pivots": pivots,
                    "margin": integer_matrix(margin)}
            entry["stars"].append(data)
            print(json.dumps({"file": Path(filename).name, "record": item["record"],
                              "roots": roots, "G_rank": rank(g), "even_rank": rank(even),
                              "margin_rank": len(pivots)}), flush=True)
        result["records"].append(entry)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
