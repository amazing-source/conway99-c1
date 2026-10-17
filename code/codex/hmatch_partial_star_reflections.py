"""Construct exact rank-preserving partial swaps of a mate pair of stars.

If u is +1 on selected labels(a,y), -1 on their(b,y) partners, Gamma*u=lambda*u,
and F swaps these label pairs, R=F+u*u^t/m is orthogonal and fixes B.
Thus R*Gamma*R=F*Gamma*F preserves both Gram spectra by congruence.
The search enumerates only subsets; no seed PSD/rank is recomputed.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
import time

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hmatch_cycle_reflections import B, INDEX, LABELS, ROOTS, load_graph, new_candidate_checks


def run(source, output):
    started = time.monotonic()
    records = json.loads(Path(source).read_text(encoding='utf-8'))
    if 'labels' in records:
        records = {Path(source).stem: records}
    reports, hits = [], []
    for name, record in records.items():
        matrix = load_graph(record)
        for a, b in [(0, 1), (2, 3)]+list(combinations(range(4, 14), 2)):
            letters = sorted(ROOTS[a] & ROOTS[b])
            left = [INDEX[tuple(sorted((a, r)))] for r in letters]
            right = [INDEX[tuple(sorted((b, r)))] for r in letters]
            columns = np.eye(44, dtype=np.int64)[:, left]-np.eye(44, dtype=np.int64)[:, right]
            image = matrix@columns
            stats = Counter()
            for half in range(3, len(letters)+1):
                for selected in combinations(range(len(letters)), half):
                    stats['subsets'] += 1
                    u = columns[:, selected].sum(axis=1)
                    changed = image[:, selected].sum(axis=1)
                    eigenvalue = int(changed[left[selected[0]]])
                    if not np.array_equal(changed, eigenvalue*u):
                        continue
                    stats['adjacency_eigenmodes'] += 1
                    permutation = list(range(44))
                    for j in selected:
                        permutation[left[j]], permutation[right[j]] = right[j], left[j]
                    switched = matrix[np.ix_(permutation, permutation)]
                    if np.array_equal(switched, matrix):
                        stats['unchanged'] += 1
                        continue
                    scaled_r = half*np.eye(44, dtype=np.int64)[permutation, :]+np.outer(u, u)
                    assert np.array_equal(scaled_r@scaled_r, half*half*np.eye(44, dtype=np.int64))
                    assert np.array_equal(B@scaled_r, half*B)
                    assert np.array_equal(scaled_r@matrix@scaled_r, half*half*switched)
                    status = new_candidate_checks(switched)
                    stats[status] += 1
                    if status == 'H_MATCH_BROKEN':
                        target = Path(output).with_name(Path(output).stem+'_HIT_%d.json' % len(hits))
                        result = dict(source=name, source_file=str(source),
                            producer_certificates=record.get('certificates'),
                            labels=LABELS,
                            edges=[[i, j] for i, j in combinations(range(44), 2) if switched[i, j]],
                            partial_star_swap=dict(stars=[a, b], letters=[letters[j] for j in selected]),
                            exact_T_U_congruence=True, combinatorial_verdict=status)
                        target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
                        hits.append(str(target))
            reports.append(dict(source=name, stars=[a, b], **dict(stats)))
            if a < 4 or stats.get('adjacency_eigenmodes'):
                print(json.dumps(reports[-1]), flush=True)
    result = dict(status='EXACT_PARTIAL_STAR_REFLECTION_CONSTRUCTIONS', reports=reports,
                  hits=hits, seconds=time.monotonic()-started,
                  scope='Only this transformation family and the cited seeds; no universal H-MATCH conclusion.')
    Path(output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    run(args.source, args.output)
