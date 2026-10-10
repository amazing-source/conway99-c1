"""Bounded pilot on selected intersection types; never extrapolate STOPPED."""
import argparse
import json
from pathlib import Path
import subprocess

import networkx as nx

ROOT = Path(__file__).resolve().parents[2]


def run(types, seconds, output, spectral=False):
    groups = json.loads((ROOT/'data/codex_norm16_D_intersection_types.json').read_text())['classes']
    cases = json.loads((ROOT/'data/codex_norm16_attachments_rank.json').read_text())['cases']
    forests = json.loads((ROOT/'data/codex_norm16_far_forest_refined.json').read_text())['forests']
    forests = [f for f in forests if f['edges_D'] == 0]
    symmetry = {}
    for f in forests:
        az = f['adjacency_Z']
        graph = nx.Graph()
        graph.add_nodes_from(range(11))
        graph.add_edges_from((i, j) for i in range(11) for j in range(i+1, 11) if az[i][j])
        autos = list(nx.algorithms.isomorphism.GraphMatcher(graph, graph).isomorphisms_iter())
        symmetry[f['id']] = ([' '.join(str(sum(1 << j for j, v in enumerate(row) if v)) for row in az)],
                             [str(len(autos))]+[' '.join(str(auto[z]) for z in range(11)) for auto in autos])
    target = ROOT/output
    scratch = target.with_suffix('.instance.txt')
    results = []
    for t in types:
        group = groups[t]
        ci, oi = group['representative']
        attachment = cases[ci]['orbits'][oi]['representative']
        coreline = ' '.join(str(sum(1 << p for p in row[:2])+sum(1 << (8+q) for q in row[2:]))
                            for row in attachment)
        for f in forests:
            top, tail = symmetry[f['id']]
            scratch.write_text('\n'.join(top+[coreline]+tail)+'\n', encoding='ascii')
            command = [str(ROOT/'code/codex/norm16_dz_catalogue.exe'), str(scratch), str(seconds)]
            if spectral:
                from norm16_schur_data import matrices
                scale, h, w = matrices(ci, oi, f['id'])
                spectral_file = target.with_suffix('.schur.txt')
                spectral_file.write_text('\n'.join([str(scale)]+[' '.join(map(str, row)) for row in h+w])+'\n', encoding='ascii')
                command += ['-', str(spectral_file)]
            completed = subprocess.run(command, check=True, capture_output=True, text=True)
            result = json.loads(completed.stdout)
            result.update({'intersection_type': t, 'case': ci, 'orbit': oi, 'forest': f['id'],
                           'attachment_multiplicity': len(group['members'])})
            if spectral:
                result['attachment_multiplicity'] = 1
                result['scope_warning'] = 'Schur matrix also depends on the core: do not reuse this count for all C-equivalent attachments.'
            results.append(result)
            target.write_text(json.dumps({'scope': __doc__, 'results': results}, indent=2)+'\n')
            print(json.dumps(result), flush=True)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--types', default='0,11,42,85,82')
    parser.add_argument('--seconds', type=float, default=3)
    parser.add_argument('--output', default='data/codex_norm16_dz_five_types.json')
    parser.add_argument('--spectral', action='store_true')
    args = parser.parse_args()
    run([int(t) for t in args.types.split(',')], args.seconds, args.output, args.spectral)
