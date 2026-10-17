"""Shared neighbourhood equations beyond an induced border.

The residual vertices' attachments to S are fixed by their forced types.
Consequently N(s), for every s in S, is known as a set of actual vertices.
One edge variable must serve all the neighbourhood equations.  No residual
coclique colours are used: a contradiction excludes every colouring of this
fixed induced border and its (uncoloured) forced residual multiset.
"""
from pathlib import Path
from itertools import combinations
import argparse
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix, eye, hstack, vstack


def build(witness, support=18, degree=14, lam=1, mu=2):
    bsize = witness['vertices']
    rows = [set() for _ in range(bsize)]
    for item in witness['remaining_population']:
        rows.extend([set(item['vertices']) for _ in range(item['count'])])
    n = len(rows)
    known = [set() for _ in range(n)]
    for u, v in witness['edges']:
        known[u].add(v); known[v].add(u)
    for u in range(bsize, n):
        for s in rows[u]:
            known[u].add(s); known[s].add(u)
    assert all(len(known[s]) == degree for s in range(support))
    saturated = { (u,v) for u,v in combinations(range(bsize),2)
                  if len(known[u] & known[v] & set(range(bsize))) == mu-(mu-lam)*int(v in known[u]) }
    closed = {u for u in range(bsize) if len(known[u]) == degree}
    forbidden = {}
    edges = []
    for u,v in combinations(range(n),2):
        if v < bsize or u < support or u in closed or v in closed:
            continue
        common = len(known[u] & known[v])
        if common > lam:
            forbidden[u,v] = ('too_many_known_common', sorted(known[u]&known[v]))
            continue
        # A new vertex v cannot be a common neighbour of an already
        # saturated old pair (s,u), when v~s is fixed by its type.
        if u < bsize:
            blockers = [s for s in rows[v] if tuple(sorted((s,u))) in saturated]
            if blockers:
                forbidden[u,v] = ('saturated_old_pair', blockers)
                continue
        edges.append((u,v))
    index = {e:j for j,e in enumerate(edges)}
    def variable(u,v):
        return index.get(tuple(sorted((u,v))))
    eq=[]
    for u in range(support,n):
        eq.append(dict(reason=['degree',u],rhs=degree-len(known[u]),
                       variables=[j for j,e in enumerate(edges) if u in e]))
        for s in range(support):
            target=mu-(mu-lam)*int(s in known[u])
            ids=[variable(u,v) for v in known[s] if v!=u]
            eq.append(dict(reason=['common',u,s],star=s in known[u],
                           rhs=target-len(known[u]&known[s]),
                           variables=sorted(j for j in ids if j is not None)))
    packing=[]
    # Only old/old saturated pairs: all their additional common neighbours
    # must be residual, and the two incident edge variables are shared.
    for u,v in sorted(saturated):
        for w in range(bsize,n):
            a=variable(u,w); b=variable(v,w)
            if a is not None and b is not None:
                packing.append(dict(reason=['saturated',u,v,w],variables=[a,b],rhs=1))
    return dict(vertices=n,border=bsize,support=support,degree=degree,lam=lam,mu=mu,
                edges=edges,equations=eq,packing=packing,known=known,rows=rows,
                forbidden=forbidden)


