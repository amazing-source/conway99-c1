"""Exact Farkas certificates for a Gram-free rectangle count design.

The LP proposes multipliers only. Certification uses integer arithmetic:
nonnegative combinations of the E3 upper bounds, plus arbitrary multiples
of count/moment equalities, give a nonnegative expression <= a negative
constant. No floating infeasibility verdict is used as a certificate.
"""

import argparse
from fractions import Fraction
from functools import reduce
import hashlib
from itertools import combinations, combinations_with_replacement
import json
import math
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortools.linear_solver import pywraplp
from sympy import Matrix
from root_component_z_distribution import RECTANGLES
from root_component_resources import atomic_json_write, limit_research_process


def linear_system(template, catalogue, degree_histograms=False):
    columns = [(qi, si, state) for qi, item in enumerate(catalogue['row_types'])
               for si, state in enumerate(item['states'])]
    equations, bounds = [], []
    def equation(coefficients, target, kind, indices):
        assert any(coefficients) or target == 0
        if any(coefficients):
            equations.append({'coefficients': coefficients, 'target': target,
                              'kind': kind, 'indices': list(indices)})
    nongrid = {tuple(e) for e in template['nongrid_edges']}
    for i in range(21):
        equation([int(qi == i) for qi, si, z in columns], 4, 'four_rows', [i])
        if RECTANGLES[i] in nongrid:
            bounds.append({'coefficients': [z[i] if qi == i else 0 for qi, si, z in columns],
                           'upper': 4, 'kind': 'no_three_edge_rectangle', 'indices': [i]})
            if degree_histograms:
                # With at most two internal edges the only degree histograms
                # are (4,0,0), (2,2,0), (0,4,0), (1,2,1).
                # In particular, twice the number of degree-two vertices is
                # at most the number of degree-one vertices.
                bounds.append({'coefficients': [(2 * int(z[i] == 2) - int(z[i] == 1))
                                                if qi == i else 0 for qi, si, z in columns],
                               'upper': 0, 'kind': 'degree_histogram', 'indices': [i]})
    for i, j in combinations(range(21), 2):
        equation([int(qi == i) * z[j] - int(qi == j) * z[i] for qi, si, z in columns],
                 0, 'block_symmetry', [i, j])
    for i, j in combinations_with_replacement(range(21), 2):
        target = 64 if i == j else 24 if set(RECTANGLES[i]) & set(RECTANGLES[j]) else 32
        equation([z[i] * z[j] + int(qi == i) * z[j] for qi, si, z in columns],
                 target, 'neighbor_moment', [i, j])
    return columns, equations, bounds


def certificate(columns, equations, bounds, y, mu):
    if not all(isinstance(v, int) for v in y + mu) or any(v < 0 for v in mu):
        return None
    vector = [sum(v * row['coefficients'][j] for v, row in zip(y, equations))
              + sum(v * row['coefficients'][j] for v, row in zip(mu, bounds))
              for j in range(len(columns))]
    rhs = sum(v * row['target'] for v, row in zip(y, equations)) + sum(v * row['upper'] for v, row in zip(mu, bounds))
    if rhs >= 0 or min(vector, default=0) < 0:
        return None
    def term(row, multiplier):
        return {k: v for k, v in row.items() if k != 'coefficients'} | {'multiplier': multiplier}
    return {'status': 'EXCLUDED_BY_INTEGER_CERTIFICATE', 'constant_upper_bound': rhs,
            'nonnegative_variable_coefficients': vector,
            'equation_multipliers': [term(r, v) for r, v in zip(equations, y) if v],
            'upper_bound_multipliers': [term(r, v) for r, v in zip(bounds, mu) if v],
            'conclusion': 'A sum of nonnegative multiples of nonnegative row multiplicities is <= a negative integer.'}


def reduce_diagonal_system(columns, equations, bounds, fallback_full=False):
    """Find a small candidate core. Only the final integer certificate proves it."""
    def infeasible(es, bs):
        lp = pywraplp.Solver.CreateSolver('GLOP')
        lp.SetTimeLimit(1000)
        xs = [lp.NumVar(0, lp.infinity(), f'x{i}') for i in range(len(columns))]
        for row in es + bs:
            constraint = lp.Constraint(row.get('target', -lp.infinity()),
                                       row.get('target', row.get('upper')))
            for x, value in zip(xs, row['coefficients']):
                if value:
                    constraint.SetCoefficient(x, value)
        return lp.Solve() == pywraplp.Solver.INFEASIBLE
    es = [r for r in equations if r['kind'] != 'neighbor_moment'
          or r['indices'][0] == r['indices'][1]]
    bs = list(bounds)
    if not infeasible(es, bs):
        if not fallback_full or not infeasible(equations, bounds):
            return equations, bounds
        es = list(equations)
    for group in ('neighbor_moment', 'bound', 'block_symmetry', 'four_rows'):
        rows = list(bs) if group == 'bound' else [r for r in es if r['kind'] == group]
        for row in rows:
            trial = [r for r in (bs if group == 'bound' else es) if r is not row]
            removable = infeasible(es, trial) if group == 'bound' else infeasible(trial, bs)
            if removable:
                if group == 'bound':
                    bs = trial
                else:
                    es = trial
    return es, bs


