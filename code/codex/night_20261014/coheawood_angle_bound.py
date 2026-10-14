"""Exact finite checks for the general co-Heawood angle restriction.

The journal supplies the graph argument excluding coefficients of magnitude
two in integral -4 eigenvectors of norm at most 24. Here we check the small
coefficient parameter cases and exhaust every induced co-Heawood subgraph.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json


def coheawood():
    ns = [0] * 14
    for a in range(1, 8):
        for b in range(1, 8):
            if (a & b).bit_count() % 2:
                ns[a-1] |= 1 << (b+6)
                ns[b+6] |= 1 << (a-1)
    assert all(row.bit_count() == 4 for row in ns)
    for x, y in combinations(range(14), 2):
        assert (ns[x] & ns[y]).bit_count() == (2 if (x < 7) == (y < 7) else 0)
    return ns


def small_coefficient_cases():
    # ||h||^2 >= a^2+7a, where a=max|h|, excludes a>=3.
    assert 3*3 + 7*3 > 24
    # Two +2 entries would require negative mass M>=8+8-2*2=12.
    # But ||h||^2=2(M+t)<=24 with t>=2 gives M<=10.
    assert 16-4 > 12-2
    cases = []
    for positive_twos, negative_twos in [(1, 0), (1, 1)]:
        t = positive_twos + negative_twos
        for mass in range(8, 13-t):
            norm = 2*(mass+t)
            if negative_twos == 0:
                # Once the +2 vertex has no positive neighbor, it meets eight
                # negative ones. Each positive one needs >=2 of the rest.
                outside_negative = mass-8
                positive_ones = mass-2
                if outside_negative < 2:
                    reason = 'not_enough_negative_neighbors_outside_the_plus_two'
                elif outside_negative == 2:
                    assert outside_negative == 2 and positive_ones > 2
                    reason = 'two_negative_vertices_have_more_than_two_common_neighbors'
                else:
                    assert outside_negative == 3 and positive_ones == 9
                    assert positive_ones > 2*3
                    reason = 'nine_positive_vertices_exceed_six_available_negative_pairs'
            else:
                # The +/-2 vertices must be adjacent. Six positive ones meet
                # the -2 vertex, and each needs an additional negative one
                # outside the six negative-one neighbors of +2.
                outside_negative = mass-8
                if outside_negative == 0:
                    reason = 'positive_one_cannot_have_weighted_negative_degree_four'
                elif outside_negative == 1:
                    assert outside_negative == 1
                    reason = 'minus_two_and_remaining_negative_one_have_six_common_neighbors'
                else:
                    assert mass == 10
                    assert 8 > 7 and 6 > 2*2
                    reason = ('nonadjacent_twos_require_eight_independent_neighbors; '
                              'adjacent_twos_require_six_edges_where_only_four_are_available')
            cases.append(dict(positive_twos=positive_twos, negative_twos=negative_twos,
                              mass=mass, squared_norm=norm, reason=reason))
    assert len(cases) == 7
    return cases


def main():
    ns = coheawood()
    histogram = Counter()
    complements = {}
    for selected in range(1, 1 << 14):
        if all((ns[x] & selected).bit_count() >= 3
               for x in range(14) if selected >> x & 1):
            size = selected.bit_count()
            histogram[size] += 1
            if size == 10:
                complement = ((1 << 14)-1) ^ selected
                degrees = sorted((ns[x] & complement).bit_count()
                                 for x in range(14) if complement >> x & 1)
                assert degrees == [2, 2, 2, 2]
                assert (complement & 127).bit_count() == 2
                complements[complement] = degrees
            elif size == 12:
                complement = ((1 << 14)-1) ^ selected
                assert (complement & 127).bit_count() == 1
    assert dict(histogram) == {10: 21, 12: 49, 13: 14, 14: 1}
    excluded = [dot for dot in range(3, 8) if histogram[14-dot] == 0]
    assert excluded == [3, 5, 6, 7]
    report = dict(coefficient_bound=dict(max_norm=24, max_abs_entry=1,
                                        rejected_twos=small_coefficient_cases()),
                  induced_minimum_degree_three=dict(sorted(histogram.items())),
                  subsets_checked=(1 << 14)-1,
                  excluded_absolute_inner_products=excluded,
                  possible_absolute_inner_products=[0, 1, 2, 4],
                  absolute_inner_product_four_requires='aligned induced four-cycle intersection',
                  absolute_inner_product_two_requires='aligned two-vertex intersection of opposite signs',
                  sign_subgraph_edge_bounds={p: min(p*(p-7)//9,
                                                    (p*p-19*p+99)//5) for p in range(7, 13)},
                  sign_subgraph_constraint='9*e + sum_v binom(d_same_sign(v),2) <= p*(p-7)',
                  outside_incidence_constraint='5*e + W <= p*p-19*p+99',
                  outside_incidence_identity='sum_outside (a-1)*(a-2)/2 = p*p-19*p+99-5*e-W',
                  norm24_three_edges_case=dict(each_sign_graph='three disjoint edges',
                                                outside_degree_one_in_each_sign=42,
                                                outside_degree_two_in_each_sign=33),
                  sign_subgraphs_triangle_free=True,
                  four_cycle_complements=sorted(complements))
    out = Path(__file__).resolve().parents[3] / 'data' / 'codex_night_20261014'
    (out / 'coheawood_angle_bound.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
