"""Variable-core attack on the complete (0,2) profile via its negative edge.

For e1~e2 with common neighbour z, their two exclusive 12-neighbour sets
have internal perfect matchings and a cross perfect matching. Their induced
union is a disjoint union of cycles of lengths 4*k, where sum(k)=6.
This model keeps ALL normalized positive cores variable, chooses z's core
column, and embeds that entire 24-vertex union with common-neighbour caps.
Feasibility is only a necessary induced-subgraph relaxation.
"""
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json
import time

from ortools.sat.python import cp_model


def partitions(n, minimum=1):
    if n==0:
        yield (); return
    for k in range(minimum,n+1):
        for rest in partitions(n-k,k): yield (k,)+rest


def cycle_edges(partition):
    # A_i--B_i, A_{2j}--A_{2j+1}. Each block of 2*k indices is closed
    # by B_{2j+1}--B_{2j+2}, yielding a cycle on 4*k vertices.
    result={(18+i,30+i) for i in range(12)}
    result|={(18+i,19+i) for i in range(0,12,2)}
    start=0
    for k in partition:
        for j in range(k):
            a=30+start+2*j+1; b=30+start+(2*j+2)%(2*k)
            result.add(tuple(sorted((a,b))))
        start+=2*k
    assert start==12
    return result


