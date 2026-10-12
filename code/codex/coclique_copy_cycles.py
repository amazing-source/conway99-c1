"""Lazy separation of actual-copy sharing on changing borders and factors.

One copy requires an independent requester set in the saturated-pair
graph. Two disjoint copies require a bipartite requester set. Every odd
cycle Q therefore gives sum_{u in Q} y_{u,T} <= floor(|Q|/2)*m_T.
These cuts exclude factor choices, not necessarily their whole border.
"""
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json

from coclique_forced_types import odd_cycle


def evaluate(w,cut):
    from coclique_variable_border_cuts import border_data
    n,a,m,d,r,allowed,sat=border_data(w)
    cycle=cut['cycle'];row=tuple(cut['type'])
    edges=[tuple(sorted(e)) for e in zip(cycle,cycle[1:]+cycle[:1])]
    if not all(e in sat for e in edges):return dict(applies=False)
    y={(item['vertex'],tuple(item['type'])):item['count'] for item in w['factors']}
    left=sum(y.get((u,row),0) for u in cycle);upper=(len(cycle)//2)*m.get(row,0)
    return dict(applies=True,left=left,upper=upper,multiplicity=m.get(row,0),violated=left>upper)


def install(master,cut):
    if not master.factors:raise ValueError('Copy-cycle cuts require explicit residual factors')
    cycle=cut['cycle'];row=tuple(cut['type'])
    assert len(cycle)==len(set(cycle)) and (len(cycle)==2 or len(cycle)%2==1)
    if any(u>=master.ctx['n'] for u in cycle):return False
    guards=[]
    for u,v in zip(cycle,cycle[1:]+cycle[:1]):
        u,v=sorted((u,v))
        guards.append(master.predicate(('sat',u,v),master.ctx['common'][u,v]+master.edge(u,v),2))
    master.model.Add(sum(master.factors[u,row] for u in cycle)<=(len(cycle)//2)*master.m[row]).OnlyEnforceIf(guards)
    master.installed.append(cut);return True


def discover(w,chordless=True):
    from coclique_variable_border_cuts import border_data
    n,a,m,d,r,allowed,sat=border_data(w);cuts=[]
    y={(item['vertex'],tuple(item['type'])):item['count'] for item in w['factors']}
    for row,mult in m.items():
        users=[u for u in range(18,n) if y.get((u,row),0)]
        cycles=[]
        if mult==1:
            pair=next((list(e) for e in sorted(sat) if all(u in users for u in e)),None)
            if pair:cycles.append(pair)
        elif mult==2:
            cycle=odd_cycle(users,sat)
            if cycle:cycles.append(cycle)
            if chordless and cycle:
                for sub in combinations(users,5):
                    edges={e for e in combinations(sub,2) if e in sat}
                    if len(edges)!=5 or any(sum(u in e for e in edges)!=2 for u in sub):continue
                    cycle=odd_cycle(sub,edges)
                    if cycle and len(cycle)==5:cycles.append(cycle);break
        for cycle in cycles:
            cut=dict(kind='copy_cycle_capacity',type=list(row),cycle=cycle,
                     law='Each actual copy serves an independent set of saturated requesters')
            cut['separation']=evaluate(w,cut);assert cut['separation']['violated'];cuts.append(cut)
    return cuts


def run(folder,resume,seeds,rounds=3,seconds=90,workers=2,partition=(6,),root_h=1,closed_balances=False):
    from coclique_variable_border_cuts import Master
    from coclique_residual_squares import discover as squares
    from coclique_copy_stars import discover as stars
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'config.json').write_text(json.dumps(dict(resume=str(resume),seeds=list(map(str,seeds)),rounds=rounds,
        seconds=seconds,workers=workers,partition=partition,root_h=root_h,closed_balances=closed_balances,
        code_sha256={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in
                     ('coclique_copy_cycles.py','coclique_copy_stars.py','coclique_variable_border_cuts.py','coclique_pair_factors.py','coclique_residual_squares.py','coclique_two_exception_cycles.py','coclique_closed_star_balance.py')}),indent=2)+'\n')
    master=Master(partition,root_h,factors=True,simple=True)
    if closed_balances:
        from coclique_closed_star_balance import install as install_balances
        install_balances(master)
    for cut in json.loads(resume.read_text()):master.install(cut)
    for source in seeds:
        w=json.loads(source.read_text())
        for cut in discover(w)+stars(w):
            cut['source']=str(source);master.install(cut)
    (folder/'cuts.json').write_text(json.dumps(master.installed,indent=2)+'\n')
    for iteration in range(rounds):
        source=folder/f'border_{iteration:03d}.json';w=master.solve(source,seconds,workers,no_lp=True)
        if w['status'] not in ('FEASIBLE','OPTIMAL'):break
        fresh=discover(w)+stars(w)+squares(w)
        for cut in fresh:cut['source']=str(source);master.install(cut)
        (folder/'cuts.json').write_text(json.dumps(master.installed,indent=2)+'\n')
        print(json.dumps(dict(stage='learned',iteration=iteration,cycles=sum(c['kind']=='copy_cycle_capacity' for c in fresh),
                             closed_stars=sum(c['kind']=='copy_closed_star_capacity' for c in fresh),
                             squares=sum(c['kind']=='integer_residual_square' for c in fresh),
                             total=len(master.installed),saturation_sharing_passed=not any(c['kind']=='copy_cycle_capacity' for c in fresh))),flush=True)
        if not fresh:break


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--cuts',type=Path,required=True)
    ap.add_argument('--seed',type=Path,action='append',default=[]);ap.add_argument('--rounds',type=int,default=3)
    ap.add_argument('--seconds',type=float,default=90);ap.add_argument('--workers',type=int,default=2)
    ap.add_argument('--closed-balances',action='store_true')
    args=ap.parse_args();run(args.folder,args.cuts,args.seed,args.rounds,args.seconds,args.workers,closed_balances=args.closed_balances)
