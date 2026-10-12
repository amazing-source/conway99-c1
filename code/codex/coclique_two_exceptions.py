"""The normalized 4-cycle reduction for the (n1,n5)=(0,2) defect profile.

H: four charge-2 vertices in a cycle.
X: one charge-1 vertex on each cycle edge.
Y: two charge-1 vertices attached to each H vertex.
E: two isolated-from-positive charge-minus-1 vertices forming an edge.
Only X/Y edges remain variable, with degrees 1 on X and 3 on Y.
"""
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json
import sys
import time

from ortools.sat.python import cp_model
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'c1-audit-deps'))
import igraph as ig

BASE=Path(__file__).resolve().parents[2]


def enumerate_cores(seconds=60):
    model=cp_model.CpModel()
    fixed=set()
    def add(i,j):fixed.add(tuple(sorted((i,j))))
    for i in range(4):
        add(i,(i+1)%4)
        add(4+i,i);add(4+i,(i+1)%4)
        add(i,8+2*i);add(i,9+2*i)
    add(16,17)
    variables={p:model.NewBoolVar(f'e{p[0]}_{p[1]}') for p in combinations(range(4,16),2)}
    def edge(i,j):
        pair=tuple(sorted((i,j)))
        return variables.get(pair,int(pair in fixed))
    for i in range(4,16):
        model.Add(sum(edge(i,j) for j in range(4,16) if i!=j) == (1 if i<8 else 3))
    for i,j in combinations(range(18),2):
        common=[]
        for k in range(18):
            if k in (i,j):continue
            a,b=edge(i,k),edge(j,k)
            if isinstance(a,int):
                if a:common.append(b)
            elif isinstance(b,int):
                if b:common.append(a)
            else:
                z=model.NewBoolVar(f'and{i}_{j}_{k}')
                model.Add(z<=a);model.Add(z<=b);model.Add(z>=a+b-1);common.append(z)
        model.Add(sum(common)<=2-edge(i,j))
    q=[2]*4+[1]*12+[-1]*2
    folder=BASE/'data/codex_coclique_defects/two_exceptions'
    folder.mkdir(exist_ok=True)
    classes={};started=time.monotonic()
    class Callback(cp_model.CpSolverSolutionCallback):
        def __init__(self):super().__init__();self.count=0
        def on_solution_callback(self):
            self.count+=1
            edges=sorted(fixed|{e for e,v in variables.items() if self.Value(v)})
            g=ig.Graph(18,edges);g.vs['charge']=q
            cg=g.permute_vertices(g.canonical_permutation(color=[x+1 for x in q]))
            canonical=dict(charges=cg.vs['charge'],edges=sorted(tuple(sorted(e)) for e in cg.get_edgelist()))
            key=hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest()
            if key not in classes:
                classes[key]=dict(charges=q,edges=edges,boundary_degrees=[4-v for v in q],
                                  parameters=dict(degree=14,r=3,shift=2),
                                  profile=dict(b1=0,b2=4,b3=12,b4=60,b5=2),
                                  scope='Normalized necessary core; not an SRG',key=key)
                (folder/f'core_{key[:12]}.json').write_text(json.dumps(classes[key],indent=2)+'\n')
                print(json.dumps(dict(seconds=round(time.monotonic()-started,3),labelled=self.count,classes=len(classes))),flush=True)
    callback=Callback()
    solver=cp_model.CpSolver()
    solver.parameters.max_time_in_seconds=seconds
    solver.parameters.num_search_workers=1
    solver.parameters.enumerate_all_solutions=True
    status=solver.Solve(model,callback)
    result=dict(status=solver.StatusName(status),complete=status==cp_model.OPTIMAL,
                seconds=time.monotonic()-started,limit_seconds=seconds,
                labelled_count=callback.count,classes=len(classes),keys=sorted(classes),
                response_stats=solver.ResponseStats(),model_stats=model.ModelStats())
    (folder/'enumeration.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--seconds',type=float,default=60)
    args=parser.parse_args();enumerate_cores(args.seconds)
