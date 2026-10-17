"""Explore the 17-point core of a mill-cubic collision.

The nonnegative kernel vector is (2 at v, 1 on eight neighbours X and
eight cubic vertices V). Enumerate all simple 2-factors on V, whose
edges represent X, and all compatible perfect matchings of X.
Local feasibility is not a completion to SRG(99,14,1,2).
"""
from collections import Counter
from itertools import combinations, permutations, product
import json
import time

from higher_census_minima import ROOT


def cycles(vertices):
    vertices=sorted(vertices)
    for tail in permutations(vertices[1:]):
        if tail[0]>tail[-1]:continue
        order=(vertices[0],)+tail
        yield tuple(sorted(tuple(sorted((order[i],order[(i+1)%len(order)]))) for i in range(len(order))))


def two_factors():
    for edges in cycles(range(8)):yield (8,),edges
    for three in combinations(range(8),3):
        other=sorted(set(range(8))-set(three))
        triangle=tuple(combinations(three,2))
        for five in cycles(other):yield (5,3),tuple(sorted(triangle+five))
    for four in combinations(range(1,8),3):
        a=(0,)+four;b=sorted(set(range(8))-set(a))
        for x,y in product(list(cycles(a)),list(cycles(b))):
            yield (4,4),tuple(sorted(x+y))


def matchings(remaining,allowed):
    if not remaining:
        yield ();return
    a=min(remaining)
    for b in sorted(remaining-{a}):
        if (a,b) not in allowed:continue
        for tail in matchings(remaining-{a,b},allowed):yield ((a,b),)+tail


def build_graph(cubic,edges,matching):
    graph=list(cubic)+[0]*9
    for i,(a,b) in enumerate(edges):
        graph[8+i]=(1<<a)|(1<<b)|(1<<16)
        graph[a]|=1<<(8+i);graph[b]|=1<<(8+i)
    for a,b in matching:
        graph[8+a]|=1<<(8+b);graph[8+b]|=1<<(8+a)
    graph[16]=sum(1<<i for i in range(8,16))
    return graph


def prism(graph):
    triangles=[s for s in combinations(range(len(graph)),3)
               if all(graph[i]>>j&1 for i,j in combinations(s,2))]
    for a,b in combinations(triangles,2):
        if set(a)&set(b):continue
        ma=sum(1<<i for i in a);mb=sum(1<<i for i in b)
        if all((graph[i]&mb).bit_count()==1 for i in a) and all((graph[i]&ma).bit_count()==1 for i in b):
            return a+b
    return None


def main():
    started=time.monotonic()
    stages=json.loads((ROOT/'data/codex_census_validation_99.json').read_text())['stages']
    rows=[r for r in next(s for s in stages if s['order']==8)['counts'] if set(r['degrees'])=={3}]
    factors=list(two_factors())
    assert len(factors)==3507 and len({e for _,e in factors})==3507
    records=[];survivors=[]
    for row in rows:
        cubic=row['adjacency_bits'];counts=Counter()
        allowed_edges={tuple((i,j)) for i,j in combinations(range(8),2)
                       if (cubic[i]&cubic[j]).bit_count() < (1 if cubic[i]>>j&1 else 2)}
        for shape,edges in factors:
            if any(e not in allowed_edges for e in edges):continue
            counts['allowed_2_factors']+=1
            allowed_pairs=set()
            for a,b in combinations(range(8),2):
                ea,eb=edges[a],edges[b]
                if set(ea)&set(eb):continue
                if any(sum(bool(cubic[i]>>j&1) for j in eb)>1 for i in ea):continue
                if any(sum(bool(cubic[i]>>j&1) for j in ea)>1 for i in eb):continue
                allowed_pairs.add((a,b))
            for matching in matchings(set(range(8)),allowed_pairs):
                graph=build_graph(cubic,edges,matching)
                counts['locally_admissible_cores']+=1
                p=prism(graph)
                if p:
                    counts['contains_prism']+=1
                else:
                    counts['prismfree_unresolved']+=1
                    survivors.append({'cubic_code':row['code'],'factor_cycles':shape,
                                      'factor_edges':edges,'X_matching':matching,
                                      'adjacency_bits':graph})
        records.append({'cubic_code':row['code'],'counts':dict(counts)})
        print(json.dumps(records[-1]),flush=True)
    report={'scope':__doc__,'lemma':'mill-cubic collision implies positive kernel vector (2,1^16)',
            'two_factors':3507,'records':records,'prismfree_cores':survivors,
            'seconds':time.monotonic()-started,
            'status':'necessary finite cores only; no ambient completions claimed'}
    (ROOT/'data/codex_mill_cubic_positive18.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Prismfree cores:',len(survivors),'seconds:',round(report['seconds'],2),flush=True)


if __name__=='__main__':main()
