"""One 61/38 boundary factorization for ALL coclique profiles (0,2).

The border consists of C, the positive support, and the 24 zero-charge
neighbours of H. Four complete H neighbourhoods are present. All 38
missing vertices are shared columns, not independent local choices.
Only the B-B block of A^2+A=12I+2J is imposed. A solution is passed to
the exact global completion criterion; SAT here alone is not a graph.
No negative-edge cycle partition, epsilon or positive core is fixed.
"""
from pathlib import Path
from itertools import combinations
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import time
from ortools.sat.python import cp_model


def build():
    C=list(range(21));H=list(range(21,25));L=list(range(25,37))
    E=[37,38];ZH=list(range(39,63));Z0=list(range(63,99))
    B=C+H+L+ZH;M=E+Z0
    fixed={};variables={};model=cp_model.CpModel()
    def put(u,v,x):
        key=tuple(sorted((u,v)))
        assert key not in fixed or fixed[key]==x
        fixed[key]=x
    for u,v in combinations(C,2):put(u,v,0)
    for u,v in combinations(H+L+E,2):
        if u in E and v in E:continue
        if u in L and v in L:continue
        value=0
        if u in H and v in H:value=int((v-u)%4 in (1,3))
        elif u in H and v in range(25,29):value=int(u-21 in ((v-25)%4,(v-24)%4))
        elif u in H and v in range(29,37):value=int(u-21==(v-29)//2)
        put(u,v,value)
    for i,h in enumerate(H):
        for c in C:put(h,c,int(c in (2*i,2*i+1)))
        for z in ZH+Z0:put(h,z,int(39+6*i<=z<45+6*i))
    for u,v in combinations(range(99),2):
        if u in M and v in M:continue
        if (u,v) not in fixed:variables[u,v]=model.NewBoolVar(f'a{u}_{v}')
    def edge(u,v):
        if u==v:return 0
        key=tuple(sorted((u,v)))
        return fixed[key] if key in fixed else variables[key]
    products={}
    def mul(a,b):
        if isinstance(a,int):return b if a else 0
        if isinstance(b,int):return a if b else 0
        key=tuple(sorted((a.Index(),b.Index())))
        if key not in products:
            z=model.NewBoolVar(f'p{len(products)}')
            model.Add(z<=a);model.Add(z<=b);model.Add(z>=a+b-1);products[key]=z
        return products[key]
    for u in B:model.Add(sum(edge(u,v) for v in range(99) if u!=v)==14)
    for u in M:model.Add(sum(edge(u,v) for v in B)<=14)
    for u in L+E+ZH+Z0:
        model.Add(sum(edge(u,c) for c in C)==(3 if u in L else 5 if u in E else 4))
    for u in L:model.Add(sum(edge(u,v) for v in L if u!=v)==(1 if u<29 else 3))
    for u in C+ZH:
        model.Add(2*sum(edge(u,h) for h in H)+sum(edge(u,l) for l in L)-sum(edge(u,e) for e in E)==2)
    for u in Z0:
        model.Add(sum(edge(u,l) for l in L)>=2)
        model.Add(sum(edge(u,l) for l in L)<=4)
    for u,v in combinations(B,2):
        model.Add(sum(mul(edge(u,w),edge(v,w)) for w in range(99) if w not in (u,v))==2-edge(u,v))
    # Zero-variance consequences of the four completed neighbourhoods.
    for h in H:
        neighbours=[u for u in B if isinstance(edge(h,u),int) and edge(h,u)]
        assert len(neighbours)==14
        for v in M:model.Add(sum(edge(u,v) for u in neighbours)==2)
    groups=[[2*i,2*i+1] for i in range(4)]+[list(range(8,21))]
    groups+=[list(range(39+6*i,45+6*i)) for i in range(4)]+[Z0]
    for group in groups:
        anchors=H+L if group is Z0 else H+L+E
        signature=lambda u:sum((1<<(s-21))*edge(u,s) for s in anchors)
        for u,v in zip(group,group[1:]):model.Add(signature(u)<=signature(v))
    return model,variables,fixed,B,M,edge,len(products)


def run(folder,seconds=300,workers=2):
    folder.mkdir(parents=True,exist_ok=True)
    config=dict(start_utc=datetime.now(timezone.utc).isoformat(),seconds=seconds,workers=workers,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope='All (0,2) profiles; no fixed core, cycle partition or epsilon',
                meaning='A boundary Gram factor is necessary, not automatically a full SRG')
    (folder/'config.json').write_text(json.dumps(config,indent=2)+'\n')
    start=time.monotonic();model,variables,fixed,B,M,edge,products=build();built=time.monotonic()-start
    meta=dict(build_seconds=built,border=B,missing=M,edge_variables=len(variables),product_variables=products,
              model_stats=model.ModelStats(),pid=os.getpid())
    (folder/'model.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps({k:v for k,v in meta.items() if k not in ('border','missing','model_stats')}),flush=True)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=seconds
    solver.parameters.num_search_workers=workers;solver.parameters.subsolvers.append('no_lp')
    solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
    with (folder/'search.log').open('w') as log:
        solver.log_callback=lambda line:(log.write(line+'\n'),log.flush())
        status=solver.Solve(model)
    report=dict(status=solver.StatusName(status),seconds=solver.WallTime(),branches=solver.NumBranches(),
                conflicts=solver.NumConflicts(),build_seconds=built,workers=workers,
                scope=config['scope'],response_stats=solver.ResponseStats(),full_srg=False)
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        import sympy as sp
        from coclique_global_completion import eliminate,encode,integral_completion
        value=lambda u,v:edge(u,v) if isinstance(edge(u,v),int) else solver.Value(edge(u,v))
        BB=sp.Matrix(len(B),len(B),lambda i,j:value(B[i],B[j]))
        DD=sp.Matrix(len(B),len(M),lambda i,j:value(B[i],M[j]))
        result=eliminate(BB,DD)
        report.update(B=encode(BB),D=encode(DD),border=B,missing=M,
                      E0=encode(result['E0']),P=encode(result['P']),nullity=result['nullity'])
        if result['nullity']==0:
            integral=all(x.is_Integer for x in result['E0'])
            report['forced_block_integral']=integral
            if integral:
                A=integral_completion(BB,DD,result['E0'])
                # The coclique is fully inside B. Verify its exact profile.
                assert list(B[:21])==list(range(21))
                counts={b:sum(sum(A[i,j] for j in range(21))==b for i in range(21,99)) for b in range(6)}
                assert counts=={0:0,1:0,2:4,3:12,4:60,5:2}
                report.update(full_srg=True,adjacency=encode(A),profile=counts)
    (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('B','D','E0','P','adjacency','response_stats')}),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path)
    ap.add_argument('--seconds',type=float,default=300);ap.add_argument('--workers',type=int,default=2)
    args=ap.parse_args();run(args.folder,args.seconds,args.workers)
