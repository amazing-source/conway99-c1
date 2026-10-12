"""Actual shared copies of residual pair types, on a variable (0,2) border.

Each type has at most two globally named copies. Incidences with all old
vertices use these same copies; pairwise aggregate capacities alone do not
enforce this. Optional Gram equalities complete every old pair's common
neighbours. This remains a necessary relaxation, not an SRG construction.
"""
from pathlib import Path
from itertools import combinations
from datetime import datetime, timezone
import argparse
import hashlib
import json
import time

from ortools.sat.python import cp_model
from coclique_variable_border_cuts import Master, evaluate
from coclique_pair_factors import verify as verify_factors


def install(master, gram=False, partners=False, closed_stars=False):
    assert master.factors and master.simple
    model=master.model; ctx=master.ctx; users=list(range(18,ctx['n']))
    x={}; active={}
    for row,m in master.m.items():
        for copy in range(2):
            active[row,copy]=master.predicate(('copy_present',*row,copy),m,copy+1)
            for u in users:
                var=model.NewBoolVar(f'copy_{row[0]}_{row[1]}_{copy}_u{u}')
                model.Add(var<=active[row,copy])
                model.Add(var<=master.allowed(u,row))
                x[u,row,copy]=var
        for u in users:
            model.Add(x[u,row,0]+x[u,row,1]==master.factors[u,row])
            # Independent interchange of the two unnamed copies is harmless.
            model.Add(x[u,row,1]<=sum(x[v,row,0] for v in users if v<u))
        for copy in range(2):
            model.Add(sum(x[u,row,copy] for u in users)<=12*active[row,copy])
            if closed_stars:
                for s in (0,1,2,3,16,17):
                    common=master.edge(s,row[0])+master.edge(s,row[1])
                    common+=sum(ctx['product'](master.edge(s,u),x[u,row,copy]) for u in users)
                    model.Add(common==2).OnlyEnforceIf(active[row,copy])
            for i in row:
                terms=[ctx['product'](x[u,row,copy],master.edge(u,i)) for u in users]
                model.Add(sum(terms)<=1-master.edge(*row))
            if partners:
                # Common neighbours of a missing copy and each old u,
                # counted inside B; neighbours induce a matching.
                for u in users:
                    common=master.edge(u,row[0])+master.edge(u,row[1])
                    common+=sum(ctx['product'](master.edge(u,v),x[v,row,copy]) for v in users if v!=u)
                    model.Add(common<=2-x[u,row,copy]).OnlyEnforceIf(active[row,copy])
    for u,v in combinations(users,2):
        if gram:
            terms=[ctx['product'](x[u,row,copy],x[v,row,copy]) for row in master.m for copy in range(2)]
            model.Add(sum(terms)==2-master.edge(u,v)-ctx['common'][u,v])
        else:
            sat=master.predicate(('sat',u,v),ctx['common'][u,v]+master.edge(u,v),2)
            for row in master.m:
                for copy in range(2):
                    model.Add(x[u,row,copy]+x[v,row,copy]<=1).OnlyEnforceIf(sat)
    return x,active


def verify(report):
    verify_factors(report)
    n=report['vertices'];a=[set() for _ in range(n)]
    for u,v in report['edges']:a[u].add(v);a[v].add(u)
    m={tuple(t['vertices']):t['count'] for t in report['remaining_population']}
    selected={(tuple(t['type']),t['copy']):set(t['users']) for t in report['copies']}
    y={(t['vertex'],tuple(t['type'])):t['count'] for t in report['factors']}
    assert len(selected)==sum(m.values())
    for row,mult in m.items():
        assert len(row)==2
        groups=[selected[row,c] for c in range(mult)]
        assert all(not(s&t) for s,t in combinations(groups,2))
        for u in range(18,n):assert sum(u in group for group in groups)==y.get((u,row),0)
        for group in groups:
            assert len(group)<=12
            assert all(sum(u in a[i] for u in group)<=1-int(row[1] in a[row[0]]) for i in row)
            if report['copy_partner_caps']:
                for u in range(18,n):assert len(a[u]&(set(row)|group))<=2-int(u in group)
            if report.get('copy_closed_stars'):
                for s in (0,1,2,3,16,17):assert len(a[s]&(set(row)|group))==2
    for u,v in combinations(range(18,n),2):
        missing=sum(u in group and v in group for group in selected.values())
        need=2-int(v in a[u])-len(a[u]&a[v])
        if need==0:assert missing==0
        if report['copy_gram_equalities']:assert missing==need
    return True


