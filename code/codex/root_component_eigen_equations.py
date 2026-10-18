"""Shared signed Boolean-times-integer encoder for Gamma H equations.

The fixed-Gram Conway model uses Gamma H=-4H. On the actual SRG243,
the same rectangle-count H=W-Gamma P satisfies Gamma H=-4H+8(J-P).
For Y=H_F-H_G this becomes Gamma Y=-4Y+8(P_G-P_F), with both signs.
The positive control below exercises precisely the same signed encoder,
including its negative domains, with this correct inhomogeneous identity.
It does not assert that SRG243 has eigenvalue -4.
"""

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))


def add_eigen_equations(model, graph, values, bounds, eigenvalue=-4, offsets=None):
    n, d = len(graph), len(values[0])
    assert len(values) == len(bounds) == n
    products = 0
    for u in range(n):
        for i in range(d):
            terms = []
            for v in range(n):
                edge, h = graph[u][v], values[v][i]
                if isinstance(edge, int):
                    if edge:
                        terms.append(h)
                elif isinstance(h, int):
                    if h:
                        terms.append(h*edge)
                else:
                    lo, hi = bounds[v][i]
                    term = model.new_int_var(min(lo, 0), max(hi, 0), f'eh_{u}_{v}_{i}')
                    model.add(term == h).only_enforce_if(edge)
                    model.add(term == 0).only_enforce_if(edge.Not())
                    terms.append(term)
                    products += 1
            offset = offsets[u][i] if offsets is not None else 0
            model.add(sum(terms) == eigenvalue*values[u][i]+offset)
    return {'equations': n*d, 'boolean_integer_products': products,
            'bounds_source': 'Explicit Python bounds, no proto-domain reads.'}


def positive_control(path):
    from ortools.sat.python import cp_model
    import numpy as np
    from root_component_neighbor_moment_controls import extract_root
    from root_component_z_joint import solve_joint
    edges = [tuple(map(int, line.split())) for line in path.read_text().splitlines() if line.strip()]
    n = max(max(edge) for edge in edges)+1
    assert n == 243
    A = np.zeros((n, n), dtype=np.int64)
    for u, v in edges:
        A[u, v] = A[v, u] = 1
    assert np.all(A.sum(axis=1) == 22)
    assert np.array_equal(A@A+A, 20*np.eye(n, dtype=np.int64)+2*np.ones_like(A))
    labels, gamma = extract_root(A.tolist(), 0)
    rect, other = (0, 1), (0, 2)
    members = [v for v, label in enumerate(labels) if tuple(x//2 for x in label) == rect]
    other_members = [v for v, label in enumerate(labels) if tuple(x//2 for x in label) == other]
    model = cp_model.CpModel()
    graph = [[0]*len(labels) for _ in labels]
    for u, v in combinations(range(len(labels)), 2):
        graph[u][v] = graph[v][u] = model.new_bool_var(f'e_{u}_{v}')
        model.add(graph[u][v] == gamma[u][v])
    values, bounds, offsets, actual = [], [], [], []
    for w, label in enumerate(labels):
        q = tuple(x//2 for x in label)
        base = 2 if q == rect else 0 if set(q) & set(rect) else 1
        first_lo, first_hi = (0, 2) if q == rect else (-2, 0) if set(q) & set(rect) else (-3, 1)
        other_base = 2 if q == other else 0 if set(q) & set(other) else 1
        other_lo, other_hi = (0, 2) if q == other else (-2, 0) if set(q) & set(other) else (-3, 1)
        lo, hi = first_lo-other_hi, first_hi-other_lo
        h = base-sum(gamma[w][v] for v in members)-other_base+sum(gamma[w][v] for v in other_members)
        assert lo <= h <= hi
        actual.append(h)
        var = model.new_int_var(lo, hi, f'h_{w}')
        model.add(var == h)
        values.append([var]); bounds.append([(lo, hi)]); offsets.append([8*(int(q == other)-int(q == rect))])
    assert any(h < 0 for h in actual) and any(h > 0 for h in actual)
    assert all(sum(gamma[u][v]*actual[v] for v in range(len(labels)))
               == -4*actual[u]+offsets[u][0] for u in range(len(labels)))
    info = add_eigen_equations(model, graph, values, bounds, offsets=offsets)
    assert info['boolean_integer_products'] == len(labels)*(len(labels)-1)
    assert not model.validate(), model.validate()
    result = solve_joint(model, labels, graph, 22, 10)
    assert result.get('exact_srg_verified'), result['status']
    return {'status': 'POSITIVE_SIGNED_ENCODER_CONTROL_PASSED', 'source_graph': str(path),
            'identity': 'Gamma Y=-4Y+8(P_G-P_F), Y=H_F-H_G, for this actual SRG243',
            'conway_eigenvalue_asserted_for_243': False, 'shared_encoder': add_eigen_equations.__name__,
            **info, 'solver_status': result['status'], 'cpu_seconds': result['cpu_seconds'],
            'model_variables': result['model_variables'], 'model_constraints': result['model_constraints'],
            'exact_srg_verified': True, 'minimum_H': min(actual), 'maximum_H': max(actual)}


def main():
    from root_component_resources import limit_research_process, atomic_json_write
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--positive-edges', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    result = positive_control(a.positive_edges)
    result['resources'] = resources
    atomic_json_write(a.output, result)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
