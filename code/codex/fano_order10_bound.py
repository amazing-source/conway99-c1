"""Exact order-ten census certificate for the Fano cap proposed by LAB.

The optimiser discovers a dual support only. The published bound is an
identity with nonnegative rational weights on induced-embedding counts.
--verify-only rechecks that identity without optimisation.
--audit-recurrences independently rebuilds every count used by the proof.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import gzip
import json
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from sympy import Matrix, Rational

from higher_census_minima import ROOT
from targeted_order10_census import canonical, load_stage, TriangularCensus
from seven_vertex_census import canon as small_canon

sys.path.insert(0, str(ROOT/'code/lab_theta_lp_2026-10-08'))
import census2 as lab

OUTPUT = ROOT/'data/codex_fano_order10_bound.json'


def induced(adj, keep):
    return tuple(sum(1 << j for j, u in enumerate(keep) if adj[v] >> u & 1) for v in keep)


def core_check(source):
    adj = [0]*14
    for i in range(1, 8):
        for j in range(1, 8):
            if (i & j).bit_count() % 2:
                adj[i-1] |= 1 << (j+6)
                adj[j+6] |= 1 << (i-1)
    assert all(row.bit_count() == 4 for row in adj)
    found = Counter()
    graphs = {}
    for size in range(6, 11):
        for keep in combinations(range(14), size):
            small = induced(adj, keep)
            if min(row.bit_count() for row in small) < 3:
                continue
            key, _ = lab.canon(size, small)
            found[size, key] += 1
            graphs[size, key] = small
    assert len(found) == 1
    (size, key), multiplicity = next(iter(found.items()))
    assert size == 10 and multiplicity == 21
    graph = graphs[size, key]
    assert sorted(row.bit_count() for row in graph) == [3]*8+[4]*2
    reached = {0}
    while True:
        enlarged = reached | {j for i in reached for j in range(10) if graph[i] >> j & 1}
        if enlarged == reached:
            break
        reached = enlarged
    assert len(reached) == 10
    parameter = next(i for i, (n, k, _) in enumerate(source['params'], 1) if (n, k) == (size, key))
    return {'parameter_id': parameter, 'order': size, 'lab_key': key,
            'adjacency_bits': list(graph), 'copies_per_Fano_configuration': multiplicity,
            'full_seed_vertices': [i for i, row in enumerate(graph) if row.bit_count() == 4],
            'uniqueness_argument': 'A degree-four vertex and all its neighbours are a full Fano seed; note 180 proves unique extension.'}


def load():
    with gzip.open(ROOT/'data/codex_lab_full_order10.json.gz', 'rt', encoding='utf-8') as stream:
        source = json.load(stream)
    rows, graphs = {}, {}
    for n in range(6, 11):
        for key, adj, _, form in source['types'][str(n)]:
            name = f'{n}:{key}'
            rows[name] = {int(k): F(v) for k, v in form.items() if F(v)}
            graphs[name] = tuple(adj)
    return source, rows, graphs


def verify(rows, report):
    total = {}
    for name, weight in report['certificate']:
        weight = F(weight)
        assert weight >= 0
        for key, value in rows[name].items():
            total[key] = total.get(key, F(0))+weight*value
    total = {key: value for key, value in total.items() if value}
    expected = {0: F(report['F10_upper_bound']), report['core']['parameter_id']: F(-1)}
    assert total == expected, (total, expected)
    a7_upper = 2*F(report['F10_upper_bound'])/21
    assert F(report['a7_rational_upper_bound']) == a7_upper
    assert report['a7_even_integer_upper_bound'] == 2*(a7_upper//2)


def audit_recurrences(source, rows, graphs, report):
    """Independent vertex choice/canonical labels and the Codex order-nine census."""
    packet = json.loads((ROOT/'data/codex_census_validation_99.json').read_text())
    stages = {n: load_stage(packet, n)[2] for n in range(6, 10)}
    solver = TriangularCensus(10, 99, 14, stages[9])
    names = {0: '1'}
    for i, (n, _, adj) in enumerate(source['params'], 1):
        if n in (6, 7):
            name = 'P' if n == 6 else 'H'
        elif n == 8:
            name = f'C8_{small_canon(tuple(adj))[0]}'
        else:
            name = f'C{n}_{canonical(tuple(adj))[0]}'
        names[i] = name
    for name, _ in report['certificate']:
        n = int(name.split(':')[0])
        actual = solver.solve(graphs[name]) if n == 10 else stages[n][canonical(graphs[name])[0]]
        expected = {names[i]: value for i, value in rows[name].items()}
        assert actual == expected, name
    solver.verify_equations()
    print('Independently rebuilt all', len(report['certificate']), 'certificate counts;',
          len(solver.forms), 'order-ten dependency types', flush=True)
    return {'certificate_counts_checked': len(report['certificate']),
            'order10_dependency_types': len(solver.forms),
            'exact_equations_checked': len(solver.equations)}


def discover(source, rows, core):
    started = time.monotonic()
    names = list(rows)
    npar = len(source['params'])
    ii, jj, vv, constants = [], [], [], []
    for i, name in enumerate(names):
        row = rows[name]
        scale = max(map(abs, row.values()), default=F(1))
        constants.append(float(row.get(0, 0)/scale))
        for key, value in row.items():
            if key:
                ii.append(i); jj.append(key-1); vv.append(float(value/scale))
    matrix = coo_matrix((vv, (ii, jj)), shape=(len(names), npar)).tocsr()
    target = [0]*npar
    target[core['parameter_id']-1] = -1
    result = linprog(np.array(target, dtype=float), A_ub=-matrix, b_ub=np.array(constants),
                     bounds=[(None, None)]*npar, method='highs-ipm')
    assert result.success, result.message
    support = [i for i, weight in enumerate(-result.ineqlin.marginals) if weight > 1e-9]
    print('Discovered F10 upper bound', -result.fun, 'with', len(support),
          'dual rows after', round(time.monotonic()-started, 1), 'seconds', flush=True)
    exact = Matrix([[Rational(rows[names[i]].get(key, 0)) for i in support] for key in range(1, npar+1)])
    weights, free = exact.gauss_jordan_solve(Matrix(target))
    if free:
        weights = weights.subs({symbol: 0 for symbol in free})
    weights = list(map(F, weights))
    assert all(weight >= 0 for weight in weights)
    upper = sum(weight*rows[names[i]].get(0, 0) for i, weight in zip(support, weights))
    return {'source': 'codex_lab_full_order10.json.gz', 'core': core,
            'F10_upper_bound': str(upper), 'a7_rational_upper_bound': str(2*upper/21),
            'a7_even_integer_upper_bound': int(2*((2*upper/21)//2)),
            'certificate': [(names[i], str(weight)) for i, weight in zip(support, weights) if weight],
            'scope': 'Exact census upper bound and unique-seed double count; no rank exclusion.'}


def main():
    source, rows, graphs = load()
    core = core_check(source)
    report = json.loads(OUTPUT.read_text()) if '--verify-only' in sys.argv else discover(source, rows, core)
    assert report['core'] == core
    verify(rows, report)
    if '--audit-recurrences' in sys.argv:
        audit = audit_recurrences(source, rows, graphs, report)
        if '--verify-only' not in sys.argv:
            report['independent_recurrence_audit'] = audit
    if '--verify-only' not in sys.argv:
        OUTPUT.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Exact certificate verified: N(F10) <=', report['F10_upper_bound'],
          '; a7 <=', report['a7_even_integer_upper_bound'], flush=True)


if __name__ == '__main__':
    main()
