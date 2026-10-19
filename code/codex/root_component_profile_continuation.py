"""Exact necessary continuation of already selected outside profiles.

The known Gamma rows and every outside-to-known edge are fixed. Unknown
outside edges are first bounded by lambda=1, mu=2, and upper-letter
quotas. Degree, letter and known/outside common-neighbour equalities
then form a finite binary linear system. Tight-cardinality propagation
can refute it with a replayable proof; passing is not a completion.

This module needs the full 84 root-rectangle labels, with an arbitrary
split into known and outside vertices. It assumes no P3/K3 symmetry.
"""

import argparse
from collections import Counter, deque
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_p3_neighbor_support import mask, prepare_profile, edge_failure
from root_component_resources import atomic_json_write, limit_research_process


def known_rows_check(rows, known_labels, outside_labels, profiles):
    labels = [tuple(q) for q in list(known_labels) + list(outside_labels)]
    all_labels = {(2*a+s, 2*b+t) for a, b in combinations(range(7), 2)
                  for s, t in product(range(2), repeat=2)}
    assert len(labels) == 84 and set(labels) == all_labels
    n = len(rows)
    assert n == len(known_labels) and len(profiles) == len(outside_labels)
    assert all(0 <= r < (1 << n) and not r & (1 << u) for u, r in enumerate(rows))
    assert all(((rows[u] >> v) & 1) == ((rows[v] >> u) & 1)
               for u, v in combinations(range(n), 2))
    assert all(len(set(p)) == len(p) and all(0 <= v < n for v in p) for p in profiles)
    full = [r | sum(1 << (n+i) for i, p in enumerate(profiles) if u in p)
            for u, r in enumerate(rows)]
    violations = []
    for u, row in enumerate(full):
        if row.bit_count() != 12:
            violations.append({'kind': 'known_degree', 'vertex': u, 'actual': row.bit_count(), 'target': 12})
        roots = {l // 2 for l in labels[u]}
        for l in range(14):
            actual = sum(bool(row & (1 << v)) for v, q in enumerate(labels) if l in q)
            target = 1 if l // 2 in roots else 2
            if actual != target:
                violations.append({'kind': 'known_letter', 'vertex': u, 'letter': l,
                                   'actual': actual, 'target': target})
    for u, v in combinations(range(n), 2):
        target = 2 - ((rows[u] >> v) & 1) - len(set(labels[u]) & set(labels[v]))
        actual = (full[u] & full[v]).bit_count()
        if actual != target:
            violations.append({'kind': 'known_pair', 'vertices': [u, v], 'actual': actual, 'target': target})
    return {'valid': not violations, 'violations': violations}


def linear_system(rows, known_labels, outside_labels, profiles):
    """Every omitted edge has an exact local obstruction to adjacency."""
    prepared = [prepare_profile(rows, known_labels, q, p) for q, p in zip(outside_labels, profiles)]
    invalid = [i for i, p in enumerate(prepared) if not p['valid']]
    if invalid:
        return {'invalid_profiles': invalid}
    n = len(profiles); edges = []; incidence = [[] for _ in range(n)]; forbidden = Counter()
    for u, v in combinations(range(n), 2):
        why = edge_failure(prepared[u], prepared[v])
        if why:
            forbidden[why] += 1
        else:
            ei = len(edges); edges.append((u, v))
            incidence[u].append((ei, v)); incidence[v].append((ei, u))
    constraints = []
    for u, (q, p, info) in enumerate(zip(outside_labels, profiles, prepared)):
        constraints.append({'kind': 'degree', 'vertex': u, 'target': 12-len(p),
                            'edges': [e for e, _ in incidence[u]]})
        for v, row in enumerate(rows):
            target = 2 - int(v in p) - len(set(q) & set(known_labels[v])) - (info['mask'] & row).bit_count()
            constraints.append({'kind': 'common_with_known', 'vertex': u, 'known_vertex': v,
                                'target': target, 'edges': [e for e, w in incidence[u] if v in profiles[w]]})
        roots = {l // 2 for l in q}
        for l in range(14):
            target = (1 if l // 2 in roots else 2) - sum(l in known_labels[v] for v in p)
            constraints.append({'kind': 'upper_letter', 'vertex': u, 'letter': l,
                                'target': target, 'edges': [e for e, w in incidence[u] if l in outside_labels[w]]})
    return {'edges': edges, 'constraints': constraints, 'forbidden_edge_counts': dict(forbidden)}


def replay_quota_refutation(constraints, edge_count, proof):
    """Read the derivation once; no branching or search is repeated."""
    state = [-1] * edge_count
    for step in proof['trace']:
        c = constraints[step['constraint']]
        unknown = [e for e in c['edges'] if state[e] == -1]
        need = c['target'] - sum(state[e] == 1 for e in c['edges'])
        assert unknown == step['edges'] and unknown
        assert (step['value'] == 0 and need == 0) or (step['value'] == 1 and need == len(unknown))
        for e in unknown:
            state[e] = step['value']
    c = constraints[proof['conflict_constraint']]
    remaining = sum(state[e] == -1 for e in c['edges'])
    need = c['target'] - sum(state[e] == 1 for e in c['edges'])
    assert need < 0 or need > remaining
    assert proof['remaining_target'] == need and proof['remaining_capacity'] == remaining
    return {'valid': True, 'checked_steps': len(proof['trace']),
            'fixed_edges': sum(x != -1 for x in state)}


def propagate_quotas(constraints, edge_count):
    occurrence = [[] for _ in range(edge_count)]
    for ci, c in enumerate(constraints):
        assert len(set(c['edges'])) == len(c['edges'])
        for e in c['edges']:
            occurrence[e].append(ci)
    state = [-1] * edge_count
    need = [c['target'] for c in constraints]
    count = [len(c['edges']) for c in constraints]
    queue = deque(range(len(constraints))); pending = set(queue); trace = []
    while queue:
        ci = queue.popleft(); pending.remove(ci)
        if need[ci] < 0 or need[ci] > count[ci]:
            proof = {'trace': trace, 'conflict_constraint': ci,
                     'remaining_target': need[ci], 'remaining_capacity': count[ci]}
            return {'status': 'EXCLUDED_PROFILE_CONTINUATION', 'proof': proof,
                    'conflict': constraints[ci],
                    'proof_check': replay_quota_refutation(constraints, edge_count, proof)}
        if not count[ci] or need[ci] not in (0, count[ci]):
            continue
        value = int(need[ci] == count[ci])
        unknown = [e for e in constraints[ci]['edges'] if state[e] == -1]
        trace.append({'constraint': ci, 'value': value, 'edges': unknown})
        for e in unknown:
            state[e] = value
            for cj in occurrence[e]:
                need[cj] -= value; count[cj] -= 1
                if cj not in pending:
                    pending.add(cj); queue.append(cj)
    return {'status': 'PASSES_LINEAR_PROFILE_CONTINUATION',
            'forced_ones': [i for i, s in enumerate(state) if s == 1],
            'forced_zeroes': [i for i, s in enumerate(state) if s == 0],
            'unknown_edges': sum(s == -1 for s in state), 'propagation_steps': len(trace)}


def continue_profiles(rows, known_labels, outside_labels, profiles):
    validity = known_rows_check(rows, known_labels, outside_labels, profiles)
    if not validity['valid']:
        return {'status': 'INVALID_COMPLETE_KNOWN_ROWS', 'known_rows_check': validity}
    system = linear_system(rows, known_labels, outside_labels, profiles)
    if 'invalid_profiles' in system:
        return {'status': 'INVALID_SINGLE_PROFILE', **system, 'known_rows_check': validity}
    result = propagate_quotas(system['constraints'], len(system['edges']))
    return {'scope': 'Necessary symmetric outside-edge continuation of this fixed profile selection only.',
            'known_rows_check': validity, **system, **result}


def controls():
    bad = [{'edges': [0], 'target': 1}, {'edges': [0, 1], 'target': 1}, {'edges': [1], 'target': 1}]
    refuted = propagate_quotas(bad, 2)
    assert refuted['status'] == 'EXCLUDED_PROFILE_CONTINUATION' and refuted['proof_check']['valid']
    good = propagate_quotas([{'edges': [0, 1], 'target': 1}], 2)
    assert good['status'] == 'PASSES_LINEAR_PROFILE_CONTINUATION' and good['unknown_edges'] == 2
    altered = json.loads(json.dumps(refuted['proof']))
    altered['trace'][0]['value'] ^= 1
    try:
        replay_quota_refutation(bad, 2, altered)
    except AssertionError:
        rejected = True
    else:
        rejected = False
    assert rejected
    return {'tight_quota_refutation': refuted, 'open_binary_equation': good,
            'altered_derivation_rejected': rejected}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path, nargs='?'); p.add_argument('--output', type=Path, required=True)
    args = p.parse_args(); resources = limit_research_process(1); started = time.process_time()
    out = {'controls': controls(), 'resources': resources}
    if args.input:
        data = json.loads(args.input.read_text(encoding='utf-8-sig'))
        out['result'] = continue_profiles(data['rows'], data['known_labels'], data['outside_labels'], data['profiles'])
    out['cpu_seconds'] = time.process_time() - started
    atomic_json_write(args.output, out)
    print(json.dumps({'cpu_seconds': out['cpu_seconds'],
                      'status': out.get('result', {}).get('status', 'CONTROLS_PASSED')}))


if __name__ == '__main__':
    main()
