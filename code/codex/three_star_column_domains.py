"""Exact necessary column domains beyond a Conway three-star object.

Input: the induced adjacency Gamma on the 34 far labels meeting {0,1,2},
where star mates are i^1. This does NOT construct the object or a full SRG.
The remaining 50 labels are fixed, not interchangeable anonymous columns.
All arithmetic used for rejection is integral/rational. No group audit.
"""
import argparse
from collections import defaultdict
from itertools import combinations
from math import comb, gcd, lcm
from pathlib import Path
import json
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_ambient_upper import analyse as analyse_ambient_upper


CENTRES = (0, 1, 2)
FAR = tuple(p for p in combinations(range(14), 2) if (p[0] ^ 1) != p[1])
S = tuple(p for p in FAR if set(p).intersection(CENTRES))
U = tuple(p for p in FAR if not set(p).intersection(CENTRES))
INDEX = {p: i for i, p in enumerate(S)}
P, PP = INDEX[(0, 2)], INDEX[(1, 2)]
GROUPS = (
    tuple(i for i, p in enumerate(S) if 0 in p and i != P),
    tuple(i for i, p in enumerate(S) if 1 in p and i != PP),
    tuple(i for i, p in enumerate(S) if 2 in p and i not in (P, PP)),
)
STAR_MASKS = tuple(sum(1 << i for i, p in enumerate(S) if c in p)
                   for c in range(14))


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def k8(a, b):
    return 3 * len(set(a).intersection(b)) + sum((c ^ 1) in b for c in a) - 2


def raw_bound(delta):
    return sum(comb(11, 2-z) * comb(11, 2-zp) * comb(10, r)
               for z in (0, 1) for zp in (0, 1)
               if 0 <= (r := 2-delta-z-zp) <= 10)


