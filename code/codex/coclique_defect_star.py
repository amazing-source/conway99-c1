"""A real matching in the neighbourhood of a mandatory zero-charge vertex.

Local version: exact common-neighbour demands, followed by N(z)=7K2.
Population version: the same selected neighbours must belong to one Gram
factorization and its one coclique. Feasibility is still only necessary.
"""
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json
import time

from ortools.sat.python import cp_model
from coclique_defect_gluing import gluing_data


def targets(data, row):
    return [2-((row >> i)&1)-(row & nbr).bit_count()
            for i, nbr in enumerate(data['neighbours'])]


def compatible(data, r, t, *, common_root=False):
    if (r & t).bit_count() > (0 if common_root else 1):
        return False
    hr, ht = targets(data, r), targets(data, t)
    return all(hr[i] > 0 for i in range(len(hr)) if (t >> i)&1) and all(
        ht[i] > 0 for i in range(len(ht)) if (r >> i)&1)


def population(model, data, core):
    n=len(data['charges']);rows=data['rows']
    counts=[];coclique=[];used=[]
    for t,row in enumerate(rows):
        members=[i for i in range(n) if row>>i&1]
        upper=min([data['order']-n]+[data['outside_degrees'][i] for i in members]
                  +[data['residual'][i,j] for i,j in combinations(members,2)])
        if len(members)>=3:upper=min(upper,1)
        x=model.NewIntVar(0,upper,f'x{t}');c=model.NewIntVar(0,upper,f'c{t}')
        b=model.NewBoolVar(f'used{t}')
        model.Add(c<=x);model.Add(x>=b);model.Add(x<=upper*b)
        counts.append(x);coclique.append(c);used.append(b)
    model.Add(sum(counts)==data['order']-n)
    model.Add(sum(coclique)==data['coclique_size'])
    for i in range(n):
        idx=[t for t,row in enumerate(rows) if row>>i&1]
        model.Add(sum(counts[t] for t in idx)==data['outside_degrees'][i])
        model.Add(sum(coclique[t] for t in idx)==core['boundary_degrees'][i])
    for (i,j),need in data['residual'].items():
        model.Add(sum(counts[t] for t,row in enumerate(rows) if row>>i&1 and row>>j&1)==need)
    for t,u in combinations(range(len(rows)),2):
        if (rows[t]&rows[u]).bit_count()>2:model.Add(used[t]+used[u]<=1)
    return counts,coclique


def root_model(core, data, root, *, with_population=False):
    n=len(data['charges']);rows=data['rows'];r=rows[root]
    h=targets(data,r);degree=core['parameters']['degree']
    model=cp_model.CpModel()
    pop=population(model,data,core) if with_population else None
    if pop:
        counts,coclique=pop
        model.Add(counts[root]==1)
    copies=[];selected=[];colour=[]
    for t,s in enumerate(rows):
        if not compatible(data,r,s):continue
        # In this reduction all neighbours are singleton charge-2 or pairs
        # of charge-1. A pair may occur only once: two copies and the root
        # would give three common neighbours to those two vertices.
        assert s.bit_count()<=2 and all(data['charges'][i]>0 for i in range(n) if s>>i&1)
        upper=min(h[i] for i in range(n) if s>>i&1)
        if s.bit_count()==2:upper=min(upper,1)
        for k in range(upper):
            copies.append((t,s));selected.append(model.NewBoolVar(f'sel{t}_{k}'))
            if pop:
                colour.append(model.NewBoolVar(f'inC{t}_{k}'))
                model.Add(colour[-1]<=selected[-1])
                model.Add(colour[-1]+coclique[root]<=1)
        if pop:
            ids=[j for j,(tt,_) in enumerate(copies) if tt==t]
            model.Add(sum(selected[j] for j in ids)<=counts[t]-int(t==root))
            model.Add(sum(colour[j] for j in ids)<=coclique[t]-(coclique[root] if t==root else 0))
            model.Add(sum(selected[j]-colour[j] for j in ids)<=counts[t]-coclique[t]-(1-coclique[root] if t==root else 0))
    model.Add(sum(selected)==degree-r.bit_count())
    for i,need in enumerate(h):
        model.Add(sum(selected[j] for j,(_,s) in enumerate(copies) if s>>i&1)==need)
    if pop:
        b=4 if degree==14 else 2
        model.Add(sum(colour)==b*(1-coclique[root]))
    free=[j for j,(_,s) in enumerate(copies) if not(s&r)]
    mates={}
    for j,k in combinations(free,2):
        if not compatible(data,copies[j][1],copies[k][1],common_root=True):continue
        v=model.NewBoolVar(f'mate{j}_{k}');mates[j,k]=v
        model.Add(v<=selected[j]);model.Add(v<=selected[k])
        if pop:model.Add(v+colour[j]+colour[k]<=2)
    for j in free:
        model.Add(sum(v for (a,b),v in mates.items() if j in (a,b))==selected[j])
    return model,copies,selected,mates,pop,colour


