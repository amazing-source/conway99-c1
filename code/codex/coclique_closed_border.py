"""Exact cover certificates for a required vertex beyond a closed 59/60 border.

The six complete neighbourhoods (four H and the negative edge) must be met
by one common selection among the known vertices. Saturated old pairs prune
impossible neighbours. A Farkas certificate can exclude all completions of
this border without choosing any of the 39/40 remaining vertices' edges.
"""
from pathlib import Path
from itertools import combinations
import argparse
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,hstack,vstack,eye


def analyse(witness):
    n=witness['vertices'];adj=[set() for _ in range(n)]
    for i,j in witness['edges']:adj[i].add(j);adj[j].add(i)
    C=set(witness['coclique']);closed=[i for i in range(n) if len(adj[i])==14]
    saturated={(i,j) for i,j in combinations(range(n),2) if len(adj[i]&adj[j])==2-int(j in adj[i])}
    results=[]
    for item in witness['remaining_population']:
        R=set(item['vertices'])
        for colour,count in ((True,item['coclique_count']),(False,item['count']-item['coclique_count'])):
            if not count:continue
            candidates=[v for v in range(18,n) if v not in closed and not(colour and v in C)
                        and all(tuple(sorted((i,v))) not in saturated for i in R)]
            eq=[dict(centre=i,rhs=2-int(i in R)-len(adj[i]&R),
                     variables=[j for j,v in enumerate(candidates) if v in adj[i]]) for i in closed]
            A=np.array([[int(j in e['variables']) for j in range(len(candidates))] for e in eq],dtype=float)
            b=np.array([e['rhs'] for e in eq],dtype=float)
            # Only closed-centre equations are used. Further constraints on
            # the new vertex would strengthen this necessary relaxation.
            A=csr_matrix(A.reshape((len(eq),len(candidates))))
            cons=vstack([hstack([A.T,-A.T,-eye(len(candidates))],format='csr'),
                         csr_matrix(np.r_[-b,b,np.ones(len(candidates))][None,:])],format='csr')
            lp=linprog(np.r_[np.ones(2*len(eq)),np.zeros(len(candidates))],A_ub=cons,
                       b_ub=np.r_[np.zeros(len(candidates)),-1.],bounds=(0,None),
                       method='highs',options={'time_limit':2})
            entry=dict(row=sorted(R),in_coclique=colour,required_copies=count,candidates=candidates,
                       closed=closed,lp_status=int(lp.status),status='NO_CERTIFICATE')
            if lp.x is not None:
                raw=lp.x[:len(eq)]-lp.x[len(eq):2*len(eq)]
                for scale in (1,2,3,4,6,8,12,24,48):
                    y=[round(scale*float(x)) for x in raw]
                    left=sum(t*e['rhs'] for t,e in zip(y,eq))
                    weights=[sum(t for t,e in zip(y,eq) if j in e['variables']) for j in range(len(candidates))]
                    right=sum(max(0,t) for t in weights)
                    if left>right:
                        entry.update(status='EXACT_CONTRADICTION',equations=eq,coefficients=y,left=left,right=right)
                        break
            results.append(entry)
    return dict(scope='Every completion of this fixed induced border and its forced residual population',
                required_types=len(results),excluded=sum(x['status']=='EXACT_CONTRADICTION' for x in results),results=results)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path)
    args=ap.parse_args();result=analyse(json.loads(args.source.read_text()))
    result['source']=str(args.source);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='results'}),flush=True)
