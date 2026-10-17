"""Linear shared-neighbour completion of a fixed defect-core population.

All core/zero common-neighbour equations are simultaneous. Unless the final
integer SRG check succeeds, feasibility remains only a relaxation.
"""

from pathlib import Path
from itertools import combinations
from collections import deque
import argparse
import hashlib
import json
import time

from ortools.sat.python import cp_model


def propagate_equalities(equations):
    """Exact Boolean equality propagation, with a replayable reason per assignment."""
    incidence = {}
    for eid, eq in enumerate(equations):
        for v in eq['variables']:
            incidence.setdefault(v, []).append(eid)
    values, trace = {}, []
    pending = deque(range(len(equations)))
    while pending:
        eid = pending.popleft()
        eq = equations[eid]
        need = eq['rhs']-sum(values.get(v, 0) for v in eq['variables'])
        free = [v for v in eq['variables'] if v not in values]
        if need < 0 or need > len(free):
            return dict(status='CONTRADICTION', assignments=trace,
                        equation=eid, reason=eq['reason'], residual_rhs=need,
                        remaining_variables=len(free), equations=equations)
        if free and need in (0, len(free)):
            value = int(need != 0)
            for v in free:
                values[v] = value
                trace.append(dict(variable=v, value=value, equation=eid))
                pending.extend(incidence[v])
    return dict(status='FIXPOINT', assignment_count=len(trace), assignments=trace)


def complete(core, population, seconds=60, workers=4):
    q = core['charges']
    s = len(q)
    degree = core['parameters']['degree']
    core_n = [set() for _ in q]
    for i, j in core['edges']:
        core_n[i].add(j)
        core_n[j].add(i)
    rows, is_c = [], []
    for item in population['selected_rows']:
        for occurrence in range(item['count']):
            rows.append(set(item['vertices']))
            is_c.append(occurrence < item['coclique_count'])
    n = len(rows)
    in_column = [[z for z, row in enumerate(rows) if i in row] for i in range(s)]
    model = cp_model.CpModel()
    edges = {}
    for z, w in combinations(range(n), 2):
        if (is_c[z] and is_c[w]) or len(rows[z] & rows[w]) >= 2:
            edges[z, w] = 0
        else:
            edges[z, w] = model.NewBoolVar(f'd_{z}_{w}')

    def edge(z, w):
        return 0 if z == w else edges[tuple(sorted((z, w)))]

    equations = []

    def equation(z, columns, rhs, reason):
        columns = list(columns)
        model.Add(sum(edge(z, w) for w in columns) == rhs)
        variables = [f'{min(z,w)}_{max(z,w)}' for w in columns
                     if z != w and not isinstance(edge(z, w), int)]
        equations.append(dict(variables=variables, rhs=int(rhs), reason=reason))

    for z in range(n):
        equation(z, range(n), degree-len(rows[z]), ['degree', z])
        if not is_c[z]:
            # Zero charge off the coclique means exactly -s = 4 neighbours in it.
            assert degree in (4, 14)
            least_abs = 4 if degree == 14 else 2
            equation(z, (w for w in range(n) if is_c[w]), least_abs, ['coclique_degree', z])
        for i in range(s):
            rhs = 2-(i in rows[z])-len(core_n[i] & rows[z])
            equation(z, in_column[i], rhs, ['common_with_core', z, i])
    propagation = propagate_equalities(equations)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    started = time.monotonic()
    status = solver.Solve(model)
    result = dict(status=solver.StatusName(status), seconds=time.monotonic()-started,
                  zero_vertices=n, core_vertices=s,
                  branches=solver.NumBranches(), conflicts=solver.NumConflicts(),
                  propagation=propagation,
                  scope='Fixed population only; zero/zero common-neighbour equations not imposed',
                  response_stats=solver.ResponseStats())
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        selected = [(z, w) for (z, w), value in edges.items() if solver.Value(value)]
        all_n = [set(v) for v in core_n]+[set(row) for row in rows]
        for z, row in enumerate(rows):
            for i in row:
                all_n[i].add(s+z)
        for z, w in selected:
            all_n[s+z].add(s+w)
            all_n[s+w].add(s+z)
        assert all(len(row) == degree for row in all_n)
        violations = [[i, j, len(all_n[i] & all_n[j]), 2-(j in all_n[i])]
                      for i, j in combinations(range(s+n), 2)
                      if len(all_n[i] & all_n[j]) != 2-(j in all_n[i])]
        assert all(i >= s and j >= s for i, j, _, _ in violations)
        result['zero_edges'] = selected
        result['full_srg_check'] = not violations
        result['violations'] = violations
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('core', type=Path)
    parser.add_argument('population', type=Path)
    parser.add_argument('--seconds', type=float, default=60)
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    result = complete(json.loads(args.core.read_text()), json.loads(args.population.read_text()),
                      args.seconds, args.workers)
    result['core_sha256'] = hashlib.sha256(args.core.read_bytes()).hexdigest()
    result['population_sha256'] = hashlib.sha256(args.population.read_bytes()).hexdigest()
    output = args.population.with_name(args.population.stem+'_linear_completion.json')
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf8')
    print(json.dumps({k: result[k] for k in ('status', 'seconds', 'branches', 'conflicts')}), flush=True)


if __name__ == '__main__':
    main()
