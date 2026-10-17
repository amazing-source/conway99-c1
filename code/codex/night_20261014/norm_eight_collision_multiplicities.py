"""Collision multiplicities for z in {0,+/-1}^99, |supp z|=8, sum z=0,
and 7*z^T*P*z=8. Counts are ordered representations z-z'=h of a fixed h.

The integral kernels of l1 mass 16 need no vertices outside their support.
The norm-14 kernels need one shared outside vertex. Norm-12 kernels need
two. Their incidence and pair-count relaxations have exact rational duals.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json

import numpy as np
from scipy.optimize import linprog

from small_positive_three_supports import decode, edge, outside_patterns, pairs, valid


def templates(report):
    for p in [6, 7, 8]:
        section = report[str(p)]
        reps = section['representatives']
        for coupling in section['support_couplings']:
            left = decode(reps[coupling['first']]['code'], p)
            right = decode(reps[coupling['second']]['code'], p)
            for matching in coupling['matchings']:
                rows = left + [row << p for row in right]
                fours = [x for x in range(p) if left[x].bit_count() == 4]
                for x, y in zip(fours, matching):
                    edge(rows, x, p+y)
                yield dict(p=p, first=coupling['first'], second=coupling['second'],
                           fours=len(fours), matching=matching), rows, [1]*p+[-1]*p
    for item in report['weighted_l1_at_most_16']:
        rows = [0]*len(item['signs'])
        for x, y in item['edges']:
            edge(rows, x, y)
        yield dict(weighted=item['second_part']), rows, item['signs']


def assignments(rows, h, outside):
    """Return base z data compatible with both support sizes being eight."""
    n = len(rows)
    forced = [x for x in range(n) if abs(h[x]) == 2]
    variable = [x for x in range(n) if abs(h[x]) == 1]
    signs = [1 if x > 0 else -1 for x in h]
    needed = 8-outside-len(forced)
    positive = sum(1 << x for x in range(n) if signs[x] > 0)
    negative = ((1 << n)-1) ^ positive
    for selected in combinations(variable, needed):
        vertices = forced + list(selected)
        mask = sum(1 << x for x in vertices)
        total = (mask & positive).bit_count()-(mask & negative).bit_count()
        if abs(total) > outside or (total+outside) % 2:
            continue
        signed_edges = sum(signs[x]*((rows[x] & mask & positive).bit_count() -
                                     (rows[x] & mask & negative).bit_count()) for x in vertices)//2
        yield mask, total, signed_edges, positive, negative


def exact_upper_bound(matrix, rhs, objective, labels):
    """Nonnegative variables, equalities; verify a rational maximizing dual."""
    result = linprog(-np.asarray(objective, dtype=float), A_eq=np.asarray(matrix, dtype=float),
                     b_eq=np.asarray(rhs, dtype=float), bounds=(0, None), method='highs')
    assert result.success, result.message
    dual = [Fraction(-float(value)).limit_denominator(1000000) for value in result.eqlin.marginals]
    # The first row is all ones, so a small exact correction repairs rounding.
    assert all(value == 1 for value in matrix[0])
    deficits = [Fraction(objective[j])-sum(dual[i]*matrix[i][j] for i in range(len(rhs)) if matrix[i][j])
                for j in range(len(objective))]
    dual[0] += max(Fraction(0), max(deficits))
    slacks = [sum(dual[i]*matrix[i][j] for i in range(len(rhs)) if matrix[i][j])-objective[j]
              for j in range(len(objective))]
    assert min(slacks) >= 0
    upper = sum(value*factor for value, factor in zip(dual, rhs))
    return dict(upper_bound=str(upper), integer_upper_bound=upper.numerator//upper.denominator,
                dual=[dict(row=labels[i], coefficient=str(value)) for i, value in enumerate(dual) if value],
                minimum_slack=str(min(slacks)))


def one_outside(rows, h):
    patterns, residual = outside_patterns(rows, h)
    objective = [0]*len(patterns)
    for mask, total, signed_edges, positive, negative in assignments(rows, h, 1):
        sign = -total
        assert sign in [-1, 1]
        for j, pattern in enumerate(patterns):
            incidence = (mask & pattern & positive).bit_count()-(mask & pattern & negative).bit_count()
            objective[j] += signed_edges+sign*incidence == 8
    labels = [[]] + [[x] for x in range(len(rows))] + [list(pair) for pair in pairs(len(rows))]
    rhs = [99-len(rows)] + [14-row.bit_count() for row in rows] + [residual[x,y] for x,y in pairs(len(rows))]
    matrix = [[int(all(pattern >> x & 1 for x in label)) for pattern in patterns] for label in labels]
    bound = exact_upper_bound(matrix, rhs, objective, labels)
    return dict(pattern_count=len(patterns), objectives=objective, **bound)


def two_outside(rows, h):
    patterns, residual = outside_patterns(rows, h)
    n, count = len(rows), len(patterns)
    outside_count = 99-n
    base = list(assignments(rows, h, 2))
    sums = np.array([item[1] for item in base])
    base_edges = np.array([item[2] for item in base])
    incidence = np.array([[(mask & pattern & positive).bit_count()-(mask & pattern & negative).bit_count()
                           for pattern in patterns] for mask, _, _, positive, negative in base])
    pair_columns, objectives = [], [0]*count
    for i in range(count):
        for j in range(i, count):
            for adjacent in [0, 1]:
                extended = rows + [0, 0]
                for x in range(n):
                    if patterns[i] >> x & 1:
                        edge(extended, x, n)
                    if patterns[j] >> x & 1:
                        edge(extended, x, n+1)
                if adjacent:
                    edge(extended, n, n+1)
                if not valid(extended):
                    continue
                objective = 0
                for first_sign in [-1, 1]:
                    for second_sign in [-1, 1]:
                        objective += int(np.count_nonzero((sums+first_sign+second_sign == 0) &
                            (base_edges+first_sign*incidence[:, i]+second_sign*incidence[:, j]
                             +first_sign*second_sign*adjacent == 8)))
                pair_columns.append((i, j, adjacent))
                objectives.append(objective)
    width = len(objectives)
    matrix, rhs, labels = [], [], []

    def add(label, value, first, second):
        matrix.append(first+second)
        rhs.append(value)
        labels.append(label)

    # An all-positive row also allows exact repair of a rounded numerical dual.
    add(['all_variables'], outside_count+outside_count*(outside_count-1)//2,
        [1]*count, [1]*len(pair_columns))
    for subset in [[]]+[[x] for x in range(n)]+[list(pair) for pair in pairs(n)]:
        value = outside_count if not subset else (14-rows[subset[0]].bit_count() if len(subset) == 1 else residual[tuple(subset)])
        add(['pattern_marginal']+subset, value,
            [int(all(pattern >> x & 1 for x in subset)) for pattern in patterns], [0]*len(pair_columns))
    for i, pattern in enumerate(patterns):
        for only_edges in [False, True]:
            for vertex in [None]+list(range(n)):
                if only_edges:
                    factor = 14-pattern.bit_count() if vertex is None else (
                        (1 if pattern >> vertex & 1 else 2)-(rows[vertex] & pattern).bit_count())
                else:
                    factor = outside_count-1 if vertex is None else (
                        14-rows[vertex].bit_count()-((pattern >> vertex) & 1))
                left = [0]*count
                left[i] = -factor
                right = []
                for a, b, adjacent in pair_columns:
                    value = 0
                    if adjacent or not only_edges:
                        if a == i and (vertex is None or patterns[b] >> vertex & 1):
                            value += 1
                        if b == i and (vertex is None or patterns[a] >> vertex & 1):
                            value += 1
                    right.append(value)
                add(['edge_marginal' if only_edges else 'pair_marginal', i, vertex], 0, left, right)
    assert all(len(row) == width for row in matrix)
    bound = exact_upper_bound(matrix, rhs, objectives, labels)
    return dict(pattern_count=count, pair_column_count=len(pair_columns), equation_count=len(rhs),
                maximum_pair_objective=max(objectives), **bound)


def main():
    data = Path(__file__).resolve().parents[3] / 'data' / 'codex_night_20261014'
    source = json.loads((data / 'small_positive_three_supports.json').read_text())
    report = []
    for item, rows, h in templates(source):
        outside = (16-sum(abs(x) for x in h))//2
        if outside == 2:
            item['two_outside'] = two_outside(rows, h)
            item['representation_bound'] = item['two_outside']['integer_upper_bound']
        elif outside == 1:
            item['one_outside'] = one_outside(rows, h)
            item['representation_bound'] = item['one_outside']['integer_upper_bound']
        else:
            count = sum(signed_edges == 8 for _, _, signed_edges, _, _ in assignments(rows, h, 0))
            item['exact_representations'] = count
            item['representation_bound'] = count
        report.append(item)
    grouped = {}
    for item in report:
        key = 'weighted' if 'weighted' in item else f"p{item['p']}_fours{item['fours']}"
        grouped.setdefault(key, Counter())[item['representation_bound']] += 1
    print(json.dumps({key: dict(value) for key, value in grouped.items()}), flush=True)
    maxima = {}
    for item in report:
        if item.get('p') == 8:
            key = item['first'], item['second']
            maxima[key] = max(maxima.get(key, 0), item['representation_bound'])
    reps = source['8']['representatives']
    losses = dict(norm12=2871*2508, norm14=4158*184)
    for fours, degree in [(0, 2), (2, 4), (4, 10)]:
        indices = [i for i, rep in enumerate(reps) if rep['degrees'].count(4) == fours]
        for i in indices:
            for j in indices:
                if i <= j:
                    assert 2*maxima[i,j] <= maxima[i,i]+maxima[j,j]
        losses[f'norm16_fours{fours}'] = degree*sum(reps[i]['induced_copy_bound']*maxima[i,i] for i in indices)//2
    # Charge a windmill/cubic pair at most 96 to its windmill. Charge a
    # windmill/windmill pair 144/2=72 to each endpoint. Each has <=3 partners.
    assert max(item['representation_bound'] for item in report if 'weighted' in item and item['weighted'] != 'windmill') == 96
    losses['weighted_norm18_or_20'] = 3*96*3465
    assert sum(losses.values()) == 15932268
    output = dict(scope='support exactly eight, sum zero, squared projected norm eight',
                  ordered_representations_of_fixed_signed_kernel=report,
                  unordered_collision_pair_bounds=losses,
                  all_unordered_collision_pairs_bound=sum(losses.values()))
    (data / 'norm_eight_collision_multiplicities.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(losses=losses, total=sum(losses.values()))), flush=True)


if __name__ == '__main__':
    main()
