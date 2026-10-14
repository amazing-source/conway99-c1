"""Exact rank-two edge trades, including the two overlap vertices.

Minimal signed dependencies among the three star-membership rows have
support2,3,or4. Disjoint pairs give zero-diagonal, star-preserving rank-two
changes. This extends the earlier rectangles, which fixed both overlaps.
No claim of exhausting all star-preserving changes is made.
"""
import argparse
from collections import Counter
from itertools import combinations, product
from math import gcd
from pathlib import Path
import json
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_rank_repairs import (
    LABELS, GROUPS, STARS, load_gamma, boundary_masks,
    spectral_matrix, response_metric, switched,
)
from three_star_connected_repairs import classify_gamma
from three_star_ambient_upper import analyse as analyse_upper


def circuits():
    A, AP, B = GROUPS
    p, pp = LABELS.index((0, 2)), LABELS.index((1, 2))
    result = []
    for group in GROUPS:
        result.extend(((u, 1), (v, -1)) for u, v in combinations(group, 2))
    for overlap, group in ((p, A), (pp, AP)):
        result.extend(tuple(sorted(((overlap, 1), (u, -1), (v, -1))))
                      for u, v in product(group, B))
    result.extend(tuple(sorted(((p, 1), (pp, -1), (u, -1), (v, 1))))
                  for u, v in product(A, AP))
    assert len(result) == 496
    assert len(set(result)) == len(result)
    assert all(all(sum(value*STARS[i, c] for i, value in a) == 0
                       for c in range(3)) for a in result)
    return tuple(result)


def pair_patterns(all_circuits, include_rectangles=False):
    patterns = []
    for ia, ib in combinations(range(len(all_circuits)), 2):
        a, b = all_circuits[ia], all_circuits[ib]
        if not include_rectangles and len(a) == len(b) == 2:
            continue
        if {i for i, _ in a}.intersection(i for i, _ in b):
            continue
        positive, negative = 0, 0
        for i, av in a:
            for j, bv in b:
                lo, hi = sorted((i, j))
                bit = 1 << (34*lo+hi)
                if av*bv > 0:
                    positive |= bit
                else:
                    negative |= bit
        patterns.append((ia, ib, positive, negative))
    return patterns


def dot_metric(W, a, b):
    return sum(av*bv*W[i][j] for i, av in a for j, bv in b)


def trade_rows(rows, a, b):
    changed = [15+i for i, _ in a+b]
    out = rows[:]
    for i, _ in a:
        for j, _ in b:
            out[15+i] ^= 1 << (15+j)
            out[15+j] ^= 1 << (15+i)
    for i in changed:
        if out[i].bit_count() > 14:
            return None
        for j in range(49):
            if i == j or (j in changed and j < i):
                continue
            edge = (out[i] >> j) & 1
            if (out[i] & out[j]).bit_count() > 2-edge:
                return None
    return out


def trade_gamma(gamma, a, b):
    out = [row[:] for row in gamma]
    for i, _ in a:
        for j, _ in b:
            out[i][j] = out[j][i] = 1-out[i][j]
    return out


def analyse(gamma, all_circuits, patterns, output_folder):
    start = time.perf_counter()
    rows = boundary_masks(gamma)
    if any(row.bit_count() > 14 for row in rows) or any(
            (rows[i] & rows[j]).bit_count() > 2-((rows[i] >> j) & 1)
            for i in range(49) for j in range(i+1, 49)):
        raise ValueError('Input violates a boundary degree or common-neighbour cap.')
    # Rank31/PSD is supplied by the producer or by the proved lifting formula.
    W, den = response_metric(spectral_matrix(gamma))
    energies = [dot_metric(W, a, a) for a in all_circuits]
    encoded = sum(1 << (34*i+j) for i in range(34) for j in range(i+1, 34)
                  if gamma[i][j])
    counts = Counter()
    shapes = Counter()
    candidates = []
    closest = []
    for ia, ib, positive, negative in patterns:
        pos, neg = encoded & positive, encoded & negative
        if not pos and neg == negative:
            sign = 1
        elif not neg and pos == positive:
            sign = -1
        else:
            continue
        a, b = all_circuits[ia], all_circuits[ib]
        counts['binary_legal'] += 1
        shapes[f'{len(a)}x{len(b)}'] += 1
        if trade_rows(rows, a, b) is None:
            counts['local_cap_rejections'] += 1
            continue
        counts['locally_admissible'] += 1
        alpha, beta = energies[ia], energies[ib]
        cross = dot_metric(W, a, b)
        value = (den-sign*cross)**2-alpha*beta
        if value < 0:
            counts['indefinite'] += 1
        elif value > 0:
            counts['PSD_rank31'] += 1
        else:
            counts['PSD_rank30'] += 1
            new_gamma = trade_gamma(gamma, a, b)
            structure = classify_gamma(new_gamma)
            if structure['component_count'] != 1:
                counts['rank30_Q_disconnected'] += 1
                candidates.append(dict(a=a, b=b, sign=sign,
                                       component_count=structure['component_count'],
                                       components=structure['outer_pair_components'],
                                       disposition='Outside the connected-Q counterexample target; no further rank or U audit.'))
                continue
            upper = analyse_upper(new_gamma)
            q = [sign*beta*sum(W[i][j]*av for j, av in a)
                 +(den-sign*cross)*sum(W[i][j]*bv for j, bv in b) for i in range(34)]
            common = gcd(*q)
            q = [x//common for x in q]
            assert spectral_matrix(new_gamma)*sp.Matrix(q) == sp.zeros(34, 1)
            record = dict(a=a, b=b, sign=sign, extra_relation=q,
                          component_count=structure['component_count'],
                          components=structure['outer_pair_components'],
                          complementary_gram=upper['complementary_gram'])
            if upper['complementary_gram']['psd']:
                path = output_folder/f'rank30_candidate_{len(candidates):03d}.json'
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(dict(labels=LABELS, gamma=new_gamma,
                                                provenance=record), indent=2)+'\n', encoding='utf-8')
                record['candidate_path'] = str(path)
            candidates.append(record)
        closest.append((abs(value), value, ia, ib, sign))
    closest.sort()
    return dict(status='EXACT_DISJOINT_CIRCUIT_PAIR_SCAN',
                patterns=len(patterns), counts=dict(counts), binary_shapes=dict(shapes),
                candidates=candidates, response_denominator=den,
                closest=[dict(numerator=v, a=all_circuits[ia], b=all_circuits[ib], sign=sign)
                         for _, v, ia, ib, sign in closest[:5]],
                elapsed_seconds=time.perf_counter()-start,
                scope='All disjoint pairs of the stated minimal membership circuits, with optional2x2 rectangles. No longer or general higher-rank changes are exhausted.')


