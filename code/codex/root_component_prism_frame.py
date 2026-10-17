"""Complete a line neighbourhood using two prism components as a frame.

Let L be a triangle, C the cubic graph on its 36 neighbours, coloured by
their unique neighbour in L, and D its incidence to the remaining 60
vertices.  Every outside vertex meets each six-vertex component once.
Two prism components P,Q therefore label the 60 outside vertices by
(p,q,copy): one copy when p,q have the same colour, two copies otherwise.
This follows from (DD^t)[p,q]=2-[same colour]. It is a relabelling of every
completion, not a choice of a boundary seed.

All completions satisfy
 DD^t=12I-C-C^2+2J-Z,  D(H+I)=2J-CD,
 H^2+H+D^tD=12I+2J,
where H is symmetric binary with degree 8, and each column of D has two
entries in each colour. Stage 0 imposes DD^t, stage 1 also the twelve
fixed rows of D(H+I), stage 2 all of D(H+I), stage 3 all three identities.
Only stage 3 can produce a full SRG; weaker SATs are boundary witnesses.

For the remaining root templates: template 7 has a six-prism line, while
9 and 19 have a line with components 12+12+6+6. The first case has one
neighbourhood type; the second is covered by 14*32=448 types. Normalize
colours on the first 12-component only; retain colour-preserving types
on the second. A repeated isomorphism is harmless; omitting relative
colour orientations would not be sound. No time bound is asserted.
"""

import argparse
from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process
from ortools.sat.python import cp_model


