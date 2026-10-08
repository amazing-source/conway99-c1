"""Exact depth-one two-star proofs, with a trace for every candidate.

Each leaf starts from the SAME base domains and fixes one candidate of
the SAME pivot. No deletion from another leaf is inherited. Verification
uses original candidate indices, not the producer's restricted tables.
The input pools and common-apex filters retain their usual hypotheses.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from generic_star_apex_audit import cyclic_ball
from joint_generic_stars import prepare
from joint_star_propagation import propagate
from two_star_core_ablation import filtered_system


def restrict(system, domains):
    common, labels, arrays, sides, targets, compat = system
    return (common, labels, [a[d] for a, d in zip(arrays, domains)], sides, targets,
            {(i, j): table[np.ix_(domains[i], domains[j])]
             for (i, j), table in compat.items()})


def replay_original(system, result, domains):
    """Verify supplied reasons in the original tables; do not call propagate.

    Trace indices are local to domains. Map them back before checking each
    integer sum bound or pair support. This also audits restriction indexing.
    """
    _, _, arrays, sides, targets, compat = system
    assert len(domains) == len(arrays) == 18
    maps = []
    for a, d in zip(arrays, domains):
        assert d == sorted(set(d)) and all(type(c) is int and 0 <= c < len(a) for c in d)
        maps.append(np.array(d, dtype=np.int64))
    alive = [np.ones(len(d), dtype=bool) for d in domains]

    def live(i):
        return maps[i][alive[i]]

    def bounds(indices, point):
        assert all(alive[j].any() for j in indices)
        return (sum(int(arrays[j][live(j), point].min()) for j in indices),
                sum(int(arrays[j][live(j), point].max()) for j in indices))

    for event in result['trace']:
        i, removed = event['variable'], event['removed']
        assert type(i) is int and 0 <= i < 18 and removed
        assert len(removed) == len(set(removed))
        assert all(type(c) is int and 0 <= c < len(maps[i]) and alive[i][c] for c in removed)
        candidates = maps[i][removed]
        if event['kind'] == 'pair_support':
            j = event['other_variable']
            assert type(j) is int and 0 <= j < 18 and j != i
            assert not compat[i, j][np.ix_(candidates, live(j))].any()
        elif event['kind'] == 'sum_support':
            s, p = event['side'], event['point']
            assert s in (0, 1) and i in sides[s] and type(p) is int and 0 <= p < 36
            low, high = bounds([j for j in sides[s] if j != i], p)
            residual = int(targets[s][p])-arrays[i][candidates, p]
            assert np.all((residual < low) | (residual > high))
        else:
            raise AssertionError('unknown deletion reason')
        alive[i][removed] = False
    reason = result['contradiction']
    if reason is not None:
        if reason['kind'] == 'empty_domain':
            i = reason['variable']
            assert type(i) is int and 0 <= i < 18 and not alive[i].any()
        elif reason['kind'] == 'sum_outside_bounds':
            s, p = reason['side'], reason['point']
            assert s in (0, 1) and type(p) is int and 0 <= p < 36
            low, high = bounds(sides[s], p)
            target = int(targets[s][p])
            assert (low, high, target) == (reason['minimum'], reason['maximum'], reason['target'])
            assert target < low or target > high
        else:
            raise AssertionError('unknown terminal reason')
    assert [int(a.sum()) for a in alive] == result['remaining_domain_sizes']
    assert dict(Counter(e['kind'] for e in result['trace'])) == result['deletion_counts']
    return [live(i).tolist() for i in range(18)]


def branch_proof(system, apex):
    domains = [list(range(len(a))) for a in system[2]]
    base = propagate(system)
    kept = replay_original(system, base, domains)
    record = {'apex_index': apex, 'common_apex_support': list(system[0]),
              'base_propagation': base, 'pivot': None, 'leaves': []}
    if base['contradiction'] is not None:
        return record
    pivot = min(range(18), key=lambda i: len(kept[i]))
    record['pivot'] = pivot
    for candidate in kept[pivot]:
        trial = [d if i != pivot else [candidate] for i, d in enumerate(kept)]
        result = propagate(restrict(system, trial))
        # Every leaf is checked, including contradicting leaves.
        replay_original(system, result, trial)
        record['leaves'].append({'candidate': candidate, 'propagation': result})
    return record


def verify_branch(system, record):
    assert record['common_apex_support'] == list(system[0])
    domains = [list(range(len(a))) for a in system[2]]
    kept = replay_original(system, record['base_propagation'], domains)
    if record['base_propagation']['contradiction'] is not None:
        assert record['pivot'] is None and not record['leaves']
        return 'plain_propagation', 0
    pivot = record['pivot']
    assert type(pivot) is int and 0 <= pivot < 18
    assert pivot == min(range(18), key=lambda i: len(kept[i]))
    # Exhaustivity, uniqueness, and ordering are checked explicitly.
    assert [leaf['candidate'] for leaf in record['leaves']] == kept[pivot]
    excluded = True
    for leaf in record['leaves']:
        trial = [d if i != pivot else [leaf['candidate']] for i, d in enumerate(kept)]
        replay_original(system, leaf['propagation'], trial)
        excluded &= leaf['propagation']['contradiction'] is not None
    return ('single_choice' if excluded else 'survives'), len(record['leaves'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ball', type=Path)
    parser.add_argument('--u', type=int, default=0)
    parser.add_argument('--v', type=int, default=12)
    parser.add_argument('--peer-report', type=Path)
    parser.add_argument('--max-apex', type=int, default=0)
    parser.add_argument('--seconds', type=float, default=900)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    started = time.monotonic()
    peer = json.loads(args.peer_report.read_text(encoding='utf-8')) if args.peer_report else None
    if args.verify_only:
        report = json.loads(args.out.read_text(encoding='utf-8'))
        assert report['pair_mode'] == 'green' and report['format_version'] == 1
        g, (u, v) = report['adjacency'], report['centers']
        proof_path = args.out.parent/report['proof_file']
        assert hashlib.sha256(proof_path.read_bytes()).hexdigest() == report['proof_sha256']
    else:
        g = json.loads(args.ball.read_text(encoding='utf-8'))['adjacency'] if args.ball else cyclic_ball()
        u, v = args.u, args.v
        proof_path = args.out.with_suffix('.proofs.jsonl.gz')
    prepared = prepare(g, u, v)
    count = len(prepared[6])
    processed, classified, leaves, sizes = [], Counter(), 0, []

    def process(record, system, verified=False):
        nonlocal leaves
        index = record['apex_index']
        if verified:
            category, nleaves = verify_branch(system, record)
        else:
            # branch_proof has already independently replayed every trace.
            category = ('plain_propagation' if record['base_propagation']['contradiction'] is not None else
                        'single_choice' if all(x['propagation']['contradiction'] is not None for x in record['leaves']) else 'survives')
            nleaves = len(record['leaves'])
        if peer is not None:
            old = peer['branches'][str(index)]
            assert old['mode'] == 'green' and old['common_apex_support'] == list(system[0])
            assert old['domain_sizes_after_plain_propagation'] == record['base_propagation']['remaining_domain_sizes']
            assert old['deletions'] == [[record['pivot'], x['candidate']] for x in record['leaves']]
            assert old['rounds'] == 1 and old['status'].startswith('EXCLUDED: empty domain')
            assert category == 'single_choice'
        processed.append(index)
        classified[category] += 1
        leaves += nleaves
        if nleaves:
            sizes.append(nleaves)
        if len(processed) % 25 == 0:
            print(json.dumps({'processed': len(processed), 'classified': dict(classified),
                              'leaves': leaves, 'seconds': round(time.monotonic()-started, 1)}), flush=True)

    if args.verify_only:
        requested = report['processed_indices']
        assert requested == sorted(set(requested)) and all(0 <= i < count for i in requested)
        with gzip.open(proof_path, 'rt', encoding='utf-8') as stream:
            for index, line in zip(requested, stream, strict=True):
                record = json.loads(line)
                assert record['apex_index'] == index
                process(record, filtered_system(prepared, u, v, index, 'green'), verified=True)
        assert report['apex_candidates'] == count
        assert report['classifications'] == dict(classified)
        assert report['propagation_leaves'] == leaves
    else:
        end = count if args.max_apex == 0 else min(count, args.max_apex)
        with gzip.open(proof_path, 'wt', encoding='utf-8') as stream:
            for index in range(end):
                if time.monotonic()-started >= args.seconds:
                    break
                system = filtered_system(prepared, u, v, index, 'green')
                record = branch_proof(system, index)
                process(record, system)
                stream.write(json.dumps(record, separators=(',', ':'))+'\n')
        report = {'format_version': 1, 'adjacency': np.asarray(g).tolist(), 'centers': [u, v],
                  'pair_mode': 'green', 'apex_candidates': count, 'processed_indices': processed,
                  'classifications': dict(classified), 'propagation_leaves': leaves,
                  'pivot_size_min_mean_max': [min(sizes), sum(sizes)/len(sizes), max(sizes)] if sizes else None,
                  'proof_file': proof_path.name, 'proof_sha256': hashlib.sha256(proof_path.read_bytes()).hexdigest(),
                  'production_seconds': time.monotonic()-started,
                  'scope': 'one edge of one input ball; historical unary/apex filters retained; no uniform or rank exclusion'}
        if peer is not None:
            report['peer_source'] = {k: peer[k] for k in ('source_commit', 'source_files')}
            report['peer_deletion_lists_matched'] = len(processed)
    complete = processed == list(range(count))
    conclusion = 'ALL_APEX_BRANCHES_EXCLUDED_AT_DEPTH_ONE' if complete and not classified['survives'] else 'PARTIAL_OR_UNRESOLVED'
    if args.verify_only:
        assert report['conclusion'] == conclusion
    else:
        report['conclusion'] = conclusion
        args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'verified_replay': args.verify_only, 'conclusion': conclusion, 'processed': len(processed),
                      'classified': dict(classified), 'leaves': leaves, 'seconds': round(time.monotonic()-started, 2)}), flush=True)


if __name__ == '__main__':
    main()
