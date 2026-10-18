"""Positive controls for the new neighbour-count tables on actual SRGs."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conway_global_cover import build_global, reconstruct_and_check
from root_component_neighbor_moments import add_neighbor_moments, root_rectangles
from root_component_resources import atomic_json_write, limit_research_process


def extract_root(matrix, root):
    neighbors = [u for u, x in enumerate(matrix[root]) if x]
    mate_edges = [(u, v) for u, v in combinations(neighbors, 2) if matrix[u][v]]
    assert len(mate_edges) * 2 == len(neighbors)
    assert len({u for pair in mate_edges for u in pair}) == len(neighbors)
    letters = [u for pair in mate_edges for u in pair]
    exterior = set(range(len(matrix))) - set(neighbors) - {root}
    by_label = {}
    for w in exterior:
        label = tuple(i for i, u in enumerate(letters) if matrix[w][u])
        assert len(label) == 2 and label not in by_label
        by_label[label] = w
    labels = sorted(by_label)
    order = [by_label[p] for p in labels]
    gamma = [[int(matrix[u][v]) for v in order] for u in order]
    return labels, gamma


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--positive-edges', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    records = []
    # The free k=4 instance checks the finite tables with genuine variables.
    model, labels, graph, _, _ = build_global(k=4, normalize_star=False)
    added = add_neighbor_moments(model, labels, graph, mixed=True)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = 5
    assert solver.solve(model) in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    gamma = [[solver.value(x) for x in row] for row in graph]
    reconstruct_and_check(4, labels, gamma)
    records.append({'graph': 'rook9', 'free_adjacency': True, 'status': 'PASSED',
                    'moments': added['info']})

    edges = [tuple(map(int, line.split())) for line in a.positive_edges.read_text().splitlines() if line.strip()]
    size = 1 + max(max(e) for e in edges)
    matrix = np.zeros((size, size), dtype=np.int64)
    for u, v in edges:
        matrix[u, v] = matrix[v, u] = 1
    k = int(matrix.sum(axis=1)[0])
    assert (size, k) == (243, 22)
    assert np.all(matrix.sum(axis=1) == k) and not np.any(np.diag(matrix))
    assert np.array_equal(matrix @ matrix + matrix, (k - 2) * np.eye(size, dtype=np.int64) + 2 * np.ones_like(matrix))
    labels, gamma = extract_root(matrix.tolist(), 0)
    _, rectangles = root_rectangles(labels)
    # Count all 55 rectangles, including all 1485 mixed pairs, arithmetically.
    model = cp_model.CpModel()
    added = add_neighbor_moments(model, labels, gamma, mixed=True)
    assert not model.validate(), model.validate()
    assert solver.solve(model) in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    histogram_counts = Counter()
    for q, column in added['columns'].items():
        histogram = Counter(column)
        e = added['local_edges'][q]
        assert histogram[2] + 3 * histogram[3] + 6 * histogram[4] + e == 8
        histogram_counts[tuple(histogram[i] for i in range(5))] += 1
    # Exercise mixed TABLES on an actual graph, with fixed Boolean variables.
    model = cp_model.CpModel()
    variable_graph = [[0] * len(labels) for _ in labels]
    for u, v in combinations(range(len(labels)), 2):
        x = model.new_bool_var(f'fixed_edge_{u}_{v}')
        model.add(x == gamma[u][v])
        variable_graph[u][v] = variable_graph[v][u] = x
    variable_added = add_neighbor_moments(model, labels, variable_graph, mixed=True,
                                         selected=[(0, 1), (0, 2), (3, 4)])
    assert not model.validate(), model.validate()
    assert solver.solve(model) in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    records.append({'graph': str(a.positive_edges), 'parameters': [243, 22, 1, 2],
                    'root': 0, 'status': 'PASSED', 'moments': added['info'],
                    'fixed_boolean_table_control': variable_added['info'],
                    'histogram_types': [{'n0_to_n4': list(h), 'rectangles': count}
                                        for h, count in sorted(histogram_counts.items())]})
    atomic_json_write(a.output, {'status': 'PASSED', 'resources': resources, 'controls': records,
                                'global_conway_exclusion': False})
    print(json.dumps({'status': 'PASSED', 'controls': len(records),
                      'positive_rectangles': len(rectangles), 'positive_mixed_pairs': 1485}))


if __name__ == '__main__':
    main()
