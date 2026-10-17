"""Exact integer coupling cuts from exterior mate sectors of four stars.

Uses the producer's coarse identity D T D^t. New contribution: small
negative witnesses at saturation and integer row cuts near saturation.
No producer example is independently checked by the self-test.
"""
import argparse
from collections import Counter
from itertools import combinations, permutations, product
from math import gcd, lcm
from pathlib import Path
import json
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_profile_join import LABELS
from three_star_column_domains import k8

N = len(LABELS)
EDGES = tuple(combinations(range(N), 2))
OUTSIDE = tuple(range(4, 14))


def primitive(v):
    scale = lcm(*(int(x.q) for x in v))
    out = [int(x*scale) for x in v]
    common = gcd(*out)
    out = [x//common for x in out]
    if next(x for x in out if x) < 0:
        out = [-x for x in out]
    return tuple(out)


def lift(z):
    values = dict(zip(OUTSIDE, z))
    return tuple(sum(values.get(c, 0) for c in p) for p in LABELS)


def short_directions():
    for coefficients in product((-1, 0, 1), repeat=5):
        if not any(coefficients) or next(x for x in coefficients if x) < 0:
            continue
        if sum(coefficients) == 0:
            z = tuple(x for a in coefficients for x in (a, a))
            yield dict(sector='mate_symmetric_zero_sum', alpha=1, z=z, q=lift(z))
        z = tuple(x for a in coefficients for x in (a, -a))
        yield dict(sector='mate_antisymmetric', alpha=2, z=z, q=lift(z))


def saturated_directions(gamma):
    D = sp.Matrix([[int(x in p) for p in LABELS] for x in OUTSIDE])
    E = D*sp.Matrix(gamma)*D.T
    mate = sp.Matrix(10, 10, lambda i, j: int((i ^ 1) == j))
    coarse = 6*sp.eye(10)+2*(sp.ones(10)-mate)-E
    symmetric = sp.Matrix(10, 4, lambda i, j: int(i//2 == j)-int(i//2 == 4))
    antisymmetric = sp.Matrix(10, 5, lambda i, j: (1 if i % 2 == 0 else -1)*int(i//2 == j))
    for sector, alpha, basis in [('mate_symmetric_zero_sum', 1, symmetric),
                                 ('mate_antisymmetric', 2, antisymmetric)]:
        for relation in (basis.T*coarse*basis).nullspace():
            z = primitive(basis*relation)
            yield dict(sector=sector, alpha=alpha, z=z, q=lift(z), from_coarse_kernel=True)


def strict_upper_cuts():
    """100 integer-strengthened rows from strictly positive upper sectors.

For N=15U, Nq=bq+15Gamma*q with b=48 or40. Zero energy in a
PSD N would force the noninteger rational eigenvalue -b/15 of integer
Gamma, impossible. For these directions, q^tNq is a multiple of30,
so it is at least30, improving the ordinary PSD row by one unit.
"""
    directions = []
    for coefficients in product((-1, 0, 1), repeat=5):
        if sum(x != 0 for x in coefficients) == 3 and next(x for x in coefficients if x) > 0:
            z = tuple(x for a in coefficients for x in (a, -a))
            directions.append(('mate_antisymmetric', 40, z))
    for coefficients in permutations((2, 1, 0, -1, -2)):
        if next(x for x in coefficients if x) > 0:
            z = tuple(x for a in coefficients for x in (a, a))
            directions.append(('mate_symmetric_zero_sum', 48, z))
    for sector, b, z in directions:
        q = lift(z)
        norm = sum(x*x for x in q)
        base = b*norm
        assert base % 30 == 0
        yield dict(sector=sector, z=z, q=q, norm_squared=norm, b=b,
                   coefficients=[[i, j, q[i]*q[j]] for i, j in EDGES if q[i] and q[j]],
                   lower_bound=1-base//30, ordinary_PSD_lower_bound=-base//30,
                   validity='Integer symmetric Gamma with zero diagonal and U PSD. Rational noninteger eigenvalues are impossible.')


def row_cut(q, alpha, row, t):
    """Twice [5h-(2t+1)s_i+t(t+1)] >= 0, linear in Gamma."""
    norm = sum(x*x for x in q)
    constant = 5*alpha*norm-2*(2*t+1)*alpha*q[row]+2*t*(t+1)
    coefficients = []
    for i, j in EDGES:
        value = -10*q[i]*q[j]
        if i == row:
            value += 2*(2*t+1)*q[j]
        if j == row:
            value += 2*(2*t+1)*q[i]
        if value:
            coefficients.append([i, j, value])
    return dict(constant=constant, coefficients=coefficients, lower_bound=0,
                q=q, alpha=alpha, row=row, t=t,
                validity='Binary symmetric Gamma; follows from T PSD and integer s_i.')


def quadratic_M(gamma, v):
    return 24*sum(x*x for x in v)-sum(v[i]*v[j]*(8*gamma[i][j]+k8(LABELS[i], LABELS[j]))
                                     for i in range(N) for j in range(N))


def analyse_direction(gamma, direction, limit):
    q, alpha = direction['q'], direction['alpha']
    gq = [sum(x*y for x, y in zip(row, q)) for row in gamma]
    energy = alpha*sum(x*x for x in q)-sum(x*y for x, y in zip(q, gq))
    assert energy % 2 == 0
    h = energy//2
    s = [alpha*x-y for x, y in zip(q, gq)]
    violations = [i for i in range(N) if s[i]*s[i] > 5*h]
    record = dict(**direction, h=h, energy_T=energy, violating_rows=violations, cuts=[])
    for i in violations[:limit]:
        cut = row_cut(q, alpha, i, s[i])
        value = cut['constant']+sum(c*gamma[a][b] for a, b, c in cut['coefficients'])
        assert value == 2*(5*h-s[i]*s[i]) < 0
        cut['value_at_input'] = value
        record['cuts'].append(cut)
    if h == 0 and violations:
        i = violations[0]
        witness = [2*x for x in q]
        witness[i] -= 1 if s[i] > 0 else -1
        value = quadratic_M(gamma, witness)
        assert value == 20-32*abs(s[i]) <= -12
        record['saturation_witness'] = dict(vector=witness, quadratic_value_for_8T=value,
                                            row=i, residual_Tq=s[i])
    return record


def separate(gamma, cut_limit):
    directions = list(short_directions())+list(saturated_directions(gamma))
    seen, records, remaining = set(), [], cut_limit
    for direction in directions:
        key = direction['alpha'], direction['q']
        if key in seen:
            continue
        seen.add(key)
        result = analyse_direction(gamma, direction, remaining)
        if result['violating_rows']:
            remaining -= len(result['cuts'])
            records.append(result)
    upper_violations = []
    for cut in strict_upper_cuts():
        value = sum(c*gamma[i][j] for i, j, c in cut['coefficients'])
        if value < cut['lower_bound']:
            cut['value_at_input'] = value
            upper_violations.append(cut)
    return dict(status='NECESSARY_COUPLING_CUTS', directions=len(seen), violations=records,
                returned_coupling_cuts=cut_limit-remaining, labels=LABELS,
                strict_upper_cut_violations=upper_violations,
                scope='Necessary integer inequalities only; absence of violations does not prove PSD or a Conway completion.')


def self_test():
    gamma = [[0]*N for _ in range(N)]
    z = (1, -1)+(0,)*8
    q = lift(z)
    positive = [i for i, x in enumerate(q) if x == 1]
    negative = [i for i, x in enumerate(q) if x == -1]
    # Our own algebraic fixture: coarse energy zero, fine coupling nonzero.
    # It is deliberately not asserted to be locally admissible or a graph seed.
    for i, j in list(combinations(positive, 2))+[(negative[0], negative[1]), (negative[0], negative[2])]:
        gamma[i][j] = gamma[j][i] = 1
    direction = dict(sector='mate_antisymmetric', alpha=2, z=z, q=q)
    result = analyse_direction(gamma, direction, 44)
    assert result['energy_T'] == 0 and result['saturation_witness']['quadratic_value_for_8T'] == -12
    counts = Counter()
    for direction in short_directions():
        counts[direction['sector']] += 1
        q, alpha = direction['q'], direction['alpha']
        for i in range(N):
            value = sum((24*int(i == j)-8*gamma[i][j]-k8(LABELS[i], LABELS[j]))*q[j]
                        for j in range(N))
            assert value == 8*(alpha*q[i]-sum(gamma[i][j]*q[j] for j in range(N)))
    assert counts == dict(mate_symmetric_zero_sum=25, mate_antisymmetric=121)
    strict_counts = Counter()
    strict_bounds = {}
    for cut in strict_upper_cuts():
        strict_counts[cut['sector']] += 1
        strict_bounds[cut['sector']] = cut['lower_bound']
        q = cut['q']
        for i in range(N):
            value = sum((60*int(i == j)+15*gamma[i][j]
                         -4*len(set(LABELS[i]) & set(LABELS[j]))
                         +sum((c ^ 1) in LABELS[j] for c in LABELS[i])-2)*q[j]
                        for j in range(N))
            assert value == cut['b']*q[i]+15*sum(gamma[i][j]*q[j] for j in range(N))
    assert strict_counts == dict(mate_antisymmetric=40, mate_symmetric_zero_sum=60)
    assert strict_bounds == dict(mate_antisymmetric=-31, mate_symmetric_zero_sum=-127)
    return dict(status='PASS', short_direction_counts=dict(counts),
                strict_upper_cut_counts=dict(strict_counts), strict_upper_lower_bounds=strict_bounds,
                own_saturation_witness=result['saturation_witness'],
                scope='Own algebraic fixture and exact identities; no producer object audited.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input')
    p.add_argument('--output', required=True)
    p.add_argument('--cut-limit', type=int, default=100)
    p.add_argument('--self-test', action='store_true')
    p.add_argument('--export-strict-upper', action='store_true')
    a = p.parse_args()
    if a.self_test:
        result = self_test()
    elif a.export_strict_upper:
        result = dict(status='100_VALID_STRICT_UPPER_CUTS', labels=LABELS, cuts=list(strict_upper_cuts()))
    else:
        if not a.input or a.cut_limit < 1:
            p.error('Supply --input and a positive --cut-limit.')
        data = json.loads(Path(a.input).read_text(encoding='utf-8-sig'))
        old_labels = tuple(tuple(sorted(x)) for x in data['labels'])
        if len(old_labels) != 44 or set(old_labels) != set(LABELS):
            raise ValueError('Expected the44 labels meeting centres0,1,2,3.')
        indices = {label:i for i, label in enumerate(LABELS)}
        source = data['structures'][0] if 'structures' in data else data
        gamma = [[0]*N for _ in range(N)]
        for i, j in source['edges']:
            i, j = indices[old_labels[i]], indices[old_labels[j]]
            gamma[i][j] = gamma[j][i] = 1
        result = separate(gamma, a.cut_limit)
    output = Path(a.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','short_direction_counts','strict_upper_cut_counts','directions','returned_coupling_cuts','scope') if k in result}))


if __name__ == '__main__':
    main()
