"""Exact scalar consequence of the prism cap: >=254 non-grid low-line blocks.

No local graph is read or tested. The accompanying proof uses the spectrum
18^1, 7^54, 0^44, (-3)^132 of the line intersection graph, and the fact that
distinct grids through a line use disjoint pairs of its prisms.
"""

import argparse
from fractions import Fraction as F
import json
from math import ceil, floor
from pathlib import Path


def derive(prism_cap=852):
    line_count = 231
    deficit = 8 * line_count - 2 * prism_cap
    assert deficit > 0
    smallest_low_set = ceil(F(deficit, 8))
    cases = []
    for size in range(smallest_low_set, line_count + 1):
        # t <= 7 on the selected lines; t >= 8 on all other lines.
        low_prism_sum_upper = min(7 * size, 8 * size - deficit)
        # Each low line has at most 3 grids, and two prisms per grid.
        grid_incidence_upper = min(3 * size, low_prism_sum_upper // 2)
        nongrid_line_incidences = 18 * size - 3 * grid_incidence_upper
        # The largest nontrivial eigenvalue of the line graph is 7.
        meeting_pairs_upper = floor(F(7 * size, 2) + F(size * size, 42))
        meeting_pairs_upper = min(meeting_pairs_upper, size * (size - 1) // 2)
        block_lower = max(ceil(F(nongrid_line_incidences, 2)),
                          nongrid_line_incidences - meeting_pairs_upper)
        cases.append(dict(
            low_lines=size,
            low_prism_sum_upper=low_prism_sum_upper,
            nongrid_low_line_incidences_lower=nongrid_line_incidences,
            low_line_meeting_pairs_upper=meeting_pairs_upper,
            distinct_nongrid_low_line_blocks_lower=block_lower,
        ))
    minimum = min(row["distinct_nongrid_low_line_blocks_lower"] for row in cases)
    if prism_cap == 852:
        assert smallest_low_set == 18 and minimum == 254
    return dict(
        status="EXACT_NECESSARY_CONSEQUENCE_NOT_A_CONWAY_EXCLUSION",
        prism_cap=prism_cap,
        total_lines=line_count,
        total_four_star_flags=2079,
        low_line_definition="t(line) <= 7",
        low_lines_lower=smallest_low_set,
        nongrid_blocks_with_a_low_line_lower=minimum,
        extremal_scalar_cases=[row for row in cases if
                              row["distinct_nongrid_low_line_blocks_lower"] == minimum],
        missing_sufficient_statement=(
            "No non-grid four-star object with min(t_l,t_m)<=7 passes all "
            "necessary Conway block conditions. This statement is OPEN."
        ),
        hypotheses=[
            "Conway SRG parameters (99,14,1,2)",
            "sum_line t(line)=2P and P<=prism_cap",
            "A line occurs in 18 four-star flags",
            "A grid through a line contributes 3 of those flags and 2 distinct prisms",
            "Each prism belongs to at most one grid",
            "Line intersection graph has degree18 and largest nontrivial eigenvalue7",
        ],
        proof_formulas={
            "deficit": "sum_low(8-t) >= 1848-2P",
            "incidence_bound_at_852": "I >= max(9m,6m+216)",
            "spectral_edge_bound": "e(low) <= floor(7m/2+m^2/42)",
            "block_bound": "N >= max(ceil(I/2), I-e(low))",
        },
        all_cardinalities=cases,
        sharpness="254 is the minimum of these scalar lower bounds; no realizing graph or optimality for actual Conway blocks is asserted.",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prism-cap", type=int, default=852)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = derive(args.prism_cap)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "all_cardinalities"}, indent=2))
