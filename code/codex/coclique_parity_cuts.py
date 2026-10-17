"""Exact redundant parity cuts discovered at fractional reciprocal solutions.

The float LP is an oracle. Every cut stores an XOR of original integer
equations and a forbidden parity assignment, both checked with integers.
"""
from pathlib import Path
import argparse
import json
import random
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from coclique_completion_certificate import equations


def bits(mask):
    while mask:
        bit=mask & -mask; mask-=bit
        yield bit.bit_length()-1


def discover(eq, values, rng, attempts=4):
    n=len(values); nearest=[int(x>0.5) for x in values]
    costs=[min(x,1-x) for x in values]
    found={}
    for attempt in range(attempts):
        # Eliminate expensive (strongly fractional) coordinates first.
        order=sorted(range(n), key=lambda j:costs[j]+rng.random()*0.03, reverse=True)
        rank={j:k for k,j in enumerate(order)}
        sequence=[(sum(1<<rank[j] for j in e['variables']), e['rhs']%2, 1<<i) for i,e in enumerate(eq)]
        rng.shuffle(sequence)
        pivots={}
        for mask, rhs, source in sequence:
            while mask:
                pivot=mask & -mask
                if pivot not in pivots:
                    pivots[pivot]=(mask,rhs,source);break
                other, b, s=pivots[pivot];mask^=other;rhs^=b;source^=s
            if not mask:
                assert rhs==0, 'Input parity system itself inconsistent'
                continue
            support=sorted(order[j] for j in bits(mask))
            flips=[j for j in support if nearest[j]]
            if len(flips)%2==rhs:continue
            violation=1-sum(costs[j] for j in support)
            if violation<=1e-7:continue
            key=(tuple(support),tuple(flips))
            if key not in found:
                proof=dict(equations=list(bits(source)),support=support,odd_rhs=rhs,
                           flipped=flips,violation=float(violation))
                verify_cut(eq,proof)
                found[key]=proof
    return list(found.values())


def verify_cut(eq, proof):
    support=set();rhs=0
    for i in proof['equations']:
        support.symmetric_difference_update(eq[i]['variables']);rhs^=eq[i]['rhs']%2
    assert support==set(proof['support'])
    assert rhs==proof['odd_rhs']
    assert set(proof['flipped'])<=support
    assert len(proof['flipped'])%2 != rhs
    return True


def run(core, pop, output, iterations=12):
    eq,edges,rows,c=equations(core,pop,prune_incompatible=True)
    er=[];ec=[]
    for i,e in enumerate(eq):
        for j in e['variables']:er.append(i);ec.append(j)
    A=coo_matrix((np.ones(len(er)),(er,ec)),shape=(len(eq),len(edges))).tocsr()
    b=np.array([e['rhs'] for e in eq],dtype=float)
    objective=np.random.default_rng(0).random(len(edges))
    rng=random.Random(0); cuts=[];keys=set();history=[];started=time.monotonic()
    report=dict(scope='This population; parity cuts necessary for every binary solution',cuts=cuts,history=history)
    for step in range(iterations):
        rr=[];cc=[];vv=[];bb=[]
        for i,cut in enumerate(cuts):
            flips=set(cut['flipped']);bb.append(len(flips)-1)
            for j in cut['support']:rr.append(i);cc.append(j);vv.append(1 if j in flips else -1)
        kwargs={}
        if cuts:kwargs=dict(A_ub=coo_matrix((vv,(rr,cc)),shape=(len(cuts),len(edges))).tocsr(),b_ub=bb)
        lp=linprog(objective,A_eq=A,b_eq=b,bounds=(0,1),method='highs-ds',options={'time_limit':30},**kwargs)
        entry=dict(step=step,lp_status=int(lp.status),elapsed=time.monotonic()-started,cuts=len(cuts))
        if lp.status!=0:
            history.append(entry);report['status']='LP_INFEASIBLE_AFTER_PARITY' if lp.status==2 else 'LP_UNKNOWN'
            print(json.dumps(entry),flush=True);break
        added=discover(eq,lp.x,rng)
        fresh=[]
        for cut in added:
            key=(tuple(cut['support']),tuple(cut['flipped']))
            if key not in keys:keys.add(key);fresh.append(cut)
        cuts.extend(fresh);entry['new_cuts']=len(fresh)
        entry['max_violation']=max((p['violation'] for p in fresh),default=0)
        history.append(entry);print(json.dumps(entry),flush=True)
        report['status']='CUTS_FOUND' if fresh else 'NO_VIOLATED_PARITY_FOUND'
        output.write_text(json.dumps(report,indent=2)+'\n')
        if not fresh:break
    output.write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('core',type=Path);ap.add_argument('population',type=Path)
    ap.add_argument('output',type=Path);ap.add_argument('--iterations',type=int,default=12)
    args=ap.parse_args();run(json.loads(args.core.read_text()),json.loads(args.population.read_text()),args.output,args.iterations)
