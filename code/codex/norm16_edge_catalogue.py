"""Enumerate the one-edge D branch with fixed endpoint templates (note253).

Counts are modulo Aut(Z) only, with ordered labelled D endpoints. Exact
Schur minors through order4 precede the full exact8x8 PSD filter.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
import subprocess
import time

import networkx as nx
import numpy as np

from norm16_schur_data import ROOT, matrices, source_data
from norm16_edge_endpoints import templates, bits
from norm16_edge_omitted_pair import refined_sources
from norm16_independent_catalogue import positive_semidefinite, adjacency, rank7


def run(case, orbit, edge_index, seconds, directory):
    sources = refined_sources()
    edges = sources['cases'][case]['orbits'][orbit]['eligible_edges']
    chosen_edges = edges if edge_index is None else [edges[edge_index]]
    cores, attachments, forests = source_data()
    attachment = attachments[case]['orbits'][orbit]['representative']
    coreline = ' '.join(str(sum(1 << p for p in row[:2])+sum(1 << (8+q) for q in row[2:])) for row in attachment)
    target = ROOT/directory
    target.mkdir(parents=True, exist_ok=True)
    scratch, schur, raw = (target/name for name in ('instance.txt', 'schur.txt', 'rows.txt'))
    records = []
    ranks = Counter()
    started = time.monotonic()
    if not chosen_edges:
        summary = {'scope': __doc__, 'case': case, 'orbit': orbit, 'D_edges': [],
                   'results': [], 'completed_all_planned': True,
                   'total_after_minors4': 0, 'total_full_PSD': 0, 'rank_counts': {},
                   'reason': 'No D edge survives the omitted-pair theorem.'}
        (target/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
        print(json.dumps(summary), flush=True)
        return
    live_file = (target/'supports.jsonl').open('w')
    for f in forests:
        if not f['edges_D'] or not templates(f['id'], True):
            continue
        fid = f['id']
        graph = nx.from_numpy_array(np.array(f['adjacency_Z']))
        autos = list(nx.algorithms.isomorphism.GraphMatcher(graph, graph).isomorphisms_iter())
        forest_line = ' '.join(str(sum(1 << z for z, value in enumerate(row) if value)) for row in f['adjacency_Z'])
        for edge in chosen_edges:
            d, e = edge
            scale, h, w = matrices(case, orbit, fid, tuple(edge))
            hi, wi = np.array(h, dtype=np.int64), np.array(w, dtype=np.int64)
            schur.write_text('\n'.join([str(scale)]+[' '.join(map(str, row)) for row in h+w])+'\n')
            for ti, template in enumerate(templates(fid, True)):
                r, t = template['rows']
                group = [a for a in autos if sum(1 << a[z] for z in bits(r)) == r and sum(1 << a[z] for z in bits(t)) == t]
                scratch.write_text('\n'.join([forest_line, coreline, str(len(group))]+[' '.join(str(a[z]) for z in range(11)) for a in group]+[f'{d} {e} {r} {t}'])+'\n')
                command = [str(ROOT/'code/codex/norm16_edge_catalogue.exe'), str(scratch), str(seconds), str(raw), str(schur)]
                result = json.loads(subprocess.run(command, check=True, capture_output=True, text=True).stdout)
                result['count_mod_endpoint_stabilizer'] = result.pop('count_mod_Aut_Z')
                result['endpoint_stabilizer_order'] = result.pop('Aut_Z')
                result.update({'forest': fid, 'edge': edge, 'endpoint_template': ti, 'endpoint_rows': [r, t]})
                live = 0
                for line in raw.read_text().splitlines():
                    masks = list(map(int, line.split()))
                    k = np.array([[3-7*((m >> z) & 1) for z in range(11)] for m in masks], dtype=np.int64)
                    if not positive_semidefinite((hi-k @ wi @ k.T).tolist()):
                        continue
                    a = adjacency(cores[case]['representatives'][0], attachment, f, masks)
                    a[16+d, 16+e] = a[16+e, 16+d] = 1
                    rank = rank7(np.ones((35, 35), dtype=np.int64)-np.eye(35, dtype=np.int64)-2*a)
                    live_file.write(json.dumps({'case': case, 'orbit': orbit, 'forest': fid, 'D_edge': edge, 'D_Z_row_masks': masks, 'seidel_rank_mod7': rank})+'\n')
                    ranks[rank] += 1
                    live += 1
                result['full_PSD_count'] = live
                records.append(result)
            summary = {'scope': __doc__, 'case': case, 'orbit': orbit, 'D_edges': chosen_edges,
                       'results': records, 'completed_all_planned': False,
                       'total_after_minors4': sum(x['count_mod_endpoint_stabilizer'] for x in records),
                       'total_full_PSD': sum(x['full_PSD_count'] for x in records),
                       'rank_counts': dict(sorted(ranks.items())), 'seconds': time.monotonic()-started}
            (target/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
            print(json.dumps({'forest': fid, 'edge': edge, 'full_PSD': sum(x['full_PSD_count'] for x in records if x['forest'] == fid and x['edge'] == edge), 'stopped': sum(x['status'] != 'EXHAUSTED' for x in records)}), flush=True)
    live_file.close()
    summary['completed_all_planned'] = all(x['status'] == 'EXHAUSTED' for x in records)
    (target/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'results'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int, default=0)
    parser.add_argument('--orbit', type=int, default=0)
    parser.add_argument('--edge-index', type=int)
    parser.add_argument('--seconds', type=float, default=2)
    parser.add_argument('--directory', default='data/codex_norm16_edge_catalogue_0_0')
    args = parser.parse_args()
    run(args.case, args.orbit, args.edge_index, args.seconds, args.directory)
