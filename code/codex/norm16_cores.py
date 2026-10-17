"""Exhaustive support-core classification for integer (-4)-eigenvectors of norm 16.

Standard-library exact enumerator; optional --crosscheck-ortools compares a
different constraint solver. Outputs data/codex_norm16_cores.json.
The result classifies support cores, NOT extensions to a 99-vertex graph.
"""
import argparse
import json
from itertools import combinations, permutations
from pathlib import Path

POINTS = range(8)
PAIRS = list(combinations(POINTS, 2))
BLOCKS = list(combinations(POINTS, 4))
BLOCK_SETS = [frozenset(b) for b in BLOCKS]
BLOCK_INDEX = {b: i for i, b in enumerate(BLOCKS)}
COSTS = [[i for i in POINTS if i in b] +
         [8 + i for i, pair in enumerate(PAIRS) if set(pair) <= b] for b in BLOCK_SETS]
CONFLICTS = [sum(1 << j for j, c in enumerate(BLOCK_SETS) if i == j or len(b & c) > 2)
             for i, b in enumerate(BLOCK_SETS)]
PARTITIONS = [(8,), (6, 2), (5, 3), (4, 4), (4, 2, 2), (3, 3, 2), (2, 2, 2, 2)]


def cycle_matrix(parts):
    M = [[0] * 8 for _ in POINTS]
    offset = 0
    for length in parts:
        for i in range(length):
            a, b = offset + i, offset + (i + 1) % length
            M[a][b] += 1
            M[b][a] += 1
        offset += length
    assert offset == 8 and all(sum(row) == 2 for row in M)
    return M


def enumerate_columns(M):
    """Exact multicover search. A state is a SET of already chosen columns.

    Each unfinished demand must occur in a future column. Branch on all
    feasible columns meeting one such demand. Reaching the same column set
    in another order is redundant: demands and available columns depend
    only on that set. Every solution therefore has a branch to completion.
    """
    demands = tuple([4] * 8 + [2 - M[a][b] for a, b in PAIRS])
    seen, solutions = set(), set()

    def visit(selected, available, remaining, depth):
        if selected in seen:
            return
        seen.add(selected)
        if depth == 8:
            if not any(remaining):
                solutions.add(tuple(i for i in range(70) if selected >> i & 1))
            return
        candidates = [i for i in range(70) if available >> i & 1 and
                      all(remaining[j] > 0 for j in COSTS[i])]
        if len(candidates) < 8 - depth:
            return
        best = None
        for j, demand in enumerate(remaining):
            if not demand:
                continue
            options = [i for i in candidates if j in COSTS[i]]
            if len(options) < demand:
                return
            if best is None or len(options) * best[0] < len(best[1]) * demand:
                best = demand, options
        assert best is not None
        for i in best[1]:
            new_remaining = list(remaining)
            for j in COSTS[i]:
                new_remaining[j] -= 1
            visit(selected | 1 << i, available & ~CONFLICTS[i], tuple(new_remaining), depth + 1)

    visit(0, (1 << 70) - 1, demands, 0)
    return solutions, len(seen)


def cp_crosscheck(M):
    from ortools.sat.python import cp_model
    model = cp_model.CpModel()
    vs = [model.new_bool_var('column_' + str(i)) for i in range(70)]
    model.add(sum(vs) == 8)
    for a in POINTS:
        model.add(sum(vs[i] for i, b in enumerate(BLOCK_SETS) if a in b) == 4)
    for a, b in PAIRS:
        model.add(sum(vs[i] for i, c in enumerate(BLOCK_SETS) if a in c and b in c) == 2 - M[a][b])
    for i in range(70):
        for j in range(i):
            if len(BLOCK_SETS[i] & BLOCK_SETS[j]) > 2:
                model.add(vs[i] + vs[j] <= 1)

    class Collect(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
            self.solutions = set()

        def on_solution_callback(self):
            self.solutions.add(tuple(i for i, v in enumerate(vs) if self.value(v)))

    callback = Collect()
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = 10
    status = solver.solve(model, callback)
    assert status in (cp_model.OPTIMAL, cp_model.INFEASIBLE), solver.status_name(status)
    return callback.solutions, solver.status_name(status)


def matrix_from_columns(solution):
    return [[int(a in BLOCK_SETS[i]) for i in solution] for a in POINTS]


def audit_matrix(B, M):
    assert all(sum(row) == 4 for row in B)
    assert all(sum(B[a][j] for a in POINTS) == 4 for j in POINTS)
    for a in POINTS:
        for b in POINTS:
            assert sum(B[a][j] * B[b][j] for j in POINTS) == 2 * int(a == b) + 2 - M[a][b]
    N = [[0 if i == j else 2 - sum(B[a][i] * B[a][j] for a in POINTS)
          for j in POINTS] for i in POINTS]
    assert all(0 <= x <= 2 for row in N for x in row)
    assert all(sum(row) == 2 for row in N)
    sizes, unseen = [], set(POINTS)
    while unseen:
        stack = [min(unseen)]
        component = set()
        while stack:
            v = stack.pop()
            if v in component:
                continue
            component.add(v)
            stack.extend(w for w in POINTS if N[v][w])
        unseen -= component
        sizes.append(len(component))
    return tuple(sorted(sizes, reverse=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--crosscheck-ortools', action='store_true')
    args = parser.parse_args()
    results = []
    for parts in PARTITIONS:
        M = cycle_matrix(parts)
        solutions, states = enumerate_columns(M)
        check = None
        if args.crosscheck_ortools:
            other, check = cp_crosscheck(M)
            assert other == solutions, (parts, other ^ solutions)
        automorphisms = [p for p in permutations(POINTS)
                         if all(M[a][b] == M[p[a]][p[b]] for a, b in PAIRS)]
        representatives = set()
        for solution in solutions:
            B = matrix_from_columns(solution)
            assert audit_matrix(B, M) == parts
            images = {tuple(sorted(BLOCK_INDEX[tuple(sorted(p[a] for a in BLOCKS[i]))]
                                   for i in solution)) for p in automorphisms}
            assert images <= solutions
            representatives.add(min(images))
        assert len(representatives) == (0 if any(x % 2 for x in parts) else 1)
        row = {'defect_cycle_lengths': parts, 'labelled_column_sets': len(solutions),
               'search_states': states, 'row_automorphisms': len(automorphisms),
               'isomorphism_classes_preserving_the_two_sides': len(representatives),
               'representatives': [matrix_from_columns(s) for s in sorted(representatives)]}
        if check is not None:
            row['ortools_crosscheck'] = check
        results.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != 'representatives'}), flush=True)
    assert sum(r['isomorphism_classes_preserving_the_two_sides'] for r in results) == 5
    output = {'scope': 'Support incidence matrices only; no 99-vertex extension is claimed.', 'cases': results}
    path = Path(__file__).resolve().parents[2] / 'data' / 'codex_norm16_cores.json'
    path.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
