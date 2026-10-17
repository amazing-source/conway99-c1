"""Test extension of uncertified numerical seed candidates, without PSD audits.

Exact column elimination is needed to determine their possible extensions.
We do not certify their positivity or repeat a producer-excluded seed.
The filter is necessary regardless of whether numerical positivity was exact.
"""
import argparse
from collections import Counter
from hashlib import sha256
from math import lcm
from pathlib import Path
import json
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import three_star_column_domains as cd
from four_star_profile_join import boundary, residual


def extension_data(gamma):
    M = sp.Matrix(34, 34, lambda i, j: 24*int(i == j)-8*gamma[i][j]-cd.k8(cd.S[i], cd.S[j]))
    reduced, basis = M.rref()
    rank = len(basis)
    if rank > 30:
        return dict(rank=rank)
    kernels = []
    for j in range(34):
        if j not in basis:
            q = [sp.Integer(0)]*34
            q[j] = sp.Integer(1)
            for row, i in enumerate(basis):
                q[i] = -reduced[row, j]
            kernels.append(cd.primitive(q))
    inverse = M.extract(basis, basis).inv(method='DM')
    denominator = lcm(*(int(x.q) for x in inverse))
    numerator = [[int(x*denominator) for x in inverse.row(i)] for i in range(rank)]
    return dict(rank=rank, basis=basis, kernels=kernels, inverse=numerator, denominator=denominator,
                residual=residual(boundary(gamma, cd.S)))


def batch(input_path, folder, total_seconds, seconds_per_case, skip_indices):
    started = time.monotonic()
    raw = input_path.read_bytes()
    source = json.loads(raw)
    source_hash = sha256(raw).hexdigest()
    labels = tuple(tuple(p) for p in source['labels'])
    remap = [cd.INDEX[p] for p in labels]
    folder.mkdir(parents=True, exist_ok=True)
    (folder/'input_source_snapshot.json').write_bytes(raw)
    log_path = folder/'extension_results.jsonl'
    previous = []
    if log_path.exists():
        previous = [json.loads(line) for line in log_path.read_text(encoding='utf-8').splitlines() if line.strip()]
        if any(r['input_sha256'] != source_hash for r in previous):
            raise ValueError('Cannot resume a different input list.')
    records = {r['index']: r for r in previous}
    with log_path.open('a', encoding='utf-8') as log:
        for number, item in enumerate(source['structures']):
            if number in skip_indices or (number in records and records[number]['status'] != 'INCOMPLETE'):
                continue
            if time.monotonic()-started >= total_seconds:
                break
            begin = time.monotonic()
            gamma = [[0]*34 for _ in range(34)]
            for i, j in item['edges']:
                i, j = remap[i], remap[j]
                gamma[i][j] = gamma[j][i] = 1
            record = dict(index=number, input_sha256=source_hash, source=item.get('source'),
                          source_index=item.get('index'), seed_PSD_audited=False,
                          adjacency_sha256=sha256(bytes(x for row in gamma for x in row)).hexdigest())
            prepared = extension_data(gamma)
            record['extension_basis_rank'] = prepared['rank']
            if prepared['rank'] > 30:
                record.update(status='NO_COMPLETION', reason='Necessary spectral dimension exceeds30.')
            else:
                deadline = min(started+total_seconds, begin+seconds_per_case)
                column = cd.column_domain(gamma, prepared, cd.ProfileJoin(prepared['kernels']),
                                          (4, 6), deadline, keep_profiles=True)
                complete = column['complete']
                if complete and column['spectral_profiles'] == 0:
                    record.update(status='NO_COMPLETION', reason='Complete domain of label(4,6) is empty.')
                elif complete:
                    record['status'] = 'SURVIVES_FIRST_COLUMN'
                    bundle = dict(input_labels=cd.S, spectral_rank=prepared['rank'],
                                  spectral_basis=prepared['basis'], kernels=prepared['kernels'],
                                  inverse_numerator=prepared['inverse'], inverse_denominator=prepared['denominator'],
                                  columns=[column], seed_PSD_audited=False,
                                  input_seed_index=number, input_sha256=source_hash)
                    (folder/('survivor_%d_first_column.json'%number)).write_text(json.dumps(bundle)+'\n', encoding='utf-8')
                    (folder/('survivor_%d_seed.json'%number)).write_text(json.dumps(dict(labels=cd.S, gamma=gamma))+'\n', encoding='utf-8')
                else:
                    record['status'] = 'INCOMPLETE'
                column.pop('profiles', None)
                record['column'] = column
            record['seconds'] = time.monotonic()-begin
            records[number] = record
            log.write(json.dumps(record)+'\n')
            log.flush()
            print(json.dumps({k:record[k] for k in ('index', 'status', 'extension_basis_rank', 'seconds')}), flush=True)
    counts = Counter(r['status'] for r in records.values())
    pending = [i for i in range(len(source['structures'])) if i not in skip_indices
               and (i not in records or records[i]['status'] == 'INCOMPLETE')]
    complete_empty = [r for r in records.values() if r['status'] == 'NO_COMPLETION' and r.get('column')]
    report = dict(input_path=str(input_path), input_sha256=source_hash, input_count=len(source['structures']),
                  skipped_producer_excluded_indices=sorted(skip_indices), counts=dict(counts),
                  pending_indices=pending,
                  survivors=[i for i, r in records.items() if r['status'] == 'SURVIVES_FIRST_COLUMN'],
                  locally_admissible_profiles=sum(r['column']['cap_profiles'] for r in complete_empty),
                  kernel_profiles=sum(r['column']['kernel_profiles'] for r in complete_empty),
                  norm_comparisons={name:sum(r['column']['norm_comparison_counts'][name] for r in complete_empty)
                                    for name in ('below_20', 'equal_20', 'above_20')},
                  seconds_this_run=time.monotonic()-started, seed_PSD_audited=False,
                  scope='Necessary extension test for this supplied finite list; numerical PSD is not certified and no full graph is constructed.')
    (folder/'summary.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report), flush=True)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', required=True)
    p.add_argument('--folder', required=True)
    p.add_argument('--seconds', type=float, default=45)
    p.add_argument('--seconds-per-case', type=float, default=4)
    p.add_argument('--skip-indices', type=int, nargs='*', default=[])
    a = p.parse_args()
    if min(a.seconds, a.seconds_per_case) <= 0:
        p.error('Budgets must be positive.')
    batch(Path(a.input), Path(a.folder), a.seconds, a.seconds_per_case, set(a.skip_indices))


if __name__ == '__main__':
    main()
