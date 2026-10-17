"""Explain a fixed partial Conway matrix by exact cardinality propagation.

For fixed complete rows F and remaining rows U, write Gamma=[A B; B^t E].
The unknown symmetric binary block E must satisfy its residual root counts
and B E = 2 J - root_intersections(F,U) - A B - B. These are necessary
linear conditions, not a sufficient construction of Gamma. Saturated
common-neighbour budgets also forbid some edges and pairs of neighbours.

All propagation below uses integers. Certificates can be replayed without
CP-SAT. A contradiction excludes only the supplied fixed frame.
"""
import argparse
from collections import deque
from itertools import combinations
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conway_star_extension import read_frame


def build_system(labels, fixed, saturated_pairs=False):
    unknown = [i for i in range(len(labels)) if i not in fixed]
    edges = list(combinations(unknown, 2))
    index = {edge: i for i, edge in enumerate(edges)}
    constraints = []

    def term(z, q):
        if z == q:
            return None, 0
        if z in fixed:
            return None, fixed[z][q]
        if q in fixed:
            return None, fixed[q][z]
        return index[tuple(sorted((z, q)))], 0

    def add(positions, lower, upper, reason):
        variables = []
        constant = 0
        for z, q in positions:
            variable, value = term(z, q)
            constant += value
            if variable is not None:
                variables.append(variable)
        assert len(variables) == len(set(variables))
        if not variables and lower <= constant <= upper:
            return
        constraints.append(dict(variables=variables, lower=lower-constant,
                                upper=upper-constant, reason=reason))

    saturated = []
    for q, w in combinations(range(len(labels)), 2):
        common = sum(row[q] * row[w] for row in fixed.values())
        shared = len(set(labels[q]) & set(labels[w]))
        capacity = 2 - common - shared
        known_edge = fixed[q][w] if q in fixed else fixed[w][q] if w in fixed else None
        if known_edge is None and capacity < 1:
            add([(q, w)], 0, capacity,
                dict(kind='edge_capacity', pair=[labels[q], labels[w]],
                     fixed_common=common, root_common=shared))
        used = common + shared + (known_edge or 0)
        if used > 2:
            add([], 0, 2-used, dict(kind='already_over_capacity', pair=[labels[q], labels[w]]))
        elif used == 2:
            saturated.append((q, w))
    for z in unknown:
        add([(z, q) for q in range(len(labels))], 12, 12,
            dict(kind='degree', row=labels[z]))
        for r in range(14):
            target = 2-int(r in labels[z])-int((r ^ 1) in labels[z])
            add([(z, q) for q, p in enumerate(labels) if r in p], target, target,
                dict(kind='root_count', row=labels[z], root=r, target=target))
        for p, prow in fixed.items():
            target = 2-len(set(labels[z]) & set(labels[p]))-prow[z]
            add([(z, q) for q in range(len(labels)) if prow[q]], target, target,
                dict(kind='common_with_fixed', row=labels[z], other=labels[p], target=target))
    if saturated_pairs:
        for z in unknown:
            for q, w in saturated:
                if z not in (q, w):
                    add([(z, q), (z, w)], 0, 1,
                        dict(kind='saturated_pair', row=labels[z], pair=[labels[q], labels[w]]))
    return edges, constraints


def propagate(edges, constraints):
    values = [-1] * len(edges)
    occurrences = [[] for _ in edges]
    for ci, constraint in enumerate(constraints):
        for v in constraint['variables']:
            occurrences[v].append(ci)
    queue = deque(range(len(constraints)))
    queued = set(queue)
    trail = []
    proof_of = {}
    conflict = None
    while queue:
        ci = queue.popleft()
        queued.remove(ci)
        constraint = constraints[ci]
        variables = constraint['variables']
        ones = [v for v in variables if values[v] == 1]
        zeros = [v for v in variables if values[v] == 0]
        free = [v for v in variables if values[v] < 0]
        lo, hi = len(ones), len(ones)+len(free)
        if lo > constraint['upper'] or hi < constraint['lower']:
            dependencies = ones if lo > constraint['upper'] else zeros
            conflict = dict(constraint=ci, possible_lower=lo, possible_upper=hi,
                            dependencies=[proof_of[v] for v in dependencies])
            break
        forced = 0 if lo == constraint['upper'] else 1 if hi == constraint['lower'] else None
        if forced is None:
            continue
        dependencies = ones if forced == 0 else zeros
        for v in free:
            proof_of[v] = len(trail)
            trail.append(dict(variable=v, value=forced, constraint=ci,
                              dependencies=[proof_of[w] for w in dependencies]))
            values[v] = forced
            for other in occurrences[v]:
                if other not in queued:
                    queue.append(other)
                    queued.add(other)
    result = dict(status='EXACT_PROPAGATION_CONTRADICTION' if conflict else 'PROPAGATION_FIXED_POINT',
                  edge_count=len(edges), constraint_count=len(constraints),
                  forced_zero=values.count(0), forced_one=values.count(1), remaining=values.count(-1),
                  values=values, trail=trail)
    if conflict:
        needed = set()
        stack = list(conflict['dependencies'])
        while stack:
            step = stack.pop()
            if step not in needed:
                needed.add(step)
                stack.extend(trail[step]['dependencies'])
        kept = sorted(needed)
        used = sorted({conflict['constraint']} | {trail[i]['constraint'] for i in kept})
        constraint_ids = {old:new for new,old in enumerate(used)}
        step_ids = {old:new for new,old in enumerate(kept)}
        result['certificate'] = dict(
            constraints=[constraints[i] for i in used],
            steps=[dict(variable=trail[i]['variable'], value=trail[i]['value'],
                        constraint=constraint_ids[trail[i]['constraint']],
                        dependencies=[step_ids[j] for j in trail[i]['dependencies']]) for i in kept],
            contradiction=dict(conflict, constraint=constraint_ids[conflict['constraint']],
                               dependencies=[step_ids[i] for i in conflict['dependencies']]))
        replay_certificate(result['certificate'])
    return result


