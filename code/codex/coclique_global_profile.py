"""One exact model of the ENTIRE (0,2) profile, without fixed border/cycle.

C=0..20; H=21..24; X=25..28; Y=29..36; E=37,38; Z=39..98.
H has a forced C4. Its four C-neighbour pairs are disjoint, as are its
four sets of six Z neighbours. This is a labelling normalization, not a
restriction on cores, epsilon, or the eleven negative-edge cycle types.
All remaining edges are shared global variables. Degree 14 and the
common-neighbour upper bounds already imply every SRG equality.
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


def pair_caps(model,n,edge,degree=14,lam=1,mu=2):
    products={};common={}
    def mul(a,b):
        if isinstance(a,int):return b if a else 0
        if isinstance(b,int):return a if b else 0
        key=tuple(sorted((a.Index(),b.Index())))
        if key not in products:
            z=model.NewBoolVar(f'p{len(products)}')
            model.Add(z<=a);model.Add(z<=b);model.Add(z>=a+b-1);products[key]=z
        return products[key]
    for u in range(n):model.Add(sum(edge(u,v) for v in range(n) if v!=u)==degree)
    for u,v in combinations(range(n),2):
        common[u,v]=sum(mul(edge(u,w),edge(v,w)) for w in range(n) if w not in (u,v))
        model.Add(common[u,v]<=mu+(lam-mu)*edge(u,v))
    return common,mul,len(products)


def build(order_columns=True):
    model=cp_model.CpModel();fixed={};variables={}
    def set_edge(u,v,value):
        key=tuple(sorted((u,v)))
        assert key not in fixed or fixed[key]==value
        fixed[key]=value
    C=list(range(21));H=list(range(21,25));L=list(range(25,37));E=[37,38];Z=list(range(39,99))
    for u,v in combinations(C,2):set_edge(u,v,0)
    for u,v in combinations(range(21,39),2):
        if u in L and v in L:continue
        value=0
        if u in H and v in H:value=int((v-u)%4 in (1,3))
        elif u in H and v in range(25,29):value=int(u-21 in ((v-25)%4,(v-24)%4))
        elif u in H and v in range(29,37):value=int(u-21==(v-29)//2)
        elif (u,v)==(37,38):value=1
        set_edge(u,v,value)
    for h in range(4):
        for c in C:set_edge(21+h,c,int(c in (2*h,2*h+1)))
        for z in Z:set_edge(21+h,z,int(39+6*h<=z<45+6*h))
    for u,v in combinations(range(99),2):
        if (u,v) not in fixed:variables[u,v]=model.NewBoolVar(f'e{u}_{v}')
    def edge(u,v):
        if u==v:return 0
        key=tuple(sorted((u,v)))
        return fixed[key] if key in fixed else variables[key]
    for u in L:model.Add(sum(edge(u,c) for c in C)==3)
    for u in E:model.Add(sum(edge(u,c) for c in C)==5)
    for u in Z:model.Add(sum(edge(u,c) for c in C)==4)
    for u in L:model.Add(sum(edge(u,v) for v in L if u!=v)==(1 if u<29 else 3))
    charge={**{u:2 for u in H},**{u:1 for u in L},**{u:-1 for u in E}}
    for u in C+Z:model.Add(sum(value*edge(u,s) for s,value in charge.items())==2)
    groups=[[2*h,2*h+1] for h in range(4)]+[list(range(8,21))]
    groups+=[list(range(39+6*h,45+6*h)) for h in range(4)]+[list(range(63,99))]
    if order_columns:
        signature=lambda u:sum((1<<(s-21))*edge(u,s) for s in range(21,39))
        for group in groups:
            for u,v in zip(group,group[1:]):model.Add(signature(u)<=signature(v))
    common,mul,product_count=pair_caps(model,99,edge)
    return model,variables,fixed,dict(C=C,H=H,L=L,E=E,Z=Z,groups=groups,edge=edge,common=common,product=mul,product_count=product_count)


def verify(adj):
    assert len(adj)==99 and all(len(s)==14 for s in adj)
    assert all(u not in adj[u] and all(u in adj[v] for v in adj[u]) for u in range(99))
    assert all(len(adj[u]&adj[v])==2-int(v in adj[u]) for u,v in combinations(range(99),2))
    C=set(range(21));assert all(not(adj[u]&C) for u in C)
    counts={b:sum(len(adj[u]&C)==b for u in range(21,99)) for b in range(8)}
    assert counts=={0:0,1:0,2:4,3:12,4:60,5:2,6:0,7:0}
    return counts


def positive_control():
    # Tests the global degree+upper-cap encoding on a known complete SRG;
    # the (0,2) normalization itself is justified separately in the note.
    model=cp_model.CpModel();variables={e:model.NewBoolVar(f'g{e}') for e in combinations(range(9),2)}
    edge=lambda u,v:0 if u==v else variables[tuple(sorted((u,v)))]
    pair_caps(model,9,edge,degree=4)
    for u,v in variables:model.Add(edge(u,v)==int(u//3==v//3 or u%3==v%3))
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    status=solver.Solve(model);assert status==cp_model.OPTIMAL
    return dict(graph='3x3 rook',status=solver.StatusName(status),scope='Global degree/common-neighbour-cap encoding, not a C1 example')


def run(folder,seconds=240,workers=2,order_columns=True):
    folder.mkdir(parents=True,exist_ok=True)
    config=dict(start_utc=datetime.now(timezone.utc).isoformat(),seconds=seconds,workers=workers,order_columns=order_columns,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                scope='All C1 graphs with a 21-coclique of profile (0,2), up to the proved H-neighbour normalization',
                fixed_support=False,fixed_population=False,fixed_negative_edge_cycles=False)
    (folder/'config.json').write_text(json.dumps(config,indent=2)+'\n')
    control=positive_control();begun=time.monotonic();model,variables,fixed,ctx=build(order_columns)
    build_seconds=time.monotonic()-begun
    (folder/'model.json').write_text(json.dumps(dict(build_seconds=build_seconds,model_stats=model.ModelStats(),
                      edge_variables=len(variables),product_variables=ctx['product_count'],positive_control=control),indent=2)+'\n')
    print(json.dumps(dict(stage='built',pid=os.getpid(),seconds=build_seconds,edge_variables=len(variables),product_variables=ctx['product_count'],model_stats=model.ModelStats())),flush=True)
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=workers;solver.parameters.max_time_in_seconds=seconds
    solver.parameters.subsolvers.append('no_lp');solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
    with (folder/'search.log').open('w') as log:
        solver.log_callback=lambda line:(log.write(line+'\n'),log.flush())
        status=solver.Solve(model)
    report=dict(status=solver.StatusName(status),seconds=solver.WallTime(),build_seconds=build_seconds,
                branches=solver.NumBranches(),conflicts=solver.NumConflicts(),workers=workers,
                scope=config['scope'],normalization='Four disjoint H pairs in C and four disjoint H six-sets in Z; no fixed cycle pattern or epsilon',
                complete_graph_equations=True,model_stats=model.ModelStats(),response_stats=solver.ResponseStats(),positive_control=control)
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        a=[set() for _ in range(99)]
        for (u,v),value in fixed.items():
            if value:a[u].add(v);a[v].add(u)
        for (u,v),var in variables.items():
            if solver.Value(var):a[u].add(v);a[v].add(u)
        report['profile_check']=verify(a);report['adjacency']=[sorted(s) for s in a];report['full_srg_check']=True
    (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('adjacency','model_stats','response_stats')}),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--seconds',type=float,default=240)
    ap.add_argument('--workers',type=int,default=2);ap.add_argument('--no-column-order',action='store_true')
    args=ap.parse_args();run(args.folder,args.seconds,args.workers,not args.no_column_order)