def find_certificate(columns, equations, bounds):
    lp = pywraplp.Solver.CreateSolver('GLOP')
    lp.SetTimeLimit(10000)
    inf = lp.infinity()
    ys = [lp.NumVar(-inf, inf, f'y{i}') for i in range(len(equations))]
    mus = [lp.NumVar(0, inf, f'mu{i}') for i in range(len(bounds))]
    norms = [lp.NumVar(0, inf, f'abs{i}') for i in range(len(equations))]
    for y, norm in zip(ys, norms):
        lp.Add(norm >= y)
        lp.Add(norm >= -y)
    for j in range(len(columns)):
        lp.Add(sum(y * r['coefficients'][j] for y, r in zip(ys, equations))
               + sum(mu * r['coefficients'][j] for mu, r in zip(mus, bounds)) >= 0)
    lp.Add(sum(y * r['target'] for y, r in zip(ys, equations))
           + sum(mu * r['upper'] for mu, r in zip(mus, bounds)) <= -1)
    lp.Minimize(sum(norms) + sum(mus))
    status = lp.Solve()
    if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        values = [x.solution_value() for x in ys + mus]
        candidates = []
        for limit in (10, 100, 1000, 10000, 1000000):
            fractions = [Fraction(x).limit_denominator(limit) for x in values]
            candidates.append((f'denominator_limit_{limit}', fractions))
        # Floating values at a vertex can be slightly inconsistent when rounded
        # one by one. Reconstruct the active linear equations over Q instead.
        rows = [r['coefficients'] for r in equations + bounds]
        targets = [r['target'] for r in equations] + [r['upper'] for r in bounds]
        support = [i for i, v in enumerate(values) if abs(v) > 1e-7]
        tight = [j for j in range(len(columns))
                 if abs(sum(values[i] * rows[i][j] for i in support)) < 1e-7]
        system = Matrix([[rows[i][j] for i in support] for j in tight]
                        + [[targets[i] for i in support]])
        rhs = Matrix([0] * len(tight) + [-1])
        try:
            rational, parameters = system.gauss_jordan_solve(rhs)
            rational = rational.subs({p: 0 for p in parameters})
            fractions = [Fraction(0)] * len(values)
            for i, v in zip(support, rational):
                fractions[i] = Fraction(int(v.p), int(v.q))
            candidates.append(('exact_active_equations', fractions))
        except ValueError:
            pass
        for method, fractions in candidates:
            den = math.lcm(*(x.denominator for x in fractions))
            integers = [int(x * den) for x in fractions]
            divisor = reduce(math.gcd, integers, 0) or 1
            integers = [x // divisor for x in integers]
            result = certificate(columns, equations, bounds, integers[:len(ys)], integers[len(ys):])
            if result:
                result['lp_status_code'] = status
                result['reconstruction'] = method
                return result
    return {'status': 'NO_INTEGER_CERTIFICATE_FOUND', 'lp_status_code': status}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--catalogue', type=Path, required=True)
    p.add_argument('--reduce-diagonal', action='store_true',
                   help='Reduce to a candidate core using diagonal moments before exact certification.')
    p.add_argument('--reduce-full', action='store_true',
                   help='Also reduce the full moment system if diagonal moments alone are feasible.')
    p.add_argument('--degree-histograms', action='store_true',
                   help='Use 2 n_degree2 <= n_degree1 in each nongrid rectangle, a consequence of E3.')
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    template = json.loads(a.bundle.read_text(encoding='utf-8-sig'))['template']
    catalogue = json.loads(a.catalogue.read_text(encoding='utf-8-sig'))['catalogue']
    assert catalogue['status'] == 'ROW_CATALOGUE_COMPLETE'
    start = time.process_time()
    columns, equations, bounds = linear_system(template, catalogue, a.degree_histograms)
    if a.reduce_diagonal or a.reduce_full:
        equations, bounds = reduce_diagonal_system(columns, equations, bounds, a.reduce_full)
    result = find_certificate(columns, equations, bounds)
    result.update(scope=__doc__, resources=resources, source_bundle=str(a.bundle),
                  source_catalogue=str(a.catalogue), source_catalogue_sha256=hashlib.sha256(a.catalogue.read_bytes()).hexdigest(),
                  template=template, rectangles=[list(q) for q in RECTANGLES],
                  variables=len(columns), equalities=len(equations), inequalities=len(bounds),
                  column_order=[{'rectangle': list(RECTANGLES[qi]), 'state_index': si} for qi, si, z in columns],
                  uses_Gram_cover=False, uses_prism_budget=False, uses_universal_E3_exclusion=True,
                  uses_degree_histogram_bounds=a.degree_histograms,
                  global_conway_exclusion=False, cpu_seconds=time.process_time() - start)
    atomic_json_write(a.output, result)
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ('scope', 'resources', 'template', 'rectangles', 'column_order', 'nonnegative_variable_coefficients',
                      'equation_multipliers', 'upper_bound_multipliers')}))


if __name__ == '__main__':
    main()
