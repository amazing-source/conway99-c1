"""Small exploratory boundary LP for three nongrid twin prisms.

No enumeration of SRGs or rank claim. Uses 21 fixed vertices and at most
1729 boundary profiles, not the P3/N25 pilot owned by LAP.
"""
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[2]


def explore(apex_edges):
    a = np.zeros((21, 21), dtype=np.int64)
    for block in range(3):
        for i, j in combinations(range(6), 2):
            if i // 3 == j // 3 or i % 3 == j % 3:
                a[6*block+i, 6*block+j] = a[6*block+j, 6*block+i] = 1
        for i in range(6):
            a[6*block+i, 18+i % 3] = a[18+i % 3, 6*block+i] = 1
    for i, j in [(18, 19), (19, 20)][:apex_edges]:
        a[i, j] = a[j, i] = 1
    deficit = 2 - a - a @ a
    pairs = list(combinations(range(21), 2))
    assert all(deficit[i, j] >= 0 for i, j in pairs)
    candidates = []
    # All three apices of each prism already lie in the fixed support.
    # Every other external vertex sees zero or one vertex of each prism,
    # with the same count in all three because their projections agree.
    for choices in [()] + list(product(range(6), repeat=3)):
        for apex_mask in range(8):
            b = np.zeros(21, dtype=np.int64)
            for block, vertex in enumerate(choices):
                b[6*block+vertex] = 1
            for i in range(3):
                b[18+i] = (apex_mask >> i) & 1
            support = np.flatnonzero(b)
            if any(deficit[i, j] == 0 for i, j in combinations(support, 2)):
                continue
            if np.any(a @ b > 2 - b):
                continue
            candidates.append(b)
    columns = np.array(candidates, dtype=np.int64)
    matrix = np.array([np.ones(len(columns), dtype=np.int64)]
                      + [columns[:, i] for i in range(21)]
                      + [columns[:, i]*columns[:, j] for i, j in pairs])
    rhs = np.array([78] + list(14-a.sum(axis=0))
                   + [deficit[i, j] for i, j in pairs], dtype=np.int64)
    result = linprog(np.zeros(len(columns)), A_eq=matrix, b_eq=rhs,
                     bounds=(0, None), method='highs', options={'time_limit': 20})
    report = {'apex_edges': apex_edges, 'profiles': len(columns),
              'status': int(result.status), 'message': result.message,
              'scope': 'Boundary multiplicities only; not a graph completion'}
    if result.success:
        report['max_residual'] = float(np.max(np.abs(matrix @ result.x-rhs)))
        report['nonzero_profiles'] = int(np.count_nonzero(result.x > 1e-8))
    return report


if __name__ == '__main__':
    results = [explore(e) for e in range(3)]
    (ROOT/'data/codex_nongrid_triple_prism_boundary.json').write_text(
        json.dumps(results, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(results, indent=2))
