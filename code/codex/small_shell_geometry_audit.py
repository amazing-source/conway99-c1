"""Finite independent checks for the norm-18 and norm-20 lemmas.

The CP-SAT models are relaxations on the nonzero support only. They use
the eigenvector equations and upper bounds on common neighbours, not
the hand proof's triangle descent or its case deductions.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import json

from ortools.sat.python import cp_model


def nonbinary20_patterns():
    answer = []
    for p2, p1, n1, n2 in product(range(6), range(21), range(21), range(6)):
        if p2 == 0 or p2+n2 > 2:
            continue
        if 2*p2+p1 != n1+2*n2 or 4*p2+p1+n1+4*n2 != 20:
            continue
        if 2*p2+p1 < 8:
            continue
        if p2 < n2:
            continue  # sign symmetry
        answer.append((p2, p1, n1, n2))
    assert sorted(answer) == [(1, 6, 6, 1), (1, 7, 9, 0), (2, 4, 8, 0)]
    return answer


def support_relaxation(pattern):
    p2, p1, n1, n2 = pattern
    weights = [2]*p2+[1]*p1+[-1]*n1+[-2]*n2
    n = len(weights)
    model = cp_model.CpModel()
    edges = {(i, j): model.NewBoolVar(f'e_{i}_{j}') for i, j in combinations(range(n), 2)}

    def edge(i, j):
        return edges[min(i, j), max(i, j)]

    for i in range(n):
        model.Add(sum(weights[j]*edge(i, j) for j in range(n) if j != i) == -4*weights[i])
        model.Add(sum(edge(i, j) for j in range(n) if j != i) <= 14)
    for i, j in combinations(range(n), 2):
        common = []
        for k in range(n):
            if k in (i, j):
                continue
            both = model.NewBoolVar(f'c_{i}_{j}_{k}')
            model.Add(both <= edge(i, k))
            model.Add(both <= edge(j, k))
            model.Add(both >= edge(i, k)+edge(j, k)-1)
            common.append(both)
        model.Add(sum(common) <= 2-edge(i, j))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 20
    solver.parameters.num_search_workers = 1
    status = solver.Solve(model)
    assert status == cp_model.INFEASIBLE, solver.StatusName(status)
    result = {'pattern_p2_p1_n1_n2': pattern, 'support_size': n,
              'status': solver.StatusName(status), 'branches': solver.NumBranches(),
              'conflicts': solver.NumConflicts()}
    print(result, flush=True)
    return result


def fano_checks():
    points = range(1, 8)
    lines = sorted({tuple(sorted((a, b, a ^ b))) for a, b in combinations(points, 2)})
    assert len(lines) == 7
    B = [[int(p not in line) for p in points] for line in lines]
    assert all(sum(row) == 4 for row in B)
    assert all(sum(B[i][k]*B[j][k] for k in range(7)) == 2 for i, j in combinations(range(7), 2))
    sums = Counter(sum(B[i][j] for i in rows for j in cols)
                   for rows in combinations(range(7), 3) for cols in combinations(range(7), 3))
    assert min(sums) == 3 and sum(sums.values()) == 1225
    survivors = []
    for r in range(12):
        s = 11-r
        for e1, e2 in product(range(2), repeat=2):
            for xr in range(r+1):
                for xu in range(s+1):
                    E = 4*r+e1+e2-xr
                    if E != 4*s+e1+e2-xu or E < 3*max(r, s):
                        continue
                    # Any Z vertex needs >=4 neighbours in the opposite X set.
                    if (r > xr and xu < 4) or (s > xu and xr < 4):
                        continue
                    for er, eu in product(range(min(e1, e2)+1), repeat=2):
                        small_x = xr if r < s else xu
                        block = small_x-e1-e2+er+eu
                        survivors.append((r, s, e1, e2, xr, xu, er, eu, block))
    assert survivors
    assert all(sorted(row[:2]) == [5, 6] and row[-1] <= 2 for row in survivors)
    return {'three_by_three_sum_distribution': dict(sorted(sums.items())),
            'common_support_relaxation_survivors': survivors,
            'contradiction': 'All candidate 3x3 Fano-complement blocks require at most 2 entries, but minimum is 3.'}


def exterior_histograms():
    answer = {}
    for e in (0, 1):
        histograms = []
        for h in range(80):
            for j in range(80):
                ns = [9-5*e-h-3*j, 40+14*e+3*h+8*j, 30-9*e-3*h-6*j, h, j]
                if min(ns) < 0:
                    continue
                assert sum(ns) == 79
                assert sum(t*ns[t] for t in range(5)) == 100-4*e
                assert sum(t*(t-1)*ns[t] for t in range(5)) == 60-18*e
                histograms.append(ns)
        answer[str(e)] = histograms
    assert len(answer['0']) == 22 and len(answer['1']) == 7
    return answer


def main():
    checks = [support_relaxation(p) for p in nonbinary20_patterns()]
    report = {'norm20_nonbinary_support_relaxations': checks, 'norm18_fano_difference': fano_checks(),
              'norm20_exterior_histograms_by_internal_edge_count': exterior_histograms(),
              'scope': 'Finite checks accompanying hand proofs; CP-SAT outputs are not formal proof-assistant certificates.'}
    path = Path(__file__).resolve().parents[2]/'data/codex_small_shell_geometry_audit.json'
    path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Three nonbinary supports infeasible; 1225 Fano blocks checked; 29 exterior histograms.')


if __name__ == '__main__':
    main()