def lifted_seeds(source_path, reports_path):
    source = json.loads(Path(source_path).read_text(encoding='utf-8-sig'))
    index = [LABELS.index(tuple(p)) for p in source['labels']]
    with Path(reports_path).open(encoding='utf-8') as handle:
        for line in handle:
            record = json.loads(line)
            positive = [r for r in record.get('closest', ()) if r['slack_numerator'] > 0]
            if not positive:
                continue
            lift = min(positive, key=lambda r:r['slack_numerator'])
            original = [[0]*34 for _ in range(34)]
            for i, j in source['structures'][record['seed_index']]['edges']:
                original[index[i]][index[j]] = original[index[j]][index[i]] = 1
            gamma = switched(original, lift['rectangle'])
            assert classify_gamma(gamma)['component_count'] == 1
            yield dict(source_index=record['seed_index'], lifting_trade=lift,
                       certification='Previous exact positive-eta calculation proves PSD rank31; no seed rank audit.'), gamma


def self_test(all_circuits, patterns):
    found = next((all_circuits[ia], all_circuits[ib]) for ia, ib, _, _ in patterns
                 if len(all_circuits[ia]) == len(all_circuits[ib]) == 3)
    a, b = found
    av, bv = sp.zeros(34, 1), sp.zeros(34, 1)
    for i, v in a:
        av[i] = v
    for i, v in b:
        bv[i] = v
    P = sp.eye(34)-STARS*(STARS.T*STARS).inv()*STARS.T
    T = 3*P
    assert av.dot(bv) == 0 and av.dot(av) == bv.dot(bv) == 3
    for sign in (-1, 1):
        q = sign*av+bv
        assert (T-sign*(av*bv.T+bv*av.T))*q == sp.zeros(34, 1)
    return dict(status='OWN_CIRCUIT_TRADE_FORMULA_CHECKS_PASS',
                circuits_by_size=dict(Counter(map(len, all_circuits))),
                patterns=len(patterns), tested_disjoint_three_circuits=found)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gamma')
    parser.add_argument('--assume-psd-rank31', action='store_true')
    parser.add_argument('--lift-source')
    parser.add_argument('--lift-reports')
    parser.add_argument('--max-seeds', type=int, default=100)
    parser.add_argument('--skip-lifts', type=int, default=0)
    parser.add_argument('--seconds', type=float, default=55)
    parser.add_argument('--include-rectangles', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    all_circuits = circuits()
    patterns = pair_patterns(all_circuits, args.include_rectangles)
    if args.self_test:
        result = self_test(all_circuits, patterns)
    elif args.lift_source:
        counts = Counter()
        candidates = []
        processed = 0
        status = 'SUPPLIED_LIFTED_SEEDS_EXHAUSTED'
        details = output.with_suffix('.jsonl')
        with details.open('w', encoding='utf-8') as handle:
            for lift_index, (provenance, gamma) in enumerate(lifted_seeds(args.lift_source, args.lift_reports)):
                if lift_index < args.skip_lifts:
                    continue
                if processed >= args.max_seeds or time.perf_counter()-start >= args.seconds:
                    status = 'BOUNDED_LIFTED_SEED_SCAN'
                    break
                report = analyse(gamma, all_circuits, patterns,
                                 output.parent/f'candidates_seed_{provenance["source_index"]}')
                report['provenance'] = provenance
                counts.update(report['counts'])
                candidates.extend(dict(source_index=provenance['source_index'], **c)
                                  for c in report['candidates'])
                handle.write(json.dumps(report)+'\n')
                handle.flush()
                processed += 1
                if processed % 25 == 0:
                    print(json.dumps(dict(processed=processed, counts=dict(counts))), flush=True)
                if any(c['component_count'] == 1 and 'candidate_path' in c for c in report['candidates']):
                    status = 'CONNECTED_Q_COUNTEREXAMPLE_FOUND'
                    break
        result = dict(status=status, processed_seeds=processed, counts=dict(counts),
                      skipped_lifts=args.skip_lifts,
                      candidates=candidates, patterns_per_seed=len(patterns),
                      elapsed_seconds=time.perf_counter()-start,
                      source=args.lift_source, lift_certificates=args.lift_reports,
                      details=str(details))
    else:
        if not args.gamma or not args.assume_psd_rank31:
            parser.error('Supply a producer-certified rank31 seed or previously certified lifts.')
        result = analyse(load_gamma(args.gamma), all_circuits, patterns, output.parent/'circuit_candidates')
        result['input'] = args.gamma
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key:value for key, value in result.items() if key in (
        'status', 'counts', 'binary_shapes', 'elapsed_seconds', 'patterns', 'processed_seeds',
        'circuits_by_size')}))


if __name__ == '__main__':
    main()
