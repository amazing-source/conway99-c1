"""Combine pencil-specific binary mass-six costs with exact grid moments."""
from fractions import Fraction as F
from math import comb
import argparse
import gzip
import json

from higher_census_minima import ROOT
from grid_neighbour_moment_bounds import profiles,model,discover,exact_bound


def read(name):
    with gzip.open(ROOT/f'data/{name}.json.gz','rt') as stream:return json.load(stream)


def main(verify_only=False):
    costs={m:read(f'codex_pencil_{m}_collision_bounds')['results']['all_including90']['even_upper_bound']
           for m in (2,3,4,6)}
    nongrid=read('codex_grid_pair_collisions_all_nongrid')['results']['all_including90']['even_integer_upper_bound']
    assert costs=={2:29144,3:29142,4:29140,6:29140} and nongrid==31976
    degrees,grouped=profiles();weighted={}
    for ds in degrees:
        key=(sum(ds)//2,sum(comb(d,2) for d in ds),sum(d>=2 for d in ds))
        weight=sum(comb(d,2)*costs[d] for d in ds if d>=2)
        weighted[key]=max(weighted.get(key,0),weight)
    path=ROOT/'data/codex_pencil_weighted_moments.json.gz'
    if verify_only:
        with gzip.open(path,'rt') as stream:report=json.load(stream)
        assert report['costs']=={str(m):c for m,c in costs.items()}
        assert report['nongrid_cost']==nongrid
    else:
        report={'costs':costs,'nongrid_cost':nongrid,'cases':{},
                'scope':'Upper bound for binary mass-six same-sum collisions only, all note195 families including90, with positive63 supports e(W)<=8.'}
    maxima=[]
    for s in range(74):
        types,rows,caps,_=model(s,grouped)
        weights=[weighted[(e,c,h)] for e,c,h in grouped
                 for d in range(min(s-int(e>=14),14 if e>=14 else 2*h)+1)]
        assert len(weights)==len(types)
        n=len(types)
        # Keep the actual number of non-grid twin pairs as a variable, so
        # the integral twin cap is retained alongside the prism-class bound.
        rows=[(name,c,a+[F(0)]) for name,c,a in rows]
        caps=caps+[852]
        rows += [
            ('nongrid_twins<=P-6rho',F(0),[F(0)]*n+[F(1),F(-6),F(-1)]),
            ('integral_total_twin_cap',F(1403),[-F(t[2],3) for t in types]+[F(0),F(0),F(-1)]),
            ('integral_grid_twin_cut',F(17),[-F(t[2],3) for t in types]+[F(0),F(11),F(0)])]
        objective=[-F(w,3) for w in weights]+[F(0),F(0),F(-nongrid)]
        proof=report['cases'][str(s)] if verify_only else discover(rows,caps,objective)
        assert not proof['infeasible']
        if not verify_only:
            simpler=[(name,str(F(w).limit_denominator(10000))) for name,w in proof['weights']]
            lower=exact_bound(rows,caps,objective,simpler)
            if lower>=F(proof['lower_bound']):
                proof['weights']=simpler;proof['lower_bound']=str(lower)
        bound=exact_bound(rows,caps,objective,proof['weights'])
        assert bound==F(proof['lower_bound'])
        maxima.append((-bound,s))
        if not verify_only:report['cases'][str(s)]=proof
    maximum,s=max(maxima)
    summary={'rational_upper_bound':str(maximum),'even_integer_upper_bound':int(2*(maximum//2)),
             'maximising_size':s,'cases_verified':74}
    if verify_only:assert report['summary']==summary
    else:
        report['summary']=summary
        with gzip.GzipFile(filename=path,mode='wb',mtime=0) as stream:
            stream.write(json.dumps(report).encode())
    print('Verified weighted collision upper bound:',summary,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true')
    main(parser.parse_args().verify_only)
