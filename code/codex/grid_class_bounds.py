"""Exact grid-class twin cap and its norm-six shell consequence (note 194).

The geometry is proved in the note. This script checks the small graph
inequality, the H(3,3) obstruction, and every rational census certificate.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
import json
import sys

from higher_census_minima import ROOT, certify


def finite_checks():
    # Necessary degree conditions suffice for the inequality; no graph atlas
    # or numerical graph enumeration is used as a premise.
    counts = Counter(); maxima = {}
    for degrees in combinations_with_replacement((0,1,2,3,4,6),7):
        if sum(degrees) % 2 or sum(degrees) > 34: continue
        universals = degrees.count(6)
        if any(d < universals for d in degrees if d != 6): continue
        assert universals <= 3
        e = sum(degrees)//2; c = sum(d*(d-1)//2 for d in degrees)
        assert c <= (universals+3)*e-universals*(universals+8)
        assert 17*c <= 69*e
        counts[universals] += 1
        maxima[e] = max(maxima.get(e,0),c)
    # The sharp degree pattern is realised by K7 with a four-cycle deleted.
    edges = {(i,j) for i,j in combinations(range(7),2)}-{(0,1),(1,2),(2,3),(0,3)}
    ds = [sum(i in edge for edge in edges) for i in range(7)]
    assert sorted(ds) == [4]*4+[6]*3
    assert len(edges) == 17 and sum(d*(d-1)//2 for d in ds) == 69

    cube = list(product(range(3),repeat=3))
    distance = lambda x,y: sum(a != b for a,b in zip(x,y))
    adj = [sum(1 << j for j,y in enumerate(cube) if distance(x,y) == 1) for x in cube]
    assert all(row.bit_count() == 6 for row in adj)
    for i,j in combinations(range(27),2):
        common = (adj[i]&adj[j]).bit_count()
        assert common == {1:1,2:2,3:0}[distance(cube[i],cube[j])]
    diagonals = [triple for triple in combinations(range(27),3)
                 if all(distance(cube[i],cube[j]) == 3 for i,j in combinations(triple,2))]
    assert len(diagonals) == 36
    assert 27*(14-6) == (99-27)*3 and 99-27 > len(diagonals)

    # Three pairwise grids at a root have a locally admissible 19-point union.
    # This fixture is NOT an ambient completion or a proof that Xi has triangles.
    keep = [i for i,x in enumerate(cube) if sum(bool(a) for a in x) <= 2]
    union = [sum(1 << b for b,j in enumerate(keep) if adj[i] >> j & 1) for i in keep]
    assert len(union) == 19
    assert all((union[i]&union[j]).bit_count() <= (1 if union[i] >> j & 1 else 2)
               for i,j in combinations(range(19),2))
    return {'necessary_degree_vectors_checked':sum(counts.values()),
            'degree_vector_counts_by_universal_vertices':dict(counts),
            'sharp_graph_degrees':sorted(ds),'sharp_edge_count':17,'sharp_cherries':69,
            'H33_vertices':27,'H33_diagonal_triples':36,'H33_required_outside_vertices':72,
            'three_grid_union_vertices':19,'three_grid_union_adjacency_bits':union}


def systems():
    data = json.loads((ROOT/'data/codex_order9_census.json').read_text())
    raw = json.loads((ROOT/'data/codex_order9_raw_family_minima.json').read_text())
    rows = [(str(r['code']),list(map(F,r['affine']))) for r in data['counts']]
    width = len(data['parameters'])+1
    P = [F(0),F(1)]+[F(0)]*(width-2)
    rho = dict(rows)['13262907120']
    N4 = list(map(F,raw['Q4_edges9_3_cross0']['objective']))
    new = [17*x+105*y for x,y in zip(P,rho)]+[F(-17)]
    twins = [(name,row+[F(0)]) for name,row in rows]
    twins += [('tau>=0',[F(0)]*width+[F(1)]),
              ('2tau<=5P',[5*x for x in P]+[F(-2)]),
              ('tau<=2P+3rho',[2*x+3*y for x,y in zip(P,rho)]+[F(-1)]),
              ('8tau<=N4',N4+[F(-8)]),('17tau<=17P+105rho',new)]
    old = json.loads((ROOT/'data/codex_far_triangle_shell_bound.json').read_text())
    shell = [(name,row+[F(0),F(0)]) for name,row in rows]
    shell += [(name,list(map(F,row))) for name,row in old['additional_rows']]
    shell += [('17tau<=17P+105rho',new+[F(0)])]
    return data,twins,shell


def verify(rows,objective,proof):
    lookup = dict(rows); identity = [F(0)]*len(objective)
    for name,w in proof['certificate']:
        w = F(w); assert w >= 0
        identity = [a+w*b for a,b in zip(identity,lookup[name])]
    assert identity[1:] == objective[1:]
    assert objective[0]-identity[0] == F(proof['lower_bound'])
    assert proof['objective'] == list(map(str,objective))
    assert proof['verified_identity_coefficients'] == list(map(str,identity))
    point = list(map(F,proof['rational_point_attaining_bound']))
    assert all(row[0]+sum(a*b for a,b in zip(row[1:],point)) >= 0 for _,row in rows)
    assert objective[0]+sum(a*b for a,b in zip(objective[1:],point)) == F(proof['lower_bound'])


def main():
    verify_only = '--verify-only' in sys.argv
    small = finite_checks()
    smallpath = ROOT/'data/codex_grid_class_finite_checks.json'
    if verify_only: assert json.loads(smallpath.read_text()) == json.loads(json.dumps(small))
    else: smallpath.write_text(json.dumps(small,indent=2)+'\n')
    data,twins,shell = systems()
    width = len(data['parameters'])+1
    cases = [('twin_cap',twins,[F(0)]*width+[F(-1)],data['parameters']+['tau']),
             ('b3_bound',shell,[F(0)]*(width+1)+[F(1)],data['parameters']+['tau','b3'])]
    for name,rows,objective,parameters in cases:
        path = ROOT/f'data/codex_grid_class_{name}.json'
        if verify_only: proof = json.loads(path.read_text())
        else:
            proof = certify(rows,objective)
            proof.update(objective=list(map(str,objective)),parameters=parameters,
                         scope='Exact order-nine census certificate using the grid class theorem and g(v)<=17.')
            path.write_text(json.dumps(proof,indent=2)+'\n')
        verify(rows,objective,proof)
        assert F(proof['lower_bound']) == (F(-26082,17) if name == 'twin_cap' else F(778008,17))
        print('Verified',name,proof['lower_bound'],'with',len(proof['certificate']),'nonnegative rational weights',flush=True)
    print('Integer consequences: tau <=1534; b3 >=45766. H(3,3) cannot be induced. No rank exclusion.')


if __name__ == '__main__':
    main()
