"""Small fixed-border probes isolating aggregate capacities from real copies."""
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json

from ortools.sat.python import cp_model
from coclique_variable_border_cuts import border_data


def build(w,mode='copies',group=None):
    n,a,m,d,r,allowed,sat=border_data(w)
    users=list(range(18,n)) if group is None else sorted(group)
    model=cp_model.CpModel();gates={u:model.NewBoolVar(f'use_{u}') for u in users}
    y={(u,row):model.NewBoolVar(f'y{u}_{row}') for u in users for row in m if allowed[u,row]}
    for (u,row),var in y.items():model.Add(var<=gates[u])
    for u in users:
        model.Add(sum(v for (vtx,row),v in y.items() if vtx==u)==d[u]).OnlyEnforceIf(gates[u])
        for i in range(4,16):
            model.Add(sum(v for (vtx,row),v in y.items() if vtx==u and i in row)==r[u,i]).OnlyEnforceIf(gates[u])
    for row,mult in m.items():
        for i in row:model.Add(sum(y.get((u,row),0) for u in users if u in a[i])<=(1-int(row[1] in a[row[0]]))*mult)
    x={}
    if mode=='aggregate':
        for u,v in sat:
            if u not in gates or v not in gates:continue
            for row,mult in m.items():model.Add(y.get((u,row),0)+y.get((v,row),0)<=mult)
    else:
        for row,mult in m.items():
            for u in users:
                if (u,row) not in y:continue
                for c in range(mult):x[u,row,c]=model.NewBoolVar(f'x{u}_{row}_{c}')
                model.Add(sum(x[u,row,c] for c in range(mult))==y[u,row])
            for c in range(mult):
                model.Add(sum(x.get((u,row,c),0) for u in users)<=12)
                for i in row:model.Add(sum(x.get((u,row,c),0) for u in users if u in a[i])<=1-int(row[1] in a[row[0]]))
                for u,v in sat:
                    if u in gates and v in gates:model.Add(x.get((u,row,c),0)+x.get((v,row,c),0)<=1)
                if mode in ('partners','gram'):
                    for u in users:
                        model.Add(len(a[u]&set(row))+sum(x.get((v,row,c),0) for v in a[u] if v in gates)<=2-x.get((u,row,c),0))
        if mode=='gram':
            for u,v in combinations(users,2):
                terms=[]
                for row,mult in m.items():
                    for c in range(mult):
                        if (u,row,c) not in x or (v,row,c) not in x:continue
                        term=model.NewBoolVar(f'common{u}_{v}_{row}_{c}')
                        model.AddMultiplicationEquality(term,[x[u,row,c],x[v,row,c]]);terms.append(term)
                model.Add(sum(terms)==2-int(v in a[u])-len(a[u]&a[v])).OnlyEnforceIf([gates[u],gates[v]])
    model.AddAssumptions(list(gates.values()))
    return model,gates,y,x


def solve(w,mode,seconds=15,group=None,shrink=False):
    model,gates,y,x=build(w,mode,group);solver=cp_model.CpSolver()
    solver.parameters.max_time_in_seconds=seconds;solver.parameters.num_search_workers=1
    status=solver.Solve(model)
    result=dict(mode=mode,status=solver.StatusName(status),seconds=solver.WallTime(),vertices=list(gates),
                branches=solver.NumBranches(),conflicts=solver.NumConflicts(),limit_seconds=seconds)
    if status==cp_model.INFEASIBLE:
        by_index={v.Index():u for u,v in gates.items()}
        core=[by_index[i] for i in solver.SufficientAssumptionsForInfeasibility()]
        result['sufficient_core']=core
        if shrink:
            trials=[]
            for u in core[:]:
                candidate=[v for v in core if v!=u];trial=solve(w,mode,seconds,candidate)
                trials.append(dict(removed=u,status=trial['status'],seconds=trial['seconds']))
                if trial['status']=='INFEASIBLE':core=candidate
            result['reduced_core']=core;result['shrink_trials']=trials
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        result['factors']=[dict(vertex=u,type=row,count=1) for (u,row),v in y.items() if solver.Value(v)]
        result['incidences']=[dict(vertex=u,type=row,copy=c) for (u,row,c),v in x.items() if solver.Value(v)]
    return result


def run(source,output,seconds=15,shrink=False):
    w=json.loads(source.read_text());report=dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                               scope='One fixed border, nested necessary incidence relaxations',results=[])
    for mode in ('aggregate','copies','partners','gram'):
        entry=solve(w,mode,seconds,shrink=shrink);report['results'].append(entry)
        output.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in entry.items() if k not in ('factors','incidences','shrink_trials')}),flush=True)
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path)
    ap.add_argument('--seconds',type=float,default=15);ap.add_argument('--shrink',action='store_true')
    args=ap.parse_args();run(args.source,args.output,args.seconds,args.shrink)
