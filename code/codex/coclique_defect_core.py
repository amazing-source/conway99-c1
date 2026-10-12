"""Necessary coexistence constraints on the support of a coclique defect.

For Conway and a 21-coclique C, q = 4*1 - (A+4I)*1_C satisfies
A*q = 3*q + 2*1.  The core is supp(q); it has at most 30 vertices.
A feasible core is NOT a strongly regular graph or a realizable boundary.
"""

from pathlib import Path
from itertools import combinations
import argparse
import json
import time

from ortools.sat.python import cp_model

BASE = Path(__file__).resolve().parents[2]


def solve_core(charges, *, degree=14, positive_eigenvalue=3, shift=2,
               boundary_degrees=None, seconds=60, workers=4):
    n = len(charges)
    model = cp_model.CpModel()
    edges = {(i, j): model.NewBoolVar(f'e_{i}_{j}')
             for i, j in combinations(range(n), 2)}

    def edge(i, j):
        return edges[tuple(sorted((i, j)))]

    for i, qi in enumerate(charges):
        model.Add(sum(charges[j]*edge(i, j) for j in range(n) if j != i)
                  == positive_eigenvalue*qi + shift)
        bound = degree - (boundary_degrees[i] if boundary_degrees else 0)
        model.Add(sum(edge(i, j) for j in range(n) if j != i) <= bound)

    for i, j in combinations(range(n), 2):
        common = []
        for k in range(n):
            if k in (i, j):
                continue
            z = model.NewBoolVar(f'common_{i}_{j}_{k}')
            model.Add(z <= edge(i, k))
            model.Add(z <= edge(j, k))
            model.Add(z >= edge(i, k) + edge(j, k) - 1)
            common.append(z)
        model.Add(sum(common) <= 2-edge(i, j))

    # Safe row ordering for exchangeable vertices of the same charge.
    # Compare all columns except the two swapped ones (standard graph lex order).
    for i in range(n-1):
        if charges[i] != charges[i+1]:
            continue
        columns = [j for j in range(n) if j not in (i, i+1)]
        model.Add(sum((1 << t)*edge(i, j) for t, j in enumerate(columns))
                  <= sum((1 << t)*edge(i+1, j) for t, j in enumerate(columns)))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    start = time.monotonic()
    status = solver.Solve(model)
    result = dict(status=solver.StatusName(status), seconds=time.monotonic()-start,
                  charges=charges, boundary_degrees=boundary_degrees,
                  branches=solver.NumBranches(), conflicts=solver.NumConflicts(),
                  scope='Necessary induced-support relaxation; SAT is not an SRG',
                  parameters=dict(degree=degree, r=positive_eigenvalue, shift=shift),
                  model_stats=model.ModelStats(), response_stats=solver.ResponseStats())
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        actual = [list(e) for e, v in edges.items() if solver.Value(v)]
        result['edges'] = actual
        neighbours = [set() for _ in charges]
        for i, j in actual:
            neighbours[i].add(j)
            neighbours[j].add(i)
        assert all(sum(charges[j] for j in neighbours[i]) == positive_eigenvalue*charges[i]+shift
                   for i in range(n))
        assert all(len(neighbours[i] & neighbours[j]) <= 2-(j in neighbours[i])
                   for i, j in combinations(range(n), 2))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--a', type=int, default=0, help='number of b=1 / charge 3 vertices')
    parser.add_argument('--e', type=int, default=0, help='number of b=5 / charge -1 vertices')
    parser.add_argument('--seconds', type=float, default=60)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--control', action='store_true')
    args = parser.parse_args()
    folder = BASE/'data'/'codex_coclique_defects'
    folder.mkdir(exist_ok=True)
    if args.control:
        # A two-vertex coclique of the 3x3 grid gives the bow-tie support:
        # one charge-2 vertex and four charge-1 vertices.
        result = solve_core([2, 1, 1, 1, 1], degree=4,
                            positive_eigenvalue=1, boundary_degrees=[0, 1, 1, 1, 1],
                            seconds=10, workers=1)
        assert result['status'] in ('OPTIMAL', 'FEASIBLE'), result
        output = folder/'grid9_positive_control.json'
    else:
        a, e = args.a, args.e
        b = 6-3*a-e
        assert a >= 0 and e >= 0 and b >= 0
        charges = [3]*a + [2]*b + [1]*(6+3*a+3*e) + [-1]*e
        assert sum(charges) == 18 and sum(q*q for q in charges) == 30
        result = solve_core(charges, boundary_degrees=[4-q for q in charges],
                            seconds=args.seconds, workers=args.workers)
        result['profile'] = dict(b1=a, b2=b, b3=6+3*a+3*e,
                                 b4=66-a-3*e, b5=e)
        output = folder/f'core_a{a}_e{e}.json'
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf8')
    print(json.dumps({k: result[k] for k in ('status', 'seconds', 'branches', 'conflicts')}), flush=True)


if __name__ == '__main__':
    main()
