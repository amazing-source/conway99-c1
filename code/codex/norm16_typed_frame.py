"""Export a local norm16 frame with labelled, admissible binary columns.

Only necessary integer/local rules are used here. The Seidel products and
the simultaneous placement of the remaining vertices belong to LAB's test.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from math import comb
import time

from norm16_far_incidence import ROOT


def bits(values):
    return sum(1 << v for v in values)


def export(frame_file):
    source = json.loads(frame_file.read_text())
    a, labels = source['adjacency'], source['labels']
    n = len(a)
    rows = [bits(i for i, value in enumerate(row) if value) for row in a]
    z_indices = [i for i, label in enumerate(labels) if label['kind'] == 'Z']
    d_indices = [i for i, label in enumerate(labels) if label['kind'] == 'D']
    b_indices = [i for i, label in enumerate(labels) if label['kind'] == 'B']
    y_indices = d_indices+b_indices
    zmask = bits(z_indices)
    dmask = bits(d_indices)
    attachment = source['attachment_D']
    known_d = {labels[i]['index'] for i in d_indices}
    unknown = [{'kind': 'D', 'index': d, 'P': row[:2], 'Q': row[2:]}
               for d, row in enumerate(attachment) if d not in known_d]
    unknown += [{'kind': 'B', 'cell': cell[:2], 'copy': cell[2]}
                for cell in source['all_simple_labels'] if cell[0] != 0]
    assert len(unknown) == 62
    wz = sum(comb((rows[z] & zmask).bit_count(), 2) for z in z_indices)
    wb = 9-wz
    known_b_d_degrees = {b: (rows[b] & zmask).bit_count()-1 for b in b_indices}
    remaining_wb = wb-sum(comb(k, 2) for k in known_b_d_degrees.values())
    assert remaining_wb >= 0
    z_masks = {k: [bits(c) for c in combinations(z_indices, k)] for k in range(1, 7)}
    y_masks = {k: [bits(c) for c in combinations(y_indices, k)] for k in range(3)}
    z_masks[0] = [0]
    cache = {}
    domains = []
    for label in unknown:
        key = (label['kind'], tuple(label.get('cell', [])), label.get('index'))
        if key not in cache:
            if label['kind'] == 'D':
                core = bits(label['P']+[8+q for q in label['Q']])
            else:
                p, q = label['cell']
                core = bits((p, 8+q))
            y_count = 2-(core & rows[0]).bit_count()
            candidates = []
            for ym in y_masks[y_count]:
                known_d_count = (ym & dmask).bit_count()
                if label['kind'] == 'D':
                    if known_d_count:
                        continue  # This frame belongs to the D-independent branch.
                    if any((ym >> b & 1) > known_b_d_degrees[b]-(rows[b] & dmask).bit_count()
                           for b in b_indices):
                        continue
                    z_counts = (4,)
                else:
                    z_counts = [k for k in range(1+known_d_count, min(6, 8+known_d_count))
                                if comb(k-1, 2) <= remaining_wb]
                for k in z_counts:
                    for zm in z_masks[k]:
                        mask = core | ym | zm
                        if all((mask & row).bit_count() <= 2-(mask >> i & 1)
                               for i, row in enumerate(rows)):
                            assert (mask & rows[0]).bit_count() == 2
                            candidates.append(mask)
            cache[key] = sorted(candidates)
        domains.append({'label': label, 'neighbour_masks': cache[key]})
    cells = []
    for p in range(1, 8):
        in_cell = lambda label: (label['kind'] == 'D' and p in label['P']) or (
            label['kind'] == 'B' and label['cell'][0] == p)
        cells.append({'positive': p,
                      'known_Q_neighbours': [8+q for q in range(8) if a[p][8+q]],
                      'known_exterior_members': [i for i, label in enumerate(labels) if in_cell(label)],
                      'unknown_exterior_members': [i for i, item in enumerate(domains) if in_cell(item['label'])]})
    f = [int(i < 8)-int(8 <= i < 16) for i in range(n)]
    g = [4*int(i == 0)+a[0][i] for i in range(n)]
    seidel = [[0 if i == j else 1-2*a[i][j] for j in range(n)] for i in range(n)]
    assert all(sum(x*v for x, v in zip(row, f)) % 7 == 0 for row in seidel)
    assert all(sum(x*v for x, v in zip(row, g)) % 7 == 0 for row in seidel)
    result = {'scope': __doc__, 'source_local_frame': frame_file.name,
              'case': source['case'], 'orbit': source['orbit'], 'forest': source['forest'],
              'edges_D': 0, 'base_labels': labels, 'base_adjacency': a,
              'seidel_rank_mod7': source['seidel_rank_mod7'],
              'two_known_relations_mod7': [f, g],
              'integer_budget_WB_total': wb, 'integer_budget_WB_remaining': remaining_wb,
              'attachment_D': attachment, 'domains': domains, 'cells': cells,
              'mask_convention': 'bit i = adjacency to base vertex i; positive integer, bits 0..36',
              'rules': [
                  'Only the 37 base vertices are fixed; the 43-vertex auxiliary witness is NOT fixed.',
                  'D is independent; every D vertex has four neighbours in Z.',
                  'B cell(p,q) has exactly core neighbours p and Qq.',
                  'For each B vertex, number of D neighbours equals number of Z neighbours minus one.',
                  'Sum over all B of binom(degree_D,2) equals integer_budget_WB_total.',
                  'Each cell plus its four Q neighbours is the complete 14-neighbourhood of its positive; it induces 7 disjoint edges.',
                  'For two new vertices with masks u,v and adjacency e, popcount(u & v) <= 2-e; count any placed extra common vertices too.',
                  'Each vertex has degree14, each adjacent pair exactly1 and each nonadjacent pair exactly2 common neighbours in the final graph.',
                  'Seidel products and isotropy in dimension36 over F7 still have to be imposed by the rank37 test.'
              ]}
    target = frame_file.with_name(frame_file.stem.replace('frame_', 'typed_frame_')+'.json')
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    return {'file': str(target), 'base_rank': source['seidel_rank_mod7'],
            'domain_size_histogram': dict(sorted(Counter(len(item['neighbour_masks']) for item in domains).items())),
            'second_cell': [{'label': domains[i]['label'], 'candidates': len(domains[i]['neighbour_masks'])}
                            for i in cells[0]['unknown_exterior_members']]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/codex_norm16_frame_0_0_2.json')
    args = parser.parse_args()
    start = time.monotonic()
    result = export(ROOT/args.input)
    result['seconds'] = time.monotonic()-start
    print(json.dumps(result, indent=2))
