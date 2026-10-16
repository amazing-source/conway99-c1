"""Construct a root-count relaxation, ONLY to initialize the global search.

The seed search uses cyclic root relabelling to reduce its integer model.
That symmetry is NEVER imposed on the global completion search. The seed
is a full matrix with correct root counts, not a Conway graph unless the
separate exact all-pair check succeeds. All edges remain free afterwards.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time

import numpy as np
from ortools.sat.python import cp_model

sys.path.insert(0,str(Path(__file__).resolve().parent))
from conway_global_lazy import problem,root_check,separate
from conway_global_cover import matching_type


def normalize(labels,graph,candidate,cover):
    index={p:i for i,p in enumerate(labels)}
    def edge(p,q):
        return int(candidate[index[tuple(sorted(p))],index[tuple(sorted(q))]])
    marked=next(a for a in range(2,14,2) if
                edge((0,a),(0,a^1))+edge((1,a),(1,a^1))+
                edge((0,a),(1,a))+edge((0,a^1),(1,a^1))<4)
    matching={}
    for a in range(2,14):
        partners=[b for b in range(2,14) if a!=b and edge((0,a),(0,b))]
        assert len(partners)==1
        matching[a]=partners[0]
    def component(first):
        order=[]
        vertex=first
        while vertex not in order:
            order.extend([vertex,vertex^1])
            vertex=matching[vertex^1]
        assert vertex==first
        return order
    distinguished=component(marked)
    unseen=set(range(2,14))-set(distinguished)
    rest=[]
    while unseen:
        order=component(min(unseen))
        rest.append(order)
        unseen-=set(order)
    rest.sort(key=lambda component:(len(component),component))
    old_roots=[0,1]+distinguished+[v for component in rest for v in component]
    old_indices=[index[tuple(sorted(old_roots[r] for r in p))] for p in labels]
    normalized=candidate[np.ix_(old_indices,old_indices)]
    star_matching=[(a-2,b-2) for a,b in combinations(range(2,14),2)
                   if normalized[index[0,a],index[0,b]]]
    kind=matching_type(star_matching,12,True)
    case=next(i for i,entry in enumerate(cover['cases'])
              if (tuple(entry['partition']),entry['marked_component'])==kind)
    assert sorted(star_matching)==[tuple(p) for p in cover['cases'][case]['canonical_matching']]
    return normalized,case,old_roots


def run(output,seconds=10):
    started=time.monotonic()
    labels,edge_vars,edges,cards,clauses,selectors,cover=problem(14,True)
    index={p:i for i,p in enumerate(labels)}
    # Acting by seven rotations of physical pairs and simultaneous bit flip.
    permutations=[]
    for shift in range(7):
        for flip in range(2):
            root_image=[2*((r//2+shift)%7)+((r%2)^flip) for r in range(14)]
            permutations.append([index[tuple(sorted(root_image[r] for r in p))] for p in labels])
    remaining=set(edges)
    orbits=[]
    while remaining:
        p,q=min(remaining)
        orbit=sorted({tuple(sorted((perm[p],perm[q]))) for perm in permutations})
        orbits.append(orbit)
        remaining.difference_update(orbit)
    model=cp_model.CpModel()
    variables=[model.NewBoolVar('orbit_%d'%i) for i in range(len(orbits))]
    gamma=[[0]*84 for _ in range(84)]
    for variable,orbit in zip(variables,orbits):
        for p,q in orbit:
            gamma[p][q]=gamma[q][p]=variable
    for p,label in enumerate(labels):
        for r in range(14):
            model.Add(sum(gamma[p][q] for q,other in enumerate(labels) if r in other)
                      ==2-int(r in label)-int((r^1) in label))
    model.Add(sum(gamma[index[0,y]][index[1,y]] for y in range(2,14))<=7)
    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=seconds
    status=solver.Solve(model)
    result=dict(status=solver.StatusName(status),scope='ROOT_COUNT_RELAXATION_ONLY_NOT_AN_SRG',
                orbit_variables=len(orbits),solver_seconds=solver.WallTime(),
                global_symmetry_restriction=False,all_edges_released_after_seeding=True,
                branches=solver.NumBranches(),conflicts=solver.NumConflicts())
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        candidate=np.array([[solver.Value(v) for v in row] for row in gamma],dtype=np.int64)
        root_check(14,labels,candidate)
        candidate,case,old_roots=normalize(labels,edge_vars,candidate,cover)
        root_check(14,labels,candidate)
        cuts,statistics=separate(labels,edge_vars,candidate)
        result.update(candidate=candidate.tolist(),matching_case=case,new_roots_to_old=old_roots,
                      exact_root_check=True,pair_statistics=statistics,
                      universal_cuts=list(cuts.values()))
    result['total_seconds']=time.monotonic()-started
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('candidate','universal_cuts')},ensure_ascii=False),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    parser.add_argument('--seconds',type=float,default=10)
    args=parser.parse_args()
    run(args.output,args.seconds)
