"""Search for ONE moment polynomial separating every nonempty Gram case.

The earlier corner report identifies cases with no local realization.
For all other cases, seek common coefficients and certify each resulting
inequality with exact integers. NOT_FOUND does not prove impossibility
of a common certificate. This is explanatory research, not a new SAT run.
"""

import argparse
from fractions import Fraction
from functools import reduce
import gzip
import hashlib
from itertools import combinations_with_replacement
import json
import math
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortools.linear_solver import pywraplp
from root_component_corner_moment_bounds import corner_data
from root_component_corner_moment_separation import certify_coefficients
from root_component_resources import atomic_json_write, limit_research_process


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover', type=Path, required=True)
    p.add_argument('--bounds', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    start = time.process_time()
    blob = a.cover.read_bytes()
    cover = json.loads(gzip.decompress(blob) if a.cover.suffix == '.gz' else blob)
    report = json.loads(a.bounds.read_text(encoding='utf-8-sig'))
    assert report['source_sha256'] == hashlib.sha256(blob).hexdigest()
    assert report['all_received_grams_tested']
    edges = cover.get('edges', cover.get('edge_order'))
    pairs = list(combinations_with_replacement(cover['anchors'], 2))
    selected = [c['gram_selector'] for c in report['cases'] if not c['empty_rectangles']]
    solver = pywraplp.Solver.CreateSolver('GLOP')
    solver.SetTimeLimit(10000)
    inf = solver.infinity()
    weights = [solver.NumVar(-inf, inf, f'c_{i}') for i in range(len(pairs))]
    norms = [solver.NumVar(0, inf, f'a_{i}') for i in range(len(pairs))]
    for c, n in zip(weights, norms):
        solver.Add(n >= c)
        solver.Add(n >= -c)
    prepared = []
    for gi in selected:
        matrix, _, domains, tables = corner_data(edges, cover['grams'][gi])
        assert all(t['rows'] for t in tables)
        target = [7 * int(matrix[i, j]) for i, j in pairs]
        vectors, rectangles = [], []
        for table in tables:
            q = tuple(table['rectangle'])
            hs = domains[q]['signatures']
            vectors.append(sorted({tuple(sum(hs[s][i] * hs[s][j] for s in row[:4])
                                         for i, j in pairs) for row in table['rows']}))
            rectangles.append(q)
        minima = [solver.NumVar(-inf, inf, f'b_{gi}_{q}') for q in range(21)]
        for q, choices in enumerate(vectors):
            for vector in choices:
                solver.Add(minima[q] <= sum(c * x for c, x in zip(weights, vector)))
        solver.Add(sum(minima) - sum(c * x for c, x in zip(weights, target)) >= 1)
        prepared.append((gi, target, vectors, rectangles))
    solver.Minimize(sum(norms))
    status = solver.Solve()
    result = {'scope': __doc__, 'source_cover': str(a.cover), 'source_bounds': str(a.bounds),
              'source_sha256': report['source_sha256'], 'selected_grams': selected,
              'lp_status_code': status, 'status': 'NOT_FOUND', 'resources': resources,
              'global_conway_exclusion': False}
    if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        values = [c.solution_value() for c in weights]
        for limit in (1, 2, 5, 10, 100, 10000):
            rational = [Fraction(c).limit_denominator(limit) for c in values]
            den = math.lcm(*(c.denominator for c in rational))
            integer = [int(c * den) for c in rational]
            divisor = reduce(math.gcd, integer, 0) or 1
            integer = [c // divisor for c in integer]
            certificates = [certify_coefficients(pairs, integer, target, vectors, rectangles)
                            for gi, target, vectors, rectangles in prepared]
            if all(certificates):
                for (gi, *_), certificate in zip(prepared, certificates):
                    certificate['gram_selector'] = gi
                result.update(status='COMMON_INTEGER_CERTIFICATE', certificates=certificates)
                break
    result['cpu_seconds'] = time.process_time() - start
    atomic_json_write(a.output, result)
    print(json.dumps({k: v for k, v in result.items() if k not in ('certificates', 'scope', 'resources')}))
    if result.get('certificates'):
        print(json.dumps({'common_terms': result['certificates'][0]['terms'],
                          'gaps': [c['gap'] for c in result['certificates']]}))


if __name__ == '__main__':
    main()
