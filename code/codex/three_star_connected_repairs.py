"""Try exact two-edge trades that destroy a known closed-set kernel relation.

The input rank30 and T/U PSD certifications are supplied by the producer.
We compute a NEW rank-update scalar, not a second rank audit of the seed.
A zero scalar produces a candidate connected-Q counterexample to H3''.
"""
import argparse
from collections import Counter
from pathlib import Path
import json
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_column_domains import prepare, S, load_gamma
from three_star_rank_repairs import (
    rectangles, binary_sign, boundary_masks, switch_caps, switched,
    spectral_matrix, STARS,
)
from three_star_ambient_upper import analyse as analyse_upper
from two_mate_star_structure import classify, LABELS as X_LABELS


def quadratic(numerator, basis, coefficients):
    terms = [(j, coefficients[i]) for j, i in enumerate(basis) if coefficients.get(i)]
    return sum(a*b*numerator[i][j] for i, a in terms for j, b in terms)


def classify_gamma(gamma):
    indices = [S.index(p) for p in X_LABELS]
    return classify([[gamma[i][j] for j in indices] for i in indices])


def scan(gamma, closed_pairs, candidate_directory):
    start = time.perf_counter()
    structure = classify_gamma(gamma)
    if structure['component_count'] != 2:
        raise ValueError('This scan requires exactly two initial Q components.')
    p = prepare(gamma, producer_closed_pairs=closed_pairs)
    q = p['kernels'][-1]
    rows = boundary_masks(gamma)
    counts = Counter()
    candidates = []
    closest = []
    for rectangle in rectangles():
        u, r, v, s = rectangle
        a0, b0 = q[u]-q[r], q[v]-q[s]
        # A rank-two PSD update can lift the old kernel only if both
        # contrasts are nonzero and -2*sign*a0*b0 is positive.
        if not a0 or not b0:
            continue
        sign = binary_sign(gamma, rectangle)
        if not sign:
            continue
        counts['kernel_moving_binary_trades'] += 1
        delta = -2*sign*a0*b0
        if delta <= 0:
            counts['nonpositive_old_kernel_energy'] += 1
            continue
        if not switch_caps(rows, rectangle):
            counts['local_cap_rejections'] += 1
            continue
        counts['locally_admissible'] += 1
        w = {u:b0, r:-b0, v:-a0, s:a0}
        # w is orthogonal to ALL four known kernel generators.
        assert all(sum(row[i]*value for i, value in w.items()) == 0
                   for row in p['kernels'])
        energy_numerator = 8*quadratic(p['inverse'], p['basis'], w)
        slack = delta*p['denominator']-energy_numerator
        closest.append((abs(slack), slack, rectangle, sign, delta))
        if slack < 0:
            counts['indefinite'] += 1
        elif slack > 0:
            counts['PSD_rank31'] += 1
        else:
            counts['PSD_rank30'] += 1
            new_gamma = switched(gamma, rectangle)
            new_structure = classify_gamma(new_gamma)
            if new_structure['component_count'] != 1:
                counts['rank30_Q_disconnected'] += 1
                candidates.append(dict(rectangle=rectangle, sign=sign,
                                       component_count=new_structure['component_count'],
                                       components=new_structure['outer_pair_components'],
                                       disposition='The kernel changed but Q remains disconnected; this is not a counterexample to(A).'))
                continue
            upper = analyse_upper(new_gamma)
            record = dict(rectangle=rectangle, sign=sign,
                          component_count=1, rank_T_by_update_theorem=30,
                          complementary_gram=upper['complementary_gram'])
            if upper['complementary_gram']['psd']:
                # A newly constructed candidate: produce its new relation.
                M = spectral_matrix(new_gamma)
                kernel = M.nullspace()
                assert len(kernel) == 4
                extra = next(qnew for qnew in kernel
                             if sp.Matrix.hstack(STARS, qnew).rank() == 4)
                record['extra_relation'] = [str(value) for value in extra]
                path = candidate_directory/f'connected_rank30_{len(candidates):04d}.json'
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(dict(labels=S, gamma=new_gamma,
                                                provenance=record), indent=2)+'\n', encoding='utf-8')
                record['candidate_path'] = str(path)
            candidates.append(record)
    closest.sort()
    return dict(status='EXACT_KERNEL_MOVING_RECTANGLE_SCAN',
                input_components=structure['outer_pair_components'],
                counts=dict(counts), candidates=candidates,
                scalar_denominator=p['denominator'],
                closest=[dict(slack_numerator=value, rectangle=rect, sign=sign, delta=delta)
                         for _, value, rect, sign, delta in closest[:8]],
                elapsed_seconds=time.perf_counter()-start,
                scope='All single membership-preserving rectangle trades that move this closed-set relation are covered. Longer trades and intermediate changes are not exhausted.')


