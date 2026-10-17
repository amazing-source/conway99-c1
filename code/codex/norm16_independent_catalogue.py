"""Catalogue the D-independent branch after exact spectral Schur filters.

The C++ search uses principal minors through order4; this driver then tests
the full8x8 Schur matrix by exact fraction-free elimination. All objects
remain necessary local supports, not SRG completions.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import subprocess
import time

import networkx as nx
import numpy as np

from norm16_schur_data import ROOT, matrices, source_data


def positive_semidefinite(matrix):
    a = [[int(x) for x in row] for row in matrix]
    previous = 1
    while a:
        n = len(a)
        if any(a[i][i] < 0 for i in range(n)):
            return False
        pivot = next((i for i in range(n) if a[i][i] > 0), None)
        if pivot is None:
            return not any(x for row in a for x in row)
        if pivot:
            a[0], a[pivot] = a[pivot], a[0]
            for row in a:
                row[0], row[pivot] = row[pivot], row[0]
        value = a[0][0]
        b = []
        for i in range(1, n):
            row = []
            for j in range(1, n):
                numerator = value*a[i][j]-a[i][0]*a[0][j]
                q, r = divmod(numerator, previous)
                assert r == 0
                row.append(q)
            b.append(row)
        previous, a = value, b
    return True


def rank7(matrix):
    a = np.array(matrix, dtype=np.int64) % 7
    rank = 0
    for j in range(a.shape[1]):
        candidates = np.flatnonzero(a[rank:, j])
        if not len(candidates):
            continue
        i = int(candidates[0])+rank
        a[[i, rank]] = a[[rank, i]]
        a[rank] = (a[rank]*pow(int(a[rank, j]), -1, 7)) % 7
        factors = a[:, j].copy()
        factors[rank] = 0
        a = (a-factors[:, None]*a[rank]) % 7
        rank += 1
        if rank == len(a):
            break
    return rank


def adjacency(core, attachment, forest, masks):
    a = np.zeros((35, 35), dtype=np.int64)
    b = np.array(core, dtype=np.int64)
    a[:8, 8:16], a[8:16, :8] = b, b.T
    a[24:, 24:] = forest['adjacency_Z']
    for d, row in enumerate(attachment):
        for v in row[:2]+[8+q for q in row[2:]]:
            a[v, 16+d] = a[16+d, v] = 1
    x = np.array([[(mask >> z) & 1 for z in range(11)] for mask in masks], dtype=np.int64)
    a[16:24, 24:], a[24:, 16:24] = x, x.T
    return a


def run(cases, orbits, seconds, directory, count_only=False, seed=None, executable='norm16_dz_catalogue.exe'):
    started = time.monotonic()
    cores, attachments, forests = source_data()
    forests = [f for f in forests if not f['edges_D']]
    planned_instances = len(forests)*sum(len(attachments[ci]['orbits']) if orbits is None else len(orbits) for ci in cases)
    symmetry = {}
    for f in forests:
        az = f['adjacency_Z']
        graph = nx.Graph()
        graph.add_nodes_from(range(11))
        graph.add_edges_from((i, j) for i, j in combinations(range(11), 2) if az[i][j])
        autos = list(nx.algorithms.isomorphism.GraphMatcher(graph, graph).isomorphisms_iter())
        symmetry[f['id']] = ([' '.join(str(sum(1 << j for j, v in enumerate(row) if v)) for row in az)],
                             [str(len(autos))]+[' '.join(str(auto[z]) for z in range(11)) for auto in autos])
    target = ROOT/directory
    target.mkdir(parents=True, exist_ok=True)
    scratch = target/'instance.txt'
    spectral_file = target/'schur.txt'
    raw_file = target/'rows.txt'
    prior = json.loads((ROOT/seed).read_text()) if seed else {}
    records = prior.get('results', [])[:]
    completed_keys = {(r['case'], r['orbit'], r['forest']) for r in records if r['status'] == 'EXHAUSTED'}
    if any(r['status'] != 'EXHAUSTED' for r in records):
        raise ValueError('Only exhausted seed records may be reused.')
    rank_counts = Counter({int(k): v for k, v in prior.get('rank_counts', {}).items()})
    total_minors = sum(r['count_mod_Aut_Z'] for r in records)
    total_psd = sum(r.get('full_PSD_count', 0) for r in records)
    output = None if count_only else (target/'supports.jsonl').open('w', encoding='utf-8')
    try:
        for ci in cases:
            case = attachments[ci]
            selected = range(len(case['orbits'])) if orbits is None else orbits
            for oi in selected:
                attachment = case['orbits'][oi]['representative']
                coreline = ' '.join(str(sum(1 << p for p in row[:2])+sum(1 << (8+q) for q in row[2:]))
                                    for row in attachment)
                orbit_records = []
                for f in forests:
                    if (ci, oi, f['id']) in completed_keys:
                        continue
                    top, tail = symmetry[f['id']]
                    scratch.write_text('\n'.join(top+[coreline]+tail)+'\n', encoding='ascii')
                    scale, h, w = matrices(ci, oi, f['id'])
                    spectral_file.write_text('\n'.join([str(scale)]+[' '.join(map(str, row)) for row in h+w])+'\n', encoding='ascii')
                    command = [str(ROOT/'code/codex'/executable), str(scratch), str(seconds),
                               '-' if count_only else str(raw_file), str(spectral_file)]
                    completed = subprocess.run(command, check=True, capture_output=True, text=True)
                    result = json.loads(completed.stdout)
                    result.update({'case': ci, 'orbit': oi, 'forest': f['id'], 'schur_scale': scale})
                    hi, wi = np.array(h, dtype=np.int64), np.array(w, dtype=np.int64)
                    live = 0
                    for line in ([] if count_only else raw_file.read_text().splitlines()):
                        masks = list(map(int, line.split()))
                        k = np.array([[3-7*((mask >> j) & 1) for j in range(11)] for mask in masks], dtype=np.int64)
                        r = hi-k @ wi @ k.T
                        if not positive_semidefinite(r.tolist()):
                            continue
                        a = adjacency(cores[ci]['representatives'][0], attachment, f, masks)
                        seidel = np.ones((35, 35), dtype=np.int64)-np.eye(35, dtype=np.int64)-2*a
                        rank = rank7(seidel)
                        item = {'case': ci, 'orbit': oi, 'forest': f['id'], 'D_Z_row_masks': masks,
                                'seidel_rank_mod7': rank}
                        output.write(json.dumps(item)+'\n')
                        rank_counts[rank] += 1
                        live += 1
                    if output is not None:
                        output.flush()
                    if not count_only:
                        result['full_PSD_count'] = live
                    total_psd += live
                    total_minors += result['count_mod_Aut_Z']
                    records.append(result)
                    orbit_records.append(result)
                summary = {'scope': __doc__, 'results': records, 'total_after_minors4': total_minors,
                           'total_after_full_PSD': total_psd, 'rank_counts': dict(sorted(rank_counts.items())),
                           'all_completed_instances_exhausted': all(r['status'] == 'EXHAUSTED' for r in records),
                           'planned_instance_count': planned_instances,
                           'campaign_complete': len(records) == planned_instances,
                           'full_PSD_completed_on_all_records': all('full_PSD_count' in r for r in records),
                           'run_mode': 'count_only_minors4' if count_only else 'full_PSD_and_rank',
                           'seconds': time.monotonic()-started,
                           'planned_cases': cases, 'planned_orbits': orbits}
                (target/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
                print(json.dumps({'case': ci, 'orbit': oi,
                                  'stage': 'minors4' if count_only else 'full_PSD',
                                  'counts': [r.get('full_PSD_count', r['count_mod_Aut_Z']) for r in orbit_records],
                                  'total_minors4': total_minors,
                                  'total_full_PSD': total_psd,
                                  'stopped': sum(r['status'] != 'EXHAUSTED' for r in records),
                                  'seconds': time.monotonic()-started}), flush=True)
    finally:
        if output is not None:
            output.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cases', default='0,1,2,3,4')
    parser.add_argument('--orbits', default=None, help='Comma-separated indices, or omitted for all')
    parser.add_argument('--seconds', type=float, default=3)
    parser.add_argument('--directory', default='data/codex_norm16_independent_catalogue')
    parser.add_argument('--count-only', action='store_true')
    parser.add_argument('--seed', help='Reuse exhausted results from this summary without recomputing them')
    parser.add_argument('--executable', default='norm16_dz_catalogue.exe')
    args = parser.parse_args()
    run([int(x) for x in args.cases.split(',')],
        None if args.orbits is None else [int(x) for x in args.orbits.split(',')],
        args.seconds, args.directory, args.count_only, args.seed, args.executable)
