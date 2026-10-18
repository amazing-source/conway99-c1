"""Eight unseeded global models using the necessary existence of c(L)<=3.

The root is not required to lie on L. The eight relative positions form
a complete cover before any additional root-template normalization. All
84x84 unknown adjacencies are variable. No local witness, Gram, matching
template, automorphism, or prism budget at the selected line is assumed.
This finite specification has no proved affordable running time.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import threading
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ortools.sat.python import cp_model
from conway_global_cover import build_global,reconstruct_and_check
from root_component_resources import atomic_json_write,limit_research_process
from root_component_small_line import add_small_line
from root_component_triangle_orbits import cover


def full_matrix(k,labels,gamma):
    n=1+k+len(labels);graph=[[0]*n for _ in range(n)]
    for a in range(k):
        graph[0][a+1]=graph[a+1][0]=1
        graph[a+1][(a^1)+1]=1
    for w,pair in enumerate(labels,k+1):
        for a in pair:graph[a+1][w]=graph[w][a+1]=1
    for u,v in combinations(range(len(labels)),2):
        graph[k+1+u][k+1+v]=graph[k+1+v][k+1+u]=gamma[u][v]
    return graph


def build(case,maximum_components=3,k=14,prism_budget=False,rectangle_moments=None):
    assert k in (4,14) and (k==14 or case==0)
    model,labels,gamma,selectors,info=build_global(k=k,normalize_star=False)
    assert not selectors and not info['star_matching_normalization']
    graph=full_matrix(k,labels,gamma)
    record=cover()['records'][case] if k==14 else {'index':0,'kind':'through_root','line':[0,1,2]}
    line_info=add_small_line(model,graph,record['line'],maximum_components)
    moment_info=None
    if rectangle_moments:
        assert rectangle_moments in ('diagonal','full')
        from root_component_neighbor_moments import add_neighbor_moments
        moment_info=add_neighbor_moments(model,labels,gamma,mixed=rectangle_moments=='full')['info']
    if prism_budget:
        assert k==14
        rectangles={pair:[i for i,label in enumerate(labels) if tuple(a//2 for a in label)==pair]
                    for pair in combinations(range(k//2),2)}
        cost=sum(gamma[u][v] for corners in rectangles.values() for u,v in combinations(corners,2)
                 if set(labels[u])&set(labels[v]))
        model.add(cost<=51)
    info.update(scope=__doc__,covers_all_graphs=False,
                complete_global_cover_cases=8 if k==14 else 1,
                root_template_fixed=False,relative_line_position=record,
                small_line=line_info,root_prism_budget=51 if prism_budget else None,
                budget_at_selected_line=False,all_eight_required_for_global_exclusion=k==14,
                rectangle_neighbor_moments=moment_info,
                small_line_existence_dependency='c4_selected_root_closed.json' if k==14 and maximum_components==3 else None,
                all_eight_cover_every_Conway_graph=k==14 and maximum_components==3,
                additional_unproved_small_line_hypothesis=k==14 and maximum_components<3,
                global_conway_exclusion=False,portable_unsat_proof=False,
                affordable_global_solve_proved=False)
    return model,labels,gamma,info


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--case',type=int,choices=range(8),required=True)
    p.add_argument('--maximum-components',type=int,choices=(1,2,3),default=3)
    p.add_argument('--control-rook9',action='store_true')
    p.add_argument('--root-prism-budget51',action='store_true')
    p.add_argument('--rectangle-moments',choices=('diagonal','full'))
    p.add_argument('--probing-level',type=int,choices=range(4),default=0)
    p.add_argument('--build-only',action='store_true')
    p.add_argument('--seconds',type=float,default=30)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists()
    resources=limit_research_process(1);start=time.process_time()
    k=4 if a.control_rook9 else 14
    model,labels,gamma,info=build(a.case,a.maximum_components,k,a.root_prism_budget51,a.rectangle_moments)
    assert not model.validate(),model.validate()
    info.update(status='MODEL_BUILT',resources=resources,build_cpu_seconds=time.process_time()-start,
                variables=len(model.proto.variables),constraints=len(model.proto.constraints),
                cpu_seconds_budget=a.seconds)
    atomic_json_write(a.output,info)
    print(json.dumps({key:info[key] for key in ('status','parameters','variables','constraints','build_cpu_seconds')}),flush=True)
    if a.build_only:return
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    solver.parameters.cp_model_probing_level=a.probing_level;solver.parameters.symmetry_level=0
    solver.parameters.max_presolve_iterations=1;solver.parameters.linearization_level=0
    solver.parameters.max_time_in_seconds=max(600,100*a.seconds)
    start=time.process_time();done=threading.Event()
    def stop():
        while not done.wait(.05):
            if time.process_time()-start>=a.seconds:solver.stop_search()
    timer=threading.Thread(target=stop,daemon=True);timer.start()
    try:status=solver.solve(model)
    finally:done.set();timer.join()
    info.update(status=solver.status_name(status),cpu_seconds=time.process_time()-start,
                branches=solver.num_branches,conflicts=solver.num_conflicts)
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        info['adjacency']=reconstruct_and_check(k,labels,[[solver.value(x) for x in row] for row in gamma])
        info.update(exact_all_pair_check=True,status='CONTROL_GRAPH_FOUND' if k==4 else 'CONWAY_GRAPH_FOUND')
    atomic_json_write(a.output,info)
    print(json.dumps({key:info[key] for key in ('status','cpu_seconds','branches','conflicts')}),flush=True)


if __name__=='__main__':main()