def self_test():
    # Test the new rank-update formula on our own tiny PSD matrices.
    checks = []
    for energy in (1, 2, 3):
        T = sp.diag(sp.Rational(1, energy), 1, 0)
        q = sp.Matrix([0, 0, 1])
        a, b = sp.Matrix([1, 0, 1]), sp.Matrix([0, 0, 1])
        sign = -1
        w = (b.dot(q))*a-(a.dot(q))*b
        delta = -2*sign*a.dot(q)*b.dot(q)
        slack = delta-(w.T*sp.diag(energy, 1, 0)*w)[0]
        changed = T-sign*(a*b.T+b*a.T)
        if slack > 0:
            assert all(pivot > 0 for pivot in changed.LDLdecomposition(hermitian=False)[1].diagonal())
            outcome = 'positive_definite'
        elif slack == 0:
            assert changed.rank() == 2
            assert changed.is_positive_semidefinite
            outcome = 'PSD_same_rank'
        else:
            assert changed.det() < 0
            outcome = 'indefinite'
        checks.append(dict(energy=energy, slack=int(slack), outcome=outcome))
    # q itself need not be orthogonal to the forced kernel. The contrasts
    # and range-vector energy are invariant under adding a forced relation.
    return dict(status='OWN_EXACT_RANK_UPDATE_CHECKS_PASS', cases=checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gamma')
    parser.add_argument('--batch')
    parser.add_argument('--closed-pairs', type=int, nargs='+', default=[1])
    parser.add_argument('--producer-certified-psd-rank30', action='store_true')
    parser.add_argument('--output', required=True)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.self_test:
        report = self_test()
    elif not args.producer_certified_psd_rank30:
        parser.error('Producer PSD/rank30 certification must be explicitly supplied.')
    elif args.batch:
        start = time.perf_counter()
        data = json.loads(Path(args.batch).read_text(encoding='utf-8-sig'))
        order = [tuple(p) for p in data['labels']]
        index = [S.index(p) for p in order]
        counts = Counter()
        statuses = Counter()
        candidates = []
        details = output.with_suffix('.jsonl')
        with details.open('w', encoding='utf-8') as handle:
            for seed_index, entry in enumerate(data['structures']):
                gamma = [[0]*34 for _ in range(34)]
                for i, j in entry['edges']:
                    gamma[index[i]][index[j]] = gamma[index[j]][index[i]] = 1
                try:
                    result = scan(gamma, args.closed_pairs,
                                  output.parent/f'candidates_seed_{seed_index}')
                    counts.update(result['counts'])
                    candidates.extend(dict(seed_index=seed_index, **c) for c in result['candidates'])
                except ValueError as exc:
                    result = dict(status='INPUT_NOT_APPLICABLE', reason=str(exc))
                result['seed_index'] = seed_index
                statuses[result['status']] += 1
                handle.write(json.dumps(result)+'\n')
                handle.flush()
                if (seed_index+1) % 100 == 0:
                    print(json.dumps(dict(processed=seed_index+1, counts=dict(counts))), flush=True)
        report = dict(status='FINITE_BATCH_KERNEL_MOVING_SCAN',
                      input=args.batch, seed_count=len(data['structures']),
                      input_statuses=dict(statuses), counts=dict(counts),
                      candidates=candidates, details=str(details),
                      elapsed_seconds=time.perf_counter()-start,
                      scope='Only the supplied finite batch and single specified rectangle trades. No conclusion for all admissible three-star structures.')
    else:
        report = scan(load_gamma(args.gamma), args.closed_pairs, output.parent/'connected_repairs')
        report['input'] = args.gamma
    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key:value for key, value in report.items()
                      if key in ('status', 'counts', 'input_statuses', 'elapsed_seconds', 'cases')}))


if __name__ == '__main__':
    main()
