"""Require one common population of zero-charge vertices around a defect core.

This is a necessary binary Gram-factorization test. Every actual completion
supplies a feasible solution; a feasible factorization is not a graph.
"""

from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json
import time

from ortools.sat.python import cp_model

BASE = Path(__file__).resolve().parents[2]


def gluing_data(core, order=99, coclique_size=21):
    q = core['charges']
    n = len(q)
    masks = [0]*n
    for i, j in core['edges']:
        masks[i] |= 1 << j
        masks[j] |= 1 << i
    degree = core['parameters']['degree']
    target = core['parameters']['shift']
    residual = {(i, j): 2-((masks[i] >> j)&1)-(masks[i]&masks[j]).bit_count()
                for i, j in combinations(range(n), 2)}
    assert min(residual.values()) >= 0
    allowed = [(1 << n)-1 for _ in q]
    for (i, j), r in residual.items():
        if r == 0:
            allowed[i] &= ~(1 << j)
            allowed[j] &= ~(1 << i)
    rows = []
    nodes = 0

    def dfs(chosen, candidates, weight):
        nonlocal nodes
        nodes += 1
        if weight == target:
            rows.append(chosen)
        if chosen.bit_count() == degree:
            return
        # Negative charges mean that reaching target is not a stopping rule.
        low = high = weight
        cc = candidates
        while cc:
            bit = cc & -cc
            cc -= bit
            value = q[bit.bit_length()-1]
            low += min(0, value)
            high += max(0, value)
        if not low <= target <= high:
            return
        while candidates:
            bit = candidates & -candidates
            candidates -= bit
            i = bit.bit_length()-1
            new = chosen | bit
            if any((new & masks[j]).bit_count() > 2-((new >> j)&1) for j in range(n)):
                continue
            dfs(new, candidates & allowed[i], weight+q[i])

    start = time.monotonic()
    dfs(0, (1 << n)-1, 0)
    assert len(rows) == len(set(rows))
    return dict(charges=q, neighbours=masks, residual=residual, rows=rows,
                outside_degrees=[degree-m.bit_count() for m in masks],
                order=order, coclique_size=coclique_size,
                enumeration_nodes=nodes, enumeration_seconds=time.monotonic()-start)


