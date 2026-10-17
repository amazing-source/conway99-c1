"""General (2,2,0) six-pencil patterns and the discriminant obstruction.

All 225 placements have three relabelling types. Enumerate every integer
column model using rational elimination certificates from note203.
At r>=39 all are excluded by rank. At r=37, full-rank square determinant
models are also excluded by the ambient genus from note101.
"""
from collections import Counter, deque
from itertools import product, combinations_with_replacement
from math import prod
import argparse
import gzip
import json

from grid_kernel_rank_dense_apices import (
    ROOT, PAIRS, model, gram, affine_certificate, verify_affine,
    integer_candidates, rank_pivots, minor_det,
)

PATH = ROOT / 'data/codex_grid_kernel_rank_two_dense_apices.json.gz'


def orbits():
    states = {(a, b, ()) for a, b in product(PAIRS, repeat=2)}
    result = []
    while states:
        root = min(states)
        orbit, queue = {root}, deque([root])
        while queue:
            t = queue.popleft()
            neighbours = [(t[1], t[0], ())]
            for a in range(5):
                def swap(k):
                    return a+1 if k == a else a if k == a+1 else k
                neighbours.append(tuple(tuple(sorted(swap(k) for k in h)) for h in t))
            for u in neighbours:
                if u not in orbit:
                    orbit.add(u)
                    queue.append(u)
        assert orbit <= states
        states -= orbit
        result.append((root, len(orbit)))
    assert [n for _, n in result] == [15, 120, 90]
    return result


def ambient_types():
    result = {}
    for r in (37, 39, 41, 43):
        alpha, m = r-1, (r-15)//2
        # Note101 oddity identity forces the Legendre sign of the
        # scaled Jordan factor V. Opposite discriminant forms preserve
        # it here because alpha is even. det(K+) has square unit 9.
        signs = [delta for delta in (0, 1) if (44+8+6*alpha+4*delta) % 8 == 0]
        assert signs == [m % 2] and alpha % 2 == 0
        D = 56-r
        character = 1 if m % 2 == 0 else 6
        assert pow(6, (D-1)//2, 7) == character
        result[str(r)] = {'dimension': D, 'determinant_character': character}
    return result


def pencil_relations(hubs, grids, matrix):
    labels = [('G', k) for k in range(6)]+[('H', i, p) for i, ps in enumerate(grids) for p in ps]
    n = len(labels)
    assert n == 24
    augmented = [row+[2] for row in matrix]+[[2]*n+[1]]
    rows = [[int(v[0] == 'G') for v in labels]+[-5]]
    for i, h in enumerate(hubs):
        for k in h:
            rows.append([int((v[0] == 'G' and v[1] == k) or
                             (v[0] == 'H' and v[1] == i and k in v[2]))
                         for v in labels]+[-5])
    assert len(rows) == rank_pivots(rows)[0] == 5
    assert all(sum(a*augmented[j][k] for j, a in enumerate(row)) % 7 == 0
               for row in rows for k in range(n+1))
    assert rank_pivots(augmented)[0] == rank_pivots(matrix)[0]
    return rows


def describe(hubs, grids, values):
    matrix = gram(grids, values)
    rank, ri, ci = rank_pivots(matrix)
    assert rank >= 18
    principal_det = minor_det(matrix, ci, ci)
    assert principal_det
    relation_basis = pencil_relations(hubs, grids, matrix)
    excluded37 = rank > 19 or (rank == 19 and pow(principal_det, 3, 7) != 6)
    return {'values': values, 'rank': rank, 'principal_indices': ci,
            'principal_det_mod7': principal_det, 'order18_rows': ri[:18],
            'order18_cols': ci[:18], 'order18_det_mod7': minor_det(matrix, ri[:18], ci[:18]),
            'pencil_relation_rank': len(relation_basis), 'excluded_at_rank37': excluded37,
            'extra_relations_beyond_five_local_pencils': None if excluded37 else 25-rank-5}


def generate():
    report = {'scope': __doc__, 'ambient_types': ambient_types(), 'cases': []}
    for hubs, orbit_size in orbits():
        grids, rows, caps = model(hubs)
        proof = affine_certificate(rows)
        verify_affine(rows, proof)
        solutions = [describe(hubs, grids, values) for values in integer_candidates(rows, caps, proof)]
        report['cases'].append({'hubs': hubs, 'orbit_size': orbit_size, 'affine': proof,
                                'assignments_checked': prod(caps[j]+1 for j in proof['free']),
                                'solutions': solutions})
    with gzip.GzipFile(filename=PATH, mode='wb', mtime=0) as stream:
        stream.write(json.dumps(report, separators=(',', ':')).encode())


def verify(report):
    assert report['scope'] == __doc__ and report['ambient_types'] == ambient_types()
    representatives = orbits()
    assert len(report['cases']) == len(representatives)
    total = excluded = 0
    for record, (hubs, orbit_size) in zip(report['cases'], representatives):
        assert record['hubs'] == list(map(list, hubs)) and record['orbit_size'] == orbit_size
        grids, rows, caps = model(hubs)
        proof = record['affine']
        verify_affine(rows, proof)
        assert record['assignments_checked'] == prod(caps[j]+1 for j in proof['free'])
        candidates = list(integer_candidates(rows, caps, proof))
        assert candidates == [s['values'] for s in record['solutions']]
        for values, solution in zip(candidates, record['solutions']):
            assert solution == describe(hubs, grids, values)
            assert solution['order18_det_mod7'] != 0
        histogram = Counter((s['rank'], s['principal_det_mod7'], s['excluded_at_rank37'])
                            for s in record['solutions'])
        print('Verified', hubs, 'orbit', orbit_size, 'assignments', record['assignments_checked'],
              'candidates', len(candidates), 'rank/determinant/excluded37', dict(histogram), flush=True)
        total += len(candidates)
        excluded += sum(s['excluded_at_rank37'] for s in record['solutions'])
    assert total == 29 and excluded == 7
    # Consequence for r>=39: at most one u6=3 point on a six-grid line.
    allowed = [t for t in combinations_with_replacement((1, 2, 3), 3) if t.count(3) <= 1]
    assert all(2*t.count(3) <= t.count(1)+t.count(2) for t in allowed)
    assert 198//8 == 24
    # The common-star family has rank18 and nonsquare determinant.
    grids, _, _ = model(((0,), (0,), (0,)))
    base = gram(grids, [0]*90)  # All cross-apex intersections are known zero.
    rank, _, indices = rank_pivots(base)
    assert rank == 18 and pow(minor_det(base, indices, indices), 3, 7) == 6
    # Hence its one-dimensional orthogonal complement at r37 has square norm.
    assert {pow(t, 2, 7) for t in range(7)} == {0, 1, 2, 4}
    assert (2-2*2) % 7 not in {0, 1, 3}
    print('Verified all 225 placements; r>=39 exclusion and 6*n3<=n1+2*n2, n3<=24.', flush=True)
    print('At r37: 4 rank-obstructed and 3 discriminant-obstructed candidates; 22 remain.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    if not args.verify_only:
        generate()
    with gzip.open(PATH, 'rt') as stream:
        verify(json.load(stream))
