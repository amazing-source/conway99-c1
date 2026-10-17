"""Classify the ten positive F0 types and certify the triangle-free raw count."""
from fractions import Fraction as F
from itertools import combinations
import json
import sys

from higher_census_minima import ROOT, certify
from higher_vertex_census import ir_orders
from seven_vertex_census import decode


def main():
    data = json.loads((ROOT/'data/codex_order9_census.json').read_text())
    found = {}
    for row in data['counts']:
        if row['edges'] != 10: continue
        adj = decode(9,row['code'])
        for Y in combinations(range(9),3):
            mask = sum(1 << i for i in Y)
            if any(adj[i] != (mask ^ (1 << i)) for i in Y): continue
            W = [i for i in range(9) if i not in Y]
            sub = tuple(sum(((adj[i] >> j) & 1) << b for b,j in enumerate(W)) for i in W)
            key = ir_orders(sub)[0]
            assert str(key) not in found  # One isolated triangle in each graph.
            tri = sum(bool(sub[i] >> j & 1 and sub[i] >> k & 1 and sub[j] >> k & 1)
                      for i,j,k in combinations(range(6),3))
            four = 0
            for S in combinations(range(6),4):
                sm = sum(1 << i for i in S)
                four += all((sub[i] & sm).bit_count() == 2 for i in S)
            found[str(key)] = {'W':list(sub),'degrees':sorted(r.bit_count() for r in sub),
                              'triangles':tri,'fourcycles':four,'order9_code':row['code'],'affine':row['affine']}
    assert len(found) == 10
    chosen = [v for v in found.values() if not v['triangles']]
    assert len(chosen) == 2
    assert {v['order9_code'] for v in chosen} == {1292951744,35652125060}
    catalogue = {'types':found,'parameters':data['parameters'],
                 'scope':'Each order-nine count is unsigned F0 representatives of this W type.'}
    catpath = ROOT/'data/codex_f0_positive_types.json'
    certpath = ROOT/'data/codex_f0_triangle_free_raw_minimum.json'
    rows = [(str(r['code']),list(map(F,r['affine']))) for r in data['counts']]
    objective = [2*sum(F(v['affine'][j]) for v in chosen) for j in range(len(data['parameters'])+1)]
    if '--verify-only' in sys.argv:
        assert json.loads(catpath.read_text()) == catalogue
        proof = json.loads(certpath.read_text())
    else:
        proof = certify(rows,objective)
        proof.update(parameters=data['parameters'],objective=list(map(str,objective)),
                     scope='Raw signed representatives only. No collisions subtracted.')
        catpath.write_text(json.dumps(catalogue,indent=2)+'\n')
        certpath.write_text(json.dumps(proof,indent=2)+'\n')
    lookup = dict(rows); identity = [F(0)]*len(objective)
    for name,weight in proof['certificate']:
        weight = F(weight); assert weight >= 0
        identity = [a+weight*b for a,b in zip(identity,lookup[name])]
    assert identity[1:] == objective[1:]
    assert objective[0]-identity[0] == F(proof['lower_bound']) == 166320
    assert proof['objective'] == list(map(str,objective))
    point = list(map(F,proof['rational_point_attaining_bound']))
    assert all(row[0]+sum(a*b for a,b in zip(row[1:],point)) >= 0 for _,row in rows)
    assert objective[0]+sum(a*b for a,b in zip(objective[1:],point)) == 166320
    print('Ten F0 positive types; two triangle-free types; raw signed count >=166320, exact certificate and attaining census point verified.')


if __name__ == '__main__':
    main()
