"""Controls of the shared C2 encoder, not of the full Conway Gram model."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import textwrap
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process


def legacy_equivalence():
    """Compare serialized models with the actual pre-extraction Conway loop."""
    from ortools.sat.python import cp_model
    from root_component_c2_layers import add_c2_layers, label_pair_layer
    from root_component_propagation import LABELS, PAIRS
    source = subprocess.check_output(
        ['git', 'show', '8055c032:code/codex/root_component_signature_joint.py'],
        cwd=Path(__file__).resolve().parents[2], encoding='utf-8')
    source = textwrap.dedent(source[source.index('    products = {}'):source.index('    minc_info=None')])
    compiled = compile(source, '<legacy-signature-joint-c2>', 'exec')
    results = []
    for layer in range(5):
        models = []
        for legacy in (True, False):
            model = cp_model.CpModel()
            graph = [[0] * 84 for _ in LABELS]
            for i, (u, v) in enumerate(PAIRS):
                # Both constants (0,1) and Boolean variables in the same graph.
                e = model.new_bool_var(f'e{i}') if i % 17 == 0 else int(i % 37 == 0)
                graph[u][v] = graph[v][u] = e
            if legacy:
                scope = dict(model=model, graph=graph, PAIRS=PAIRS, LABELS=LABELS,
                             layer=layer, pair_layer=lambda u, v: label_pair_layer(LABELS[u], LABELS[v]))
                exec(compiled, scope)
            else:
                info = add_c2_layers(model, graph, LABELS, layer)
            assert not model.validate(), model.validate()
            models.append(str(model.proto))
        assert models[0] == models[1], layer
        results.append({'layer': layer, 'serialized_model_identical': True, **info})
    return results


def control_243(path):
    import numpy as np
    from ortools.sat.python import cp_model
    from root_component_c2_layers import add_c2_layers, label_pair_layer
    from root_component_neighbor_moment_controls import extract_root
    from conway_global_cover import reconstruct_and_check
    A = np.zeros((243, 243), dtype=np.int64)
    for line in path.read_text().splitlines():
        if line.strip():
            u, v = map(int, line.split())
            A[u, v] = A[v, u] = 1
    assert np.all(A.sum(axis=1) == 22) and not np.any(np.diag(A))
    assert np.array_equal(A @ A + A, 20 * np.eye(243, dtype=np.int64) + 2 * np.ones_like(A))
    labels, gamma = extract_root(A.tolist(), 0)
    n = len(labels)
    model = cp_model.CpModel()
    graph = [[0] * n for _ in labels]
    zeros, ones = 0, 0
    for u, v in combinations(range(n), 2):
        if gamma[u][v] or (u < 12 and v < 12):
            e = model.new_bool_var(f'edge_{u}_{v}')
            model.add(e == gamma[u][v])
            graph[u][v] = graph[v][u] = e
            ones += gamma[u][v]
            zeros += 1 - gamma[u][v]
    # The full layer contains every constraint of the four nested layers.
    info = add_c2_layers(model, graph, labels, 4)
    expected = Counter(label_pair_layer(labels[u], labels[v]) for u, v in combinations(range(n), 2))
    assert info['equations_by_stratum'] == dict(expected)
    assert all(expected[i] > 0 for i in range(1, 5))
    assert not model.validate(), model.validate()
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = 30
    started = time.process_time()
    status = solver.solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE), solver.status_name(status)
    actual = [[solver.value(x) for x in row] for row in graph]
    assert actual == gamma
    reconstruct_and_check(22, labels, actual)
    return {'graph': str(path), 'status': solver.status_name(status),
            'exact_srg_verified': True, 'cpu_seconds': time.process_time() - started,
            'one_edges_as_boolean_variables': ones, 'zero_edges_as_boolean_variables': zeros,
            'all_four_strata_exercised': True, **info}


def control_rook_and_corruption():
    from ortools.sat.python import cp_model
    from root_component_c2_layers import add_c2_layers
    from conway_global_cover import reconstruct_and_check
    labels = [(0, 2), (0, 3), (1, 2), (1, 3)]
    model = cp_model.CpModel()
    graph = [[0] * 4 for _ in labels]
    for u, v in combinations(range(4), 2):
        graph[u][v] = graph[v][u] = model.new_bool_var(f'e_{u}_{v}')
    add_c2_layers(model, graph, labels, 4)
    for row in graph:
        model.add(sum(row) == 2)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = 5
    status = solver.solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    gamma = [[solver.value(e) for e in row] for row in graph]
    reconstruct_and_check(4, labels, gamma)
    u, v = next((u, v) for u, v in combinations(range(4), 2) if gamma[u][v])
    gamma[u][v] = gamma[v][u] = 0
    broken = cp_model.CpModel()
    add_c2_layers(broken, gamma, labels, 4)
    assert solver.solve(broken) == cp_model.INFEASIBLE
    return {'free_rook9_exact_srg': True, 'deleted_edge_rejected': True}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--graph', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    result = {'scope': __doc__, 'resources': resources,
              'legacy_equivalence': legacy_equivalence(),
              'rook9': control_rook_and_corruption(), 'srg243': control_243(a.graph),
              'full_Conway_Gram_model_positive_control': False,
              'status': 'C2_LAYERS_CONTROLS_PASSED'}
    atomic_json_write(a.output, result)
    print(json.dumps(result), flush=True)
