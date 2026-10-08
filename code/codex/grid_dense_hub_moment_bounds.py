"""Exact consequences of the note203 dense-hub exclusion, for rank_7>=37.

Refine note196 profiles by u6, the number of incident six-grid lines.
Certify all 74 neighbour-moment models with 2*n1+n2-3*n3>=0.
Floating optimization only discovers weights; verification uses Fractions.
"""
from fractions import Fraction as F
from math import comb, floor
import argparse
import gzip
import json

from higher_census_minima import ROOT, certify
from grid_neighbour_moment_bounds import profiles, model, census_cut, discover, exact_bound
from grid_class_bounds import systems, verify as verify_shell


def read(name):
    with gzip.open(ROOT / f'data/{name}.json.gz', 'rt') as stream:
        return json.load(stream)


def refined_profiles():
    degrees, _ = profiles()
    grouped = sorted({(sum(ds)//2, sum(comb(d, 2) for d in ds),
                       sum(d >= 2 for d in ds), ds.count(6)) for ds in degrees})
    assert len(degrees) == 179 and len(grouped) == 177
    assert all(u <= 3 for _, _, _, u in grouped)
    return degrees, grouped


def refined_model(s, grouped):
    # Preserve repeated (e,c,h2) entries when their u6 values differ.
    types, rows, caps, objective = model(s, [g[:3] for g in grouped])
    expanded = [(e, c, h, u, d) for e, c, h, u in grouped
                for d in range(min(s-int(e >= 14), 14 if e >= 14 else 2*h)+1)]
    assert types == [(int(e >= 14), e, c, d) for e, c, _, _, d in expanded]
    rows.append(('dense_hub_incidence_cut', F(0),
                 [F(2*(u == 1)+(u == 2)-3*(u == 3)) for _, _, _, u, _ in expanded]
                 + [F(0), F(0)]))
    return types, expanded, rows, caps, objective


def finite_bound(verify_only, kind, tau_cap=None):
    degrees, grouped = refined_profiles()
    costs = {m: read(f'codex_pencil_{m}_degree_moments')['results']['all_including90']['even_upper_bound']
             for m in (2, 3, 4, 6)} if kind == 'weighted' else {}
    weighted = {}
    if kind == 'weighted':
        assert costs == {2: 27828, 3: 27818, 4: 27810, 6: 27798}
        nongrid = read('codex_grid_pair_collisions_all_nongrid')['results']['all_including90']['even_integer_upper_bound']
        assert nongrid == 31976 and tau_cap == 1354
        for ds in degrees:
            key = (sum(ds)//2, sum(comb(d, 2) for d in ds), sum(d >= 2 for d in ds), ds.count(6))
            value = sum(comb(d, 2)*costs[d] for d in ds if d >= 2)
            weighted[key] = max(weighted.get(key, 0), value)
    path = ROOT / f'data/codex_dense_hub_{kind}_moments.json.gz'
    if verify_only:
        with gzip.open(path, 'rt') as stream:
            report = json.load(stream)
        assert report['degree_vectors'] == list(map(list, degrees))
        assert report['profiles'] == list(map(list, grouped))
        assert report['rank_scope'] == 'r>=37'
        assert report['objective'] == kind
    else:
        report = {'rank_scope': 'r>=37', 'degree_vectors': degrees, 'profiles': grouped,
                  'objective': kind, 'cases': {}}
    maxima = []
    for s in range(74):
        types, expanded, rows, caps, objective = refined_model(s, grouped)
        if kind == 'weighted':
            n = len(types)
            rows = [(name, c, a+[F(0)]) for name, c, a in rows]
            caps = caps+[852]
            rows += [
                ('nongrid_twins<=P-6rho', F(0), [F(0)]*n+[F(1), F(-6), F(-1)]),
                ('integral_total_twin_cap', F(tau_cap), [-F(t[2], 3) for t in types]+[F(0), F(0), F(-1)]),
                ('integral_grid_twin_cut', F(17), [-F(t[2], 3) for t in types]+[F(0), F(11), F(0)])]
            objective = [-F(weighted[(e, c, h, u)], 3) for e, c, h, u, _ in expanded]+[F(0), F(0), F(-nongrid)]
        proof = report['cases'][str(s)] if verify_only else discover(rows, caps, objective)
        if proof['infeasible']:
            rows = [(name, c, a+[F(1)]) for name, c, a in rows]
            caps = caps+[10**6]
            objective = [F(0)]*(len(caps)-1)+[F(1)]
        if not verify_only:
            simpler = [(name, str(F(w).limit_denominator(10000))) for name, w in proof['weights']]
            lower = exact_bound(rows, caps, objective, simpler)
            if lower >= F(proof['lower_bound']):
                proof['weights'], proof['lower_bound'] = simpler, str(lower)
        bound = exact_bound(rows, caps, objective, proof['weights'])
        assert bound == F(proof['lower_bound'])
        if proof['infeasible']:
            assert bound > 0
        else:
            maxima.append((-bound, s))
        if not verify_only:
            report['cases'][str(s)] = proof
        if s % 20 == 0:
            print('Verified', kind, 's=', s, flush=True)
    maximum, s = max(maxima)
    summary = {'rational_upper_bound': str(maximum), 'integer_upper_bound': floor(maximum),
               'maximising_size': s, 'feasible_sizes': len(maxima), 'infeasible_sizes': 74-len(maxima)}
    if kind == 'weighted':
        summary['even_integer_upper_bound'] = int(2*(maximum//2))
    if verify_only:
        assert report['summary'] == summary
    else:
        report['summary'] = summary
        with gzip.GzipFile(filename=path, mode='wb', mtime=0) as stream:
            stream.write(json.dumps(report).encode())
    print('Verified all 74 cases for', kind, summary, flush=True)
    return summary


def shell_bound(verify_only, tau_cap):
    source, _, rows = systems()
    width = len(source['parameters'])+1
    rows += [(f'dense_hub_tau<={tau_cap}', [F(tau_cap)]+[F(0)]*(width-1)+[F(-1), F(0)])]
    objective = [F(0)]*(width+1)+[F(1)]
    path = ROOT / 'data/codex_dense_hub_b3_bound.json'
    if verify_only:
        proof = json.loads(path.read_text())
    else:
        proof = certify(rows, objective)
        proof.update(objective=list(map(str, objective)), tau_cap=tau_cap, rank_scope='r>=37',
                     b3_even_floor=int(-2*((-F(proof['lower_bound']))//2)))
        path.write_text(json.dumps(proof, indent=2)+'\n')
    verify_shell(rows, objective, proof)
    assert proof['tau_cap'] == tau_cap and proof['rank_scope'] == 'r>=37'
    assert proof['b3_even_floor'] == int(-2*((-F(proof['lower_bound']))//2))
    print('Verified b3 >=', proof['lower_bound'], 'hence', proof['b3_even_floor'], flush=True)
    return proof['b3_even_floor']


def main(verify_only=False):
    census_cut(verify_only=True)
    tau = finite_bound(verify_only, 'tau')['integer_upper_bound']
    assert tau == 1354
    finite_bound(verify_only, 'weighted', tau)
    assert shell_bound(verify_only, tau) == 45964


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    main(parser.parse_args().verify_only)
