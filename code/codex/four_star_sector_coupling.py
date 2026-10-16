"""Separate odd rank loss and the final symmetric residual through 20 fixed labels.

All arithmetic is rational. Input objects and Q matrices are already accepted;
this computes the new coupling identity and diagnostics, not a fresh census.
"""

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_line_resonance import B, INDEX, LABELS, adjacency, records
from four_star_sym6_reduction import integer_matrix, pseudoinverse, rank


def two_coordinate_negative(matrix):
    for i, j in combinations(range(matrix.rows), 2):
        sign = -1 if matrix[i, j] > 0 else 1
        energy = matrix[i, i] + matrix[j, j] + 2 * sign * matrix[i, j]
        if energy < 0:
            return {"indices": [i, j], "values": [1, sign], "energy": str(energy)}
    return None


def one_side(item, t, pair):
    roots = (pair, pair + 1)
    letters = [a for a in range(14) if a not in roots]
    star = [INDEX[tuple(sorted((a, b)))] for a in roots for b in letters]
    fixed = [a for a in range(44) if a not in star]
    p, r = sp.zeros(44, 12), sp.zeros(44, 12)
    for j, a in enumerate(star):
        p[a, j % 12] = 1
        r[a, j % 12] = 1 if j < 12 else -1
    k, c, n = t.extract(fixed, fixed), t[fixed, :] * r, t[fixed, :] * p
    g, h, phi = p.T * t * p, p.T * t * r, r.T * t * r
    phi_inverse = pseudoinverse(phi)
    k1 = k - c * phi_inverse * c.T
    n1 = n - c * phi_inverse * h.T
    e = g - h * phi_inverse * h.T
    final = e - n1.T * pseudoinverse(k1) * n1
    corner_indices = [letters.index(a) for a in (0, 1, 2, 3) if a not in roots]
    outer = [letters.index(a) for a in range(4, 14)]
    for a in corner_indices:
        assert final[:, a] == sp.zeros(12, 1)

    # Compare the two orders of elimination; this is the new identity.
    line = item["lines"][1 if pair == 0 else 0]
    q = sp.Matrix(line["Q"]["integer_matrix"]) / line["Q"]["denominator"]
    f = q + sp.ones(20) / 12
    pp, rr = sp.zeros(20, 10), sp.zeros(20, 10)
    labels = [tuple(p) for p in line["far_labels"]]
    for a in range(4, 14):
        for root, sign in zip(roots, (1, -1)):
            j = labels.index((root, a))
            pp[j, a - 4] = 1
            rr[j, a - 4] = sign
    old_a, old_c, old_d = pp.T * f * pp, pp.T * f * rr, rr.T * f * rr
    old_z = old_a - old_c * pseudoinverse(old_d) * old_c.T
    z = final.extract(outer, outer)
    assert z == old_z
    c_line = line["component_count"]
    delta = rank(k) - rank(k1)
    assert rank(k) == 21 - c_line
    assert delta == 9 - rank(old_d)
    assert rank(t) == 32 - c_line - delta + rank(z)

    normalized = pseudoinverse(e) * final
    tau = sp.trace(normalized)
    eta = sp.trace(normalized * normalized)
    effective = tau * tau / eta if eta else sp.Integer(0)
    crude = k - c * c.T / 2
    witness = two_coordinate_negative(crude)
    if witness:
        witness["labels"] = [LABELS[fixed[j]] for j in witness["indices"]]
    mate_plus, mate_minus = sp.zeros(10, 5), sp.zeros(10, 5)
    for j in range(5):
        mate_plus[2 * j, j] = mate_plus[2 * j + 1, j] = 1
        mate_minus[2 * j, j], mate_minus[2 * j + 1, j] = 1, -1
    return {
        "odd_star_pair": roots, "base_line": line["line_root_letters"], "c_base": c_line,
        "raw_fixed_rank": rank(k), "residual_fixed_rank": rank(k1), "odd_rank_loss_delta": delta,
        "D_rank": rank(old_d), "Z_rank": rank(z), "T_rank": rank(t),
        "even12_rank": rank(e), "even_coupling_rank": rank(n1),
        "uncoupled_direction_rank_bound": rank(e) - rank(n1),
        "normalized_residual_trace": str(tau), "normalized_residual_square_trace": str(eta),
        "normalized_effective_rank": str(effective),
        "single_trace_rank_bound": int(sp.ceiling(tau)),
        "two_trace_rank_bound": int(sp.ceiling(effective)),
        "crude_half_inverse_negative_witness": witness,
        "mate_plus_compression_rank": rank(mate_plus.T * z * mate_plus),
        "mate_minus_compression_rank": rank(mate_minus.T * z * mate_minus),
        "final_even12": integer_matrix(final),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    original = json.loads(args.source.read_text(encoding="utf-8"))
    result = {"source": str(args.source), "scope": "Exact coupling reduction; SYM6 remains open.", "records": []}
    cache = {}
    for item in original["records"]:
        filename = item["source_file"]
        if filename not in cache:
            cache[filename] = dict(records(json.loads(Path(filename).read_text(encoding="utf-8"))))
        gamma = adjacency(cache[filename][item["record"]])
        t = (24 * sp.eye(44) - 8 * gamma - 3 * B.T * B
             - B.T * B[[j ^ 1 for j in range(14)], :] + 2 * sp.ones(44)) / 8
        entry = {"source_file": filename, "source_record": item["record"],
                 "grid_overlap": item["grid_overlap"], "sides": []}
        for pair in (0, 2):
            side = one_side(item, t, pair)
            entry["sides"].append(side)
            print(json.dumps({"file": Path(filename).name, "record": item["record"], "odd_pair": pair,
                              "delta": side["odd_rank_loss_delta"], "Z_rank": side["Z_rank"],
                              "uncoupled_bound": side["uncoupled_direction_rank_bound"],
                              "single_trace_bound": side["single_trace_rank_bound"],
                              "two_trace_bound": side["two_trace_rank_bound"],
                              "crude_negative_witness": side["crude_half_inverse_negative_witness"]}), flush=True)
        result["records"].append(entry)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