def solve_gluing(core, *, order=99, coclique_size=21, seconds=60, workers=4,
                pair_consistency=False, neighbour_capacity=False):
    data = gluing_data(core, order, coclique_size)
    q, rows = data['charges'], data['rows']
    n = len(q)
    by_vertex = [[t for t, r in enumerate(rows) if (r >> i)&1] for i in range(n)]
    model = cp_model.CpModel()
    counts, coclique = [], []
    for t, row in enumerate(rows):
        members = [i for i in range(n) if (row >> i)&1]
        upper = min([order-n]+[data['outside_degrees'][i] for i in members]
                    +[data['residual'][i, j] for i, j in combinations(members, 2)])
        # Two distinct vertices cannot share three neighbours.
        if len(members) >= 3:
            upper = min(upper, 1)
        counts.append(model.NewIntVar(0, upper, f'x_{t}'))
        coclique.append(model.NewIntVar(0, min(upper, coclique_size), f'c_{t}'))
        model.Add(coclique[-1] <= counts[-1])
    model.Add(sum(counts) == order-n)
    model.Add(sum(coclique) == coclique_size)
    for i in range(n):
        model.Add(sum(counts[t] for t in by_vertex[i]) == data['outside_degrees'][i])
        model.Add(sum(coclique[t] for t in by_vertex[i]) == core['boundary_degrees'][i])
    for (i, j), value in data['residual'].items():
        model.Add(sum(counts[t] for t in by_vertex[i] if (rows[t] >> j)&1) == value)
    forbidden_pairs = 0
    if pair_consistency or neighbour_capacity:
        used = [model.NewBoolVar(f'used_{t}') for t in range(len(rows))]
        for t in range(len(rows)):
            model.Add(counts[t] >= 1).OnlyEnforceIf(used[t])
            model.Add(counts[t] == 0).OnlyEnforceIf(used[t].Not())
    if pair_consistency:
        for i, j in combinations(range(len(rows)), 2):
            if (rows[i] & rows[j]).bit_count() > 2:
                model.AddBoolOr([used[i].Not(), used[j].Not()])
                forbidden_pairs += 1
    capacity_inequalities = 0
    if neighbour_capacity:
        degree = core['parameters']['degree']
        least_abs = 4 if degree == 14 else 2
        assert degree in (4, 14)
        targets = [[2-((row >> i)&1)-(data['neighbours'][i] & row).bit_count()
                    for i in range(n)] for row in rows]
        zero_masks = [sum(1 << i for i, value in enumerate(h) if value == 0) for h in targets]
        for r, row in enumerate(rows):
            candidates = [t for t, other in enumerate(rows)
                          if (row & other).bit_count() <= 1
                          and not (other & zero_masks[r]) and not (row & zero_masks[t])]
            c_used = model.NewBoolVar(f'c_used_{r}')
            f_used = model.NewBoolVar(f'f_used_{r}')
            model.Add(coclique[r] >= 1).OnlyEnforceIf(c_used)
            model.Add(coclique[r] == 0).OnlyEnforceIf(c_used.Not())
            model.Add(counts[r]-coclique[r] >= 1).OnlyEnforceIf(f_used)
            model.Add(counts[r]-coclique[r] == 0).OnlyEnforceIf(f_used.Not())
            model.Add(sum(counts[t] for t in candidates) >= degree-row.bit_count()+int(r in candidates)).OnlyEnforceIf(used[r])
            model.Add(sum(counts[t]-coclique[t] for t in candidates) >= degree-row.bit_count()).OnlyEnforceIf(c_used)
            model.Add(sum(coclique[t] for t in candidates) >= least_abs).OnlyEnforceIf(f_used)
            capacity_inequalities += 3
            for i, need in enumerate(targets[r]):
                if need <= 0:
                    continue
                candidate_i = [t for t in candidates if (rows[t] >> i)&1]
                model.Add(sum(counts[t] for t in candidate_i) >= need+int(r in candidate_i)).OnlyEnforceIf(used[r])
                model.Add(sum(counts[t]-coclique[t] for t in candidate_i) >= need).OnlyEnforceIf(c_used)
                capacity_inequalities += 2
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    start = time.monotonic()
    status = solver.Solve(model)
    result = dict(status=solver.StatusName(status), row_count=len(rows),
                  enumeration_nodes=data['enumeration_nodes'],
                  enumeration_seconds=data['enumeration_seconds'],
                  solver_seconds=time.monotonic()-start,
                  branches=solver.NumBranches(), conflicts=solver.NumConflicts(),
                  order=order, coclique_size=coclique_size,
                  pair_consistency=pair_consistency, forbidden_row_pairs=forbidden_pairs,
                  neighbour_capacity=neighbour_capacity, capacity_inequalities=capacity_inequalities,
                  scope='Necessary common zero-charge population, not an SRG',
                  response_stats=solver.ResponseStats())
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result['selected_rows'] = [dict(vertices=[i for i in range(n) if (r >> i)&1],
                                      count=solver.Value(counts[t]),
                                      coclique_count=solver.Value(coclique[t]))
                                   for t, r in enumerate(rows) if solver.Value(counts[t])]
        assert sum(r['count'] for r in result['selected_rows']) == order-n
        assert sum(r['coclique_count'] for r in result['selected_rows']) == coclique_size
        assert all(sum(r['count'] for r in result['selected_rows'] if i in r['vertices'])
                   == data['outside_degrees'][i] for i in range(n))
        assert all(sum(r['count'] for r in result['selected_rows'] if i in r['vertices'] and j in r['vertices'])
                   == v for (i, j), v in data['residual'].items())
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('core', type=Path)
    parser.add_argument('--seconds', type=float, default=60)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--order', type=int, default=99)
    parser.add_argument('--coclique', type=int, default=21)
    parser.add_argument('--pair-consistency', action='store_true')
    parser.add_argument('--neighbour-capacity', action='store_true')
    args = parser.parse_args()
    raw = args.core.read_bytes()
    core = json.loads(raw)
    result = solve_gluing(core, order=args.order, coclique_size=args.coclique,
                          seconds=args.seconds, workers=args.workers,
                          pair_consistency=args.pair_consistency,
                          neighbour_capacity=args.neighbour_capacity)
    result['input_sha256'] = hashlib.sha256(raw).hexdigest()
    result['input'] = str(args.core)
    output = args.core.with_name(args.core.stem+'_gluing'+('_pairs' if args.pair_consistency else '')+
                                ('_capacity' if args.neighbour_capacity else '')+'.json')
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf8')
    print(json.dumps({k: result[k] for k in ('status', 'row_count', 'enumeration_nodes',
                                           'enumeration_seconds', 'solver_seconds')}), flush=True)


if __name__ == '__main__':
    main()
