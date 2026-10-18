"""Realize one aggregate Z design as a binary Gamma, with all row orders free.

Each rectangle's four complete count rows may be assigned to its four
labelled vertices in any permutation. No Gram cover, prism budget or
matching normalization is used. An infeasible result excludes only this
aggregate design; it does not exclude its entire component template.
"""

import argparse
import hashlib
from itertools import permutations
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortools.sat.python import cp_model
from root_component_propagation import LABELS, PAIRS, RECTANGLES, constraints, propagate
from root_component_resources import atomic_json_write, limit_research_process


def build_lift(template, row_multisets, full_c2=False):
    propagated = propagate(template, use_c2=full_c2)
    if propagated['status'] == 'PROPAGATION_CONTRADICTION':
        return None, None, {'status': propagated['status'], 'propagation': propagated}
    initial = {PAIRS[i]: value for i, value, reason in propagated['assignments']}
    if full_c2:
        from conway_global_cover import build_global
        model, labels, graph, selectors, info = build_global(normalize_star=False, initial_edges=initial)
        assert tuple(labels) == LABELS and not selectors
    else:
        model = cp_model.CpModel()
        graph = [[0] * 84 for _ in range(84)]
        for u, v in PAIRS:
            graph[u][v] = graph[v][u] = initial[(u, v)] if (u, v) in initial else model.new_bool_var(f'e_{u}_{v}')
        info = {}
    equations, bounds, _ = constraints(template)
    for indices, target, reason in equations:
        model.add(sum(graph[PAIRS[i][0]][PAIRS[i][1]] for i in indices) == target)
    for indices, upper, reason in bounds:
        model.add(sum(graph[PAIRS[i][0]][PAIRS[i][1]] for i in indices) <= upper)
    rectangles = list(RECTANGLES)
    assert [list(q) for q in rectangles] == [item['rectangle'] for item in row_multisets]
    table_rows = []
    for qi, (q, item) in enumerate(zip(rectangles, row_multisets)):
        states = item['states']
        assert len(states) == 4 and all(len(row) == 21 for row in states)
        variables = []
        for w in RECTANGLES[q]:
            for f in rectangles:
                upper = 2 if set(q) & set(f) else 4
                z = model.new_int_var(0, upper, f'z_{w}_{f[0]}_{f[1]}')
                model.add(z == sum(graph[w][v] for v in RECTANGLES[f]))
                variables.append(z)
        rows = sorted({tuple(v for row in ordering for v in row) for ordering in permutations(states)})
        model.add_allowed_assignments(variables, rows)
        table_rows.append(len(rows))
    assert not model.validate(), model.validate()
    info.update(model_variables=len(model.proto.variables), model_constraints=len(model.proto.constraints),
                row_assignment_tables=table_rows, full_C2=full_c2)
    return model, graph, info


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--design', type=Path, required=True)
    p.add_argument('--full-c2', action='store_true')
    p.add_argument('--seconds', type=float, default=5)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    assert not a.output.exists()
    resources = limit_research_process(1)
    template = json.loads(a.bundle.read_text(encoding='utf-8-sig'))['template']
    design = json.loads(a.design.read_text(encoding='utf-8-sig'))['design']
    start = time.process_time()
    model, graph, info = build_lift(template, design['row_multisets'], a.full_c2)
    info.update(scope=__doc__, resources=resources, source_design=str(a.design),
                source_design_sha256=hashlib.sha256(a.design.read_bytes()).hexdigest(),
                build_cpu_seconds=time.process_time() - start,
                uses_Gram_cover=False, uses_prism_budget=False, whole_template_excluded=False,
                global_conway_exclusion=False, portable_unsat_proof=False)
    if model is not None:
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.cp_model_probing_level = 0
        solver.parameters.max_time_in_seconds = max(30, a.seconds * 100)
        started = time.process_time()
        done = threading.Event()
        def stop():
            while not done.wait(.05):
                if time.process_time() - started >= a.seconds:
                    solver.stop_search()
        timer = threading.Thread(target=stop, daemon=True)
        timer.start()
        try:
            status = solver.solve(model)
        finally:
            done.set()
            timer.join()
        info.update(status=solver.status_name(status), solver_cpu_seconds=time.process_time() - started,
                    branches=solver.num_branches, conflicts=solver.num_conflicts)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            adjacency = [[solver.value(x) for x in row] for row in graph]
            violations = []
            for u, v in PAIRS:
                value = sum(a * b for a, b in zip(adjacency[u], adjacency[v])) + adjacency[u][v]
                required = 2 - len(set(LABELS[u]) & set(LABELS[v]))
                if value != required:
                    violations.append([u, v, value, required])
            info.update(Gamma=adjacency, C2_violations=violations, exact_C2_violations=len(violations))
            if not violations:
                from conway_global_cover import reconstruct_and_check
                info['srg99'] = reconstruct_and_check(14, LABELS, adjacency)
                info['exact_srg_verified'] = True
            else:
                assert not a.full_c2
    atomic_json_write(a.output, info)
    print(json.dumps({k: v for k, v in info.items() if k not in
                      ('scope', 'resources', 'Gamma', 'C2_violations', 'srg99', 'propagation', 'coverage')}))


if __name__ == '__main__':
    main()
