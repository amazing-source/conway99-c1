"""Bounded exact exploration through PSD rank30 closed-relation boundaries.

Starts from producer-certified rank30 seeds. It combines the two proved
rank-two formulas with incidence-fixing reflections. Intermediate states
are not filtered by U; a counterexample to(A) must pass U at the end.
"""
import argparse
from collections import Counter, deque
from math import lcm
from pathlib import Path
import json
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_rank_repairs import LABELS, STARS, spectral_matrix, load_gamma, boundary_masks
from three_star_circuit_trades import circuits, pair_patterns, dot_metric, trade_rows, trade_gamma
from three_star_connected_repairs import classify_gamma
from three_star_incidence_reflections import analyse as reflect
from three_star_ambient_upper import analyse as analyse_upper


def rank30_metric(gamma, closed_pairs):
    q = [int(p[0] in (0, 1) and p[1]//2 in closed_pairs) for p in LABELS]
    relations = STARS.T.col_join(sp.Matrix([q]))
    M = spectral_matrix(gamma)
    assert M*relations.T == sp.zeros(34, 4), 'Known kernel contract mismatch.'
    excluded = relations.rref()[1]
    assert len(excluded) == 4
    basis = [i for i in range(34) if i not in excluded]
    inverse = M.extract(basis, basis).inv(method='DM')
    den = lcm(*(int(x.q) for x in inverse))
    W = [[0]*34 for _ in range(34)]
    for i, u in enumerate(basis):
        for j, v in enumerate(basis):
            W[u][v] = int(8*den*inverse[i, j])
    # W/den is a generalized inverse: energies are valid for range vectors.
    # For a kernel-moving trade only w=s*a-r*b is in that range.
    return q, W, den


def new_extra_relation(gamma):
    # Only for a newly constructed candidate, never for a producer's seed.
    kernel = spectral_matrix(gamma).nullspace()
    return next([str(x) for x in q] for q in kernel
                if sp.Matrix.hstack(STARS, q).rank() == 4)


def walk(seed_paths, maximum_states, seconds, maximum_queue, output):
    start = time.perf_counter()
    all_circuits = circuits()
    patterns = pair_patterns(all_circuits, include_rectangles=True)
    key = lambda g:bytes(x for row in g for x in row)
    queue, seen = deque(), set()
    for seed_index, path in enumerate(seed_paths):
        gamma = load_gamma(path)
        structure = classify_gamma(gamma)
        if structure['component_count'] != 2:
            raise ValueError('This walk requires a rank30 seed with exactly two Q components.')
        pairs = min(structure['outer_pair_components'], key=lambda c:(len(c), c))
        queue.append((gamma, pairs, seed_index, []))
        seen.add(key(gamma))
    totals = Counter()
    reports = output.with_suffix('.jsonl')
    candidates, candidate_seen = [], set()
    processed = 0
    found = False
    rank29_found = False

    def offer_candidate(gamma, seed_index, history, mechanism, known_relation=None, rank=30):
        nonlocal found, rank29_found
        code = key(gamma)
        if code in candidate_seen:
            return
        candidate_seen.add(code)
        structure = classify_gamma(gamma)
        upper = analyse_upper(gamma)['complementary_gram']
        record = dict(seed_index=seed_index, history=history, mechanism=mechanism,
                      rank_T_by_proved_formula=rank, components=structure['outer_pair_components'],
                      complementary_gram=upper)
        if known_relation is not None:
            assert spectral_matrix(gamma)*sp.Matrix(known_relation) == sp.zeros(34, 1)
            record['new_relation'] = known_relation
        elif rank == 30:
            record['new_relation'] = new_extra_relation(gamma)
        record['counterexample_to_A'] = rank <= 30 and structure['component_count'] == 1 and upper['psd']
        path = output.parent/f'{output.stem}_candidate_{len(candidates):03d}.json'
        path.write_text(json.dumps(dict(labels=LABELS, gamma=gamma, provenance=record), indent=2)+'\n', encoding='utf-8')
        record['path'] = str(path)
        candidates.append(record)
        found |= record['counterexample_to_A']
        rank29_found |= rank == 29 and upper['psd']

    def enqueue(gamma, pairs, seed_index, history):
        code = key(gamma)
        if code in seen:
            return
        seen.add(code)
        if len(queue) >= maximum_queue:
            totals['states_not_queued_at_memory_bound'] += 1
            return
        queue.append((gamma, pairs, seed_index, history))

    with reports.open('w', encoding='utf-8') as handle:
        while queue and processed < maximum_states and time.perf_counter()-start < seconds:
            gamma, pairs, seed_index, history = queue.popleft()
            counts = Counter()
            rows = boundary_masks(gamma)
            assert all(row.bit_count() <= 14 for row in rows)
            assert all((rows[i] & rows[j]).bit_count() <= 2-((rows[i] >> j) & 1)
                       for i in range(49) for j in range(i+1, 49))
            q, W, den = rank30_metric(gamma, pairs)
            energies = [dot_metric(W, a, a) for a in all_circuits]
            dots = [sum(q[i]*av for i, av in a) for a in all_circuits]
            encoded = sum(1 << (34*i+j) for i in range(34) for j in range(i+1, 34) if gamma[i][j])
            for ia, ib, positive, negative in patterns:
                pos, neg = encoded & positive, encoded & negative
                if not pos and neg == negative:
                    sign = 1
                elif not neg and pos == positive:
                    sign = -1
                else:
                    continue
                counts['binary_legal'] += 1
                a, b = all_circuits[ia], all_circuits[ib]
                if trade_rows(rows, a, b) is None:
                    counts['local_cap_rejections'] += 1
                    continue
                counts['locally_admissible'] += 1
                r, s = dots[ia], dots[ib]
                delta = -2*sign*r*s
                move = dict(kind='circuit_pair', a_index=ia, b_index=ib, sign=sign)
                if delta < 0 or (delta == 0 and (r or s)):
                    counts['old_kernel_immediately_forbids_PSD'] += 1
                    continue
                cross = dot_metric(W, a, b)
                if not r and not s:
                    value = (den-sign*cross)**2-energies[ia]*energies[ib]
                    if value < 0:
                        counts['kernel_preserving_indefinite'] += 1
                    elif value > 0:
                        counts['kernel_preserving_PSD30'] += 1
                        enqueue(trade_gamma(gamma, a, b), pairs, seed_index, history+[move])
                    else:
                        counts['kernel_preserving_PSD29'] += 1
                        offer_candidate(trade_gamma(gamma, a, b), seed_index, history+[move],
                                        'Rank-two determinant exactly zero on the rank30 image.', rank=29)
                else:
                    value = delta*den-(s*s*energies[ia]+r*r*energies[ib]-2*r*s*cross)
                    if value < 0:
                        counts['kernel_moving_indefinite'] += 1
                    elif value > 0:
                        counts['kernel_moving_PSD31'] += 1
                    else:
                        counts['kernel_moving_PSD30'] += 1
                        new_gamma = trade_gamma(gamma, a, b)
                        structure = classify_gamma(new_gamma)
                        if structure['component_count'] == 1:
                            offer_candidate(new_gamma, seed_index, history+[move],
                                            'Exact positive-kernel-pivot eta=0.')
                        else:
                            assert structure['component_count'] == 2
                            new_pairs = min(structure['outer_pair_components'], key=lambda c:(len(c), c))
                            enqueue(new_gamma, new_pairs, seed_index, history+[move])
                if found or rank29_found:
                    break
            reflection_report = reflect(gamma, pairs)
            counts.update({'reflection_'+k:v for k, v in reflection_report['counts'].items()})
            for candidate in reflection_report['candidates']:
                move = dict(kind='incidence_reflection', u=candidate['u'])
                if len(candidate['components']) == 1:
                    offer_candidate(candidate['gamma'], seed_index, history+[move],
                                    'Orthogonal incidence-fixing reflection.', candidate['new_relation_twice'])
                else:
                    new_pairs = min(candidate['components'], key=lambda c:(len(c), c))
                    enqueue(candidate['gamma'], new_pairs, seed_index, history+[move])
            processed += 1
            totals.update(counts)
            handle.write(json.dumps(dict(state=processed-1, seed_index=seed_index, history=history,
                                         closed_pairs=pairs, counts=dict(counts)))+'\n')
            handle.flush()
            if processed % 50 == 0:
                print(json.dumps(dict(processed=processed, queued=len(queue), counts=dict(totals))), flush=True)
            if found or rank29_found:
                break
    status = ('COUNTEREXAMPLE_TO_A_FOUND' if found else 'NEW_PSD_RANK29_BOUNDARY_FOUND' if rank29_found
              else 'BOUNDED_RANK30_CIRCUIT_WALK' if queue or totals['states_not_queued_at_memory_bound']
              else 'SPECIFIED_RANK30_MOVE_COMPONENTS_EXHAUSTED')
    return dict(status=status, processed_states=processed, queued_states=len(queue),
                discovered_states=len(seen), counts=dict(totals), candidates=candidates,
                seed_paths=seed_paths, maximum_states=maximum_states, seconds_budget=seconds,
                maximum_queue=maximum_queue, patterns_per_state=len(patterns),
                elapsed_seconds=time.perf_counter()-start, details=str(reports),
                scope=[
                    'Seed rank30 and both PSD certifications are accepted from their producer.',
                    'Only exact PSD rank30 states with a two-star closed-set relation are queued.',
                    'No upper-Gram audit is performed on intermediate states; final candidates require U PSD.',
                    'A generalized inverse is used only for vectors in the image, including w=s*a-r*b.',
                    'A bounded search is not an exclusion and does not prove assertion(A).'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seeds', nargs='+', required=True)
    parser.add_argument('--producer-certified-psd-rank30', action='store_true')
    parser.add_argument('--max-states', type=int, default=400)
    parser.add_argument('--seconds', type=float, default=55)
    parser.add_argument('--max-queue', type=int, default=5000)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if not args.producer_certified_psd_rank30:
        parser.error('The input rank30/PSD certificates must be supplied by the producer.')
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result = walk(args.seeds, args.max_states, args.seconds, args.max_queue, output)
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k, v in result.items() if k in (
        'status', 'processed_states', 'queued_states', 'counts', 'elapsed_seconds')}))


if __name__ == '__main__':
    main()
