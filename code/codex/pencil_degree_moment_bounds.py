"""Pointwise degree moments for grid-pencil collision counts (note 198).

The note 197 model imposed first moments of degrees in B and the three
apex fibres of Z. Here we also impose all centred second moments, including
mixed ones. Every row follows from the prescribed degrees of each vertex.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from math import comb
import argparse
import gzip
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, vstack

from higher_census_minima import ROOT
from pencil_collision_bounds import model as base_model, read
from six_three_mass6_profile_lp import certificate
from f0_prism_bounds import verify


def model(m):
    caps, rows, matrix, constants, objectives = base_model(m)
    packet = read(f'codex_pencil_{m}_patterns')
    meta = packet['cells']; patterns = packet['by_outside_size']['3']['patterns']
    offset = len(caps)-len(patterns)
    moments = defaultdict(dict)
    counts90 = []; triangles_z = []
    for t, pattern in enumerate(patterns):
        ids = pattern['profiles']; edges = pattern['edges']
        adjacency = [[0]*3 for _ in range(3)]
        for bit, (i, j) in enumerate(combinations(range(3), 2)):
            adjacency[i][j] = adjacency[j][i] = (edges >> bit) & 1
        kinds = [meta[i]['kind'] for i in ids]
        # An independent check of the previously enumerated 90_90 cost.
        criterion = sum({'Z': 0, 'B': 1, 'A': 2}[kind] for kind in kinds)+edges.bit_count()
        count = 2*int(criterion == 5)
        assert pattern['counts']['90_90'] == count
        counts90.append(count)
        triangles_z.append(int(kinds == ['Z']*3 and edges == 7))
        for centre in range(3):
            ends = [i for i in range(3) if i != centre]
            if not all(adjacency[centre][end] for end in ends):
                continue
            groups = []
            for end in ends:
                cell = meta[ids[end]]
                groups.append(0 if cell['kind'] == 'B' else
                              1+cell['colour'] if cell['kind'] == 'Z' else -1)
            if -1 in groups:
                continue
            key = (ids[centre], *sorted(groups))
            coefficients = moments[key]
            coefficients[offset+t] = coefficients.get(offset+t, 0)+1
    extra = []
    for i, cell in enumerate(meta):
        if cell['kind'] == 'B':
            degrees = [8]+cell['quota']
        elif cell['kind'] == 'Z':
            degrees = [10, 1, 1, 1]
        else:
            degrees = [0]+[8*int(c == cell['colour']) for c in range(3)]
        for a, b in combinations_with_replacement(range(4), 2):
            value = comb(degrees[a], 2) if a == b else degrees[a]*degrees[b]
            value *= cell['size']
            coefficients = moments[(i, a, b)]
            name = f'pointwise_degree_moment_{i}_{a}_{b}'
            extra.append((name+'+', -value, coefficients))
            extra.append((name+'-', value, {j: -v for j, v in coefficients.items()}))
    rr, cc, vv = [], [], []
    for r, (_, _, coefficients) in enumerate(extra):
        for c, v in coefficients.items():
            rr.append(r); cc.append(c); vv.append(v)
    addon = coo_matrix((vv, (rr, cc)), shape=(len(extra), len(caps))).tocsr()
    rows += extra; matrix = vstack((matrix, addon)).tocsr()
    constants = np.concatenate((constants, np.array([v for _, v, _ in extra], dtype=float)))
    objectives['90_90'] = (0, [0]*offset+[-v for v in counts90])
    identity = [0]*offset+[-v+12*t for v, t in zip(counts90, triangles_z)]
    objectives['90_identity_upper'] = (0, identity)
    objectives['90_identity_negative'] = (0, [-v for v in identity])
    return caps, rows, matrix, constants, objectives


def run(m, verify_only=False, selected=None):
    start = time.monotonic()
    caps, rows, matrix, constants, objectives = model(m)
    path = ROOT/f'data/codex_pencil_{m}_degree_moments.json.gz'
    if verify_only or path.exists():
        with gzip.open(path, 'rt') as stream:
            report = json.load(stream)
    else:
        report = {'pencil_size': m, 'results': {}, 'scope': __doc__}
    if verify_only:
        assert report['variables'] == len(caps) and report['rows'] == len(rows)
        if selected is None:
            selected = list(report['results'])
    else:
        report.update(variables=len(caps), rows=len(rows))
    for label, (offset, objective) in objectives.items():
        if selected is not None and label not in selected:
            continue
        if not verify_only:
            print('Solving degree moments', m, label, flush=True)
            result = linprog(np.array(objective, dtype=float), A_ub=-matrix,
                             b_ub=constants, bounds=list(zip([0]*len(caps), caps)),
                             method='highs-ipm')
            assert result.success, result.message
            proof = certificate(rows, caps, objective, result)
            upper = F(proof['collision_upper_bound'])+offset
            report['results'][label] = {'certificate': proof, 'objective_constant': offset,
                                       'upper_bound': str(upper), 'even_upper_bound': int(2*(upper//2))}
        record = report['results'][label]
        verify(rows, caps, objective, record['certificate'])
        upper = F(record['certificate']['collision_upper_bound'])+offset
        assert record['objective_constant'] == offset and F(record['upper_bound']) == upper
        assert record['even_upper_bound'] == 2*(upper//2)
        print('Verified degree moments', m, label, '<=', record['even_upper_bound'],
              'rational', str(upper), 'seconds', round(time.monotonic()-start, 1), flush=True)
        if not verify_only:
            with gzip.GzipFile(filename=path, mode='wb', mtime=0) as stream:
                stream.write(json.dumps(report).encode())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, choices=(2, 3, 4, 6), required=True)
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--objectives', nargs='+')
    args = parser.parse_args()
    run(args.size, args.verify_only, args.objectives)
