"""Extract and verify an integer Farkas certificate for a fixed population.

For Ax=b, 0<=x<=1, every integer y satisfies
    y.b <= sum_j max(0,(y.A)_j).
A strict violation is a complete arithmetic impossibility certificate.
Floating-point LP is used only to FIND y; all reported proofs are then
checked with Python integers against reconstructed graph equations.
"""
from pathlib import Path
from itertools import combinations
from fractions import Fraction
from functools import reduce
from math import lcm,gcd
import argparse
import hashlib
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,eye,hstack,vstack,csr_matrix


def equations(core, population, *, prune_incompatible=False):
    q=core['charges'];s=len(q);degree=core['parameters']['degree']
    neighbours=[set() for _ in q]
    for i,j in core['edges']:neighbours[i].add(j);neighbours[j].add(i)
    rows=[];c=[]
    for item in population['selected_rows']:
        for k in range(item['count']):rows.append(set(item['vertices']));c.append(k<item['coclique_count'])
    n=len(rows)
    h=[[2-int(i in row)-len(neighbours[i]&row) for i in range(s)] for row in rows]
    edges=[(u,v) for u,v in combinations(range(n),2) if not(c[u] and c[v]) and len(rows[u]&rows[v])<2
           and (not prune_incompatible or (all(h[u][i]>0 for i in rows[v]) and all(h[v][i]>0 for i in rows[u])))]
    index={e:j for j,e in enumerate(edges)};eq=[]
    def add(u,vertices,rhs,reason):
        ids=[index[tuple(sorted((u,v)))] for v in vertices if v!=u and tuple(sorted((u,v))) in index]
        eq.append(dict(variables=ids,rhs=int(rhs),reason=reason))
    for u,row in enumerate(rows):
        add(u,range(n),degree-len(row),['degree',u])
        if not c[u]:add(u,(v for v in range(n) if c[v]),4 if degree==14 else 2,['coclique_degree',u])
        for i in range(s):add(u,(v for v in range(n) if i in rows[v]),2-int(i in row)-len(neighbours[i]&row),['common_with_core',u,i])
    return eq,edges,rows,c


def verify(eq, edges, coefficients):
    lhs=sum(y*e['rhs'] for y,e in zip(coefficients,eq))
    weights=[0]*len(edges)
    for y,e in zip(coefficients,eq):
        if y:
            for j in e['variables']:weights[j]+=y
    bound=sum(max(0,w) for w in weights)
    return dict(valid=lhs>bound,left=lhs,upper_bound=bound,gap=lhs-bound,
                nonzero_equations=sum(y!=0 for y in coefficients),
                positive_edge_terms=sum(w>0 for w in weights),negative_edge_terms=sum(w<0 for w in weights),
                edge_weights=[dict(edge=edges[j],weight=w) for j,w in enumerate(weights) if w])


def certificate(core, population, seconds=60, *, sparse=False, prune_incompatible=False):
    start=time.monotonic();eq,edges,rows,c=equations(core,population,prune_incompatible=prune_incompatible)
    er=[];ec=[]
    for i,e in enumerate(eq):
        for j in e['variables']:er.append(i);ec.append(j)
    A=coo_matrix((np.ones(len(er)),(er,ec)),shape=(len(eq),len(edges))).tocsr()
    b=np.array([e['rhs'] for e in eq],dtype=float)
    # A^T y - z <= 0, z>=0; minimizing sum z-b^T y.
    if sparse:
        constraints=vstack([hstack([A.T,-A.T,-eye(len(edges))],format='csr'),
                            csr_matrix(np.concatenate([-b,b,np.ones(len(edges))])[None,:])],format='csr')
        result=linprog(np.concatenate([np.ones(2*len(eq)),np.zeros(len(edges))]),
                       A_ub=constraints,b_ub=np.concatenate([np.zeros(len(edges)),[-1.]]),
                       bounds=(0,None),method='highs',options={'time_limit':seconds})
    else:
        result=linprog(np.concatenate([-b,np.ones(len(edges))]),
                       A_ub=hstack([A.T,-eye(len(edges))],format='csr'),b_ub=np.zeros(len(edges)),
                       bounds=[(-1,1)]*len(eq)+[(0,None)]*len(edges),
                       method='highs',options={'time_limit':seconds})
    report=dict(lp_status=int(result.status),lp_message=result.message,seconds=time.monotonic()-start,
                equations=len(eq),variables=len(edges),sparse=sparse,prune_incompatible=prune_incompatible,
                scope='This fixed population; exact integer verification required')
    if result.x is None or (not sparse and result.fun>=-1e-7):
        report['status']='NO_CERTIFICATE';return report
    raw=result.x[:len(eq)]-(result.x[len(eq):2*len(eq)] if sparse else 0)
    yy=None
    for scale in (1,2,3,4,6,8,12,16,24,32,64,128,256,512,1024):
        trial=[round(float(v)*scale) for v in raw]
        if verify(eq,edges,trial)['valid']:yy=trial;break
    if yy is None:
        fractions=[Fraction(float(v)).limit_denominator(1000) for v in raw]
        denominator=lcm(*(x.denominator for x in fractions))
        yy=[int(x*denominator) for x in fractions]
    divisor=reduce(gcd,(abs(v) for v in yy if v),0)
    yy=[v//divisor for v in yy]
    checked=verify(eq,edges,yy)
    report.update(status='EXACT_CONTRADICTION' if checked['valid'] else 'ROUNDING_FAILED',verification=checked,
                  coefficients=[dict(equation=i,coefficient=y,reason=eq[i]['reason'],rhs=eq[i]['rhs']) for i,y in enumerate(yy) if y])
    if checked['valid']:
        # Also keep a compact human-oriented list of the distinct vertices
        # and their types used in the separating linear combination.
        active=sorted({eq[i]['reason'][1] for i,y in enumerate(yy) if y})
        report['active_vertices']=[dict(vertex=i,core_neighbours=sorted(rows[i]),in_coclique=c[i]) for i in active]
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('core',type=Path);ap.add_argument('population',type=Path)
    ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--sparse',action='store_true');ap.add_argument('--prune',action='store_true');args=ap.parse_args()
    cr=args.core.read_bytes();pr=args.population.read_bytes()
    report=certificate(json.loads(cr),json.loads(pr),args.seconds,sparse=args.sparse,prune_incompatible=args.prune)
    report.update(core_sha256=hashlib.sha256(cr).hexdigest(),population_sha256=hashlib.sha256(pr).hexdigest(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    out=args.population.with_name(args.population.stem+'_farkas'+('_sparse' if args.sparse else '')+('_pruned' if args.prune else '')+'.json');out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('coefficients','active_vertices','verification')}),flush=True)
    if 'verification' in report:print(json.dumps({k:v for k,v in report['verification'].items() if k!='edge_weights'}),flush=True)
