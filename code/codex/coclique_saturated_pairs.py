"""Use saturated common-neighbour pairs as reusable packing inequalities.

If two exterior columns already intersect in two core vertices, they cannot
have any other common neighbour. For every w: d_uw+d_vw <= 1.
An integer Farkas combination of these bounds and the shared linear quotas
is an independently checkable certificate, even when the old LP is feasible.
"""
from pathlib import Path
from itertools import combinations
from functools import reduce
from math import gcd,lcm
from fractions import Fraction
import argparse
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,hstack,vstack,eye,csr_matrix
from coclique_completion_certificate import equations


def system(core,pop):
    eq,edges,rows,colours=equations(core,pop,prune_incompatible=True)
    index={e:j for j,e in enumerate(edges)};packing={}
    for u,v in combinations(range(len(rows)),2):
        if len(rows[u]&rows[v])!=2:continue
        for w in range(len(rows)):
            a=index.get(tuple(sorted((u,w))));b=index.get(tuple(sorted((v,w))))
            if a is None or b is None:continue
            key=tuple(sorted((a,b)))
            packing.setdefault(key,dict(variables=list(key),rhs=1,saturated_pair=[u,v],neighbour=w))
    return eq,edges,rows,list(packing.values())


def verify(eq,edges,packing,y,z):
    assert all(t>=0 for t in z)
    lhs=sum(a*e['rhs'] for a,e in zip(y,eq))-sum(a*e['rhs'] for a,e in zip(z,packing))
    weights=[0]*len(edges)
    for a,e in zip(y,eq):
        for j in e['variables']:weights[j]+=a
    for a,e in zip(z,packing):
        for j in e['variables']:weights[j]-=a
    bound=sum(max(0,a) for a in weights)
    return dict(valid=lhs>bound,left=lhs,upper_bound=bound,gap=lhs-bound)


def run(core,pop,output,seconds=60,packing_indices=None):
    started=time.monotonic();eq,edges,rows,packing=system(core,pop)
    selected_indices=list(range(len(packing))) if packing_indices is None else packing_indices
    packing=[packing[i] for i in selected_indices]
    def matrix(items):
        rr=[];cc=[]
        for i,e in enumerate(items):
            for j in e['variables']:rr.append(i);cc.append(j)
        return coo_matrix((np.ones(len(rr)),(rr,cc)),shape=(len(items),len(edges))).tocsr()
    A=matrix(eq);G=matrix(packing);b=np.array([e['rhs'] for e in eq],dtype=float)
    # y = y+ - y-. z >= 0 weights upper-bound premises Gx <= 1.
    constraints=vstack([hstack([A.T,-A.T,-G.T,-eye(len(edges))],format='csr'),
        csr_matrix(np.r_[-b,b,np.ones(len(packing)+len(edges))][None,:])],format='csr')
    result=linprog(np.r_[np.ones(2*len(eq)+len(packing)),np.zeros(len(edges))],
            A_ub=constraints,b_ub=np.r_[np.zeros(len(edges)),-1.],bounds=(0,None),
            method='highs',options={'time_limit':seconds})
    report=dict(lp_status=int(result.status),lp_message=result.message,packing_inequalities=len(packing),
                seconds=time.monotonic()-started,status='NO_CERTIFICATE',
                scope='This population; universal saturated-pair packing lemma')
    if result.x is not None:
        rawy=result.x[:len(eq)]-result.x[len(eq):2*len(eq)]
        rawz=result.x[2*len(eq):2*len(eq)+len(packing)]
        found=None
        for scale in (1,2,3,4,6,8,12,16,24,32,64,128,256,512,1024):
            y=[round(float(x)*scale) for x in rawy];z=[round(float(x)*scale) for x in rawz]
            check=verify(eq,edges,packing,y,z)
            if check['valid']:found=(y,z,check);break
        if found:
            y,z,check=found;report.update(status='EXACT_CONTRADICTION',verification=check,
                equations=[dict(index=i,coefficient=a,reason=eq[i]['reason'],rhs=eq[i]['rhs']) for i,a in enumerate(y) if a],
                packing=[dict(index=selected_indices[i],coefficient=a,**packing[i]) for i,a in enumerate(z) if a])
        else:report['status']='ROUNDING_FAILED'
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('equations','packing')}),flush=True)
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('core',type=Path);ap.add_argument('population',type=Path)
    ap.add_argument('output',type=Path);ap.add_argument('--seconds',type=float,default=60)
    args=ap.parse_args();run(json.loads(args.core.read_text()),json.loads(args.population.read_text()),args.output,args.seconds)
