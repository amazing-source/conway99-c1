"""Export a core+D+Z base passing 3I-A+J/9 PSD, with local domains for64 simples."""
from itertools import combinations
import argparse
import json

from norm16_independent_catalogue import adjacency
from norm16_schur_data import ROOT, source_data


def mask(vertices):
    return sum(1 << v for v in vertices)


def main(source='data/codex_norm16_world35_seed.json', output='data/codex_norm16_typed_world35_0_3_2.json'):
    source_file = ROOT/source
    item = json.loads(source_file.read_text())
    cores, cases, forests = source_data()
    ci, oi = item['case'], item['orbit']
    b = cores[ci]['representatives'][0]
    attachment = cases[ci]['orbits'][oi]['representative']
    forest = next(f for f in forests if f['id'] == item['forest'])
    a = adjacency(b, attachment, forest, item['D_Z_row_masks']).tolist()
    edge = item.get('D_edge')
    if edge is not None:
        d, e = edge
        a[16+d][16+e] = a[16+e][16+d] = 1
    row_masks = [mask(i for i, value in enumerate(row) if value) for row in a]
    wb = 9-5*forest['edges_D']-forest['wedges_Z']
    saturated_pairs = [mask((i, j)) for i, j in combinations(range(35), 2)
                       if (row_masks[i] & row_masks[j]).bit_count() == 2-a[i][j]]
    ext_masks = []
    for r in range(5):
        if r*(r-1)//2 > wb:
            continue
        ds = [mask(row) for row in combinations(range(16, 24), r)]
        zs = [mask(row) for row in combinations(range(24, 35), r+1)]
        ext_masks.extend(d | z for d in ds for z in zs)
    domains = []
    for p in range(8):
        for q in range(8):
            copies = 2-b[p][q]-sum(p in d[:2] and q in d[2:] for d in attachment)
            if not copies:
                continue
            core_mask = mask((p, 8+q))
            candidates = []
            for ext in ext_masks:
                value = core_mask | ext
                if all((value & row).bit_count() <= 2-((value >> i) & 1)
                       for i, row in enumerate(row_masks)) and not any(value & pair == pair for pair in saturated_pairs):
                    candidates.append(value)
            domains.append({'cell': [p, q], 'multiplicity': copies,
                            'neighbour_masks': sorted(candidates)})
    labels = [{'kind': 'P', 'index': i} for i in range(8)]
    labels += [{'kind': 'Q', 'index': i} for i in range(8)]
    labels += [{'kind': 'D', 'index': i, 'P': d[:2], 'Q': d[2:]} for i, d in enumerate(attachment)]
    labels += [{'kind': 'Z', 'index': i} for i in range(11)]
    result = {'scope': __doc__, 'source': item, 'base_labels': labels, 'base_adjacency': a,
              'seidel_rank_mod7': item['seidel_rank_mod7'],
              'relations_mod7': [[1]*8+[-1]*8+[0]*19, [3]*16+[1]*8+[-1]*11],
              'ambient_dimension': 36, 'residual_dimension_when_base_rank33': 3,
              'domains': domains, 'total_unknown_vertices': sum(d['multiplicity'] for d in domains),
              'WB_budget': wb,
              'required_simple_neighbours_by_base_vertex': [14-sum(row) for row in a],
              'rules': [
                  'A domain corresponds to a cell(p,q); choose multiplicity DISTINCT vertices from it.',
                  'Distinct vertices may have the SAME base neighbour mask; their residual vectors and mutual products must still be tested.',
                  'All D vertices are already in the base; the64 unknowns are all simple B vertices.',
                  'Each unknown has exactly the core neighbours p and Qq, and degree_Z=1+degree_D.',
                  'Sum over the64 simples of binom(degree_D,2) equals WB_budget.',
                  'Each D vertex must receive6-2*degree_D(d) simple neighbours; each Z vertex z must receive16-2*degree_D(z) simple neighbours.',
                  'The domain omits any pair whose common-neighbour quota is already saturated inside the base.',
                  'A simple with r D neighbours has11-2r neighbours among simples.',
                  'The eight simples with first cell index p, the two D neighbours of p, and the four Q neighbours of p induce7 disjoint edges.',
                  'Apply the analogous complete-neighbourhood condition for every Q vertex.',
                  'Count all common neighbours: adjacent pairs require1; nonadjacent pairs require2.',
                  'Seidel isotropy and mutual products in dimension36 are not imposed in these local domains.'
              ],
              'mask_convention': 'bit i = adjacency to base vertex i, bits0..34'}
    target = ROOT/output
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'file': str(target), 'vertices': result['total_unknown_vertices'],
                      'nonempty_cells': len(domains), 'total_candidate_columns_by_cell': sum(len(d['neighbour_masks']) for d in domains),
                      'cellP0': [{'cell': d['cell'], 'multiplicity': d['multiplicity'], 'columns': len(d['neighbour_masks'])}
                                 for d in domains if d['cell'][0] == 0]}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='data/codex_norm16_world35_seed.json')
    parser.add_argument('--output', default='data/codex_norm16_typed_world35_0_3_2.json')
    args = parser.parse_args()
    main(args.source, args.output)
