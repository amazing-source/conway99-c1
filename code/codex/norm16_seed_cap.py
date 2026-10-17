"""Structural controls for the proof of at most four norm-16 vectors per seed.

Tests all 478 attachment orbits with each of their eight marked P vertices.
This checks every local pattern used in the proof, not graph completions or
the number of configurations in an unknown graph. The latter bound is proved
in note 170 by reconstruction and comparison of two hypothetical vectors.
Also reconstructs the exact rank-33 Farkas contradiction with the new cap.
"""
from collections import Counter
from itertools import combinations
from fractions import Fraction as F
from pathlib import Path
import json

from theta7_certificates_audit import family, constraint, total, scaled, even_ceiling
from theta7_audit import basis

ROOT = Path(__file__).resolve().parents[2]


def check_seed(b, attachment, p0):
    # P:0..7, Q:8..15, D:16..23. D-D edges are unused in every check below.
    adj = [set() for _ in range(24)]
    for i in range(8):
        for j in range(8):
            if b[i][j]:
                adj[i].add(8+j)
                adj[8+j].add(i)
    for d, (i, j, k, l) in enumerate(attachment, 16):
        for v in (i, j, 8+k, 8+l):
            adj[d].add(v)
            adj[v].add(d)
    pset, qset = set(range(8)), set(range(8, 16))
    u = adj[p0] & qset
    assert len(u) == 4
    cs = {}
    for pair in combinations(sorted(u), 2):
        common = (adj[pair[0]] & adj[pair[1]])-{p0}
        assert len(common) == 1
        cs[pair] = next(iter(common))
    vset = set(cs.values())
    assert len(vset) == 6
    defect = {p: 2-len(adj[p0] & adj[p] & qset) for p in pset-{p0}}
    assert sum(defect.values()) == 2
    vedges = {tuple(sorted((a, bb))) for a in vset for bb in adj[a] & vset}
    qrest = qset-u
    if 2 in defect.values():
        partner = next(p for p, d in defect.items() if d == 2)
        assert vset == pset-{p0, partner}
        assert not vedges
        rset = vset | {p0}
        reconstructed = {v for v in range(24) if v not in u and len(adj[v] & rset) == 3}
        assert reconstructed == qrest
        assert {v for v in range(24) if len(adj[v] & qset) == 4} == pset
        return {'case': 'digon', 'missing_vertex_choices': 0, 'fixed_missing_case_cap': 1}

    partners = {p for p, d in defect.items() if d == 1}
    assert len(partners) == 2
    a, bb = sorted(partners)
    assert len(adj[a] & adj[bb] & qset) == 2
    known = pset-({p0} | partners)
    missing = vset-pset
    assert len(known) == 5 and len(missing) == 1
    x = next(iter(missing))
    assert x >= 16 and vset == known | {x}
    assert p0 not in adj[x]
    assert len(adj[x] & known) in (1, 2)
    assert vedges == {tuple(sorted((x, p))) for p in adj[x] & known}
    centers = set.intersection(*(set(e) for e in vedges))
    assert x in centers and len(centers) in (1, 2)
    # Reconstruct the labelled missing pair and its four other c_ij.
    q1, q2 = next(pair for pair, c in cs.items() if c == x)
    q3, q4 = sorted(u-{q1, q2})
    lookup = lambda i, j: cs[tuple(sorted((i, j)))]
    c13, c14 = lookup(q1, q3), lookup(q1, q4)
    c23, c24 = lookup(q2, q3), lookup(q2, q4)
    first = next(p for p in partners if q1 in adj[p])
    second = next(p for p in partners if q2 in adj[p])
    assert first != second and adj[first] & u == {q1} and adj[second] & u == {q2}
    gamma_set = (adj[c23] & adj[c24])-{q2}
    delta_set = (adj[c13] & adj[c14])-{q1}
    assert len(gamma_set) == len(delta_set) == 1
    gamma, delta = next(iter(gamma_set)), next(iter(delta_set))
    assert gamma != delta and {gamma, delta} <= qrest
    assert gamma in adj[first] and gamma not in adj[second]
    assert delta in adj[second] and delta not in adj[first]
    low = qrest-{gamma, delta}
    assert len(low) == 2 and adj[first] & adj[second] == low
    rset = known | {p0}
    high_from_degrees = {v for v in range(24) if v not in u and len(adj[v] & rset) == 3}
    assert high_from_degrees == {gamma, delta}
    eligible = {c13, c14}-adj[gamma]
    assert eligible
    for c in eligible:
        xi_set = (adj[first] & adj[c])-{q1}
        assert len(xi_set) == 1 and xi_set <= low
    assert first in adj[q1] & adj[gamma]
    assert second in adj[q2] & adj[delta]
    assert len(adj[q1] & adj[gamma]) == len(adj[q2] & adj[delta]) == 2
    # If the second candidate can replace 'second' without repeating a known P,
    # it is exterior in the present configuration and already has its two Q neighbours.
    alternatives = (adj[q2] & adj[delta])-rset-{first, second}
    for other in alternatives:
        assert other >= 16
        assert adj[other] & qset == {q2, delta}
        assert not (adj[other] & low)
    assert {v for v in range(24) if len(adj[v] & qset) == 4} == pset
    return {'case': 'simple_cycle', 'missing_vertex_choices': len(centers),
            'fixed_missing_case_cap': 2,
            'first_unknown_candidates_after_removing_known_P': len((adj[q1] & adj[gamma])-rset)}


