"""Connectivity controls for the at-most-three-component forest constraint."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ortools.sat.python import cp_model
from root_component_resources import atomic_json_write,limit_research_process
from root_component_small_line import add_small_line


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists();resources=limit_research_process(1)
    results=[]
    # Components of several shapes, including an isolated vertex. These
    # are encoding controls, not purported SRGs. A point outside N(L)
    # touches every component and must not serve as a forbidden bridge.
    for sizes in [(6,),(3,3),(2,2,2),(2,2,1,1)]:
        graph=[[0]*10 for _ in range(10)]
        def edge(u,v):graph[u][v]=graph[v][u]=1
        for u,v in combinations(range(3),2):edge(u,v)
        for w in range(3,9):edge(0,w);edge(9,w)
        start=3
        for size in sizes:
            for w in range(start,start+size-1):edge(w,w+1)
            start+=size
        for bound in (1,2,3):
            model=cp_model.CpModel();add_small_line(model,graph,[0,1,2],bound)
            solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
            solver.parameters.max_time_in_seconds=10
            status=solver.solve(model)
            expected=cp_model.OPTIMAL if len(sizes)<=bound else cp_model.INFEASIBLE
            assert status==expected,(sizes,bound,solver.status_name(status))
            results.append({'component_sizes':sizes,'maximum_components':bound,'status':solver.status_name(status)})
    atomic_json_write(a.output,{'status':'PASSED','resources':resources,'controls':results,'count':len(results)})
    print(json.dumps({'status':'PASSED','count':len(results)}))


if __name__=='__main__':main()
