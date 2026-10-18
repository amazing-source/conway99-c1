"""Small integer design of complete neighbour-count rows, with no Gram cover.

Each root rectangle has four vertices. Choose multiplicities of complete
count vectors z satisfying its component equations, then impose symmetry
of K=P^t Z and Z^t Z+K=D. All moment equations are LINEAR in these
multiplicities. A feasible design is a relaxation, not an adjacency graph.
"""

import argparse
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortools.sat.python import cp_model
from root_component_z_distribution import RECTANGLES, row_catalogue
from root_rectangle_domains import corner_graphs
from root_component_resources import atomic_json_write, limit_research_process


def solve_design(template, catalogue, seconds=5, exclude_three_edges=False, short_columns=False,
                 eigen_directions=None):
    assert catalogue['status'] == 'ROW_CATALOGUE_COMPLETE'
    model = cp_model.CpModel()
    states = [item['states'] for item in catalogue['row_types']]
    counts = [[model.new_int_var(0, 4, f'n_{qi}_{si}') for si in range(len(rows))]
              for qi, rows in enumerate(states)]
    k = [[sum(n * row[j] for n, row in zip(counts[i], states[i])) for j in range(21)]
         for i in range(21)]
    nongrid = {tuple(e) for e in template['nongrid_edges']}
    for qi, q in enumerate(RECTANGLES):
        model.add(sum(counts[qi]) == 4)
        degree_counts = [model.new_int_var(0, 4, f'own_degree_{qi}_{v}') for v in range(3)]
        for v, count in enumerate(degree_counts):
            model.add(count == sum(n for n, row in zip(counts[qi], states[qi]) if row[qi] == v))
        permitted = set()
        for e in range(3 if exclude_three_edges else 4) if q in nongrid else (4,):
            for _, _, hs in corner_graphs(e):
                degrees = [2 - h for h in hs]
                permitted.add(tuple(degrees.count(v) for v in range(3)))
        model.add_allowed_assignments(degree_counts, sorted(permitted))
    for i, j in combinations(range(21), 2):
        model.add(k[i][j] == k[j][i])
    for i, j in combinations_with_replacement(range(21), 2):
        target = 64 if i == j else 24 if set(RECTANGLES[i]) & set(RECTANGLES[j]) else 32
        quadratic_sum = sum(n * row[i] * row[j]
                            for rows, ns in zip(states, counts) for row, n in zip(rows, ns))
        model.add(quadratic_sum + k[i][j] == target)
    histogram_info = None
    if short_columns:
        assert exclude_three_edges, 'The short-column tables use the universal E3 exclusion.'
        from root_component_short_column_histograms import add_histogram_tables
        terms = [(qi, row, n) for qi, (rows, ns) in enumerate(zip(states, counts)) for row, n in zip(rows, ns)]
        histogram_info = add_histogram_tables(model, RECTANGLES, nongrid, terms)
    direction_info = None
    if eigen_directions:
        from root_component_variable_norm_cuts import add_direction_cuts
        terms = [(qi, row, n) for qi, (rows, ns) in enumerate(zip(states, counts)) for row, n in zip(rows, ns)]
        direction_info = add_direction_cuts(model, RECTANGLES, terms, eigen_directions)
    assert not model.validate(), model.validate()
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = max(30, seconds * 100)
    start = time.process_time()
    done = threading.Event()
    def stop():
        while not done.wait(.05):
            if time.process_time() - start >= seconds:
                solver.stop_search()
    timer = threading.Thread(target=stop, daemon=True)
    timer.start()
    try:
        status = solver.solve(model)
    finally:
        done.set()
        timer.join()
    result = {'status': solver.status_name(status), 'cpu_seconds': time.process_time() - start,
              'variables': len(model.proto.variables), 'constraints': len(model.proto.constraints),
              'branches': solver.num_branches, 'conflicts': solver.num_conflicts,
              'is_adjacency_graph': False, 'uses_gram_cover': False, 'uses_prism_budget': False,
              'uses_universal_E3_exclusion': exclude_three_edges,
              'portable_unsat_proof': False}
    if histogram_info is not None:
        result['short_column_histograms'] = histogram_info
    if direction_info is not None:
        result['variable_norm_cuts'] = direction_info
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        selected = [[(row, solver.value(n)) for row, n in zip(rows, ns) if solver.value(n)]
                    for rows, ns in zip(states, counts)]
        result['row_multisets'] = [{'rectangle': list(q), 'states': [row for row, count in rows for _ in range(count)]}
                                 for q, rows in zip(RECTANGLES, selected)]
        # Check the aggregate witness in ordinary integer arithmetic.
        z = [row for group in result['row_multisets'] for row in group['states']]
        kk = [[sum(row[j] for row in result['row_multisets'][i]['states']) for j in range(21)] for i in range(21)]
        assert len(z) == 84
        for i, j in combinations_with_replacement(range(21), 2):
            target = 64 if i == j else 24 if set(RECTANGLES[i]) & set(RECTANGLES[j]) else 32
            assert kk[i][j] == kk[j][i]
            assert sum(row[i] * row[j] for row in z) + kk[i][j] == target
        result['aggregate_witness_checked_exactly'] = True
        if short_columns:
            from root_component_short_column_histograms import check_witness
            result['short_column_witness_checked_exactly'] = check_witness(result['row_multisets'], nongrid)
        if eigen_directions:
            from root_component_short_column_histograms import h_value
            from root_component_variable_norm_cuts import scalar_violations
            row_rectangles = [q for q in RECTANGLES for _ in range(4)]
            for d in eigen_directions:
                values = [sum(c*h_value(q, RECTANGLES[j], row[j]) for j, c in d)
                          for q, group in zip(RECTANGLES, result['row_multisets']) for row in group['states']]
                assert not scalar_violations(values, row_rectangles)
            result['variable_norm_witness_checked_exactly'] = True
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', type=Path)
    p.add_argument('--all-grid-control', action='store_true')
    p.add_argument('--e3', action='store_true', help='Use the established universal exclusion of three-edge rectangles.')
    p.add_argument('--short-columns', action='store_true', help='Add Gram-free integral eigenvector histogram tables.')
    p.add_argument('--seconds', type=float, default=5)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists() and bool(a.bundle) != a.all_grid_control
    resources = limit_research_process(1)
    template = {'nongrid_edges': [], 'nontrivial_component_groups': [[] for _ in range(7)]} if a.all_grid_control else json.loads(a.bundle.read_text(encoding='utf-8-sig'))['template']
    start = time.process_time()
    catalogue = row_catalogue(template)
    result = {'scope': __doc__, 'resources': resources, 'source_bundle': str(a.bundle),
              'all_grid_control': a.all_grid_control, 'free_dimension': catalogue.get('free_dimension'),
              'row_state_counts': [r['state_count'] for r in catalogue.get('row_types', [])],
              'catalogue_cpu_seconds': time.process_time() - start, 'global_conway_exclusion': False}
    if catalogue['status'] == 'ROW_CATALOGUE_COMPLETE':
        result['design'] = solve_design(template, catalogue, a.seconds, a.e3, a.short_columns)
    else:
        result['catalogue_status'] = catalogue['status']
    atomic_json_write(a.output, result)
    print(json.dumps({k: v for k, v in result.get('design', {}).items() if k != 'row_multisets'}))


if __name__ == '__main__':
    main()
