"""List the 15 necessary far forests of a norm-16 (-4)-eigenvector.

The classification is proved in note251; this script only lists its small
component multisets and combines them with the five previously saved cores.
No SRG completion or new enumeration of the norm-16 cores is performed.
"""
from collections import Counter
from itertools import product
import json

from norm16_attachments_rank import ROOT, rank


COMPONENTS = (
    ('K2', 2, ((0, 1),)),
    ('P3', 3, ((0, 1), (1, 2))),
    ('P4', 4, ((0, 1), (1, 2), (2, 3))),
    ('K13', 4, ((0, 1), (0, 2), (0, 3))),
)


def forests():
    out = []
    for e_d in (0, 1):
        for counts in product(range(7), range(4), range(3), range(3)):
            k2, p3, p4, star = counts
            edges = k2+2*p3+3*p4+3*star
            vertices = 2*k2+3*p3+4*p4+4*star
            wedges = p3+2*p4+3*star
            if edges != 5+e_d or vertices > 11 or wedges > 9-5*e_d:
                continue
            graph = [[0]*11 for _ in range(11)]
            offset = 0
            for count, (_, order, edge_list) in zip(counts, COMPONENTS):
                for _ in range(count):
                    for i, j in edge_list:
                        graph[offset+i][offset+j] = graph[offset+j][offset+i] = 1
                    offset += order
            assert sum(map(sum, graph)) == 2*edges
            assert sum(sum(row)*(sum(row)-1)//2 for row in graph) == wedges
            out.append({'id': len(out)+1, 'edges_D': e_d,
                        'components': dict(zip((x[0] for x in COMPONENTS), counts)),
                        'isolates': 11-vertices, 'edges_Z': edges,
                        'wedges_Z': wedges, 'wedges_from_simple_vertices_into_D': 9-5*e_d-wedges,
                        'adjacency_Z': graph})
    return out


def main():
    far = forests()
    source = json.loads((ROOT/'data/codex_norm16_cores.json').read_text())
    cores = [case for case in source['cases'] if case['representatives']]
    configurations = []
    for case in cores:
        b = case['representatives'][0]
        for z in far:
            a = [[0]*27 for _ in range(27)]
            for i in range(8):
                for j in range(8):
                    a[i][8+j] = a[8+j][i] = b[i][j]
            for i in range(11):
                for j in range(11):
                    a[16+i][16+j] = z['adjacency_Z'][i][j]
            seidel = [[0 if i == j else 1-2*a[i][j] for j in range(27)] for i in range(27)]
            configurations.append({'core_defect_cycles': case['defect_cycle_lengths'],
                                   'far_forest_id': z['id'],
                                   'seidel_rank_mod7': rank(seidel),
                                   'edges': [[i, j] for i in range(27) for j in range(i+1, 27) if a[i][j]]})
    report = {'scope': __doc__, 'forests': far, 'configurations_27': configurations,
              'forest_count_by_edges_D': dict(Counter(str(z['edges_D']) for z in far)),
              'seidel_rank_counts': dict(sorted(Counter(str(c['seidel_rank_mod7']) for c in configurations).items()))}
    (ROOT/'data/codex_norm16_far_forest.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'forests': len(far), 'configurations': len(configurations),
                      'by_edges_D': report['forest_count_by_edges_D'],
                      'seidel_ranks': report['seidel_rank_counts'],
                      'forms': [{k: v for k, v in z.items() if k != 'adjacency_Z'} for z in far]}, indent=2))


if __name__ == '__main__':
    main()
