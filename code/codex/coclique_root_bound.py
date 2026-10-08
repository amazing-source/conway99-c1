"""Exact arithmetic supporting the coclique/centre proof in note 192.

The structural proof is in the note. In particular this verifier does not
assume that an SRG or a 22-coclique exists, nor construct either one.
"""
from fractions import Fraction as F
from itertools import product
import json

from theta7_certificates_audit import ROOT


def main():
    # Equality in the coclique moment bound forces all 77 outside degrees to 4.
    c, outside = 22, 77
    first, second = 14*c, 2*c*(c-1)+14*c
    assert (first, second) == (308, 1232)
    assert outside*second == first*first
    p_norm = F(c)-F(c*c, 99)
    p_pair = F(15)-F(c*c, 99)
    assert p_norm == F(154, 9) and p_pair == F(91, 9)
    # x_Rv = p_R - 7 P4 e_v, v in R.
    norm = p_norm+49*F(4, 9)-14*F(7, 9)
    assert norm == 28
    entries = {'v': F(7, 9)-7*F(4, 9),
               'N(v)': -F(2, 9)+7*F(8, 63),
               'R-v': F(7, 9)-7*F(1, 63),
               'others': -F(2, 9)-7*F(1, 63)}
    assert entries == {'v': -F(7, 3), 'N(v)': F(2, 3),
                       'R-v': F(2, 3), 'others': -F(1, 3)}
    # h_i=p_Ri+p_Si. Equal cross-intersections t give an even off-diagonal.
    diagonal = F(9, 2)*(2*p_norm+2*p_pair)
    assert diagonal == 245 and int(diagonal) % 2 == 1
    off_diagonal = {}
    for t in range(23):
        value = F(9, 2)*4*(F(t)-F(44, 9))
        assert value == 18*t-88 and value.denominator == 1 and value % 2 == 0
        off_diagonal[t] = int(value)
    # Thus the scaled Gram matrix is I modulo 2, for every size and pattern.
    root_lines_at_most = 44//2
    assert root_lines_at_most == 22
    # Integer neighbour sums at a triangle of a Fano: a nonzero sum is
    # represented by exactly one supported vertex with that same sign.
    reflection_entries = set()
    for values in product((-1, 0, 1), repeat=3):
        if values.count(-1) > 1 or values.count(1) > 1 or abs(sum(values)) != 1:
            continue
        epsilon = sum(values)
        reflection_entries.update(F(4, 3)-epsilon*v for v in values)
    reflection_entries.update(base-value for base, value in product((-F(2, 3), F(1, 3)), (-1, 0, 1)))
    assert max(map(abs, reflection_entries)) == F(5, 3) < F(7, 3)
    lower_by_k = []
    for k in range(root_lines_at_most+1):
        geometric = 462+84*k+2*k*(k-1)+88*k
        theta = 1000-16*k
        lower_by_k.append({'root_lines': k, 'b1': 2*k,
                           'distinct_22_cocliques_at_least': 2*k,
                           'profile_C_norm4_vectors_at_least': 88*k,
                           'b2_geometric_lower': geometric, 'b2_lower': max(theta, geometric)})
    assert min(row['b2_lower'] for row in lower_by_k) == 968
    assert [row['root_lines'] for row in lower_by_k if row['b2_lower'] == 968] == [2]
    # At rank43, 7 divides (x_Rv,x_Sw). All three vertex relations give t-1 mod7.
    intersections = []
    for t in range(23):
        for relation in ('equal', 'adjacent', 'nonadjacent'):
            pv_pw = {'equal': F(4, 9), 'adjacent': -F(8, 63), 'nonadjacent': F(1, 63)}[relation]
            value_without_memberships = F(t)-F(44, 9)+F(28, 9)+49*pv_pw
            assert value_without_memberships.denominator == 1
            assert (value_without_memberships-(t-1)) % 7 == 0
        if t % 7 == 1:
            intersections.append(t)
    assert intersections == [1, 8, 15, 22]
    report = {'coclique_size': c, 'outside_degree': first//outside,
              'profile_C_vectors_per_coclique_in_L1': 44,
              'profile_C_coordinates': {key: str(value) for key, value in entries.items()},
              'centre_Gram_scaled_by': '9/2', 'centre_Gram_diagonal': int(diagonal),
              'centre_Gram_off_diagonal_by_intersection': off_diagonal,
              'centre_Gram_mod2': 'identity; therefore nonsingular over Q and R',
              'all_ranks_b1_upper_bound': 44,
              'rank43_b2_lower_bound': 968,
              'rank43_nontriangle_norm4_lower_bound': 506,
              'rank43_b2_geometric_lower': '462 + 85*b1 + b1^2/2',
              'rank43_distinct_coclique_intersections': intersections[:-1],
              'by_root_lines': lower_by_k,
              'scope': 'Arithmetic checks for the hand proof in note 192. No exclusion of the graph or of any remaining rank.'}
    (ROOT/'data/codex_coclique_root_bound.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Verified centre Gram parity: b1 <= 44 at every rank.')
    print('Rank43: b2 >= 968; at least 506 nontriangle norm4 vectors.')
    print('Rank43 coclique intersections:', intersections[:-1])


if __name__ == '__main__':
    main()