def build(partition, *, colour=True, fixed_core=None, triangle=False, root_h=0, population=False, hcomplete=False):
    # 0..15 positive support, 16/17 negative edge, 18..29 A,30..41 B,42 z.
    assert not (triangle and hcomplete)
    n=59+root_h if hcomplete else (51+root_h if triangle else 43)
    model=cp_model.CpModel(); fixed=set();variables={}
    def add(i,j):fixed.add(tuple(sorted((i,j))))
    if fixed_core:
        fixed.update(tuple(sorted(e)) for e in fixed_core['edges'])
    else:
        for i in range(4):
            add(i,(i+1)%4);add(4+i,i);add(4+i,(i+1)%4)
            add(i,8+2*i);add(i,9+2*i)
        add(16,17)
        for e in combinations(range(4,16),2): variables[e]=model.NewBoolVar(f'f{e[0]}_{e[1]}')
    fixed.update(cycle_edges(partition))
    for i in range(18,30):add(16,i)
    for i in range(30,42):add(17,i)
    add(16,42);add(17,42)
    for u in range(18,43):
        for i in range(16):variables[i,u]=model.NewBoolVar(f'h{i}_{u}')
    if triangle:
        for u in range(43,n):
            add(42,u)
            for i in list(range(16))+list(range(18,42)):
                variables[i,u]=model.NewBoolVar(f'h{i}_{u}')
        for e in combinations(range(43,n),2):variables[e]=model.NewBoolVar(f'w{e[0]}_{e[1]}')
    if hcomplete:
        cursor=43
        for h in range(4):
            for _ in range(4+int(root_h and h==0)):
                add(h,cursor)
                for u in range(18,43):variables[u,cursor]=model.NewBoolVar(f'hnew{u}_{cursor}')
                cursor+=1
        assert cursor==n
        for e in combinations(range(43,n),2):variables[e]=model.NewBoolVar(f'new{e[0]}_{e[1]}')
    def edge(i,j):
        if i==j:return 0
        pair=tuple(sorted((i,j)))
        return variables.get(pair,int(pair in fixed))
    if not fixed_core:
        for i in range(4,16):
            model.Add(sum(edge(i,j) for j in range(4,16) if i!=j)==(1 if i<8 else 3))
    q=[2]*4+[1]*12
    model.Add(sum(q[i]*edge(i,42) for i in range(16))==4)
    model.Add(sum(edge(i,42) for i in range(4))<=1)
    if triangle or hcomplete:
        model.Add(sum(edge(i,42) for i in range(4))==root_h)
        if root_h:model.Add(edge(0,42)==1)
    if triangle:
        for u in range(43,n):model.Add(sum(q[i]*edge(i,u) for i in range(16))==2)
    for u in range(18,42):model.Add(sum(q[i]*edge(i,u) for i in range(16))==3)
    for i in range(16):
        model.Add(sum(edge(i,u) for u in range(18,30))+edge(i,42)==2)
        model.Add(sum(edge(i,u) for u in range(30,42))+edge(i,42)==2)
    # Actual induced graph: cap all common-neighbour numbers. This includes
    # core/core and mixed core/cycle obligations, not just column intersections.
    ands={}
    def product(a,b):
        if isinstance(a,int):return b if a else 0
        if isinstance(b,int):return a if b else 0
        if a.Index()==b.Index():return a
        key=tuple(sorted((a.Index(),b.Index())))
        if key not in ands:
            v=model.NewBoolVar(f'and{len(ands)}')
            model.Add(v<=a);model.Add(v<=b);model.Add(v>=a+b-1);ands[key]=v
        return ands[key]
    core_common={}
    for i,j in combinations(range(n),2):
        terms=[product(edge(i,k),edge(j,k)) for k in range(n) if k!=i and k!=j]
        if j<16:core_common[i,j]=sum(terms)
        rhs=2-edge(i,j)
        if i in (16,17) or j in (16,17) or (triangle and 42 in (i,j)) or (hcomplete and i<4):
            model.Add(sum(terms)==rhs)
        else:model.Add(sum(terms)<=rhs)
    partial_degree=[sum(edge(i,j) for j in range(n) if i!=j) for i in range(n)]
    for value in partial_degree:model.Add(value<=14)
    if hcomplete:
        for i in range(4):model.Add(partial_degree[i]==14)
    colours={}
    if colour:
        colours={u:model.NewBoolVar(f'c{u}') for u in range(18,n)}
        model.Add(sum(colours[u] for u in range(18,30))+colours[42]==5)
        model.Add(sum(colours[u] for u in range(30,42))+colours[42]==5)
        for i,j in cycle_edges(partition):model.Add(colours[i]+colours[j]<=1)
        for i in range(16):model.Add(sum(product(edge(i,u),colours[u]) for u in colours)<=4-q[i])
        # Every zero-charge vertex outside C has four C neighbours in total.
        for u in colours:
            model.Add(sum(product(edge(u,v),colours[v]) for v in colours if v!=u)<=4*(1-colours[u]))
        if triangle:model.Add(sum(colours[u] for u in range(43,n))==4*(1-colours[42]))
    populations=[]
    if population:
        # The two negative neighbourhoods are complete. Every vertex still
        # absent therefore has positive support column {H_i} or {L_i,L_j}.
        # The full residual Gram matrix determines all these multiplicities.
        for i in range(4):
            for j in range(i+1,16):model.Add(core_common[i,j]==2-edge(i,j))
        for row in [(i,) for i in range(4)]+list(combinations(range(4,16),2)):
            x=model.NewIntVar(0,5 if len(row)==1 else 2,'p_'+'_'.join(map(str,row)))
            if len(row)==1:model.Add(x==14-partial_degree[row[0]])
            else:model.Add(x==2-edge(*row)-core_common[row])
            c=model.NewIntVar(0,5 if len(row)==1 else 2,'pc_'+'_'.join(map(str,row)))
            model.Add(c<=x);populations.append((row,x,c))
        model.Add(sum(x for _,x,_ in populations)==99-n)
        model.Add(sum(c for _,_,c in populations)+sum(colours.values())==21)
        for i in range(16):
            model.Add(sum(x for row,x,_ in populations if i in row)+partial_degree[i]==14)
            model.Add(sum(c for row,_,c in populations if i in row)
                      +sum(product(edge(i,u),colours[u]) for u in colours)==4-q[i])
    return model,variables,fixed,colours,populations


