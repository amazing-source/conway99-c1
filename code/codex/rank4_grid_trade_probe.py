"""Exact small-core follow-up, followed by bounded binary linear pilots."""
import itertools as it
import json
from pathlib import Path
import time

import networkx as nx
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

from rank4_binary_difference_probe import bilinear, inverse, matrix

ROOT = Path(__file__).resolve().parents[2]
K3 = np.array([[0, 1, -1], [-1, 0, 1], [1, -1, 0]], dtype=int)
S9 = np.kron(K3, K3)


def signed_isomorphism(z, target):
    g = nx.from_numpy_array((z != 0).astype(int))
    h = nx.from_numpy_array((target != 0).astype(int))
    for iso in nx.algorithms.isomorphism.GraphMatcher(g, h).isomorphisms_iter():
        for global_sign in (1, -1):
            signs = {0: 1}
            stack = [0]
            good = True
            while stack and good:
                i = stack.pop()
                for j in g[i]:
                    want = signs[i] * int(z[i, j]) * global_sign * int(target[iso[i], iso[j]])
                    if j in signs and signs[j] != want:
                        good = False
                        break
                    if j not in signs:
                        signs[j] = want
                        stack.append(j)
            if good:
                return {'permutation': [iso[i] for i in range(len(z))],
                        'signs': [signs[i] for i in range(len(z))], 'global_sign': global_sign}
    return None


def fixed_common_edge_pilot(d):
    n = len(d)
    minus = (d == -1).astype(int)
    plus = (d == 1).astype(int)
    if not np.all(d.sum(axis=1) == 0):
        return {'status': 'row_sums_fail'}
    for a in (minus, plus):
        a2 = a @ a
        np.fill_diagonal(a2, 0)
        if np.any(a2 > 2 - a):
            return {'status': 'common_neighbor_bound_fail'}
    variables = [(i, j) for i in range(n) for j in range(i+1, n) if d[i, j] == 0]
    mats = []
    for i, j in variables:
        e = np.zeros((n, n), dtype=int)
        e[i, j] = e[j, i] = 1
        mats.append(e)
    target = -(minus @ d + d @ minus + d @ d + d)
    coeff = np.array([(e @ d + d @ e).ravel() for e in mats], dtype=float).T
    degree = np.array([e.sum(axis=1) for e in mats], dtype=float).T
    result = milp(np.zeros(len(variables)), integrality=np.ones(len(variables)),
                  bounds=Bounds(0, 1),
                  constraints=[LinearConstraint(coeff, target.ravel(), target.ravel()),
                               LinearConstraint(degree, 0, 8-minus.sum(axis=1))],
                  options={'time_limit': 3.0})
    out = {'n': n, 'variables': len(variables), 'solver_status': int(result.status),
           'solver_message': result.message}
    if result.x is not None:
        x = np.rint(result.x).astype(int)
        common = sum((e * b for e, b in zip(mats, x)), np.zeros_like(d))
        a = minus + common
        ap = a + d
        out['exact_linear_equation_passes'] = bool(np.all(a @ d + d @ a + d @ d + d == 0))
        out['degree_cap_passes'] = bool(np.max(a.sum(axis=1)) <= 8)
        out['common_edges'] = [edge for edge, b in zip(variables, x) if b]
        out['local_common_bounds_pass'] = all(
            np.all((b @ b - np.diag(np.diag(b @ b))) <= 2-b) for b in (a, ap))
    return out


def main():
    started = time.monotonic()
    source = json.loads((ROOT/'data/codex_rank4_binary_difference_probe.json').read_text())
    iso_records = []
    for rec in source['records']:
        inv = inverse(matrix(rec['basis_upper_triangle']))
        for survivor in rec['survivors']:
            v = survivor['vectors']
            z = np.array([[bilinear(a, inv, b) for b in v] for a in v], dtype=int)
            z[z == 6] = -1
            iso = signed_isomorphism(z, S9)
            iso_records.append({'basis': rec['basis_upper_triangle'], 'isomorphism': iso})
            assert iso is not None

    # Each occupied direction has +, -, or both; no direction is repeated
    # with the same sign. A rectangle codeword has four nonzero directions.
    rectangles = [[3*i+j for i in rows for j in cols]
                  for rows in it.combinations(range(3), 2)
                  for cols in it.combinations(range(3), 2)]
    candidates = []
    for states in it.product((0, 1, 2, 3), repeat=9):
        multiplicities = np.array([0 if x == 0 else 2 if x == 3 else 1 for x in states])
        if sum(multiplicities) < 6 or any(sum(multiplicities[r]) < 6 for r in rectangles):
            continue
        imbalance = np.array([1 if x == 1 else -1 if x == 2 else 0 for x in states])
        # The actual integer D has zero row sums on occupied positions.
        if any((S9 @ imbalance)[i] != 0 for i, x in enumerate(states) if x):
            continue
        indices, signs = [], []
        for i, x in enumerate(states):
            for sign in ([1, -1] if x == 3 else [1] if x == 1 else [-1] if x == 2 else []):
                indices.append(i)
                signs.append(sign)
        d = S9[np.ix_(indices, indices)] * np.outer(signs, signs)
        candidates.append((states, d))

    # Quotient only for the bounded pilot, retaining the complete candidate count.
    representatives = []
    for states, d in candidates:
        if any(d.shape == old.shape and signed_isomorphism(d, old) is not None
               for _, old in representatives):
            continue
        representatives.append((states, d))
    pilots = []
    for states, d in representatives:
        record = {'states': states, 'D': d.tolist(), 'pilot': fixed_common_edge_pilot(d)}
        pilots.append(record)
        print(json.dumps({'states': states, 'pilot': record['pilot']}), flush=True)
    result = {'complete_direction_classification': source['complete'],
              'nine_direction_isomorphisms': iso_records,
              'balanced_oriented_configurations': len(candidates),
              'pilot_representatives': pilots, 'seconds': time.monotonic()-started,
              'warning': 'MILP infeasibility is exploratory unless accompanied by an exact certificate.'}
    dest = ROOT/'data/codex_rank4_grid_trade_probe.json'
    dest.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({'candidate_count': len(candidates), 'representatives': len(representatives),
                      'seconds': result['seconds']}))


if __name__ == '__main__':
    main()
