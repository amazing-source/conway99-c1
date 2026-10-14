"""Exact domains beyond a producer-certified four-star Conway boundary.

Consumes an exact principal basis and PSD/rank certification, without
repeating them. Four-star sums use two reusable4356-entry tables. The
number of matching profiles is input-dependent, at most4,949,026/label.
If rank(T)=30 and rank(U)=40, both new Gram norms must be exact.
"""
import argparse
from collections import defaultdict
from itertools import combinations, islice
from math import comb, lcm
from pathlib import Path
import json
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_profile_join import LABELS, boundary, residual, upper_entry
from three_star_column_domains import bits, k8, primitive

S = LABELS
INDEX = {p: i for i, p in enumerate(S)}
MISSING = tuple(p for p in combinations(range(4, 14), 2) if p[1] != (p[0] ^ 1))
OVERLAP = tuple(INDEX[p] for p in ((0, 2), (0, 3), (1, 2), (1, 3)))
GROUPS = tuple(tuple(INDEX[(c, x)] for x in range(4, 14)) for c in range(4))
STAR_MASKS = tuple(sum(1 << i for i, p in enumerate(S) if c in p) for c in range(14))


def pattern_degrees(mask):
    degree = [0]*4
    for j, index in enumerate(OVERLAP):
        if (mask >> j) & 1:
            for c in S[index]:
                degree[c] += 1
    return degree


class ProfileJoin:
    def __init__(self, kernels):
        self.width = len(kernels)
        groups = []
        for group in GROUPS:
            entries = {}
            for size in range(3):
                entries[size] = [(sum(1 << i for i in chosen),
                                  tuple(sum(q[i] for i in chosen) for q in kernels))
                                 for chosen in combinations(group, size)]
            groups.append(entries)
        self.left, self.right = {}, {}
        self.raw_count = self.left_entries = self.right_entries = 0
        for mask in range(16):
            degree = pattern_degrees(mask)
            sizes = [2-d for d in degree]
            overlap = sum(1 << OVERLAP[j] for j in range(4) if (mask >> j) & 1)
            offset = tuple(sum(q[OVERLAP[j]] for j in range(4) if (mask >> j) & 1) for q in kernels)
            left = defaultdict(list)
            for h0, v0 in groups[0][sizes[0]]:
                for h1, v1 in groups[1][sizes[1]]:
                    key = tuple(a+b+c for a, b, c in zip(v0, v1, offset))
                    left[key].append(h0 | h1 | overlap)
                    self.left_entries += 1
            right = []
            for h2, v2 in groups[2][sizes[2]]:
                for h3, v3 in groups[3][sizes[3]]:
                    right.append((h2 | h3, tuple(a+b for a, b in zip(v2, v3))))
                    self.right_entries += 1
            self.left[mask], self.right[mask] = left, right
            self.raw_count += comb(10, sizes[0])*comb(10, sizes[1])*comb(10, sizes[2])*comb(10, sizes[3])

    def profiles(self, rhs):
        for mask in range(16):
            table = self.left[mask]
            for right, values in self.right[mask]:
                key = tuple(a-b for a, b in zip(rhs, values))
                for left in table.get(key, ()):
                    yield left | right

    def count(self, rhs):
        return sum(len(self.left[mask].get(tuple(a-b for a, b in zip(rhs, values)), ()))
                   for mask in range(16) for _, values in self.right[mask])


def principal_data(matrix, basis):
    inverse = matrix.extract(basis, basis).inv(method='DM')
    denominator = lcm(*(int(x.q) for x in inverse))
    numerator = [[int(x*denominator) for x in inverse.row(i)] for i in range(len(basis))]
    return dict(basis=basis, inverse=numerator, denominator=denominator), inverse


def prepare(gamma, rank, basis, upper_rank40):
    if len(basis) != rank or len(set(basis)) != rank or any(i not in range(44) for i in basis):
        raise ValueError('Principal basis must contain exactly rank distinct indices0..43.')
    M = sp.Matrix(44, 44, lambda i, j: 24*int(i == j)-8*gamma[i][j]-k8(S[i], S[j]))
    lower, inverse = principal_data(M, basis)
    kernels = []
    for j in range(44):
        if j in basis:
            continue
        coefficients = inverse*M.extract(basis, [j])
        vector = [sp.Integer(0)]*44
        vector[j] = sp.Integer(1)
        for i, value in zip(basis, coefficients):
            vector[i] = -value
        kernels.append(primitive(vector))
    # These relations follow from the producer-certified rank and basis.
    # No independent rank, nullspace, or PSD test is run on the input.
    result = dict(rank=rank, lower=lower, kernels=kernels,
                  residual=residual(boundary(gamma, S)), upper=None)
    if upper_rank40:
        stars = sp.Matrix([[int(c in p) for p in S] for c in range(4)])
        anchors = stars.rref()[1]
        upper_basis = [i for i in range(44) if i not in anchors]
        N = sp.Matrix(44, 44, lambda i, j: upper_entry(S[i], S[j], gamma[i][j], i == j))
        result['upper'], _ = principal_data(N, upper_basis)
    return result


