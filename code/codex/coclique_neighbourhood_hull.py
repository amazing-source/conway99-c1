"""Couple convex hulls of exact binary neighbourhood choices by column generation.

An antisymmetric edge price gives a uniform obstruction: in a reciprocal
graph the total price is zero. The sum of minimum prices of allowed integer
neighbourhoods must therefore be <=0. Pricing uses small exact CP models.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,hstack,eye,vstack,csr_matrix
from ortools.sat.python import cp_model
from coclique_completion_certificate import equations


def run(core,pop,folder,iterations=60):
    folder.mkdir(parents=True,exist_ok=True)
    eq,edges,rows,colours=equations(core,pop,prune_incompatible=True)
    nv=len(rows);ne=len(edges)
    by_vertex=[[e for e in eq if e['reason'][1]==v] for v in range(nv)]
    models=[];variables=[];patterns=[set() for _ in rows]
    for v in range(nv):
        ids=sorted({j for e in by_vertex[v] for j in e['variables']})
        model=cp_model.CpModel();x={j:model.NewBoolVar(f'x{j}') for j in ids}
        for e in by_vertex[v]:model.Add(sum(x[j] for j in e['variables'])==e['rhs'])
        models.append(model);variables.append(x)
    scale=1000000
    def price(v,w):
        model=models[v];x=variables[v]
        coeff={j:int(w[j])*(1 if edges[j][0]==v else -1) for j in x}
        model.Maximize(sum(coeff[j]*x[j] for j in x))
        solver=cp_model.CpSolver();solver.parameters.num_search_workers=1;solver.parameters.max_time_in_seconds=5
        status=solver.Solve(model)
        item=dict(vertex=v,status=solver.StatusName(status),seconds=solver.WallTime())
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            item['pattern']=tuple(j for j in x if solver.Value(x[j]))
            item['value']=sum(coeff[j] for j in item['pattern'])
            item['upper_bound']=int(round(solver.BestObjectiveBound()))
        return item
    started=time.monotonic();history=[];report=dict(history=history,scope='One population; integer local choices, reciprocal convex mixing')
    with ThreadPoolExecutor(max_workers=4) as pool:
        initial=list(pool.map(lambda v:price(v,np.zeros(ne,dtype=int)),range(nv)))
        assert all('pattern' in item for item in initial)
        for item in initial:patterns[item['vertex']].add(item['pattern'])
        for iteration in range(iterations):
            rr=[];cc=[];vv=[];columns=[]
            for v in range(nv):
                for pattern in sorted(patterns[v]):
                    k=len(columns);columns.append((v,pattern));rr.append(v);cc.append(k);vv.append(1)
                    for j in pattern:
                        rr.append(nv+j);cc.append(k);vv.append(1 if edges[j][0]==v else -1)
            B=coo_matrix((vv,(rr,cc)),shape=(nv+ne,len(columns))).tocsr()
            slack=vstack([csr_matrix((nv,ne)),eye(ne)],format='csr')
            A=hstack([B,slack,-slack],format='csr')
            lp=linprog(np.r_[np.zeros(len(columns)),np.ones(2*ne)],A_eq=A,
                       b_eq=np.r_[np.ones(nv),np.zeros(ne)],bounds=(0,None),
                       method='highs-ds',options={'time_limit':30})
            if lp.status!=0:
                report['status']='LP_UNKNOWN';break
            entry=dict(iteration=iteration,patterns=len(columns),phase_one_objective=float(lp.fun),elapsed=time.monotonic()-started)
            if lp.fun<1e-7:
                entry['new_patterns']=0;history.append(entry);report['status']='RECIPROCAL_INTEGER_HULL_FEASIBLE'
                print(json.dumps(entry),flush=True);break
            prices=np.rint(lp.eqlin.marginals[nv:]*scale).astype(np.int64)
            priced=list(pool.map(lambda v:price(v,prices),range(nv)))
            added=0
            for item in priced:
                if 'pattern' in item:
                    bucket=patterns[item['vertex']]
                    if item['pattern'] not in bucket:bucket.add(item['pattern']);added+=1
            entry['new_patterns']=added
            if all(x['status']=='OPTIMAL' for x in priced):
                # For every actual reciprocal graph, the sum of these signed
                # scores is zero. A negative sum of maxima is impossible.
                total=sum(x['value'] for x in priced);entry['integer_upper_sum']=total
                if total<0:
                    report['status']='INTEGER_NEIGHBOURHOOD_PRICE_OBSTRUCTION'
                    report['proof']=dict(edge_prices=prices.tolist(),upper_sum=total,pricing=priced,
                            verification='CP optimal pricing; no independent certificate yet')
                    history.append(entry);print(json.dumps(entry),flush=True);break
            history.append(entry);print(json.dumps(entry),flush=True)
            report['status']='ITERATION_LIMIT';report['last_pricing']=priced
            (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n')
        report['seconds']=time.monotonic()-started
        report['pattern_count']=sum(map(len,patterns))
        (folder/'patterns.json').write_text(json.dumps([sorted(p) for p in patterns])+'\n')
        (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('core',type=Path);ap.add_argument('population',type=Path)
    ap.add_argument('folder',type=Path);ap.add_argument('--iterations',type=int,default=60)
    args=ap.parse_args();run(json.loads(args.core.read_text()),json.loads(args.population.read_text()),args.folder,args.iterations)
