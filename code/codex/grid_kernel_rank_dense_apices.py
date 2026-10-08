"""Exclude the (2,2,1) extra-hub pattern on a six-grid line at r>=37.

Ninety labelled column words have integer multiplicities. Pair margins,
tight-grid margins, and binary intersections restrict them to a finite
list. Rational row-combination certificates prove the affine reduction;
nonzero order-20 minors exclude every remaining intersection matrix.
All seven relabelling orbits are covered, without assuming automorphisms.
"""
from collections import Counter, deque
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from math import lcm, prod
from pathlib import Path
import argparse
import gzip
import json

import sympy as sp
from sympy.polys.matrices import DomainMatrix
from grid_kernel_rank_obstruction import rank_pivots, minor_det

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / 'data/codex_grid_kernel_rank_dense_apices.json.gz'
PAIRS = list(combinations(range(6), 2))
WORDS = [tuple(0 if k in a else 1 if k in b else 2 for k in range(6))
         for a in PAIRS for b in combinations([k for k in range(6) if k not in a], 2)]
DUADS = [tuple(tuple(k for k in range(6) if w[k] == i) for i in range(3)) for w in WORDS]


def orbits():
    states = set(product(PAIRS, PAIRS, [(i,) for i in range(6)]))
    result = []
    while states:
        root = min(states)
        orbit, queue = {root}, deque([root])
        while queue:
            t = queue.popleft()
            neighbours = [(t[1], t[0], t[2])]
            for a in range(5):
                def swap(k):
                    return a + 1 if k == a else a if k == a + 1 else k
                neighbours.append(tuple(tuple(sorted(swap(k) for k in h)) for h in t))
            for u in neighbours:
                if u not in orbit:
                    orbit.add(u)
                    queue.append(u)
        assert orbit <= states
        states -= orbit
        result.append((root, len(orbit)))
    assert len(result) == 7 and sum(n for _, n in result) == 1350
    return result


def model(hubs):
    grids = [[p for p in PAIRS if set(p) & set(h)] for h in hubs]
    rows = []
    for a, b in PAIRS:
        for i in range(3):
            for j in range(3):
                rows.append([int(w[a] == i and w[b] == j) for w in WORDS]
                            + [4 if i == j else 8])
    for i, pairs in enumerate(grids):
        for a, b in pairs:
            for k in range(6):
                if k in (a, b):
                    continue
                for j in range(3):
                    if j != i:
                        rows.append([int(w[a] == w[b] == i and w[k] == j) for w in WORDS] + [2])
    caps = [1 if sum(d[i] in grids[i] for i in range(3)) >= 2 else 4 for d in DUADS]
    return grids, rows, caps


def gram(grids, values):
    labels = [('G', k) for k in range(6)] + [('H', i, p) for i, ps in enumerate(grids) for p in ps]
    matrix = [[0] * len(labels) for _ in labels]
    lookup = {word: i for i, word in enumerate(WORDS)}
    for i, u in enumerate(labels):
        for j in range(i, len(labels)):
            v = labels[j]
            if u == v:
                x = 9
            elif u[0] == v[0] == 'G':
                x = 3
            elif u[0] == 'G' or v[0] == 'G':
                g, h = (u, v) if u[0] == 'G' else (v, u)
                x = 3 if g[1] in h[2] else 1
            elif u[1] == v[1]:
                x = 3 if set(u[2]) & set(v[2]) else 1
            elif set(u[2]) & set(v[2]):
                x = 0
            else:
                remaining_colour = 3 - u[1] - v[1]
                word = tuple(u[1] if k in u[2] else v[1] if k in v[2] else remaining_colour
                             for k in range(6))
                x = values[lookup[word]]
                assert 0 <= x <= 1
            matrix[i][j] = matrix[j][i] = x
    return matrix


def affine_certificate(rows):
    matrix = sp.Matrix(rows)
    _, basis = DomainMatrix.from_Matrix(matrix[:, :90].T).rref()
    selected = matrix[list(basis), :]
    augmented = selected.row_join(sp.eye(len(basis)))
    reduced, pivots = DomainMatrix.from_Matrix(augmented).rref()
    reduced = reduced.to_Matrix()
    assert len(pivots) == len(basis) and all(p < 90 for p in pivots)
    free = [j for j in range(90) if j not in pivots]
    expressions = []
    for t, pivot in enumerate(pivots):
        expressions.append({
            'pivot': pivot, 'constant': str(reduced[t, 90]),
            'terms': [[j, str(-reduced[t, j])] for j in free if reduced[t, j]],
            'combination': [[int(basis[j]), str(reduced[t, 91 + j])]
                            for j in range(len(basis)) if reduced[t, 91 + j]]})
    return {'free': free, 'expressions': expressions}


