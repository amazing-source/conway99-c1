"""A rank-independent, exhaustive catalogue around an unavoidable defect.

Two triangles joined by exactly two edges force eight vertices with two
neighbours in the seed. Catalogue their 14-vertex cores, preserving the
distinguished seed. This is NOT a catalogue of complete SRGs/completions.
"""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
import json
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
SEED = {(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4)}
MASKS = [(0, 3), (1, 4), (2, 3), (2, 4), (0, 5), (1, 5), (2, 5), (2, 5)]
PAIRS = list(combinations(range(14), 2))


def base_rows():
    rows = [0]*14
    for u, v in list(SEED)+[(i, p) for i, mask in enumerate(MASKS, 6) for p in mask]:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return rows


def valid(rows):
    return all((rows[u] & rows[v]).bit_count() <= 2-((rows[u] >> v) & 1)
               for u, v in PAIRS)


def toggle(rows, u, v):
    rows[u] ^= 1 << v
    rows[v] ^= 1 << u


def enumerate_cores():
    rows = base_rows()
    assert valid(rows)
    edges = []
    for u, v in combinations(range(6, 14), 2):
        toggle(rows, u, v)
        if valid(rows):
            edges.append((u, v))
        toggle(rows, u, v)
    found = []
    nodes = 0

    def dfs(pos, bits):
        nonlocal nodes
        nodes += 1
        if pos == len(edges):
            found.append(bits)
            return
        dfs(pos+1, bits)
        u, v = edges[pos]
        toggle(rows, u, v)
        if valid(rows):
            dfs(pos+1, bits | (1 << pos))
        toggle(rows, u, v)

    dfs(0, 0)
    return edges, found, nodes


def automorphisms(edges):
    actions = []
    for p in permutations(range(6)):
        if {tuple(sorted((p[u], p[v]))) for u, v in SEED} != SEED:
            continue
        for swap in (0, 1):
            full = list(p)
            for i, mask in enumerate(MASKS):
                dest = tuple(sorted(p[u] for u in mask))
                candidates = [6+j for j, other in enumerate(MASKS) if other == dest]
                full.append(candidates[0] if len(candidates) == 1 else candidates[(i-6+swap) % 2])
            assert len(set(full)) == 14
            actions.append([edges.index(tuple(sorted((full[u], full[v])))) for u, v in edges])
    assert len(actions) == 8
    return actions


def transform(bits, action):
    return sum(1 << action[i] for i in range(len(action)) if (bits >> i) & 1)


def matrix(bits, edges):
    rows = base_rows()
    for i, (u, v) in enumerate(edges):
        if (bits >> i) & 1:
            toggle(rows, u, v)
    return np.array([[(rows[u] >> v) & 1 for v in range(14)] for u in range(14)], dtype=np.int64)


def is_psd_exact(matrix):
    """Rational symmetric elimination, including singular PSD matrices."""
    a = [[Fraction(int(x)) for x in row] for row in matrix]
    size = len(a)
    rank = 0
    for k in range(size):
        if any(a[i][i] < 0 for i in range(k, size)):
            return False, None
        pivot = next((i for i in range(k, size) if a[i][i] > 0), None)
        if pivot is None:
            return all(a[i][j] == 0 for i in range(k, size) for j in range(k, size)), rank
        a[k], a[pivot] = a[pivot], a[k]
        for row in a:
            row[k], row[pivot] = row[pivot], row[k]
        d = a[k][k]
        for i in range(k+1, size):
            for j in range(i, size):
                a[i][j] -= a[i][k]*a[j][k]/d
                a[j][i] = a[i][j]
        rank += 1
    return True, rank


def quadratic(a, z):
    return sum(int(a[i, j])*int(z[i])*int(z[j]) for i in range(len(z)) for j in range(len(z)))


def negative_witness(a):
    # Floats only propose a short integer vector; integer arithmetic certifies it.
    _, vectors = np.linalg.eigh(a)
    for scale in (10, 100, 1000, 10000, 100000, 1000000):
        z = np.rint(scale*vectors[:, 0]).astype(np.int64).tolist()
        q = quadratic(a, z)
        if q < 0:
            return {'vector': z, 'quadratic_value': q}
    raise AssertionError('failed to produce an exact negative witness')


def profile():
    s = matrix(0, [])[:6, :6]
    s2 = s@s
    pairs = list(combinations(range(6), 2))
    deficit = {p: 2-int(s[p])-int(s2[p]) for p in pairs}
    masks = []
    for bits in product((0, 1), repeat=6):
        if any(bits[u]*bits[v] and deficit[u, v] == 0 for u, v in pairs):
            continue
        if any(sum(int(s[u, v])*bits[v] for v in range(6)) > 2-bits[u] for u in range(6)):
            continue
        masks.append(bits)
    incidence = sp.Matrix([[1]*len(masks)]+[[b[u] for b in masks] for u in range(6)]+
                          [[b[u]*b[v] for b in masks] for u, v in pairs])
    k = sp.Symbol('k')
    rhs = sp.Matrix([k*k/2-5]+[k-int(s[u].sum()) for u in range(6)]+[deficit[p] for p in pairs])
    solution = list(sp.linsolve((incidence, rhs)))[0]
    assert incidence.rank() == len(masks) == 14
    return [{'support': [i for i, b in enumerate(bits) if b], 'size_formula': str(expr),
             'size_at_14': int(expr.subs(k, 14)), 'size_at_22': int(expr.subs(k, 22))}
            for bits, expr in zip(masks, solution)]


