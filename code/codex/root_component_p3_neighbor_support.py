"""Necessary profile-only neighbours of Q56 in the P3/P3N families.

P3 assumes H01=-H02 != 0 and grids Q12,Q45,Q46. Each z in Q56
has 1+d_z neighbours in T=Q03+Q13+Q23, hence at least one.
P3N drops Q12 grid: z has 2+d_z neighbours in U=Q12+T, hence at
least two. Here d_z is its unknown degree inside Q56.

An edge between two outside profiles must respect every already
saturated common-neighbour and upper-letter quota. For P3N, two
neighbours of z must also fit their joint quotas and their common
neighbour z. No outside-outside adjacency is added to the input.

This is a necessary condition only. A passing support is not a graph.
The caller is responsible for the stated family hypotheses.
"""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process


def mask(vertices):
    return sum(1 << v for v in vertices)


def prepare_profile(rows, known_labels, outside_label, profile, root_count=7):
    p = mask(profile)
    letters = mask(outside_label)
    shared = [len(set(outside_label) & set(q)) for q in known_labels]
    slacks = [2 - int(bool(p & (1 << v))) - shared[v] - (p & row).bit_count()
              for v, row in enumerate(rows)]
    roots = {l // 2 for l in outside_label}
    upper = [1 if l // 2 in roots else 2 for l in range(2*root_count)]
    for v in profile:
        for l in known_labels[v]:
            upper[l] -= 1
    return {
        'mask': p, 'letters': letters, 'degree_remaining': 2*root_count-2-len(profile),
        'zero': mask(v for v, s in enumerate(slacks) if s == 0),
        'one': mask(v for v, s in enumerate(slacks) if s == 1),
        'upper_zero': mask(l for l, s in enumerate(upper) if s == 0),
        'upper_one': mask(l for l, s in enumerate(upper) if s == 1),
        'valid': min(slacks + upper + [2*root_count-2-len(profile)]) >= 0,
    }


def edge_failure(a, b):
    """First exact necessary inequality ruling out an edge, or None."""
    if not a['valid'] or not b['valid']:
        return 'invalid_single_profile'
    if min(a['degree_remaining'], b['degree_remaining']) < 1:
        return 'no_degree_capacity'
    if ((a['mask'] & b['mask']).bit_count()
            + (a['letters'] & b['letters']).bit_count() > 1):
        return 'adjacent_pair_common_neighbours'
    if (a['mask'] & b['zero']) or (b['mask'] & a['zero']):
        return 'saturated_known_pair'
    if (a['letters'] & b['upper_zero']) or (b['letters'] & a['upper_zero']):
        return 'saturated_upper_letter'
    return None


def two_star_failure(z, a, b):
    """Given possible edges za,zb, rule out their simultaneous presence."""
    if z['degree_remaining'] < 2:
        return 'centre_degree_capacity'
    if ((a['mask'] & b['mask']).bit_count()
            + (a['letters'] & b['letters']).bit_count() > 1):
        return 'two_neighbours_already_share_two'
    if a['mask'] & b['mask'] & z['one']:
        return 'centre_known_pair_capacity_one'
    if a['letters'] & b['letters'] & z['upper_one']:
        return 'centre_upper_letter_capacity_one'
    return None


def star_support(z, partner_domains, minimum, include_candidates=False):
    """Exact enumeration of a necessary one- or two-neighbour star.

partner_domains maps outside indices to prepared profiles. Profiles of
one outside vertex are alternatives, never two distinct neighbours.
"""
    assert minimum in (1, 2)
    candidates = []
    rejected = Counter()
    for u, domain in partner_domains.items():
        for pi, p in enumerate(domain):
            reason = edge_failure(z, p)
            if reason:
                rejected[reason] += 1
            else:
                candidates.append((u, pi, p))
                if minimum == 1 and not include_candidates:
                    return {'possible': True, 'witness': [[u, pi]]}
    info = {'candidate_profiles': len(candidates),
            'candidate_vertices': len({u for u, _, _ in candidates}),
            'edge_rejections': dict(rejected)}
    if include_candidates:
        info['candidates'] = [[u, pi] for u, pi, _ in candidates]
    if minimum == 1:
        return {**info, 'possible': bool(candidates),
                'witness': [[candidates[0][0], candidates[0][1]]] if candidates else []}
    pair_rejected = Counter()
    for (u, pi, a), (v, pj, b) in combinations(candidates, 2):
        if u == v:
            pair_rejected['same_outside_vertex'] += 1
            continue
        reason = two_star_failure(z, a, b)
        if reason:
            pair_rejected[reason] += 1
        else:
            return {**info, 'possible': True, 'witness': [[u, pi], [v, pj]]}
    return {**info, 'possible': False, 'pair_rejections': dict(pair_rejected)}


def filter_profiles(rows, known_labels, outside_labels, domains, mode='P3', include_supports=False):
    """Return pruned domains, exact rejection diagnostics and optional SAT cuts.

For each retained Q56 profile, optional supports give a necessary
conditional cardinality: if this profile is selected, at least
minimum_neighbours of its listed partner profile literals are true.
Each partner vertex must still select exactly one profile in the caller.
Indices in supports refer to the INPUT domains.
"""
    assert mode in ('P3', 'P3N')
    assert len(rows) == len(known_labels)
    assert len(outside_labels) == len(domains)
    assert all(len(q) == 2 and q[0] // 2 != q[1] // 2
               for q in list(known_labels) + list(outside_labels))
    assert all(len(set(p)) == len(p) and all(0 <= v < len(rows) for v in p)
               for d in domains for p in d)
    minimum = 1 if mode == 'P3' else 2
    partner_roots = {(0, 3), (1, 3), (2, 3)}
    if mode == 'P3N':
        partner_roots.add((1, 2))
    z_indices = [i for i, q in enumerate(outside_labels) if tuple(l // 2 for l in q) == (5, 6)]
    partners = [i for i, q in enumerate(outside_labels) if tuple(l // 2 for l in q) in partner_roots]
    assert len(z_indices) == 4 and len(partners) == (12 if mode == 'P3' else 16)
    prepared = {i: [prepare_profile(rows, known_labels, outside_labels[i], p) for p in domains[i]]
                for i in z_indices + partners}
    partner_domains = {i: prepared[i] for i in partners}
    kept = [list(range(len(d))) for d in domains]
    removed = []; cuts = []
    for zi in z_indices:
        kept[zi] = []
        for pi, z in enumerate(prepared[zi]):
            result = star_support(z, partner_domains, minimum, include_supports)
            if result['possible']:
                kept[zi].append(pi)
                if include_supports:
                    cuts.append({'outside_index': zi, 'profile_index': pi,
                                 'minimum_neighbours': minimum,
                                 'support_profiles': result['candidates']})
            else:
                # Rejection counts cover every candidate edge/pair; no time
                # limit or heuristic rejection is used by this enumerator.
                removed.append({'outside_index': zi, 'outside_label': outside_labels[zi],
                                'profile_index': pi, 'profile': domains[zi][pi],
                                'minimum_neighbours': minimum, **result})
    empty = [i for i, indices in enumerate(kept) if not indices]
    return {'status': 'EXCLUDED_Q56_NEIGHBOUR_SUPPORT' if empty else 'PASSES_Q56_NEIGHBOUR_SUPPORT',
            'mode': mode, 'minimum_neighbours': minimum, 'empty_domains': empty,
            'removed_count': len(removed), 'rejections': removed, 'kept_indices': kept,
            'domains': [[d[i] for i in indices] for d, indices in zip(domains, kept)],
            'conditional_cardinality_cuts': cuts,
            'scope': 'Necessary profile-only condition under the explicitly stated P3/P3N hypotheses.'}


def controls():
    # Synthetic local stars: both single edges are allowed, but using a
    # common known vertex twice can exceed the centre's remaining mu quota.
    rows = [0] * 4
    labels = [(0, 2), (1, 3), (8, 10), (9, 12)]
    z = prepare_profile(rows, labels, (10, 12), (0, 1))
    a = prepare_profile(rows, labels, (0, 6), (2,))
    b = prepare_profile(rows, labels, (2, 7), (3,))
    bad_b = prepare_profile(rows, labels, (2, 7), (2,))
    assert edge_failure(z, a) is None and edge_failure(z, bad_b) is None
    positive = star_support(z, {0: [a], 1: [b]}, 2)
    assert positive['possible']
    negative = star_support(z, {0: [a], 1: [bad_b]}, 2)
    assert not negative['possible']
    assert negative['pair_rejections'] == {'centre_known_pair_capacity_one': 1}
    same = star_support(z, {0: [a, b]}, 2)
    assert not same['possible'] and same['candidate_vertices'] == 1
    return {'positive_two_star': positive, 'joint_quota_obstruction': negative,
            'alternatives_not_distinct_vertices': same,
            'scope': 'Synthetic local inequality controls, not Conway constructions.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, nargs='?')
    parser.add_argument('--mode', choices=('P3', 'P3N'), default='P3')
    parser.add_argument('--include-supports', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    resources = limit_research_process(1)
    started = time.process_time()
    out = {'controls': controls(), 'resources': resources}
    if args.input:
        data = json.loads(args.input.read_text(encoding='utf-8-sig'))
        out['result'] = filter_profiles(data['rows'], data['known_labels'], data['outside_labels'],
                                        data['domains'], args.mode, args.include_supports)
    out['cpu_seconds'] = time.process_time() - started
    atomic_json_write(args.output, out)
    print(json.dumps({k: v for k, v in out.items() if k != 'result'}))
    if 'result' in out:
        print(json.dumps({k: out['result'][k] for k in ('status', 'removed_count', 'empty_domains')}))


if __name__ == '__main__':
    main()
