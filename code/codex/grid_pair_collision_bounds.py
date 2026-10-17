"""Split binary mass-six collision bounds by grid/non-grid twin prisms.

The core is the same labelled pair of prisms as in note 188.  Its three
singleton apex profiles form a triangle exactly in the grid case.  All
certificates are verified over Q with finite variable caps, independently
of the floating point optimisation.  This does not audit other masses.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
import gzip
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, hstack, vstack

from higher_census_minima import ROOT
from six_three_mass6_profile_lp import build, certificate
from f0_prism_bounds import pair_model, verify


def read_patterns(name):
    with gzip.open(ROOT / f'data/{name}.json.gz', 'rt') as stream:
        return json.load(stream)


def add_type(data, pairs, caps, rows, matrix, constants, kind):
    apex = [i for i, (mask, count) in enumerate(data['profiles'])
            if (mask & 63).bit_count() == 2]
    simple = [i for i, (mask, count) in enumerate(data['profiles'])
              if (mask & 63).bit_count() == 1]
    assert len(apex) == 3 and all(data['profiles'][i][1] == 1 for i in apex)
    indices = {pair: j for j, pair in enumerate(pairs)}
    extra = []
    if kind == 'grid':
        # A triangle of apices has no neighbours among the 60 simple profiles.
        # The latter also follows from the SRG identities, but stating it makes
        # the numerical problem smaller after presolve.
        for pair in combinations(apex, 2):
            extra.append((f'grid_apex_edge_{pair}', -1, {indices[pair]: 1}))
        for a in apex:
            for b in simple:
                pair = tuple(sorted((a, b)))
                extra.append((f'grid_no_apex_simple_edge_{pair}', 0,
                              {indices[pair]: -1}))
    elif kind == 'independent':
        extra.append(('independent_apex_edges_zero', 0,
                      {indices[pair]: -1 for pair in combinations(apex, 2)}))
    else:
        extra.append(('nongrid_apex_edges_at_most_two', 2,
                      {indices[pair]: -1 for pair in combinations(apex, 2)}))
    rr, cc, vv = [], [], []
    for r, (_, _, row) in enumerate(extra):
        for c, value in row.items():
            rr.append(r); cc.append(c); vv.append(value)
    addon = coo_matrix((vv, (rr, cc)), shape=(len(extra), len(caps))).tocsr()
    return rows + extra, vstack((matrix, addon)).tocsr(), np.concatenate(
        (constants, np.array([c for _, c, _ in extra], dtype=float)))


def model(family, kind):
    if family == 'all':
        packet = read_patterns('codex_mass6_family_patterns')['by_outside_size']
        data = packet['3']
        pairs, caps, rows, matrix, constants = build(data)
        objectives = {}
        for label in ('63_63', '90_90'):
            objectives[label] = (0, [0]*len(pairs)+[-r['counts'][label] for r in data['patterns']])
        for label in ('71_71', '63_52', '44_44'):
            small = packet['2']
            custom = dict(small, patterns=[dict(r, counts={'F0':r['counts'][label]})
                                          for r in small['patterns']])
            pp, pc, pr, pm, pconst, offset, po = pair_model(custom)
            assert pairs == pp and caps[:len(pp)] == pc
            objectives[label] = (offset, po+[0]*(len(caps)-len(pairs)))
            if label == '71_71':
                chosen = [i for i,(name,_,_) in enumerate(pr)
                          if name.startswith(('forced_','forbidden_'))]
                matrix = vstack((matrix, hstack((pm[chosen],
                    coo_matrix((len(chosen),len(caps)-len(pp))))))).tocsr()
                rows += [pr[i] for i in chosen]
                constants = np.concatenate((constants,pconst[chosen]))
        exact = read_patterns('codex_mass6_family_patterns')['exact_small_channels']
        groups = {'63_joint': (['63_63','63_52'],exact['63_30']+exact['63_41']),
                  '44_joint': (['44_44'],exact['44_22']+exact['44_33']),
                  '71_joint': (['71_71'],exact['71_60'])}
        for label,(parts,offset) in groups.items():
            for part in parts: offset += objectives[part][0]
            objectives[label] = (offset,[sum(objectives[p][1][j] for p in parts)
                                         for j in range(len(caps))])
        old = exact['60_60']+exact['52_41']+exact['52_52']+exact['33_33']
        for label,parts in [('all_except90',['63_joint','44_joint','71_joint']),
                            ('all_including90',['63_joint','44_joint','71_joint','90_90'])]:
            objectives[label] = (old+sum(objectives[p][0] for p in parts),
                [sum(objectives[p][1][j] for p in parts) for j in range(len(caps))])
    elif family in ('63', 'f0split'):
        data = read_patterns('codex_six_three_mass6_patterns' if family == '63'
                             else 'codex_f0_internal_pattern_split')
        pairs, caps, rows, matrix, constants = build(data)
        objectives = {
            name: (0, [0]*len(pairs)+[-row['counts'][name] for row in data['patterns']])
            for name in (('Q6_no_prism', 'Q8_no_prism') if family == '63'
                         else ('disjoint_negative_triangles','shared_rung_apex'))}
    else:
        suffix = '_tf' if family == 'ftf' else ''
        data = read_patterns(f'codex_f0_mass6_p6{suffix}_patterns')
        pairs, caps, rows, matrix, constants = build(data)
        internal = [0]*len(pairs)+[-row['counts']['F0'] for row in data['patterns']]
        objectives = {'internal': (0, internal)}
        cross = read_patterns(f'codex_f0_mass6_p5{suffix}_patterns')
        pp, pc, pr, pm, pconst, offset, po = pair_model(cross)
        assert pairs == pp and caps[:len(pp)] == pc
        chosen = [i for i, (name, _, _) in enumerate(pr)
                  if name.startswith(('forced_', 'forbidden_'))]
        matrix = vstack((matrix, hstack((pm[chosen],
            coo_matrix((len(chosen), len(caps)-len(pp))))))).tocsr()
        rows += [pr[i] for i in chosen]
        constants = np.concatenate((constants, pconst[chosen]))
        small = read_patterns(f'codex_f0_mass6_p4{suffix}_patterns')
        offset += sum(small['profiles'][r['profiles'][0]][1]*r['counts']['F0']
                      for r in small['patterns'])
        joint = list(internal); joint[:len(pairs)] = po
        objectives['joint_with_old'] = (offset, joint)
    rows, matrix, constants = add_type(data, pairs, caps, rows, matrix, constants, kind)
    return caps, rows, matrix, constants, objectives


def run(family, kind, verify_only=False, selected=None):
    start = time.monotonic()
    caps, rows, matrix, constants, objectives = model(family, kind)
    path = ROOT / f'data/codex_grid_pair_collisions_{family}_{kind}.json.gz'
    if verify_only or path.exists():
        with gzip.open(path, 'rt') as stream:
            report = json.load(stream)
    else:
        report = {'family': family, 'twin_pair_type': kind, 'results': {},
                  'scope': 'Unordered binary mass-six collision pairs per twin-prism pair; both signs. Other channels excluded.'}
    if verify_only:
        assert report['variables'] == len(caps) and report['rows'] == len(rows)
        if not selected: selected = list(report['results'])
    else:
        report.update(variables=len(caps), rows=len(rows))
    for name, (offset, objective) in objectives.items():
        if selected and name not in selected:
            continue
        if not verify_only:
            print('Solving', family, kind, name, flush=True)
            result = linprog(np.array(objective, dtype=float), A_ub=-matrix,
                             b_ub=constants, bounds=list(zip([0]*len(caps), caps)),
                             method='highs-ipm',
                             options={'time_limit': 120} if kind == 'independent' else {})
            assert result.success, result.message
            proof = certificate(rows, caps, objective, result)
            upper = F(proof['collision_upper_bound'])+offset
            report['results'][name] = {'objective_constant': offset, 'certificate': proof,
                                      'collision_upper_bound': str(upper),
                                      'even_integer_upper_bound': int(2*(upper//2))}
        record = report['results'][name]
        verify(rows, caps, objective, record['certificate'])
        upper = F(record['certificate']['collision_upper_bound'])+offset
        assert record['objective_constant'] == offset
        assert F(record['collision_upper_bound']) == upper
        assert record['even_integer_upper_bound'] == 2*(upper//2)
        print('Verified', family, kind, name, '<=', record['even_integer_upper_bound'],
              '; rational', str(upper), '; seconds', round(time.monotonic()-start, 1), flush=True)
        if not verify_only:
            with gzip.GzipFile(filename=path, mode='wb', mtime=0) as stream:
                stream.write(json.dumps(report).encode())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=('63', 'f0', 'ftf', 'all', 'f0split'), required=True)
    parser.add_argument('--kind', choices=('grid', 'nongrid', 'independent'), required=True)
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--objectives', nargs='+')
    args = parser.parse_args()
    run(args.family, args.kind, args.verify_only, args.objectives)
