"""Thirteen exact pilot proofs after removing all cross-star pair constraints.

The chosen pivots are explicit; three differ from the smallest-domain pivot.
This is a finite ablation, not an exhaustive sweep of the four input balls.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

from joint_generic_stars import prepare
from joint_star_propagation import propagate
from two_star_core_ablation import filtered_system
from two_star_single_choice import restrict, replay_original


CASES = {'ball5': [(0, 8), (33, 10)], 'ball9': [(0, 3), (33, 3)],
         'ball12': [(0, 12), (33, 11), (113, 4), (137, 17), (184, 13)],
         'cyclic241': [(0, 9), (33, 12), (53, 6), (100, 11)]}


def check(system, record):
    arrays, labels = system[2], system[1]
    kept = replay_original(system, record['base'], [list(range(len(a))) for a in arrays])
    assert record['base']['contradiction'] is None
    # Even the base deletions cannot depend on the opposite star.
    for event in record['base']['trace']:
        if event['kind'] == 'pair_support':
            assert labels[event['variable']][0] == labels[event['other_variable']][0]
    pivot = record['pivot']
    assert 0 <= pivot < 18
    assert [leaf['candidate'] for leaf in record['leaves']] == kept[pivot]
    for leaf in record['leaves']:
        trial = [d if i != pivot else [leaf['candidate']] for i, d in enumerate(kept)]
        result = leaf['propagation']
        replay_original(system, result, trial)
        reason = result['contradiction']
        assert reason is not None
        side = labels[pivot][0]
        assert all(labels[e['variable']][0] == side for e in result['trace'])
        if reason['kind'] == 'empty_domain':
            assert labels[reason['variable']][0] == side
        else:
            assert reason['kind'] == 'sum_outside_bounds' and reason['side'] == side


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=Path('data'))
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    proof_path = args.out.with_suffix('.proofs.jsonl.gz')
    old, stream = None, None
    if args.verify_only:
        old = json.loads(args.out.read_text(encoding='utf-8'))
        assert old['proof_sha256'] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
        stream = gzip.open(proof_path, 'rt', encoding='utf-8')
    else:
        stream = gzip.open(proof_path, 'wt', encoding='utf-8')
    reports = []
    with stream:
        for ball, cases in CASES.items():
            source = json.loads((args.data_dir/('codex_single_choice_'+ball+'.json')).read_text(encoding='utf-8'))
            prepared = prepare(source['adjacency'], 0, 12)
            for apex, pivot in cases:
                system = list(filtered_system(prepared, 0, 12, apex, 'green'))
                labels = system[1]
                system[-1] = {ij: table if labels[ij[0]][0] == labels[ij[1]][0] else np.ones_like(table)
                              for ij, table in system[-1].items()}
                if args.verify_only:
                    record = json.loads(next(stream))
                    assert (record['ball'], record['apex'], record['pivot']) == (ball, apex, pivot)
                else:
                    base = propagate(system)
                    kept = replay_original(system, base, [list(range(len(a))) for a in system[2]])
                    record = {'ball': ball, 'apex': apex, 'pivot': pivot, 'base': base, 'leaves': []}
                    for candidate in kept[pivot]:
                        trial = [d if i != pivot else [candidate] for i, d in enumerate(kept)]
                        result = propagate(restrict(system, trial))
                        record['leaves'].append({'candidate': candidate, 'propagation': result})
                check(system, record)
                if not args.verify_only:
                    stream.write(json.dumps(record, separators=(',', ':'))+'\n')
                reports.append({'ball': ball, 'apex': apex, 'pivot': pivot, 'leaves': len(record['leaves'])})
        if args.verify_only:
            assert next(stream, None) is None
    report = {'cases': reports, 'leaves': sum(r['leaves'] for r in reports), 'proof_file': proof_path.name,
              'proof_sha256': hashlib.sha256(proof_path.read_bytes()).hexdigest(),
              'scope': '13 pilot branches, one conditioned star suffices; not full-ball exclusions'}
    if args.verify_only:
        assert report == old
    else:
        args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
