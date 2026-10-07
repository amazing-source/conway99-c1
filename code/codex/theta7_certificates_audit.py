"""Independent exact verification of LAB theta certificates and ladder.

No LAB Python module or optimisation solver is imported. Coefficients are
reconstructed in c_1,...,c_7 coordinates using our eta recurrence; LAB uses
b_1,...,b_7 coordinates. Ladder multipliers are recovered from its supports.
All arithmetic uses standard-library Fraction.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json
import re

from theta7_audit import basis

ROOT = Path(__file__).resolve().parents[2]
LOWER = {2: 462, 3: 24948, 4: 388080, 5: 196812}


def scaled(v, s):
    return [s*x for x in v]


def total(vectors):
    return [sum(xs, F(0)) for xs in zip(*vectors)]


def family(alpha, forms):
    cs = [[F(0)] * 8 for _ in range(15)]
    cs[0][0] = F(7)**(25-alpha//2)
    for j in range(1, 8):
        cs[j][j] = F(1)
    # Independently recover fixed coordinates from a_0=1, a_1=...=a_6=0.
    for n in range(7):
        j = 14-n
        cs[j][0] = F(n == 0) - sum(cs[k][0]*forms[k][n] for k in range(j+1, 15))
    ds = [scaled(cs[14-i], F(7)**(alpha//2+3-2*i)) for i in range(15)]
    def expansion(coords):
        return [total([scaled(coords[j], forms[j][n]) for j in range(15)])
                for n in range(len(forms[0]))]
    a, b = expansion(cs), expansion(ds)
    assert a[0] == b[0] == [1]+[0]*7
    assert all(a[n] == [0]*8 for n in range(1, 7))
    return a, b


def constraint(label, a, b, zeros):
    """Strictly admit only independently justified constraints."""
    m = re.fullmatch(r'([ab])_(\d+) >= (\d+)', label)
    if m:
        side, ns, ls = m.groups()
        n, lower = int(ns), int(ls)
        assert 1 <= n < len(a)
        assert lower == 0 or side == 'b' and LOWER.get(n) == lower
        row = list((a if side == 'a' else b)[n])
        row[0] -= lower
        return row
    m = re.fullmatch(r'a_(\d+) >= b_(\d+)', label)
    if m:
        n, k = map(int, m.groups())
        assert n == 7*k and 1 <= n < len(a)
        return total([a[n], scaled(b[k], -1)])
    m = re.fullmatch(r'a_(\d+) <= 0', label)
    assert m is not None, label
    n = int(m[1])
    assert n in zeros, (label, zeros)
    return scaled(a[n], -1)


def verify(certificate, a, b, zeros):
    weights = [F(weight) for _, weight in certificate]
    assert all(w > 0 for w in weights)
    rows = [constraint(label, a, b, zeros) for label, _ in certificate]
    result = total([scaled(row, weight) for row, weight in zip(rows, weights)])
    assert result[1:] == [0]*7, result
    assert result[0] < 0, result
    return result[0]


def solve(matrix, rhs):
    """Small square rational Gaussian elimination, with residual check."""
    n = len(rhs)
    original = [list(map(F, row)) for row in matrix]
    aug = [row+[F(y)] for row, y in zip(original, rhs)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[pivot] = aug[pivot], aug[j]
        divisor = aug[j][j]
        aug[j] = [x/divisor for x in aug[j]]
        for i in range(n):
            if i != j:
                factor = aug[i][j]
                aug[i] = [x-factor*y for x, y in zip(aug[i], aug[j])]
    result = [row[-1] for row in aug]
    assert [sum(x*y for x, y in zip(row, result)) for row in original] == rhs
    return result


def even_ceiling(value):
    # Nonzero shell sizes are even, due to the free involution x -> -x.
    return 2*((value.numerator + 2*value.denominator-1)//(2*value.denominator))


def shell_lower(certificate, constant, label):
    weight = next(F(w) for name, w in certificate if name == label)
    bound = -constant/weight
    return {'shell': label.split(' <=')[0], 'rational_lower_bound': str(bound),
            'even_integer_lower_bound': even_ceiling(bound)}


def census(adj, name):
    """Direct graph counts, not the formulas to be tested."""
    n, k = len(adj), adj[0].bit_count()
    assert all(row.bit_count() == k and not (row >> i & 1) for i, row in enumerate(adj))
    assert all((adj[u] >> v & 1) == (adj[v] >> u & 1) for u, v in combinations(range(n), 2))
    assert all((adj[u] & adj[v]).bit_count() == (1 if adj[u] >> v & 1 else 2)
               for u, v in combinations(range(n), 2))
    edges = [(u, v) for u, v in combinations(range(n), 2) if adj[u] >> v & 1]
    triples = [0]*4
    triangles = []
    for u, v, w in combinations(range(n), 3):
        e = (adj[u] >> v & 1)+(adj[u] >> w & 1)+(adj[v] >> w & 1)
        triples[e] += 1
        if e == 3:
            triangles.append((u, v, w))
    anti_pairs = 0
    for i, (u, v) in enumerate(edges):
        excluded = adj[u] | adj[v] | (1 << u) | (1 << v)
        for x, y in edges[i+1:]:
            if not (excluded >> x & 1 or excluded >> y & 1):
                anti_pairs += 1
    cross_counts = [0]*4
    for i, t in enumerate(triangles):
        mask = sum(1 << v for v in t)
        for s in triangles[i+1:]:
            if any(mask >> v & 1 for v in s):
                continue
            count = sum((adj[v] & mask).bit_count() for v in s)
            assert count <= 3
            cross_counts[count] += 1
    common_non_neighbors = n-2*k+1
    assert triples[3] == n*k//6
    assert triples[2] == n*k*(k-2)//2
    assert triples[1] == len(edges)*common_non_neighbors
    assert 2*anti_pairs == len(edges)*(common_non_neighbors*(k-4)+k-2)//2
    assert 2*cross_counts[1] == 3*len(triangles)*(k-2)*(k-6)//2+6*cross_counts[3]
    return {'name': name, 'vertices': n, 'degree': k, 'triples_by_edge_count': triples,
            'ordered_anticomplete_edge_pairs': 2*anti_pairs,
            'unordered_disjoint_triangle_pairs_by_cross_edges': cross_counts}


def small_graph_check():
    """Exhaust all graphs of order <=6, min degree >=3 and local pair budgets."""
    counts = {}
    for n in range(4, 7):
        pairs = list(combinations(range(n), 2))
        valid = 0
        for mask in range(1 << len(pairs)):
            adj = [0]*n
            for j, (u, v) in enumerate(pairs):
                if mask >> j & 1:
                    adj[u] |= 1 << v
                    adj[v] |= 1 << u
            if any(x.bit_count() < 3 for x in adj):
                continue
            if any((adj[u] & adj[v]).bit_count() > (1 if adj[u] >> v & 1 else 2)
                   for u, v in pairs):
                continue
            assert n == 6 and all(x.bit_count() == 3 for x in adj)
            valid += 1
        counts[n] = valid
    assert counts == {4: 0, 5: 0, 6: 60}
    return counts


def main():
    forms = basis(84)
    assert forms == json.loads((ROOT/'data/codex_theta7_basis_q84.json').read_text())
    peer_path = ROOT/'code/lab_theta_lp_2026-10-08/certificates_N84.json'
    peer = json.loads(peer_path.read_text())
    assert peer['N'] == 84 and len(peer['cases']) == 15
    cases = []
    for case in peer['cases']:
        alpha = case['d']
        assert case['r'] == alpha+1
        assert case['mode'] == ('ext' if alpha <= 26 else 'ext+a7')
        assert alpha in range(2, 31, 2)
        zeros = set() if alpha <= 26 else {7}
        a, b = family(alpha, forms)
        value = verify(case['certificate'], a, b, zeros)
        record = {'r': alpha+1, 'zero_shells': sorted(zeros), 'negative_constant': str(value),
                  'certificate': case['certificate']}
        if zeros:
            record['required_shell_if_zero_removed'] = shell_lower(case['certificate'], value, 'a_7 <= 0')
        cases.append(record)
        print('Verified LAB rank', alpha+1, 'constant', value, flush=True)
    assert [c['r'] for c in cases] == list(range(3, 32, 2))

    supports = {
        33: (18, ['a_9 >= 0', 'a_10 >= 0', 'a_11 >= 0', 'b_3 >= 24948',
                  'b_4 >= 388080', 'a_7 >= b_1', 'a_7 <= 0', 'a_8 <= 0']),
        35: (22, ['a_12 >= 0', 'b_1 >= 0', 'b_3 >= 0', 'b_2 >= 462',
                  'a_7 <= 0', 'a_8 <= 0', 'a_9 <= 0', 'a_10 <= 0']),
        37: (22, ['a_12 >= 0', 'b_1 >= 0', 'b_2 >= 462', 'b_3 >= 24948',
                  'a_7 <= 0', 'a_8 <= 0', 'a_9 <= 0', 'a_10 <= 0']),
        39: (26, ['b_1 >= 0', 'b_2 >= 0', 'a_7 <= 0', 'a_8 <= 0',
                  'a_9 <= 0', 'a_10 <= 0', 'a_11 <= 0', 'a_12 <= 0']),
        41: (26, ['b_1 >= 0', 'b_2 >= 0', 'a_7 <= 0', 'a_8 <= 0',
                  'a_9 <= 0', 'a_10 <= 0', 'a_11 <= 0', 'a_12 <= 0']),
        43: (28, ['a_7 >= 0', 'a_10 >= 0', 'a_11 >= 0', 'a_12 >= 0',
                  'a_14 >= 0', 'a_8 <= 0', 'a_9 <= 0', 'a_13 <= 0']),
    }
    ladder = []
    for rank, (minimum, labels) in supports.items():
        a, b = family(rank-1, forms)
        zeros = set(range(7, minimum//2))
        rows = [constraint(label, a, b, zeros) for label in labels]
        matrix = [[row[j] for row in rows] for j in range(1, 8)]+[[F(1)]*8]
        weights = solve(matrix, [F(0)]*7+[F(1)])
        certificate = [(label, str(w)) for label, w in zip(labels, weights)]
        value = verify(certificate, a, b, zeros)
        record = {'r': rank, 'excluded_minimum': minimum, 'upper_bound_minimum': minimum-2,
                  'zero_shells': sorted(zeros), 'negative_constant': str(value),
                  'certificate': certificate}
        if rank == 33:
            record['required_shell_if_a8_zero_removed_with_a7_zero'] = shell_lower(certificate, value, 'a_8 <= 0')
        ladder.append(record)
        print('Verified ladder rank', rank, 'minimum <=', minimum-2, flush=True)

    # Reject two corruptions, including a nonnegative but incorrect multiplier.
    a, b = family(30, forms)
    good = peer['cases'][-1]['certificate']
    for bad_weight in ['-1', str(F(good[0][1])+1)]:
        bad = [[label, w] for label, w in good]
        bad[0][1] = bad_weight
        try:
            verify(bad, a, b, {7})
        except AssertionError:
            pass
        else:
            raise AssertionError('Corrupted certificate accepted')

    controls = []
    rook = [sum(1 << j for j in range(9) if i != j and (i//3 == j//3 or i%3 == j%3))
            for i in range(9)]
    controls.append(census(rook, 'rook_3x3'))
    for filename in ['bvls243.edges', 'twin243_switched.edges']:
        path = ROOT/'data/srg243'/filename
        adj = [0]*243
        for line in path.read_text().splitlines():
            u, v = map(int, line.split())
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        entry = census(adj, filename)
        entry['normalized_lf_sha256'] = hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        controls.append(entry)
        print('Census control passed:', filename, flush=True)
    target_counts = {'triangles': 231, 'signed_two_paths': 16632,
                     'signed_one_edge_triples': 99792, 'signed_independent_triples': 196812,
                     'ordered_anticomplete_edge_pairs': 253638,
                     'ordered_one_cross_edge_triangle_pairs_lower_bound': 33264}
    assert 2*(comb(99, 3)-231-8316-49896) == target_counts['signed_independent_triples']
    assert 8316+16632 == LOWER[3]
    assert 1386+99792+253638+33264 == LOWER[4]
    report = {'scope': 'Independent exact certificate audit, not formal proof-assistant verification.',
              'basis_sha256': hashlib.sha256(json.dumps(forms, separators=(',', ':')).encode()).hexdigest(),
              'peer_certificate_normalized_lf_sha256': hashlib.sha256(peer_path.read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
              'extended_lower_bounds_b': LOWER, 'target_graph_counts': target_counts,
              'rank_certificates': cases, 'reconstructed_ladder_certificates': ladder,
              'local_min_degree_three_graphs': small_graph_check(), 'graph_census_controls': controls,
              'corrupted_certificates_rejected': 2}
    (ROOT/'data/codex_theta7_certificates_audit.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Verified 15 rank certificates, 6 ladder certificates, 3 graph censuses.')


if __name__ == '__main__':
    main()