def primitive(vector):
    den = lcm(*(int(v.q) for v in vector))
    out = [int(v * den) for v in vector]
    common = gcd(*out)
    out = [v // common for v in out]
    if next(v for v in out if v) < 0:
        out = [-v for v in out]
    return tuple(out)


class ProfileJoin:
    """Meet-in-the-middle for the exact three-star sums and kernel equations."""
    def __init__(self, kernels):
        self.kernels = kernels
        self.width = len(kernels)
        self.groups = []
        for group in GROUPS:
            entries = {}
            for size in range(3):
                entries[size] = [
                    (sum(1 << i for i in subset),
                     tuple(sum(v[i] for i in subset) for v in kernels))
                    for subset in combinations(group, size)
                ]
            self.groups.append(entries)
        self.left = {}
        for z in (0, 1):
            for zp in (0, 1):
                bucket = defaultdict(list)
                base = (z << P) | (zp << PP)
                offset = tuple(z*v[P] + zp*v[PP] for v in kernels)
                for m, w in self.groups[0][2-z]:
                    for mp, wp in self.groups[1][2-zp]:
                        key = tuple(a+b+c for a, b, c in zip(w, wp, offset))
                        bucket[key].append(base | m | mp)
                self.left[z, zp] = bucket

    def profiles(self, delta, rhs):
        for z in (0, 1):
            for zp in (0, 1):
                size = 2-delta-z-zp
                if size < 0:
                    continue
                bucket = self.left[z, zp]
                for m, w in self.groups[2][size]:
                    key = tuple(a-b for a, b in zip(rhs, w))
                    for left in bucket.get(key, ()):
                        yield left | m


def load_gamma(path):
    data = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    labels = tuple(tuple(sorted(p)) for p in data.get('labels', S))
    matrix = data.get('gamma', data.get('adjacency'))
    if matrix is None or len(labels) != 34 or set(labels) != set(S):
        raise ValueError('Expected gamma/adjacency and the 34 labels meeting {0,1,2}.')
    if len(matrix) != 34 or any(len(row) != 34 for row in matrix):
        raise ValueError('Gamma must be 34 by 34.')
    if any(x not in (0, 1) for row in matrix for x in row):
        raise ValueError('Gamma must be binary.')
    old = {p: i for i, p in enumerate(labels)}
    gamma = [[int(matrix[old[p]][old[q]]) for q in S] for p in S]
    if any(gamma[i][i] or any(gamma[i][j] != gamma[j][i] for j in range(34))
           for i in range(34)):
        raise ValueError('Gamma must be symmetric with zero diagonal.')
    return gamma


def boundary_degree_statistics(gamma):
    epsilon = gamma[P][PP]
    double = 1-epsilon-sum(a*b for a, b in zip(gamma[P], gamma[PP]))
    bp_inside = (INDEX[(0, 3)], INDEX[(1, 3)])
    bp_double_degree = 2-sum(gamma[i][j] for i in (P, PP) for j in bp_inside)
    if double not in (0, 1) or bp_double_degree not in (0, 1, 2):
        raise ValueError('The two overlap labels violate a common-neighbour budget.')
    n8 = double+bp_double_degree
    n7 = 28+2*epsilon-2*n8
    n6 = 50-n7-n8
    return dict(overlap_edge=epsilon, common_outside_neighbours=double,
                degree8_labels_containing_3=bp_double_degree,
                degree_counts={6:n6, 7:n7, 8:n8},
                far_induced_edges=68+epsilon, boundary_edges=157+epsilon,
                cross_edges=372-2*epsilon, remaining_induced_edges=164+epsilon,
                degree8_position_upper_bound=(40 if double else 1)*comb(10, bp_double_degree))


def prepare(gamma, producer_certified_grid_rank30=False, producer_closed_pairs=None):
    producer_certified = producer_certified_grid_rank30 or producer_closed_pairs is not None
    # Full induced 49 by 49 boundary: root, its 14 neighbours, then S.
    boundary = [[0]*49 for _ in range(49)]
    for c in range(14):
        boundary[0][1+c] = boundary[1+c][0] = 1
        boundary[1+c][1+(c ^ 1)] = 1
    for i, label in enumerate(S):
        for c in label:
            boundary[15+i][1+c] = boundary[1+c][15+i] = 1
        for j in range(34):
            boundary[15+i][15+j] = gamma[i][j]
    B = sp.Matrix(boundary)
    residual = 12*sp.eye(49) + 2*sp.ones(49) - B - B*B
    if any(x < 0 for x in residual):
        raise ValueError('Boundary exceeds a degree or common-neighbour cap.')
    for centre in (0, 1, 2, 3):  # root and star letters 0,1,2
        if sum(boundary[centre]) != 14 or any(residual[centre, j] for j in range(49)):
            raise ValueError('The four closed neighbourhoods are not complete/consistent.')
    statistics = boundary_degree_statistics(gamma)
    M = sp.Matrix(34, 34, lambda i, j:
                  24*(i == j) - 8*gamma[i][j] - k8(S[i], S[j]))
    if producer_certified:
        # This path consumes the producer's rank and BOTH Gram certifications.
        # The four known relations determine a principal basis without auditing
        # the seed rank or repeating its PSD computations.
        outer_pairs = (1,) if producer_closed_pairs is None else tuple(producer_closed_pairs)
        assert 1 <= len(outer_pairs) <= 5 and len(set(outer_pairs)) == len(outer_pairs)
        assert all(i in range(1, 7) for i in outer_pairs)
        closed_set = {(c, x) for c in (0, 1) for i in outer_pairs for x in (2*i, 2*i+1)}
        kernels = [tuple(int(c in p) for p in S) for c in CENTRES]
        kernels.append(tuple(int(p in closed_set) for p in S))
        relation_matrix = sp.Matrix(kernels)
        assert M*relation_matrix.T == sp.zeros(34, 4), 'Producer closed-set/label contract mismatch.'
        excluded = relation_matrix.rref()[1]
        basis = tuple(i for i in range(34) if i not in excluded)
        rank = 30
        assert len(basis) == rank
    else:
        upper = analyse_ambient_upper(gamma)
        if not upper['complementary_gram']['psd']:
            witness = upper['complementary_gram']
            raise ValueError('Complementary Gram 7Pi_SS-T_SS is not PSD: '
                             f'integer quadratic witness value {witness["quadratic_value"]} for 15U; '
                             f'vector {witness["integer_witness"]}.')
        reduced, basis = M.rref()
        rank = len(basis)
        if rank > 30:
            raise ValueError(f'Exact residual spectral rank {rank} exceeds 30.')
        kernels = []
        for j in range(34):
            if j not in basis:
                v = [sp.Integer(0)]*34
                v[j] = sp.Integer(1)
                for i, pivot in enumerate(basis):
                    v[pivot] = -reduced[i, j]
                kernels.append(primitive(v))
    principal = M.extract(basis, basis)
    # A nonsingular principal block of a PSD matrix must be positive definite.
    # Exact LDL pivots certify that property without floating tolerances.
    lower = [[sp.Integer(i == j) for j in range(rank)] for i in range(rank)]
    diagonal = []
    for i in range(0 if producer_certified else rank):
        pivot = principal[i, i] - sum(lower[i][j]**2*diagonal[j] for j in range(i))
        if pivot <= 0:
            raise ValueError('The residual spectral matrix is not positive semidefinite.')
        diagonal.append(pivot)
        for row in range(i+1, rank):
            lower[row][i] = (principal[row, i] - sum(
                lower[row][j]*lower[i][j]*diagonal[j] for j in range(i))) / pivot
    inverse = principal.inv(method='DM')
    denominator = lcm(*(int(x.q) for x in inverse))
    numerator = [[int(inverse[i, j]*denominator) for j in range(rank)] for i in range(rank)]
    return dict(B=boundary, residual=[[int(x) for x in residual.row(i)] for i in range(49)],
                rank=rank, basis=basis, kernels=kernels, inverse=numerator,
                denominator=denominator, statistics=statistics,
                complementary_gram_psd=True,
                spectral_properties_source=('producer certification' if producer_certified
                                            else 'exact local preparation'),
                M=[[int(x) for x in M.row(i)] for i in range(34)])


def norm_polynomial(prepared, base):
    basis, H, den = prepared['basis'], prepared['inverse'], prepared['denominator']
    b = [base[i] for i in basis]
    Hb = [sum(x*y for x, y in zip(row, b)) for row in H]
    constant = sum(x*y for x, y in zip(b, Hb)) - 20*den
    linear, pair = [0]*34, [[0]*34 for _ in range(34)]
    for a, i in enumerate(basis):
        linear[i] = 64*H[a][a] - 16*Hb[a]
        for c, j in enumerate(basis):
            pair[i][j] = 128*H[a][c]
    return constant, linear, pair


def column_domain(gamma, prepared, join, label, deadline, keep_profiles=False):
    delta = int(3 in label)
    base = [-k8(s, label) for s in S]
    dot = [sum(x*y for x, y in zip(v, base)) for v in prepared['kernels']]
    report = dict(label=label, raw_bound=raw_bound(delta), kernel_profiles=0,
                  cap_profiles=0, spectral_profiles=0, complete=True,
                  remaining_degree_profile_counts={6:0, 7:0, 8:0},
                  norm_comparison_counts={'below_20':0, 'equal_20':0, 'above_20':0})
    if any(x % 8 for x in dot):
        report['obstruction'] = 'A kernel equation has a nonintegral required sum.'
        return report
    rhs = tuple(x//8 for x in dot)
    constant, linear, pair = norm_polynomial(prepared, base)
    R = prepared['residual']
    forced_star = tuple(1+c for c in label)
    if any(R[i][j] == 0 for i in forced_star for j in forced_star):
        report['obstruction'] = 'The fixed star entries exceed a boundary capacity.'
        return report
    forbidden = sum(1 << i for i in range(34)
                    if R[15+i][15+i] == 0 or any(R[15+i][j] == 0 for j in forced_star))
    conflicts = [sum(1 << j for j in range(34) if R[15+i][15+j] == 0) for i in range(34)]
    gamma_masks = [sum(v << j for j, v in enumerate(row)) for row in gamma]
    intersections = [len(set(s).intersection(label)) for s in S]
    forced, possible = (1 << 49)-1, 0
    pair_possible = [0]*49
    profiles = []
    minimum_deficit = maximum_deficit = None
    for h in join.profiles(delta, rhs):
        report['kernel_profiles'] += 1
        if report['kernel_profiles'] % 256 == 0 and time.monotonic() > deadline:
            report['complete'] = False
            break
        if h & forbidden:
            continue
        selected = tuple(bits(h))
        if any(h & conflicts[i] for i in selected):
            continue
        if any((STAR_MASKS[c] & h).bit_count() + int((c ^ 1) in label) >
               (1 if c in label else 2) for c in range(14)):
            continue
        if any(intersections[i] + (gamma_masks[i] & h).bit_count() >
               (1 if (h >> i) & 1 else 2) for i in range(34)):
            continue
        report['cap_profiles'] += 1
        value = constant + sum(linear[i] for i in selected)
        value += sum(pair[i][j] for i, j in combinations(selected, 2))
        comparison = 'below_20' if value < 0 else 'above_20' if value > 0 else 'equal_20'
        report['norm_comparison_counts'][comparison] += 1
        if ('minimum_norm_excess_numerator' not in report or
                value < report['minimum_norm_excess_numerator']):
            report['minimum_norm_excess_numerator'] = value
            report['minimum_norm_profile'] = [S[i] for i in selected]
        if ('maximum_norm_excess_numerator' not in report or
                value > report['maximum_norm_excess_numerator']):
            report['maximum_norm_excess_numerator'] = value
        report['norm_excess_denominator'] = prepared['denominator']
        if value > 0 or (prepared['rank'] == 30 and value != 0):
            continue
        report['spectral_profiles'] += 1
        report['remaining_degree_profile_counts'][12-len(selected)] += 1
        deficit = -value
        minimum_deficit = deficit if minimum_deficit is None else min(minimum_deficit, deficit)
        maximum_deficit = deficit if maximum_deficit is None else max(maximum_deficit, deficit)
        d = (h << 15) | sum(1 << j for j in forced_star)
        forced &= d
        possible |= d
        for i in bits(d):
            pair_possible[i] |= d
        if keep_profiles:
            profiles.append(h)
    if report['spectral_profiles']:
        report.update(forced_rows=forced, possible_rows=possible,
                      possible_row_pairs=pair_possible,
                      minimum_spectral_deficit_numerator=minimum_deficit,
                      maximum_spectral_deficit_numerator=maximum_deficit)
    if keep_profiles:
        report['profiles'] = profiles
    return report


def interval_obstructions(columns, prepared):
    """Necessary marginal bounds on D 1 and D D^t, after all domains are exact."""
    violations = []
    for i in range(49):
        for j in range(i, 49):
            lower = sum(bool((c['forced_rows'] >> i) & (c['forced_rows'] >> j) & 1)
                        for c in columns)
            upper = sum((c['possible_row_pairs'][i] >> j) & 1 for c in columns)
            target = prepared['residual'][i][j]
            if not lower <= target <= upper:
                violations.append(dict(rows=[i, j], minimum=lower, maximum=upper, target=target))
    return violations


def degree_obstructions(columns, expected):
    violations = []
    for size in (1, 2, 3):
        for subset in combinations((6, 7, 8), size):
            selected = set(subset)
            forced = sum(all(not count or degree in selected for degree, count in
                             c['remaining_degree_profile_counts'].items()) for c in columns)
            capacity = sum(expected[d] for d in selected)
            if forced > capacity:
                violations.append(dict(degrees=subset, forced_labels=forced, capacity=capacity))
    return violations


def analyse(gamma, seconds=30, keep_profiles=False, label_indices=None,
            producer_certified_grid_rank30=False, producer_closed_pairs=None):
    started = time.monotonic()
    report = dict(status='NECESSARY_DOMAINS_ONLY', input_labels=S, remaining_labels=U,
                  full_srg_constructed=False, solver_or_group_audit_run=False)
    try:
        prepared = prepare(gamma, producer_certified_grid_rank30, producer_closed_pairs)
    except ValueError as error:
        report.update(status='NO_COMPLETION', reason=str(error), seconds=time.monotonic()-started)
        return report
    report.update(spectral_rank=prepared['rank'], kernel_dimension=len(prepared['kernels']),
                  complementary_gram_psd=prepared['complementary_gram_psd'],
                  spectral_properties_source=prepared['spectral_properties_source'],
                  full_rank_reconstruction_available_after_columns=(prepared['rank'] == 30),
                  spectral_basis=prepared['basis'], kernels=prepared['kernels'],
                  inverse_numerator=prepared['inverse'], inverse_denominator=prepared['denominator'],
                  boundary_statistics=prepared['statistics'])
    join = ProfileJoin(prepared['kernels'])
    columns = []
    indices = list(range(50)) if label_indices is None else label_indices
    for index in indices:
        if time.monotonic() >= started+seconds:
            break
        result = column_domain(gamma, prepared, join, U[index], started+seconds, keep_profiles)
        columns.append(result)
        if result['complete'] and result['spectral_profiles'] == 0:
            report.update(status='NO_COMPLETION', reason='A remaining label has an empty necessary domain.')
            break
        if not result['complete']:
            break
    report['columns'] = columns
    report['all_50_domains_complete'] = (len(columns) == 50 and all(c['complete'] for c in columns)
                                       and {tuple(c['label']) for c in columns} == set(U))
    if report['all_50_domains_complete'] and all(c['spectral_profiles'] for c in columns):
        bad = interval_obstructions(columns, prepared)
        bad_degrees = degree_obstructions(columns, prepared['statistics']['degree_counts'])
        deficit_low = sum(c['minimum_spectral_deficit_numerator'] for c in columns)
        deficit_high = sum(c['maximum_spectral_deficit_numerator'] for c in columns)
        deficit_target = 56*(30-prepared['rank'])*prepared['denominator']
        report['marginal_obstructions'] = bad
        report['degree_histogram_obstructions'] = bad_degrees
        report['spectral_deficit_budget'] = dict(minimum=deficit_low, maximum=deficit_high,
                                                target=deficit_target,
                                                denominator=prepared['denominator'])
        if bad or bad_degrees or not deficit_low <= deficit_target <= deficit_high:
            report.update(status='NO_COMPLETION', reason='Column domains cannot meet a boundary marginal.')
        elif prepared['rank'] == 30:
            product_bound = 1
            for c in columns:
                product_bound *= c['spectral_profiles']
            report['labelled_completion_product_upper_bound'] = str(product_bound)
    report['seconds'] = time.monotonic()-started
    return report


def universal_counts():
    started = time.monotonic()
    join, rows = ProfileJoin([]), []
    for label in ((4, 6), (3, 4)):
        counts = {6:0, 7:0, 8:0}
        for h in join.profiles(int(3 in label), ()):
            if all((STAR_MASKS[c] & h).bit_count() + int((c ^ 1) in label) <=
                   (1 if c in label else 2) for c in range(14)):
                counts[12-h.bit_count()] += 1
        rows.append(dict(representative_label=label, counts_by_remaining_degree=counts,
                         total=sum(counts.values())))
    return dict(status='EXACT_FINITE_COLUMN_ENUMERATION', rows=rows,
                seconds=time.monotonic()-started,
                scope='Only root-star common-neighbour budgets; no Gamma sample or SRG construction.')


def self_test():
    assert len(S) == 34 and len(U) == 50
    assert tuple(map(len, GROUPS)) == (11, 11, 10)
    assert sum(3 in p for p in U) == 10
    assert [raw_bound(d) for d in (0, 1)] == [148346, 31460]
    kernels = [tuple(int(c in p) for p in S) for c in CENTRES]
    join = ProfileJoin(kernels)
    observed = []
    for delta in (0, 1):
        profiles = set(join.profiles(delta, (2, 2, 2-delta)))
        assert len(profiles) == raw_bound(delta)
        assert all((h & STAR_MASKS[0]).bit_count() == 2 and
                   (h & STAR_MASKS[1]).bit_count() == 2 and
                   (h & STAR_MASKS[2]).bit_count() == 2-delta for h in profiles)
        observed.append(len(profiles))
    extra = tuple(int(i in (P, PP)) for i in range(34))
    cut_join = ProfileJoin(kernels+[extra])
    cut_counts = [sum(1 for _ in cut_join.profiles(d, (2, 2, 2-d, 1))) for d in (0, 1)]
    assert cut_counts == [12100, 1210]
    # Compare the sparse exact norm polynomial against a dense rational formula.
    inverse = [[2, 1], [1, 3]]
    prepared = dict(basis=(0, 2), inverse=inverse, denominator=5)
    base = [0]*34
    base[0], base[2] = 3, -1
    constant, linear, pair = norm_polynomial(prepared, base)
    for chosen in ((), (0,), (2,), (0, 2), (1,), (0, 1, 2)):
        v = [base[i]-8*int(i in chosen) for i in (0, 2)]
        dense = sum(v[i]*inverse[i][j]*v[j] for i in range(2) for j in range(2))-100
        sparse = constant+sum(linear[i] for i in chosen)+sum(pair[i][j] for i, j in combinations(chosen, 2))
        assert dense == sparse
    # A required degree8 cannot be supplied by fifty domains allowing only6/7.
    columns = [dict(remaining_degree_profile_counts={6:1, 7:1, 8:0}) for _ in range(50)]
    expected = {6:23, 7:26, 8:1}
    assert degree_obstructions(columns, expected)
    columns[-1] = dict(remaining_degree_profile_counts={6:0, 7:0, 8:1})
    assert not degree_obstructions(columns, expected)
    for i in range(24):
        columns[i] = dict(remaining_degree_profile_counts={6:1, 7:0, 8:0})
    assert degree_obstructions(columns, expected)
    return dict(status='PASS', exact_star_domain_counts=observed,
                extra_relation_counts=cut_counts, sparse_norm_polynomial='PASS',
                degree_histogram_hall_bounds='PASS',
                scope='Own column-domain primitives only; no graph or peer result re-audited.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gamma')
    parser.add_argument('--output')
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--save-profiles', action='store_true')
    parser.add_argument('--label-indices', type=int, nargs='+')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--universal-counts', action='store_true')
    parser.add_argument('--producer-certified-grid-rank30', action='store_true',
                        help='Consume a producer certification of rank30, both PSD Grams, and the fixed grid; do not re-audit them.')
    parser.add_argument('--producer-certified-closed-pairs', type=int, nargs='+',
                        help='Same producer certification with relation on {0,1} times the listed mate pairs (indices1..6).')
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    elif args.universal_counts:
        result = universal_counts()
    else:
        if not args.gamma or args.seconds <= 0:
            parser.error('--gamma and a positive --seconds are required.')
        if args.label_indices is not None and any(i not in range(50) for i in args.label_indices):
            parser.error('Remaining-label indices must lie in 0..49.')
        if args.label_indices is not None and len(set(args.label_indices)) != len(args.label_indices):
            parser.error('Remaining-label indices must not be repeated.')
        result = analyse(load_gamma(args.gamma), args.seconds, args.save_profiles, args.label_indices,
                         args.producer_certified_grid_rank30, args.producer_certified_closed_pairs)
    rendered = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(rendered+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k in
                      ('status', 'reason', 'spectral_rank', 'kernel_dimension', 'seconds',
                       'all_50_domains_complete', 'exact_star_domain_counts', 'extra_relation_counts', 'scope')}))


if __name__ == '__main__':
    main()