def replay_certificate(certificate):
    """Check the arithmetic of our own extracted proof; no solver needed."""
    values = {}
    for step in certificate['steps']:
        row = certificate['constraints'][step['constraint']]
        assert step['variable'] in row['variables'] and step['variable'] not in values
        lo = sum(values.get(v, 0) for v in row['variables'])
        hi = sum(values.get(v, 1) for v in row['variables'])
        assert row['lower'] <= hi and lo <= row['upper']
        assert (step['value'] == 0 and lo == row['upper']) or (step['value'] == 1 and hi == row['lower'])
        values[step['variable']] = step['value']
    row = certificate['constraints'][certificate['contradiction']['constraint']]
    lo = sum(values.get(v, 0) for v in row['variables'])
    hi = sum(values.get(v, 1) for v in row['variables'])
    assert lo > row['upper'] or hi < row['lower']
    return True


def solve_relaxation(labels, fixed, seconds=2, saturated_pairs=False):
    """Complete the whole binary block under the necessary linear system.

    A feasible result does NOT enforce the C2 equations between two rows
    outside fixed. It is recorded as a relaxation witness, never as a graph.
    """
    from ortools.sat.python import cp_model
    edges, constraints = build_system(labels, fixed, saturated_pairs)
    propagation = propagate(edges, constraints)
    if 'certificate' in propagation:
        return dict(status='INFEASIBLE', method='exact_integer_propagation',
                    seconds=0, propagation=propagation)
    model = cp_model.CpModel()
    variables = [model.NewBoolVar('e_%d_%d' % edge) for edge in edges]
    for row in constraints:
        model.AddLinearConstraint(sum(variables[v] for v in row['variables']), row['lower'], row['upper'])
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = seconds
    status = solver.Solve(model)
    result = dict(status=solver.StatusName(status), method='binary_linear_relaxation',
                  seconds=solver.WallTime(), constraints=len(constraints), variables=len(edges),
                  saturated_pairs=saturated_pairs)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        values = [solver.Value(v) for v in variables]
        for row in constraints:
            total = sum(values[v] for v in row['variables'])
            assert row['lower'] <= total <= row['upper']
        matrix = [[0]*len(labels) for _ in labels]
        for p, row in fixed.items():
            for q, value in enumerate(row):
                matrix[p][q] = matrix[q][p] = value
        for (p,q), value in zip(edges, values):
            matrix[p][q] = matrix[q][p] = value
        for p,row in enumerate(matrix):
            assert row[p] == 0 and sum(row) == 12
            for r in range(14):
                assert sum(row[q] for q,lab in enumerate(labels) if r in lab) == 2-int(r in labels[p])-int((r ^ 1) in labels[p])
        mismatches = []
        for p,q in combinations(range(len(labels)), 2):
            observed = sum(a*b for a,b in zip(matrix[p],matrix[q]))+matrix[p][q]+len(set(labels[p])&set(labels[q]))
            if observed != 2:
                mismatches.append(dict(pair=[labels[p],labels[q]],observed=observed))
        result['binary_relaxation'] = dict(labels=labels, rows=matrix, c2_violation_count=len(mismatches),
                                           c2_violations=mismatches, is_graph84=(not mismatches))
    return result


def run(source, output, saturated_pairs=False):
    started = time.monotonic()
    labels, fixed = read_frame(source)
    edges, constraints = build_system(labels, fixed, saturated_pairs)
    result = propagate(edges, constraints)
    result.update(source_file=str(source), fixed_row_labels=[labels[z] for z in sorted(fixed)],
                  edge_labels=[[labels[z], labels[q]] for z,q in edges], saturated_pairs=saturated_pairs,
                  scope='Necessary conditions with exactly this frame fixed. Not an exclusion of all Conway frames.',
                  seconds=time.monotonic()-started)
    Path(output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('trail','values','edge_labels','certificate')}, ensure_ascii=False), flush=True)
    if 'certificate' in result:
        proof = result['certificate']
        print(json.dumps(dict(proof_constraints=len(proof['constraints']), proof_steps=len(proof['steps']),
                              contradiction=proof['constraints'][proof['contradiction']['constraint']]), ensure_ascii=False), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--saturated-pairs', action='store_true')
    args = parser.parse_args()
    run(args.source, args.output, args.saturated_pairs)
