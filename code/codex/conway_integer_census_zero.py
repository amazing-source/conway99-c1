"""Seek integer P=0 counts in the supplied censuses, without building a graph.

Only a bounded box around our earlier rational census point is searched.
An infeasible box is not an infeasible census. A returned point is evaluated
exactly against all supplied affine counts of orders seven, eight and nine.
The census identities themselves are accepted, not regenerated or audited.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb, gcd, lcm
from pathlib import Path
import time

from ortools.sat.python import cp_model


def investigate(source, seed, radius=1000, seconds=20):
    started = time.monotonic()
    source = Path(source)
    original = json.loads(Path(seed).read_text(encoding="utf-8"))
    filenames = {
        7: "codex_seven_vertex_census.json",
        8: "codex_order8_census.json",
        9: "codex_order9_census.json",
    }
    census, hashes = {}, {}
    for order, filename in filenames.items():
        raw = (source / filename).read_bytes()
        census[order] = json.loads(raw)
        hashes[str(order)] = sha256(raw).hexdigest()
    names = census[9]["parameters"]
    lookup = {name: i for i, name in enumerate(names)}
    rational = [F(original["point"][name]) for name in names]
    base = [v.numerator // v.denominator for v in rational]

    model = cp_model.CpModel()
    bounds = [(max(-radius, -b), radius) for b in base]
    bounds[lookup["P"]] = (0, 0)
    variables = [model.NewIntVar(lo, hi, name) for name, (lo, hi)
                 in zip(names, bounds)]
    for var, q, b in zip(variables, rational, base):
        model.AddHint(var, round(q) - b)

    rows = []
    congruences = set()
    active_inequalities = 0
    for order, data in census.items():
        positions = [lookup[name] for name in data["parameters"]]
        for row in data["counts"]:
            coefficients = [F(x) for x in row["affine"]]
            denominator = lcm(*(c.denominator for c in coefficients))
            constant = int(coefficients[0] * denominator)
            terms = [(j, int(c * denominator)) for j, c in
                     zip(positions, coefficients[1:]) if c]
            offset = constant + sum(c * base[j] for j, c in terms)
            rows.append((order, row["code"], denominator, constant, terms))
            low = offset + sum(c * bounds[j][int(c < 0)] for j, c in terms)
            if low < 0:
                model.Add(sum(c * variables[j] for j, c in terms) >= -offset)
                active_inequalities += 1

            # Integrality is a small congruence, even for very large counts.
            residues = [(j, c % denominator) for j, c in terms
                        if c % denominator]
            residue = offset % denominator
            divisor = gcd(denominator, gcd(residue, gcd(*(c for _, c in residues))))
            modulus = denominator // divisor
            if modulus == 1:
                continue
            residue //= divisor
            residues = [(j, c // divisor) for j, c in residues]
            key = (modulus, residue, tuple(residues))
            if key in congruences:
                continue
            congruences.add(key)
            lo = residue + sum(c * bounds[j][0] for j, c in residues)
            hi = residue + sum(c * bounds[j][1] for j, c in residues)
            quotient = model.NewIntVar(-((-lo) // modulus), hi // modulus,
                                       f"congruence_{len(congruences)}")
            model.Add(residue + sum(c * variables[j] for j, c in residues)
                      == modulus * quotient)

    problem_error = model.Validate()
    if problem_error:
        raise ValueError(problem_error)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 15
    status = solver.Solve(model)
    report = dict(
        status=solver.StatusName(status), radius=radius,
        seconds_limit=seconds, workers=1,
        supplied_source=str(source.resolve()), source_sha256=hashes,
        seed=str(Path(seed).resolve()),
        parameters=len(names), total_counts=len(rows),
        distinct_congruences=len(congruences),
        active_nonnegativity_inequalities=active_inequalities,
        model_scope="For each parameter x: x=floor(seed_x)+delta, -radius<=delta<=radius, x>=0, P=0.",
        not_a_graph=True,
    )
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        point = [b + solver.Value(x) for b, x in zip(base, variables)]
        summaries = {n: dict(types=0, zero=0, total=0, minimum=None)
                     for n in census}
        for order, code, denominator, constant, terms in rows:
            numerator = constant + sum(c * point[j] for j, c in terms)
            if numerator < 0 or numerator % denominator:
                raise AssertionError((order, code, numerator, denominator))
            value = numerator // denominator
            result = summaries[order]
            result["types"] += 1
            result["zero"] += (value == 0)
            result["total"] += value
            result["minimum"] = value if result["minimum"] is None else min(result["minimum"], value)
        for order, result in summaries.items():
            assert result["total"] == comb(99, order)
        assert point[lookup["P"]] == 0 and min(point) >= 0
        report.update(
            status="EXACT_NONNEGATIVE_INTEGER_P_ZERO_CENSUS_POINT",
            point=dict(zip(names, point)),
            exact_evaluation=summaries,
            all_counts_integer_and_nonnegative=True,
            max_distance_from_seed=str(max(abs(F(v)-q) for v, q in zip(point, rational))),
            conclusion="The supplied order7/8/9 census admits integer nonnegative counts at P=0; global realization and block PSD/ranks are not asserted.",
        )
    else:
        report["conclusion"] = "No integer point returned from this bounded box; no census or graph exclusion follows."
    report["elapsed_seconds"] = time.monotonic() - started
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--seed", required=True)
    parser.add_argument("--radius", type=int, default=1000)
    parser.add_argument("--seconds", type=float, default=20)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = investigate(args.source, args.seed, args.radius, args.seconds)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "point"}, indent=2))
