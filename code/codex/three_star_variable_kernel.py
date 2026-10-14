"""Search connected-Q boundaries with a variable fourth kernel z=2q+u.

q is a reference closed-set indicator, not a relation imposed on Gamma.
All entries of u in {-1,0,1} are free subject to Du=0. This replaces a
fixed incidence-cycle template by an entire bounded coefficient family.
No peer graph is input or audited. A timeout is not an exclusion.
"""
import argparse
from itertools import combinations
from pathlib import Path
import json
import sys
import time

import numpy as np
import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_prescribed_kernel import (LABELS, EDGES, N, K8, S, U0,
    linear_constraints, spectral_witnesses, binary_obstruction)
from three_star_rank_repairs import boundary_masks
from three_star_ambient_upper import psd_or_witness
from two_mate_star_structure import LABELS as TWO_LABELS, classify


def search(reference_pairs, seconds, max_candidates, seed, normalize_incidence=True):
    start = time.monotonic()
    q = np.array([int(p[0] in (0, 1) and p[1]//2 in reference_pairs)
                  for p in LABELS], dtype=np.int64)
    twice_Kq = (K8@q)//4
    assert not np.any((K8@q) % 4)
    D = np.array([[int(c in p) for p in LABELS] for c in range(14)],
                 dtype=np.int64)
    report = dict(reference_pairs=reference_pairs, reference_indicator=q.tolist(),
                  labels=LABELS, iterations=[], cuts=[],
                  family='z=2q+u, u_i in{-1,0,1}, Du=0, nonconstant third-star tail, connected Q',
                  scope='A restricted integer-kernel family, not all possible fourth relations.',
                  no_peer_graph_input=True, global_binary_distance_not_imposed=True)
    model = cp_model.CpModel()
    edges = {e:model.NewBoolVar('e%d_%d'%e) for e in EDGES}
    def edge(i, j):
        return edges[tuple(sorted((i, j)))]
    for row, lo, hi, _ in linear_constraints():
        expr = sum(a*edges[e] for e, a in row.items())
        if lo is not None:
            model.Add(expr >= lo)
        if hi is not None:
            model.Add(expr <= hi)
    # Common-neighbour caps for every pair of far labels.
    for i, j in EDGES:
        wedges = []
        for k in range(N):
            if k in (i, j):
                continue
            w = model.NewBoolVar('w%d_%d_%d'%(i, j, k))
            model.Add(w >= edge(i, k)+edge(j, k)-1)
            wedges.append(w)
        model.Add(sum(wedges)+edge(i, j) <= 2-len(set(LABELS[i]).intersection(LABELS[j])))
    u = [model.NewIntVar(-1, 1, 'u%d'%i) for i in range(N)]
    pos = [model.NewBoolVar('p%d'%i) for i in range(N)]
    neg = [model.NewBoolVar('n%d'%i) for i in range(N)]
    for i in range(N):
        model.Add(u[i] == pos[i]-neg[i])
        model.Add(pos[i]+neg[i] <= 1)
    for c in range(14):
        model.Add(sum(u[i] for i, p in enumerate(LABELS) if c in p) == 0)
    if normalize_incidence:
        # Exact normal form for ker(D_S): on each outside letter there
        # are seven possible ternary triples, and the overlap coefficients
        # occur in opposite pairs. These are implications of Du=0.
        index = {p:i for i, p in enumerate(LABELS)}
        states = [(0, 0, 0), (1, -1, 0), (1, 0, -1), (-1, 1, 0),
                  (0, 1, -1), (-1, 0, 1), (0, -1, 1)]
        state = {}
        for x in range(4, 14):
            state[x] = model.NewIntVar(0, 6, 'state%d'%x)
            model.AddAllowedAssignments([state[x]]+[u[index[c, x]] for c in (0, 1, 2)],
                                        [(s,)+triple for s, triple in enumerate(states)])
        a, b = index[0, 2], index[1, 2]
        c, d = index[0, 3], index[1, 3]
        model.Add(u[a]+u[b] == 0)
        model.Add(u[c]+u[d] == 0)
        model.Add(sum(u[index[2, x]] for x in range(4, 14)) == 0)
        # Swapping the mate centres0 and1 preserves q. Do this first;
        # subsequent permutations of outside mate pairs preserve a,c.
        model.Add(u[a] >= 0)
        model.Add(u[c] >= 0).OnlyEnforceIf(pos[a].Not())
        pair_code = {}
        for pair in range(2, 7):
            model.Add(state[2*pair] <= state[2*pair+1])
            pair_code[pair] = 7*state[2*pair]+state[2*pair+1]
        for membership in (False, True):
            group = [pair for pair in range(2, 7) if (pair in reference_pairs) == membership]
            for first, second in zip(group, group[1:]):
                model.Add(pair_code[first] <= pair_code[second])
        report['incidence_normal_form'] = dict(states=states,
            meaning='All ternary incidence-kernel vectors covered up to symmetries preserving the reference q.',
            overlap='u02=-u12=a, u03=-u13=c; a>0 or a=0,c>=0',
            exterior='Sort each mate pair of states and sort pair codes inside and outside M.')
    tail = [i for i, p in enumerate(LABELS) if p[0] == 2]
    assert len(tail) == 10 and all(q[i] == 0 for i in tail)
    # On the ten tail labels the three forced star relations are constant.
    # Nonconstancy therefore proves z is independent of their span.
    model.Add(sum(pos[i]+neg[i] for i in tail) >= 1)
    model.Add(sum(pos[i] for i in tail) <= 9)
    model.Add(sum(neg[i] for i in tail) <= 9)
    for i in range(N):
        products = []
        for j in range(N):
            if i == j:
                continue
            value = model.NewIntVar(-1, 1, 'eu%d_%d'%(i, j))
            model.Add(value == u[j]).OnlyEnforceIf(edge(i, j))
            model.Add(value == 0).OnlyEnforceIf(edge(i, j).Not())
            products.append(value)
        fixed_q_part = sum(2*int(q[j])*edge(i, j) for j in range(N)
                           if j != i and q[j])
        model.Add(sum(products)+fixed_q_part == 3*u[i]+int(6*q[i]-twice_Kq[i]))
    # A graph on six vertices is connected iff every proper nonempty cut
    # has an edge. Keep just the31 cuts containing outer-pair index1.
    two = {i for i, p in enumerate(LABELS) if p[0] in (0, 1)}
    cut_count = 0
    for mask in range(1, 63, 2):
        part = {j+1 for j in range(6) if (mask>>j)&1}
        cross = [edges[i, j] for i, j in EDGES if i in two and j in two
                 and ((LABELS[i][1]//2 in part) != (LABELS[j][1]//2 in part))]
        model.Add(sum(cross) >= 1)
        cut_count += 1
    assert cut_count == 31
    report['Q_connectivity_cuts'] = cut_count
    signatures = set()
    for iteration in range(max_candidates):
        remaining = seconds-(time.monotonic()-start)
        if remaining <= 0:
            report['status'] = 'TIME_LIMIT_NO_EXCLUSION'
            break
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = remaining
        solver.parameters.random_seed = seed
        status = solver.Solve(model)
        record = dict(iteration=iteration, status=solver.StatusName(status),
                      solver_seconds=solver.WallTime(), branches=solver.NumBranches())
        report['iterations'].append(record)
        if status == cp_model.INFEASIBLE:
            report['status'] = 'VARIABLE_COEFFICIENT_FAMILY_UNSAT_BY_CP_SAT'
            break
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            report['status'] = 'TIME_LIMIT_NO_EXCLUSION'
            break
        gamma = np.zeros((N, N), dtype=np.int64)
        for i, j in EDGES:
            gamma[i, j] = gamma[j, i] = solver.Value(edges[i, j])
        u_value = np.array([solver.Value(x) for x in u], dtype=np.int64)
        z = 2*q+u_value
        M = 24*np.eye(N, dtype=np.int64)-8*gamma-K8
        U = U0+15*gamma
        assert not np.any(D@u_value)
        assert not np.any(M@np.column_stack((S, z)))
        assert len(set(map(int, u_value[tail]))) > 1
        masks = boundary_masks(gamma.tolist())
        assert all((masks[i]&masks[j]).bit_count() <= 2-((masks[i]>>j)&1)
                   for i, j in combinations(range(49), 2))
        index = {p:i for i, p in enumerate(LABELS)}
        structure = classify([[int(gamma[index[p], index[r]]) for r in TWO_LABELS]
                              for p in TWO_LABELS])
        assert structure['component_count'] == 1
        record['u'] = u_value.tolist()
        record['binary_kernel_test'] = binary_obstruction(z)
        report['last_gamma'] = gamma.tolist()
        report['last_kernel'] = z.tolist()
        new_cuts = 0
        for name, matrix in (('T', M), ('U', U)):
            minimum, witnesses = spectral_witnesses(matrix)
            record[name+'_minimum_eigenvalue_approx'] = minimum
            if not witnesses:
                exact = psd_or_witness(sp.Matrix(matrix.tolist()))
                if not exact['psd']:
                    witnesses = [(np.array(exact['integer_witness'], dtype=object),
                                  exact['quadratic_value'])]
            for v, energy in witnesses:
                signature = (name, tuple(map(int, v)))
                if signature in signatures:
                    continue
                signatures.add(signature)
                assert int(v@matrix@v) == energy < 0
                expr = sum(int(v[i]*v[j])*edges[i, j] for i, j in EDGES if v[i]*v[j])
                if name == 'T':
                    model.Add(16*expr <= int(24*(v@v)-v@K8@v))
                else:
                    model.Add(30*expr >= int(-v@U0@v))
                report['cuts'].append(dict(matrix=name, vector=list(map(int, v)),
                                          negative_value=energy, candidate=iteration))
                new_cuts += 1
        record['new_exact_cuts'] = new_cuts
        print(json.dumps({k:v for k, v in record.items() if k not in ('u', 'binary_kernel_test')}), flush=True)
        if not new_cuts:
            rank = int(sp.Matrix(M.tolist()).rank())
            report.update(status='NEW_CONNECTED_Q_LOCAL_T_AND_U_PSD_BOUNDARY', rank=rank,
                          counterexample_to_A=True, exact_PSD=True)
            assert rank <= 30
            break
    else:
        report['status'] = 'CANDIDATE_LIMIT_NO_EXCLUSION'
    report['elapsed_seconds'] = time.monotonic()-start
    report['local_candidates'] = sum('u' in record for record in report['iterations'])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference-pairs', type=int, nargs='+', required=True)
    parser.add_argument('--seconds', type=float, default=40)
    parser.add_argument('--max-candidates', type=int, default=100)
    parser.add_argument('--seed', type=int, default=31)
    parser.add_argument('--raw-incidence', action='store_true')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    report = search(args.reference_pairs, args.seconds, args.max_candidates, args.seed,
                    normalize_incidence=not args.raw_incidence)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status', 'elapsed_seconds', 'local_candidates')}))


if __name__ == '__main__':
    main()