def run(folder,partition,root_h,resume,seconds=180,workers=2,gram=False,partners=False,no_lp=False,closed_stars=False):
    folder.mkdir(parents=True,exist_ok=True)
    config=dict(start_utc=datetime.now(timezone.utc).isoformat(),partition=partition,root_h=root_h,
                resume_cuts=str(resume),resume_sha256=hashlib.sha256(resume.read_bytes()).hexdigest(),
                seconds=seconds,workers=workers,gram=gram,partners=partners,no_lp=no_lp,closed_stars=closed_stars,
                code_sha256={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in
                             ('coclique_copy_sharing.py','coclique_variable_border_cuts.py','coclique_pair_factors.py','coclique_two_exception_cycles.py')})
    (folder/'config.json').write_text(json.dumps(config,indent=2)+'\n')
    begun=time.monotonic();master=Master(partition,root_h,factors=True,all_pairs=False,simple=True)
    for cut in json.loads(resume.read_text()):master.install(cut)
    x,active=install(master,gram,partners,closed_stars)
    print(json.dumps(dict(stage='built',seconds=time.monotonic()-begun,model_stats=master.model.ModelStats())),flush=True)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=seconds
    solver.parameters.num_search_workers=workers;solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
    if no_lp:solver.parameters.subsolvers.append('no_lp')
    with (folder/'search.log').open('w') as log:
        solver.log_callback=lambda line:(log.write(line+'\n'),log.flush())
        status=solver.Solve(master.model)
    report=dict(partition=partition,root_h=root_h,vertices=master.ctx['n'],hcomplete=True,population=True,triangle=False,
                scope='All normalized (0,2) cores and borders for this partition and epsilon',
                relaxation='Globally shared residual copies; edges between missing vertices are not modelled',
                status=solver.StatusName(status),seconds=solver.WallTime(),cuts=len(master.installed),
                branches=solver.NumBranches(),conflicts=solver.NumConflicts(),workers=workers,limit_seconds=seconds,
                factor_packing=True,triangle_capacity=True,simple_factors=True,actual_copy_sharing=True,
                copy_gram_equalities=gram,copy_partner_caps=partners,copy_closed_stars=closed_stars,
                model_stats=master.model.ModelStats(),response_stats=solver.ResponseStats())
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        report['edges']=sorted(master.fixed|{e for e,v in master.variables.items() if solver.Value(v)})
        report['coclique']=[u for u,v in master.colours.items() if solver.Value(v)]
        report['remaining_population']=[dict(vertices=row,count=solver.Value(v),coclique_count=solver.Value(c))
                                       for row,v,c in master.populations if solver.Value(v)]
        report['factors']=[dict(vertex=u,type=row,count=solver.Value(y)) for (u,row),y in master.factors.items() if solver.Value(y)]
        report['copies']=[dict(type=row,copy=c,users=[u for u in range(18,master.ctx['n']) if solver.Value(x[u,row,c])])
                          for (row,c),present in active.items() if solver.Value(present)]
        report['verified']=verify(report)
        assert all(not evaluate(report,c).get('violated',False) for c in master.installed)
    (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('edges','coclique','remaining_population','factors','copies','model_stats','response_stats')}),flush=True)
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--cuts',type=Path,required=True)
    ap.add_argument('--partition',default='6');ap.add_argument('--root-h',type=int,choices=(0,1),default=1)
    ap.add_argument('--seconds',type=float,default=180);ap.add_argument('--workers',type=int,default=2)
    ap.add_argument('--gram',action='store_true');ap.add_argument('--partners',action='store_true');ap.add_argument('--no-lp',action='store_true')
    ap.add_argument('--closed-stars',action='store_true')
    args=ap.parse_args();run(args.folder,tuple(map(int,args.partition.split(','))),args.root_h,args.cuts,args.seconds,args.workers,args.gram,args.partners,args.no_lp,args.closed_stars)
