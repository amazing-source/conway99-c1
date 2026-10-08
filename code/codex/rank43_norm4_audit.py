"""Exact rank-43 identities, root counting, and fractional norm-28 profiles.

This script uses Codex's eta basis and rational arithmetic. The geometric
arguments behind the root bounds and profile reductions are in note 191.
No optimisation solver or LAB module is imported.
"""
from fractions import Fraction as F
from itertools import product
import json

from theta7_audit import basis
from theta7_certificates_audit import ROOT, family, solve


def affine_change():
    a, b = family(42, basis(84))
    equations = a[7:13]+[[x-y for x, y in zip(b[1], a[7])]]
    matrix = [row[1:] for row in equations]
    columns = []
    for column in range(7):
        rhs = [-row[0] if column == 0 else F(i == column-1) for i, row in enumerate(equations)]
        columns.append(solve(matrix, rhs))
    def transform(row):
        return [row[0]+sum(x*y for x, y in zip(row[1:], columns[0]))]+[
            sum(x*y for x, y in zip(row[1:], columns[j])) for j in range(1, 7)]
    aa, bb = list(map(transform, a)), list(map(transform, b))
    expected = {
        'a13': [2632, 56, -2, -16, 7, 2, 1],
        'a15': [74704, 1064, -196, 86, 22, 13, -6],
        'b2': [1000, -8, 25, 11, 8, 3, 1],
        'b3': [10648712, 19388, 5150, 1237, 31, -68, -39],
        'b4': [4464109880, 275744, -14374, -24188, -3996, 388, 701],
    }
    for name, values in expected.items():
        assert (aa if name[0] == 'a' else bb)[int(name[1:])] == list(map(F, values)), name
    assert all(aa[7*k] == bb[k] for k in range(1, 13))
    assert all(row[0] >= 0 and row[0].denominator == 1 for row in aa+bb)
    assert all(row[0] % 2 == 0 for row in aa[1:]+bb[1:])
    return {'coordinates': ['1']+[f'a{i}' for i in range(7, 13)],
            'identities': expected, 'a7k_equals_bk_checked_through_k': 12,
            'origin_nonnegative_even_coefficients_checked_through_q': 84,
            'origin': {'a13': int(aa[13][0]), 'a14': int(aa[14][0]),
                       'a15': int(aa[15][0]), 'b2': int(bb[2][0]),
                       'b3': int(bb[3][0]), 'b4': int(bb[4][0])}}