def verify_affine(rows, proof):
    free = proof['free']
    pivots = [row['pivot'] for row in proof['expressions']]
    assert sorted(free + pivots) == list(range(90))
    for row in proof['expressions']:
        actual = [F(0)] * 91
        for i, coefficient in row['combination']:
            assert 0 <= i < len(rows)
            coefficient = F(coefficient)
            for j, a in enumerate(rows[i]):
                if a:
                    actual[j] += coefficient * a
        expected = [F(0)] * 91
        expected[row['pivot']] = F(1)
        expected[90] = F(row['constant'])
        assert len({j for j, _ in row['terms']}) == len(row['terms'])
        for j, coefficient in row['terms']:
            assert j in free
            expected[j] = -F(coefficient)
        assert actual == expected


def integer_candidates(rows, caps, proof):
    free = proof['free']
    affine = []
    for row in proof['expressions']:
        constant = F(row['constant'])
        terms = [(j, F(c)) for j, c in row['terms']]
        denominator = lcm(constant.denominator, *(c.denominator for _, c in terms))
        affine.append((row['pivot'], denominator, int(constant * denominator),
                       [(j, int(c * denominator)) for j, c in terms]))
    for assignment in product(*(range(caps[j] + 1) for j in free)):
        values = [0] * 90
        for j, value in zip(free, assignment):
            values[j] = value
        valid = True
        for pivot, denominator, constant, terms in affine:
            numerator = constant + sum(c * values[j] for j, c in terms)
            if numerator % denominator or not 0 <= numerator <= caps[pivot] * denominator:
                valid = False
                break
            values[pivot] = numerator // denominator
        if valid and all(sum(a * b for a, b in zip(row[:90], values)) == row[90] for row in rows):
            yield values


def generate():
    report = {'scope': __doc__, 'cases': []}
    for hubs, orbit_size in orbits():
        grids, rows, caps = model(hubs)
        proof = affine_certificate(rows)
        verify_affine(rows, proof)
        solutions = []
        for values in integer_candidates(rows, caps, proof):
            matrix = gram(grids, values)
            rank, ri, ci = rank_pivots(matrix)
            assert rank >= 20, (hubs, values, rank)
            ri, ci = ri[:20], ci[:20]
            determinant = minor_det(matrix, ri, ci)
            assert determinant
            solutions.append({'values': values, 'rank': rank, 'rows': ri, 'cols': ci, 'det_mod7': determinant})
        record = {'hubs': hubs, 'orbit_size': orbit_size, 'affine': proof,
                  'assignments_checked': prod(caps[j] + 1 for j in proof['free']), 'solutions': solutions}
        report['cases'].append(record)
        print(hubs, 'free', len(proof['free']), 'assignments', record['assignments_checked'],
              'solutions', len(solutions), 'ranks', dict(Counter(s['rank'] for s in solutions)), flush=True)
    with gzip.GzipFile(filename=PATH, mode='wb', mtime=0) as stream:
        stream.write(json.dumps(report, separators=(',', ':')).encode('utf-8'))


def verify(report):
    assert report['scope'] == __doc__
    representatives = orbits()
    assert len(report['cases']) == len(representatives)
    total = 0
    for record, (hubs, orbit_size) in zip(report['cases'], representatives):
        assert record['hubs'] == [list(h) for h in hubs] and record['orbit_size'] == orbit_size
        grids, rows, caps = model(hubs)
        proof = record['affine']
        verify_affine(rows, proof)
        assert record['assignments_checked'] == prod(caps[j] + 1 for j in proof['free'])
        candidates = list(integer_candidates(rows, caps, proof))
        assert candidates == [s['values'] for s in record['solutions']]
        for solution in record['solutions']:
            matrix = gram(grids, solution['values'])
            ri, ci = solution['rows'], solution['cols']
            assert len(ri) == len(ci) == len(set(ri)) == len(set(ci)) == 20
            assert all(0 <= i < len(matrix) for i in ri + ci)
            assert minor_det(matrix, ri, ci) == solution['det_mod7'] != 0
            assert rank_pivots(matrix)[0] == solution['rank'] >= 20
        total += len(candidates)
        print('Verified orbit', hubs, 'size', orbit_size, 'integer candidates', len(candidates),
              'ranks', dict(Counter(s['rank'] for s in record['solutions'])), flush=True)
    print('Verified all 1350 placements in seven orbits;', total, 'order-20 minor certificates.', flush=True)
    allowed = []
    for triple in combinations_with_replacement((1, 2, 3), 3):
        if triple.count(3) >= 2 and min(triple) >= 2:
            continue
        assert 4 * triple.count(1) + triple.count(2) - 2 * triple.count(3) >= 0
        allowed.append(triple)
    assert len(allowed) == 8
    print('Verified incidence cut: 3*n3 <= 2*n1+n2, hence n3 <=39 on 99 vertices.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    if args.verify_only:
        with gzip.open(PATH, 'rt', encoding='utf-8') as stream:
            verify(json.load(stream))
    else:
        generate()
