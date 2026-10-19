"""Exact root-cut layouts for K2BC, without enumerating LAB attachments.

The shared pair is Q01,Q02; the known grids are Q45,Q13,Q26.
This enumerates the 63 root subsets up to complementation, not graphs.
"""

from collections import Counter
from itertools import combinations, product
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process

if not __debug__:
    raise RuntimeError('Exact layout checks require assertions; do not use python -O.')

KNOWN = ((0, 1), (0, 2), (4, 5), (1, 3), (2, 6))
GRIDS = KNOWN[2:]
RECTANGLES = tuple(combinations(range(7), 2))


def base(q, f):
    return 2 if q == f else (0 if set(q) & set(f) else 1)


def layout(roots):
    roots = frozenset(roots)
    score = lambda q: 1 - len(roots.intersection(q))
    negative = [q for q in RECTANGLES if q not in KNOWN and score(q) == -1]
    positive = [q for q in RECTANGLES if q not in KNOWN and score(q) == 1]
    equations = []
    for q in sorted(negative + positive):
        ncore = base(q, (0, 1)) + base(q, (0, 2))
        constant = 12 - 4 * len(roots) + 2 * len(roots.intersection(q))
        constant -= score((0, 2)) * ncore
        constant -= sum(score(g) * base(q, g) for g in GRIDS)
        coefficient = score((0, 2)) - score((0, 1))
        if ncore == 0:
            coefficient = 0
        equations.append({'rectangle': q, 'constant': constant,
                          'coefficient_of_neighbours_in_Q01': coefficient,
                          'neighbours_in_Q01_plus_Q02': ncore})
    count = 4 * (len(negative) + len(positive))
    return {'roots': sorted(roots), 'negative_rectangles': negative,
            'positive_rectangles': positive, 'vertices': count,
            'edge_variables': count * (count - 1) // 2,
            'signed_equations': equations}


def overlap_report(layouts):
    all_edges, all_vertices = set(), set()
    raw_edges = 0
    for item in layouts:
        vertices = sorted((2 * i + a, 2 * j + b)
                          for i, j in item['negative_rectangles'] + item['positive_rectangles']
                          for a, b in product(range(2), repeat=2))
        edges = set(combinations(vertices, 2))
        all_vertices.update(vertices)
        all_edges.update(edges)
        raw_edges += len(edges)
    return {'vertices': len(all_vertices), 'distinct_edges': len(all_edges),
            'raw_edge_variables': raw_edges, 'edge_identifications': raw_edges - len(all_edges)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--positive-controls', action='store_true')
    parser.add_argument('--lab-source', type=Path,
                        help='Load only GEN definitions to test the targeted interface; never run its census.')
    args = parser.parse_args()
    assert not args.output.exists(), 'Keep the previous measurement; use a fresh output name.'
    resources = limit_research_process(1)
    start = time.process_time()
    all_layouts = [layout(s) for k in (1, 2, 3) for s in combinations(range(7), k)]
    smallest = min(d['vertices'] for d in all_layouts)
    best = [d for d in all_layouts if d['vertices'] == smallest]
    assert smallest == 20
    assert [d['roots'] for d in best] == [[0, 1, 3], [0, 2, 6], [3, 4, 5], [4, 5, 6]]
    fixed = [d for d in best if all(e['coefficient_of_neighbours_in_Q01'] == 0
                                  for e in d['signed_equations'])]
    assert [d['roots'] for d in fixed] == [[3, 4, 5], [4, 5, 6]]
    for d in fixed:
        assert Counter(e['constant'] for e in d['signed_equations']) == {1: 4, 0: 1}
        assert all(next(e['constant'] for e in d['signed_equations'] if e['rectangle'] == q) == 1
                   for q in d['negative_rectangles'])
    assert overlap_report(fixed) == {
        'vertices': 36, 'distinct_edges': 374, 'raw_edge_variables': 380, 'edge_identifications': 6}
    assert overlap_report(best)['distinct_edges'] == 622
    data = {'scope': 'Exact cut-layout algebra, not a family exclusion or an attachment census.',
            'known_rectangles': KNOWN, 'root_subsets_up_to_complement': len(all_layouts),
            'core_size_histogram': dict(sorted(Counter(d['vertices'] for d in all_layouts).items())),
            'minimum_core_size': smallest, 'minimizers': best,
            'original_S012': layout([0, 1, 2]),
            'two_constant_cores': overlap_report(fixed), 'four_minimum_cores': overlap_report(best),
            'resources': resources}
    data['encoder_sha256'] = hashlib.sha256(
        Path(__file__).with_name('root_component_signed_internal_core.py').read_bytes()).hexdigest()
    if args.positive_controls:
        from root_component_signed_internal_core import controls
        data['two_core_srg243_control'] = controls(root_subsets=[d['roots'] for d in fixed])
        data['four_core_srg243_control'] = controls(root_subsets=[d['roots'] for d in best])
    if args.lab_source:
        # Execute definitions only. No boundary file or attachment enumeration is read/run.
        raw = args.lab_source.read_bytes()
        source = raw.decode('utf-8-sig')
        assert source.count('\nOUT = next(') == 1
        assert source.count("            out['status'] = 'SAT_KNOWN_ROWS_COMPLETE'") == 1
        assert source.count('        ans = s.solve_limited()') == 1
        previous = sys.argv[:]
        try:
            sys.argv = [str(args.lab_source), str(Path(__file__).resolve().parent),
                        'GEN', 'UNREAD_BOUNDARY.json.gz', '0', '1',
                        '--yr=45', '--extra=13,26', '--sat', '--lean']
            ns = {'__name__': 'gen_definitions_only', '__file__': str(args.lab_source)}
            exec(compile(source.split('\nOUT = next(')[0], str(args.lab_source), 'exec'), ns)
        finally:
            sys.argv = previous
        assert tuple(ns['RECT']) == KNOWN
        assert len(ns['LABELS']) == 20 and len(ns['OUTSIDE']) == 64
        assert len(ns['MATCH_BLOCKS']) == 5 and not ns['Q12K'] and not ns['YY']
        archive = args.output.with_suffix('.lab_source.py.gz')
        archive.write_bytes(gzip.compress(raw, mtime=0))
        data['lab_gen_interface'] = {
            'source_sha256': hashlib.sha256(raw).hexdigest(), 'matching_blocks': ns['MATCH_BLOCKS'],
            'source_archive': str(archive),
            'known_vertices': 20, 'outside_vertices': 64,
            'census_or_sat_run': False, 'hook_markers_present': True}
    data['cpu_seconds'] = time.process_time() - start
    atomic_json_write(args.output, data, indent=2)
    print(json.dumps({k: data[k] for k in ('minimum_core_size', 'two_constant_cores',
                                          'four_minimum_cores', 'cpu_seconds')}))


if __name__ == '__main__':
    main()
