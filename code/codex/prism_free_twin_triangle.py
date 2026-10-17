"""Verify a local triple of prism-free representatives and its shorter copy.

In any hypothetical six-grid pencil the construction is forced. The small
fixture is locally admissible, but is not a claimed completion to 99 points.
"""
from itertools import combinations
import argparse
import json

from higher_census_minima import ROOT
from six_three_small_mass_bounds import admissible
from prism_free_mass6_bounds import prism_free


def norm(graph,vector):
    assert sum(vector)%3==0
    return (3*sum(x*x for x in vector)+(sum(vector)//3)**2
            -sum(vector[i]*vector[j] for i in range(len(graph))
                 for j in range(len(graph)) if graph[i]>>j&1))


def main(verify_only=False):
    n=22; graph=[0]*n; neighbours=[0,6,13]; theta=20; centre=21
    for i,j in combinations(range(n),2):
        edge=((i<18 and j<18 and i//6==j//6 and
               (i%6//3==j%6//3 or i%3==j%3))
              or (18<=i<21 and 18<=j<21)
              or (i<18 and 18<=j<21 and i%3==j-18)
              or (j==centre and i in neighbours))
        if edge: graph[i]|=1<<j; graph[j]|=1<<i
    assert admissible(graph)
    vectors=[]; records=[]
    shorter=[-int(i in set(neighbours)|{centre,18,19}) for i in range(n)]
    assert norm(graph,shorter)==8
    assert prism_free(graph,[i for i,x in enumerate(shorter) if x])
    for block,omitted in enumerate(neighbours):
        prism=set(range(6*block,6*block+6))
        positive=prism-{omitted}|{theta}
        negative=set(neighbours)-{omitted}|{centre}
        vector=[int(i in positive)-int(i in negative) for i in range(n)]
        assert norm(graph,vector)==8
        assert prism_free(graph,positive) and prism_free(graph,negative)
        ep=sum(bool(graph[i]>>j&1) for i,j in combinations(positive,2))
        en=sum(bool(graph[i]>>j&1) for i,j in combinations(negative,2))
        cross=sum(bool(graph[i]>>j&1) for i in positive for j in negative)
        assert (len(positive),len(negative),ep,en,cross)==(6,3,8,2,0)
        grid=[int(i in prism|{18,19,20}) for i in range(n)]
        assert all(sum(grid[j] for j in range(n) if graph[i]>>j&1)-3*grid[i]==1 for i in range(n))
        assert [x-y for x,y in zip(vector,grid)]==shorter
        assert sum(vector[i]*grid[i] for i in range(n))==6
        vectors.append(vector)
        records.append({'positive':sorted(positive),'negative':sorted(negative),
                        'positive_edges':ep,'negative_edges':en,'cross_edges':cross,
                        'norm':8,'grid_net_sum':6})
    for i,j in combinations(range(3),2):
        delta=[x-y for x,y in zip(vectors[i],vectors[j])]
        expected=[int(v//6==i and v<18)-int(v//6==j and v<18) for v in range(n)]
        assert delta==expected
        assert all(sum(delta[v] for v in range(n) if graph[u]>>v&1)==3*delta[u] for u in range(n))
    report={'adjacency_bits':graph,'representatives':records,
            'shorter_representative':shorter,'shorter_support_size':6,'shorter_norm':8,
            'forced_positive_triples_per_six_grid_pencil':60*3*4,
            'forced_triples_both_signs_per_six_grid_pencil':2*60*3*4,
            'scope':__doc__}
    path=ROOT/'data/codex_prism_free_twin_triangle.json'
    if verify_only: assert json.loads(path.read_text())==report
    else:path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Verified three prism-free Q8 representatives, their twin differences, and their common support-six copy.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true')
    main(parser.parse_args().verify_only)
