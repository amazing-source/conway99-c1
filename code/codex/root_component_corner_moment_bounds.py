"""Exact cornerwise bounds on H^t H=7R, with no adjacency search.

For a supplied rectangle Gram R, enumerate every integral vertex signature
and every binary four-corner realization passing the necessary Schur test.
If b_q(i,j) is the largest sum of h_i*h_j in a rectangle q, every Conway
completion satisfies 7R_ij <= sum_q b_q(i,j). The analogous lower bound
also holds. A strict violation is an integer arithmetic obstruction.

This filter does not use the complementary projector, short-vector cuts,
or a prism budget. A supplied finite Gram cover may itself depend on a
root budget. Passing this filter does not provide a graph or a completion.
"""

import argparse
from collections import Counter
import hashlib
import gzip
from itertools import combinations_with_replacement
import json
from pathlib import Path
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_corner_tables import enumerate_corner_rows
from root_component_gram_enumeration import integer_psd
from root_component_resources import atomic_json_write, limit_research_process
from root_rectangle_domains import signature_domains


def corner_data(edges, raw):
    """Enumerate a superset of all genuine corner states, exactly over Q."""
    edges = [tuple(e) for e in edges]
    matrix = sp.Matrix(raw)
    assert matrix.shape == (len(edges), len(edges))
    assert len(set(edges)) == len(edges)
    assert matrix == matrix.T and all(x.q == 1 for x in matrix)
    assert integer_psd(matrix.tolist())
    anchors = list(matrix.rref()[1])
    if not 1 <= len(anchors) <= 5:
        raise ValueError('This finite enumerator supports ranks 1 through 5.')
    domains = {tuple(d['rectangle']): d for d in signature_domains(edges, raw)}
    small = matrix.extract(anchors, anchors)
    det = int(small.det())
    adj = [[int(x) for x in row] for row in (small.inv() * det).tolist()]
    tables = enumerate_corner_rows(edges, matrix, domains, anchors, det, adj)
    return matrix, anchors, domains, tables


def moment_ranges(matrix, anchors, domains, tables):
    """Bounds are sums of separate extrema; no coupling is assumed."""
    assert all(t['rows'] for t in tables)
    reports = []
    for i, j in combinations_with_replacement(anchors, 2):
        rectangles = []
        for table in tables:
            signatures = domains[tuple(table['rectangle'])]['signatures']
            values = [sum(signatures[s][i] * signatures[s][j] for s in row[:4])
                      for row in table['rows']]
            rectangles.append({'rectangle': list(table['rectangle']),
                               'minimum': min(values), 'maximum': max(values)})
        lower = sum(r['minimum'] for r in rectangles)
        upper = sum(r['maximum'] for r in rectangles)
        target = 7 * int(matrix[i, j])
        reports.append({'coordinates': [i, j], 'required_moment': target,
                        'lower_bound': lower, 'upper_bound': upper,
                        'contradiction': not lower <= target <= upper,
                        'gap': max(0, lower - target, target - upper),
                        'rectangle_bounds': rectangles})
    return reports


def analyze_gram(edges, raw):
    """Public filter API. EXCLUDED is sound; PASSES is only inconclusive."""
    started = time.process_time()
    matrix, anchors, domains, tables = corner_data(edges, raw)
    empty = [list(t['rectangle']) for t in tables if not t['rows']]
    reports = [] if empty else moment_ranges(matrix, anchors, domains, tables)
    contradictions = [r for r in reports if r['contradiction']]
    result = {'status': 'EXCLUDED' if empty or contradictions else 'PASSES',
              'rank': len(anchors), 'anchors': anchors,
              'empty_rectangles': empty,
              'signature_count': sum(len(d['signatures']) for d in domains.values()),
              'corner_row_count': sum(len(t['rows']) for t in tables),
              'corner_row_counts': [{'rectangle': list(t['rectangle']), 'count': len(t['rows'])}
                                    for t in tables],
              'checked_moment_count': len(reports),
              'moment_contradictions': contradictions,
              'cpu_seconds': time.process_time() - started,
              'solver_used': False}
    for report in contradictions:
        report['coordinate_rectangles'] = [list(edges[i]) for i in report['coordinates']]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--index', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists()
    resources = limit_research_process(1)
    blob = args.bundle.read_bytes()
    text = gzip.decompress(blob).decode('utf-8-sig') if args.bundle.suffix == '.gz' else blob.decode('utf-8-sig')
    bundle = json.loads(text)
    assert bundle['gram_count'] == len(bundle['grams']) and bundle['gram_count'] > 0
    if 'status' in bundle:
        assert bundle['status'] == 'COMPLETE'
    if 'template_index' in bundle:
        assert bundle['template_index'] == args.index
    edges = [tuple(e) for e in bundle.get('edge_order', bundle.get('edges'))]
    result = {'scope': __doc__, 'template_index': args.index,
              'source_bundle': str(args.bundle),
              'source_sha256': hashlib.sha256(args.bundle.read_bytes()).hexdigest(),
              'received_cover_scope': bundle.get('scope', 'LAB complete Gram cover, c3 root budget <=51.'),
              'cover_completeness': 'Accepted LAB result; not re-enumerated here.',
              'resources': resources, 'cases': [], 'global_conway_exclusion': False}
    for gi, raw in enumerate(bundle['grams']):
        case = analyze_gram(edges, raw)
        case['gram_selector'] = gi
        result['cases'].append(case)
        atomic_json_write(args.output, result)
        print(json.dumps({'gram_selector': gi, 'status': case['status'],
                          'cpu_seconds': case['cpu_seconds'],
                          'empty_rectangles': case['empty_rectangles'],
                          'moment_contradictions': [
                              {k: r[k] for k in ('coordinates', 'required_moment',
                                                'lower_bound', 'upper_bound', 'gap')}
                              for r in case['moment_contradictions']]}), flush=True)
    result['counts'] = dict(Counter(c['status'] for c in result['cases']))
    result['all_received_grams_excluded'] = all(c['status'] == 'EXCLUDED' for c in result['cases'])
    result['cpu_seconds_total'] = sum(c['cpu_seconds'] for c in result['cases'])
    atomic_json_write(args.output, result)


if __name__ == '__main__':
    main()
