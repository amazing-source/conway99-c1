"""Necessary fractional stars, with integer certificates for rejected profiles.

Fix the known-neighbour profile p of x. A possible future neighbour y
chooses a compatible profile q. Nonnegative weights z[y,q] obey:
 * at most one choice per y;
 * x's exact degree, upper-letter, and known-common-neighbour quotas;
 * at most one neighbour containing any two known vertices;
 * at most one neighbour containing a known vertex and an upper letter.
The last two bounds follow because two neighbours of x cannot share
two further neighbours: that would give three common neighbours.

The LP is only a discovery mechanism. A rejection requires integer
weights on constraints whose combined coefficients are nonpositive,
whose upper-bound weights are nonpositive, and whose combined RHS is
positive. This is a directly replayable contradiction for z >= 0.
"""

from collections import defaultdict
from fractions import Fraction
from functools import reduce
from itertools import combinations
from math import gcd, lcm

from root_component_p3_neighbor_support import edge_failure


def system(oracle, x, pi):
    a = oracle.prepared[x][pi]
    options = []
    degree = []; known = defaultdict(list); letters = defaultdict(list)
    by_y = defaultdict(list); pairs = defaultdict(list); mixed = defaultdict(list)
    for y, domain in enumerate(oracle.prepared):
        if y == x:
            continue
        for qi, b in enumerate(domain):
            if edge_failure(a, b) is not None:
                continue
            j = len(options); options.append((y, qi)); degree.append(j); by_y[y].append(j)
            p = oracle.domains[y][qi]
            for u in p:
                known[u].append(j)
                for letter in oracle.outside[y]:
                    mixed[u, letter].append(j)
            for uv in combinations(p, 2):
                pairs[uv].append(j)
            for letter in oracle.outside[y]:
                letters[letter].append(j)
    target = oracle.targets(x, pi)
    constraints = [{'kind': 'degree', 'key': None, 'sense': '=', 'rhs': target[1], 'columns': degree}]
    constraints += [{'kind': 'known', 'key': u, 'sense': '=', 'rhs': target[2+u], 'columns': known[u]}
                    for u in range(oracle.nk)]
    constraints += [{'kind': 'letter', 'key': v, 'sense': '=', 'rhs': target[2+oracle.nk+v], 'columns': letters[v]}
                    for v in range(2*oracle.roots)]
    for kind, group in (('one_vertex', by_y), ('known_pair', pairs), ('known_letter', mixed)):
        for key, columns in sorted(group.items()):
            if kind != 'one_vertex' and len({options[j][0] for j in columns}) <= 1:
                continue
            constraints.append({'kind': kind, 'key': key, 'sense': '<=', 'rhs': 1, 'columns': columns})
    return options, constraints


def check_certificate(options, constraints, certificate):
    weights = certificate['weights']
    assert len(weights) == len(constraints) and all(isinstance(w, int) for w in weights)
    totals = [0]*len(options); rhs = 0
    for weight, c in zip(weights, constraints):
        assert c['sense'] == '=' or weight <= 0
        rhs += weight*c['rhs']
        for j in c['columns']:
            totals[j] += weight
    assert rhs > 0 and all(v <= 0 for v in totals)
    assert rhs == certificate['rhs']
    return True


