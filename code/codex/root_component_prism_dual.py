"""Extract rational linear lower bounds on the number of root prisms.

The floating-point LP only proposes multipliers. The recorded lower bound
is recomputed with fractions and valid for every x in [0,1]^3486 satisfying
the component/C1 rows. No floating-point feasibility verdict is used.
"""

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import sys

from ortools.linear_solver import pywraplp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_propagation import LABELS, PAIRS, RECTANGLES, VARIABLE, constraints


def encoded(value):
    return [value.numerator, value.denominator]


def flip_orbits():
    """Edge orbits under the seven independent swaps of root mate letters."""
    label_index = {label: i for i, label in enumerate(LABELS)}
    representatives = []
    for a, b in PAIRS:
        roots = sorted({v // 2 for v in LABELS[a] + LABELS[b]})
        images = []
        for mask in range(1 << len(roots)):
            flip = {root: (mask >> j) & 1 for j, root in enumerate(roots)}
            endpoints = [label_index[tuple(v ^ flip[v // 2] for v in LABELS[w])] for w in (a, b)]
            images.append(VARIABLE[tuple(sorted(endpoints))])
        representatives.append(min(images))
    unique = sorted(set(representatives))
    numbers = {value: i for i, value in enumerate(unique)}
    mapping = [numbers[value] for value in representatives]
    assert len(unique) == 378
    return mapping


def certificate(template):
    equations, bounds, initial = constraints(template)
    equations += [((i,), value, ["grid", i]) for i, value in sorted(initial.items())]
    orbit = flip_orbits()
    solver = pywraplp.Solver.CreateSolver("GLOP")
    variables = [solver.NumVar(0, 1, f"o{i}") for i in range(max(orbit) + 1)]
    rows = []
    seen = set()
    for relation, source in (("eq", equations), ("le", bounds)):
        for indices, target, reason in source:
            indices = tuple(sorted(orbit[i] for i in indices))
            key = (relation, indices, target)
            if key in seen:
                continue
            seen.add(key)
            row = solver.Constraint(target if relation == "eq" else -solver.infinity(), target)
            for i, coefficient in Counter(indices).items():
                row.SetCoefficient(variables[i], coefficient)
            rows.append((row, relation, indices, target, reason))
    objective = [0] * len(variables)
    for corners in RECTANGLES.values():
        for a, b in combinations(corners, 2):
            if set(LABELS[a]) & set(LABELS[b]):
                objective[orbit[VARIABLE[a, b]]] += 1
    obj = solver.Objective()
    for i, coefficient in enumerate(objective):
        obj.SetCoefficient(variables[i], coefficient)
    obj.SetMinimization()
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        return {"status": "LP_NO_OPTIMUM", "raw_status": status}
    residual = list(map(Fraction, objective))
    lower = Fraction(0)
    terms = []
    for row, relation, indices, target, reason in rows:
        # A COMMON denominator prevents enormous least common multiples on
        # degenerate dual solutions. Any rational rounding remains sound,
        # because the residual is retained and bounded exactly below.
        multiplier = Fraction(round(row.DualValue() * 1000000), 1000000)
        if relation == "le":
            multiplier = min(multiplier, Fraction(0))
        if not multiplier:
            continue
        lower += multiplier * target
        for i in indices:
            residual[i] -= multiplier
        terms.append({"relation": relation, "indices": list(indices), "target": target,
                      "multiplier": encoded(multiplier), "reason": reason})
    lower += sum(min(x, 0) for x in residual)
    # This identity and the signs establish the lower bound exactly.
    for term in terms:
        assert term["relation"] == "eq" or Fraction(*term["multiplier"]) <= 0
    return {"status": "EXACT_LINEAR_LOWER_BOUND", "lower_bound": encoded(lower),
            "integer_prism_lower_bound": -(-lower.numerator // lower.denominator),
            "excludes_budget51": lower > 51, "lp_objective_informational": obj.Value(),
            "terms": terms,
            "residual_coefficients": [[i, encoded(x)] for i, x in enumerate(residual) if x],
            "variable_bounds": [0, 1], "objective_coefficients": [[i, x] for i, x in enumerate(objective) if x],
            "quotient_variables": len(variables), "quotient_rows": len(rows),
            "proof_identity": "objective = sum(multiplier*row_lhs) + sum(residual_i*x_i); use row_eq, negative*row_le, and 0<=x<=1."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("templates", type=Path)
    parser.add_argument("--indices", nargs="+", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    templates = json.loads(args.templates.read_text(encoding="utf-8"))["survivors"]
    records = []
    for index in args.indices:
        record = {"template_index": index, **certificate(templates[index])}
        records.append(record)
        print(json.dumps({k: v for k, v in record.items() if k not in (
            "terms", "residual_coefficients", "objective_coefficients", "proof_identity")}), flush=True)
    args.output.write_text(json.dumps({"scope": "Rational linear certificates for selected component templates.",
                                      "symmetry_argument": "Only the LINEAR relaxation is averaged over independent root mate flips. Its constraints and prism objective are invariant, so every graph yields a fractional invariant solution. No graph automorphism is assumed.",
                                      "edge_to_flip_orbit": flip_orbits(),
                                      "records": records}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
