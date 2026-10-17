"""Seek exact exclusions of fixed positive relations by PSD cutting planes.

Every integer vector supplies a necessary linear PSD inequality, including
vectors suggested by floating-point relaxations. Only exactly cancelled
Farkas combinations count as exclusions. A numerical PSD point is neither
an exact PSD certificate nor a binary graph. No peer graph is input.
"""
import argparse
from collections import Counter
from functools import reduce
from math import gcd
from pathlib import Path
import json
import sys
import time

import numpy as np
from ortools.linear_solver import pywraplp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_prescribed_kernel import N, EDGES, K8, U0, linear_constraints, linear_certificate
from three_star_weight_profile_scan import compact_certificate


def normalized_vector(vector):
    divisor = reduce(gcd, map(abs, map(int, vector)))
    assert divisor
    v = np.array(vector, dtype=np.int64)//divisor
    if next(int(a) for a in v if a) < 0:
        v = -v
    return v


def cut_row(cut):
    v = np.array(cut['vector'], dtype=np.int64)
    if cut['matrix'] == 'T':
        row = {(i, j):16*int(v[i]*v[j]) for i, j in EDGES if v[i]*v[j]}
        bound = int(24*(v@v)-v@K8@v)
    else:
        assert cut['matrix'] == 'U'
        row = {(i, j):-30*int(v[i]*v[j]) for i, j in EDGES if v[i]*v[j]}
        bound = int(v@U0@v)
    return row, None, bound, 'psd_'+cut['matrix']


def fractional_witnesses(matrix):
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    result = []
    for i, value in enumerate(eigenvalues):
        if value >= -1e-7:
            break
        v = eigenvectors[:, i]/max(abs(eigenvectors[:, i]))
        for scale in (1, 2, 4, 8, 16, 32, 64, 128, 512, 1024):
            q = np.rint(scale*v).astype(np.int64)
            if float(q@matrix@q) < -1e-7:
                result.append(normalized_vector(q))
                break
    return float(eigenvalues[0]), result


def search(input_path, seed_path, seconds, profile_limit, iterations):
    start = time.monotonic()
    data = json.loads(Path(input_path).read_text(encoding='utf-8-sig'))
    profiles = [r for r in data['records'] if r.get('certificate', {}).get('status') !=
                'EXACT_NONNEGATIVE_LINEAR_COMBINATION_CONTRADICTION']
    pool, signatures = [], set()
    def add_cut(name, vector, source):
        v = normalized_vector(vector)
        signature = name, tuple(map(int, v))
        if signature in signatures:
            return False
        signatures.add(signature)
        pool.append(dict(matrix=name, vector=list(map(int, v)), source=source))
        return True
    if seed_path:
        for cut in json.loads(Path(seed_path).read_text(encoding='utf-8-sig'))['cuts']:
            add_cut(cut['matrix'], cut['vector'], str(seed_path))
    records = []
    for source in profiles[:profile_limit]:
        if time.monotonic()-start >= seconds:
            break
        q = np.array(source['q'], dtype=np.int64)
        record = dict(profile_index=source['profile_index'], q=source['q'], iterations=[])
        solver = pywraplp.Solver.CreateSolver('GLOP')
        variables = {e:solver.NumVar(0, 1, 'e%d_%d'%e) for e in EDGES}
        def add_row(row):
            coeff, lo, hi, _ = row
            constraint = solver.Constraint(-solver.infinity() if lo is None else lo,
                                           solver.infinity() if hi is None else hi)
            for e, a in coeff.items():
                constraint.SetCoefficient(variables[e], a)
        for row in linear_constraints(q, connected_Q=True):
            add_row(row)
        for cut in pool:
            add_row(cut_row(cut))
        for iteration in range(iterations):
            remaining = seconds-(time.monotonic()-start)
            if remaining <= 0:
                record['status'] = 'TIME_LIMIT_NO_EXCLUSION'
                break
            solver.SetTimeLimit(max(1, int(1000*remaining)))
            status = solver.Solve()
            step = dict(iteration=iteration, lp_status=int(status), cut_count=len(pool))
            record['iterations'].append(step)
            if status == pywraplp.Solver.INFEASIBLE:
                extra = [cut_row(cut) for cut in pool]
                certificate = linear_certificate(q, extra_rows=extra, connected_Q=True)
                record['certificate'] = compact_certificate(q, certificate, extra_rows=extra, connected_Q=True)
                record['status'] = certificate['status']
                record['certificate_cut_prefix'] = len(pool)
                break
            if status != pywraplp.Solver.OPTIMAL:
                record['status'] = 'NUMERICAL_LP_STOP_NO_EXCLUSION'
                break
            gamma = np.zeros((N, N))
            for i, j in EDGES:
                gamma[i, j] = gamma[j, i] = variables[i, j].solution_value()
            new = 0
            for name, matrix in (('T', 24*np.eye(N)-K8-8*gamma), ('U', U0+15*gamma)):
                minimum, witnesses = fractional_witnesses(matrix)
                step[name+'_min_approx'] = minimum
                for v in witnesses:
                    if add_cut(name, v, dict(profile=source['profile_index'], iteration=iteration)):
                        add_row(cut_row(pool[-1]))
                        new += 1
            step['new_cuts'] = new
            if not new:
                record['status'] = ('NUMERICAL_PSD_POINT_NOT_AN_EXACT_CERTIFICATE' if
                    min(step['T_min_approx'], step['U_min_approx']) >= -1e-7 else
                    'NO_NEW_CUT_NO_EXCLUSION')
                record['fractional_gamma'] = gamma.tolist()
                break
        else:
            record['status'] = 'ITERATION_LIMIT_NO_EXCLUSION'
        records.append(record)
        print(json.dumps(dict(profile=record['profile_index'], status=record['status'],
                              iterations=len(record['iterations']), cuts=len(pool),
                              elapsed=time.monotonic()-start)), flush=True)
    return dict(input=str(input_path), available_profiles=len(profiles), processed=len(records),
                complete=len(records) == len(profiles), status_counts=dict(Counter(r['status'] for r in records)),
                exact_exclusions=sum(r['status'] == 'EXACT_NONNEGATIVE_LINEAR_COMBINATION_CONTRADICTION' for r in records),
                cuts=pool, records=records, elapsed_seconds=time.monotonic()-start,
                cut_validity='Each stored integer vector gives v^t(8T)v>=0 or v^t(15U)v>=0. Validity of the cut does not depend on numerical eigenvalue accuracy.',
                scope='Only processed fixed coefficient profiles. Numerical infeasibility without an exact certificate and iteration/time limits do not exclude a profile.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--seed-cuts')
    parser.add_argument('--seconds', type=float, default=45)
    parser.add_argument('--profile-limit', type=int, default=12)
    parser.add_argument('--iterations', type=int, default=12)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    report = search(args.input, args.seed_cuts, args.seconds, args.profile_limit, args.iterations)
    Path(args.output).write_text(json.dumps(report, separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('cuts','records')}), flush=True)


if __name__ == '__main__':
    main()