def norm_polynomial(data, base, slope, diagonal):
    basis, inverse, den = data['basis'], data['inverse'], data['denominator']
    b = [base[i] for i in basis]
    hb = [sum(x*y for x, y in zip(row, b)) for row in inverse]
    constant = sum(x*y for x, y in zip(b, hb))-diagonal*den
    linear, pair = [0]*44, [[0]*44 for _ in range(44)]
    for a, i in enumerate(basis):
        linear[i] = slope*slope*inverse[a][a]+2*slope*hb[a]
        for c, j in enumerate(basis):
            pair[i][j] = 2*slope*slope*inverse[a][c]
    return constant, linear, pair


def value_of(polynomial, selected):
    constant, linear, pair = polynomial
    return constant+sum(linear[i] for i in selected)+sum(pair[i][j] for i, j in combinations(selected, 2))


def column(gamma, prepared, join, label, deadline, save_profiles):
    base = [-k8(p, label) for p in S]
    dot = [sum(x*y for x, y in zip(q, base)) for q in prepared['kernels']]
    report = dict(label=label, complete=True, raw_profiles=join.raw_count,
                  kernel_profiles=0, capacity_profiles=0, lower_norm_profiles=0,
                  final_profiles=0, upper_rank40_filter=prepared['upper'] is not None)
    if any(x % 8 for x in dot):
        report['obstruction'] = 'A kernel equation has a noninteger required sum.'
        return report
    rhs = tuple(x//8 for x in dot)
    lower_poly = norm_polynomial(prepared['lower'], base, -8, 20)
    upper_poly = (norm_polynomial(prepared['upper'], [upper_entry(p, label, 0) for p in S], 15, 50)
                  if prepared['upper'] is not None else None)
    R = prepared['residual']
    roots = tuple(1+c for c in label)
    if any(R[i][j] == 0 for i in roots for j in roots):
        report['obstruction'] = 'The fixed neighbours exceed a boundary capacity.'
        return report
    forbidden = sum(1 << i for i in range(44) if R[15+i][15+i] == 0 or any(R[15+i][j] == 0 for j in roots))
    conflicts = [sum(1 << j for j in range(44) if R[15+i][15+j] == 0) for i in range(44)]
    gamma_masks = [sum(x << j for j, x in enumerate(row)) for row in gamma]
    intersections = [len(set(p) & set(label)) for p in S]
    profiles = []
    for h in join.profiles(rhs):
        report['kernel_profiles'] += 1
        if report['kernel_profiles'] % 256 == 0 and time.monotonic() >= deadline:
            report['complete'] = False
            break
        if h & forbidden:
            continue
        selected = tuple(bits(h))
        if any(h & conflicts[i] for i in selected):
            continue
        if any((h & STAR_MASKS[c]).bit_count()+int((c ^ 1) in label) > 2-int(c in label) for c in range(14)):
            continue
        if any(intersections[i]+(gamma_masks[i] & h).bit_count() > 2-((h >> i) & 1) for i in range(44)):
            continue
        report['capacity_profiles'] += 1
        lower = value_of(lower_poly, selected)
        if lower > 0 or (prepared['rank'] == 30 and lower != 0):
            continue
        report['lower_norm_profiles'] += 1
        if upper_poly is not None and value_of(upper_poly, selected) != 0:
            continue
        report['final_profiles'] += 1
        if save_profiles:
            profiles.append(h)
    if save_profiles:
        report['profiles'] = profiles
    return report


def analyse(gamma, rank, basis, upper_rank40, indices, seconds, save_profiles):
    start = time.monotonic()
    prepared = prepare(gamma, rank, basis, upper_rank40)
    join = ProfileJoin(prepared['kernels'])
    report = dict(status='NECESSARY_DOMAINS_ONLY', input_labels=S, missing_labels=MISSING,
                  seed_properties_source='producer certification', seed_reaudited=False,
                  rank_T=rank, rank_U=(40 if upper_rank40 else 'not used'),
                  spectral_basis=basis, inverse_numerator=prepared['lower']['inverse'],
                  inverse_denominator=prepared['lower']['denominator'], kernels=prepared['kernels'],
                  table_entries=[join.left_entries, join.right_entries], raw_profiles_per_label=join.raw_count,
                  columns=[], full_srg_constructed=False)
    for index in indices:
        if time.monotonic() >= start+seconds:
            report['status'] = 'TIME_LIMIT_NO_EXCLUSION'
            break
        result = column(gamma, prepared, join, MISSING[index], start+seconds, save_profiles)
        report['columns'].append(result)
        if result['complete'] and not result['final_profiles']:
            report.update(status='NO_COMPLETION', empty_domain_label=MISSING[index])
            break
        if not result['complete']:
            report['status'] = 'TIME_LIMIT_NO_EXCLUSION'
            break
    report['all40_domains_complete'] = (len(report['columns']) == 40 and all(c['complete'] for c in report['columns']))
    report['seconds'] = time.monotonic()-start
    return report


def self_test():
    assert len(S) == 44 and len(MISSING) == 40 and all(len(g) == 10 for g in GROUPS)
    stars = [tuple(int(c in p) for p in S) for c in range(4)]
    join = ProfileJoin(stars)
    assert (join.left_entries, join.right_entries, join.raw_count) == (4356, 4356, 4949026)
    assert join.count((2, 2, 2, 2)) == 4949026
    for h in islice(join.profiles((2, 2, 2, 2)), 128):
        assert all((h & STAR_MASKS[c]).bit_count() == 2 for c in range(4))
    overlap_relation = tuple(int(i == OVERLAP[0]) for i in range(44))
    refined = ProfileJoin(stars+[overlap_relation])
    assert refined.count((2, 2, 2, 2, 1)) == 221801
    data = dict(basis=(0, 2), inverse=[[2, 1], [1, 3]], denominator=5)
    base = [0]*44
    base[0], base[2] = 3, -1
    for slope, diagonal in ((-8, 20), (15, 50)):
        polynomial = norm_polynomial(data, base, slope, diagonal)
        for chosen in ((), (0,), (2,), (0, 2), (1,), (0, 1, 2)):
            m = [base[i]+slope*int(i in chosen) for i in data['basis']]
            dense = sum(m[i]*data['inverse'][i][j]*m[j] for i in range(2) for j in range(2))-diagonal*5
            assert value_of(polynomial, chosen) == dense
    return dict(status='PASS', raw_profiles=join.raw_count, table_entries=[join.left_entries, join.right_entries],
                one_forced_overlap_profiles=221801, lower_and_upper_norm_polynomials='PASS',
                scope='Own domain and exact norm primitives; no four-star rank30 seed available or audited.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input')
    p.add_argument('--producer-rank', type=int, default=30)
    p.add_argument('--basis', type=int, nargs='+', help='Producer principal basis, in the input label order.')
    p.add_argument('--producer-upper-rank40', action='store_true')
    p.add_argument('--seconds', type=float, default=30)
    p.add_argument('--label-indices', type=int, nargs='+')
    p.add_argument('--save-profiles', action='store_true')
    p.add_argument('--self-test', action='store_true')
    p.add_argument('--output', required=True)
    a = p.parse_args()
    if a.self_test:
        result = self_test()
    else:
        if not a.input or not 1 <= a.producer_rank <= 30 or a.seconds <= 0:
            p.error('Supply a certified seed with rank in1..30 and a positive time budget.')
        data = json.loads(Path(a.input).read_text(encoding='utf-8-sig'))
        labels = tuple(tuple(sorted(x)) for x in data['labels'])
        if len(labels) != 44 or set(labels) != set(S):
            raise ValueError('Expected the44 four-star labels.')
        supplied_basis = a.basis if a.basis is not None else data.get('T_principal_basis')
        if supplied_basis is None:
            p.error('A producer principal basis is required; no seed rank/PSD audit is performed.')
        basis = [INDEX[labels[i]] for i in supplied_basis]
        source = data['structures'][0] if 'structures' in data else data
        gamma = [[0]*44 for _ in range(44)]
        for i, j in source['edges']:
            i, j = INDEX[labels[i]], INDEX[labels[j]]
            gamma[i][j] = gamma[j][i] = 1
        indices = list(range(40)) if a.label_indices is None else a.label_indices
        if len(indices) != len(set(indices)) or any(i not in range(40) for i in indices):
            p.error('Label indices must be distinct and in0..39.')
        result = analyse(gamma, a.producer_rank, basis, a.producer_upper_rank40, indices, a.seconds, a.save_profiles)
    output = Path(a.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'raw_profiles', 'table_entries', 'seconds', 'scope') if k in result}))


if __name__ == '__main__':
    main()
