"""Exact first-column completion filter on a producer-certified grid batch.

Input rank30 and PSD certifications for T and 7Pi-T are consumed, not
repeated. This processes a finite supplied list, not all possible Z5 cases.
"""
import argparse
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import three_star_column_domains as domains


def batch(input_file, output_folder, seconds_per_column):
    started = time.perf_counter()
    raw = Path(input_file).read_bytes()
    data = json.loads(raw)
    labels = [tuple(sorted(p)) for p in data['labels']]
    if len(labels) != 34 or set(labels) != set(domains.S):
        raise ValueError('Expected the34 three-star labels, centres0,1,2 and mates i xor1.')
    index = {p:i for i, p in enumerate(domains.S)}
    remap = [index[p] for p in labels]
    output_folder.mkdir(parents=True, exist_ok=True)
    (output_folder/'input_source_snapshot.json').write_bytes(raw)
    records = []
    counts = Counter()
    distinct = set()
    with (output_folder/'column_results.jsonl').open('w', encoding='utf-8') as log:
        for number, item in enumerate(data['structures']):
            try:
                if item['rank'] != 30:
                    raise ValueError('Producer rank30 precondition not declared.')
                gamma = [[0]*34 for _ in range(34)]
                for a, b in item['edges']:
                    if a not in range(34) or b not in range(34) or a == b:
                        raise ValueError('Invalid edge index.')
                    a, b = remap[a], remap[b]
                    gamma[a][b] = gamma[b][a] = 1
                code = sha256(bytes(x for row in gamma for x in row)).hexdigest()
                distinct.add(code)
                result = domains.analyse(gamma, seconds=seconds_per_column,
                                         label_indices=[0], producer_certified_grid_rank30=True)
                columns = result.get('columns', [])
                excluded = result['status'] == 'NO_COMPLETION'
                complete = bool(columns and columns[0]['complete'])
                status = ('EXCLUDED' if excluded else 'SURVIVES_FIRST_COLUMN' if complete
                          else 'INCOMPLETE')
                record = dict(index=number, status=status, adjacency_sha256=code,
                              reason=result.get('reason'), columns=columns,
                              elapsed_seconds=result['seconds'],
                              spectral_properties_source=result.get('spectral_properties_source'))
            except Exception as error:
                record = dict(index=number, status='ERROR', error=f'{type(error).__name__}: {error}')
            counts[record['status']] += 1
            records.append(record)
            log.write(json.dumps(record)+'\n')
            log.flush()
            if (number+1) % 64 == 0 or number+1 == len(data['structures']):
                print(json.dumps(dict(processed=number+1, total=len(data['structures']),
                                      counts=dict(counts), seconds=time.perf_counter()-started)), flush=True)
    complete_empty = [r for r in records if r['status'] == 'EXCLUDED' and r.get('columns')
                      and r['columns'][0]['complete'] and r['columns'][0]['spectral_profiles'] == 0]
    cap_counts = [r['columns'][0]['cap_profiles'] for r in complete_empty]
    comparisons = Counter()
    for record in complete_empty:
        comparisons.update(record['columns'][0]['norm_comparison_counts'])
    summary = dict(
        status='ALL_SUPPLIED_BOUNDARIES_EXCLUDED' if counts['EXCLUDED'] == len(records)
               else 'BATCH_FINISHED_WITH_REMAINING_CASES',
        input_path=str(input_file), input_sha256=sha256(raw).hexdigest(),
        producer_description=data.get('description'), structures=len(records),
        distinct_labelled_adjacencies=len(distinct), counts=dict(counts),
        tested_column=list(domains.U[0]),
        complete_empty_first_column_domains=len(complete_empty),
        total_locally_admissible_profiles=sum(cap_counts),
        local_profile_count_range=[min(cap_counts), max(cap_counts)] if cap_counts else None,
        total_norm_comparisons=dict(comparisons),
        surviving_indices=[r['index'] for r in records if r['status'] != 'EXCLUDED'],
        elapsed_seconds=time.perf_counter()-started,
        spectral_certification_source='Producer: both Grams PSD, exact rank30, fixed grid. No repeated rank/PSD audit.',
        scope=[
            'This is the supplied finite batch, selected from the first10000 structures examined by the producer.',
            'No exhaustive classification of all Z5 three-star structures is claimed.',
            'No symmetry is assumed for a completion; each labelled boundary is excluded in any Conway graph.',
            'No claim that the inputs are pairwise nonisomorphic is made.',
            'A surviving first-column domain would be necessary only, not a completed graph.'
        ])
    (output_folder/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output-folder', required=True)
    parser.add_argument('--seconds-per-column', type=float, default=5)
    args = parser.parse_args()
    if args.seconds_per_column <= 0:
        parser.error('--seconds-per-column must be positive.')
    result = batch(Path(args.input), Path(args.output_folder), args.seconds_per_column)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