def verify_star(data, root, selected, matching):
    """Check the actual induced partial graph, independently of CP equations."""
    q=data['charges'];n=len(q);r=data['rows'][root]
    adjacency=[set() for _ in range(n+1+len(selected))]
    def add(i,j):adjacency[i].add(j);adjacency[j].add(i)
    for i,m in enumerate(data['neighbours']):
        for j in range(i+1,n):
            if m>>j&1:add(i,j)
    for i in range(n):
        if r>>i&1:add(i,n)
    for k,s in enumerate(selected):
        add(n,n+1+k)
        for i in range(n):
            if s>>i&1:add(i,n+1+k)
    for j,k in matching:add(n+1+j,n+1+k)
    for i,j in combinations(range(len(adjacency)),2):
        assert len(adjacency[i]&adjacency[j])<=2-int(j in adjacency[i]),(i,j)
    for v in adjacency[n]:assert len(adjacency[v]&adjacency[n])==1
    assert all(len(adjacency[i]&adjacency[n])==2-int(i in adjacency[n]) for i in range(n))
    return True


def probe(core, *, order=99, coclique_size=21, seconds=10, with_population=False, limit=None):
    data=gluing_data(core,order,coclique_size);q=data['charges'];n=len(q)
    negative=sum(1<<i for i,v in enumerate(q) if v<0)
    roots=[t for t,r in enumerate(data['rows']) if r&negative==negative]
    if limit is not None:roots=roots[:limit]
    results=[];start=time.monotonic()
    for root in roots:
        model,copies,selected,mates,pop,colour=root_model(core,data,root,with_population=with_population)
        solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
        solver.parameters.max_time_in_seconds=seconds
        status=solver.Solve(model)
        entry=dict(root=[i for i in range(n) if data['rows'][root]>>i&1],
                   status=solver.StatusName(status),seconds=solver.WallTime(),
                   branches=solver.NumBranches(),conflicts=solver.NumConflicts())
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            ids=[j for j,v in enumerate(selected) if solver.Value(v)]
            new_id={old:new for new,old in enumerate(ids)}
            rows=[copies[j][1] for j in ids]
            matching=[(new_id[j],new_id[k]) for (j,k),v in mates.items() if solver.Value(v)]
            entry['star_verified']=verify_star(data,root,rows,matching)
            entry['zero_neighbour_types']=[[i for i in range(n) if s>>i&1] for s in rows]
            entry['matching']=matching
            if pop:
                counts,coclique=pop
                entry['root_in_coclique']=solver.Value(coclique[root])
                entry['neighbours_in_coclique']=[solver.Value(colour[j]) for j in ids]
                entry['selected_rows']=[dict(vertices=[i for i in range(n) if s>>i&1],
                                             count=solver.Value(counts[t]),coclique_count=solver.Value(coclique[t]))
                                        for t,s in enumerate(data['rows']) if solver.Value(counts[t])]
        results.append(entry)
        if len(results)%10==0:print(json.dumps(dict(done=len(results),roots=len(roots),seconds=round(time.monotonic()-start,3))),flush=True)
    return dict(roots=len(roots),status_counts={s:sum(r['status']==s for r in results) for s in sorted({r['status'] for r in results})},
                seconds=time.monotonic()-start,with_population=with_population,
                complete=limit is None and all(r['status'] in ('OPTIMAL','INFEASIBLE') for r in results),
                scope='Necessary realized root star'+(' in a common population' if with_population else '')+'; not a complete SRG',
                results=results)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('core',type=Path)
    ap.add_argument('--population',action='store_true');ap.add_argument('--seconds',type=float,default=10)
    ap.add_argument('--limit',type=int);ap.add_argument('--order',type=int,default=99);ap.add_argument('--coclique',type=int,default=21)
    args=ap.parse_args();raw=args.core.read_bytes()
    report=probe(json.loads(raw),order=args.order,coclique_size=args.coclique,seconds=args.seconds,with_population=args.population,limit=args.limit)
    report.update(input_sha256=hashlib.sha256(raw).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    output=args.core.with_name(args.core.stem+'_star'+('_population' if args.population else '')+'.json')
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'}),flush=True)
