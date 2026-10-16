"""Expose the exact corner term in the symmetric sector of a four-star block.

Uses accepted objects already named by a line-resonance certificate. This
computes a new boundary elimination; it does not rerun graph certification.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_line_resonance import B, INDEX, LABELS, adjacency, components, records
from four_star_sym6_reduction import integer_matrix, pseudoinverse, rank


def laplacian_components(matrix):
    return components(sp.Matrix(matrix.rows, matrix.cols,
                                lambda i, j: 1 if i != j and matrix[i, j] < 0 else 0))


def analyze(item, gamma):
    t = (24 * sp.eye(44) - 8 * gamma - 3 * B.T * B
         - B.T * B[[j ^ 1 for j in range(14)], :] + 2 * sp.ones(44)) / 8
    corners = [INDEX[p] for p in ((0, 2), (0, 3), (1, 2), (1, 3))]
    corner_edges = sum(gamma[i, j] for i in corners for j in corners) // 2
    mate = sp.Matrix(10, 10, lambda i, j: int(j == (i ^ 1)))
    answer = []
    for line_number, line in enumerate(item["lines"]):
        roots = (2, 3) if line["line_root_letters"][0] == 0 else (0, 1)
        y = [INDEX[(a, s)] for a in roots for s in range(4, 14)]
        x = [i for i in range(44) if i not in y]
        p = sp.eye(10).col_join(sp.eye(10))
        u = sp.Matrix([int(i in corners) for i in x])
        tx = t.extract(x, x)
        k = t.extract(x, y) * p
        g = p.T * t.extract(y, y) * p
        rho = p.T * gamma.extract(y, corners) * sp.ones(4, 1)
        boundary = sum(rho)
        assert g == sp.Rational(9, 2) * sp.eye(10) - mate / 2 - p.T * gamma.extract(y, y) * p
        assert g * sp.ones(10, 1) == rho
        assert boundary == 8 - 2 * corner_edges
        assert (u.T * tx * u)[0] == boundary
        assert k.T * u == -rho
        groups = laplacian_components(g)
        ungrounded = [group for group in groups if all(rho[i] == 0 for i in group)]
        other_c = item["lines"][1 - line_number]["component_count"]
        assert len(ungrounded) == other_c - 1
        assert rank(g) == 11 - other_c

        # Use the previously computed Q in its own label order.
        q = sp.Matrix(line["Q"]["integer_matrix"]) / line["Q"]["denominator"]
        old_y = [INDEX[tuple(label)] for label in line["far_labels"]]
        reorder = [old_y.index(i) for i in y]
        f = (q + sp.ones(20) / 12).extract(reorder, reorder)
        a = p.T * f * p
        result = {
            "line": line["line_root_letters"],
            "c_line": line["component_count"], "c_other_line": other_c,
            "corner_edges": int(corner_edges), "boundary_mass": int(boundary),
            "rho": list(map(int, rho)), "G_rank": rank(g), "A_rank": rank(a),
            "G_components": [[s + 4 for s in group] for group in groups],
            "G_ungrounded_components": [[s + 4 for s in group] for group in ungrounded],
            "G": integer_matrix(g),
        }
        if boundary:
            ell = g - rho * rho.T / boundary
            txu = tx * u
            residual_x = tx - txu * txu.T / boundary
            residual_k = k + txu * rho.T / boundary
            assert ell * sp.ones(10, 1) == sp.zeros(10, 1)
            assert all(ell[i, j] <= 0 for i in range(10) for j in range(10) if i != j)
            assert len(laplacian_components(ell)) == other_c
            assert rank(ell) == 10 - other_c
            assert rank(residual_x) == 22 - line["component_count"]
            assert a == ell - residual_k.T * pseudoinverse(residual_x) * residual_k
            result.update({
                "L_rank": rank(ell), "L": integer_matrix(ell),
                "L_components": [[s + 4 for s in group] for group in laplacian_components(ell)],
                "remaining_X_rank": rank(residual_x),
                "rank_lost_after_corner_elimination": rank(ell) - rank(a),
            })
        else:
            assert tx * u == sp.zeros(tx.rows, 1)
            result["L_rank"] = None
        answer.append(result)
    return answer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    original = json.loads(args.source.read_text(encoding="utf-8"))
    cache = {}
    result = {"source": str(args.source), "scope": "New corner identity, not a proof of SYM6.", "records": []}
    for item in original["records"]:
        filename = item["source_file"]
        if filename not in cache:
            cache[filename] = dict(records(json.loads(Path(filename).read_text(encoding="utf-8"))))
        gamma = adjacency(cache[filename][item["record"]])
        record = {"source_file": filename, "source_record": item["record"],
                  "grid_overlap": item["grid_overlap"], "lines": analyze(item, gamma)}
        result["records"].append(record)
        for line in record["lines"]:
            print(json.dumps({"file": Path(filename).name, "record": item["record"],
                              "side": line["line"], "boundary_mass": line["boundary_mass"],
                              "G_rank": line["G_rank"], "L_rank": line["L_rank"],
                              "A_rank": line["A_rank"]}), flush=True)
    result["seconds"] = time.monotonic() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"objects": len(result["records"]), "seconds": result["seconds"]}))


if __name__ == "__main__":
    main()
