"""New linear mass-nine collision bound, conditional on P=0.

For norm-eight (6,3) representatives with at most eight positive edges.
Uses the existing induced-graph census; does not repeat its construction.
Both signs are included. Other masses and sum changes are not bounded here.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
from math import ceil

import numpy as np
from scipy.optimize import linprog

from higher_census_minima import ROOT


def edge_count(adj, vertices):
    mask = sum(1 << v for v in vertices)
    return sum((adj[v] & mask).bit_count() for v in vertices)//2


def has_prism(adj):
    return any(all((adj[v] & sum(1 << w for w in chosen)).bit_count() == 3
                   for v in chosen) for chosen in combinations(range(len(adj)), 6))


def main():
    census = json.loads((ROOT/'data/codex_census_validation_99.json').read_text())['stages'][-1]
    rows = []
    for row in census['counts']:
        if min(row['degrees']) < 3 or has_prism(row['adjacency_bits']):
            continue
        adj = row['adjacency_bits']
        partitions = Counter()
        for negative in combinations(range(9), 3):
            positive = set(range(9))-set(negative)
            key = edge_count(adj, positive), edge_count(adj, negative)
            if key[0] in (7, 8) and key[1] in (2, 3):
                partitions[key] += 1
        # Deleting the two common vertices of an intersecting pair leaves D.
        deletions = 0
        for deleted in combinations(range(9), 2):
            keep = set(range(9))-set(deleted)
            mask = sum(1 << v for v in keep)
            if min((adj[v]&mask).bit_count() for v in keep) >= 3:
                deletions += 1
        e = row['edges']
        assert e in (14, 15, 16)
        k = F(4 if e < 16 else 2)
        a, b, c, d = [partitions[x] for x in ((7,2),(7,3),(8,2),(8,3))]
        weight = F(a)/k+b+c+k*d
        rows.append({'code': row['code'], 'edges': e,
                     'partition_counts_A_B_C_D': [a,b,c,d],
                     'weight_k': str(k), 'weight': str(weight),
                     'D_deletions': deletions})
    maxima = {e: max(F(r['weight']) for r in rows if r['edges'] == e) for e in (14,15,16)}
    for row in rows:
        a = F(162-11*(2*row['edges']-27),77)
        w = F(row['weight'])
        # Weighted positivity of E_3; overlap one has nonpositive coefficient.
        # At overlap two, each deletion has at most two other D partners.
        coefficient = (9-a)/a*w*w + 2*(2-a)/a*row['D_deletions']*w*maxima[row['edges']]
        if row['edges'] == 14:
            # These supports are disjoint within each projection class;
            # their unique degree-four vertices form a clique, of size <=3.
            assert row['D_deletions'] == 0
            coefficient = min(coefficient, 2*w*w)
            row['bound_method'] = 'disjoint classes of size at most three'
        else:
            row['bound_method'] = 'weighted projector positivity and D deletions'
        row['rational_coefficient'] = str(coefficient)
        row['integer_coefficient'] = ceil(coefficient)

    source = json.loads((ROOT/'data/codex_order9_census.json').read_text())
    affines = {r['code']: list(map(F,r['affine'])) for r in source['counts']}
    objective = [sum(r['integer_coefficient']*affines[r['code']][i] for r in rows)
                 for i in range(len(source['parameters'])+1)]
    matrix = np.array([list(map(float,v)) for v in affines.values()])
    scale = np.maximum(1, np.maximum(abs(matrix[:,0]), np.max(abs(matrix[:,1:])*1e6, axis=1)))
    obj = np.array(list(map(float,objective)))
    bounds = [(0,None)]*len(source['parameters'])
    bounds[source['parameters'].index('P')] = (0,0)
    oscale = max(abs(obj[0]),np.max(abs(obj[1:])*1e6),1)
    result = linprog(-obj[1:]*1e6/oscale, A_ub=-matrix[:,1:]*1e6/scale[:,None],
                     b_ub=matrix[:,0]/scale,bounds=bounds,method='highs')
    discovery = {'status': result.message, 'certified': False}
    if result.success:
        discovery['upper_bound_float'] = float(obj[0]-result.fun*oscale)
    report = {'scope': __doc__, 'type_count': len(rows), 'coefficients': rows,
              'linear_bound': 'sum(integer_coefficient * C_code), conditional on P=0',
              'affine_parameters': source['parameters'], 'affine_objective': list(map(str,objective)),
              'order9_LP_discovery_only': discovery}
    (ROOT/'data/codex_mass9_prismfree_collision_bound.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'type_count':len(rows),'max_coefficient':max(r['integer_coefficient'] for r in rows),
                      'LP_discovery_only':discovery}))


if __name__ == '__main__':
    main()
