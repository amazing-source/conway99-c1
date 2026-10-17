"""Transported rows assigned to their actual centres, with arc consistency.

For centres in different root triangles, |S_j & S_k| + |B_j & B_k|=1.
For the two centres of one triangle, the intersection is exactly {j,k}.
Unknown incidences are relaxed only within their remaining capacities.
"""
from collections import deque


def indices(mask):
    while mask:
        bit=mask&-mask;mask-=bit
        yield bit.bit_length()-1


def centred_resolution(centres,domains,patterns,quotas,known_overlap,missing,
                       max_nodes=100000,support=None,support_start=None):
    n=len(centres);width=len(quotas)
    assert n==10
    cols=[[sum(1<<a for a,row in enumerate(dom) if row>>j&1)
           for j in range(width)] for dom in domains]
    compat={}
    for x in range(n):
        for y in range(x+1,n):
            j,k=centres[x],centres[y]
            if patterns[x]==patterns[y]:lo=hi=2
            else:
                hi=1-known_overlap[j][k]
                lo=max(0,hi-min(missing[j],missing[k]))
            xy=[0]*len(domains[x]);yx=[0]*len(domains[y])
            for a,r in enumerate(domains[x]):
                for b,s in enumerate(domains[y]):
                    if r!=s and lo<=(r&s).bit_count()<=hi:
                        xy[a] |= 1<<b;yx[b] |= 1<<a
            compat[x,y]=xy;compat[y,x]=yx
    nodes=arc_prunes=quota_prunes=point_prunes=0
    limited=False;witness=None;final_pool=None

    def propagate(ds,pool):
        nonlocal arc_prunes,quota_prunes,point_prunes
        again=True
        while again:
            before=tuple(ds)
            queue=deque((x,y) for x in range(n) for y in range(n) if x!=y)
            while queue:
                x,y=queue.popleft();old=ds[x];dy=ds[y]
                ds[x]=sum(1<<a for a in indices(old) if compat[x,y][a]&dy)
                if not ds[x]:arc_prunes+=1;return None
                if old!=ds[x]:
                    queue.extend((z,x) for z in range(n) if z!=x and z!=y)
            for j,q in enumerate(quotas):
                can=[x for x in range(n) if ds[x]&cols[x][j]]
                must=[x for x in can if not ds[x]&~cols[x][j]]
                if len(must)>q or len(can)<q:
                    quota_prunes+=1;return None
                if len(must)==q:
                    for x in can:
                        if x not in must:ds[x] &= ~cols[x][j]
                elif len(can)==q:
                    for x in can:ds[x] &= cols[x][j]
            if support is not None:
                for x in range(n):
                    available=0
                    for a in indices(ds[x]):available |= support.masks[domains[x][a]]
                    pool &= available
                if not support.possible(pool):point_prunes+=1;return None
            again=tuple(ds)!=before
        return ds,pool

    def dfs(ds,pool):
        nonlocal nodes,limited,witness,final_pool
        nodes+=1
        if nodes>max_nodes:limited=True;return False
        p=propagate(ds,pool)
        if p is None:return False
        ds,pool=p
        sizes=[d.bit_count() for d in ds]
        if max(sizes)==1:
            witness=[domains[x][d.bit_length()-1] for x,d in enumerate(ds)]
            final_pool=pool
            return True
        x=min((x for x in range(n) if sizes[x]>1),key=lambda x:sizes[x])
        for a in indices(ds[x]):
            child=list(ds);child[x]=1<<a
            if dfs(child,pool):return True
            if limited:return False
        return False

    sat=dfs([(1<<len(dom))-1 for dom in domains],support_start)
    return dict(status='SAT_RESOLUTION_ONLY' if sat else 'UNKNOWN' if limited else 'UNSAT_RESOLUTION',
                nodes=nodes,witness_rows=witness,centres=centres,
                arc_prunes=arc_prunes,quota_prunes=quota_prunes,support_prunes=point_prunes)
