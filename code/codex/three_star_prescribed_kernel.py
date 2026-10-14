"""Construct a new three-star boundary with a prescribed extra kernel.

No input seed is used. CP-SAT enforces the local binary counts; all spectral
cuts are justified by an exactly negative integer quadratic value. A timeout
is not an exclusion. Even an exact local PSD output is not a Conway graph.
"""
import argparse
from fractions import Fraction
from itertools import combinations, product
from math import lcm
from pathlib import Path
import json
import sys
import time

import numpy as np
import sympy as sp
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_rank_repairs import LABELS, STARS, k8, boundary_masks
from three_star_ambient_upper import psd_or_witness
from two_mate_star_structure import LABELS as TWO_LABELS, classify

N = len(LABELS)
EDGES = tuple(combinations(range(N), 2))
K8 = np.array([[k8(p, q) for q in LABELS] for p in LABELS], dtype=np.int64)
S = np.array(STARS.tolist(), dtype=np.int64)
U0 = np.array([[60*int(i == j)-4*len(set(p).intersection(q))
                +sum((c ^ 1) in q for c in p)-2
                for j, q in enumerate(LABELS)] for i, p in enumerate(LABELS)],
              dtype=np.int64)


def prescribed_vector(closed_pairs, x, y, extra_cycles=()):
    index = {p:i for i, p in enumerate(LABELS)}
    q = np.array([int(p[0] in (0, 1) and p[1]//2 in closed_pairs)
                  for p in LABELS], dtype=np.int64)
    u = np.zeros(N, dtype=np.int64)
    for p, sign in (((0, y), 1), ((0, x), -1), ((2, x), 1), ((2, y), -1)):
        u[index[p]] = sign
    for cycle in extra_cycles:
        if len(cycle) % 2 or len(set(cycle)) != len(cycle):
            raise ValueError('Each added incidence cycle must have even length and distinct letters.')
        for i, a in enumerate(cycle):
            p = tuple(sorted((a, cycle[(i+1) % len(cycle)])))
            u[index[p]] += (-1)**i
    assert all(sum(int(u[j]) for j, p in enumerate(LABELS) if c in p) == 0
               for c in range(14))
    return 2*q+u


def linear_constraints(z=None, connected_Q=False):
    """Yield integer edge rows, lower bound, upper bound, and provenance."""
    relations = S if z is None else np.column_stack((S, z))
    rhs8 = 24*relations-K8@relations
    if np.any(rhs8 % 8):
        raise ValueError('Prescribed kernel has noninteger required row sums.')
    for a in range(relations.shape[1]):
        for i in range(N):
            row = {tuple(sorted((i, j))):int(relations[j, a])
                   for j in range(N) if j != i and relations[j, a]}
            rhs = int(rhs8[i, a]//8)
            yield row, rhs, rhs, 'kernel'
    for i, p in enumerate(LABELS):
        for c in range(14):
            row = {tuple(sorted((i, j))):1 for j, pj in enumerate(LABELS)
                   if j != i and c in pj}
            yield row, None, 2-int(c in p)-int((c ^ 1) in p), 'root_letter_cap'
    for choices in product((-1, 1), repeat=4):
        signs = {4:1, 5:-1}
        for c, sign in zip((6, 8, 10, 12), choices):
            signs[c], signs[c+1] = sign, -sign
        v = [signs.get(p[1], 0) for p in LABELS]
        row = {(i, j):v[i]*v[j] for i, j in EDGES if v[i]*v[j]}
        yield row, -45, 33, 'orientation_psd'
    if connected_Q:
        two = {i for i, p in enumerate(LABELS) if p[0] in (0, 1)}
        for mask in range(1, 63, 2):
            part = {j+1 for j in range(6) if (mask>>j)&1}
            row = {(i, j):1 for i, j in EDGES if i in two and j in two
                   and ((LABELS[i][1]//2 in part) != (LABELS[j][1]//2 in part))}
            yield row, 1, None, 'Q_connectivity'


def binary_obstruction(z):
    """A global noncompletion test, not an exclusion of a local PSD object."""
    full_labels = tuple(p for p in combinations(range(14), 2)
                        if p[1] != (p[0] ^ 1))
    full_K8 = np.array([[k8(p, q) for q in LABELS] for p in full_labels],
                      dtype=np.int64)
    D = np.array([[int(c in p) for p in LABELS] for c in range(14)],
                 dtype=np.int64)
    incidence_even = not np.any((D@z) % 2)
    correction_even = not np.any((full_K8@z) % 16)
    odd_weight = int(np.count_nonzero(z % 2))
    return dict(incidence_even=incidence_even, full_Kz_even=correction_even,
                odd_weight=odd_weight,
                rules_out_Conway_completion=bool(incidence_even and correction_even
                                                 and 0 < odd_weight < 10),
                reason='A nonzero binary fixed word supported on three far stars has weight>=10.',
                does_not_by_itself_rule_out_local_PSD=True)


def lp_probe(rows):
    solver = pywraplp.Solver.CreateSolver('GLOP')
    variables = {e:solver.NumVar(0, 1, 'e%d_%d'%e) for e in EDGES}
    for row, lo, hi, _ in rows:
        constraint = solver.Constraint(-solver.infinity() if lo is None else lo,
                                       solver.infinity() if hi is None else hi)
        for e, a in row.items():
            constraint.SetCoefficient(variables[e], a)
    status = solver.Solve()
    return dict(status=int(status), optimal_code=int(pywraplp.Solver.OPTIMAL),
                iterations=solver.iterations(),
                meaning='Numerical continuous relaxation; no exact infeasibility certificate.')


def linear_certificate(z):
    """Extract and exactly check a nonnegative combination yielding 0<=-1."""
    rows = []
    for number, (coeff, lo, hi, origin) in enumerate(linear_constraints(z)):
        if lo is not None:
            rows.append(( {e:-a for e, a in coeff.items()}, -lo, origin, number))
        if hi is not None:
            rows.append((coeff, hi, origin, number))
    for e in EDGES:
        rows.extend((({e:1}, 1, 'edge_upper_bound', None),
                     ({e:-1}, 0, 'edge_lower_bound', None)))
    solver = pywraplp.Solver.CreateSolver('GLOP')
    solver.SetTimeLimit(5000)
    multipliers = [solver.NumVar(0, solver.infinity(), 'a%d'%i)
                   for i in range(len(rows))]
    cancel = {e:solver.Constraint(0, 0) for e in EDGES}
    normalize = solver.Constraint(-1, -1)
    objective = solver.Objective()
    for i, (row, bound, _, _) in enumerate(rows):
        for e, value in row.items():
            cancel[e].SetCoefficient(multipliers[i], value)
        normalize.SetCoefficient(multipliers[i], bound)
        objective.SetCoefficient(multipliers[i], 1)
    objective.SetMinimization()
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        return dict(status='NO_EXACT_LINEAR_CERTIFICATE', dual_solver_status=int(status))
    fractions = [Fraction(v.solution_value()).limit_denominator(1000000)
                 for v in multipliers]
    denominator = lcm(*(v.denominator for v in fractions))
    weights = [int(v*denominator) for v in fractions]
    sums = {e:0 for e in EDGES}
    total = 0
    terms = []
    for weight, (row, bound, origin, number) in zip(weights, rows):
        if weight < 0:
            return dict(status='RATIONALIZATION_FAILED')
        if not weight:
            continue
        for e, value in row.items():
            sums[e] += weight*value
        total += weight*bound
        terms.append(dict(multiplier=weight, rhs=bound, origin=origin, row_number=number,
                          coefficients=[[i, j, a] for (i, j), a in row.items()]))
    if any(sums.values()) or total >= 0:
        return dict(status='RATIONALIZATION_FAILED')
    return dict(status='EXACT_NONNEGATIVE_LINEAR_COMBINATION_CONTRADICTION',
                terms=terms, combined_coefficients_zero=True,
                combined_rhs=total, conclusion='The weighted sum of necessary inequalities is0<=a negative integer.')


def spectral_witnesses(matrix):
    values, vectors = np.linalg.eigh(matrix.astype(float))
    witnesses = []
    for j, value in enumerate(values):
        if value >= -1e-8:
            break
        v = vectors[:, j]/max(abs(vectors[:, j]))
        for scale in (1, 2, 4, 8, 16, 32, 64, 128, 512):
            q = np.rint(scale*v).astype(np.int64)
            energy = int(q@matrix@q)
            if energy < 0:
                witnesses.append((q, energy))
                break
    return float(values[0]), witnesses


def construct(z, seconds, max_candidates, seed, connected_Q=False):
    start = time.monotonic()
    rows = list(linear_constraints(z, connected_Q=connected_Q))
    report = dict(labels=LABELS, prescribed_kernel=z.tolist(),
                  linear_relaxation=lp_probe(rows),
                  global_binary_kernel_test=binary_obstruction(z),
                  connected_Q_required=connected_Q,
                  scope='One prescribed kernel family, not all connected Q boundaries.',
                  solver='OR-Tools CP-SAT, one worker', cuts=[], iterations=[])
    model = cp_model.CpModel()
    variables = {e:model.NewBoolVar('e%d_%d'%e) for e in EDGES}
    def var(i, j):
        return variables[tuple(sorted((i, j)))]
    for row, lo, hi, _ in rows:
        expr = sum(a*variables[e] for e, a in row.items())
        if lo is not None:
            model.Add(expr >= lo)
        if hi is not None:
            model.Add(expr <= hi)
    # Only a lower bound for each AND is needed: it occurs solely in an
    # upper bound on the number of common neighbours.
    for i, j in EDGES:
        wedges = []
        for k in range(N):
            if k in (i, j):
                continue
            w = model.NewBoolVar('w%d_%d_%d'%(i, j, k))
            model.Add(w >= var(i, k)+var(j, k)-1)
            wedges.append(w)
        model.Add(sum(wedges)+var(i, j) <= 2-len(set(LABELS[i]).intersection(LABELS[j])))
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
            report['status'] = 'PRESCRIBED_FAMILY_UNSAT_BY_CP_SAT'
            break
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            report['status'] = 'TIME_LIMIT_NO_EXCLUSION'
            break
        gamma = np.zeros((N, N), dtype=np.int64)
        for i, j in EDGES:
            gamma[i, j] = gamma[j, i] = solver.Value(var(i, j))
        M = 24*np.eye(N, dtype=np.int64)-8*gamma-K8
        U = U0+15*gamma
        assert not np.any(M@np.column_stack((S, z)))
        masks = boundary_masks(gamma.tolist())
        assert all((masks[i]&masks[j]).bit_count() <= 2-((masks[i]>>j)&1)
                   for i, j in combinations(range(49), 2))
        report['last_gamma'] = gamma.tolist()
        new_cuts = 0
        for name, matrix in (('T', M), ('U', U)):
            minimum, witnesses = spectral_witnesses(matrix)
            record[name+'_minimum_eigenvalue_approx'] = minimum
            if not witnesses:
                exact = psd_or_witness(sp.Matrix(matrix.tolist()))
                if not exact['psd']:
                    witnesses = [(np.array(exact['integer_witness'], dtype=object),
                                  exact['quadratic_value'])]
            for q, energy in witnesses:
                signature = (name, tuple(map(int, q)))
                if signature in signatures:
                    continue
                signatures.add(signature)
                assert int(q@matrix@q) == energy < 0
                expr = sum(int(q[i]*q[j])*var(i, j) for i, j in EDGES if q[i]*q[j])
                if name == 'T':
                    model.Add(16*expr <= int(24*(q@q)-q@K8@q))
                else:
                    model.Add(30*expr >= int(-q@U0@q))
                report['cuts'].append(dict(matrix=name, vector=list(map(int, q)),
                                          negative_value=energy, candidate=iteration))
                new_cuts += 1
        record['new_exact_cuts'] = new_cuts
        print(json.dumps(record), flush=True)
        if not new_cuts:
            rank = int(sp.Matrix(M.tolist()).rank())
            index = {p:i for i, p in enumerate(LABELS)}
            two = [[int(gamma[index[p], index[q]]) for q in TWO_LABELS] for p in TWO_LABELS]
            structure = classify(two)
            report.update(status='NEW_LOCAL_T_AND_U_PSD_BOUNDARY', rank=rank,
                          two_star_structure=structure,
                          counterexample_to_A=(rank <= 30 and structure['component_count'] == 1))
            break
    else:
        report['status'] = 'CANDIDATE_LIMIT_NO_EXCLUSION'
    report['elapsed_seconds'] = time.monotonic()-start
    report['local_candidates'] = sum('new_exact_cuts' in x for x in report['iterations'])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--closed-pairs', type=int, nargs='+')
    parser.add_argument('--x', type=int, default=4)
    parser.add_argument('--y', type=int)
    parser.add_argument('--extra-cycle', type=int, nargs='+', action='append', default=[])
    parser.add_argument('--seconds', type=float, default=40)
    parser.add_argument('--max-candidates', type=int, default=100)
    parser.add_argument('--seed', type=int, default=19)
    parser.add_argument('--kernel-json')
    parser.add_argument('--connected-Q', action='store_true')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.kernel_json:
        raw = json.loads(Path(args.kernel_json).read_text(encoding='utf-8-sig'))
        z = np.array(raw['prescribed_kernel'], dtype=np.int64)
        if z.shape != (N,):
            raise ValueError('Expected34 integer kernel coordinates in the standard LABELS order.')
        template = dict(source=args.kernel_json, odd_weight=int(np.count_nonzero(z % 2)))
    else:
        if args.closed_pairs is None or args.y is None:
            parser.error('Supply --kernel-json, or --closed-pairs together with --y.')
        z = prescribed_vector(args.closed_pairs, args.x, args.y, args.extra_cycle)
        template = dict(closed_pairs=args.closed_pairs, x=args.x, y=args.y,
                        extra_cycles=args.extra_cycle, odd_weight=int(np.count_nonzero(z % 2)),
                        formula='z=2*closed_indicator+incidence_rectangle+extra_incidence_cycles')
    result = construct(z, args.seconds, args.max_candidates, args.seed, connected_Q=args.connected_Q)
    result['template'] = template
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status', 'elapsed_seconds', 'local_candidates')}))


if __name__ == '__main__':
    main()
