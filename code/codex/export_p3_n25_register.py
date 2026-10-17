"""Export stable support IDs and explicit edges for the peer's integer search.

This transports existing data; it does not rerun the mathematical search.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import shutil

from p3_n25_saturated import ROOT, adjacency


def write_jsonl(path, records):
    text = ''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in records)
    path.write_bytes(text.encode('utf-8'))
    return {'path': path.name, 'records': len(records), 'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    original = json.loads((ROOT / 'data/codex_p3_n25_open_triangles.json').read_text())
    local = json.loads((ROOT / 'data/codex_p3_n25_local_matching.json').read_text())
    retained = {r['id'] for r in local['retained']}
    local_excluded = {r['id'] for r in local['excluded']}
    all_records = []
    for row in original['supports']:
        a = adjacency(row)
        edges = [[i, j] for i, j in combinations(range(28), 2) if a[i][j]]
        labels = [sum(a[v][p] << p for p in range(3)) for v in range(3, 28)]
        if row['id'] in retained:
            status = 'open'
        elif row['status'] == 'excluded_exact_spectral':
            status = 'excluded_spectral'
        elif row['outside_N_triangles'] == 2:
            status = 'excluded_delta2'
        elif row['id'] in local_excluded:
            status = 'excluded_local_matching'
        else:
            raise ValueError('Unclassified support')
        assert len(edges) == 36 and len(set(map(tuple, edges))) == 36
        # Transport check: edges and label masks must reconstruct the same graph.
        rebuilt = [[0] * 28 for _ in range(28)]
        for i, j in edges:
            rebuilt[i][j] = rebuilt[j][i] = 1
        assert rebuilt == a
        assert all(labels[v - 3] == sum((1 << p) for p in range(3) if rebuilt[v][p])
                   for v in range(3, 28))
        all_records.append({'id': row['id'], 'status': status,
                            'delta': row['outside_N_triangles'], 'edges': edges,
                            'labels_N': labels, 'star': row['star'],
                            'path_counts': row['path_counts'], 'isolates': row['isolates'],
                            'degree2': row['degree2']})
    open_records = [r for r in all_records if r['id'] in retained]
    assert len(all_records) == 6899 and len(open_records) == 4581
    assert len({r['id'] for r in all_records}) == 6899
    files = [write_jsonl(args.out / 'supports_all_6899.jsonl', all_records),
             write_jsonl(args.out / 'supports_open_4581.jsonl', open_records)]
    manifest = {
        'format': 'conway99-p3-n25-register-v1',
        'source_commit': 'ee50cd2',
        'source_branch': 'codex/c1-arithmetic-audit',
        'P': [0, 1, 2], 'N': list(range(3, 28)),
        'vertex_count': 28, 'edge_count': 36,
        'edge_convention': 'Undirected simple graph; one pair [u,v] with u<v per edge; all other pairs are nonedges.',
        'labels_N': 'Entry i corresponds to vertex 3+i. Bit p is 1 iff that vertex is adjacent to positive vertex p.',
        'delta': 'Number of N-N edges whose unique triangle has its third vertex outside the 28-vertex support.',
        'all_scope': 'After the analytic forest and initial delta reductions; before spectral and per-positive matching filters.',
        'open_scope': 'Necessary supports not excluded as of note246; not asserted extendible to SRG(99,14,1,2).',
        'status_counts': dict(Counter(r['status'] for r in all_records)),
        'open_counts_by_delta': dict(sorted(Counter(r['delta'] for r in open_records).items())),
        'integer_design_run_by_codex': False,
        'fractional_pilot': {'support_id': 4, 'delta': 3, 'status': 'numerically_feasible_relaxation_only',
                             'max_residual': 2.7133850721838826e-13,
                             'pairwise_block_intersection_constraints': False},
        'files': files,
    }
    (args.out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    for filename in ('245_CODEX_P3_N25_FORETS_ET_TRIANGLES_SORTANTS.md',
                     '246_CODEX_APPARIEMENTS_LOCAUX_P3_N25.md'):
        shutil.copyfile(ROOT / 'notes' / filename, args.out / filename)
    print(json.dumps({'counts': manifest['status_counts'], 'files': files}))


if __name__ == '__main__':
    main()
