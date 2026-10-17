"""Bounded linear scan of a complete or partial coefficient enumeration.

Exact Farkas certificates store references to the reproducible inequality
rows instead of duplicating all their coefficients. Passing a relaxation
does not construct a graph. This script reads no peer graph.
"""
import argparse
from collections import Counter
from pathlib import Path
import json
import sys
import time

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_prescribed_kernel import linear_constraints, lp_probe, linear_certificate


def compact_certificate(q, full, extra_rows=(), connected_Q=False):
    if full['status'] != 'EXACT_NONNEGATIVE_LINEAR_COMBINATION_CONTRADICTION':
        return full
    source = list(linear_constraints(q, connected_Q=connected_Q))+list(extra_rows)
    terms = []
    combined = Counter()
    total = 0
    for term in full['terms']:
        number = term['row_number']
        if number is None:
            assert len(term['coefficients']) == 1
            i, j, a = term['coefficients'][0]
            row, rhs = {(i, j):a}, term['rhs']
            compact = dict(edge=[i, j], coefficient=a, rhs=rhs)
        else:
            row, lower, upper, origin = source[number]
            expanded = {(i, j):a for i, j, a in term['coefficients']}
            if expanded == row:
                assert upper == term['rhs']
                rhs, sign = upper, 1
            else:
                assert expanded == {e:-a for e, a in row.items()}
                assert -lower == term['rhs']
                row, rhs, sign = expanded, -lower, -1
            compact = dict(row_number=number, sign=sign)
        compact['multiplier'] = term['multiplier']
        terms.append(compact)
        for e, a in row.items():
            combined[e] += term['multiplier']*a
        total += term['multiplier']*rhs
    assert not any(combined.values()) and total == full['combined_rhs'] < 0
    return dict(status=full['status'], combined_rhs=total, terms=terms,
                schema='row_number refers to list(linear_constraints(q, connected_Q=...)) followed by the recorded extra rows; sign=1 takes the upper inequality, -1 the negated lower inequality. Edge rows are explicit. Multipliers are nonnegative integers.',
                connected_Q=connected_Q, extra_row_count=len(extra_rows),
                expanded_integer_combination_checked=True)


def scan(path, seconds):
    start = time.monotonic()
    source = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    records = []
    candidates = [(i, row) for i, row in enumerate(source['profiles']) if row['impossible_row'] is None]
    for i, row in candidates:
        if time.monotonic()-start >= seconds:
            break
        q = np.array(row['q'], dtype=np.int64)
        lp = lp_probe(list(linear_constraints(q, connected_Q=True)))
        record = dict(profile_index=i, q=row['q'], lp=lp)
        if lp['status'] == 2:
            record['certificate'] = compact_certificate(q, linear_certificate(q))
        records.append(record)
        if len(records) % 100 == 0:
            print(json.dumps(dict(processed=len(records), elapsed=time.monotonic()-start)), flush=True)
    return dict(source=str(path), source_enumeration_complete=source['complete'],
                source_profiles=source['normalized_profiles'], row_domain_survivors=len(candidates),
                processed=len(records), complete=len(records) == len(candidates),
                lp_status_counts=dict(Counter(row['lp']['status'] for row in records)),
                exact_exclusions=sum(row.get('certificate', {}).get('status') ==
                    'EXACT_NONNEGATIVE_LINEAR_COMBINATION_CONTRADICTION' for row in records),
                records=records, elapsed_seconds=time.monotonic()-start,
                graph_not_constructed=True,
                scope='Only the stated nonnegative normalized coefficient weight. Numerical infeasibility without an exact certificate is not counted as an exact exclusion.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--seconds', type=float, default=40)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    report = scan(args.input, args.seconds)
    Path(args.output).write_text(json.dumps(report, separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps({k:v for k, v in report.items() if k != 'records'}), flush=True)


if __name__ == '__main__':
    main()
