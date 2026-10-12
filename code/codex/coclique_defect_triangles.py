"""Glue ALL core-centred triangles into the SAME zero-charge population.

The edge variables describe actual shared matchings, one per support vertex.
Edges whose endpoints have disjoint support columns are left unchosen, with
necessary remaining-capacity bounds. Thus SAT is not a completed graph.
"""
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json
import time

from ortools.sat.python import cp_model
from coclique_defect_gluing import gluing_data
from coclique_defect_star import population,targets,compatible


def solve(core, *, order=99, coclique_size=21, seconds=60, workers=4, log_path=None):
    start=time.monotonic();data=gluing_data(core,order,coclique_size)
    q=data['charges'];rows=data['rows'];n=len(q);nr=len(rows)
    degree=core['parameters']['degree'];c_degree=4 if degree==14 else 2
    model=cp_model.CpModel();counts,coclique=population(model,data,core)
    # Keep these bounds as Python integers; do not retain protobuf views
    # while extending the model (the installed OR-Tools binding is native).
    upper=[]
    for row in rows:
        members=[i for i in range(n) if row>>i&1]
        bound=min([order-n]+[data['outside_degrees'][i] for i in members]
                  +[data['residual'][i,j] for i,j in combinations(members,2)])
        upper.append(min(bound,1) if len(members)>=3 else bound)
    free=[model.NewIntVar(0,u,f'f{t}') for t,u in enumerate(upper)]
    for t in range(nr):model.Add(free[t]+coclique[t]==counts[t])
    cells=[(t,c) for t in range(nr) for c in range(2)] # 0 = C, 1 = outside C
    pop=[coclique[t] if c==0 else free[t] for t,c in cells]
    incidence=[[] for _ in cells]
    edges={};row_edges={};row_adj=[set() for _ in rows]
    def register(a,b,v):
        incidence[a].append((b,v,2 if a==b else 1))
        if a!=b:incidence[b].append((a,v,1))
    h=[targets(data,r) for r in rows]
    zeros=[sum(1<<i for i,v in enumerate(hh) if v==0) for hh in h]
    def allowed(t,u):
        return not(rows[t]&zeros[u] or rows[u]&zeros[t])
    for t in range(nr):
        for u in range(t,nr):
            if (rows[t]&rows[u]).bit_count()!=1 or not allowed(t,u):continue
            variables=[]
            for ct,cu in ((0,1),(1,0),(1,1)):
                if t==u and ct==1 and cu==0:continue
                a,b=2*t+ct,2*u+cu
                bound=min(upper[t],upper[u])
                if a==b:bound//=2
                if bound==0:continue
                v=model.NewIntVar(0,bound,f'g{t}_{ct}_{u}_{cu}')
                edges[a,b]=v;variables.append(v);register(a,b,v)
            if t!=u and variables:
                v=model.NewIntVar(0,min(upper[t],upper[u]),f'edge{t}_{u}')
                model.Add(v==sum(variables));row_edges[t,u]=v
                row_adj[t].add(u);row_adj[u].add(t)
    disjoint=[[u for u,s in enumerate(rows) if not(r&s) and allowed(t,u)] for t,r in enumerate(rows)]
    for a,(t,colour) in enumerate(cells):
        known_degree=sum(mult*v for b,v,mult in incidence[a])
        model.Add(known_degree<=(degree-rows[t].bit_count())*pop[a])
        avail=sum((free[u] if colour==0 else counts[u]) for u in disjoint[t])
        model.Add(known_degree+upper[t]*avail>=(degree-rows[t].bit_count())*pop[a])
        for i,need in enumerate(h[t]):
            known=sum(mult*v for b,v,mult in incidence[a] if rows[cells[b][0]]>>i&1)
            if rows[t]>>i&1:model.Add(known==need*pop[a])
            else:
                model.Add(known<=need*pop[a])
                available=sum((free[u] if colour==0 else counts[u]) for u in disjoint[t] if rows[u]>>i&1)
                model.Add(known+upper[t]*available>=need*pop[a])
        if colour==1:
            known_c=sum(mult*v for b,v,mult in incidence[a] if cells[b][1]==0)
            model.Add(known_c<=c_degree*pop[a])
            model.Add(known_c+upper[t]*sum(coclique[u] for u in disjoint[t])>=c_degree*pop[a])

    def ev(t,u):return row_edges[tuple(sorted((t,u)))]
    triangle_cuts=wedge_cuts=0
    for t in range(nr):
        if upper[t]!=1:continue
        for u in sorted(row_adj[t]):
            if u<=t or upper[u]!=1:continue
            for v in row_adj[t]&row_adj[u]:
                if v<=u or upper[v]!=1:continue
                # The edge t-u already has its unique common neighbour in S.
                model.Add(ev(t,u)+ev(t,v)+ev(u,v)<=2);triangle_cuts+=1
    for t,u in combinations(range(nr),2):
        if upper[t]!=1 or upper[u]!=1 or (rows[t]&rows[u]).bit_count()!=2:continue
        for v in row_adj[t]&row_adj[u]:
            if upper[v]!=1:continue
            model.Add(ev(t,v)+ev(u,v)<=1);wedge_cuts+=1
    built=time.monotonic()
    validation=model.Validate()
    if validation:raise ValueError(validation)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=seconds
    solver.parameters.num_search_workers=workers
    log=log_path.open('w',encoding='utf8') if log_path else None
    if log:
        solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
        def callback(line):log.write(f'{time.monotonic()-built:.3f} {line}\n');log.flush()
        solver.log_callback=callback
    try:status=solver.Solve(model)
    finally:
        if log:log.close()
    result=dict(status=solver.StatusName(status),rows=nr,edge_variables=len(edges),
                triangle_cuts=triangle_cuts,wedge_cuts=wedge_cuts,
                build_seconds=built-start,solver_seconds=time.monotonic()-built,
                branches=solver.NumBranches(),conflicts=solver.NumConflicts(),
                model_stats=model.ModelStats(),response_stats=solver.ResponseStats(),
                scope='Shared core-centred triangles and common population, not all external edges')
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        result['selected_rows']=[dict(vertices=[i for i in range(n) if r>>i&1],count=solver.Value(counts[t]),
                                     coclique_count=solver.Value(coclique[t])) for t,r in enumerate(rows) if solver.Value(counts[t])]
        result['selected_edges']=[dict(left=dict(vertices=[i for i in range(n) if rows[cells[a][0]]>>i&1],in_coclique=cells[a][1]==0),
                                      right=dict(vertices=[i for i in range(n) if rows[cells[b][0]]>>i&1],in_coclique=cells[b][1]==0),
                                      count=solver.Value(v)) for (a,b),v in edges.items() if solver.Value(v)]
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('core',type=Path)
    ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--workers',type=int,default=4)
    ap.add_argument('--order',type=int,default=99);ap.add_argument('--coclique',type=int,default=21)
    args=ap.parse_args();raw=args.core.read_bytes();output=args.core.with_name(args.core.stem+'_triangles.json')
    report=solve(json.loads(raw),order=args.order,coclique_size=args.coclique,seconds=args.seconds,workers=args.workers,log_path=output.with_suffix('.log'))
    report.update(input_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('selected_rows','selected_edges','model_stats','response_stats')}),flush=True)
