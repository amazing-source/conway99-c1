"""Enumerate bounded incidence-kernel templates and filter impossible rows.

All ternary u with Du=0 and nonconstant third-star tail are covered up to
specified relabellings preserving q. The row interval test is necessary,
not sufficient for a common symmetric binary Gamma or for PSD.
"""
import argparse
from collections import Counter, defaultdict
from itertools import combinations_with_replacement, product
from math import factorial
from pathlib import Path
import json
import sys
import time

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_prescribed_kernel import LABELS, S, K8

STATES = ((0, 0, 0), (1, -1, 0), (1, 0, -1), (-1, 1, 0),
          (0, 1, -1), (-1, 0, 1), (0, -1, 1))
PAIR_TYPES = tuple(combinations_with_replacement(range(7), 2))
INDEX = {p:i for i, p in enumerate(LABELS)}
OVERLAP = (INDEX[0, 2], INDEX[1, 2])
GROUPS = tuple(tuple(i for i, p in enumerate(LABELS)
                     if tuple(c for c in (0, 1, 2) if c in p) == (centre,))
               for centre in (0, 1, 2))
TAIL = GROUPS[2]
CANONICAL_AC = ((0, 0), (0, 1), (1, -1), (1, 0), (1, 1))


def multiset_records(size):
    records = []
    for choices in combinations_with_replacement(range(28), size):
        triples = [STATES[s] for pair in choices for s in PAIR_TYPES[pair]]
        total0 = sum(t[0] for t in triples)
        total2 = sum(t[2] for t in triples)
        active2 = sum(abs(t[2]) for t in triples)
        orbit = factorial(size)
        for count in Counter(choices).values():
            orbit //= factorial(count)
        orbit *= 2**sum(PAIR_TYPES[p][0] != PAIR_TYPES[p][1] for p in choices)
        records.append((choices, total0, total2, active2, orbit))
    return records


def labelled_count_by_dp():
    counts = {(0, 0, False):1}
    for _ in range(10):
        after = defaultdict(int)
        for (sum0, sum2, active), count in counts.items():
            for x0, _, x2 in STATES:
                after[sum0+x0, sum2+x2, active or bool(x2)] += count
        counts = after
    return sum(counts.get((-a-c, 0, True), 0) for a, c in CANONICAL_AC)


def enumerate_vectors(reference_pairs):
    first = [p for p in range(2, 7) if p in reference_pairs]
    second = [p for p in range(2, 7) if p not in reference_pairs]
    left, right = multiset_records(len(first)), multiset_records(len(second))
    by_sum = defaultdict(list)
    for rec in right:
        by_sum[rec[1], rec[2]].append(rec)
    vectors = []
    weighted_count = 0
    for a, c in CANONICAL_AC:
        for lrec in left:
            for rrec in by_sum[-a-c-lrec[1], -lrec[2]]:
                if not (lrec[3]+rrec[3]):
                    continue
                u = [0]*34
                u[INDEX[0, 2]], u[INDEX[1, 2]] = a, -a
                u[INDEX[0, 3]], u[INDEX[1, 3]] = c, -c
                for pairs, rec in ((first, lrec), (second, rrec)):
                    for pair, pair_type in zip(pairs, rec[0]):
                        for x, state in zip((2*pair, 2*pair+1), PAIR_TYPES[pair_type]):
                            for centre, value in enumerate(STATES[state]):
                                u[INDEX[centre, x]] = value
                vectors.append(u)
                weighted_count += lrec[4]*rrec[4]
    expected = labelled_count_by_dp()
    assert weighted_count == expected
    array = np.array(vectors, dtype=np.int16).reshape((-1, 34))
    D = np.array([[int(c in p) for p in LABELS] for c in range(14)], dtype=np.int16)
    assert not np.any(array@D.T)
    assert np.all(np.any(array[:, TAIL], axis=1))
    return array, dict(normalized_templates=len(vectors),
                       labelled_templates_with_canonical_ac=weighted_count,
                       independent_dynamic_program_count=expected,
                       orbit_coverage_count_passed=True)


def filter_row_intervals(vectors, q):
    survivors = vectors.copy()
    star_rhs = (24*S-K8@S)//8
    twice_Kq = (K8@q)//4
    records = []
    order = list(TAIL)+[i for i in range(34) if i not in TAIL]
    for i in order:
        before = len(survivors)
        if not before:
            break
        z = survivors+2*q
        target = 3*z[:, i]-twice_Kq[i]
        low, high = [], []
        for group in GROUPS:
            values = np.sort(z[:, [j for j in group if j != i]], axis=1)
            low.append((np.zeros(before, dtype=np.int16), values[:, 0],
                        values[:, 0]+values[:, 1]))
            high.append((np.zeros(before, dtype=np.int16), values[:, -1],
                         values[:, -1]+values[:, -2]))
        keep = np.zeros(before, dtype=bool)
        admissible_overlap_masks = 0
        for bits in product((0, 1), repeat=2):
            chosen = [j for j, bit in zip(OVERLAP, bits) if bit]
            if i in chosen:
                continue
            needed = star_rhs[i].copy()
            for j in chosen:
                needed -= S[j]
            if any(k < 0 or k > 2 for k in needed):
                continue
            admissible_overlap_masks += 1
            lower = z[:, chosen].sum(axis=1) if chosen else np.zeros(before, dtype=np.int16)
            upper = lower.copy()
            for c, k in enumerate(needed):
                lower = lower+low[c][int(k)]
                upper = upper+high[c][int(k)]
            keep |= (lower <= target) & (target <= upper)
        survivors = survivors[keep]
        records.append(dict(row=i, label=LABELS[i], before=before,
                            rejected=before-len(survivors), after=len(survivors),
                            overlap_masks=admissible_overlap_masks))
    return survivors, records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference-pairs', type=int, nargs='+', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    start = time.monotonic()
    q = np.array([int(p[0] in (0, 1) and p[1]//2 in args.reference_pairs)
                  for p in LABELS], dtype=np.int16)
    vectors, counts = enumerate_vectors(args.reference_pairs)
    original_weights = dict(sorted(Counter(map(int, np.count_nonzero(vectors, axis=1))).items()))
    survivors, rows = filter_row_intervals(vectors, q)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    array_path = path.with_suffix('.npz')
    np.savez_compressed(array_path, u=survivors, q=q)
    report = dict(status='EXACT_FINITE_TERNARY_ENUMERATION_WITH_NECESSARY_ROW_FILTER',
                  reference_pairs=args.reference_pairs, counts=counts,
                  original_odd_weight_histogram=original_weights,
                  surviving_templates=len(survivors), row_filters=rows,
                  surviving_odd_weight_histogram=dict(sorted(Counter(map(int,
                      np.count_nonzero(survivors, axis=1))).items())),
                  survivors_file=str(array_path), elapsed_seconds=time.monotonic()-start,
                  all_coefficient_templates_covered_in_stated_family=True,
                  no_Gamma_family_exhaustion_claim=True,
                  global_binary_distance_not_used_to_discard_local_A_candidates=True,
                  scope='Only z=2q+u with ternary u in kerD and nonconstant tail. Passing the row test does not construct any graph.')
    path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status', 'counts', 'surviving_templates', 'elapsed_seconds')}))


if __name__ == '__main__':
    main()
