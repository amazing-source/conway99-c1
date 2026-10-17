"""Independent audit: cycle/paw dual vectors, r>=35, and r35 minimum<=18.

The verifier imports only our own modular-form implementation. It admits no
unaudited higher dual bounds or root-system cap. Two of the seven peer
certificates require such higher bounds and are explicitly not used here.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json

from theta7_audit import basis
from theta7_certificates_audit import family, constraint, total, scaled

ROOT = Path(__file__).resolve().parents[2]
NEW_B4 = 1431738


def count_controls(adj, name):
    n, k = len(adj), adj[0].bit_count()
    assert all(row.bit_count() == k and not row >> i & 1 for i, row in enumerate(adj))
    cycles, triangles = set(), set()
    for u, v in combinations(range(n), 2):
        assert (adj[u] >> v & 1) == (adj[v] >> u & 1)
        common = adj[u] & adj[v]
        if adj[u] >> v & 1:
            assert common.bit_count() == 1
            w = common.bit_length()-1
            triangles.add(tuple(sorted((u, v, w))))
        else:
            assert common.bit_count() == 2
            cycles.add(common | (1 << u) | (1 << v))
    paws = set()
    for triangle in triangles:
        mask = sum(1 << v for v in triangle)
        for v in triangle:
            outside = adj[v] & ~mask
            while outside:
                bit = outside & -outside
                outside -= bit
                assert (adj[bit.bit_length()-1] & mask).bit_count() == 1
                paws.add(mask | bit)
    assert not (paws & cycles)

    def audit_shapes(masks, kind):
        far_counts, external_degree_histograms = Counter(), Counter()
        for mask in masks:
            vertices = [i for i in range(n) if mask >> i & 1]
            assert len(vertices) == 4
            degrees = sorted((adj[i] & mask).bit_count() for i in vertices)
            assert degrees == ([2]*4 if kind == 'cycle' else [1, 2, 2, 3])
            assert sum(degrees) == 8
            touched = mask
            for i in vertices:
                touched |= adj[i]
            far = n-touched.bit_count()
            far_counts[far] += 1
            # Direct external degree census, to test the incidence arguments as well.
            hist = [0]*5
            for j in range(n):
                if not (mask >> j & 1):
                    hist[(adj[j] & mask).bit_count()] += 1
            external_degree_histograms[tuple(hist)] += 1
        expected_far = n-4*k+(8 if kind == 'cycle' else 7)
        assert far_counts == {expected_far: len(masks)}
        return {'subgraphs': len(masks), 'far_vertices_per_subgraph': expected_far,
                'signed_representatives': 2*len(masks)*expected_far,
                'external_degree_histograms': [
                    {'counts_by_degree_0_to_4': hist, 'subgraphs': count}
                    for hist, count in sorted(external_degree_histograms.items())]}

    assert len(cycles) == n*(n-1-k)//4
    assert len(paws) == n*k*(k-2)//2
    return {'graph': name, 'vertices': n, 'degree': k,
            'cycles': audit_shapes(cycles, 'cycle'), 'paws': audit_shapes(paws, 'paw')}


def audited_row(label, a, b, zeros):
    if label == 'b_4 >= 1431738':
        row = list(b[4])
        row[0] -= NEW_B4
        return row
    if label in ('a_7 <= 7920', 'a_8 <= 27720'):
        n, cap = (7, 7920) if label.startswith('a_7') else (8, 27720)
        row = scaled(a[n], -1)
        row[0] += cap
        return row
    return constraint(label, a, b, zeros)


def main():
    forms = basis(84)
    assert forms == json.loads((ROOT/'data/codex_theta7_basis_q84.json').read_text())
    path = ROOT/'code/lab_theta_lp_2026-10-08/certificates2_N84.json'
    peer = json.loads(path.read_text())
    assert peer['N'] == 84 and len(peer['cases']) == 7
    used, excluded = [], []
    # These two exact certificates use higher b5/b6 bounds not needed by this audit.
    unreviewed_labels = {'b_5 >= 3415104', 'b_6 >= 10844064', 'b_5 >= 17668728'}
    for case in peer['cases']:
        unsupported = [label for label, _ in case['certificate'] if label in unreviewed_labels]
        if unsupported:
            excluded.append({'mode': case['mode'], 'r': case['r'],
                             'reason': 'Higher dual counts outside this audit',
                             'unreviewed_constraints': unsupported})
            continue
        assert case['r'] == case['d']+1
        a, b = family(case['d'], forms)
        zeros = {7, 8, 9} if case['r'] == 35 else set()
        rows = [audited_row(label, a, b, zeros) for label, _ in case['certificate']]
        weights = [F(weight) for _, weight in case['certificate']]
        assert all(weight > 0 for weight in weights)
        result = total([scaled(row, weight) for row, weight in zip(rows, weights)])
        assert result[1:] == [0]*7 and result[0] < 0
        entry = {'mode': case['mode'], 'r': case['r'], 'zero_shells': sorted(zeros),
                 'negative_constant': str(result[0]), 'certificate': case['certificate']}
        used.append(entry)
        print('Verified', case['mode'], 'r', case['r'], 'constant', result[0], flush=True)
    assert sorted(c['r'] for c in used) == [29, 29, 31, 33, 35]
    assert len(excluded) == 2

    controls = []
    rook = [sum(1 << j for j in range(9) if i != j and (i//3 == j//3 or i%3 == j%3))
            for i in range(9)]
    controls.append(count_controls(rook, 'rook_3x3'))
    for filename in ('bvls243.edges', 'twin243_switched.edges'):
        source = ROOT/'data/srg243'/filename
        adj = [0]*243
        for line in source.read_text().splitlines():
            u, v = map(int, line.split())
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        entry = count_controls(adj, filename)
        entry['normalized_lf_sha256'] = hashlib.sha256(source.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        controls.append(entry)
        print('Graph controls passed', filename, flush=True)

    counts99 = {'induced_four_cycles': 2079, 'far_vertices_per_cycle': 51,
                'signed_cycle_minus_far_vertex': 2079*51*2,
                'induced_paws': 8316, 'far_vertices_per_paw': 50,
                'signed_paw_minus_far_vertex': 8316*50*2,
                'old_b4_lower_bound': 388080, 'new_b4_lower_bound': NEW_B4}
    assert 388080+counts99['signed_cycle_minus_far_vertex']+counts99['signed_paw_minus_far_vertex'] == NEW_B4
    report = {'scope': 'Independent exact audit of two new norm8 dual families and selected certificates; no higher dual shell counts assumed.',
              'counts_for_99': counts99, 'verified_certificates': used,
              'unused_peer_certificates': excluded, 'graph_controls': controls,
              'basis_sha256': hashlib.sha256(json.dumps(forms, separators=(',', ':')).encode()).hexdigest(),
              'peer_certificate_normalized_lf_sha256': hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
              'global_rank7_lower_bound_combining_previous_certificates': 35,
              'remaining_ranks': [35, 37, 39, 41, 43],
              'minimum_L1_upper_bound_by_rank': {35: 18, 37: 20, 39: 24, 41: 24, 43: 26}}
    (ROOT/'data/codex_dual_paw_cycle_rank35.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Verified r>=35; r35 implies min(L1)<=18. Two higher-bound certificates not used.')


if __name__ == '__main__':
    main()
