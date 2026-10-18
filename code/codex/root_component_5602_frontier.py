"""Exact single-vertex obstruction beyond a partial 36-vertex 5602 core.

Every missing vertex is in X x Y. It has exactly four neighbours in the
known block: one core vertex, one vertex in each of the two X-grids
disjoint from its roots, and one vertex in the disjoint Y-grid. These
8*4^3=512 possibilities are exhaustive. Reject only by already saturated
common-neighbour counts or root-letter quotas. An empty domain proves
that this partial 36-vertex graph has no Conway completion.
"""

from collections import Counter
from itertools import combinations, product

RECTANGLES=((0,3),(1,2),(0,1),(0,2),(1,3),(2,3),(4,5),(4,6),(5,6))
LABELS=tuple((a,b) for q in RECTANGLES for a in (2*q[0],2*q[0]+1)
             for b in (2*q[1],2*q[1]+1))
OUTSIDE=tuple((2*a+s,2*b+t) for a in range(4) for b in range(4,7)
              for s,t in product(range(2),repeat=2))
SHARED=tuple(tuple(len(set(a)&set(b)) for b in LABELS) for a in LABELS)


def test(g,keep_domains=False):
    deficits=[[12-sum(g[u]) if u==v else 2-g[u][v]-SHARED[u][v]-
               sum(g[u][w]*g[v][w] for w in range(36)) for v in range(36)] for u in range(36)]
    letter_deficits=[[2-int(l in LABELS[u])-int((l^1) in LABELS[u])-
                      sum(g[u][v] for v in range(36) if l in LABELS[v])
                      for l in range(14)] for u in range(36)]
    assert all(min(row)>=0 for row in deficits+letter_deficits)
    domains=[];rejections=[]
    for qi,q in enumerate(OUTSIDE):
        roots={l//2 for l in q}
        groups=[i for i,r in enumerate(RECTANGLES) if i>=2 and roots.isdisjoint(r)]
        assert len(groups)==3
        good=[];rejected=Counter()
        for core,a,b,c in product(range(8),range(4),range(4),range(4)):
            profile=(core,4*groups[0]+a,4*groups[1]+b,4*groups[2]+c)
            if any(deficits[u][v]==0 for u,v in combinations(profile,2)):
                rejected['known_pair_saturated']+=1;continue
            if any(letter_deficits[v][l]==0 for v in profile for l in q):
                rejected['known_vertex_letter_quota']+=1;continue
            if any(sum(g[v][u] for u in profile)>2-int(v in profile)-len(set(q)&set(LABELS[v]))
                   for v in range(36)):
                rejected['new_to_known_C2']+=1;continue
            if any(sum(l in LABELS[v] for v in profile)>2-int(l in q)-int((l^1) in q)
                   for l in range(14)):
                rejected['new_vertex_letter_quota']+=1;continue
            good.append(profile)
        assert len(good)+sum(rejected.values())==512
        domains.append(good);rejections.append(dict(rejected))
        if not good:
            return {'status':'EXCLUDED_EMPTY_VERTEX_DOMAIN','outside_index':qi,
                    'outside_letters':q,'grid_rectangles':[RECTANGLES[i] for i in groups],
                    'total_profiles':512,'rejected_by':dict(rejected),
                    'earlier_domain_sizes':[len(d) for d in domains[:-1]]}
    # A second necessary condition: the selected outside profiles must
    # reproduce the entire residual Gram B B^t of the 36 known vertices.
    for u in range(36):
        for v in range(u,36):
            demand=deficits[u][v]
            maximum=sum(any(u in p and v in p for p in d) for d in domains)
            minimum=sum(all(u in p and v in p for p in d) for d in domains)
            if not minimum<=demand<=maximum:
                return {'status':'EXCLUDED_PROFILE_CAPACITY','known_vertices':[u,v],
                        'demand':demand,'minimum':minimum,'maximum':maximum,
                        'domain_sizes':[len(d) for d in domains]}
    out={'status':'PASSES_SINGLE_VERTEX_AND_PAIR_CAPACITY','domain_sizes':[len(d) for d in domains]}
    if keep_domains:out.update(domains=domains,residual_gram=deficits,letter_deficits=letter_deficits)
    return out
