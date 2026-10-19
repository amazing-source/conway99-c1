"""Propagate the existence of future edges through outside profile domains.

For one fixed profile p of vertex x, every outside neighbour y must
choose a profile q allowing the edge xy. Count DISTINCT possible y
for each required degree, upper-letter and known-pair quota of x.
Too few possible y refute p. Deletions are iterated to a fixed point.
No numerical solver or global symmetry is used. Passing is only local.
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_p3_neighbor_support import prepare_profile, edge_failure
from root_component_resources import atomic_json_write, limit_research_process


def bits(value):
    while value:
        low = value & -value
        yield low.bit_length() - 1
        value ^= low


def filter_edge_capacity(rows, known_labels, outside_labels, domains, root_count=7):
    n = len(domains)
    assert n == len(outside_labels) and len(rows) == len(known_labels)
    prepared = [[prepare_profile(rows, known_labels, q, p, root_count) for p in domain]
                for q, domain in zip(outside_labels, domains)]
    active = [set(range(len(d))) for d in domains]
    letter_vertices = [sum(1 << v for v, q in enumerate(outside_labels) if l in q)
                       for l in range(2*root_count)]
    rounds = []; removed = []
    while True:
        # supports[x][p][y] is the union of known neighbours in all
        # currently possible profiles of y permitting the edge xy.
        supports = [{pi: {} for pi in ids} for ids in active]
        edge_tests = 0; possible_edges = 0
        for x in range(n):
            for y in range(x+1, n):
                for pi in active[x]:
                    a = prepared[x][pi]
                    for qi in active[y]:
                        b = prepared[y][qi]; edge_tests += 1
                        if edge_failure(a, b) is None:
                            supports[x][pi][y] = supports[x][pi].get(y, 0) | b['mask']
                            supports[y][qi][x] = supports[y][qi].get(x, 0) | a['mask']
                            possible_edges += 1
        failures = []
        for x, ids in enumerate(active):
            q = outside_labels[x]; roots = {l // 2 for l in q}
            for pi in sorted(ids):
                p = domains[x][pi]; info = prepared[x][pi]
                if not info['valid']:
                    failures.append({'outside_index': x, 'profile_index': pi,
                                     'kind': 'invalid_single_profile'})
                    continue
                by_vertex = supports[x][pi]
                possible = sum(1 << y for y in by_vertex)
                checks = [('degree', None, info['degree_remaining'], possible)]
                for l in range(2*root_count):
                    target = (1 if l // 2 in roots else 2) - sum(l in known_labels[v] for v in p)
                    checks.append(('upper_letter', l, target, possible & letter_vertices[l]))
                known_support = [0] * len(rows)
                for y, union in by_vertex.items():
                    for v in bits(union):
                        known_support[v] |= 1 << y
                for v, row in enumerate(rows):
                    target = 2-int(v in p)-len(set(q) & set(known_labels[v]))-(info['mask'] & row).bit_count()
                    checks.append(('common_with_known', v, target, known_support[v]))
                for kind, target_index, target, support in checks:
                    if target > support.bit_count():
                        failures.append({'outside_index': x, 'outside_label': q, 'profile_index': pi,
                                         'profile': p, 'kind': kind, 'target_index': target_index,
                                         'required': target, 'capacity': support.bit_count(),
                                         'possible_partners': list(bits(support))})
                        break
        rounds.append({'input_profile_count': sum(map(len, active)), 'edge_tests': edge_tests,
                       'possible_profile_edges': possible_edges, 'removed': len(failures)})
        if not failures:
            break
        for record in failures:
            record['round'] = len(rounds)-1
            active[record['outside_index']].remove(record['profile_index'])
        removed.extend(failures)
        if any(not ids for ids in active):
            break
    empty = [i for i, ids in enumerate(active) if not ids]
    return {'status': 'EXCLUDED_FUTURE_EDGE_CAPACITY' if empty else 'PASSES_FUTURE_EDGE_CAPACITY',
            'empty_domains': empty, 'removed_count': len(removed), 'rejections': removed, 'rounds': rounds,
            'kept_indices': [sorted(ids) for ids in active],
            'domains': [[d[i] for i in sorted(ids)] for d, ids in zip(domains, active)],
            'scope': 'Necessary degree, letter and common-neighbour capacities for genuine future edges.'}


def controls():
    # Real SRG(9,4,1,2): the 3x3 rook graph, rooted at (0,0).
    vertices = [(a, b) for a in range(3) for b in range(3)]
    graph = [{j for j, y in enumerate(vertices) if i != j and (x[0] == y[0] or x[1] == y[1])}
             for i, x in enumerate(vertices)]
    assert all(len(r) == 4 for r in graph)
    assert all(len(graph[i] & graph[j]) == (1 if j in graph[i] else 2)
               for i in range(9) for j in range(i+1, 9))
    # Gamma is C4. Its first corner is known; the true profiles remain
    # after an extra, impossible adjacency to the opposite corner is added.
    known = [(0, 2)]; outside = [(0, 3), (1, 2), (1, 3)]
    result = filter_edge_capacity([0], known, outside, [[[0]], [[0]], [[], [0]]], root_count=2)
    assert result['status'] == 'PASSES_FUTURE_EDGE_CAPACITY'
    assert result['domains'] == [[[0]], [[0]], [[]]]
    return {'actual_srg_parameters': [9, 4, 1, 2], 'planted_completion_preserved': True,
            'false_opposite_corner_profile_removed': result['removed_count'] == 1,
            'result': result}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path, nargs='?'); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); resources = limit_research_process(1); started = time.process_time()
    report = {'controls': controls(), 'resources': resources}
    if a.input:
        data = json.loads(a.input.read_text(encoding='utf-8-sig'))
        report['result'] = filter_edge_capacity(data['rows'], data['known_labels'], data['outside_labels'], data['domains'])
    report['cpu_seconds'] = time.process_time()-started
    atomic_json_write(a.output, report)
    print(json.dumps({'cpu_seconds': report['cpu_seconds'],
                      'status': report.get('result', {}).get('status', 'CONTROLS_PASSED'),
                      'removed': report.get('result', {}).get('removed_count', 0)}))


if __name__ == '__main__':
    main()
