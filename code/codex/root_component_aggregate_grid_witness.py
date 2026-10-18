"""An exact aggregate witness shows why the adjacency realization must remain.

This is a matrix of neighbour COUNTS, not an adjacency matrix. It realizes
the rectangle moment equations with all rectangle Grams zero. The complete
grid star is excluded elsewhere; the aggregate identities alone cannot
detect that obstruction after the actual adjacency variables are removed.
"""

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_neighbor_moments import root_rectangles
from root_component_resources import atomic_json_write, limit_research_process


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    labels = [p for p in combinations(range(14), 2) if p[1] != (p[0] ^ 1)]
    _, rectangles = root_rectangles(labels)
    qs = list(rectangles)
    row_qs = [tuple(x // 2 for x in label) for label in labels]
    incidence = np.array([[int(q == row) for q in qs] for row in row_qs], dtype=np.int64)
    z = np.array([[2 if row == q else 0 if set(row) & set(q) else 1
                   for q in qs] for row in row_qs], dtype=np.int64)
    k = incidence.T @ z
    target = np.array([[64 if q == f else 24 if set(q) & set(f) else 32
                        for f in qs] for q in qs], dtype=np.int64)
    assert np.array_equal(k, k.T)
    assert np.array_equal(z.T @ z + k, target)
    assert np.all(z.sum(axis=1) == 12) and np.all(z.sum(axis=0) == 48)
    assert np.all(np.diag(k) == 8)
    assert np.all((z * (z - 1) // 2).sum(axis=0) + np.diag(k) // 2 == 8)
    for w, root_pair in enumerate(row_qs):
        for line in range(7):
            assert sum(z[w, i] for i, q in enumerate(qs) if line in q) == (2 if line in root_pair else 4)
    atomic_json_write(a.output, {'scope': __doc__, 'status': 'EXACT_AGGREGATE_WITNESS',
                                'resources': resources, 'rectangles': [list(q) for q in qs],
                                'Z': z.tolist(), 'K': k.tolist(), 'is_graph': False,
                                'gram_R': 'zero', 'global_conway_exclusion': False})
    print(json.dumps({'status': 'EXACT_AGGREGATE_WITNESS', 'shape': list(z.shape), 'is_graph': False}))


if __name__ == '__main__':
    main()