def separate(system, mode='matching', seconds=15):
    started=time.monotonic()
    edges=system['edges']
    eq=[e for e in system['equations'] if mode!='matching' or e.get('star')]
    packing=system['packing'] if mode=='packing' else []
    def matrix(items):
        rr=[]; cc=[]
        for i,e in enumerate(items):
            for j in e['variables']: rr.append(i); cc.append(j)
        return coo_matrix((np.ones(len(rr)),(rr,cc)),shape=(len(items),len(edges))).tocsr()
    A=matrix(eq); G=matrix(packing)
    b=np.array([e['rhs'] for e in eq],dtype=float)
    d=np.array([e['rhs'] for e in packing],dtype=float)
    constraints=vstack([hstack([A.T,-A.T,-G.T,-eye(len(edges))],format='csr'),
                         csr_matrix(np.r_[-b,b,d,np.ones(len(edges))][None,:])],format='csr')
    lp=linprog(np.r_[np.ones(2*len(eq)+len(packing)),np.zeros(len(edges))],
               A_ub=constraints,b_ub=np.r_[np.zeros(len(edges)),-1.],bounds=(0,None),
               method='highs',options={'time_limit':seconds})
    result=dict(mode=mode,variables=len(edges),equations=len(eq),packing=len(packing),
                lp_status=int(lp.status),lp_message=lp.message,seconds=time.monotonic()-started,
                status='NO_CERTIFICATE')
    if lp.x is not None:
        rawy=lp.x[:len(eq)]-lp.x[len(eq):2*len(eq)]
        rawz=lp.x[2*len(eq):2*len(eq)+len(packing)]
        for scale in (1,2,3,4,6,8,12,24,48,96,192,384,768,1536):
            y=[round(scale*float(t)) for t in rawy]
            z=[round(scale*float(t)) for t in rawz]
            weights=[0]*len(edges)
            left=sum(t*e['rhs'] for t,e in zip(y,eq))-sum(t*e['rhs'] for t,e in zip(z,packing))
            for t,e in zip(y,eq):
                for j in e['variables']:weights[j]+=t
            for t,e in zip(z,packing):
                for j in e['variables']:weights[j]-=t
            upper=sum(max(0,t) for t in weights)
            if left>upper and all(t>=0 for t in z):
                result.update(status='EXACT_CONTRADICTION',left=left,upper=upper,
                    certificate_equations=[dict(coefficient=t,**e) for t,e in zip(y,eq) if t],
                    certificate_packing=[dict(coefficient=t,**e) for t,e in zip(z,packing) if t],
                    positive_edges=[dict(edge=edges[j],coefficient=t) for j,t in enumerate(weights) if t>0])
                break
        else:result['status']='ROUNDING_FAILED'
    return result


def positive_fixture():
    # Rook graph on a 3x3 grid: all actual edges must survive pruning and
    # satisfy every equation and packing premise of the new model.
    order=[0,1,3,4,2,5,6,7,8]
    actual=[{j for j,b in enumerate(order) if i!=j and (a//3==b//3 or a%3==b%3)}
            for i,a in enumerate(order)]
    witness=dict(vertices=4,edges=[(i,j) for i,j in combinations(range(4),2) if j in actual[i]],
                 remaining_population=[dict(vertices=sorted(actual[i]&{0,1}),count=1) for i in range(4,9)])
    system=build(witness,support=2,degree=4,lam=1,mu=2)
    x=[int(v in actual[u]) for u,v in system['edges']]
    assert all(v not in actual[u] for u,v in system['forbidden'])
    assert all(sum(x[j] for j in e['variables'])==e['rhs'] for e in system['equations'])
    assert all(sum(x[j] for j in e['variables'])<=e['rhs'] for e in system['packing'])
    return dict(status='PASS',graph='3x3 rook',variables=len(x),equations=len(system['equations']))


def run(source,output,seconds=15):
    witness=json.loads(source.read_text())
    system=build(witness)
    report=dict(source=str(source),scope='All completions and residual coclique colourings of this fixed induced border',
                vertices=system['vertices'],border=system['border'],fixture=positive_fixture(),stages=[])
    for mode in ('matching','linear','packing'):
        result=separate(system,mode,seconds)
        report['stages'].append(result)
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(source=source.name,**{k:v for k,v in result.items() if not isinstance(v,list)})),flush=True)
        if result['status']=='EXACT_CONTRADICTION':break
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path)
    ap.add_argument('--seconds',type=float,default=15)
    args=ap.parse_args();run(args.source,args.output,args.seconds)
