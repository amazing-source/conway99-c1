"""Exact arithmetic for the lambda=1, mu=2 family synthesis, 16 October 2026.

This does not rerun any graph construction, group computation, or peer proof.
It records the five noncomplete parameter sets and the coefficients in the
component-variance, induced-grid, and five-star capacity identities.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


def family_rows() -> list[dict]:
    rows = []
    for gap in (3, 7, 9, 21, 63):
        degree = (gap * gap + 7) // 4
        half_degree = degree // 2
        order = 1 + degree * degree // 2
        positive = (gap - 1) // 2
        negative = -(gap + 1) // 2
        f = half_degree**2 + Fraction(half_degree * (half_degree - 2), gap)
        assert f.denominator == 1
        f = int(f)
        g = order - 1 - f
        assert degree + positive * f + negative * g == 0
        assert degree**2 + positive**2 * f + negative**2 * g == order * degree
        assert degree * (degree - 2) == 2 * (order - degree - 1)

        near_size = 3 * (degree - 2)
        far_size = (degree - 2) * (degree - 4) // 2
        resonance = degree - 14
        assert resonance == (positive - 3) * (3 - negative)
        # Sum n_C^2 - 2*mean*sum n_C + |F|*mean^2, coefficient of |C|^2.
        centered_c2 = (
            Fraction(5, 3)
            - Fraction(4 * (degree - 4), degree - 2)
            + Fraction(4 * far_size, (degree - 2) ** 2)
        )
        assert centered_c2 == -Fraction(resonance, near_size)

        grid_holes = (degree - 4) * (degree - 14) // 2
        assert grid_holes == order - 9 - 9 * (degree - 4)
        capacity = None
        if degree >= 14:
            x_size = degree - 6
            b_size = 4 * degree - 20
            offset = b_size - x_size * (x_size - 1) // 2
            assert offset == 8 - resonance * (resonance + 7) // 2
            capacity = {
                "base_Bprime_size": b_size,
                "X_size": x_size,
                "internal_X_edges_a_min": 0,
                "internal_X_edges_a_max": x_size // 2,
                "raw_forced_Y_labels_lower_bound": f"{offset} + a",
                "raw_bound_offset": offset,
                "interpretation": "The actual lower bound is max(0, offset+a).",
            }

        rows.append({
            "v": order,
            "k": degree,
            "lambda": 1,
            "mu": 2,
            "spectral_gap": gap,
            "restricted_eigenvalues": [positive, negative],
            "restricted_multiplicities": [f, g],
            "line_neighborhood_M_size": near_size,
            "far_from_line_F_size": far_size,
            "component_variance_coefficient_k_minus_14": resonance,
            "component_variance": "(k-14)*c*(1-c/(3*(k-2)))",
            "component_variance_mean": "2*c/(k-2) (F is empty at k=4)",
            "induced_grid_external_vertices_without_grid_neighbor": grid_holes,
            "induced_grid_external_vertices_with_one_grid_neighbor": 9 * (degree - 4),
            "five_star_capacity": capacity,
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = family_rows()
    payload = {
        "date": "2026-10-16",
        "scope": "Exact arithmetic and algebra for a synthesis; no new graph exclusion.",
        "parameter_completeness": (
            "For a noncomplete SRG(v,k,1,2), integral multiplicities imply an odd "
            "spectral gap d dividing 63. The d=1 case is complete K3 and is omitted."
        ),
        "hypotheses": {
            "component": "C is a whole component or union of components of G[N(line) minus line].",
            "grid": "An induced 3 by 3 grid is present; its existence is not assumed universally.",
            "capacity": "The four-star/fifth-star setup of LAB 918-920, k >= 14.",
        },
        "rows": rows,
        "checks": "Spectral traces, SRG feasibility, and centered-variance polynomial coefficients exact over Q.",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        capacity = row["five_star_capacity"]
        offset = capacity["raw_bound_offset"] if capacity else "n/a"
        print(f"v={row['v']:6d} k={row['k']:3d} d={row['spectral_gap']:2d} "
              f"r,s={row['restricted_eigenvalues']} f,g={row['restricted_multiplicities']} "
              f"k-14={row['component_variance_coefficient_k_minus_14']:3d} "
              f"grid_holes={row['induced_grid_external_vertices_without_grid_neighbor']:6d} "
              f"capacity_offset={offset}")


if __name__ == "__main__":
    main()
