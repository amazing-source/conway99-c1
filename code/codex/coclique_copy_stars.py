"""Bipartite requesters can still exceed a closed-star quota on one copy.

If a centre uses one of <=2 copies, all its saturated requester neighbours
must use the other copy. At most q=2-|type intersect N(s)| of those users
may lie in a completed N(s). A star with q+1 such leaves is forbidden.
The source obstruction need not contain any odd cycle.
"""
from itertools import combinations
from coclique_closed_star_balance import CLOSED


def evaluate(w,cut):
    from coclique_variable_border_cuts import border_data
    n,a,m,d,r,allowed,sat=border_data(w)
    row=tuple(cut['type']);u=cut['center'];leaves=cut['leaves'];s=cut['closed_vertex'];q=cut['quota']
    applies=(len(a[s])==14 and 2-len(a[s]&set(row))<=q and all(v in a[s] and tuple(sorted((u,v))) in sat for v in leaves))
    if not applies:return dict(applies=False)
    y={(t['vertex'],tuple(t['type'])):t['count'] for t in w['factors']}
    left=sum(y.get((v,row),0) for v in [u]+leaves)
    return dict(applies=True,left=left,upper=len(leaves),violated=left>len(leaves))


def install(master,cut):
    row=tuple(cut['type']);u=cut['center'];leaves=cut['leaves'];s=cut['closed_vertex'];q=cut['quota']
    assert master.factors and master.simple and s in CLOSED and len(leaves)==q+1 and len(set([u]+leaves))==q+2
    if max([u]+leaves)>=master.ctx['n']:return False
    anchor_common=sum(master.edge(s,i) for i in row)
    assert isinstance(anchor_common,int)
    if 2-anchor_common>q:return False
    guards=[]
    for v in leaves:
        i,j=sorted((u,v));guards.append(master.predicate(('sat',i,j),master.ctx['common'][i,j]+master.edge(i,j),2))
        guards.append(master.edge(s,v))
    master.model.Add(sum(master.factors[v,row] for v in [u]+leaves)<=len(leaves)).OnlyEnforceIf(guards)
    master.installed.append(cut);return True


def discover(w):
    from coclique_variable_border_cuts import border_data
    n,a,m,d,r,allowed,sat=border_data(w)
    y={(t['vertex'],tuple(t['type'])):t['count'] for t in w['factors']};cuts=[]
    for row,mult in m.items():
        if mult!=2:continue
        users=[u for u in range(18,n) if y.get((u,row),0)]
        for s in CLOSED:
            q=2-len(a[s]&set(row))
            if q<1:continue
            found=False
            for center in users:
                leaves=[v for v in users if v!=center and v in a[s] and tuple(sorted((center,v))) in sat]
                for group in combinations(leaves,q+1):
                    # Seek an induced star, so no odd-cycle cut already
                    # explains the obstruction on these same requesters.
                    if any(tuple(sorted(e)) in sat for e in combinations(group,2)):continue
                    cut=dict(kind='copy_closed_star_capacity',type=list(row),center=center,leaves=list(group),closed_vertex=s,quota=q,
                             law='Saturated neighbours of one requester use the other copy and obey its closed-star quota')
                    cut['separation']=evaluate(w,cut);assert cut['separation']['violated'];cuts.append(cut);found=True;break
                if found:break
    return cuts
