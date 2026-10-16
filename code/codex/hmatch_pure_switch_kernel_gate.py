"""Construct pure matching switches, allowing a changed kernel.

For old edges ab,cd and new edges ac,bd, Delta=uv^t+vu^t with
u=e_a-e_d, v=e_c-e_b. If T and T-Delta are PSD, their kernel
profiles u|ker(T),v|ker(T) either both vanish, or are nonzero negative
multiples. Independent profiles give an exact negative-energy witness.
This gate does NOT assume preservation of the old kernel or its nullity.
The antipodal gate additionally restricts ALL rematchings of one star,
using the extremal eigenvalue -1 of a matching matrix. Integer lifts of
the antipodal profiles supply exact certificates for that restriction.

Producer PSD certificates are accepted. An exact kernel is computed to
construct NEW perturbations and witnesses, not to re-audit the producer.
"""
import argparse
from collections import Counter
from functools import reduce
from itertools import combinations
import json
from math import gcd, lcm
from pathlib import Path
import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hmatch_cycle_reflections import B, LABELS, ROOT_INTERSECTION, load_graph, new_candidate_checks
from odd9_endpoint_mate_family import exact_psd


def integer_kernel(matrix):
    vectors = []
    for v in sp.Matrix(matrix.tolist()).nullspace():
        denominator = lcm(*(int(x.q) for x in v))
        w = [int(x*denominator) for x in v]
        divisor = reduce(gcd, map(abs, w))
        vectors.append([x//divisor for x in w])
    return np.array(vectors, dtype=object).T


def antipodal_gate(gamma, kernel, star):
    """Necessary edges for ANY new matching supported on this one star.

    Let P be the old matching and W=projection(ker T) intersect ker(P+I).
    If replacing P by P' keeps T PSD, v^t(P-P')v>=0 for v in W.
    But Pv=-v and P'>=-I, so equality is forced and P'v=-v.
    Every new mate therefore has the opposite W-profile, with no
    assumption on preservation of the old kernel, rank, or nullity.
    """
    projection = sp.Matrix(kernel[star].tolist())
    matching = sp.Matrix(gamma[np.ix_(star, star)].tolist())
    coefficients = ((matching+sp.eye(len(star)))*projection).nullspace()
    integer_columns, lifts = [], []
    if coefficients:
        coefficient_matrix = sp.Matrix.hstack(*coefficients)
        projected = projection*coefficient_matrix
        pivots = projected.rref()[1]
        for j in pivots:
            lift = sp.Matrix(kernel.tolist())*coefficient_matrix[:, j]
            denominator = lcm(*(int(x.q) for x in lift))
            integral = [int(x*denominator) for x in lift]
            divisor = reduce(gcd, map(abs, integral))
            integral = [x//divisor for x in integral]
            lifts.append(integral)
            integer_columns.append([integral[i] for i in star])
    profiles = [[column[i] for column in integer_columns] for i in range(len(star))]
    allowed = [(star[i],star[j]) for i,j in combinations(range(len(star)),2)
               if all(x+y == 0 for x,y in zip(profiles[i], profiles[j]))]
    old_edges = [(i,j) for i,j in combinations(star,2) if gamma[i,j]]
    assert set(old_edges).issubset(allowed)
    return dict(antipodal_dimension=len(integer_columns), vertices=star, profiles=profiles,
                integer_kernel_lifts=lifts,
                allowed_edges=allowed, old_edges=old_edges,
                all_pure_rematchings_excluded=(set(old_edges) == set(allowed)))


def negative_witness(kernel, a, b, c, d, changed_t8):
    # u=e_a-e_d, v=e_c-e_b, Gamma'-Gamma=uv^t+vu^t.
    up = list(kernel[a]-kernel[d])
    vp = list(kernel[c]-kernel[b])
    for i, j in combinations(range(kernel.shape[1]), 2):
        determinant = up[i]*vp[j]-up[j]*vp[i]
        if determinant:
            w = (vp[j]-up[j])*kernel[:, i]+(up[i]-vp[i])*kernel[:, j]
            return 'INDEPENDENT_PROFILES', w
    unonzero = next((i for i, x in enumerate(up) if x), None)
    vnonzero = next((i for i, x in enumerate(vp) if x), None)
    if unonzero is None and vnonzero is None:
        return 'BOTH_PROFILES_ZERO', None
    if unonzero is not None and vnonzero is not None:
        if up[unonzero]*vp[unonzero] > 0:
            return 'POSITIVE_PROPORTIONAL_PROFILES', kernel[:, unonzero].copy()
        return 'NEGATIVE_PROPORTIONAL_PROFILES', None
    # A zero-energy kernel vector leaking to a nonzero row also forbids PSD.
    q = kernel[:, vnonzero if unonzero is None else unonzero].copy()
    y = np.zeros(44, dtype=object)
    if unonzero is None:
        y[a], y[d] = 1, -1
        factor = vp[vnonzero]
    else:
        y[c], y[b] = 1, -1
        factor = up[unonzero]
    if factor < 0:
        q = -q
        factor = -factor
    energy_y = int(y @ changed_t8 @ y)
    multiple = abs(energy_y)//(32*factor)+1
    return 'ONE_ZERO_PROFILE_LEAKAGE', multiple*q+y


def run(source, output, name=None):
    started = time.monotonic()
    records = json.loads(Path(source).read_text(encoding='utf-8'))
    if 'labels' in records:
        records = {Path(source).stem: records}
    if name is not None:
        records = {name: records[name]}
    reports, hits = [], []
    mate_gram = B.T @ B[[r ^ 1 for r in range(14)]]
    for record_name, record in records.items():
        gamma = load_graph(record)
        t8 = 24*np.eye(44, dtype=np.int64)-8*gamma-3*ROOT_INTERSECTION-mate_gram+2
        kernel = integer_kernel(t8)
        assert not np.any(t8 @ kernel)
        details, star_profiles = [], []
        statuses = Counter()
        for central in range(4):
            star = [i for i, p in enumerate(LABELS) if central in p]
            outer = [i for i in star if max(LABELS[i]) >= 4]
            # Full projection onto a support implies rigidity of EVERY
            # zero-diagonal perturbation on that support, not just switches.
            star_profiles.append(dict(central=central,
                full_star_profile_rank=int(sp.Matrix(kernel[star].tolist()).rank()),
                outer_profile_rank=int(sp.Matrix(kernel[outer].tolist()).rank()),
                antipodal_gate=antipodal_gate(gamma, kernel, star)))
            for lift in star_profiles[-1]['antipodal_gate']['integer_kernel_lifts']:
                q = np.array(lift, dtype=object)
                assert not np.any(t8 @ q)
                assert not np.any((gamma[np.ix_(star, star)]+np.eye(12,dtype=int)) @ q[star])
            edges = [(i, j) for i, j in combinations(star, 2) if gamma[i, j]]
            assert len(edges) == 6 and len({i for edge in edges for i in edge}) == 12
            for (a, b), (c0, d0) in combinations(edges, 2):
                for c, d in [(c0, d0), (d0, c0)]:
                    changed = gamma.copy()
                    for i, j in [(a, b), (c, d)]:
                        changed[i, j] = changed[j, i] = 0
                    for i, j in [(a, c), (b, d)]:
                        changed[i, j] = changed[j, i] = 1
                    new_t8 = t8-8*(changed-gamma)
                    gate, w = negative_witness(kernel, a, b, c, d, new_t8)
                    info = dict(central=central, old_edges=[[a,b],[c,d]],
                                new_edges=[[a,c],[b,d]], profile_gate=gate)
                    statuses[gate] += 1
                    if w is not None:
                        divisor = reduce(gcd, (abs(int(x)) for x in w))
                        w = np.array([int(x)//divisor for x in w], dtype=object)
                        energy = int(w @ new_t8 @ w)
                        assert energy < 0
                        info.update(verdict='T_NOT_PSD_EXACT_WITNESS',
                                    witness=list(map(int, w)), energy_T8=energy)
                    else:
                        combinatorics = new_candidate_checks(changed)
                        info['combinatorics'] = combinatorics
                        if not combinatorics.startswith('H_MATCH_'):
                            info['verdict'] = combinatorics
                        else:
                            t_psd, rank_t, reason_t = exact_psd(new_t8)
                            info.update(T_PSD=t_psd, rank_T=rank_t, reason_T=reason_t)
                            if not t_psd:
                                info['verdict'] = 'T_NOT_PSD_EXACT'
                            else:
                                u15 = 60*np.eye(44, dtype=np.int64)+15*changed-4*ROOT_INTERSECTION+mate_gram-2
                                u_psd, rank_u, reason_u = exact_psd(u15)
                                info.update(U_PSD=u_psd, rank_U=rank_u, reason_U=reason_u)
                                info['verdict'] = 'NEW_TU_PSD' if u_psd else 'U_NOT_PSD_EXACT'
                                if u_psd and rank_t <= 30 and combinatorics == 'H_MATCH_BROKEN':
                                    hit = dict(source=record_name, labels=LABELS,
                                        edges=[[i,j] for i,j in combinations(range(44),2) if changed[i,j]],
                                        T_PSD=True,U_PSD=True,rank_T=rank_t,rank_U=rank_u,
                                        construction=info.copy())
                                    hits.append(hit)
                    statuses[info['verdict']] += 1
                    details.append(info)
        report = dict(source=record_name, kernel_dimension_used=int(kernel.shape[1]),
                      switches=len(details), star_profiles=star_profiles,
                      statuses=dict(statuses), details=details)
        reports.append(report)
        summary = {k:v for k,v in report.items() if k not in ('details', 'star_profiles')}
        summary['star_profiles'] = [dict(central=s['central'],
            full_star_profile_rank=s['full_star_profile_rank'],
            outer_profile_rank=s['outer_profile_rank'],
            antipodal_dimension=s['antipodal_gate']['antipodal_dimension'],
            allowed_edges=len(s['antipodal_gate']['allowed_edges']),
            all_pure_rematchings_excluded=s['antipodal_gate']['all_pure_rematchings_excluded'])
            for s in star_profiles]
        print(json.dumps(summary), flush=True)
    result = dict(status='EXACT_NEW_PURE_SWITCH_CONSTRUCTIONS', source_file=str(source),
        reports=reports, hits=hits, seconds=time.monotonic()-started,
        scope='Constructs every pure four-vertex matching switch of the supplied seeds; antipodal certificates restrict all rematchings of a single star. All other edges and B,M stay fixed. Kernel changes are allowed. No universal rank14 or H-MATCH theorem.')
    Path(output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(hits=len(hits), seconds=result['seconds'])), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--name')
    args = parser.parse_args()
    run(args.source, args.output, args.name)
