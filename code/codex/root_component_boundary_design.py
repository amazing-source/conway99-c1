"""Necessary external triple design for one 18-vertex line component.

Every vertex outside L and N(L) has three neighbours in this component.
Writing C for its cubic adjacency and Z for equal colours, its external
incidence must satisfy D D^t=12I-C-C^2+2J-Z. Each of 60 columns is a
triple, uses at most two of each colour, and induces at most one C edge
(the outside vertex's neighbourhood is a matching). A feasible design
is only a necessary boundary completion, never a Conway graph.
"""

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time
import threading

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process,atomic_json_write
from ortools.sat.python import cp_model


def solve(record,code,seconds):
    p,m0,m1=code
    perm=record['cross_permutations'][p];n=len(perm)
    assert n==6
    graph=[[0]*18 for _ in range(18)]
    def edge(a,b):graph[a][b]=graph[b][a]=1
    for i in range(0,n,2):edge(i,i+1)
    for col,m in enumerate((m0,m1),1):
        for i,j in record['internal_matchings'][m]:edge(col*n+i,col*n+j)
    for i in range(n):
        edge(i,n+i);edge(i,2*n+i);edge(n+i,2*n+perm[i])
    targets={(u,v):2-int(u//n==v//n)-graph[u][v]-sum(graph[u][z]*graph[v][z] for z in range(18))
             for u,v in combinations(range(18),2)}
    assert min(targets.values())>=0
    triples=[t for t in combinations(range(18),3)
             if max(sum(v//n==c for v in t) for c in range(3))<=2
             and sum(graph[u][v] for u,v in combinations(t,2))<=1
             and all(targets[u,v]>0 for u,v in combinations(t,2))]
    model=cp_model.CpModel()
    counts=[model.new_int_var(0,min(targets[u,v] for u,v in combinations(t,2)),f't{i}') for i,t in enumerate(triples)]
    for (u,v),target in targets.items():
        model.add(sum(x for x,t in zip(counts,triples) if u in t and v in t)==target)
    model.add(sum(counts)==60)
    for u in range(18):model.add(sum(x for x,t in zip(counts,triples) if u in t)==10)
    model.add(sum(x for x,t in zip(counts,triples) if len({v//n for v in t})==3)==24)
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=max(600,100*seconds)
    started=time.process_time();done=threading.Event()
    def interrupt():
        while not done.wait(.05):
            if time.process_time()-started>=seconds:solver.stop_search();return
    timer=threading.Thread(target=interrupt,daemon=True);timer.start()
    try:status=solver.solve(model)
    finally:done.set();timer.join()
    result={'code':code,'status':solver.status_name(status),'cpu_seconds':time.process_time()-started,
            'allowed_triples':len(triples),'branches':solver.num_branches,'conflicts':solver.num_conflicts}
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        result['triples']=[list(t) for x,t in zip(counts,triples) for _ in range(solver.value(x))]
        assert len(result['triples'])==60
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tables',type=Path)
    parser.add_argument('--branches',type=Path,required=True)
    parser.add_argument('--seconds',type=float,default=5)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();resources=limit_research_process(4)
    record=next(r for r in json.loads(args.tables.read_text())['records'] if r['vertices']==18)
    case=json.loads(args.branches.read_text())['records'][0]['cases'][0]
    codes=case['component_codes']; results=[]
    for code in codes:
        result=solve(record,code,args.seconds);results.append(result)
        atomic_json_write(args.output,{'scope':__doc__,'resources':resources,'source':str(args.branches),'records':results})
        print(json.dumps({k:v for k,v in result.items() if k!='triples'}),flush=True)


if __name__=='__main__':main()