def positive_control(edges, actions, representatives):
    a = np.zeros((243, 243), dtype=np.int64)
    for line in (ROOT/'data/srg243/twin243_switched.edges').read_text().splitlines():
        u, v = map(int, line.split())
        a[u, v] = a[v, u] = 1
    assert np.all(a.sum(axis=0) == 22)
    assert np.array_equal(a@a+a, 20*np.eye(243, dtype=np.int64)+2)
    triangles = [(u, v, w) for u, v in combinations(range(243), 2) if a[u, v]
                 for w in np.flatnonzero(a[u] & a[v]).tolist() if w > v]
    seed = None
    for left, right in combinations(triangles, 2):
        if set(left) & set(right):
            continue
        cross = [(u, v) for u in left for v in right if a[u, v]]
        if len(cross) == 2:
            (x, y), (xx, yy) = cross
            seed = [x, xx, next(iter(set(left)-{x, xx})), y, yy, next(iter(set(right)-{y, yy}))]
            break
    assert seed is not None
    groups = {}
    for u in range(243):
        if u not in seed:
            mask = tuple(i for i, v in enumerate(seed) if a[u, v])
            groups.setdefault(mask, []).append(u)
    expected = {tuple(item['support']): item['size_at_22'] for item in profile()}
    assert {m: len(vertices) for m, vertices in groups.items()} == expected
    extra = [groups[mask][0 if i < 6 else i-6] for i, mask in enumerate(MASKS)]
    core = seed+extra
    actual = a[np.ix_(core, core)]
    bits = sum(1 << i for i, (u, v) in enumerate(edges) if actual[u, v])
    assert np.array_equal(actual, matrix(bits, edges))
    canonical = min(transform(bits, p) for p in actions)
    assert canonical in representatives
    c = groups[()]
    core_edges = int(a[np.ix_(extra, extra)].sum()//2)
    empty_edges = int(a[np.ix_(c, c)].sum()//2)
    assert len(c) == 129 and empty_edges == 705+core_edges
    assert all(int(a[u, c].sum()) == 10+int(a[u, extra].sum()) for u in c)
    return {'graph': 'twin243_switched.edges', 'seed': seed, 'core': core,
            'representative': canonical, 'empty_cell_size': len(c),
            'empty_cell_edges': empty_edges, 'extra_core_edges': core_edges}


def build():
    edges, labelled, nodes = enumerate_cores()
    actions = automorphisms(edges)
    representatives = sorted({min(transform(b, p) for p in actions) for b in labelled})
    labelled_set = set(labelled)
    orbits = {b: {transform(b, p) for p in actions} for b in representatives}
    assert set().union(*orbits.values()) == labelled_set
    assert sum(map(len, orbits.values())) == len(labelled)
    results = []
    for bits in representatives:
        a = matrix(bits, edges)
        minus = 27*np.eye(14, dtype=np.int64)-9*a+1
        plus = 44*np.eye(14, dtype=np.int64)+11*a-2
        pm, rm = is_psd_exact(minus)
        pp, rp = is_psd_exact(plus)
        row = {'bits': bits, 'orbit_size': len(orbits[bits]), 'extra_edges': bits.bit_count(),
               'passes_two_real_projectors': pm and pp}
        if not pm or not pp:
            row['projector'] = 'minus4' if not pm else 'plus3'
            row['certificate'] = negative_witness(minus if not pm else plus)
        else:
            row['real_projector_ranks'] = [rm, rp]
        results.append(row)
    rejected = sum(not r['passes_two_real_projectors'] for r in results)
    return {'scope': 'rooted 14-vertex cores only, no classification of their SRG completions',
            'profile': profile(), 'optional_edges': edges, 'group_order': len(actions),
            'labelled_count': len(labelled), 'dfs_nodes': nodes,
            'labelled_edge_histogram': dict(sorted(Counter(b.bit_count() for b in labelled).items())),
            'core_count': len(results), 'excluded_core_count': rejected,
            'remaining_core_count': len(results)-rejected, 'cores': results,
            'positive_control': positive_control(edges, actions, representatives)}


def verify(report):
    edges, labelled, _ = enumerate_cores()
    actions = automorphisms(edges)
    reps = sorted({min(transform(b, p) for p in actions) for b in labelled})
    assert [r['bits'] for r in report['cores']] == reps
    assert report['optional_edges'] == [list(e) for e in edges]
    assert report['profile'] == profile()
    assert report['labelled_count'] == len(labelled)
    assert report['group_order'] == len(actions)
    rejected = 0
    for row in report['cores']:
        a = matrix(row['bits'], edges)
        mats = {'minus4': 27*np.eye(14, dtype=np.int64)-9*a+1,
                'plus3': 44*np.eye(14, dtype=np.int64)+11*a-2}
        assert row['orbit_size'] == len({transform(row['bits'], p) for p in actions})
        assert row['extra_edges'] == row['bits'].bit_count()
        if row['passes_two_real_projectors']:
            checks = [is_psd_exact(m) for m in mats.values()]
            assert all(p for p, _ in checks)
            assert row['real_projector_ranks'] == [r for _, r in checks]
        else:
            rejected += 1
            cert = row['certificate']
            assert len(cert['vector']) == 14 and all(type(x) is int for x in cert['vector'])
            assert quadratic(mats[row['projector']], cert['vector']) == cert['quadratic_value'] < 0
    assert report['core_count'] == len(reps)
    assert report['excluded_core_count'] == rejected
    assert report['remaining_core_count'] == len(reps)-rejected
    assert report['positive_control'] == positive_control(edges, actions, reps)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    if args.verify_only:
        report = json.loads(args.out.read_text(encoding='utf-8'))
        verify(report)
    else:
        report = build()
        args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('labelled_count', 'core_count', 'excluded_core_count',
                                           'remaining_core_count', 'positive_control')}))


if __name__ == '__main__':
    main()
