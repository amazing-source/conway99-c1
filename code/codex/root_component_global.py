"""Lift a component template to the exact unseeded Conway model.

Gamma on all 84 labels and its rectangle Gram are variable. Only logically
forced edges from the template are substituted. The independent matching
normalization is disabled: it need not preserve this component template.
"""

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conway_global_cover import build_global, reconstruct_and_check
from root_component_propagation import LABELS, PAIRS, RECTANGLES, constraints, propagate


def build(template, gram_record,rank7_bound=None,gram_cover=None,normalize_grid_matchings=False):
    propagation = propagate(template)
    if propagation["status"] == "PROPAGATION_CONTRADICTION":
        return None, None, {"status":propagation["status"],"propagation":propagation}
    fixed = {PAIRS[i]:v for i,v,_ in propagation["assignments"]}
    model,labels,graph,selectors,info = build_global(normalize_star=False,initial_edges=fixed)
    assert tuple(labels)==LABELS and not selectors
    equations,bounds,_ = constraints(template)
    for items,target,_ in equations:
        model.add(sum(graph[PAIRS[i][0]][PAIRS[i][1]] for i in items)==target)
    for items,upper,_ in bounds:
        model.add(sum(graph[PAIRS[i][0]][PAIRS[i][1]] for i in items)<=upper)
    root_prism_budget=gram_record.get("root_prism_budget")
    if root_prism_budget is not None:
        model.add(sum(graph[a][b] for corners in RECTANGLES.values() for a,b in combinations(corners,2)
                      if set(LABELS[a])&set(LABELS[b]))<=root_prism_budget)
    edges = [tuple(e) for e in template["nongrid_edges"]]
    m=len(edges)
    r=[[None]*m for _ in range(m)]
    for i,e in enumerate(edges):
        corners=RECTANGLES[e]
        r[i][i]=model.new_int_var_from_domain(cp_model.Domain.from_values([2,4,6,8]),f"R_{i}_{i}")
        model.add(r[i][i]==8-2*sum(graph[a][b] for a,b in combinations(corners,2)))
        for j in range(i):
            f=edges[j]
            common=bool(set(e)&set(f))
            r[i][j]=r[j][i]=model.new_int_var(-8,0 if common else 4,f"R_{j}_{i}")
            model.add(r[i][j]==(0 if common else 4)-sum(graph[a][b] for a in corners for b in RECTANGLES[f]))
    model.add(sum(r[i][i] for i in range(m))<=28*template["kernel_dimension"])
    gram_info=None
    if gram_cover is not None:
        assert root_prism_budget==51
        from root_component_gram_table import add_gram_table
        gram_info=add_gram_table(model,graph,template,gram_cover,matrix=r)
    normalizations=[]
    if normalize_grid_matchings:
        nongrid=set(edges)
        grids=[e for e in RECTANGLES if e not in nongrid]
        used=set()
        while True:
            choices=[(e,f) for e in grids for f in grids if not set(e)&set(f) and not set(f)&used]
            if not choices:break
            e,f=min(choices)
            model.add(graph[RECTANGLES[e][0]][RECTANGLES[f][0]]==1)
            normalizations.append([e,f])
            used.update(e)
            used.update(f)
    for cut in gram_record["cuts"]:
        if cut["kind"]=="no_corner_realization":
            anchors=gram_record["anchors"]
            variables=[r[i][j] for i in anchors for j in anchors if i<=j]
            model.add_forbidden_assignments(variables,[cut["anchor_values"]])
        else:
            v=cut["vector"]
            expression=sum(v[i]*v[j]*r[i][j] for i in range(m) for j in range(m) if v[i] and v[j])
            model.add(expression>=0 if cut["kind"]=="R_psd" else expression<=cut["rhs"])
    rank7=None
    if rank7_bound is not None:
        assert rank7_bound==28, "Only the accepted necessary bound28 is enabled here."
        from modular_rank_factor import add_four_star_rank7
        rank7=add_four_star_rank7(model,labels,graph,edges[0],rank7_bound)
    info.update(status="MODEL_BUILT",covers_all_graphs=False,
                coverage_scope="One component template in the exhaustive minimum-c=4 cover.",
                fixed_local_seed=False,fixed_gram_witness=False,
                independent_matching_normalization=False,
                template_forced_edges=len(fixed),root_component_equations=len(equations),
                quotient_psd_or_realization_cuts=len(gram_record["cuts"]),
                root_prism_budget=root_prism_budget,
                modular_rank_constraint=rank7,
                complete_gram_cover=gram_info,
                grid_matching_mate_normalization=normalizations,
                affordable_global_solve_proved=False)
    return model,graph,info


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("templates",type=Path)
    parser.add_argument("grams",type=Path)
    parser.add_argument("--template-index",type=int,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--seconds",type=float,default=30)
    parser.add_argument("--build-only",action="store_true")
    parser.add_argument("--export-model",type=Path)
    parser.add_argument("--rank7-bound",type=int,choices=[28])
    parser.add_argument("--gram-cover",type=Path)
    parser.add_argument("--workers",type=int,default=1)
    parser.add_argument("--normalize-grid-matchings",action="store_true")
    parser.add_argument("--symmetry-level",type=int,choices=range(4),default=0)
    parser.add_argument("--search-log",action="store_true")
    args=parser.parse_args()
    templates=json.loads(args.templates.read_text(encoding="utf-8"))["survivors"]
    grams=json.loads(args.grams.read_text(encoding="utf-8"))["records"]
    item=next(r for r in grams if r["template_index"]==args.template_index)
    template=templates[args.template_index]
    assert item["status"]=="QUOTIENT_FEASIBLE" and min(template["component_count_by_root_line"])==4
    started=time.monotonic()
    gram_cover=None
    if args.gram_cover:
        gram_cover=next(r for r in json.loads(args.gram_cover.read_text(encoding="utf-8"))["records"]
                        if r["template_index"]==args.template_index)
    model,graph,info=build(template,item,args.rank7_bound,gram_cover,args.normalize_grid_matchings)
    info.update(template_index=args.template_index,component_count_by_root_line=template["component_count_by_root_line"],
                build_seconds=time.monotonic()-started)
    if model:
        assert not model.validate(),model.validate()
        info.update(model_variables=len(model.proto.variables),model_constraints=len(model.proto.constraints))
        if args.export_model:
            assert model.export_to_file(str(args.export_model))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(info,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in info.items() if k not in ('coverage','cuts')}),flush=True)
    if model and not args.build_only:
        solver=cp_model.CpSolver()
        solver.parameters.num_search_workers=args.workers
        solver.parameters.max_time_in_seconds=args.seconds
        solver.parameters.cp_model_probing_level=0
        solver.parameters.symmetry_level=args.symmetry_level
        solver.parameters.linearization_level=0
        solver.parameters.log_search_progress=args.search_log
        status=solver.solve(model)
        info.update(status=solver.status_name(status),solver_seconds=solver.wall_time,
                    branches=solver.num_branches,conflicts=solver.num_conflicts,
                    search_workers=args.workers,
                    total_seconds=time.monotonic()-started)
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            gamma=[[solver.value(x) for x in row] for row in graph]
            info["adjacency"]=reconstruct_and_check(14,LABELS,gamma)
            info["exact_all_pair_check"]=True
        elif status==cp_model.INFEASIBLE:
            info["certificate_scope"]="Solver verdict for this component template; not all Conway cases and not a portable UNSAT proof."
        args.output.write_text(json.dumps(info,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({k:v for k,v in info.items() if k not in ('coverage','cuts','adjacency')}),flush=True)


if __name__=="__main__":
    main()
