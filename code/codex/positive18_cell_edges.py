"""New necessary edge equations between the forced cells of a positive18 core.

Uses the acquired 359-core catalogue, without repeating its construction or
H/H+1 projector checks. Fractional feasibility is not a graph completion.
"""
import argparse
from collections import Counter
from itertools import combinations_with_replacement
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, hstack, eye

from higher_census_minima import ROOT


def model(record):
    graph = record['adjacency_bits']
    a = np.array([[(m >> j) & 1 for j in range(17)] for m in graph], dtype=np.int64)
    cells = record['forced_cells']
    c = np.array([x['count'] for x in cells], dtype=np.int64)
    b = np.array([[int(h in x['neighbours']) for h in range(17)] for x in cells], dtype=np.int64)
    inside = b @ a
    adjacent = b @ b.T <= 1
    for h in range(17):
        adjacent &= inside[:, h, None] + b[None, :, h] <= 2 - b[:, h, None]
    adjacent &= adjacent.T.copy()
    targets = np.column_stack((14-b.sum(axis=1), 2-b-inside)) * c[:, None]
    rr, cc, vv, pairs, bounds = [], [], [], [], []
    for i, j in combinations_with_replacement(range(len(c)), 2):
        if not adjacent[i, j]:
            continue
        cap = int(c[i]*(c[i]-1)//2) if i == j else int(c[i]*c[j])
        if not cap:
            continue
        # A doubled pair cell has its common-neighbour budget exhausted in H.
        if i != j:
            if len(cells[i]['neighbours']) == 2 and c[i] == 2:
                cap = min(cap, int(c[j]))
            if len(cells[j]['neighbours']) == 2 and c[j] == 2:
                cap = min(cap, int(c[i]))
        col = len(pairs)
        pairs.append([i, j])
        bounds.append((3, 3) if i == j == 0 else (0, cap))
        for source, other in ((i, j), (j, i)):
            rr.append(18*source); cc.append(col); vv.append(1)
            for h in np.flatnonzero(b[other]):
                rr.append(18*source+1+int(h)); cc.append(col); vv.append(1)
    matrix = coo_matrix((vv, (rr, cc)), shape=(18*len(c), len(pairs)), dtype=np.int64).tocsr()
    return matrix, targets.ravel(), bounds, pairs


def certificate(matrix, rhs, bounds):
    # Minimise b.y - sum(u_j*t_j), t <= M^T y, t <= 0, after shifting lower bounds.
    lower = np.array([x[0] for x in bounds], dtype=np.int64)
    upper = np.array([x[1] for x in bounds], dtype=np.int64)
    shifted = rhs-matrix@lower
    rows, cols = matrix.shape
    dual = linprog(np.r_[shifted, -(upper-lower)],
                   A_ub=hstack((-matrix.T, eye(cols, format='csr')), format='csr'),
                   b_ub=np.zeros(cols), bounds=[(-1, 1)]*rows+[(None, 0)]*cols,
                   method='highs', options={'time_limit': 20.0})
    if not dual.success or dual.fun >= -1e-7:
        return None
    for scale in (1, 10, 100, 1000, 10000, 100000, 1000000):
        y = np.rint(scale*dual.x[:rows]).astype(np.int64)
        coefficients = matrix.T@y
        box_min = sum(min(int(v)*int(lo), int(v)*int(hi))
                      for v, (lo, hi) in zip(coefficients, bounds))
        target = sum(int(v)*int(t) for v, t in zip(y, rhs))
        if box_min > target:
            return {'row_multipliers': [[i, int(v)] for i, v in enumerate(y) if v],
                    'box_minimum': box_min, 'target': target}
    return None


def check_certificate(matrix, rhs, bounds, cert):
    y = np.zeros(len(rhs), dtype=np.int64)
    for i, value in cert['row_multipliers']:
        y[i] = value
    coefficients = matrix.T@y
    minimum = sum(min(int(v)*int(lo), int(v)*int(hi))
                  for v, (lo, hi) in zip(coefficients, bounds))
    target = sum(int(v)*int(t) for v, t in zip(y, rhs))
    assert minimum == cert['box_minimum'] > cert['target'] == target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--indices', default='0,29,151,200,358')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--out', default='data/codex_positive18_cell_edges_pilot.json')
    args = parser.parse_args()
    source = json.loads((ROOT/'data/codex_positive18_forced_extensions.json').read_text())
    indices = list(range(len(source['records']))) if args.all else [int(i) for i in args.indices.split(',')]
    started = time.monotonic()
    records = []
    for index in indices:
        entry = source['records'][index]
        matrix, rhs, bounds, pairs = model(entry)
        solved = linprog(np.zeros(len(pairs)), A_eq=matrix, b_eq=rhs, bounds=bounds,
                         method='highs-ipm', options={'time_limit': 20.0})
        record = {'index': index, 'canonical_code': entry['canonical_code'],
                  'cubic_code': entry['cubic_code'], 'cells': len(entry['forced_cells']),
                  'edge_variables': len(pairs), 'solver_status': int(solved.status)}
        if solved.success:
            record['status'] = 'fractional_edges_feasible_unresolved'
        elif solved.status == 2:
            cert = certificate(matrix, rhs, bounds)
            if cert:
                check_certificate(matrix, rhs, bounds, cert)
                record.update(status='excluded_exact', certificate=cert)
            else:
                record['status'] = 'numerically_infeasible_uncertified'
        else:
            record['status'] = 'solver_unknown'
        records.append(record)
        if not args.all or len(records) % 30 == 0:
            print(json.dumps({'done': len(records), 'counts': dict(Counter(r['status'] for r in records))}), flush=True)
    report = {'scope': __doc__, 'source': 'codex_positive18_forced_extensions.json',
              'complete_over_359': len(records) == 359, 'records': records,
              'counts': dict(Counter(r['status'] for r in records)), 'seconds': time.monotonic()-started}
    (ROOT/args.out).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('complete_over_359', 'counts', 'seconds')}), flush=True)


if __name__ == '__main__':
    main()
