"""Extend the chosen star4 attachments to its twelve COMPLETE global rows.

Use the lambda1/mu2 design highlighted by LAB895: the60 vertices outside
L4 and L5 correspond bijectively to the60 nonmatching pairs in L4.
Their columns are these pairs. L5 is a perfect matching to L4. Together
with the matching inside L4 this gives all twelve rows on the84 labels.
The other72 rows remain incomplete; this is not a constructed graph84.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model

sys.path.insert(0,str(Path(__file__).resolve().parent))
from conway_attachment_probe import LABELS,OLD,NEW,STAR4

GLOBAL=[p for p in combinations(range(14),2) if p[1]!=(p[0]^1)]


def run(source,output,seconds=30,root_limit=14):
    started=time.monotonic()
    record=json.loads(Path(source).read_text(encoding='utf-8'))
    local=record['partial_adjacency']
    local_index={p:i for i,p in enumerate(LABELS)}
    index={p:i for i,p in enumerate(GLOBAL)}
    star=[GLOBAL[i] for i in range(len(GLOBAL)) if 4 in GLOBAL[i]]
    mate=[next(j for j,q in enumerate(star) if local[local_index[p]][local_index[q]]) for p in star]
    assert all(mate[mate[i]]==i and mate[i]!=i for i in range(12))
    pairs=[(a,b) for a,b in combinations(range(12),2) if mate[a]!=b]
    assert len(pairs)==60
    model=cp_model.CpModel()
    rows=[[0]*84 for _ in star]
    for i,p in enumerate(star):
        rows[i][index[star[mate[i]]]]=1
    choices={}
    domain_sizes=[]
    for z,label in enumerate(GLOBAL):
        if 4 in label:
            continue
        if 5 in label:
            allowed=[]
            for p in range(12):
                if label in local_index and any(local[local_index[star[x]]][local_index[label]]!=int(p==x)
                                                for x,q in enumerate(star) if q[0]==4):
                    continue
                allowed.append(p)
            population=[(i,) for i in range(12)]
            kind='mate_star5'
        else:
            allowed=[]
            for edge,pair in enumerate(pairs):
                if label in local_index and any(local[local_index[star[x]]][local_index[label]]!=int(x in pair)
                                                for x,q in enumerate(star) if q[0]==4):
                    continue
                allowed.append(edge)
            population=pairs
            kind='pair_outside4_5'
        if not allowed:
            result=dict(status='EMPTY_GLOBAL_COLUMN',complete=True,label=label,source_file=str(source))
            Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(result),flush=True)
            return result
        choice=model.NewIntVarFromDomain(cp_model.Domain.FromValues(allowed),'column_%d'%z)
        choices[z]=(choice,kind)
        domain_sizes.append(dict(label=label,count=len(allowed),kind=kind))
        variables=[]
        for p in range(12):
            values={int(p in population[e]) for e in allowed}
            variable=values.pop() if len(values)==1 else model.NewBoolVar('adj_%d_%d'%(p,z))
            rows[p][z]=variable
            variables.append(variable)
        model.AddAllowedAssignments([choice,*variables],[(e,*[int(p in population[e]) for p in range(12)]) for e in allowed])
    for kind in ('mate_star5','pair_outside4_5'):
        model.AddAllDifferent([v for v,k in choices.values() if k==kind])
    assumptions={}
    for i,p in enumerate(star):
        model.Add(sum(rows[i])==12)
        for r in range(root_limit):
            target=2-int(r in p)-int((r^1) in p)
            active=model.NewBoolVar('assume_%d_%d'%(i,r))
            model.Add(sum(rows[i][z] for z,q in enumerate(GLOBAL) if r in q)==target).OnlyEnforceIf(active)
            model.AddAssumption(active)
            assumptions[active.Index()]=dict(vertex=p,root=r,target=target)
    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=seconds
    status=solver.Solve(model)
    result=dict(source_file=str(source),status=solver.StatusName(status),complete=status in (cp_model.OPTIMAL,cp_model.INFEASIBLE),
                solver_seconds=solver.WallTime(),seconds=time.monotonic()-started,domains=domain_sizes,
                root_count_constraints=list(range(root_limit)),
                scope='Star4 rows on84 labels, exact C2 inside star4, root counts for the listed roots only. Other72 rows not completed.')
    if status==cp_model.INFEASIBLE:
        result['sufficient_root_core']=[assumptions[i] for i in solver.SufficientAssumptionsForInfeasibility()]
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        matrix=[[solver.Value(v) for v in row] for row in rows]
        for i,p in enumerate(star):
            assert sum(matrix[i])==12
            for r in range(root_limit):
                assert sum(matrix[i][z] for z,q in enumerate(GLOBAL) if r in q)==2-int(r in p)-int((r^1) in p)
            if p[0]==4:
                assert all(matrix[i][index[q]]==local[local_index[p]][local_index[q]] for q in LABELS)
        for i,j in combinations(range(12),2):
            assert sum(a*b for a,b in zip(matrix[i],matrix[j]))+int(mate[i]==j)==1
        result.update(labels=GLOBAL,star_labels=star,rows=matrix,exact_frame_check=True,
                      chosen_columns=[dict(label=GLOBAL[z],choice=solver.Value(v),kind=kind) for z,(v,kind) in choices.items()])
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','labels','star_labels','chosen_columns','domains')}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--seconds',type=float,default=30)
    parser.add_argument('--root-limit',type=int,default=14,help='Use fewer root equations only to locate an obstruction or exercise a relaxed positive control.')
    args=parser.parse_args()
    run(args.source,args.output,args.seconds,args.root_limit)
