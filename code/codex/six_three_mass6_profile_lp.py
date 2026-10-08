"""Exact certified collision bounds from the full exterior profile counts.

Fixed twin prisms leave 40 neighbourhood profiles of known sizes. Pair and
triple counts satisfy degree and common-neighbour identities. HiGHS locates
dual weights; rational residuals are covered by rigorous variable bounds.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from math import comb, floor
import gzip
import json
import time
import sys
from types import SimpleNamespace

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

from higher_census_minima import ROOT


def build(data):
    profiles = data['profiles']; graph = data['core_adjacency']; patterns = data['patterns']
    pairs = [(i, j) for i in range(len(profiles)) for j in range(i, len(profiles))
             if i != j or profiles[i][1] >= 2]
    pair_index = {pair: i for i, pair in enumerate(pairs)}
    offset = len(pairs)
    caps = [profiles[i][1]*profiles[j][1] if i != j else comb(profiles[i][1], 2) for i, j in pairs]
    caps += [int(np.prod([comb(profiles[i][1], m) for i, m in Counter(row['profiles']).items()])) for row in patterns]
    rows = []
    def eq(name, constant, coefficients):
        coefficients = {j: int(value) for j, value in coefficients.items() if value}
        rows.append((name+'+', int(constant), coefficients))
        rows.append((name+'-', -int(constant), {j: -value for j, value in coefficients.items()}))
    # Every outside vertex has its prescribed 0,1,2 neighbours in each prism.
    for i, (mask, count) in enumerate(profiles):
        regularity = {}
        for j in range(len(profiles)):
            pair = tuple(sorted((i, j)))
            if pair in pair_index:
                regularity[pair_index[pair]] = 2 if i == j else 1
        eq(f'degree_{i}', -count*(14-mask.bit_count()), regularity)
        for u in range(12):
            target = (1 if mask >> u & 1 else 2)-(graph[u] & mask).bit_count()
            coefficients = {index: value for index, value in regularity.items()
                            if profiles[pairs[index][1] if pairs[index][0] == i else pairs[index][0]][0] >> u & 1}
            eq(f'common_core_{i}_{u}', -count*target, coefficients)
    group_rows = defaultdict(dict); edge_rows = defaultdict(dict)
    wedge_rows = defaultdict(dict); triangle_rows = defaultdict(dict)
    local_pairs = list(combinations(range(3), 2))
    for t, row in enumerate(patterns):
        ids, mask = tuple(row['profiles']), row['edges']; index = offset+t
        group_rows[ids][index] = 1
        adjacency = [[0]*3 for _ in range(3)]
        for bit, (a, b) in enumerate(local_pairs):
            adjacency[a][b] = adjacency[b][a] = (mask >> bit) & 1
            if mask >> bit & 1:
                key = (ids, (ids[a], ids[b]))
                edge_rows[key][index] = edge_rows[key].get(index, 0)+1
        for a, b in local_pairs:
            middle = 3-a-b
            if adjacency[a][middle] and adjacency[b][middle]:
                pair = (ids[a], ids[b])
                wedge_rows[pair][index] = wedge_rows[pair].get(index, 0)+1
                if adjacency[a][b]:
                    triangle_rows[pair][index] = triangle_rows[pair].get(index, 0)+1
    for ids in combinations_with_replacement(range(len(profiles)), 3):
        multiplicities = Counter(ids)
        if any(n > profiles[i][1] for i, n in multiplicities.items()):
            continue
        total = 1
        for i, n in multiplicities.items():
            total *= comb(profiles[i][1], n)
        eq(f'triple_total_{ids}', -total, group_rows[ids])
        for pair in set(combinations(ids, 2)):
            rest = list(ids)
            for i in pair:
                rest.remove(i)
            third = rest[0]
            factor = profiles[third][1]-sum(i == third for i in pair)
            coefficients = dict(edge_rows[(ids, pair)])
            coefficients[pair_index[pair]] = -factor
            eq(f'edge_marginal_{ids}_{pair}', 0, coefficients)
    for pair, index in pair_index.items():
        i, j = pair
        common_core = (profiles[i][0] & profiles[j][0]).bit_count()
        # Sum common neighbours for all pairs, and separately for adjacent pairs.
        coefficients = dict(wedge_rows[pair]); coefficients[index] = 1
        eq(f'common_outside_{pair}', -(2-common_core)*caps[index], coefficients)
        coefficients = dict(triangle_rows[pair]); coefficients[index] = -(1-common_core)
        eq(f'triangles_through_pair_{pair}', 0, coefficients)
    rr, cc, values = [], [], []
    for i, (_, _, row) in enumerate(rows):
        for j, value in row.items():
            rr.append(i); cc.append(j); values.append(value)
    matrix = coo_matrix((values, (rr, cc)), shape=(len(rows), len(caps))).tocsr()
    constants = np.array([c for _, c, _ in rows], dtype=float)
    print('Profile LP:', len(caps), 'variables;', len(rows), 'rows;', matrix.nnz, 'nonzero coefficients', flush=True)
    return pairs, caps, rows, matrix, constants


def certificate(rows, caps, objective, result):
    weights = [(i, F(round(float(-w)*10**9), 10**9))
               for i, w in enumerate(result.ineqlin.marginals) if -w > 1e-9]
    residual = list(map(F, objective)); constant = F(0)
    for i, weight in weights:
        assert weight >= 0
        constant += weight*rows[i][1]
        for j, value in rows[i][2].items():
            residual[j] -= weight*value
    # For 0<=x_j<=U_j, residual_j*x_j >= min(0,residual_j)*U_j.
    correction = sum(value*cap for value, cap in zip(residual, caps) if value < 0)
    lower_bound = -constant+correction
    upper = -lower_bound
    return {'collision_upper_bound': str(upper), 'even_integer_upper_bound': 2*floor(upper/2),
            'row_weights': [(rows[i][0], str(weight)) for i, weight in weights],
            'residual_coefficients': {str(i): str(value) for i, value in enumerate(residual) if value},
            'weighted_constant': str(constant), 'bound_correction': str(correction),
            'numerical_upper_value': -float(result.fun),
            'scope': 'Exact rational inequality with certified finite variable bounds; no rational optimum asserted.'}


def main():
    start = time.monotonic()
    with gzip.open(ROOT/'data/codex_six_three_mass6_patterns.json.gz', 'rt', encoding='utf-8') as stream:
        data = json.load(stream)
    pairs, caps, rows, matrix, constants = build(data)
    path = ROOT/'data/codex_six_three_mass6_profile_lp.json'
    if '--compact-certificates' in sys.argv or '--verify-only' in sys.argv:
        report = json.loads(path.read_text())
        indices = {name: i for i, (name, _, _) in enumerate(rows)}
        for name, proof in list(report['results'].items()):
            objective = [0]*len(pairs)+[-row['counts'][name] for row in data['patterns']]
            if '--compact-certificates' in sys.argv:
                marginals = np.zeros(len(rows))
                for label, weight in proof['row_weights']:
                    marginals[indices[label]] = -float(F(weight))
                result = SimpleNamespace(ineqlin=SimpleNamespace(marginals=marginals), fun=-proof['numerical_upper_value'])
                proof = certificate(rows, caps, objective, result)
                report['results'][name] = proof
            residual = list(map(F, objective)); constant = F(0)
            for label, weight in proof['row_weights']:
                weight = F(weight); assert weight >= 0
                row = rows[indices[label]]
                constant += weight*row[1]
                for j, value in row[2].items():
                    residual[j] -= weight*value
            correction = sum(value*cap for value, cap in zip(residual, caps) if value < 0)
            upper = constant-correction
            assert upper == F(proof['collision_upper_bound'])
            assert constant == F(proof['weighted_constant']) and correction == F(proof['bound_correction'])
            assert {str(i): str(v) for i, v in enumerate(residual) if v} == proof['residual_coefficients']
            assert 2*floor(upper/2) == proof['even_integer_upper_bound']
            print('Verified', name, '<=', proof['even_integer_upper_bound'], flush=True)
        if '--compact-certificates' in sys.argv:
            path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
        return
    report = {'variables': len(caps), 'constraints': len(rows), 'pair_order': pairs, 'variable_caps': caps,
              'results': {}, 'scope': 'Internal mass-six collision pairs per unordered twin-prism pair, both signs.'}
    names = ['Q6_no_prism', 'Q8_no_prism']
    if '--all' in sys.argv:
        names += ['Q6_all', 'Q8_all']
    for name in names:
        objective = [0]*len(pairs)+[-row['counts'][name] for row in data['patterns']]
        result = linprog(np.array(objective, dtype=float), A_ub=-matrix, b_ub=constants,
                         bounds=list(zip([0]*len(caps), caps)), method='highs')
        assert result.success, result.message
        proof = certificate(rows, caps, objective, result)
        report['results'][name] = proof
        print(name, '<=', proof['even_integer_upper_bound'], '; rational bound about', float(F(proof['collision_upper_bound'])),
              '; seconds', round(time.monotonic()-start, 1), flush=True)
        (ROOT/'data/codex_six_three_mass6_profile_lp.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
