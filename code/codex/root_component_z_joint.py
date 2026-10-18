"""Joint binary adjacency and row-state moments, without enumerating Grams.

The row catalogue supplies necessary component equations. Each vertex
chooses one complete count row; those counts are realized by the SAME
binary Gamma with the exact letter quotas. All rectangle moments are
linear in the state indicators. Optional signed component identities and
the intrarectangle C2 layer add couplings without choosing a Gram.
An infeasible model excludes the component template; a feasible model
still requires the full SRG check.
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
from conway_global_cover import reconstruct_and_check
from root_component_resources import atomic_json_write, limit_research_process


def build_joint(k, row_types, nongrid=None, fixed=None, *, row_moment_coordinates=None,
                diagnostics=None, short_columns=False, signed_template=None,
                signed_lines=None, signed_mode='boundary', mate_normalize=False, corner_c2=False,
                grid_c2=False, square_defects=False, component_energy=False):
    labels = [p for p in combinations(range(k), 2) if p[1] != (p[0] ^ 1)]
    rectangles = list(combinations(range(k // 2), 2))
    members = [[w for w, label in enumerate(labels) if tuple(a // 2 for a in label) == q] for q in rectangles]
    assert all(len(group) == 4 for group in members)
    assert [item['rectangle'] for item in row_types] == [list(q) for q in rectangles]
    n, m = len(labels), len(rectangles)
    model = cp_model.CpModel()
    forbidden = set()
    if square_defects:
        assert k == 14 and signed_template is not None
        from root_component_square_defect import forbidden_states
        forbidden, squares = forbidden_states(signed_template, row_types)
        if diagnostics is not None:
            diagnostics['square_defect_cuts'] = {'squares':squares,'forbidden_row_states':len(forbidden)}
    graph = [[0] * n for _ in range(n)]
    for u, v in combinations(range(n), 2):
        graph[u][v] = graph[v][u] = model.new_bool_var(f'e_{u}_{v}')
        if fixed is not None:
            model.add(graph[u][v] == fixed[u][v])
    for w, label in enumerate(labels):
        model.add(sum(graph[w]) == k - 2)
        for a in range(k):
            model.add(sum(graph[w][v] for v, other in enumerate(labels) if a in other)
                      == 2 - int(a in label) - int((a ^ 1) in label))
    if nongrid is not None:
        # The no-three-edge theorem here is Conway-specific.
        assert k == 14
        nongrid = {tuple(q) for q in nongrid}
        for q, group in zip(rectangles, members):
            if q in nongrid:
                model.add(sum(graph[u][v] for u, v in combinations(group, 2)) <= 2)
            else:
                for u, v in combinations(group, 2):
                    model.add(graph[u][v] == int(bool(set(labels[u]) & set(labels[v]))))
    aggregate = []
    row_terms = []
    selectors = [None]*n
    for qi, (group, item) in enumerate(zip(members, row_types)):
        states = item['states']
        choices = [[model.new_bool_var(f'row_{w}_{s}') for s in range(len(states))] for w in group]
        for w, selected in zip(group, choices):
            model.add_exactly_one(selected)
            for si, choice in enumerate(selected):
                if (qi,si) in forbidden:
                    model.add(choice == 0)
            if mate_normalize:
                selectors[w] = model.new_int_var(0,len(states)-1,f'row_selector_{w}')
                model.add(selectors[w] == sum(i*x for i,x in enumerate(selected)))
            for j, target in enumerate(members):
                model.add(sum(graph[w][v] for v in target)
                          == sum(x * state[j] for x, state in zip(selected, states)))
        aggregate += [(sum(row[s] for row in choices), state) for s, state in enumerate(states)]
        row_terms += [(qi, state, sum(row[s] for row in choices)) for s, state in enumerate(states)]
    if mate_normalize:
        # Root-line component data is unchanged by swapping its two letters.
        # A lexicographically least full state sequence satisfies all these
        # generator comparisons; no symmetry of the sought graph is assumed.
        label_index = {label:i for i,label in enumerate(labels)}
        for root in range(k//2):
            permutation = [label_index[tuple(sorted(a ^ int(a//2 == root) for a in pair))] for pair in labels]
            prefix = 1
            for u,v in enumerate(permutation):
                if u >= v:
                    continue
                model.add(selectors[u] <= selectors[v]).only_enforce_if(prefix)
                equal = model.new_bool_var(f'row_mate_eq_{root}_{u}')
                model.add(selectors[u] == selectors[v]).only_enforce_if(equal)
                model.add(selectors[u] != selectors[v]).only_enforce_if(equal.Not())
                if isinstance(prefix,int):
                    prefix = equal
                else:
                    both = model.new_bool_var(f'row_mate_prefix_{root}_{u}')
                    model.add(both <= prefix); model.add(both <= equal)
                    model.add(both >= prefix+equal-1); prefix = both
        if diagnostics is not None:
            diagnostics['mate_flip_state_normalization'] = True
    for i, j in combinations_with_replacement(range(m), 2):
        target = 4 * k + 8 if i == j else 24 if set(rectangles[i]) & set(rectangles[j]) else 32
        block = sum(graph[u][v] for u in members[i] for v in members[j])
        model.add(sum(count * state[i] * state[j] for count, state in aggregate
                      if state[i] and state[j]) + block == target)
    if short_columns:
        assert k == 14 and nongrid is not None, 'These -4 eigenvector bounds are Conway-specific.'
        from root_component_short_column_histograms import add_histogram_tables
        info = add_histogram_tables(model, rectangles, nongrid, row_terms)
        if diagnostics is not None:
            diagnostics['short_column_histograms'] = info
    if component_energy:
        assert k==14 and signed_template is not None
        from root_component_energy_implications import add_energy_implications
        counts=[[sum(graph[u][v] for u in left for v in right) for right in members] for left in members]
        info=add_energy_implications(model,counts,rectangles,signed_template)
        if diagnostics is not None:diagnostics['component_energy_implications']=info
    if row_moment_coordinates is not None:
        from root_component_row_neighbor_moments import add_row_moments
        row_info = add_row_moments(model, graph, labels, row_types, row_moment_coordinates, fixed=fixed)
        if diagnostics is not None:
            diagnostics['row_neighbor_moments'] = row_info
    if signed_lines is not None:
        from root_component_signed_components import add_signed_components
        assert signed_template is not None
        info = add_signed_components(model, graph, labels, signed_template, signed_lines, signed_mode)
        if diagnostics is not None:
            diagnostics['signed_components'] = info
    if corner_c2:
        from root_component_corner_c2 import add_corner_c2
        info = add_corner_c2(model,graph,labels)
        if diagnostics is not None:
            diagnostics['corner_C2'] = info
    if grid_c2:
        assert nongrid is not None
        from root_component_grid_c2 import add_grid_c2
        info = add_grid_c2(model, graph, labels, [q for q in rectangles if q not in nongrid], row_types)
        if diagnostics is not None:
            diagnostics['grid_C2'] = info
    assert not model.validate(), model.validate()
    return model, labels, graph


def solve_joint(model, labels, graph, k, seconds):
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.cp_model_probing_level = 0
    solver.parameters.max_time_in_seconds = max(30, seconds * 100)
    started = time.process_time()
    done = threading.Event()
    def stop():
        while not done.wait(.05):
            if time.process_time() - started >= seconds:
                solver.stop_search()
    timer = threading.Thread(target=stop, daemon=True)
    timer.start()
    try:
        status = solver.solve(model)
    finally:
        done.set()
        timer.join()
    result = {'status': solver.status_name(status), 'cpu_seconds': time.process_time() - started,
              'model_variables': len(model.proto.variables), 'model_constraints': len(model.proto.constraints),
              'branches': solver.num_branches, 'conflicts': solver.num_conflicts, 'portable_unsat_proof': False}
    if status == cp_model.INFEASIBLE and len(model.proto.assumptions):
        result['sufficient_assumptions'] = list(solver.sufficient_assumptions_for_infeasibility())
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        adjacency = [[solver.value(x) for x in row] for row in graph]
        violations = []
        for u, v in combinations(range(len(labels)), 2):
            actual = sum(a * b for a, b in zip(adjacency[u], adjacency[v])) + adjacency[u][v]
            required = 2 - len(set(labels[u]) & set(labels[v]))
            if actual != required:
                violations.append([u, v, actual, required])
        result.update(Gamma=adjacency, exact_C2_violations=len(violations), C2_violations=violations)
        if not violations:
            result['srg'] = reconstruct_and_check(k, labels, adjacency)
            result['exact_srg_verified'] = True
    return result


def controls(positive_edges, row_moments=False):
    records = []
    rook_rows = [{'rectangle': [0, 1], 'states': [[2]]}]
    diagnostic = {}
    model, labels, graph = build_joint(4, rook_rows, row_moment_coordinates=[0] if row_moments else None,
                                     diagnostics=diagnostic)
    result = solve_joint(model, labels, graph, 4, 5)
    assert result.get('exact_srg_verified')
    records.append({'graph': 'rook9', 'free_adjacency': True, 'status': result['status'],
                    'exact_C2_violations': 0, 'cpu_seconds': result['cpu_seconds'], **diagnostic})
    if positive_edges:
        from root_component_neighbor_moment_controls import extract_root
        import numpy as np
        edges = [tuple(map(int, row.split())) for row in positive_edges.read_text().splitlines() if row.strip()]
        size = max(max(e) for e in edges) + 1
        matrix = np.zeros((size, size), dtype=np.int64)
        for u, v in edges:
            matrix[u, v] = matrix[v, u] = 1
        assert size == 243 and np.all(matrix.sum(axis=1) == 22)
        assert np.array_equal(matrix @ matrix + matrix, 20 * np.eye(size, dtype=np.int64) + 2 * np.ones_like(matrix))
        labels, adjacency = extract_root(matrix.tolist(), 0)
        rectangles = list(combinations(range(11), 2))
        groups = [[w for w, label in enumerate(labels) if tuple(a // 2 for a in label) == q] for q in rectangles]
        row_types = [{'rectangle': list(q), 'states': [list(row) for row in sorted({tuple(sum(adjacency[w][v] for v in target)
                      for target in groups) for w in group})]} for q, group in zip(rectangles, groups)]
        diagnostic = {}
        model, labels2, graph = build_joint(22, row_types, fixed=adjacency,
                                          row_moment_coordinates=range(55) if row_moments else None,
                                          diagnostics=diagnostic)
        assert labels == labels2
        result = solve_joint(model, labels, graph, 22, 5)
        assert result.get('exact_srg_verified')
        records.append({'graph': str(positive_edges), 'fixed_boolean_adjacency': True, 'status': result['status'],
                        'rectangles': 55, 'moment_equations': 1540, 'cpu_seconds': result['cpu_seconds'],
                        'exact_C2_violations': 0, **diagnostic})
        if row_moments:
            # Exercise nonconstant Boolean-times-count products too: the graph
            # variables are fixed by constraints, but not replaced by constants
            # inside the new row-moment encoder.
            from root_component_row_neighbor_moments import add_row_moments
            model, labels2, graph = build_joint(22, row_types, fixed=adjacency)
            product_info = add_row_moments(model, graph, labels2, row_types, [0])
            assert product_info['boolean_integer_products'] > 0
            result = solve_joint(model, labels2, graph, 22, 5)
            assert result.get('exact_srg_verified')
            records.append({'graph': str(positive_edges), 'fixed_adjacency_as_boolean_variables': True,
                            'status': result['status'], 'cpu_seconds': result['cpu_seconds'],
                            'exact_C2_violations': 0, 'row_neighbor_moments': product_info})
    return {'status': 'POSITIVE_CONTROLS_PASSED', 'controls': records}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', type=Path)
    p.add_argument('--catalogue', type=Path)
    p.add_argument('--controls', action='store_true')
    p.add_argument('--positive-edges', type=Path)
    p.add_argument('--seconds', type=float, default=5)
    p.add_argument('--row-moments', action='store_true', help='Vertexwise C2 sums on catalogue free coordinates.')
    p.add_argument('--short-columns', action='store_true', help='Add Gram-free integral eigenvector histogram tables.')
    p.add_argument('--signed-lines', type=int, nargs='+', help='Root lines for LAB signed component identities.')
    p.add_argument('--signed-mode', choices=('norm','eigen','boundary'), default='boundary')
    p.add_argument('--mate-normalize', action='store_true', help='Choose a representative under the independent root-mate swaps.')
    p.add_argument('--corner-c2', action='store_true', help='Add the six individual C2 equations in every rectangle.')
    p.add_argument('--grid-c2', action='store_true', help='Add individual C2 against every grid corner.')
    p.add_argument('--square-defects', action='store_true', help='Use the saturation and parity lemma for defect squares.')
    p.add_argument('--component-energy',action='store_true')
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    if a.controls:
        result = controls(a.positive_edges, row_moments=a.row_moments)
    else:
        template = json.loads(a.bundle.read_text(encoding='utf-8-sig'))['template']
        catalogue = json.loads(a.catalogue.read_text(encoding='utf-8-sig'))['catalogue']
        assert catalogue['status'] == 'ROW_CATALOGUE_COMPLETE'
        start = time.process_time()
        diagnostic = {}
        from root_component_row_neighbor_moments import coordinates_for_catalogue
        coordinates = coordinates_for_catalogue(catalogue,template) if a.row_moments else None
        model, labels, graph = build_joint(14, catalogue['row_types'], template['nongrid_edges'],
                                          row_moment_coordinates=coordinates, diagnostics=diagnostic,
                                          short_columns=a.short_columns, signed_template=template,
                                          signed_lines=a.signed_lines, signed_mode=a.signed_mode,
                                          mate_normalize=a.mate_normalize,corner_c2=a.corner_c2,
                                          grid_c2=a.grid_c2,square_defects=a.square_defects,
                                          component_energy=a.component_energy)
        build_seconds = time.process_time() - start
        result = solve_joint(model, labels, graph, 14, a.seconds)
        result.update(build_cpu_seconds=build_seconds, source_bundle=str(a.bundle), source_catalogue=str(a.catalogue),
                      scope=__doc__, uses_Gram_cover=False, uses_prism_budget=False, individual_C2_encoded=a.corner_c2,
                      global_conway_exclusion=False, **diagnostic)
    result['resources'] = resources
    atomic_json_write(a.output, result)
    print(json.dumps({k: v for k, v in result.items() if k not in ('scope', 'resources', 'Gamma', 'C2_violations', 'srg')}))


if __name__ == '__main__':
    main()
