"""Rational bounds for F0 collisions with binary twin-prism differences."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import comb
from collections import Counter
import argparse
import gzip
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, hstack, vstack

from higher_census_minima import ROOT
from six_three_mass6_profile_lp import build, certificate


def pair_model(data):
    profiles, graph = data['profiles'], data['core_adjacency']
    pairs = [(i,j) for i,j in combinations_with_replacement(range(len(profiles)),2)
             if i != j or profiles[i][1] >= 2]
    index = {pair:j for j,pair in enumerate(pairs)}
    caps = [profiles[i][1]*profiles[j][1] if i != j else comb(profiles[i][1],2) for i,j in pairs]
    rows = []
    def eq(name, constant, coeff):
        coeff = {j:int(c) for j,c in coeff.items() if c}
        rows.append((name+'+',int(constant),coeff))
        rows.append((name+'-',-int(constant),{j:-c for j,c in coeff.items()}))
    for i,(mask,count) in enumerate(profiles):
        regularity = {index[tuple(sorted((i,j)))]: 2 if i == j else 1
                      for j in range(len(profiles)) if tuple(sorted((i,j))) in index}
        eq(f'degree_{i}',-count*(14-mask.bit_count()),regularity)
        for u in range(12):
            target = (1 if mask >> u & 1 else 2)-(graph[u]&mask).bit_count()
            coeff = {j:c for j,c in regularity.items()
                     if profiles[pairs[j][1] if pairs[j][0] == i else pairs[j][0]][0] >> u & 1}
            eq(f'common_core_{i}_{u}',-count*target,coeff)
    costs = {(tuple(row['profiles']),row['edges']):row['counts']['F0'] for row in data['patterns']}
    offset, objective = 0, []
    for j,pair in enumerate(pairs):
        zero,one = costs.get((pair,0)),costs.get((pair,1))
        assert zero is not None or one is not None
        if zero is None:
            eq(f'forced_edge_{pair}',-caps[j],{j:1}); zero = 0
        if one is None:
            eq(f'forbidden_edge_{pair}',0,{j:1}); one = 0
        offset += caps[j]*zero
        objective.append(zero-one)  # negative collision objective
    rr,cc,values = [],[],[]
    for i,(_,_,coeff) in enumerate(rows):
        for j,c in coeff.items(): rr.append(i); cc.append(j); values.append(c)
    matrix = coo_matrix((values,(rr,cc)),shape=(len(rows),len(caps))).tocsr()
    return pairs,caps,rows,matrix,np.array([c for _,c,_ in rows],dtype=float),offset,objective


def verify(rows,caps,objective,proof):
    indices = {name:i for i,(name,_,_) in enumerate(rows)}
    residual = list(map(F,objective)); constant = F(0)
    for name,w in proof['row_weights']:
        w = F(w); assert w >= 0
        _,c,coeff = rows[indices[name]]; constant += w*c
        for j,a in coeff.items(): residual[j] -= w*a
    correction = sum(r*cap for r,cap in zip(residual,caps) if r < 0)
    assert constant-correction == F(proof['collision_upper_bound'])
    assert {str(j):str(r) for j,r in enumerate(residual) if r} == proof['residual_coefficients']
    assert str(constant) == proof['weighted_constant'] and str(correction) == proof['bound_correction']
    assert 2*((constant-correction)//2) == proof['even_integer_upper_bound']


def run(p,verify_only=False,triangle_free=False,positive_type=None,joint=False):
    suffix = "_tf" if triangle_free else ""
    if positive_type is not None:
        assert triangle_free
        suffix += f"_{positive_type}"
    start = time.monotonic()
    with gzip.open(ROOT/f'data/codex_f0_mass6_p{p}{suffix}_patterns.json.gz','rt') as stream:
        data = json.load(stream)
    assert not joint or p == 6
    path = ROOT/f'data/codex_f0_mass6_p{p}{suffix}{"_joint" if joint else ""}_bound.json'
    if p >= 5:
        path = path.with_suffix('.json.gz')
    if p < 5:
        count = 0
        for row in data['patterns']:
            capacity = 1
            for i,n in Counter(row['profiles']).items(): capacity *= comb(data['profiles'][i][1],n)
            count += capacity*row['counts']['F0']
        report = {'exact_collision_count_per_twin_pair':count,'scope':'Both signs; F0 versus all norm-eight representatives of the indicated family.'}
        if verify_only: assert json.loads(path.read_text()) == report
        else: path.write_text(json.dumps(report,indent=2)+'\n')
        print(p,report,flush=True); return
    if p == 5:
        pairs,caps,rows,matrix,constants,offset,objective = pair_model(data)
    else:
        pairs,caps,rows,matrix,constants = build(data)
        offset = 0
        objective = [0]*len(pairs)+[-row['counts']['F0'] for row in data['patterns']]
        if joint:
            with gzip.open(ROOT/f'data/codex_f0_mass6_p5{suffix}_patterns.json.gz','rt') as stream:
                cross = json.load(stream)
            pp,pc,pr,pm,pconst,offset,po = pair_model(cross)
            assert pairs == pp and caps[:len(pp)] == pc
            objective[:len(pp)] = po
            chosen = [i for i,(name,_,_) in enumerate(pr) if name.startswith(('forced_','forbidden_'))]
            matrix = vstack((matrix,hstack((pm[chosen],coo_matrix((len(chosen),len(caps)-len(pp))))))).tocsr()
            rows += [pr[i] for i in chosen]
            constants = np.concatenate((constants,pconst[chosen]))
            with gzip.open(ROOT/f'data/codex_f0_mass6_p4{suffix}_patterns.json.gz','rt') as stream:
                small = json.load(stream)
            offset += sum(small['profiles'][r['profiles'][0]][1]*r['counts']['F0'] for r in small['patterns'])
    if verify_only:
        with gzip.open(path,'rt') as stream:
            report = json.load(stream)
    else:
        print('Solving p=',p,'with',len(caps),'variables',flush=True)
        result = linprog(np.array(objective,dtype=float),A_ub=-matrix,b_ub=constants,
                         bounds=list(zip([0]*len(caps),caps)),method='highs-ipm')
        assert result.success,result.message
        proof = certificate(rows,caps,objective,result)
        report = {'variables':len(caps),'rows':len(rows),'objective_constant':offset,
                  'certificate':proof,'collision_upper_bound':str(F(proof['collision_upper_bound'])+offset),
                  'even_integer_upper_bound':2*((F(proof['collision_upper_bound'])+offset)//2),
                  'scope':'Both signs; binary mass-six collisions only.', 'joint_with_old_families':joint}
        report['even_integer_upper_bound'] = int(report['even_integer_upper_bound'])
        with gzip.GzipFile(filename=path,mode='wb',mtime=0) as stream:
            stream.write(json.dumps(report).encode())
    verify(rows,caps,objective,report['certificate'])
    assert report['objective_constant'] == offset
    assert F(report['collision_upper_bound']) == F(report['certificate']['collision_upper_bound'])+offset
    assert report['even_integer_upper_bound'] == 2*(F(report['collision_upper_bound'])//2)
    print('Verified p=',p,'bound',report['even_integer_upper_bound'],'rational',report['collision_upper_bound'],
          'seconds',round(time.monotonic()-start,1),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--p',type=int,choices=(3,4,5,6),required=True)
    parser.add_argument('--verify-only',action='store_true')
    parser.add_argument('--triangle-free',action='store_true')
    parser.add_argument('--positive-type',type=int,choices=(7064,21812))
    parser.add_argument('--joint',action='store_true')
    args = parser.parse_args(); run(args.p,args.verify_only,args.triangle_free,args.positive_type,args.joint)
