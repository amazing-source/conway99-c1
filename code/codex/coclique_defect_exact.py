"""Full SRG completion of a fixed support AND fixed exterior population.

Includes the missing exterior/exterior common-neighbour equations. A SAT
answer is checked as a complete graph. UNSAT excludes only this population.
"""
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json
import time

from ortools.sat.python import cp_model
from coclique_completion_certificate import equations
from coclique_defect_completion import propagate_equalities


def solve(core,population,seconds=60,workers=4,log_path=None):
    started=time.monotonic();eq,edge_list,rows,in_c=equations(core,population,prune_incompatible=True)
    propagation=propagate_equalities(eq);forced={item['variable']:item['value'] for item in propagation['assignments']}
    if propagation['status']=='CONTRADICTION':
        return dict(status='INFEASIBLE_BY_PROPAGATION',propagation=propagation)
    model=cp_model.CpModel();variables=[model.NewBoolVar(f'e{u}_{v}') for u,v in edge_list]
    for j,v in forced.items():model.Add(variables[j]==v)
    for e in eq:model.Add(sum(variables[j] for j in e['variables'])==e['rhs'])
    edges={pair:(forced[j] if j in forced else variables[j]) for j,pair in enumerate(edge_list)}
    def edge(u,v):return edges.get(tuple(sorted((u,v))),0) if u!=v else 0
    n=len(rows);and_terms=0
    for u,v in combinations(range(n),2):
        common=[]
        for w in range(n):
            if w in (u,v):continue
            a,b=edge(u,w),edge(v,w)
            if isinstance(a,int):
                if a:common.append(b)
            elif isinstance(b,int):
                if b:common.append(a)
            else:
                z=model.NewBoolVar(f'common{u}_{v}_{w}');and_terms+=1
                model.Add(z<=a);model.Add(z<=b);model.Add(z>=a+b-1);common.append(z)
        model.Add(sum(common)==2-len(rows[u]&rows[v])-edge(u,v))
    built=time.monotonic();solver=cp_model.CpSolver()
    solver.parameters.max_time_in_seconds=seconds;solver.parameters.num_search_workers=workers
    log=log_path.open('w',encoding='utf8') if log_path else None
    if log:
        solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
        def callback(line):log.write(f'{time.monotonic()-built:.3f} {line}\n');log.flush()
        solver.log_callback=callback
    try:status=solver.Solve(model)
    finally:
        if log:log.close()
    result=dict(status=solver.StatusName(status),build_seconds=built-started,solver_seconds=time.monotonic()-built,
                edge_variables=len(variables),forced_variables=len(forced),common_neighbour_variables=and_terms,
                branches=solver.NumBranches(),conflicts=solver.NumConflicts(),model_stats=model.ModelStats(),response_stats=solver.ResponseStats(),
                scope='Full graph equations for this fixed support and exterior population only')
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        s=len(core['charges']);adj=[set() for _ in range(s+n)]
        def add(i,j):adj[i].add(j);adj[j].add(i)
        for i,j in core['edges']:add(i,j)
        for z,row in enumerate(rows):
            for i in row:add(i,s+z)
        for j,(u,v) in enumerate(edge_list):
            if solver.Value(variables[j]):add(s+u,s+v)
        assert all(len(a)==core['parameters']['degree'] for a in adj)
        assert all(len(adj[i]&adj[j])==2-int(j in adj[i]) for i,j in combinations(range(len(adj)),2))
        result.update(full_srg_check=True,adjacency=[sorted(a) for a in adj])
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('core',type=Path);ap.add_argument('population',type=Path)
    ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--workers',type=int,default=4);args=ap.parse_args()
    cr=args.core.read_bytes();pr=args.population.read_bytes();out=args.population.with_name(args.population.stem+'_exact.json')
    result=solve(json.loads(cr),json.loads(pr),args.seconds,args.workers,log_path=out.with_suffix('.log'))
    result.update(core_sha256=hashlib.sha256(cr).hexdigest(),population_sha256=hashlib.sha256(pr).hexdigest(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('adjacency','propagation','model_stats','response_stats')}),flush=True)