def integer_certificate(options, constraints, values):
    for bound in (16, 64, 256, 4096):
        fractions = [Fraction(v).limit_denominator(bound) for v in values]
        scale = lcm(*(v.denominator for v in fractions))
        weights = [int(scale*v) for v in fractions]
        divisor = reduce(gcd, weights, 0)
        if divisor:
            weights = [w//divisor for w in weights]
        cert = {'weights': weights, 'rhs': sum(w*c['rhs'] for w, c in zip(weights, constraints))}
        try:
            check_certificate(options, constraints, cert)
        except AssertionError:
            continue
        return cert
    return None


def sparse_certificate(options, constraints):
    """Minimize the L1 norm of a separating combination, then check it exactly."""
    from ortools.linear_solver import pywraplp
    s = pywraplp.Solver.CreateSolver('GLOP'); s.SetTimeLimit(1000)
    cs = [s.Constraint(-s.infinity(), 0, 'col%d' % j) for j in range(len(options))]
    rhs = s.Constraint(1, s.infinity(), 'contradiction')
    objective = s.Objective(); objective.SetMinimization(); variables = []
    for i,c in enumerate(constraints):
        if not c['columns'] and not c['rhs']:
            variables.append([]); continue
        terms = []
        for sign in ((-1,1) if c['sense']=='=' else (-1,)):
            v = s.NumVar(0,s.infinity(),'w%d_%d' % (i,sign)); terms.append((sign,v))
            objective.SetCoefficient(v,1); rhs.SetCoefficient(v,sign*c['rhs'])
            for j in c['columns']:
                cs[j].SetCoefficient(v,sign)
        variables.append(terms)
    if s.Solve() != pywraplp.Solver.OPTIMAL:
        return None
    return integer_certificate(options,constraints,
                               [sum(sign*v.solution_value() for sign,v in row) for row in variables])


def solve_system(options, constraints, time_limit_ms=1000, simplify=True):
    from ortools.linear_solver import pywraplp
    solver = pywraplp.Solver.CreateSolver('GLOP')
    solver.SetTimeLimit(time_limit_ms)
    variables = [solver.NumVar(0, solver.infinity(), 'z%d' % j) for j in range(len(options))]
    objective = solver.Objective(); objective.SetMinimization()
    model_rows = []
    # Phase I is always feasible. Positive optimum supplies the dual ray;
    # a floating-point objective alone is NEVER accepted as an exclusion.
    for i, c in enumerate(constraints):
        row = solver.Constraint(c['rhs'] if c['sense'] == '=' else -solver.infinity(), c['rhs'], 'r%d' % i)
        for j in c['columns']:
            row.SetCoefficient(variables[j], 1)
        above = solver.NumVar(0, solver.infinity(), 'a%d' % i)
        row.SetCoefficient(above, -1); objective.SetCoefficient(above, 1)
        if c['sense'] == '=':
            below = solver.NumVar(0, solver.infinity(), 'b%d' % i)
            row.SetCoefficient(below, 1); objective.SetCoefficient(below, 1)
        model_rows.append(row)
    status = solver.Solve()
    answer = {'variables': len(options), 'constraints': len(constraints), 'lp_status': status}
    if status != pywraplp.Solver.OPTIMAL:
        return {**answer, 'status': 'UNKNOWN_STAR_LP'}
    answer['phase_one_objective'] = objective.Value()
    if objective.Value() < 1e-7:
        return {**answer, 'status': 'PASSES_FRACTIONAL_STAR'}
    cert = integer_certificate(options,constraints,[row.dual_value() for row in model_rows])
    if cert is not None:
        smaller = sparse_certificate(options,constraints) if simplify else None
        if smaller is not None:
            cert = smaller
        return {**answer, 'status': 'EXCLUDED_PROFILE_STAR_LP', 'certificate': cert,
                'nonzero_constraints': [{'index': i, 'weight': w, **{k:v for k,v in c.items() if k != 'columns'}}
                                        for i,(w,c) in enumerate(zip(cert['weights'],constraints)) if w]}
    return {**answer, 'status': 'UNVERIFIED_NUMERICAL_INFEASIBILITY'}


def solve_star(oracle, x, pi, time_limit_ms=1000):
    answer = solve_system(*system(oracle,x,pi),time_limit_ms)
    return {'outside_index':x,'profile_index':pi,**answer}


def controls():
    from root_component_profile_row_cuts import RowCutOracle
    oracle = RowCutOracle([0], [(0,2)], [(0,3),(1,2),(1,3)], [[[0]],[[0]],[[],[0]]], root_count=2)
    for x, pi in ((0,0),(1,0),(2,0)):
        assert solve_star(oracle,x,pi)['status'] == 'PASSES_FRACTIONAL_STAR'
    bad = solve_star(oracle,2,1)
    assert bad['status'] == 'EXCLUDED_PROFILE_STAR_LP'
    assert check_certificate(*system(oracle,2,1),bad['certificate'])
    return {'actual_rook_completion_preserved': True, 'impossible_profile_integer_certificate': bad}