def component(record=None,code=None):
    if record is None:
        n=2;perm=[0,1];matchings=[[(0,1)]]*3
    else:
        p,a,b=code;perm=record['cross_permutations'][p];n=len(perm)
        matchings=[[(i,i+1) for i in range(0,n,2)],
                   record['internal_matchings'][a],record['internal_matchings'][b]]
    c=[[0]*(3*n) for _ in range(3*n)]
    def edge(u,v):c[u][v]=c[v][u]=1
    for colour,matching in enumerate(matchings):
        for a,b in matching:edge(colour*n+a,colour*n+b)
    for i in range(n):
        edge(i,n+i);edge(i,2*n+i);edge(n+i,2*n+perm[i])
    assert all(sum(row)==3 for row in c)
    return c,[i//n for i in range(3*n)]


def neighbourhood(library,orbits,family,first,second):
    cs=[component(),component()]
    descriptors=[{'vertices':6},{'vertices':6}]
    if family=='six-prisms':
        assert first==second==0
        cs += [component() for _ in range(4)]
        descriptors += [{'vertices':6} for _ in range(4)]
    else:
        record=next(r for r in library['records'] if r['vertices']==12)
        for index,colours in ((first,True),(second,False)):
            cover=next(r for r in orbits['records'] if r['vertices']==12 and r['allow_colour_permutations']==colours)
            assert cover['all_generator_images_in_source'] and cover['all_codes_covered_disjointly']
            code=cover['orbits'][index]['representative']
            cs.append(component(record,code))
            descriptors.append({'vertices':12,'orbit_index':index,'allow_colour_permutations':colours,'code':code})
    c=[[0]*36 for _ in range(36)];colours=[];groups=[];offset=0
    for (block,colour),description in zip(cs,descriptors):
        group=list(range(offset,offset+len(block)));groups.append(group)
        for i,row in enumerate(block):
            for j,value in enumerate(row):c[offset+i][offset+j]=value
        colours.extend(colour);description['vertices_in_neighbourhood']=group
        offset+=len(block)
    assert offset==36 and Counter(colours)=={0:12,1:12,2:12}
    return c,colours,groups,descriptors


def build(c,colours,groups,stage,minc_lines=0):
    cells=[(p,q,copy) for p in range(6) for q in range(6,12)
           for copy in range(2-int(colours[p]==colours[q]))]
    assert len(cells)==60
    m=cp_model.CpModel()
    d=[[int(u==p or u==q) if u<12 else m.new_bool_var(f'd_{u}_{x}')
        for x,(p,q,_) in enumerate(cells)] for u in range(36)]
    cn=[[sum(c[u][z]*c[v][z] for z in range(36)) for v in range(36)] for u in range(36)]
    targets=[[12*int(u==v)-c[u][v]-cn[u][v]+2-int(colours[u]==colours[v])
              for v in range(36)] for u in range(36)]
    assert all(targets[u][u]==10 for u in range(36))
    assert min(map(min,targets))>=0
    products={}
    def product(a,b):
        if isinstance(a,int):return b if a else 0
        if isinstance(b,int):return a if b else 0
        if a.index==b.index:return a
        key=tuple(sorted((a.index,b.index)))
        if key not in products:
            v=m.new_bool_var(f'product_{len(products)}')
            m.add(v<=a);m.add(v<=b);m.add(v>=a+b-1);products[key]=v
        return products[key]
    for u in range(36):m.add(sum(d[u])==10)
    for x in range(60):
        for colour in range(3):m.add(sum(d[u][x] for u in range(36) if colours[u]==colour)==2)
        for group in groups:m.add(sum(d[u][x] for u in group)==len(group)//6)
        for u in range(36):
            # The neighbours of an outside vertex induce a matching.
            terms=[d[v][x] for v in range(36) if c[u][v]]
            m.add(sum(terms)<=1+3*(1-d[u][x]))
    for u,v in combinations(range(36),2):
        target=targets[u][v]
        if target==0:
            for x in range(60):m.add(d[u][x]+d[v][x]<=1)
        else:m.add(sum(product(d[u][x],d[v][x]) for x in range(60))==target)
    from root_component_rotated_boundary import fixed_forbidden_triples
    forbidden=fixed_forbidden_triples(c,colours)
    for triple in forbidden:
        for x in range(60):m.add(sum(d[u][x] for u in triple)<=2)
    # The two copies of a cell have interchangeable outside names. Ordering
    # their D columns is a valid simultaneous row/column relabelling of H.
    for x in range(59):
        if cells[x][:2]!=cells[x+1][:2]:continue
        prefix=1
        for u in range(12,36):
            a,b=d[u][x],d[u][x+1]
            m.add(a<=b).only_enforce_if(prefix)
            equal=m.new_bool_var(f'equal_{x}_{u}')
            m.add(a==b).only_enforce_if(equal)
            m.add(a!=b).only_enforce_if(equal.Not())
            if isinstance(prefix,int):prefix=equal
            else:
                both=m.new_bool_var(f'prefix_{x}_{u}')
                m.add(both<=prefix);m.add(both<=equal);m.add(both>=prefix+equal-1)
                prefix=both
    h=None;dh_count=0;core_count=0
    if stage:
        h=[[0]*60 for _ in range(60)]
        for x,y in combinations(range(60),2):
            # Same cell already means two shared neighbours in P union Q.
            h[x][y]=h[y][x]=0 if cells[x][:2]==cells[y][:2] else m.new_bool_var(f'h_{x}_{y}')
        for x in range(60):m.add(sum(h[x])==8)
        for u in range(36 if stage>=2 else 12):
            for x in range(60):
                m.add(sum(product(d[u][y],h[y][x]) for y in range(60))
                      +d[u][x]+sum(d[v][x] for v in range(36) if c[u][v])==2)
                dh_count+=1
        if stage>=3:
            for x,y in combinations(range(60),2):
                m.add(h[x][y]+sum(product(h[x][z],h[y][z]) for z in range(60))
                      +sum(product(d[u][x],d[u][y]) for u in range(36))==2)
                core_count+=1
    partition_info=None
    if minc_lines:
        assert h is not None
        full=full_graph(c,colours,d,h)
        lines=[(colour,3+u,3+v) for colour in range(3)
               for u,v in combinations(range(36),2)
               if colours[u]==colours[v]==colour and c[u][v]][:minc_lines]
        from root_component_minimum_partition import add_partitions_for_lines
        partition_info=add_partitions_for_lines(m,full,lines)
    return m,d,h,{'stage':stage,'full_SRG_equations':stage==3,'cells':[list(t) for t in cells],
                  'DDt_pair_equations':630,'DH_equations':dh_count,'core_pair_equations':core_count,
                  'products':len(products),'minimum_components':partition_info,
                  'rotated_forbidden_triples':[list(t) for t in forbidden],
                  'variables':len(m.proto.variables),'constraints':len(m.proto.constraints)}


def full_graph(c,colours,d,h):
    graph=[[0]*99 for _ in range(99)]
    for a,b in combinations(range(3),2):graph[a][b]=graph[b][a]=1
    for u in range(36):
        graph[colours[u]][3+u]=graph[3+u][colours[u]]=1
        for v in range(36):graph[3+u][3+v]=c[u][v]
        for x in range(60):graph[3+u][39+x]=graph[39+x][3+u]=d[u][x]
    for x in range(60):
        for y in range(60):graph[39+x][39+y]=h[x][y]
    return graph


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path)
    p.add_argument('--family',choices=['six-prisms','double12'],required=True)
    p.add_argument('--first',type=int,default=0);p.add_argument('--second',type=int,default=0)
    p.add_argument('--stage',type=int,choices=range(4),default=1)
    p.add_argument('--minc-lines',type=int,default=0)
    p.add_argument('--seconds',type=float,default=60)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();resources=limit_research_process(1)
    tables_path=args.directory/'line_component_pattern_tables_rotated.json'
    orbit_path=args.directory/'line_component_colored_orbits.json'
    raw=tables_path.read_bytes();library=json.loads(raw);orbits=json.loads(orbit_path.read_bytes())
    assert orbits['source_sha256']==hashlib.sha256(raw).hexdigest()
    c,colours,groups,descriptors=neighbourhood(library,orbits,args.family,args.first,args.second)
    started=time.process_time();m,d,h,info=build(c,colours,groups,args.stage,args.minc_lines)
    assert not m.validate(),m.validate()
    info.update(status='MODEL_BUILT',scope=__doc__,family=args.family,first=args.first,second=args.second,
                components=descriptors,resources=resources,build_cpu_seconds=time.process_time()-started,
                source_sha256=hashlib.sha256(raw).hexdigest())
    atomic_json_write(args.output,info)
    print({k:v for k,v in info.items() if k not in ('scope','cells','components')},flush=True)
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=max(600,100*args.seconds)
    solver.parameters.symmetry_level=0;solver.parameters.cp_model_probing_level=0
    solver.parameters.linearization_level=0
    started=time.process_time();done=threading.Event()
    def interrupt():
        while not done.wait(.05):
            if time.process_time()-started>=args.seconds:solver.stop_search();return
    timer=threading.Thread(target=interrupt,daemon=True);timer.start()
    try:status=solver.solve(m)
    finally:done.set();timer.join()
    info.update(status=solver.status_name(status),solver_cpu_seconds=time.process_time()-started,
                branches=solver.num_branches,conflicts=solver.num_conflicts)
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        dd=[[solver.value(v) for v in row] for row in d]
        info['D_columns']=[[u for u in range(36) if dd[u][x]] for x in range(60)]
        if h is not None:
            hh=[[solver.value(v) for v in row] for row in h]
            info['H_edges']=[[x,y] for x,y in combinations(range(60),2) if hh[x][y]]
            graph=full_graph(c,colours,dd,hh)
            errors=[(u,v) for u,v in combinations(range(99),2)
                    if sum(graph[u][z]*graph[v][z] for z in range(99))!=2-graph[u][v]]
            info['missing_SRG_pair_equations']=len(errors)
            info['full_SRG_verified']=not errors and all(sum(row)==14 for row in graph)
            if args.stage==3:assert info['full_SRG_verified']
    atomic_json_write(args.output,info)
    print({k:v for k,v in info.items() if k not in ('scope','cells','components','D_columns','H_edges')},flush=True)


if __name__=='__main__':main()