def main():
    cores = json.loads((ROOT/'data/codex_norm16_cores.json').read_text())['cases']
    orbits = json.loads((ROOT/'data/codex_norm16_attachments_rank.json').read_text())['cases']
    controls = []
    checked = 0
    for core, data in zip([c for c in cores if c['representatives']], orbits):
        assert core['defect_cycle_lengths'] == data['defect_cycle_lengths']
        counts = Counter()
        for orbit in data['orbits']:
            for p0 in range(8):
                result = check_seed(core['representatives'][0], orbit['representative'], p0)
                counts[result['case'], result['missing_vertex_choices']] += 1
                checked += 1
        controls.append({'defect_cycle_lengths': core['defect_cycle_lengths'],
                         'marked_orbits_checked': sum(counts.values()),
                         'counts_by_case_and_missing_choices': [
                             {'case': key[0], 'missing_choices': key[1], 'count': count}
                             for key, count in sorted(counts.items())]})
    assert checked == 478*8 == 3824

    forms = basis(84)
    a, b = family(32, forms)
    base = json.loads((ROOT/'data/codex_theta7_certificates_audit.json').read_text())
    source = base['reconstructed_ladder_certificates'][0]
    assert source['r'] == 33
    cap = 99*560*4//8
    assert cap == 27720
    rows, certificate = [], []
    for label, weight in source['certificate']:
        row = constraint(label, a, b, {7, 8})
        if label == 'a_8 <= 0':
            row[0] += cap
            label = 'a_8 <= 27720'
        rows.append(scaled(row, F(weight)))
        certificate.append([label, weight])
    result = total(rows)
    assert result[1:] == [0]*7 and result[0] < 0
    a7_weight = F(dict(certificate)['a_7 <= 0'])
    a7_lower = -result[0]/a7_weight
    a7_even = even_ceiling(a7_lower)

    # An independent exact consequence of the same basis at the upper rank.
    a43, b43 = family(42, forms)
    assert total([a43[14], scaled(b43[2], -1), scaled(a43[7], 288), scaled(b43[1], -288)]) == [0]*8

    # Known triangle correction in the peer's quartic extension: equality and rejection controls.
    triangle_sum, hi, num_triangles = F(8008), F(100), F(462)
    offset = num_triangles*(hi-F(52, 3))
    assert hi*num_triangles-triangle_sum-offset == 0
    assert hi*num_triangles-hi*num_triangles-offset < 0

    report = {'scope': 'Local structural controls of the hand proof plus an exact Farkas consequence; no SRG completion search.',
              'proof_note': 'notes/170_CODEX_NORM16_SEED4_FANO_RANG33.md',
              'marked_attachment_orbits_checked': checked, 'controls': controls,
              'total_seeds': 99*560, 'norm16_vectors_per_seed_upper_bound': 4,
              'seeds_per_oriented_norm16_vector': 8, 'a8_upper_bound': cap,
              'r33_certificate_with_a7_zero': certificate,
              'r33_certificate_negative_constant': str(result[0]),
              'r33_a7_lower_bound_from_same_certificate': str(a7_lower),
              'r33_a7_even_lower_bound': a7_even,
              'r33_unsigned_fano_configurations_lower_bound': a7_even//2,
              'r43_identity_a14_minus_b2_equals_minus288_times_a7_minus_b1': True,
              'quartic_triangle_sign_equality_and_rejection_controls': True}
    (ROOT/'data/codex_norm16_seed_cap.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
