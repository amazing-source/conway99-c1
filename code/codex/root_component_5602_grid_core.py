"""Attach all seven grid rectangles of 5602 to its eight-vertex core.

This is a necessary induced graph on 36 vertices, with all Gram entries
free. Outside it lie exactly the 48 vertices of the twelve A x B
nongrid rectangles, A={0,1,2,3}, B={4,5,6}. Each outside vertex has one
neighbour in the core and in exactly one B-grid, so it cannot contribute
to a common-neighbour count of two core vertices or two distinct B-grids.
SAT is only a partial graph. UNSAT excludes the specified core orbit.
"""

import argparse
from itertools import combinations, product
import json
import hashlib
from collections import Counter
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process

CORE = [(0,3),(1,2)]
GRIDS = [(0,1),(0,2),(1,3),(2,3),(4,5),(4,6),(5,6)]


def closed_pair(u,v):
    """The 48 remaining vertices can have no common adjacency to this pair."""
    if v<8:return True
    if u>=8 and u//4==v//4:return True
    if u>=24:return True
    rectangles=CORE+GRIDS
    return u>=8 and v<24 and set(rectangles[u//4]).isdisjoint(rectangles[v//4])


def build(core,boundary=None):
    from ortools.sat.python import cp_model
    rectangles = CORE+GRIDS
    labels = [(a,b) for q in rectangles for a in (2*q[0],2*q[0]+1) for b in (2*q[1],2*q[1]+1)]
    model=cp_model.CpModel(); n=len(labels)
    graph=[[0]*n for _ in range(n)]
    for u,v in combinations(range(n),2):
        qu,qv=rectangles[u//4],rectangles[v//4]
        if u<8 and v<8: edge=core[u][v]
        elif boundary is not None and u<8 and v>=24: edge=int(bool(boundary[v-24]&(1<<u)))
        elif u//4==v//4: edge=int(bool(set(labels[u])&set(labels[v])))
        elif set(qu)&set(qv): edge=0
        else: edge=model.new_bool_var(f'g_{u}_{v}')
        graph[u][v]=graph[v][u]=edge
    for w in range(n):
        for qi,q in enumerate(rectangles[2:],start=2):
            expected=(2 if w//4==qi else 0 if set(rectangles[w//4])&set(q) else 1)
            model.add(sum(graph[w][4*qi+j] for j in range(4))==expected)
        if w>=24:
            model.add(sum(graph[w][:8])==2)
        for letter in range(14):
            bound=2-int(letter in labels[w])-int((letter^1) in labels[w])
            model.add(sum(graph[w][v] for v in range(n) if letter in labels[v])<=bound)
    conjunctions={}
    def conjunction(x,y):
        if isinstance(x,int): return y if x else 0
        if isinstance(y,int): return x if y else 0
        if x.index==y.index: return x
        key=tuple(sorted((x.index,y.index)))
        if key not in conjunctions:
            z=model.new_bool_var(f'product_{key[0]}_{key[1]}')
            model.add(z<=x);model.add(z<=y);model.add(z>=x+y-1)
            conjunctions[key]=z
        return conjunctions[key]
    exact=inequalities=0
    for u,v in combinations(range(n),2):
        total=sum(conjunction(graph[u][w],graph[v][w]) for w in range(n))
        target=2-graph[u][v]-len(set(labels[u])&set(labels[v]))
        closed=closed_pair(u,v)
        if closed: model.add(total==target);exact+=1
        else: model.add(total<=target);inequalities+=1
    assert not model.validate(),model.validate()
    return model,labels,graph,{'vertices':n,'products':len(conjunctions),
                              'exact_pair_counts':exact,'pair_upper_bounds':inequalities}


def solve(core,seconds,boundary=None):
    from ortools.sat.python import cp_model
    start=time.process_time();model,labels,g,info=build(core,boundary)
    build_cpu=time.process_time()-start
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    solver.parameters.cp_model_probing_level=0
    solver.parameters.max_time_in_seconds=max(30,100*seconds)
    done=threading.Event();start=time.process_time()
    def stop():
        while not done.wait(.05):
            if time.process_time()-start>=seconds: solver.stop_search()
    thread=threading.Thread(target=stop,daemon=True);thread.start()
    try: status=solver.solve(model)
    finally: done.set();thread.join()
    out={'status':solver.status_name(status),'cpu_seconds':time.process_time()-start,
         'build_cpu_seconds':build_cpu,'variables':len(model.proto.variables),
         'constraints':len(model.proto.constraints),'branches':solver.num_branches,
         'conflicts':solver.num_conflicts,'model_info':info,'is_complete_graph':False,
         'portable_unsat_proof':False}
    if boundary is not None:out['fixed_twenty_vertex_boundary']=boundary
    if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
        gg=[[int(x) if isinstance(x,int) else solver.value(x) for x in row] for row in g]
        for u,v in combinations(range(36),2):
            total=sum(gg[u][w]*gg[v][w] for w in range(36))
            target=2-gg[u][v]-len(set(labels[u])&set(labels[v]))
            assert total<=target
            if closed_pair(u,v):assert total==target
        for w in range(36):
            for qi,q in enumerate((CORE+GRIDS)[2:],start=2):
                expected=2 if w//4==qi else 0 if set((CORE+GRIDS)[w//4])&set(q) else 1
                assert sum(gg[w][4*qi+j] for j in range(4))==expected
            if w>=24:assert sum(gg[w][:8])==2
            for a in range(14):
                assert sum(gg[w][v] for v in range(36) if a in labels[v])<=2-int(a in labels[w])-int((a^1) in labels[w])
        out.update(adjacency=gg,labels=labels,integer_witness_checked=True)
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cores',type=Path,required=True)
    p.add_argument('--seconds',type=float,default=5)
    p.add_argument('--orbit',type=int,nargs='*')
    p.add_argument('--boundary',action='store_true',help='Use the complete 20-vertex cover carried by --cores.')
    p.add_argument('--boundary-indices',type=int,nargs='*')
    p.add_argument('--boundary-limit',type=int)
    p.add_argument('--marginal-filter',action='store_true')
    p.add_argument('--stop-on-feasible',action='store_true')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists();resources=limit_research_process(1)
    data=json.loads(a.cores.read_text(encoding='utf8'))
    orbits=data.get('orbit_reduction',data)['orbits']
    out={'scope':__doc__,'source':str(a.cores),'source_sha256':hashlib.sha256(a.cores.read_bytes()).hexdigest(),
         'resources':resources,'cases':[],
         'whole_template_excluded':False,'global_Conway_exclusion':False}
    for i,orbit in enumerate(orbits):
        if a.orbit is not None and i not in a.orbit:continue
        choices=[(None,None)]
        if a.boundary:
            choices=[(j,c['core_neighbours_of_grid_vertices']) for j,c in enumerate(orbit['boundaries']['cases'])
                     if a.boundary_indices is None or j in a.boundary_indices]
            if a.boundary_limit is not None:choices=choices[:a.boundary_limit]
        for j,boundary in choices:
            marginal=None
            if boundary is not None and a.marginal_filter:
                from root_component_5602_grid_marginals import test
                marginal=test(boundary)
            if marginal is not None and marginal['status']=='EXCLUDED_BOUNDARY':
                result={'status':'EXCLUDED_BY_INTEGER_MARGINS','marginals':marginal,
                        'cpu_seconds':0,'is_complete_graph':False}
            else:
                result=solve(orbit['representative'],a.seconds,boundary)
            case={'orbit':i,'boundary_index':j,'mask':orbit['mask'],
                  'result':result}
            out['cases'].append(case);atomic_json_write(a.output,out)
            if not a.boundary or len(out['cases'])%25==0 or result['status'] in ('OPTIMAL','FEASIBLE'):
                print(json.dumps({'orbit':i,'boundary_index':j,'processed':len(out['cases']),
                                 'counts':dict(Counter(c['result']['status'] for c in out['cases']))}),flush=True)
            if a.stop_on_feasible and result['status'] in ('OPTIMAL','FEASIBLE'):return
    print(json.dumps({'processed':len(out['cases']),
                      'counts':dict(Counter(c['result']['status'] for c in out['cases']))}),flush=True)


if __name__=='__main__':main()
