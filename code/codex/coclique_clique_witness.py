"""Exact small-group witnesses at a fixed border: integral pair compatibility.

This tests residual L-degree factors and the stated eligibility/packing
conditions only. It never claims that a pair extends to an SRG.
"""
from pathlib import Path
from itertools import combinations
import argparse
import json

from ortools.sat.python import cp_model
from coclique_variable_border_cuts import border_data, evaluate


def run(source,cut_path,output,simple=False):
    w=json.loads(source.read_text());cut=json.loads(cut_path.read_text())
    n,adj,m,d,r,allowed,sat=border_data(w);group=cut['group']
    copies=[row for row,value in m.items() for _ in range(value)]
    result=dict(source=str(source),cut_source=str(cut_path),group=group,
                scope='Integral residual degree factors with elementary eligibility and mutual saturated-pair packing',
                simple_factors=simple,
                group_certificate=evaluate(w,cut),proper_subgroups=[])
    assert result['group_certificate']['violated']
    for subgroup in [g for size in range(1,len(group)) for g in combinations(group,size)]:
        model=cp_model.CpModel()
        x={(u,k):model.NewBoolVar(f'x{u}_{k}') for u in subgroup for k,row in enumerate(copies) if allowed[u,row]}
        for u in subgroup:
            model.Add(sum(v for (a,k),v in x.items() if a==u)==d[u])
            for i in range(4,16):
                model.Add(sum(v for (a,k),v in x.items() if a==u and i in copies[k])==r[u,i])
        for k in range(len(copies)):model.Add(sum(x.get((u,k),0) for u in subgroup)<=1)
        if simple:
            for u in subgroup:
                for row in m:model.Add(sum(x.get((u,k),0) for k,t in enumerate(copies) if t==row)<=1)
        solver=cp_model.CpSolver();solver.parameters.num_search_workers=1;solver.parameters.max_time_in_seconds=10
        status=solver.Solve(model)
        entry=dict(group=subgroup,status=solver.StatusName(status),seconds=solver.WallTime())
        if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
            chosen={u:[k for k in range(len(copies)) if (u,k) in x and solver.Value(x[u,k])] for u in subgroup}
            for u in subgroup:
                assert len(chosen[u])==d[u]
                assert all(allowed[u,copies[k]] for k in chosen[u])
                if simple:assert len({copies[k] for k in chosen[u]})==len(chosen[u])
                assert all(sum(i in copies[k] for k in chosen[u])==r[u,i] for i in range(4,16))
            assert all(not(set(chosen[u])&set(chosen[v])) for u,v in combinations(subgroup,2))
            entry.update(chosen=[dict(vertex=u,copies=ks,types=[copies[k] for k in ks]) for u,ks in chosen.items()],verified=True)
        result['proper_subgroups'].append(entry)
    result['copies']=copies
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('copies','proper_subgroups')}))
    print(json.dumps([dict(group=x['group'],status=x['status'],seconds=x['seconds']) for x in result['proper_subgroups']]))
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('cut',type=Path);ap.add_argument('output',type=Path)
    ap.add_argument('--simple',action='store_true')
    args=ap.parse_args();run(args.source,args.cut,args.output,args.simple)
