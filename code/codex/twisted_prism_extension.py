"""Bounded pilot: simultaneous outside-mask multiplicities for all 310 cores.

All local filters and exclusion certificates use exact integers/rationals.
LP feasibility is only a surviving relaxation, never an SRG completion.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog
import sympy as sp

from twisted_prism_core import ROOT, matrix, PAIRS


def projectors(a, k):
    n = len(a)
    if k == 14:
        return [(27*np.eye(n, dtype=np.int64)-9*a+1, 28, 1, -9),
                (44*np.eye(n, dtype=np.int64)+11*a-2, 42, -2, 11)]
    assert k == 22
    return [(108*np.eye(n, dtype=np.int64)-27*a+2, 110, 2, -27),
            (45*np.eye(n, dtype=np.int64)+9*a-1, 44, -1, 9)]


def spectral_masks(a, candidates, k):
    for gram, diagonal, constant, coefficient in projectors(a, k):
        q = sp.Matrix(gram.tolist())
        indices = list(q.rref()[1])
        inverse = q.extract(indices, indices).inv()
        den = int(sp.ilcm(*[x.q for x in inverse]))
        numerator = np.array((den*inverse).tolist(), dtype=object)
        cross = (constant+coefficient*candidates).astype(object)
        restricted = cross[:, indices]
        products = restricted@numerator
        values = np.sum(products*restricted, axis=1)
        keep = values <= diagonal*den
        if len(indices) != len(a):
            keep &= np.all(products@gram[:, indices].T == den*cross, axis=1)
        candidates = candidates[np.asarray(keep, dtype=bool)]
        if not len(candidates):
            break
    return candidates


def model(a, k=14):
    # All outside vertices have zero or one neighbour in the distinguished S.
    candidates = []
    for s in range(-1, 6):
        for bits in range(256):
            candidates.append([int(i == s) for i in range(6)]+[(bits >> j) & 1 for j in range(8)])
    candidates = np.array(candidates, dtype=np.int64)
    deficit = 2-a-a@a
    keep = np.all(candidates@a <= 2-candidates, axis=1)
    for u, v in PAIRS:
        if deficit[u, v] == 0:
            keep &= (candidates[:, u]*candidates[:, v] == 0)
    candidates = candidates[keep]
    before_spectral = len(candidates)
    candidates = spectral_masks(a, candidates, k)
    rows = [np.ones(len(candidates), dtype=np.int64)]
    rows += [candidates[:, u] for u in range(14)]
    rows += [candidates[:, u]*candidates[:, v] for u, v in PAIRS]
    constraints = np.array(rows, dtype=np.int64)
    n = 1+k*k//2
    rhs = np.r_[n-14, k-a.sum(axis=0), [deficit[u, v] for u, v in PAIRS]].astype(np.int64)
    cell_sizes = [k-5, k-5, k-6, k-5, k-5, k-6]
    empty_size = k*k//2-6*k+19
    upper = np.array([sum(int(b[i])*cell_sizes[i] for i in range(6)) if b[:6].any()
                      else empty_size for b in candidates], dtype=np.int64)
    return candidates, constraints, rhs, upper, before_spectral


def certify_infeasible(m, b, upper):
    if not len(upper):
        y = [-1]+[0]*(len(b)-1)
        return {'row_multipliers': y, 'box_lower_bound': 0, 'target': -int(b[0])}
    result = linprog(b, A_ub=-m.T, b_ub=np.zeros(m.shape[1]),
                     bounds=[(-1, 1)]*len(b), method='highs')
    if not result.success or result.fun >= -1e-8:
        return None
    for scale in (1, 10, 100, 1000, 10000, 100000, 1000000):
        y = np.rint(scale*result.x).astype(np.int64)
        coeff = y@m
        lower = sum(min(0, int(x)*int(u)) for x, u in zip(coeff, upper))
        target = sum(int(x)*int(t) for x, t in zip(y, b))
        if lower > target:
            return {'row_multipliers': y.tolist(), 'box_lower_bound': lower, 'target': target}
    return None


def verify_certificate(m, b, upper, cert):
    y = cert['row_multipliers']
    assert len(y) == len(b) and all(type(v) is int for v in y)
    coeff = [sum(v*int(m[i, j]) for i, v in enumerate(y)) for j in range(m.shape[1])]
    lower = sum(min(0, c*int(u)) for c, u in zip(coeff, upper))
    target = sum(v*int(t) for v, t in zip(y, b))
    assert cert['box_lower_bound'] == lower > target == cert['target']


def positive_control(core_report, edges):
    control = core_report['positive_control']
    a = np.zeros((243, 243), dtype=np.int64)
    for line in (ROOT/'data/srg243/twin243_switched.edges').read_text().splitlines():
        u, v = map(int, line.split())
        a[u, v] = a[v, u] = 1
    core = control['core']
    h = a[np.ix_(core, core)]
    masks, m, b, upper, _ = model(h, 22)
    index = {tuple(mask): i for i, mask in enumerate(masks.tolist())}
    actual = np.zeros(len(masks), dtype=np.int64)
    for u in set(range(243))-set(core):
        actual[index[tuple(a[u, core].tolist())]] += 1
    assert np.array_equal(m@actual, b) and np.all(actual <= upper)
    return {'actual_outside_vertices': int(actual.sum()), 'allowed_masks': len(masks),
            'used_masks': int(np.count_nonzero(actual)), 'all_actual_masks_retained': True,
            'all_integer_moment_equations': 'passed'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cores', type=Path, default=ROOT/'data/codex_twisted_prism_core.json')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--seconds', type=float, default=180)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    core_report = json.loads(args.cores.read_text(encoding='utf-8'))
    edges = [tuple(e) for e in core_report['optional_edges']]
    if args.verify_only:
        report = json.loads(args.out.read_text(encoding='utf-8'))
        expected = [r['bits'] for r in core_report['cores'] if r['passes_two_real_projectors']]
        seen = [r['bits'] for r in report['results']]
        assert seen == expected[:len(seen)]
        assert report['complete_over_310'] == (len(seen) == len(expected))
        assert report['counts'] == dict(Counter(r['status'] for r in report['results']))
        assert report['positive_control'] == positive_control(core_report, edges)
        for row in report['results']:
            if row['status'] != 'excluded_exact':
                continue
            _, m, b, upper, before = model(matrix(row['bits'], edges))
            assert row['masks_before_spectral'] == before and row['masks_after_spectral'] == len(upper)
            verify_certificate(m, b, upper, row['certificate'])
        print('Exact exclusion certificates and positive control verified')
        return
    started = time.monotonic()
    report = {'scope': 'necessary fractional mask-multiplicity relaxation, not SRG completion',
              'positive_control': positive_control(core_report, edges), 'results': []}
    cores = [r for r in core_report['cores'] if r['passes_two_real_projectors']]
    for i, row in enumerate(cores):
        if time.monotonic()-started > args.seconds:
            break
        _, m, b, upper, before = model(matrix(row['bits'], edges))
        entry = {'bits': row['bits'], 'masks_before_spectral': before, 'masks_after_spectral': len(upper)}
        result = None if not len(upper) else linprog(np.zeros(len(upper)), A_eq=m, b_eq=b,
                                                    bounds=list(zip(np.zeros(len(upper)), upper)), method='highs')
        if result is None or result.status == 2:
            cert = certify_infeasible(m, b, upper)
            if cert:
                verify_certificate(m, b, upper, cert)
                entry.update(status='excluded_exact', certificate=cert)
            else:
                entry['status'] = 'numerically_infeasible_uncertified'
        else:
            entry['status'] = 'lp_feasible_unresolved' if result.success else 'solver_unknown'
        report['results'].append(entry)
        if (i+1) % 50 == 0:
            print(json.dumps({'done': i+1, 'statuses': dict(Counter(r['status'] for r in report['results']))}), flush=True)
    report['complete_over_310'] = len(report['results']) == len(cores)
    report['counts'] = dict(Counter(r['status'] for r in report['results']))
    report['elapsed_seconds'] = time.monotonic()-started
    args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('complete_over_310', 'counts', 'elapsed_seconds', 'positive_control')}))


if __name__ == '__main__':
    main()
