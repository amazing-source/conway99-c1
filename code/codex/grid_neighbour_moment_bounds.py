"""Certify a twin-prism cap using neighbour moments of high-grid vertices.

S consists of vertices in at least fourteen grids. All incident lines at an
S vertex have grid multiplicity >=2. The necessary local degree profiles,
SRG neighbour moments, and all 74 possible values of |S| are checked exactly.
Floating LP solves discover certificates only; the verifier uses Fractions.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import floor
import argparse
import gzip
import json

import numpy as np
from scipy.optimize import linprog

from higher_census_minima import ROOT, certify


def profiles():
    degrees = []
    for ds in combinations_with_replacement((0,1,2,3,4,6),7):
        if sum(ds)%2 or sum(ds)>34: continue
        a = ds.count(6)
        if any(d<a for d in ds if d!=6): continue
        rev = ds[::-1]
        # For the k highest-degree vertices: at most k(k-1) internal
        # incidences, and at most min(k,d) from each remaining vertex.
        if any(sum(rev[:k]) > k*(k-1)+sum(min(k,d) for d in rev[k:])
               for k in range(1,8)): continue
        if sum(ds)>=28: assert min(ds)>=2
        degrees.append(ds)
    grouped = sorted({(sum(ds)//2,sum(d*(d-1)//2 for d in ds),sum(d>=2 for d in ds))
                      for ds in degrees})
    assert len(grouped) == 170
    # Expansion + grid incidence budget excludes every s>=74.
    assert all(14*s+F(11*s*(99-s),198)>1134 for s in range(74,100))
    return degrees,grouped


def census_cut(verify_only=False):
    source = json.loads((ROOT/'data/codex_order9_census.json').read_text())
    rows = [(str(r['code']),list(map(F,r['affine']))) for r in source['counts']]
    rho = dict(rows)['13262907120']; P = [F(0),F(1)]+[F(0)]*(len(rho)-2)
    objective = [-x-5*y for x,y in zip(P,rho)]
    path = ROOT/'data/codex_prism_plus_five_grids_cap.json'
    if verify_only: proof = json.loads(path.read_text())
    else:
        proof = certify(rows,objective)
        proof['objective'] = list(map(str,objective))
        path.write_text(json.dumps(proof,indent=2)+'\n')
    identity = [F(0)]*len(objective); lookup = dict(rows)
    for name,w in proof['certificate']:
        w = F(w); assert w>=0
        identity = [x+w*y for x,y in zip(identity,lookup[name])]
    assert identity[1:] == objective[1:]
    assert objective[0]-identity[0] == F(proof['lower_bound']) == -1386
    # Also recheck the two previously published caps used as finite bounds.
    dependencies = [
        (json.loads((ROOT/'data/codex_order9_prism_cap.json').read_text()),
         [-x for x in P],F(-11088,13)),
        (json.loads((ROOT/'data/codex_order9_geometry_caps.json').read_text())['rho'],
         [-x for x in rho],F(-126))]
    for dependency,target,bound in dependencies:
        total = [F(0)]*len(target)
        for name,w in dependency['certificate']:
            w = F(w); assert w>=0
            total = [x+w*y for x,y in zip(total,lookup[name])]
        assert total[1:] == target[1:] and target[0]-total[0] == bound
    assert floor(F(11088,13)) == 852
    print('Verified census cut: P+5rho<=1386',flush=True)


def model(s,grouped):
    types = [(int(e>=14),e,c,d) for e,c,h in grouped
             for d in range(min(s-int(e>=14),14 if e>=14 else 2*h)+1)]
    n = len(types); rows = []
    def equality(name,constant,coeff):
        rows.append((name+'+',F(-constant),list(map(F,coeff))))
        rows.append((name+'-',F(constant),[-F(x) for x in coeff]))
    equality('outside_count',99-s,[1-t[0] for t in types]+[0,0])
    equality('inside_count',s,[t[0] for t in types]+[0,0])
    equality('grid_incidence',0,[t[1] for t in types]+[0,-9])
    equality('neighbour_first_moment',14*s,[t[3] for t in types]+[0,0])
    equality('neighbour_second_moment',12*s+2*s*s,
             [t[3]**2+t[0]*t[3] for t in types]+[0,0])
    rows += [('P>=6rho',F(0),[F(0)]*n+[F(1),F(-6)]),
             ('P+5rho<=1386',F(1386),[F(0)]*n+[F(-1),F(-5)]),
             ('spectral_expansion',3*s+F(s*s,9),[-F(t[0]*t[3]) for t in types]+[F(0),F(0)])]
    caps = [99]*n+[852,126]
    objective = [-F(t[2],3) for t in types]+[F(-1),F(6)]
    return types,rows,caps,objective


def exact_bound(rows,caps,objective,weights):
    lookup = {name:(constant,coeff) for name,constant,coeff in rows}
    residual = list(objective); constant = F(0)
    for name,w in weights:
        w = F(w); assert w>=0
        c,a = lookup[name]; constant += w*c
        residual = [x-w*y for x,y in zip(residual,a)]
    correction = sum(x*u for x,u in zip(residual,caps) if x<0)
    return -constant+correction


def discover(rows,caps,objective):
    coeff = np.array([[float(x) for x in a] for _,_,a in rows])
    constants = np.array([float(c) for _,c,_ in rows])
    result = linprog(np.array(list(map(float,objective))),A_ub=-coeff,b_ub=constants,
                     bounds=list(zip([0]*len(caps),caps)),method='highs')
    infeasible = result.status == 2
    if infeasible:
        # A strictly positive lower bound for a common feasibility slack
        # excludes slack zero, hence excludes the original system.
        rows = [(name,c,a+[F(1)]) for name,c,a in rows]
        caps = caps+[10**6]; objective = [F(0)]*(len(caps)-1)+[F(1)]
        coeff = np.array([[float(x) for x in a] for _,_,a in rows])
        result = linprog(np.array(list(map(float,objective))),A_ub=-coeff,b_ub=constants,
                         bounds=list(zip([0]*len(caps),caps)),method='highs')
    assert result.success,result.message
    weights = [(rows[i][0],str(F(float(-w)).limit_denominator(10**9)))
               for i,w in enumerate(result.ineqlin.marginals) if w<0]
    lower = exact_bound(rows,caps,objective,weights)
    if infeasible: assert lower>0
    return {'infeasible':infeasible,'weights':weights,'lower_bound':str(lower),
            'numerical_discovery_value':float(result.fun)}


def main(verify_only=False):
    census_cut(verify_only)
    degrees,grouped = profiles()
    path = ROOT/'data/codex_grid_neighbour_moment_bounds.json.gz'
    if verify_only:
        with gzip.open(path,'rt') as stream: report = json.load(stream)
        assert report['degree_vectors'] == list(map(list,degrees))
        assert report['grouped_profiles'] == list(map(list,grouped))
    else:
        report = {'degree_vectors':degrees,'grouped_profiles':grouped,'cases':{},
                  'scope':'Exact rational upper certificates for tau; no graph attainment or rank exclusion claimed.'}
    maxima = []
    for s in range(74):
        types,rows,caps,objective = model(s,grouped)
        proof = report['cases'][str(s)] if verify_only else discover(rows,caps,objective)
        if proof['infeasible']:
            rows = [(name,c,a+[F(1)]) for name,c,a in rows]
            caps += [10**6]; objective = [F(0)]*(len(caps)-1)+[F(1)]
        bound = exact_bound(rows,caps,objective,proof['weights'])
        assert bound == F(proof['lower_bound'])
        if proof['infeasible']:
            assert bound>0
            print('Verified impossible high-grid size',s,flush=True)
        else: maxima.append((-bound,s))
        if not verify_only: report['cases'][str(s)] = proof
    maximum,s = max(maxima)
    summary = {'maximum_rational_upper_bound':str(maximum),'maximising_size':s,
               'integer_twin_cap':floor(maximum),
               'feasible_sizes':len(maxima),'infeasible_sizes':74-len(maxima)}
    if verify_only: assert report['summary'] == summary
    else:
        report['summary'] = summary
        with gzip.GzipFile(filename=path,mode='wb',mtime=0) as stream:
            stream.write(json.dumps(report).encode())
    print('Verified all 74 cases:',summary,flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only',action='store_true')
    main(parser.parse_args().verify_only)
