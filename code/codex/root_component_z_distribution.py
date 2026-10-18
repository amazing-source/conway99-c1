"""Eliminate a root template using row counts and one rectangle moment.

Enumerate integral solutions of the component equations C z=b for each
of the 21 row types, with quota bounds 0<=z<=2 or 4. No adjacency model,
Gram matrix, prism budget, or SAT solver is used. Project onto one target
rectangle and combine the possible counts by exact dynamic programming.
An exclusion is valid even though all compatibility between distinct
adjacency rows has been relaxed. Passing this filter is inconclusive.
"""

import argparse
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path
import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_rectangle_domains import corner_graphs
from root_component_resources import atomic_json_write, limit_research_process

RECTANGLES = list(combinations(range(7), 2))


def row_catalogue(template, max_free=6):
    rows, right = [], []
    for root, nontrivial in enumerate(template['nontrivial_component_groups']):
        assert nontrivial is not None, 'Complete component partitions required.'
        parts = [tuple(part) for part in nontrivial]
        used = {j for part in parts for j in part}
        parts += [(j,) for j in range(7) if j != root and j not in used]
        for part in parts:
            support = {tuple(sorted((root, j))) for j in part}
            rows.append([int(q in support) for q in RECTANGLES])
            right.append([3 * int(q in support) + len(part) * (1 - int(root in q))
                          - sum(j in part for j in q) for q in RECTANGLES])
    c, b = sp.Matrix(rows), sp.Matrix(right)
    reduced, pivots = c.row_join(b).rref()
    if any(p >= 21 for p in pivots):
        return {'status': 'INCONSISTENT_COMPONENT_EQUATIONS'}
    free = [i for i in range(21) if i not in pivots]
    if len(free) > max_free:
        return {'status': 'UNSUPPORTED_DIMENSION', 'free_dimension': len(free)}
    offset, linear = sp.zeros(21, 21), sp.zeros(21, len(free))
    for row, pivot in enumerate(pivots):
        for q in range(21):
            offset[pivot, q] = reduced[row, 21 + q]
        for j, f in enumerate(free):
            linear[pivot, j] = -reduced[row, f]
    for j, f in enumerate(free):
        linear[f, j] = 1
    den = lcm(*(x.q for x in list(offset) + list(linear)))
    ni = np.array((linear * den).tolist(), dtype=np.int64)
    oi = np.array((offset * den).tolist(), dtype=np.int64)
    catalogs = []
    for qi, q in enumerate(RECTANGLES):
        upper = np.array([2 if set(q) & set(f) else 4 for f in RECTANGLES], dtype=np.int64)
        assignments = np.array(list(product(*(range(int(upper[f]) + 1) for f in free))), dtype=np.int64)
        if not free:
            assignments = np.zeros((1, 0), dtype=np.int64)
        numerators = assignments @ ni.T + oi[:, qi]
        valid = np.all((numerators % den == 0) & (numerators >= 0)
                       & (numerators <= upper * den), axis=1)
        states = (numerators[valid] // den).tolist()
        catalogs.append({'rectangle': list(q), 'states': states,
                         'enumerated_free_assignments': len(assignments), 'state_count': len(states)})
    return {'status': 'ROW_CATALOGUE_COMPLETE', 'free_dimension': len(free),
            'free_coordinates': free, 'denominator': den,
            'affine_offset_numerator': oi.tolist(), 'affine_linear_numerator': ni.tolist(),
            'component_matrix': rows, 'right_sides': right, 'row_types': catalogs}


def attainable_costs(domains, maximum_sum):
    states = {(0, 0)}
    for domain in domains:
        states = {(s + z, c + z * (z - 1) // 2)
                  for s, c in states for z in domain if s + z <= maximum_sum}
    return {s: sorted(c for ss, c in states if ss == s) for s in range(maximum_sum + 1)}


def check_rectangle(template, catalogue, target):
    target = tuple(target)
    ti = RECTANGLES.index(target)
    domains = {tuple(r['rectangle']): sorted({z[ti] for z in r['states']}) for r in catalogue['row_types']}
    empty = [list(q) for q, domain in domains.items() if not domain]
    if empty:
        return {'status': 'EXCLUDED', 'target_rectangle': list(target), 'empty_row_types': empty}
    shared = [domains[q] for q in RECTANGLES if q != target and set(q) & set(target) for _ in range(4)]
    disjoint = [domains[q] for q in RECTANGLES if not set(q) & set(target) for _ in range(4)]
    shared_costs = attainable_costs(shared, 16)
    disjoint_costs = attainable_costs(disjoint, 40)
    nongrid = target in {tuple(e) for e in template['nongrid_edges']}
    cases = []
    for e in range(4) if nongrid else (4,):
        degree_patterns = {tuple(sorted(2 - h for h in degrees)) for _, _, degrees in corner_graphs(e)}
        for degrees in sorted(degree_patterns):
            if not all(z in domains[target] for z in degrees):
                cases.append({'internal_edges': e, 'corner_degrees': list(degrees),
                              'feasible': False, 'reason': 'Internal degrees absent from row domain.'})
                continue
            own_cost = sum(z * (z - 1) // 2 for z in degrees)
            needed = 8 - e - own_cost
            sc = shared_costs[16 - 4 * e]
            dc = disjoint_costs[32 + 2 * e]
            feasible = any(s + d == needed for s in sc for d in dc)
            cases.append({'internal_edges': e, 'corner_degrees': list(degrees),
                          'own_cost': own_cost, 'required_remaining_cost': needed,
                          'shared_sum': 16 - 4 * e, 'disjoint_sum': 32 + 2 * e,
                          'possible_shared_costs': sc, 'possible_disjoint_costs': dc,
                          'feasible': feasible})
    return {'status': 'EXCLUDED' if not any(c['feasible'] for c in cases) else 'PASSES',
            'target_rectangle': list(target), 'cases': cases,
            'projected_domains': [{'row_rectangle': list(q), 'z_values': domains[q], 'vertices': 4}
                                  for q in RECTANGLES]}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--rectangle', type=int, nargs=2, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    bundle = json.loads(a.bundle.read_text(encoding='utf-8-sig'))
    template = bundle['template']
    start = time.process_time()
    catalogue = row_catalogue(template)
    result = {'scope': __doc__, 'source_bundle': str(a.bundle), 'resources': resources,
              'catalogue': catalogue, 'global_conway_exclusion': False,
              'uses_gram_matrices': False, 'uses_prism_budget': False}
    if catalogue['status'] == 'ROW_CATALOGUE_COMPLETE':
        result['distribution'] = check_rectangle(template, catalogue, a.rectangle)
    result['cpu_seconds'] = time.process_time() - start
    atomic_json_write(a.output, result)
    print(json.dumps({'catalogue_status': catalogue['status'], 'free_dimension': catalogue.get('free_dimension'),
                      'state_counts': [r['state_count'] for r in catalogue.get('row_types', [])],
                      'distribution': result.get('distribution'), 'cpu_seconds': result['cpu_seconds']}))


if __name__ == '__main__':
    main()
