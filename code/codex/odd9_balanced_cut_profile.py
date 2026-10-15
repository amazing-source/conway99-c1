"""Measure all balanced24-set cuts on a supplied four-star adjacency.

This computes a NEW edge-count statistic only: no producer PSD, rank,
automorphism or admissibility claim is re-tested. Under binary C1 and
T PSD the maximum is at most48, by the strict parity cut.

There are586278 balanced choices modulo complementation of the outer20
set. Fixing (0,4) in the chosen set selects one of each complementary
pair. The two cuts have equal edge counts under C1. The six column
patterns are split into two groups of five columns; matching row totals
allows exact integer matrix arithmetic on small blocks.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import factorial
from pathlib import Path
import json
import time

import numpy as np


LABELS = [(i, j) for i, j in combinations(range(14), 2)
          if j != (i ^ 1) and i < 4]


def rational(numerator, denominator):
    value = Fraction(int(numerator), int(denominator))
    return int(value) if value.denominator == 1 else str(value)


@lru_cache(maxsize=1)
def partial_patterns():
    pairs = list(combinations(range(4), 2))
    X = np.zeros((6**5, 20), dtype=np.int64)
    for i, pattern in enumerate(product(range(6), repeat=5)):
        for y, pair_index in enumerate(pattern):
            for c in pairs[pair_index]:
                X[i, 5*c+y] = 1
    row_totals = X.reshape(-1, 4, 5).sum(axis=2)
    left, right = defaultdict(list), defaultdict(list)
    for i, counts in enumerate(row_totals):
        key = tuple(int(c) for c in counts)
        right[key].append(i)
        if X[i, 0]:
            left[key].append(i)
    groups = [(np.array(ids, dtype=int), np.array(right[tuple(5-c for c in key)], dtype=int))
              for key, ids in left.items()]
    paired_columns = (X[:, :5]*X[:, 5:10]).sum(axis=1)
    # In any complete balanced pattern, the six column multiplicities
    # are (a,b,c,c,b,a), with a+b+c=5.
    expected_by_a = [sum(factorial(10)//(factorial(a)*factorial(b)*factorial(5-a-b))**2
                         for b in range(6-a))//2 for a in range(6)]
    assert sum(len(i)*len(j) for i, j in groups) == sum(expected_by_a) == 586278
    assert expected_by_a == [31752, 220500, 252000, 75600, 6300, 126]
    return X, groups, paired_columns, expected_by_a


def profile(adjacency, labels=LABELS, scale=1):
    """Exact new statistic; admissibility hypotheses are accepted from producer.

    adjacency is an integer matrix, optionally equal to scale*Gamma.
    labels specifies its row order. Returned edge counts are exact.
    No positivity or graph-rank calculation occurs here.
    """
    labels = [tuple(sorted(p)) for p in labels]
    if len(labels) != 44 or set(labels) != set(LABELS):
        raise ValueError('Expected the44 distinct four-star labels.')
    if not isinstance(scale, int) or scale <= 0:
        raise ValueError('scale must be a positive integer.')
    raw = np.asarray(adjacency)
    if raw.shape != (44, 44) or raw.dtype.kind not in 'iu':
        raise ValueError('Expected a44-by-44 integer adjacency matrix.')
    if max(abs(int(raw.min())), abs(int(raw.max()))) > 10**12:
        raise ValueError('Coefficients are too large for this int64 implementation.')
    G = raw.astype(np.int64)
    index = {p: i for i, p in enumerate(labels)}
    O = [index[p] for p in ((0, 2), (0, 3), (1, 2), (1, 3))]
    L = [index[c, y] for c in range(4) for y in range(4, 9)]
    R = [index[c, y] for c in range(4) for y in range(9, 14)]
    X, groups, paired_columns, expected_by_a = partial_patterns()
    constant = int(G[np.ix_(O, O)].sum())//2
    local_left = (np.sum((X@G[np.ix_(L, L)])*X, axis=1)//2
                  +X@G[np.ix_(L, O)].sum(axis=1))
    local_right = (np.sum((X@G[np.ix_(R, R)])*X, axis=1)//2
                   +X@G[np.ix_(R, O)].sum(axis=1))
    cross = G[np.ix_(L, R)]
    statistics = [dict(count=0, best=None, number_best=0, at_48=0, above_48=0)
                  for _ in range(6)]
    for left_ids, right_ids in groups:
        scores = (constant+local_left[left_ids, None]+local_right[None, right_ids]
                  +X[left_ids]@cross@X[right_ids].T)
        classes = paired_columns[left_ids, None]+paired_columns[None, right_ids]
        for a in np.unique(classes):
            mask = classes == a
            values = scores[mask]
            s = statistics[int(a)]
            best = int(values.max())
            number_best = int(np.count_nonzero(values == best))
            s['count'] += int(values.size)
            s['at_48'] += int(np.count_nonzero(values == 48*scale))
            s['above_48'] += int(np.count_nonzero(values > 48*scale))
            if s['best'] is None or best > s['best']:
                row, column = np.argwhere(mask & (scores == best))[0]
                s['best'] = best
                s['number_best'] = number_best
                s['witness_ids'] = int(left_ids[row]), int(right_ids[column])
            elif best == s['best']:
                s['number_best'] += number_best
    assert [s['count'] for s in statistics] == expected_by_a

    def describe(s):
        i, j = s['witness_ids']
        selected = sorted(O+[L[t] for t in range(20) if X[i, t]]
                          +[R[t] for t in range(20) if X[j, t]])
        # A direct count on the returned witness guards the indexing of
        # this new statistic; it does not re-audit producer hypotheses.
        assert int(G[np.ix_(selected, selected)].sum()) == 2*s['best']
        return dict(indexed_directions=s['count'],
                    max_induced_edges=rational(s['best'], scale),
                    maximizing_directions=s['number_best'],
                    directions_at_48=s['at_48'], directions_above_48=s['above_48'],
                    min_T_energy_under_C1=rational(8*(49*scale-s['best']), scale),
                    witness_selected_labels=[labels[i] for i in selected])

    best = max(s['best'] for s in statistics)
    winners = [s for s in statistics if s['best'] == best]
    all_stats = dict(count=sum(s['count'] for s in statistics), best=best,
                     number_best=sum(s['number_best'] for s in winners),
                     at_48=sum(s['at_48'] for s in statistics),
                     above_48=sum(s['above_48'] for s in statistics),
                     witness_ids=winners[0]['witness_ids'])
    return dict(
        scope='New edge-count statistic only; no producer hypotheses re-tested.',
        normalization='Select (0,4); complementary choices have equal counts under C1.',
        binary_bound_under_C1_and_T_PSD=48,
        all_balanced=describe(all_stats), h_odd_subfamily=describe(statistics[0]),
        by_paired_column_count=[dict(a=a, **describe(s)) for a, s in enumerate(statistics)],
        paired_column_definition='a counts outer letters selecting both0 and1; the number selecting both2 and3 is also a.',
        count_formula='half sum_{a+b+c=5}10!/(a! b! c!)^2 =586278; a=0 gives31752.')


def from_export(data):
    """Adapter for producer JSON containing labels and edges or a matrix."""
    labels = data.get('labels', LABELS)
    if 'adjacency_scaled' in data:
        return profile(data['adjacency_scaled'], labels, data['scale'])
    if 'adjacency' in data:
        return profile(data['adjacency'], labels)
    G = np.zeros((44, 44), dtype=np.int64)
    if 'adjacency_rows_hex' in data:
        for i, row in enumerate(data['adjacency_rows_hex']):
            bits = int(row, 16)
            for j in range(44):
                G[i, j] = (bits >> j) & 1
    else:
        for i, j in data['edges']:
            G[i, j] = G[j, i] = 1
    return profile(G, labels)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, nargs='+', required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = dict(scope='New cut statistics on supplied exports; their existing certificates are accepted.',
                  profiles=[])
    for path in args.input:
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        started = time.perf_counter()
        result = from_export(data)
        result['input'] = str(path.resolve())
        result['seconds'] = time.perf_counter()-started
        # Copy only supplied descriptive metadata, with its provenance clear.
        result['producer_metadata'] = {k: data[k] for k in ('c', 'gens') if k in data}
        report['profiles'].append(result)
        if 'binary_saturation_fixture' in data:
            report['own_binary_non_PSD_fixture'] = from_export(data['binary_saturation_fixture'])
        print(json.dumps(dict(input=path.name, all_balanced_max=result['all_balanced']['max_induced_edges'],
                              h_odd_max=result['h_odd_subfamily']['max_induced_edges'],
                              at_48=result['all_balanced']['directions_at_48'],
                              seconds=round(result['seconds'], 3))))
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
