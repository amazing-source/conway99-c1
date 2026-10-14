"""Exact checks for small integral (-4)-eigenvectors in an SRG(99,14,1,2).

The proof is in the current night journal. This checks its small finite
ingredients and its polynomial identities; it does not construct an SRG.
No external packages or old result files are read.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json


def coheawood():
    # Complement of the point-line incidence matrix of the Fano plane.
    b = [[(x & y).bit_count() % 2 for y in range(1, 8)]
         for x in range(1, 8)]
    assert all(sum(row) == 4 for row in b)
    assert all(sum(b[i][k] * b[j][k] for k in range(7)) == 2
               for i, j in combinations(range(7), 2))
    # The transpose has the same property (this construction is symmetric).
    assert all(b[i][j] == b[j][i] for i in range(7) for j in range(7))
    return b


def balanced_independent_intersections(b):
    counts = {}
    for size in range(1, 8):
        counts[size] = sum(
            all(not b[i][j] for i in left for j in right)
            for left in combinations(range(7), size)
            for right in combinations(range(7), size))
    assert counts[1] == 21 and all(counts[k] == 0 for k in range(2, 8))
    return counts


def add(*terms):
    out = {}
    for term in terms:
        for key, value in term.items():
            out[key] = out.get(key, 0) + value
    return {key: value for key, value in out.items() if value}


def scale(n, term):
    return {key: n * value for key, value in term.items() if n * value}


def projector_identity():
    # Basis I,A,J,R, where R=F F^t and columns of F are pairwise
    # orthogonal integer eigenvectors with squared norm 14.
    products = {
        ('A', 'A'): {'I': 12, 'A': -1, 'J': 2},
        ('A', 'J'): {'J': 14},
        ('A', 'R'): {'R': -4},
        ('J', 'J'): {'J': 99},
        ('J', 'R'): {},
        ('R', 'R'): {'R': 14},
    }
    def multiply(left, right):
        out = {}
        for a, x in left.items():
            for b, y in right.items():
                term = {b: 1} if a == 'I' else ({a: 1} if b == 'I'
                                                       else products[tuple(sorted((a, b)))])
                out = add(out, scale(x * y, term))
        return out

    t = {'A': 2, 'I': -6, 'R': 1}
    assert multiply(t, t) == add({'J': 8}, scale(-14, t))
    p = {'I': Fraction(3, 7), 'A': Fraction(-1, 7), 'J': Fraction(1, 63)}
    assert multiply(p, p) == p
    q = add(p, {'R': Fraction(-1, 14)})
    assert multiply(q, q) == q
    assert add({'J': Fraction(2, 9)}, scale(-14, q)) == t
    # The fixed diagonal of P is 3/7+1/63=4/9.
    assert p['I'] + p['J'] == Fraction(4, 9)
    local = []
    for k in range(7):
        row_sum = 22
        diagonal = k - 6
        squared_row_sum = 92 - 14 * k
        slack = squared_row_sum - row_sum - diagonal * (diagonal - 1)
        assert slack == 28 - k * (k + 1)
        local.append(dict(root_supports_at_vertex=k,
                          off_diagonal_sum_t_times_t_minus_one=slack,
                          possible_by_nonnegativity=slack >= 0))
    assert [r['root_supports_at_vertex'] for r in local
            if r['possible_by_nonnegativity']] == list(range(5))
    return local


def minimum_norm_checks():
    # For norm <=14, norm>=8*max|f_v| forces entries 0,+1,-1.
    # There are p entries of each sign; count positive pairs through negatives.
    candidates = []
    for p in range(1, 8):
        required = 6 * p
        available = p * (p - 1)
        candidates.append(dict(positive_support=p, negative_support=p,
                               required_pair_incidences=required,
                               available_pair_incidences=available,
                               possible=required <= available))
    assert [c['positive_support'] for c in candidates if c['possible']] == [7]
    # At equality, the complement incidence 7x7 is the Fano plane.
    return candidates


def no_angle_one_checks():
    # If f.g=7, then f-g is another norm-14 eigenvector. Its support
    # difference J has 7 vertices, is bipartite, and has minimum degree 3.
    # Both parts therefore have >=3 vertices, hence sizes 3 and 4.
    possible_part_sizes = [(a, 7-a) for a in range(8) if min(a, 7-a) >= 3]
    assert possible_part_sizes == [(3, 4), (4, 3)]
    # Every vertex in the part of size 4 must meet all 3 in the other part:
    # two vertices in the part of size 4 then have >=3 common neighbors.
    for a, b in possible_part_sizes:
        assert min(a, b) == 3 > 2
    return dict(part_sizes=possible_part_sizes, forced_subgraph='K_3,4',
                forbidden_common_neighbors=3)


def check():
    b = coheawood()
    return dict(
        status='exact finite ingredients and formal identities checked',
        minimum_norm=minimum_norm_checks(),
        norm14_support='7 positive and 7 negative entries; induced co-Heawood',
        forbidden_inner_products=no_angle_one_checks(),
        distinct_nonopposite_norm14_inner_products='integers from -6 to 6',
        local_orthogonal_family_bound=projector_identity(),
        maximum_orthogonal_coheawood_sign_vectors_up_to_sign=99 * 4 // 14,
        integral_lattice=dict(
            definition='(7 P c)/sqrt(7), c integral and sum(c) divisible by 9',
            root_system='A_1^r with r<=28', maximum_roots_including_both_signs=56,
            warning='The integral-preimage condition is needed for mutual orthogonality; arbitrary co-Heawood vectors need not have inner product divisible by 7'),
        balanced_independent_subsets_of_coheawood=balanced_independent_intersections(b),
        scope='Structural obstruction and lattice bound, not exclusion of C1 or of a single co-Heawood')


if __name__ == '__main__':
    report = check()
    Path('data/codex_night_20261014/integral_root_obstructions.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: report[key] for key in (
        'status', 'distinct_nonopposite_norm14_inner_products',
        'maximum_orthogonal_coheawood_sign_vectors_up_to_sign',
        'integral_lattice', 'scope')}, indent=2))
