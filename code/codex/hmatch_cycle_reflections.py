"""Construct new H-MATCH candidates by root-balanced orthogonal reflections.

For q alternating around an even cycle in the root-label graph, Bq=0.
R=I-2qq^t/(q^t q) fixes the geometric parts of T and U. A binary
R Gamma R therefore inherits both PSD certificates and both ranks.
Only changed combinatorial constraints are checked on newly built graphs.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from math import comb
from pathlib import Path
import time

import numpy as np

LABELS = [(a, b) for a, b in combinations(range(14), 2)
          if a < 4 and b != (a ^ 1)]
INDEX = {x: i for i, x in enumerate(LABELS)}
B = np.array([[int(r in p) for p in LABELS] for r in range(14)], dtype=np.int64)
H = [INDEX[tuple(sorted(x ^ 1 if x < 4 else x for x in p))] for p in LABELS]
ROOTS = [{b if a == r else a for a, b in LABELS if r in (a, b)} for r in range(14)]
ROOT_INTERSECTION = B.T @ B
CENTRAL_ROOT_INTERSECTION = B[:4].T @ B[:4]
ROOT_LIMIT = np.array([[2-int(r in p)-int((r ^ 1) in p) for r in range(14)]
                      for p in LABELS], dtype=np.int64)


def cycles(length):
    """All undirected simple root cycles of a given even length, once each."""
    for first in range(4):
        def extend(path, seen):
            last = path[-1]
            if len(path) == length:
                if first in ROOTS[last] and path[1] < last:
                    yield tuple(path)
                return
            for x in sorted(ROOTS[last]):
                if x > first and x not in seen:
                    yield from extend(path+[x], seen | {x})
        yield from extend([first], {first})


def root_vectors(length):
    supports, roots = [], []
    for cycle in cycles(length):
        supports.append([INDEX[tuple(sorted((a, b)))]
                         for a, b in zip(cycle, cycle[1:]+cycle[:1])])
        roots.append(cycle)
    support = np.array(supports, dtype=np.int64)
    vectors = np.zeros((44, len(support)), dtype=np.int64)
    vectors[support.T, np.arange(len(support))[None, :]] = np.array([1, -1]*(length//2))[:, None]
    assert not np.any(B@vectors)
    return roots, support, vectors


def load_graph(record):
    labels = [tuple(p) for p in record['labels']]
    if len(labels) != 44 or set(labels) != set(LABELS):
        raise ValueError('Expected the complete44-label geometry, not a smaller star block.')
    if 'gamma' in record:
        matrix = np.array(record['gamma'], dtype=np.int64)
    else:
        matrix = np.zeros((44, 44), dtype=np.int64)
        for i, j in record['edges']:
            matrix[i, j] = matrix[j, i] = 1
    order = [labels.index(p) for p in LABELS]
    return matrix[np.ix_(order, order)]


def new_candidate_checks(matrix):
    if not np.all((matrix == 0) | (matrix == 1)) or np.any(np.diag(matrix)):
        return 'NON_BINARY'
    counts = matrix@B.T
    if np.any(counts[:, :4] != ROOT_LIMIT[:, :4]):
        return 'C1'
    if np.any(counts[:, 4:] > ROOT_LIMIT[:, 4:]):
        return 'C1_PRIME'
    capacity = 2-matrix-ROOT_INTERSECTION-matrix@matrix
    np.fill_diagonal(capacity, 0)
    if np.any(capacity < 0):
        return 'C2'
    difference = matrix-matrix[np.ix_(H, H)]
    matching_break = np.count_nonzero(difference*(CENTRAL_ROOT_INTERSECTION > 0))
    return 'H_MATCH_BROKEN' if matching_break else 'H_MATCH_INTACT'


def same_incidence_subsets(multiplicities, allowed):
    """All allowed root-edge sets with exactly the supplied root degrees."""
    incident = [[] for _ in range(14)]
    for i in allowed:
        a, b = LABELS[i]
        incident[a].append((b, i))
        incident[b].append((a, i))

    def extend(remaining, selected):
        active = [a for a in range(14) if remaining[a]]
        if not active:
            yield tuple(sorted(selected))
            return
        options = {a: [(b, i) for b, i in incident[a] if remaining[b]] for a in active}
        if any(len(options[a]) < remaining[a] for a in active):
            return
        a = min(active, key=lambda r: comb(len(options[r]), remaining[r]))
        for chosen in combinations(options[a], remaining[a]):
            reduced = list(remaining)
            reduced[a] = 0
            for b, _ in chosen:
                reduced[b] -= 1
            if min(reduced) < 0:
                continue
            yield from extend(tuple(reduced), selected+[i for _, i in chosen])
    yield from extend(tuple(multiplicities), [])


def all_flat_reflections(matrix):
    """Enumerate ALL nontrivial root-fixing Householder binary conjugates.

    A zero diagonal forces (Gamma q)_i=lambda q_i on supp(q). If an
    outside row changes, its entry changes must be0,+/-1, forcing all
    nonzero |q_i| equal. Bq=0 gives equal sign sizes. An affected outside
    vertex sees every positive and no negative coordinate. Thus the loop
    over neighbour subsets and equal-incidence nonneighbour subsets is
    exhaustive, including nonsimple and disconnected root supports.
    """
    seen = set()
    stats = Counter()
    for outside in range(44):
        neighbours = list(map(int, np.flatnonzero(matrix[outside])))
        allowed = [i for i in range(44) if i != outside and not matrix[outside, i]]
        cached = {}
        for half in range(2, len(neighbours)+1):
            for positive in combinations(neighbours, half):
                stats['positive_neighbour_subsets'] += 1
                incidence = tuple(map(int, B[:, positive].sum(axis=1)))
                if incidence not in cached:
                    cached[incidence] = list(same_incidence_subsets(incidence, allowed))
                for negative in cached[incidence]:
                    key = tuple(sorted((positive, negative)))
                    if key in seen:
                        continue
                    seen.add(key)
                    stats['distinct_balanced_supports'] += 1
                    q = np.zeros(44, dtype=np.int64)
                    q[list(positive)] = 1
                    q[list(negative)] = -1
                    image = matrix@q
                    eigenvalue = int(image[positive[0]])
                    support = list(positive)+list(negative)
                    if not np.array_equal(image[support], eigenvalue*q[support]):
                        continue
                    stats['eigenvector_cores'] += 1
                    external = image.copy()
                    external[support] = 0
                    if np.any(external % half):
                        continue
                    stats['binary_reflections'] += 1
                    changes = external//half
                    switched = matrix-np.outer(q, changes)-np.outer(changes, q)
                    scaled_r = half*np.eye(44, dtype=np.int64)-np.outer(q, q)
                    assert np.array_equal(scaled_r@matrix@scaled_r, half*half*switched)
                    assert np.array_equal(B@scaled_r, half*B)
                    status = new_candidate_checks(switched)
                    stats[status] += 1
                    yield dict(status=status, q=q, matrix=switched, half=half,
                               witness_outside=outside)
    yield dict(statistics=dict(stats))


def run(source, lengths, output, all_flat=False):
    started = time.monotonic()
    records = json.loads(Path(source).read_text(encoding='utf-8'))
    if 'labels' in records:
        records = {Path(source).stem: records}
    prepared = {} if all_flat else {length: root_vectors(length) for length in lengths}
    counts, examples, hits = [], [], []
    for name, record in records.items():
        matrix = load_graph(record)
        if all_flat:
            for item in all_flat_reflections(matrix):
                if 'statistics' in item:
                    counts.append(dict(source=name, all_flat=True, **item['statistics']))
                    print(json.dumps(counts[-1]), flush=True)
                    continue
                if len(examples) < 6:
                    examples.append(dict(source=name, verdict=item['status'],
                                         support=int(np.count_nonzero(item['q']))))
                if item['status'] == 'H_MATCH_BROKEN':
                    target = Path(output).with_name(Path(output).stem+'_HIT_%d.json' % len(hits))
                    result = dict(source=name, source_file=str(source),
                        producer_certificates=record.get('certificates'),
                        labels=LABELS,
                        edges=[[i, j] for i, j in combinations(range(44), 2) if item['matrix'][i, j]],
                        reflection_vector=item['q'].tolist(), reflection_denominator=item['half'],
                        exact_T_U_congruence=True, combinatorial_verdict=item['status'])
                    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
                    hits.append(str(target))
            continue
        for length, (roots, supports, vectors) in prepared.items():
            half = length//2
            images = matrix@vectors
            columns = np.arange(vectors.shape[1])
            values = images[supports[:, 0], columns]
            eigen = np.all(images[supports.T, columns[None, :]] ==
                           values[None, :]*np.array([1, -1]*half)[:, None], axis=0)
            external = images.copy()
            external[supports.T, columns[None, :]] = 0
            binary = np.all(external % half == 0, axis=0)
            active = np.any(external, axis=0)
            candidates = np.flatnonzero(eigen & binary & active)
            statuses = Counter()
            for column in candidates:
                q = vectors[:, column]
                changes = external[:, column]//half
                switched = matrix-np.outer(q, changes)-np.outer(changes, q)
                # Exact congruence identity, on the NEW transformed adjacency.
                scaled_r = half*np.eye(44, dtype=np.int64)-np.outer(q, q)
                assert np.array_equal(scaled_r@matrix@scaled_r, half*half*switched)
                assert np.array_equal(B@scaled_r, half*B)
                status = new_candidate_checks(switched)
                statuses[status] += 1
                if len(examples) < 6:
                    examples.append(dict(source=name, root_cycle=roots[column], verdict=status))
                if status == 'H_MATCH_BROKEN':
                    target = Path(output).with_name(Path(output).stem+'_HIT_%d.json' % len(hits))
                    result = dict(source=name, source_file=str(source),
                        producer_certificates=record.get('certificates'),
                        labels=LABELS, edges=[[i, j] for i, j in combinations(range(44), 2) if switched[i, j]],
                        reflection_vector=q.tolist(), reflection_denominator=half,
                        exact_T_U_congruence=True, combinatorial_verdict=status,
                        scope='New block; PSD and ranks inherited from the cited producer via the exact orthogonal conjugation.')
                    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
                    hits.append(str(target))
            counts.append(dict(source=name, length=length, root_cycles=len(roots),
                eigenvector_core=int(eigen.sum()), binary_reflections=int((eigen & binary).sum()),
                inactive_reflections=int((eigen & binary & ~active).sum()),
                new_binary_reflections=len(candidates), verdicts=dict(statuses)))
            print(json.dumps(counts[-1]), flush=True)
    result = dict(status=('HMATCH_CANDIDATE_FOUND' if hits else 'NO_HMATCH_COUNTEREXAMPLE_IN_TESTED_REFLECTION_FAMILY'), counts=counts,
        examples=examples, hits=hits, seconds=time.monotonic()-started,
        scope='A finite constructive experiment on the supplied seeds. No source ranks/PSD re-audited; no universal H-MATCH conclusion.')
    Path(output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--lengths', type=int, nargs='+', default=[4, 6, 8])
    parser.add_argument('--output', required=True)
    parser.add_argument('--all-flat', action='store_true')
    args = parser.parse_args()
    if any(n not in (4, 6, 8) for n in args.lengths):
        parser.error('Use the bounded simple-cycle lengths4,6,8.')
    run(args.source, args.lengths, args.output, args.all_flat)
