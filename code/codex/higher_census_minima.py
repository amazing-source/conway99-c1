"""Exact dual certificates for lower bounds on raw large-support counts.

Floating-point LP only selects a candidate support. Every accepted bound
is then proved by nonnegative rational multipliers and an exact identity.
These are counts of representatives, not counts of distinct vectors in M.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

import numpy as np
from scipy.optimize import linprog
from sympy import Matrix, Rational, Symbol, sympify

ROOT = Path(__file__).resolve().parents[2]


def certify(rows, objective):
    c = np.array([float(x) for x in objective[1:]])
    coeff = np.array([[float(x) for x in row[1:]] for _, row in rows])
    constants = np.array([float(row[0]) for _, row in rows])
    result = linprog(c, A_ub=-coeff, b_ub=constants, bounds=[(None, None)]*len(c), method='highs')
    point_scale = 1.0
    dual_scale = np.ones(len(rows))
    if not result.success:
        # Degenerate conditional faces can be reported numerically infeasible
        # despite an exact feasible witness. Scale discovery only; certificates
        # below always use the original rational rows.
        point_scale = 10**6
        row_scale = np.maximum(1, np.maximum(np.abs(constants), np.max(np.abs(coeff)*point_scale, axis=1)))
        objective_scale = max(1, np.max(np.abs(c)*point_scale))
        result = linprog(c*point_scale/objective_scale,
                         A_ub=-coeff*point_scale/row_scale[:, None],
                         b_ub=constants/row_scale, bounds=[(None, None)]*len(c),
                         method='highs', options={'primal_feasibility_tolerance': 1e-9,
                                                  'dual_feasibility_tolerance': 1e-9})
        dual_scale = objective_scale/row_scale
    assert result.success, result.message
    support = [i for i, w in enumerate(-result.ineqlin.marginals*dual_scale) if w > 1e-8]
    matrix = Matrix([[Rational(rows[i][1][j]) for i in support] for j in range(1, len(objective))])
    target = Matrix(list(map(Rational, objective[1:])))
    weights, free = matrix.gauss_jordan_solve(target)
    if free:
        weights = weights.subs({p: 0 for p in free})
    weights = list(map(F, weights))
    assert all(w >= 0 for w in weights)
    identity = [sum(w*rows[i][1][j] for i, w in zip(support, weights)) for j in range(len(objective))]
    assert identity[1:] == objective[1:]
    bound = objective[0]-identity[0]
    # A rationalised floating optimum is accepted as a witness only if all
    # constraints and the objective equality hold EXACTLY.
    point = [F(float(x)*point_scale).limit_denominator(10**6) for x in result.x]
    feasible = all(row[0]+sum(x*y for x, y in zip(row[1:], point)) >= 0 for _, row in rows)
    attaining = feasible and objective[0]+sum(x*y for x, y in zip(objective[1:], point)) == bound
    return {'lower_bound': str(bound),
            'certificate': [(rows[i][0], str(w)) for i, w in zip(support, weights) if w],
            'verified_identity_coefficients': list(map(str, identity)),
            'rational_point_attaining_bound': list(map(str, point)) if attaining else None,
            'numerical_discovery_value': float(objective[0])+float(c @ (result.x*point_scale)),
            'scope': 'Exact rational lower certificate; numerical discovery is not used as proof.'}


def run(n):
    source = json.loads((ROOT/f'data/codex_order{n}_census.json').read_text())
    params = [Symbol(p) for p in source['parameters']]
    rows = [(str(r['code']), list(map(F, r['affine']))) for r in source['counts']]
    rows += [('P>=0', [F(0), F(1)]+[F(0)]*(len(params)-1)),
             ('P<=1386', [F(1386), F(-1)]+[F(0)]*(len(params)-1))]
    families = {k: sympify(v) for k, v in source['families']['signed_representative_counts'].items()}
    for norm in (6, 8):
        selected = [v for k, v in families.items() if k.startswith(f'Q{norm}_')]
        if selected:
            families[f'Q{norm}_TOTAL'] = sum(selected)
    if n == 9:
        for weight in (Rational(1), Rational(5), Rational(10), Rational(651, 34), Rational(20), Rational(50)):
            families[f'Q8_PLUS_{weight}_Q6'] = families['Q8_TOTAL']+weight*families['Q6_TOTAL']
    report = {}
    for name, expr in families.items():
        zero = expr.subs({p: 0 for p in params})
        objective = [F(str(zero))]+[F(str(expr.coeff(p))) for p in params]
        result = certify(rows, objective)
        result['objective'] = list(map(str, objective))
        report[name] = result
        print(name, '>=', result['lower_bound'], '; attaining point:', result['rational_point_attaining_bound'] is not None, flush=True)
    (ROOT/f'data/codex_order{n}_raw_family_minima.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--order', type=int, choices=(8, 9), default=8)
    run(parser.parse_args().order)
