"""New 10x10 Schur form of SYM6, using previously computed exact Q matrices.

No graph producer or peer census is rerun. This explores the symmetric and
antisymmetric sectors of the invariant introduced in LAB925 and LAB928.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from math import ceil, lcm
from pathlib import Path
import time

import sympy as sp


def rank(matrix):
    return len(matrix.rref()[1])


def pseudoinverse(matrix):
    kernel = matrix.nullspace()
    if not kernel:
        return matrix.inv(method="DM")
    basis = sp.Matrix.hstack(*kernel)
    projector = basis * (basis.T * basis).inv(method="DM") * basis.T
    answer = (matrix + projector).inv(method="DM") - projector
    assert matrix * answer == sp.eye(matrix.rows) - projector
    return answer


def integer_matrix(matrix):
    denominator = lcm(*(int(x.q) for x in matrix))
    return {"denominator": denominator,
            "numerator": [[int(x * denominator) for x in row] for row in matrix.tolist()]}


def statistics(matrix):
    trace = sp.trace(matrix)
    square_trace = sp.trace(matrix * matrix)
    effective_rank = trace**2 / square_trace if square_trace else sp.Integer(0)
    values = Counter("positive" if matrix[i, j] > 0 else "negative" if matrix[i, j] < 0 else "zero"
                     for i in range(matrix.rows) for j in range(i + 1, matrix.cols))
    return {"rank": rank(matrix), "trace": str(trace), "trace_square": str(square_trace),
            "effective_rank": str(effective_rank), "trace_rank_lower_bound": int(ceil(effective_rank)),
            "off_diagonal_signs": dict(values),
            "zero_rows": [i for i in range(matrix.rows) if all(matrix[i, j] == 0 for j in range(matrix.cols))],
            "row_sums": sorted(set(str(x) for x in matrix * sp.ones(matrix.rows, 1))),
            **integer_matrix(matrix)}


def analyze(line):
    q = sp.Matrix(line["Q"]["integer_matrix"]) / line["Q"]["denominator"]
    f = q + sp.ones(20) / 12
    side = line["line_root_letters"][0]
    roots = (2, 3) if side == 0 else (0, 1)
    labels = [tuple(p) for p in line["far_labels"]]
    plus, minus = sp.zeros(20, 10), sp.zeros(20, 10)
    for s in range(4, 14):
        for r, sign in zip(roots, (1, -1)):
            i = labels.index((r, s))
            plus[i, s - 4] = 1
            minus[i, s - 4] = sign
    a, c, d = plus.T * f * plus, plus.T * f * minus, minus.T * f * minus
    for vector in d.nullspace():
        assert c * vector == sp.zeros(10, 1)
    z = a - c * pseudoinverse(d) * c.T
    other = d - c.T * pseudoinverse(a) * c
    assert f * plus * sp.ones(10, 1) == sp.zeros(20, 1)
    assert f * minus * sp.ones(10, 1) == sp.zeros(20, 1)
    kernel_q = sp.Matrix(line["Q"]["integer_kernel_basis"]).T
    symdim = rank(plus.T * kernel_q)
    odddim = rank(minus.T * kernel_q)
    assert symdim == 9 - rank(z)
    assert odddim == 10 - rank(other)
    assert rank(f) == rank(d) + rank(z)
    return {
        "line_root_letters": line["line_root_letters"],
        "component_count": line["component_count"],
        "Q_corank": line["Q"]["corank"],
        "F_rank": rank(f),
        "symmetric_projection_dimension": symdim,
        "antisymmetric_projection_dimension": odddim,
        "SYM6_holds": symdim <= 6,
        "ODDCONST_holds": odddim == 1,
        "weaker_odd_condition_D_rank9": rank(d) == 9,
        "A": statistics(a),
        "D": statistics(d),
        "Z_SYM6": statistics(z),
        "W_ODDCONST": statistics(other),
        "C": integer_matrix(c),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    original = json.loads(args.source.read_text(encoding="utf-8"))
    result = {"source": str(args.source), "scope": "New sector invariants, not a new Conway exclusion.", "records": []}
    for item in original["records"]:
        record = {"source_file": item["source_file"], "source_record": item["record"],
                  "grid_overlap": item["grid_overlap"], "lines": [analyze(line) for line in item["lines"]]}
        result["records"].append(record)
        for line in record["lines"]:
            print(json.dumps({"file": Path(item["source_file"]).name, "record": item["record"],
                              "grid": item["grid_overlap"], "side": line["line_root_letters"],
                              "c": line["component_count"], "symdim": line["symmetric_projection_dimension"],
                              "odddim": line["antisymmetric_projection_dimension"],
                              "D_rank": line["D"]["rank"], "Z_rank": line["Z_SYM6"]["rank"],
                              "Z_trace_bound": line["Z_SYM6"]["trace_rank_lower_bound"],
                              "Z_signs": line["Z_SYM6"]["off_diagonal_signs"]}), flush=True)
    result["seconds"] = time.monotonic() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"objects": len(result["records"]), "seconds": result["seconds"]}), flush=True)


if __name__ == "__main__":
    main()
