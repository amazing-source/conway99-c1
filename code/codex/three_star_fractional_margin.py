"""Seek a fractional PSD point with positive margin on forced quotients.

The four known T-kernel columns and three U-kernel columns permit exact
principal quotients. A shared margin is maximized on these two quotients.
This is an exploratory relaxation, not a binary graph construction.
"""
import argparse
from pathlib import Path
import json
import sys
import time

import numpy as np
import sympy as sp
from ortools.linear_solver import pywraplp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_prescribed_kernel import N, EDGES, LABELS, K8, U0, S, linear_constraints, linear_certificate
from three_star_weight_profile_scan import compact_certificate
from three_star_psd_profile_cuts import normalized_vector, cut_row, fractional_witnesses


def common_row(cut):
    i,j=cut['pair']
    row={(i,j):1}
    for k in cut['common_vertices']:
        row[tuple(sorted((i,k)))]=1
        row[tuple(sorted((j,k)))]=1
    cap=2-len(set(LABELS[i])&set(LABELS[j]))
    return row,None,cap+len(cut['common_vertices']),'common_neighbour_lower_bound'


def search(input_path, profile_index, seed_path, seconds, iterations, use_common_caps=False):
    start = time.monotonic()
    data = json.loads(Path(input_path).read_text(encoding='utf-8-sig'))
    source = next(r for r in data['records'] if r['profile_index'] == profile_index)
    q = np.array(source['q'], dtype=np.int64)
    relations = np.column_stack((S, q))
    anchors_T = sp.Matrix(relations.T.tolist()).rref()[1]
    anchors_U = sp.Matrix(S.T.tolist()).rref()[1]
    assert len(anchors_T) == 4 and len(anchors_U) == 3
    quotient = {'T':[i for i in range(N) if i not in anchors_T],
                'U':[i for i in range(N) if i not in anchors_U]}
    report = dict(profile_index=profile_index, q=source['q'], quotient_indices=quotient,
                  iterations=[], cuts=[], common_cuts=[], graph_not_constructed=True,
                  common_neighbour_separation=use_common_caps)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    variables = {e:solver.NumVar(0, 1, 'e%d_%d'%e) for e in EDGES}
    margin = solver.NumVar(0, 20, 'margin')
    solver.Objective().SetCoefficient(margin, 1)
    solver.Objective().SetMaximization()
    def add_row(row, margin_coefficient=0):
        coeff, lo, hi, _ = row
        constraint = solver.Constraint(-solver.infinity() if lo is None else lo,
                                       solver.infinity() if hi is None else hi)
        for e, a in coeff.items():
            constraint.SetCoefficient(variables[e], a)
        if margin_coefficient:
            constraint.SetCoefficient(margin, margin_coefficient)
    for row in linear_constraints(q, connected_Q=True):
        add_row(row)
    signatures = set()
    active_margin_signatures = set()
    common_signatures=set()
    if seed_path:
        for old in json.loads(Path(seed_path).read_text(encoding='utf-8-sig'))['cuts']:
            vector = normalized_vector(old['vector'])
            signature = old['matrix'], tuple(map(int, vector))
            if signature in signatures:
                continue
            signatures.add(signature)
            cut = dict(matrix=old['matrix'], vector=list(map(int, vector)), source=str(seed_path))
            report['cuts'].append(cut)
            add_row(cut_row(cut))
        if use_common_caps:
            for cut in json.loads(Path(seed_path).read_text(encoding='utf-8-sig')).get('common_cuts',[]):
                signature=tuple(cut['pair']),tuple(cut['common_vertices'])
                if signature not in common_signatures:
                    common_signatures.add(signature)
                    report['common_cuts'].append(cut)
                    add_row(common_row(cut))
    for iteration in range(iterations):
        remaining = seconds-(time.monotonic()-start)
        if remaining <= 0:
            report['status'] = 'TIME_LIMIT_NO_EXCLUSION'
            break
        solver.SetTimeLimit(max(1,int(1000*remaining)))
        status = solver.Solve()
        step = dict(iteration=iteration, lp_status=int(status))
        report['iterations'].append(step)
        if status == pywraplp.Solver.INFEASIBLE:
            extra = [cut_row(cut) for cut in report['cuts']]+[common_row(cut) for cut in report['common_cuts']]
            full = linear_certificate(q, extra_rows=extra, connected_Q=True)
            report['certificate'] = compact_certificate(q, full, extra_rows=extra, connected_Q=True)
            report['status'] = full['status']
            break
        if status != pywraplp.Solver.OPTIMAL:
            report['status'] = 'NUMERICAL_LP_STOP_NO_EXCLUSION'
            break
        gamma = np.zeros((N, N))
        for i, j in EDGES:
            gamma[i,j] = gamma[j,i] = variables[i,j].solution_value()
        report['last_fractional_gamma'] = gamma.tolist()
        step['proposed_margin'] = margin.solution_value()
        matrices = {'T':24*np.eye(N)-K8-8*gamma, 'U':U0+15*gamma}
        step['minima'] = {name:float(np.linalg.eigvalsh(matrix[np.ix_(quotient[name],quotient[name])])[0])
                          for name,matrix in matrices.items()}
        new_common=0
        if use_common_caps:
            for i,j in EDGES:
                common=[k for k in range(N) if k not in (i,j) and gamma[i,k]+gamma[j,k]>1+1e-9]
                lhs=gamma[i,j]+sum(gamma[i,k]+gamma[j,k]-1 for k in common)
                cap=2-len(set(LABELS[i])&set(LABELS[j]))
                signature=(i,j),tuple(common)
                if lhs>cap+1e-7 and signature not in common_signatures:
                    common_signatures.add(signature)
                    cut=dict(pair=[i,j],common_vertices=common)
                    report['common_cuts'].append(cut)
                    add_row(common_row(cut))
                    new_common+=1
        step['new_common_cuts']=new_common
        if min(step['minima'].values()) > 1e-6 and not new_common:
            report['status'] = 'NUMERICAL_STRICT_PSD_QUOTIENTS_NOT_YET_EXACT'
            break
        new = 0
        for name, matrix in matrices.items():
            indices = quotient[name]
            shifted = matrix[np.ix_(indices,indices)]-step['proposed_margin']*np.eye(len(indices))
            _, witnesses = fractional_witnesses(shifted)
            for small in witnesses:
                vector = np.zeros(N,dtype=np.int64)
                vector[indices] = small
                vector = normalized_vector(vector)
                signature = name, tuple(map(int,vector))
                if signature in active_margin_signatures:
                    continue
                active_margin_signatures.add(signature)
                cut = dict(matrix=name, vector=list(map(int,vector)), source=dict(iteration=iteration))
                if signature not in signatures:
                    signatures.add(signature)
                    report['cuts'].append(cut)
                add_row(cut_row(cut), margin_coefficient=int(vector@vector))
                new += 1
        step['new_margin_cuts'] = new
        if not new and not new_common:
            report['status'] = 'NO_NEW_MARGIN_CUT_NO_EXCLUSION'
            break
    else:
        report['status'] = 'ITERATION_LIMIT_NO_EXCLUSION'
    report['elapsed_seconds'] = time.monotonic()-start
    report['scope'] = 'A fractional linear relaxation with both PSD conditions; all nonlinear far common-neighbour caps and binary integrality still require checking.'
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True)
    parser.add_argument('--profile-index',type=int,required=True)
    parser.add_argument('--seed-cuts')
    parser.add_argument('--seconds',type=float,default=30)
    parser.add_argument('--iterations',type=int,default=80)
    parser.add_argument('--common-caps',action='store_true')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    report=search(args.input,args.profile_index,args.seed_cuts,args.seconds,args.iterations,args.common_caps)
    Path(args.output).write_text(json.dumps(report,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('profile_index','status','elapsed_seconds')}))
    print(json.dumps(report['iterations'][-1]))


if __name__=='__main__':
    main()
