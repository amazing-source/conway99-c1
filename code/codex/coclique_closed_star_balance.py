"""Reciprocal quotas for each residual type against already complete stars.

If s has its complete neighbourhood in B and a residual copy t has type
{i,j}, t is not adjacent to s. Exactly two vertices of N(s) neighbour t.
Summing over the m_ij actual copies gives a type-wise column equality.
These are necessary even before choosing names for doubled copies.
"""
from itertools import combinations


CLOSED=(0,1,2,3,16,17)


def install(master):
    assert master.factors and master.simple
    for row,m in master.m.items():
        for s in CLOSED:
            # Edges from these six vertices into L are fixed in this model.
            anchor_common=sum(master.edge(s,i) for i in row)
            assert isinstance(anchor_common,int)
            terms=[master.ctx['product'](master.edge(s,u),master.factors[u,row]) for u in range(18,master.ctx['n'])]
            master.model.Add(sum(terms)==(2-anchor_common)*m)
    master.closed_star_balances=True


def verify(w):
    n=w['vertices'];a=[set() for _ in range(n)]
    for u,v in w['edges']:a[u].add(v);a[v].add(u)
    m={tuple(t['vertices']):t['count'] for t in w['remaining_population']}
    y={(t['vertex'],tuple(t['type'])):t['count'] for t in w['factors']}
    for row,count in m.items():
        for s in CLOSED:
            assert sum(y.get((u,row),0) for u in range(18,n) if u in a[s])==(2-len(a[s]&set(row)))*count
    return True


def diagnose(w):
    n=w['vertices'];a=[set() for _ in range(n)]
    for u,v in w['edges']:a[u].add(v);a[v].add(u)
    m={tuple(t['vertices']):t['count'] for t in w['remaining_population']}
    y={(t['vertex'],tuple(t['type'])):t['count'] for t in w['factors']};bad=[]
    for row,count in m.items():
        for s in CLOSED:
            left=sum(y.get((u,row),0) for u in range(18,n) if u in a[s])
            right=(2-len(a[s]&set(row)))*count
            if left!=right:bad.append(dict(type=row,closed_vertex=s,observed=left,required=right))
    identities=[]
    for s in CLOSED:
        weights=a[s];total=sum(14-len(a[u]) for u in weights)
        q=total+2*sum(2-int(v in a[u])-len(a[u]&a[v]) for u,v in combinations(sorted(weights),2))
        assert total==2*(99-n) and q==4*(99-n)
        identities.append(dict(vertex=s,sum_loads=total,square_sum=q,variance=q-4*total+4*(99-n)))
    return dict(violations=bad,zero_variance_identities=identities)
