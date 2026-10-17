"""Explore locally admissible rooted lambda=1,mu=2 skeletons.

This constructs PARTIAL graphs, never reports them as SRGs. The closed-star
rows are complete. Far vertices have degree four (two star neighbors and
two transport neighbors); their remaining degree is unassigned. All present
edges have one common neighbor and all other pairs have at most two.
Color-preserving switches change the transport matching at one star neighbor.
We ask whether cycle lengths divisible by four are forced by these LOCAL
conditions; a counterexample cannot decide global SRG completability.
"""
from collections import Counter
import itertools
import json
from pathlib import Path
import random
import time

import igraph as ig
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/codex_asymmetry_mechanisms_20261014'


def run(t=7,seed=1401,steps=10000):
    rng=random.Random(seed);start=time.monotonic()
    labels=list(range(2*t)); pairs=[(a,b) for a,b in itertools.combinations(labels,2) if a//2!=b//2]
    first=2*t+1; n=first+len(pairs)
    idx={ab:first+i for i,ab in enumerate(pairs)}
    A=np.zeros((n,n),dtype=np.int64); match={a:{} for a in labels}
    def put(u,v): A[u,v]=A[v,u]=1
    for a in labels:
        put(0,a+1);put(a+1,(a^1)+1)
    for (a,b),y in idx.items():
        put(a+1,y);put(b+1,y)
        for common,other in [(a,b),(b,a)]:
            z=idx[tuple(sorted((common,other^1)))]
            put(y,z);match[common][y]=z
    C=A@A
    def edge(u,v,sign):
        C[:,v]+=sign*A[:,u]; C[v,:]+=sign*A[u,:]
        C[:,u]+=sign*A[:,v]; C[u,:]+=sign*A[v,:]
        C[u,u]+=1; C[v,v]+=1
        A[u,v]+=sign;A[v,u]+=sign
    def lengths():
        remaining=set(range(first,n));out=[]
        while remaining:
            v=min(remaining);remaining.remove(v);stack=[v];size=0
            while stack:
                u=stack.pop();size+=1
                ns=set(map(int,np.flatnonzero(A[u,first:])))
                ns={z+first for z in ns}&remaining
                remaining-=ns;stack.extend(ns)
            out.append(size)
        return sorted(out)
    accepted=0;found=[]
    for step in range(steps):
        a=rng.choice(labels); keys=list(match[a]);y=rng.choice(keys);z=match[a][y]
        u=rng.choice([v for v in keys if v not in [y,z]]);v=match[a][u]
        changes=[(y,z,-1),(u,v,-1),(y,u,1),(z,v,1)]
        for b,c,sign in changes:edge(b,c,sign)
        bad=C>2-A;np.fill_diagonal(bad,False)
        if bad.any():
            for b,c,sign in reversed(changes):edge(b,c,-sign)
            continue
        match[a][y]=u;match[a][u]=y;match[a][z]=v;match[a][v]=z
        accepted+=1
        ls=lengths()
        if any(k%4 for k in ls):
            # Exact checks of this newly constructed partial object only.
            assert np.array_equal(C,A@A)
            assert np.all(C[A==1]==1)
            assert all(int(A[v].sum())==2*t for v in range(first))
            assert all(int(A[v].sum())==4 for v in range(first,n))
            g=ig.Graph(n=n,edges=list(zip(*np.where(np.triu(A,1)))))
            order=g.count_automorphisms(color=[int(v==0) for v in range(n)])
            item={'step':step+1,'accepted_switches':accepted,'transport_cycle_lengths':ls,
                  'rooted_skeleton_group_order':order,'has_odd_cycle':any(k%2 for k in ls)}
            found.append(item)
            name=f'local_t{t}_s{seed}_{len(found)}'
            (OUT/(name+'.edges')).write_text(''.join(f'{u} {v}\n' for u,v in zip(*np.where(np.triu(A,1)))),encoding='ascii')
            item['edge_file']=name+'.edges'
            if order==1 and item['has_odd_cycle']:
                break
            if len(found)>=6:
                break
    result={'status':'partial_local_experiment_only','target_srg_size':n,'k':2*t,'lambda':1,'mu':2,
            'seed':seed,'attempted_switches':step+1,'accepted_switches':accepted,
            'not_a_complete_srg':True,'unknown_far_degree':2*t-4,
            'counterexamples_to_local_cycle_divisibility':found,'seconds':time.monotonic()-start}
    (OUT/f'local_t{t}_s{seed}.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    run()
