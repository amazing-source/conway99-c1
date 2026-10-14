"""Exact common-neighbour cutting planes on a bounded coefficient family."""
import argparse
from pathlib import Path
import json
import sys
import time

import numpy as np
from ortools.linear_solver import pywraplp

sys.path.insert(0,str(Path(__file__).resolve().parent))
from three_star_prescribed_kernel import N, EDGES, LABELS, linear_constraints, linear_certificate
from three_star_weight_profile_scan import compact_certificate
from three_star_fractional_margin import common_row


def search(path, seed_paths, active_pairs, seconds, iterations):
    start=time.monotonic()
    data=json.loads(Path(path).read_text(encoding='utf-8-sig'))
    profiles=[]
    for r in data['records']:
        if r.get('certificate',{}).get('status')=='EXACT_NONNEGATIVE_LINEAR_COMBINATION_CONTRADICTION':
            continue
        pairs={x//2 for label,q in zip(LABELS,r['q']) if q for x in label if x>=4}
        if len(pairs)==active_pairs:
            profiles.append(r)
    pool, signatures=[],set()
    for path0 in seed_paths:
        for cut in json.loads(Path(path0).read_text(encoding='utf-8-sig'))['common_cuts']:
            signature=tuple(cut['pair']),tuple(cut['common_vertices'])
            if signature not in signatures:
                signatures.add(signature)
                pool.append(cut)
    records=[]
    for source in profiles:
        if time.monotonic()-start>=seconds:
            break
        q=np.array(source['q'],dtype=np.int64)
        solver=pywraplp.Solver.CreateSolver('GLOP')
        variables={e:solver.NumVar(0,1,'e%d_%d'%e) for e in EDGES}
        def add_row(row):
            coeff,lo,hi,_=row
            constraint=solver.Constraint(-solver.infinity() if lo is None else lo,
                                         solver.infinity() if hi is None else hi)
            for e,a in coeff.items():constraint.SetCoefficient(variables[e],a)
        for row in linear_constraints(q,connected_Q=True):add_row(row)
        for cut in pool:add_row(common_row(cut))
        record=dict(profile_index=source['profile_index'],q=source['q'],iterations=[])
        for iteration in range(iterations):
            remaining=seconds-(time.monotonic()-start)
            if remaining<=0:
                record['status']='TIME_LIMIT_NO_EXCLUSION'
                break
            solver.SetTimeLimit(max(1,int(1000*remaining)))
            status=solver.Solve()
            record['iterations'].append(dict(iteration=iteration,lp_status=int(status),cuts=len(pool)))
            if status==pywraplp.Solver.INFEASIBLE:
                extra=[common_row(cut) for cut in pool]
                full=linear_certificate(q,extra_rows=extra,connected_Q=True)
                record['certificate']=compact_certificate(q,full,extra_rows=extra,connected_Q=True)
                record['certificate_cut_prefix']=len(pool)
                record['status']=full['status']
                break
            if status!=pywraplp.Solver.OPTIMAL:
                record['status']='NUMERICAL_LP_STOP_NO_EXCLUSION'
                break
            gamma=np.zeros((N,N))
            for i,j in EDGES:gamma[i,j]=gamma[j,i]=variables[i,j].solution_value()
            new=0
            for i,j in EDGES:
                common=[k for k in range(N) if k not in(i,j) and gamma[i,k]+gamma[j,k]>1+1e-9]
                lhs=gamma[i,j]+sum(gamma[i,k]+gamma[j,k]-1 for k in common)
                cap=2-len(set(LABELS[i])&set(LABELS[j]))
                signature=(i,j),tuple(common)
                if lhs>cap+1e-7 and signature not in signatures:
                    signatures.add(signature)
                    cut=dict(pair=[i,j],common_vertices=common)
                    pool.append(cut)
                    add_row(common_row(cut))
                    new+=1
            record['iterations'][-1]['new_cuts']=new
            if not new:
                record['status']='NUMERICALLY_FEASIBLE_COMMON_NEIGHBOUR_RELAXATION'
                record['fractional_gamma']=gamma.tolist()
                break
        else:record['status']='ITERATION_LIMIT_NO_EXCLUSION'
        records.append(record)
        print(json.dumps(dict(profile=source['profile_index'],status=record['status'],cuts=len(pool))),flush=True)
    return dict(source=str(path),active_outside_pairs=active_pairs,available_profiles=len(profiles),
                processed=len(records),complete=len(records)==len(profiles),records=records,cuts=pool,
                exact_exclusions=sum(r['status']=='EXACT_NONNEGATIVE_LINEAR_COMBINATION_CONTRADICTION' for r in records),
                elapsed_seconds=time.monotonic()-start,
                cut_proof='For0<=a,b<=1, ab>=a+b-1. Thus a common-neighbour cap implies Gamma_ij+sum_(k in K)(Gamma_ik+Gamma_jk)<=2-|label_i intersect label_j|+|K| for every subsetK.',
                scope='Only the stated positive weight16 profiles, with the indicated number of active outside mate pairs. No graph is constructed.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True)
    p.add_argument('--seed-files',nargs='*',default=[])
    p.add_argument('--active-pairs',type=int,required=True)
    p.add_argument('--seconds',type=float,default=40)
    p.add_argument('--iterations',type=int,default=40)
    p.add_argument('--output',required=True)
    a=p.parse_args()
    report=search(a.input,a.seed_files,a.active_pairs,a.seconds,a.iterations)
    Path(a.output).write_text(json.dumps(report,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in('records','cuts')}))


if __name__=='__main__':main()
