"""Exhaustive balls around four pairwise-grid root lines.

The33 vertices consist of the root, eight neighbours and six four-cycles
Q_ij. Two grids sharing a line are perfect dominating codes, so there are
no edges between Q_ij and Q_ik. Between opposite Q_ij,Q_kl there is exactly
a perfect matching. Hence only24^3 labelled balls, quotiented by the actual
root-line relabellings S4 semidirect C2^4. No automorphism of a completion
is assumed. Templates7 and9 both contain such a four-line grid clique.
"""
import argparse
from collections import Counter
from itertools import combinations,permutations,product
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process

PAIRS=list(combinations(range(4),2))
OPPOSITE=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
PERMS=list(permutations(range(4)))


def generator_tables():
    index={p:i for i,p in enumerate(PERMS)};generators=[]
    for a in range(3):
        p=list(range(4));p[a],p[a+1]=p[a+1],p[a]
        generators.append((p,[0]*4))
    for a in range(4):
        bits=[0]*4;bits[a]=1;generators.append((list(range(4)),bits))
    tables=[]
    for p,bits in generators:
        def image(pair,corner):
            (a,b)=pair;s,t=divmod(corner,2)
            labels=sorted(((p[a],s^bits[a]),(p[b],t^bits[b])))
            return tuple(i for i,_ in labels),2*labels[0][1]+labels[1][1]
        mappings=[]
        for left,right in OPPOSITE:
            local=[]
            for perm in PERMS:
                edges=[(image(left,i),image(right,perm[i])) for i in range(4)]
                target=OPPOSITE.index(tuple(sorted((edges[0][0][0],edges[0][1][0]))))
                result=[None]*4
                for (a,i),(b,j) in edges:
                    if a>b:i,j=j,i
                    result[i]=j
                assert sorted(result)==list(range(4))
                local.append((target,index[tuple(result)]))
            mappings.append(local)
        tables.append(mappings)
    return tables


def canonical_orbits():
    tables=generator_tables();unseen=set(product(range(24),repeat=3));records=[]
    while unseen:
        first=min(unseen);orbit={first};pending=[first];unseen.remove(first)
        while pending:
            state=pending.pop()
            for table in tables:
                result=[None]*3
                for i,value in enumerate(state):
                    target,new=table[i][value];result[target]=new
                image=tuple(result)
                if image not in orbit:
                    assert image in unseen
                    unseen.remove(image);orbit.add(image);pending.append(image)
        records.append({'index':len(records),'representative':list(first),'orbit_size':len(orbit),
                        'matching_permutations':[list(PERMS[i]) for i in first]})
    assert sum(r['orbit_size'] for r in records)==24**3
    return records


def gamma_ball(code):
    labels=[(2*a+s,2*b+t) for a,b in PAIRS for s,t in product(range(2),repeat=2)]
    lookup={p:i for i,p in enumerate(labels)}
    c=[[0]*24 for _ in range(24)]
    for k in range(6):
        for i,j in combinations(range(4),2):
            if (i^j) in (1,2):c[4*k+i][4*k+j]=c[4*k+j][4*k+i]=1
    for (left,right),pi in zip(OPPOSITE,code):
        li=PAIRS.index(left);ri=PAIRS.index(right)
        for i,j in enumerate(PERMS[pi]):c[4*li+i][4*ri+j]=c[4*ri+j][4*li+i]=1
    assert all(sum(row)==3 for row in c)
    return labels,c


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();resources=limit_research_process(1);started=time.process_time()
    records=canonical_orbits()
    for r in records:
        labels,c=gamma_ball(r['representative'])
        demands=[2-len(set(labels[u])&set(labels[v]))-c[u][v]-sum(c[u][z]*c[v][z] for z in range(24))
                 for u,v in combinations(range(24),2)]
        assert min(demands)>=0
        r['boundary_common_neighbour_demands']=dict(Counter(demands))
    result={'scope':__doc__,'exhaustive':True,'labelled_ball_count':24**3,'group_order':384,
            'orbit_count':len(records),'records':records,'resources':resources,'cpu_seconds':time.process_time()-started}
    atomic_json_write(args.output,result)
    print(json.dumps({'labelled_ball_count':24**3,'orbits':len(records),
        'orbit_size_histogram':dict(Counter(r['orbit_size'] for r in records)),'cpu_seconds':result['cpu_seconds']}))


if __name__=='__main__':main()
