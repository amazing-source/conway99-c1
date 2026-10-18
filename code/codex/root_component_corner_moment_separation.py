"""Find a separating combination of corner moments; certify it with integers.

The floating LP only proposes coefficients. Exclusion requires re-evaluating
the proposed integer polynomial on EVERY permitted corner state and proving
that the sum of its local minima exceeds its required global moment.
Failure to find a certificate is inconclusive, whatever the LP status.
"""

from fractions import Fraction
from functools import reduce
from itertools import combinations_with_replacement
import math


def certify_coefficients(pairs, coefficients, target, vectors, rectangles):
    """The only function allowed to report EXCLUDED; integer arithmetic."""
    assert all(isinstance(c, int) for c in coefficients)
    required = sum(c * x for c, x in zip(coefficients, target))
    bounds = [min(sum(c * x for c, x in zip(coefficients, v)) for v in choices)
              for choices in vectors]
    lower = sum(bounds)
    if lower <= required:
        return None
    return {'status': 'EXCLUDED', 'reason': 'Exact separating combination of moments.',
            'terms': [{'coordinates': list(p), 'coefficient': c}
                      for p, c in zip(pairs, coefficients) if c],
            'required_moment': required, 'lower_bound': lower,
            'gap': lower - required,
            'rectangle_bounds': [{'rectangle': list(q), 'minimum': b}
                                 for q, b in zip(rectangles, bounds)],
            'certificate_arithmetic': 'Integer extrema over all enumerated corner states.'}


def separate(matrix, anchors, domains, tables, seconds=5):
    from ortools.linear_solver import pywraplp

    assert all(t['rows'] for t in tables)
    pairs = list(combinations_with_replacement(anchors, 2))
    target = [7 * int(matrix[i, j]) for i, j in pairs]
    vectors, rectangles = [], []
    for table in tables:
        q = tuple(table['rectangle'])
        hs = domains[q]['signatures']
        vectors.append(sorted({tuple(sum(hs[s][i] * hs[s][j] for s in row[:4])
                                     for i, j in pairs) for row in table['rows']}))
        rectangles.append(q)

    solver = pywraplp.Solver.CreateSolver('GLOP')
    solver.SetTimeLimit(int(1000 * seconds))
    inf = solver.infinity()
    weights = [solver.NumVar(-inf, inf, f'c_{i}') for i in range(len(pairs))]
    norms = [solver.NumVar(0, inf, f'abs_{i}') for i in range(len(pairs))]
    minima = [solver.NumVar(-inf, inf, f'min_{q}') for q in range(len(tables))]
    for c, a in zip(weights, norms):
        solver.Add(a >= c)
        solver.Add(a >= -c)
    for q, choices in enumerate(vectors):
        for vector in choices:
            solver.Add(minima[q] <= sum(c * x for c, x in zip(weights, vector)))
    solver.Add(sum(minima) - sum(c * x for c, x in zip(weights, target)) >= 1)
    # L1 minimization tends to produce a shorter explanatory inequality.
    solver.Minimize(sum(norms))
    status = solver.Solve()
    diagnostic = {'lp_status_code': status, 'lp_wall_milliseconds': solver.wall_time(),
                  'distinct_moment_states': list(map(len, vectors)),
                  'floating_solver_is_not_the_certificate': True}
    if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        values = [c.solution_value() for c in weights]
        for limit in (1, 2, 5, 10, 100, 10000):
            rational = [Fraction(c).limit_denominator(limit) for c in values]
            denominator = math.lcm(*(x.denominator for x in rational))
            integer = [int(x * denominator) for x in rational]
            divisor = reduce(math.gcd, integer, 0) or 1
            integer = [x // divisor for x in integer]
            certificate = certify_coefficients(pairs, integer, target, vectors, rectangles)
            if certificate:
                certificate['search_diagnostic'] = diagnostic
                return certificate
    return {'status': 'NOT_FOUND', 'search_diagnostic': diagnostic}
