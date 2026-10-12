"""Integer degree-price proofs forcing use of one actual pair type.

For a simple factor, beta.r <= s_T*y_T + sum_{R!=T} max(0,s_R).
A strictly positive residual lower bound forces y_T=1. Three or more
forced users can then contradict the two colours of a doubled type.
Floating LP duals merely propose prices; acceptance is exact arithmetic.
"""
from pathlib import Path
from itertools import combinations
import argparse
import json
import time

import numpy as np
from scipy.optimize import linprog
from coclique_variable_border_cuts import border_data
from coclique_forced_types import odd_cycle


def forcing_value(data,u,target,beta):
    n,a,m,d,r,allowed,sat=data
    required=sum(beta[i-4]*r[u,i] for i in range(4,16))
    other=sum(max(0,sum(beta[i-4] for i in row)) for row in m if row!=target and allowed[u,row])
    return dict(required=required,other_upper=other,gap=required-other,
                target_score=sum(beta[i-4] for i in target))


def discover(w):
    start=time.monotonic();data=border_data(w);n,a,m,d,r,allowed,sat=data
    forced={row:{} for row in m};attempts=0
    for u in range(18,n):
        rows=[row for row in m if allowed[u,row]]
        A=np.array([[int(i in row) for row in rows] for i in range(4,16)],dtype=float)
        rhs=np.array([r[u,i] for i in range(4,16)],dtype=float)
        for k,target in enumerate(rows):
            if m[target]!=2:continue
            attempts+=1;c=np.zeros(len(rows));c[k]=1
            lp=linprog(c,A_eq=A,b_eq=rhs,bounds=(0,1),method='highs')
            if not lp.success or lp.fun<1e-7:continue
            raw=lp.eqlin.marginals
            for scale in (1,2,3,4,6,8,12,24):
                beta=[round(scale*float(x)) for x in raw];value=forcing_value(data,u,target,beta)
                if value['gap']>0 and value['target_score']>0:
                    forced[target][u]=dict(vertex=u,prices=beta,**value);break
    obstructions=[]
    for row,users in forced.items():
        if m[row]!=2:continue
        cycle=odd_cycle(sorted(users),sat)
        if cycle:obstructions.append(dict(type=row,cycle=cycle,forcing=[users[u] for u in cycle],
                                         required=len(cycle),upper=len(cycle)-1))
    return dict(seconds=time.monotonic()-start,lp_attempts=attempts,
                forced=[dict(type=row,multiplicity=m[row],users=list(users.values())) for row,users in forced.items() if users],
                odd_cycle_obstructions=obstructions)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path)
    args=ap.parse_args();w=json.loads(args.source.read_text());result=discover(w);result['source']=str(args.source)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(seconds=result['seconds'],lp_attempts=result['lp_attempts'],forced_types=len(result['forced']),
                          forced_users=sum(len(t['users']) for t in result['forced']),odd_cycle_obstructions=result['odd_cycle_obstructions'])),flush=True)
