"""Eliminate the nongrid/nongrid block and solve the whole grid boundary.

All pairs of vertices belonging to grid rectangles have exact C2, and
their complete rows are variables. Other C1/component equations are
projected to necessary bounds by forgetting unrepresented edge variables.
No Gram is selected and no root prism budget is needed for this relaxation.
"""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_propagation import LABELS, PAIRS, RECTANGLES, constraints, propagate


def build(template, normalize=False):
    nongrid = {tuple(e) for e in template["nongrid_edges"]}
    grid_vertices = sorted(w for e,corners in RECTANGLES.items() if e not in nongrid for w in corners)
    ys = set(grid_vertices)
    prop = propagate(template)
    assert not prop["conflict"],prop["conflict"]
    fixed = {i:v for i,v,_ in prop["assignments"]}
    model = cp_model.CpModel()
    variables = [fixed[i] if i in fixed else (model.new_bool_var(f"e{i}") if u in ys or v in ys else None)
                 for i,(u,v) in enumerate(PAIRS)]
    graph = [[0]*84 for _ in range(84)]
    for (u,v),value in zip(PAIRS,variables):
        graph[u][v]=graph[v][u]=value
    equations,upper_bounds,_=constraints(template)
    exact,relaxed=0,0
    for ids,target,_ in equations:
        present = [variables[i] for i in ids if variables[i] is not None]
        missing = len(ids)-len(present)
        if missing:
            model.add(sum(present)<=target)
            model.add(sum(present)>=target-missing)
            relaxed += 1
        else:
            model.add(sum(present)==target)
            exact += 1
    for ids,upper,_ in upper_bounds:
        model.add(sum(variables[i] for i in ids if variables[i] is not None)<=upper)
    products={}
    def product(a,b):
        assert a is not None and b is not None
        if isinstance(a,int):return b if a else 0
        if isinstance(b,int):return a if b else 0
        key=tuple(sorted((a.index,b.index)))
        if key not in products:
            p=model.new_bool_var(f"p{len(products)}")
            model.add(p<=a)
            model.add(p<=b)
            model.add(p>=a+b-1)
            products[key]=p
        return products[key]
    for u,v in combinations(grid_vertices,2):
        model.add(graph[u][v]+sum(product(graph[u][z],graph[v][z]) for z in range(84))
                  ==2-len(set(LABELS[u])&set(LABELS[v])))
    normalizations=[]
    if normalize:
        used=set()
        grid_rectangles=[e for e in RECTANGLES if e not in nongrid]
        while True:
            choices=[(e,f) for e in grid_rectangles for f in grid_rectangles
                     if not set(e)&set(f) and not set(f)&used]
            if not choices:break
            e,f=min(choices)
            model.add(graph[RECTANGLES[e][0]][RECTANGLES[f][0]]==1)
            normalizations.append([e,f])
            used.update(e)
            used.update(f)
    return model,graph,{"grid_vertices":grid_vertices,"exact_linear_rows":exact,"relaxed_linear_rows":relaxed,
                       "C2_equations":len(grid_vertices)*(len(grid_vertices)-1)//2,
                       "product_variables":len(products),"forgotten_edge_variables":sum(x is None for x in variables),
                       "grid_matching_mate_normalization":normalizations}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    parser.add_argument("--indices",type=int,nargs="+",required=True)
    parser.add_argument("--seconds",type=float,default=300)
    parser.add_argument("--workers",type=int,default=4)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    templates=json.loads((args.directory/"root_component_templates.json").read_text())["survivors"]
    records=[]
    for index in args.indices:
        started=time.monotonic()
        model,graph,info=build(templates[index])
        assert not model.validate(),model.validate()
        info.update(template_index=index,build_seconds=time.monotonic()-started,status="MODEL_BUILT",
                    variables=len(model.proto.variables),constraints=len(model.proto.constraints))
        print(json.dumps(info),flush=True)
        solver=cp_model.CpSolver()
        solver.parameters.num_search_workers=args.workers
        solver.parameters.max_time_in_seconds=args.seconds
        solver.parameters.cp_model_probing_level=0
        solver.parameters.symmetry_level=0
        solver.parameters.linearization_level=0
        status=solver.solve(model)
        info.update(status=solver.status_name(status),solver_seconds=solver.wall_time,
                    branches=solver.num_branches,conflicts=solver.num_conflicts)
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            gamma=[[None if x is None else solver.value(x) for x in row] for row in graph]
            for u,v in combinations(info["grid_vertices"],2):
                assert gamma[u][v]+sum(gamma[u][z]*gamma[v][z] for z in range(84))==2-len(set(LABELS[u])&set(LABELS[v]))
            info["boundary_edges"]=[[u,v] for u,v in PAIRS if gamma[u][v]==1]
        records.append(info)
        args.output.write_text(json.dumps({"scope":__doc__,"root_prism_budget":None,"records":records},separators=(",",":"))+"\n",encoding="utf-8")
        print(json.dumps({k:v for k,v in info.items() if k!="boundary_edges"}),flush=True)


if __name__=="__main__":main()
