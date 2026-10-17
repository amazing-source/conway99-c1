"""Change outer mates of an accepted broken-matching graph, seeking nullity14.

The producer's original graph is not re-audited. Binary adjacency, C1, C2,
and the matching break survive unchanged; only C1-prime and the Gram forms
change. A nonzero minor modulo101 excludes rank<=30 exactly. Remaining
new forms receive exact integer PSD/rank elimination.
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
from hmatch_cycle_reflections import B, H, INDEX, LABELS, ROOT_INTERSECTION, load_graph
from odd9_endpoint_mate_family import exact_psd, matchings


def rank_at_least(matrix, threshold=31, prime=101):
    work = np.array(matrix, dtype=np.int64) % prime
    rank = 0
    for column in range(work.shape[1]):
        candidates = np.flatnonzero(work[rank:, column])
        if not len(candidates):
            continue
        pivot = rank+int(candidates[0])
        work[[rank, pivot]] = work[[pivot, rank]]
        work[rank] = work[rank]*pow(int(work[rank, column]), -1, prime) % prime
        factors = work[rank+1:, column].copy()
        work[rank+1:] = (work[rank+1:]-factors[:, None]*work[rank]) % prime
        rank += 1
        if rank >= threshold:
            return rank
    return rank


def run(source, output):
    started = time.monotonic()
    record = json.loads(Path(source).read_text(encoding='utf-8'))
    matrix = load_graph(record)
    breaks = int(np.count_nonzero((matrix-matrix[np.ix_(H, H)])*(ROOT_INTERSECTION > 0)))
    if not breaks:
        raise ValueError('The source must already have broken star matchings.')
    counts = matrix@B.T
    Tbase = 24*np.eye(44, dtype=np.int64)-8*matrix-3*ROOT_INTERSECTION+2
    Ubase = 60*np.eye(44, dtype=np.int64)+15*matrix-4*ROOT_INTERSECTION-2
    statuses, details, hits = Counter(), [], []
    for number, pairs in enumerate(matchings(list(range(4, 14)))):
        mate = list(range(14))
        mate[:4] = [1, 0, 3, 2]
        for a, b in pairs:
            mate[a], mate[b] = b, a
        if all(mate[r] == (r ^ 1) for r in range(14)):
            statuses['ORIGINAL_PRODUCER_ASSIGNMENT_NOT_RETESTED'] += 1
            continue
        limits = 2-B.T-B[mate, :].T
        if np.any(counts[:, 4:] > limits[:, 4:]):
            statuses['C1_PRIME_VIOLATION'] += 1
            continue
        mate_gram = B.T@B[mate, :]
        T8, U15 = Tbase-mate_gram, Ubase+mate_gram
        lower = rank_at_least(T8)
        if lower >= 31:
            statuses['T_RANK_AT_LEAST_31_MOD_101'] += 1
            details.append(dict(pairs=pairs, verdict='RANK_AT_LEAST_31', modular_prime=101))
            continue
        t_psd, t_rank, t_reason = exact_psd(T8)
        if not t_psd:
            statuses['T_NOT_PSD_EXACT'] += 1
            details.append(dict(pairs=pairs, verdict='T_NOT_PSD', reason=t_reason))
            continue
        if t_rank > 30:
            statuses['T_RANK_ABOVE_30_EXACT'] += 1
            details.append(dict(pairs=pairs, verdict='T_RANK_ABOVE_30', rank=t_rank))
            continue
        u_psd, u_rank, u_reason = exact_psd(U15)
        if not u_psd:
            statuses['U_NOT_PSD_EXACT'] += 1
            details.append(dict(pairs=pairs, verdict='U_NOT_PSD', rank_T=t_rank, reason=u_reason))
            continue
        statuses['HMATCH_COUNTEREXAMPLE_EXACT'] += 1
        relabel = list(range(14))
        for i, (a, b) in enumerate(pairs):
            relabel[a], relabel[b] = 4+2*i, 5+2*i
        permutation = [INDEX[tuple(sorted(relabel[a] for a in p))] for p in LABELS]
        canonical = np.zeros((44, 44), dtype=np.int64)
        canonical[np.ix_(permutation, permutation)] = matrix
        target = Path(output).with_name(Path(output).stem+'_HIT_%d.json' % len(hits))
        candidate = dict(source_file=str(source), changed_outer_mates=pairs,
            labels=LABELS, edges=[[i, j] for i, j in combinations(range(44), 2) if canonical[i, j]],
            exact_certificates=dict(T_PSD=True, rank_T=t_rank, nullity_T=44-t_rank,
                                    U_PSD=True, rank_U=u_rank),
            combinatorics='C1/C2/binary/matching break inherited by relabelling; changed C1-prime checked exactly.')
        target.write_text(json.dumps(candidate, indent=2)+'\n', encoding='utf-8')
        hits.append(str(target))
        details.append(dict(pairs=pairs, verdict='EXACT_COUNTEREXAMPLE', file=str(target)))
    assert sum(statuses.values()) == 945
    result = dict(status='EXACT_OUTER_MATE_FAMILY', source=str(source),
        broken_matching_matrix_entries=breaks, assignments=945,
        statuses=dict(statuses), hits=hits, details=details,
        seconds=time.monotonic()-started,
        scope='All944 changed outer mate assignments of this fixed accepted adjacency; the producer assignment is not re-audited. No universal H-MATCH conclusion when no hit is found.')
    Path(output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'statuses', 'hits', 'seconds')}), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    run(args.source, args.output)