def roots():
    # P4 = (3I-A)/7+J/63; Bessel for e_u+e_v on an edge.
    diagonal, edge = F(4, 9), -F(8, 63)
    bessel = 14*(2*diagonal+2*edge)
    assert bessel == F(80, 9)
    per_edge = bessel.numerator//bessel.denominator
    per_root_line = (14-4)*14
    kmax = (99*14//2)*per_edge//per_root_line
    assert (per_edge, per_root_line, kmax) == (8, 140, 39)
    # For each root line: 42 triangles have nonzero inner product,
    # hence 84 additional signed reflected triangle vectors.
    assert 3*14 == 42
    bounds = []
    for k in range(kmax+1):
        reflected = 84*k
        root_pairs = 4*(k*(k-1)//2)
        geometric = 462+reflected+root_pairs
        theta = 1000-16*k
        bounds.append({'root_lines': k, 'b1': 2*k, 'reflected_triangles': reflected,
                       'root_pair_vectors': root_pairs, 'b2_lower': max(geometric, theta)})
    assert min(r['b2_lower'] for r in bounds) == 922
    assert [r['root_lines'] for r in bounds if r['b2_lower'] == 922] == [5]
    return {'edge_Bessel_bound': str(bessel), 'integer_bound_per_edge': per_edge,
            'edge_sum_per_root_line': per_root_line, 'root_lines_at_most': kmax,
            'b1_at_most': 2*kmax, 'all_ranks_b2_lower': '462 + 41*b1 + b1^2/2',
            'rank43_b2_at_least': 922, 'rank43_nontriangle_norm4_at_least': 460,
            'by_number_of_root_lines': bounds}


def fractional_profiles():
    values = (-2, -1, 2, 3)
    profiles = []
    for counts in product(range(4), repeat=4):
        if sum(n*v*(v-1) for v, n in zip(values, counts)) != 6:
            continue
        n1 = 33-sum(v*n for v, n in zip(values, counts))
        n0 = 99-n1-sum(counts)
        if min(n1, n0) < 0:
            continue
        histogram = {v: n for v, n in zip(values, counts) if n}
        histogram.update({0: n0, 1: n1})
        coords = [v for v, n in histogram.items() for _ in range(n)]
        assert len(coords) == 99 and sum(coords) == 33 and sum(v*v for v in coords) == 39
        failures = []
        for value in histogram:
            other = list(coords)
            other.remove(value)
            other.sort()
            low, high, need = sum(other[:14]), sum(other[-14:]), 6-4*value
            if not low <= need <= high:
                failures.append({'coordinate': value, 'needed_neighbour_sum': need,
                                 'possible_interval': [low, high]})
        profiles.append({'histogram': {str(v): n for v, n in sorted(histogram.items())},
                         'excluded_by_neighbour_sum': bool(failures), 'contradictions': failures})
    surviving = [r for r in profiles if not r['excluded_by_neighbour_sum']]
    assert len(profiles) == 6 and len(surviving) == 3
    assert {tuple(sorted((int(v), n) for v, n in r['histogram'].items())) for r in surviving} == {
        ((-1, 3), (0, 60), (1, 36)),
        ((-1, 2), (0, 63), (1, 33), (2, 1)),
        ((-2, 1), (0, 63), (1, 35)),
    }
    edge_tables = {
        'three_negative_singletons': [
            {'eZ': e, 'SZ': 30+2*e, 'SS': 51+e, 'ZO': 12-4*e,
             'SO': 372-4*e, 'OO': 228+4*e} for e in range(4)],
        'one_positive_doubleton': [
            {'eZ': e, 'vS': 0, 'vZ': 2, 'vO': 12, 'SZ': 16+2*e,
             'SS': 41+e, 'ZO': 10-4*e, 'SO': 364-4*e, 'OO': 248+4*e} for e in range(2)],
        'one_negative_doubleton': {'vS': 14, 'SS': 49, 'SO': 378, 'OO': 252},
    }
    for row in edge_tables['three_negative_singletons']:
        assert 2*row['SS']+row['SZ']+row['SO'] == 36*14
        assert 2*row['eZ']+row['SZ']+row['ZO'] == 3*14
        assert 2*row['OO']+row['SO']+row['ZO'] == 60*14
    for row in edge_tables['one_positive_doubleton']:
        assert 2*row['SS']+row['SZ']+row['SO'] == 33*14
        assert 2*row['eZ']+row['SZ']+row['ZO']+row['vZ'] == 2*14
        assert 2*row['OO']+row['SO']+row['ZO']+row['vO'] == 63*14
    # Equitable partition forced by a negative doubleton: v,A,B,O.
    q = [[0, 14, 0, 0], [1, 1, 3, 9], [0, 2, 0, 12], [0, 2, 4, 8]]
    sizes = [1, 14, 21, 63]
    for i, j in product(range(4), repeat=2):
        assert sizes[i]*q[i][j] == sizes[j]*q[j][i]
    assert all(sum(row) == 14 for row in q)
    for i, j in product(range(4), repeat=2):
        # A^2 = 12 I - A + 2 J, also on the equitable quotient.
        assert sum(q[i][k]*q[k][j] for k in range(4)) == 12*(i == j)-q[i][j]+2*sizes[j]
    return {'six_arithmetic_profiles': profiles, 'surviving_profiles': 3,
            'partition_edge_counts': edge_tables,
            'negative_doubleton_equitable_partition': {'sizes': sizes, 'quotient': q},
            'scope': 'Necessary profiles and local structure only; no existence or exclusion of the surviving shapes.'}


def main():
    report = {'theta': affine_change(), 'roots': roots(), 'fractional_norm28': fractional_profiles(),
              'scope': 'Exact identities and arithmetic checks supporting note 191; rank 43 remains open.'}
    path = ROOT/'data/codex_rank43_norm4_audit.json'
    path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Verified five rank-43 identities; a7k=bk through k=12; origin coefficients through q^84.')
    print('Bessel bound: b1 <= 78. Root reflections plus root sums: rank43 b2 >= 922, including >=460 nontriangle vectors.')
    print('Fractional norm28: six arithmetic profiles, three eliminated by neighbour sums, three remain.')


if __name__ == '__main__':
    main()
