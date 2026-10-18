"""Extend each of the59 four-grid-line balls, with all boundary rows variable.

Stage0 imposes C1 on its24 Gamma vertices, exact common-neighbour counts
between them and upper bounds between the other60 vertices. A feasible
stage0 is only a boundary witness. Stage1 adds all remaining Gamma edges,
C1 and C2, so a feasible stage1 must pass the complete99-vertex identities.
Family7 keeps all four possible isolated axes; family9 keeps all three
partitions of the four internal axes into two pairs. Therefore the S4
normalization of the ball never fixes an incompatible template orientation.
No particular completion of the boundary is prescribed.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process
from root_component_grid4_cover import gamma_ball,PAIRS,OPPOSITE
from root_component_propagation import LABELS,RECTANGLES


def build(code,family,stage):
    from ortools.sat.python import cp_model
    labels,c=gamma_ball(code);loc={p:i for i,p in enumerate(LABELS)}
    known=[loc[p] for p in labels];outside=[w for w in range(84) if w not in known]
    model=cp_model.CpModel();g=[[0]*84 for _ in range(84)];products={}
    for i,u in enumerate(known):
        for j,v in enumerate(known):g[u][v]=c[i][j]
    for u in known:
        axes_u={a//2 for a in LABELS[u]}
        for v in outside:
            if axes_u & {a//2 for a in LABELS[v]}:continue
            g[u][v]=g[v][u]=model.new_bool_var(f'd_{u}_{v}')
    if stage:
        for u,v in combinations(outside,2):g[u][v]=g[v][u]=model.new_bool_var(f'h_{u}_{v}')
    def product(a,b):
        if isinstance(a,int):return b if a else 0
        if isinstance(b,int):return a if b else 0
        if a.index==b.index:return a
        key=tuple(sorted((a.index,b.index)))
        if key not in products:
            p=model.new_bool_var(f'product_{len(products)}')
            model.add(p<=a);model.add(p<=b);model.add(p>=a+b-1);products[key]=p
        return products[key]
    for w in outside:
        for pair in PAIRS:
            target=1-sum(a//2 in pair for a in LABELS[w])
            assert target in (0,1)
            model.add(sum(g[w][v] for v in RECTANGLES[pair])==target)
    for u in (list(range(84)) if stage else known):
        for a in range(14):
            model.add(sum(g[u][v] for v in range(84) if a in LABELS[v])==2-int(a in LABELS[u])-int((a^1) in LABELS[u]))
    for u,v in combinations(known,2):
        target=2-len(set(LABELS[u])&set(LABELS[v]))-g[u][v]-sum(g[u][w]*g[v][w] for w in known)
        if target==0:
            for w in outside:model.add(g[u][w]+g[v][w]<=1)
        else:model.add(sum(product(g[u][w],g[v][w]) for w in outside)==target)
    for u,v in combinations(outside,2):
        cap=2-len(set(LABELS[u])&set(LABELS[v]))
        model.add(sum(product(g[u][w],g[v][w]) for w in known)<=cap)
    grid={pair:1 for pair in PAIRS}
    if family in (7,9):grid.update({pair:1 for pair in combinations(range(4,7),2)})
    orientations=[]
    if family==7:
        orientations=[model.new_bool_var(f'isolated_axis_{i}') for i in range(4)]
        model.add_exactly_one(orientations)
        for i in range(4):
            for j in range(4,7):grid[i,j]=orientations[i]
    elif family==9:
        orientations=[model.new_bool_var(f'partition_{i}') for i in range(3)]
        model.add_exactly_one(orientations)
        for oi,parts in enumerate(OPPOSITE):
            for axis in range(4,7):
                for part in parts:
                    vertices=[v for v in outside if axis in {a//2 for a in LABELS[v]}
                              and any(a//2 in part for a in LABELS[v])]
                    for u in known:
                        target=2-sum(a//2 in part for a in LABELS[u])
                        model.add(sum(g[u][v] for v in vertices)==target).only_enforce_if(orientations[oi])
    for pair,active in grid.items():
        corners=RECTANGLES[pair];letters={2*i+b for i in pair for b in (0,1)}
        for u in (list(range(84)) if stage else known):
            target=1+3*int(u in corners)-len(set(LABELS[u])&letters)
            constraint=model.add(sum(g[u][v] for v in corners)==target)
            if not isinstance(active,int):constraint.only_enforce_if(active)
        if stage:
            for u,v in combinations(corners,2):
                constraint=model.add(g[u][v]==int(bool(set(LABELS[u])&set(LABELS[v]))))
                if not isinstance(active,int):constraint.only_enforce_if(active)
    if stage:
        for u,v in combinations(range(84),2):
            if u in known and v in known:continue
            model.add(g[u][v]+sum(product(g[u][w],g[v][w]) for w in range(84))==2-len(set(LABELS[u])&set(LABELS[v])))
    assert not model.validate(),model.validate()
    return model,g,{'boundary_variables':sum(not isinstance(g[u][v],int) for u in known for v in outside),
                    'product_variables':len(products),'variables':len(model.proto.variables),
                    'constraints':len(model.proto.constraints),'known_gamma_vertices':known,
                    'orientation_choices':len(orientations),'full_SRG_constraints':bool(stage)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cover',type=Path);parser.add_argument('--indices',type=int,nargs='+')
    parser.add_argument('--family',type=int,choices=(0,7,9),default=0)
    parser.add_argument('--stage',type=int,choices=(0,1),default=0)
    parser.add_argument('--seconds',type=float,default=10)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();resources=limit_research_process(1)
    from ortools.sat.python import cp_model
    cover=json.loads(args.cover.read_text());assert cover['exhaustive'] and cover['orbit_count']==59
    options={'family':args.family,'stage':args.stage,'seconds':args.seconds}
    result={'scope':__doc__,'options':options,'complete_ball_count':59,'resources':resources,'records':[]}
    if args.output.exists():
        result=json.loads(args.output.read_text());assert result['options']==options
    seen={r['index'] for r in result['records']}
    for item in cover['records']:
        index=item['index']
        if index in seen or args.indices is not None and index not in args.indices:continue
        start=time.process_time();model,g,info=build(item['representative'],args.family,args.stage)
        info['build_cpu_seconds']=time.process_time()-start
        solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
        solver.parameters.cp_model_probing_level=0;solver.parameters.symmetry_level=0;solver.parameters.linearization_level=0
        solver.parameters.max_time_in_seconds=max(600,100*args.seconds)
        start=time.process_time();done=threading.Event()
        def interrupt():
            while not done.wait(.05):
                if time.process_time()-start>=args.seconds:solver.stop_search();return
        timer=threading.Thread(target=interrupt,daemon=True);timer.start()
        try:status=solver.solve(model)
        finally:done.set();timer.join()
        row=dict(info,index=index,representative=item['representative'],status=solver.status_name(status),
                 cpu_seconds=time.process_time()-start,branches=solver.num_branches,conflicts=solver.num_conflicts)
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            known=set(info['known_gamma_vertices'])
            row['edges']=[[u,v] for u,v in combinations(range(84),2) if (args.stage or u in known or v in known) and solver.value(g[u][v])]
            if args.stage:
                a=[[solver.value(e) for e in line] for line in g]
                errors=sum(a[u][v]+sum(a[u][w]*a[v][w] for w in range(84))!=2-len(set(LABELS[u])&set(LABELS[v]))
                           for u,v in combinations(range(84),2))
                assert errors==0
                row['full_C2_errors']=errors
        result['records'].append(row)
        result['counts']=dict(Counter(r['status'] for r in result['records']))
        result['complete_cover_excluded']=len(result['records'])==59 and all(r['status']=='INFEASIBLE' for r in result['records'])
        atomic_json_write(args.output,result)
        print(json.dumps({k:row[k] for k in ('index','status','build_cpu_seconds','cpu_seconds','branches','conflicts')}),flush=True)


if __name__=='__main__':main()
