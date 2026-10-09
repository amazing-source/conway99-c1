"""Group the 478 saved attachments by their weighted D-intersection graph.

For D independent, the local D--Z incidence problem depends only on this
4-regular multigraph and Z. No quotient of full SRG completions is claimed.
"""
from collections import defaultdict
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[2]


def main():
    cases = json.loads((ROOT/'data/codex_norm16_attachments_rank.json').read_text())['cases']
    groups, buckets = [], defaultdict(list)
    for ci, case in enumerate(cases):
        for oi, orbit in enumerate(case['orbits']):
            shadows = [set(row[:2]) | {8+q for q in row[2:]} for row in orbit['representative']]
            c = [[0 if i == j else len(shadows[i] & shadows[j]) for j in range(8)] for i in range(8)]
            assert all(sum(row) == 4 for row in c)
            graph = nx.Graph()
            graph.add_nodes_from(range(8))
            graph.add_edges_from((i, j, {'weight': c[i][j]})
                                 for i in range(8) for j in range(i+1, 8) if c[i][j])
            key = nx.weisfeiler_lehman_graph_hash(graph, edge_attr='weight')
            found = None
            for index in buckets[key]:
                matcher = nx.algorithms.isomorphism.GraphMatcher(
                    graph, groups[index]['graph'], edge_match=lambda x, y: x['weight'] == y['weight'])
                if matcher.is_isomorphic():
                    found, mapping = index, matcher.mapping
                    break
            if found is None:
                found = len(groups)
                groups.append({'graph': graph, 'C': c, 'representative': [ci, oi], 'members': []})
                buckets[key].append(found)
                mapping = {i: i for i in range(8)}
            groups[found]['members'].append({'case': ci, 'orbit': oi,
                                            'to_representative': [mapping[i] for i in range(8)]})
    for group in groups:
        group.pop('graph')
    result = {'scope': __doc__, 'classes': groups}
    (ROOT/'data/codex_norm16_D_intersection_types.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'classes': len(groups), 'total_attachments': sum(len(g['members']) for g in groups)}))


if __name__ == '__main__':
    main()
