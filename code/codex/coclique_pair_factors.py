"""Universal coexistence of residual degree factors on the twelve L vertices.

M has m_ij edges: these are the forced residual vertices of type {i,j}.
For each old zero-charge vertex u, its new neighbours form a submultigraph
F_u of M with degree r_ui = 2 - a_ui - common_B(u,i). Saturated old pairs
must use disjoint edges of M. This necessary model leaves the border free.
"""
from pathlib import Path
from itertools import combinations
import argparse
import json
import time

from ortools.sat.python import cp_model
from coclique_two_exception_cycles import build, verify_witness


def factor_model(partition, root_h=1, packing=True, triangle_capacity=False, context=None, simple=False):
    ctx={} if context is None else context
    model,variables,fixed,colours,populations=build(partition,root_h=root_h,population=True,hcomplete=True,context=ctx)
    edge=ctx['edge']; n=ctx['n']; common=lambda i,j:ctx['common'][tuple(sorted((i,j)))]
    multiplicities={row:x for row,x,c in populations if len(row)==2}
    residual={}
    for u in range(18,n):
        for row,m in multiplicities.items():
            y=model.NewIntVar(0,1 if simple else 2,f'factor_{u}_{row[0]}_{row[1]}')
            model.Add(y<=m)
            model.Add(y==0).OnlyEnforceIf([edge(u,row[0]),edge(u,row[1])])
            residual[u,row]=y
        for i in range(4,16):
            model.Add(sum(residual[u,row] for row in multiplicities if i in row)==2-edge(u,i)-common(u,i))
        model.Add(sum(residual[u,row] for row in multiplicities)==14-ctx['degree'][u])
    saturated={}
    if packing:
        for u,v in combinations(range(18,n),2):
            sat=model.NewBoolVar(f'sat_{u}_{v}')
            model.Add(common(u,v)==2-edge(u,v)).OnlyEnforceIf(sat)
            model.Add(common(u,v)<=1-edge(u,v)).OnlyEnforceIf(sat.Not())
            saturated[u,v]=sat
            for row,m in multiplicities.items():
                model.Add(residual[u,row]+residual[v,row]<=m).OnlyEnforceIf(sat)
    if triangle_capacity:
        # Each residual copy must itself obtain exactly one partner in the
        # neighbourhood of each of its two L anchors. If the anchors are
        # adjacent, that partner is already the other anchor.
        for row,m in multiplicities.items():
            for i in row:
                terms=[]
                for u in range(18,n):
                    if isinstance(edge(u,i),int):
                        if edge(u,i):terms.append(residual[u,row])
                        continue
                    term=model.NewIntVar(0,2,f'partner_{u}_{row[0]}_{row[1]}_{i}')
                    model.Add(term==residual[u,row]).OnlyEnforceIf(edge(u,i))
                    model.Add(term==0).OnlyEnforceIf(edge(u,i).Not())
                    terms.append(term)
                model.Add(sum(terms)<=m).OnlyEnforceIf(edge(*row).Not())
                model.Add(sum(terms)==0).OnlyEnforceIf(edge(*row))
    return model,variables,fixed,colours,populations,residual


def verify(report):
    verify_witness(report)
    n=report['vertices'];adj=[set() for _ in range(n)]
    for i,j in report['edges']:adj[i].add(j);adj[j].add(i)
    m={tuple(x['vertices']):x['count'] for x in report['remaining_population'] if len(x['vertices'])==2}
    y={(x['vertex'],tuple(x['type'])):x['count'] for x in report['factors']}
    for u in range(18,n):
        assert sum(y.get((u,row),0) for row in m)==14-len(adj[u])
        for row,value in m.items():
            count=y.get((u,row),0)
            assert 0<=count<=value
            if report.get('simple_factors'):assert count<=1
            if set(row)<=adj[u]:assert count==0
        for i in range(4,16):
            assert sum(y.get((u,row),0) for row in m if i in row)==2-int(i in adj[u])-len(adj[u]&adj[i])
    if report['factor_packing']:
        for u,v in combinations(range(18,n),2):
            if len(adj[u]&adj[v])==2-int(v in adj[u]):
                assert all(y.get((u,row),0)+y.get((v,row),0)<=value for row,value in m.items())
    if report.get('triangle_capacity'):
        for row,value in m.items():
            for i in row:
                assert sum(y.get((u,row),0) for u in range(18,n) if u in adj[i])<=(1-int(row[1] in adj[row[0]]))*value
    return True


def run(partition,root_h,output,seconds=60,workers=2,packing=True,triangle_capacity=False,no_lp=False):
    output.parent.mkdir(parents=True,exist_ok=True)
    begun=time.monotonic()
    model,variables,fixed,colours,populations,factors=factor_model(partition,root_h,packing,triangle_capacity)
    built=time.monotonic()
    print(json.dumps(dict(stage='built',partition=partition,root_h=root_h,seconds=built-begun,model_stats=model.ModelStats())),flush=True)
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=workers
    solver.parameters.max_time_in_seconds=seconds;solver.parameters.log_search_progress=True
    solver.parameters.log_to_stdout=False
    if no_lp:solver.parameters.subsolvers.append('no_lp')
    with output.with_suffix('.log').open('w') as log:
        solver.log_callback=lambda line:(log.write(line+'\n'),log.flush())
        status=solver.Solve(model)
    report=dict(partition=partition,root_h=root_h,vertices=59+root_h,hcomplete=True,population=True,triangle=False,
                scope='All normalized (0,2) borders for this cycle partition and epsilon',
                relaxation='Simultaneous degree factors in the forced residual multigraph; not a full SRG',
                factor_packing=packing,triangle_capacity=triangle_capacity,no_lp=no_lp,
                status=solver.StatusName(status),build_seconds=built-begun,
                solver_seconds=solver.WallTime(),branches=solver.NumBranches(),conflicts=solver.NumConflicts(),
                workers=workers,limit_seconds=seconds,model_stats=model.ModelStats(),response_stats=solver.ResponseStats())
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        report['edges']=sorted(fixed|{e for e,v in variables.items() if solver.Value(v)})
        report['coclique']=[u for u,v in colours.items() if solver.Value(v)]
        report['remaining_population']=[dict(vertices=row,count=solver.Value(x),coclique_count=solver.Value(c))
                                       for row,x,c in populations if solver.Value(x)]
        report['factors']=[dict(vertex=u,type=row,count=solver.Value(y)) for (u,row),y in factors.items() if solver.Value(y)]
        report['verified']=verify(report)
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('edges','coclique','remaining_population','factors','model_stats','response_stats')}),flush=True)
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path)
    ap.add_argument('--partition',default='6');ap.add_argument('--root-h',type=int,choices=(0,1),default=1)
    ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--workers',type=int,default=2)
    ap.add_argument('--no-packing',action='store_true')
    ap.add_argument('--triangle-capacity',action='store_true');ap.add_argument('--no-lp',action='store_true')
    args=ap.parse_args();run(tuple(map(int,args.partition.split(','))),args.root_h,args.output,args.seconds,args.workers,not args.no_packing,args.triangle_capacity,args.no_lp)