def verify_witness(report):
    n=report.get('vertices',43)
    adj=[set() for _ in range(n)]
    for i,j in report['edges']:adj[i].add(j);adj[j].add(i)
    assert all(len(x)<=14 for x in adj)
    assert len(adj[16])==len(adj[17])==14
    for i,j in combinations(range(n),2):
        assert len(adj[i]&adj[j])<=2-int(j in adj[i]),(i,j)
        if i in (16,17) or j in (16,17) or (report.get('triangle') and 42 in (i,j)) or (report.get('hcomplete') and i<4):
            assert len(adj[i]&adj[j])==2-int(j in adj[i]),(i,j)
    if report.get('triangle'):assert len(adj[42])==14
    if report.get('hcomplete'):assert all(len(adj[i])==14 for i in range(4))
    positive=[2]*4+[1]*12
    assert sum(positive[i] for i in adj[42] if i<16)==4
    for u in range(18,42):assert sum(positive[i] for i in adj[u] if i<16)==3
    for u in range(43,n):assert sum(positive[i] for i in adj[u] if i<16)==2
    C=set(report.get('coclique',[]))
    if C:
        assert all(not(adj[u]&C) for u in C)
        assert len(adj[16]&C)==len(adj[17]&C)==5
        assert all(len(adj[i]&C)<=4-positive[i] for i in range(16))
        if report.get('triangle'):assert len(adj[42]&C)==4*int(42 not in C)
    if report.get('population'):
        populations=report['remaining_population']
        assert sum(x['count'] for x in populations)==99-n
        assert sum(x['coclique_count'] for x in populations)+len(C)==21
        for i in range(16):
            assert len(adj[i])+sum(x['count'] for x in populations if i in x['vertices'])==14
            assert len(adj[i]&C)+sum(x['coclique_count'] for x in populations if i in x['vertices'])==4-positive[i]
        for i,j in combinations(range(16),2):
            assert len(adj[i]&adj[j])+sum(x['count'] for x in populations if i in x['vertices'] and j in x['vertices'])==2-int(j in adj[i])
    return True


def run(folder, seconds=30, workers=4, fixed_core=None, triangle=False, root_h=0, population=False, hcomplete=False):
    folder.mkdir(parents=True,exist_ok=True);all_results=[];begun=time.monotonic()
    for p in partitions(6):
        key='_'.join(map(str,p));out=folder/f'cycles_{key}.json'
        if out.exists():
            old=json.loads(out.read_text())
            if old['status'] in ('OPTIMAL','INFEASIBLE'):
                all_results.append(old);continue
        started=time.monotonic();model,variables,fixed,colours,populations=build(p,fixed_core=fixed_core,triangle=triangle,root_h=root_h,population=population,hcomplete=hcomplete)
        built=time.monotonic();solver=cp_model.CpSolver()
        solver.parameters.num_search_workers=workers;solver.parameters.max_time_in_seconds=seconds
        solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
        with out.with_suffix('.log').open('w') as log:
            solver.log_callback=lambda line:(log.write(line+'\n'),log.flush())
            status=solver.Solve(model)
        result=dict(partition=p,status=solver.StatusName(status),build_seconds=built-started,
                    triangle=triangle,root_h=root_h if triangle or hcomplete else None,
                    vertices=59+root_h if hcomplete else (51+root_h if triangle else 43),
                    population=population,hcomplete=hcomplete,
                    solver_seconds=solver.WallTime(),branches=solver.NumBranches(),conflicts=solver.NumConflicts(),
                    scope='All normalized (0,2) cores' if fixed_core is None else 'One fixed core',
                    relaxation='Complete neighbourhoods of the negative triangle' if triangle else 'Induced two-exception neighbourhood, not a full graph',
                    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    model_stats=model.ModelStats(),response_stats=solver.ResponseStats())
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            result['edges']=sorted(fixed|{e for e,v in variables.items() if solver.Value(v)})
            result['coclique']=[u for u,v in colours.items() if solver.Value(v)]
            result['remaining_population']=[dict(vertices=row,count=solver.Value(x),coclique_count=solver.Value(c))
                                            for row,x,c in populations if solver.Value(x)]
            result['verified']=verify_witness(result)
        out.write_text(json.dumps(result,indent=2)+'\n');all_results.append(result)
        print(json.dumps({k:v for k,v in result.items() if k not in ('edges','coclique','model_stats','response_stats','remaining_population')}),flush=True)
        (folder/'summary.json').write_text(json.dumps(dict(seconds=time.monotonic()-begun,
                    results=[dict(partition=x['partition'],status=x['status']) for x in all_results]),indent=2)+'\n')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--seconds',type=float,default=30)
    ap.add_argument('--workers',type=int,default=4);ap.add_argument('--core',type=Path)
    ap.add_argument('--triangle',action='store_true');ap.add_argument('--root-h',type=int,choices=(0,1),default=0)
    ap.add_argument('--population',action='store_true')
    ap.add_argument('--hcomplete',action='store_true')
    args=ap.parse_args();run(args.folder,args.seconds,args.workers,json.loads(args.core.read_text()) if args.core else None,args.triangle,args.root_h,args.population,args.hcomplete)
