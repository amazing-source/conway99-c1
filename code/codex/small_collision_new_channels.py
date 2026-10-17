"""New mass-seven cross channels and mass-eight losses for sums 0,+3,-3.

Mass-eight excludes C14 and therefore assumes P=0. Bounds on one exterior
vertex use exact first/second moments and maxima of finite local costs.
No previously completed census or mass-six calculation is repeated.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, permutations
import json

import numpy as np
from sympy import Matrix

from higher_census_minima import ROOT
from six_three_small_mass_bounds import admissible, extend


def pair_graph(left, right, cross):
    n = len(left)
    graph = list(left)+[r << n for r in right]
    for u,v in cross:
        graph[u] |= 1 << (n+v)
        graph[n+v] |= 1 << u
    return graph


def select_coordinates(weights, size):
    doubles = [i for i,x in enumerate(weights) if x == 2]
    singles = [i for i,x in enumerate(weights) if x == 1]
    return [set(doubles)|set(s) for s in combinations(singles,size-len(doubles))]


def templates(left_weights, right_weights, shape, other_shape):
    mass = sum(left_weights)
    common = (sum(shape)+sum(other_shape)-2*mass)//2
    assert common in (0,1)
    delta = np.array(left_weights+[-x for x in right_weights],dtype=np.int16)
    n = len(left_weights)
    vectors = []
    for c in range(common+1):
        for pos in select_coordinates(left_weights,shape[0]-c):
            for neg in select_coordinates(right_weights,shape[1]-(common-c)):
                v = [int(i in pos) for i in range(n)]+[-int(j in neg) for j in range(len(right_weights))]
                tail = [] if common == 0 else [1 if c else -1]
                vectors.append(v+tail)
    vectors = np.array(vectors,dtype=np.int16)
    partner = vectors-np.concatenate((delta,np.zeros(common,dtype=np.int16)))
    for x,sh in ((vectors,shape),(partner,other_shape)):
        assert np.all((x>=-1)&(x<=1))
        assert np.all(np.sum(x==1,axis=1)==sh[0])
        assert np.all(np.sum(x==-1,axis=1)==sh[1])
    return vectors,partner


def counts(graph, profiles, weights, other_weights, shape, other_shape):
    vectors, partners = templates(weights,other_weights,shape,other_shape)
    common = vectors.shape[1]-len(graph)
    core = np.array([[(mask>>j)&1 for j in range(len(graph))] for mask in graph],dtype=np.int16)
    outputs = []
    for mask,d in (profiles if common else [(0,0)]):
        if common:
            col = np.array([(mask>>j)&1 for j in range(len(graph))],dtype=np.int16)
            matrix = np.zeros((len(graph)+1,len(graph)+1),dtype=np.int16)
            matrix[:-1,:-1]=core;matrix[-1,:-1]=col;matrix[:-1,-1]=col
        else: matrix=core
        keep = np.ones(len(vectors),dtype=bool)
        for x,sh in ((vectors,shape),(partners,other_shape)):
            norm = 3*np.sum(x*x,axis=1)+((sh[0]-sh[1])//3)**2-np.sum((x@matrix)*x,axis=1)
            keep &= norm==8
            if sh==(6,3):
                pos=(x==1).astype(np.int16)
                keep &= np.sum((pos@matrix)*pos,axis=1)<=16
        outputs.append((d,int(np.count_nonzero(keep))))
    return outputs


def external_profiles(graph, weights, other_weights):
    n=len(weights);m=len(other_weights)
    left=[g&((1<<n)-1) for g in graph[:n]]
    right=[g>>n for g in graph[n:]]
    choices=[]
    for adj,ww in ((left,weights),(right,other_weights)):
        choices.append([(mask,sum(ww[i] for i in range(len(ww)) if mask>>i&1))
                        for mask in range(1<<len(ww)) if admissible(extend(adj,[mask],0))])
    return [(a|(b<<n),d) for a,d in choices[0] for b,dd in choices[1]
            if d==dd and admissible(extend(graph,[a|(b<<n)],0))]


def moment_bound(maxima, number, first, second):
    degrees=sorted(maxima)
    best=F(0);witness=None
    # Vertices of the three-equality moment polytope have at most three entries.
    for chosen in combinations(degrees,min(3,len(degrees))):
        a=Matrix([[1 for d in chosen],list(chosen),[d*d for d in chosen]])
        try: x,free=a.gauss_jordan_solve(Matrix([number,first,second]))
        except ValueError:continue
        if free:continue
        if any(v<0 for v in x):continue
        value=sum(F(v)*maxima[d] for d,v in zip(chosen,x))
        if value>=best:best=value;witness={str(d):str(v) for d,v in zip(chosen,x)}
    assert witness is not None
    return best,witness


def one_pair(left,right,weights,other_weights,cross,mass):
    graph=pair_graph(left,right,cross)
    if not admissible(graph):return None
    n=len(left);delta=weights+[-x for x in other_weights]
    assert all(sum(delta[j] for j in range(len(graph)) if graph[i]>>j&1)==3*delta[i] for i in range(len(graph)))
    profiles=external_profiles(graph,weights,other_weights)
    if mass==7:
        channels=[((6,3),(5,2)),((6,3),(4,1))]
    else: channels=[((6,3),(6,3)),((6,3),(5,2)),((4,4),(4,4))]
    maxima=defaultdict(int);constant=0;breakdown={}
    for sh,other in channels:
        variants=[(graph,profiles,weights,other_weights)]
        if sh!=other:
            rg=pair_graph(right,left,[(v,u) for u,v in cross])
            rp=[((mask>>n)|((mask&((1<<n)-1))<<len(right)),d) for mask,d in profiles]
            variants.append((rg,rp,other_weights,weights))
        # Counts in both orientations refer to the same exterior masks.
        total=None
        for gr,pr,w,ww in variants:
            costs=counts(gr,pr,w,ww,sh,other)
            if total is None: total=costs
            else:total=[(d,c+cc) for (d,c),(dd,cc) in zip(total,costs)]
        factor=1 if sh[0]==sh[1] else 2
        common=(sum(sh)+sum(other)-2*mass)//2
        if common:
            for d,c in total:maxima[d]=max(maxima[d],factor*c)
            breakdown[str((sh,other))]={'max_cost_by_degree':dict(maxima)}
        else:
            constant+=factor*total[0][1]
            breakdown[str((sh,other))]={'constant':factor*total[0][1]}
    if mass==7:first,second=75,89  # 17 degree zero, 61 degree one, 7 degree two
    else:first,second=(88,128) if not cross else (84,110)
    extra,witness=moment_bound(maxima,99-len(graph),first,second)
    return {'constant':constant,'max_cost_by_degree':dict(maxima),
            'moment_bound':str(extra),'moment_witness':witness,
            'total_bound':str(constant+extra),'breakdown':breakdown}


def main():
    stages=json.loads((ROOT/'data/codex_census_validation_99.json').read_text())['stages']
    seven=next(s for s in stages if s['order']==7)
    eight=next(s for s in stages if s['order']==8)
    d=next(r for r in seven['counts'] if min(r['degrees'])>=3)
    centre=next(i for i,x in enumerate(d['adjacency_bits']) if x.bit_count()==4)
    mass7=one_pair(d['adjacency_bits'],d['adjacency_bits'],[1]*7,[1]*7,[(centre,centre)],7)
    types=[]
    for row in eight['counts']:
        if min(row['degrees'])>=3 and row['edges']<14:
            types.append({'code':row['code'],'adj':row['adjacency_bits'],'weights':[1]*8})
    mill=next(r for r in seven['counts'] if r['code']==1723696)
    weights=[1]*7;weights[next(i for i,x in enumerate(mill['adjacency_bits']) if x.bit_count()==6)]=2
    types.append({'code':'weighted_mill','adj':mill['adjacency_bits'],'weights':weights})
    pairs=[]
    for i,left in enumerate(types):
        for right in types[i:]:
            lu=[j for j,mask in enumerate(left['adj']) if sum(left['weights'][k] for k in range(len(left['adj'])) if mask>>k&1)>3*left['weights'][j]]
            ru=[j for j,mask in enumerate(right['adj']) if sum(right['weights'][k] for k in range(len(right['adj'])) if mask>>k&1)>3*right['weights'][j]]
            if len(lu)!=len(ru):continue
            for perm in permutations(ru):
                out=one_pair(left['adj'],right['adj'],left['weights'],right['weights'],list(zip(lu,perm)),8)
                if out is not None:pairs.append({'left':left['code'],'right':right['code'],'cross':list(zip(lu,perm)),**out})
    coeffs={str(t['code']):str(2*max(F(p['total_bound']) for p in pairs if t['code'] in (p['left'],p['right']))) for t in types}
    report={'scope':__doc__,'mass7_new_cross_channels':mass7,
            'mass7_total_coefficient_Omega':str(F(mass7['total_bound'])+3612+370),
            'mass8_pair_bounds':pairs,'mass8_linear_coefficients':coeffs,
            'weighted_mill_count':3465}
    (ROOT/'data/codex_small_collision_new_channels.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'mass7_new':mass7['total_bound'],'mass7_total':report['mass7_total_coefficient_Omega'],
                      'mass8_coefficients':coeffs}))


if __name__=='__main__':main()
