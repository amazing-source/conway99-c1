"""Bounded exact-integer mask pilot, including H+2 pair coexistence.

A witness satisfies necessary incidence constraints only, not SRG completion.
An INFEASIBLE solver result is recorded as unproved, never a certified exclusion.
"""
import argparse
from collections import Counter
import json
import time

import numpy as np
from ortools.sat.python import cp_model
import sympy as sp

from twisted_prism_extension import ROOT, model, matrix, projectors


def pair_statuses(a, masks, k=14):
    common = masks @ masks.T
    adjacent = common <= 1
    nonadjacent = common <= 2
    inside = masks @ a
    for u in range(len(a)):
        adjacent &= inside[:, u, None]+masks[None, :, u] <= 2-masks[:, u, None]
    adjacent &= adjacent.T.copy()
    for gram, diagonal, constant, coefficient in projectors(a, k):
        q = sp.Matrix(gram.tolist())
        indices = list(q.rref()[1])
        inv = q.extract(indices, indices).inv()
        den = int(sp.ilcm(*[entry.q for entry in inv]))
        numerator = np.array((den*inv).tolist(), dtype=object)
        cross = (constant+coefficient*masks).astype(object)
        restricted = cross[:, indices]
        products = restricted @ numerator
        assert np.all(products @ gram[:, indices].T == den*cross)
        inner = products @ restricted.T
        residual = diagonal*den-np.diag(inner)
        assert np.all(residual >= 0)
        product = residual[:, None]*residual[None, :]
        for status, allowed in ((0, nonadjacent), (1, adjacent)):
            off = (constant+coefficient*status)*den-inner
            allowed &= np.asarray(off*off <= product, dtype=bool)
    return adjacent, nonadjacent


def verify_witness(masks, m, rhs, upper, allowed, witness):
    by_mask = {sum(int(v) << i for i, v in enumerate(b)): j for j, b in enumerate(masks)}
    x = np.zeros(len(masks), dtype=np.int64)
    for item in witness:
        assert type(item['count']) is int and 0 < item['count'] <= 243
        x[by_mask[item['mask']]] += item['count']
    assert np.all(x <= upper) and np.array_equal(m @ x, rhs)
    if allowed is not None:
        support = np.flatnonzero(x)
        for i in support:
            assert x[i] <= 1 or allowed[i, i]
            for j in support:
                if i != j:
                    assert allowed[i, j]


def solve(masks, m, rhs, upper, allowed, seconds):
    p = cp_model.CpModel()
    caps = upper.copy()
    if allowed is not None:
        caps[~np.diag(allowed)] = 1
    # Each positive entry in an incidence column gives another valid cap.
    for j in range(len(caps)):
        caps[j] = min(int(caps[j]), *(int(rhs[i]) for i in np.flatnonzero(m[:, j])))
    xs = [p.new_int_var(0, int(u), f'x{j}') for j, u in enumerate(caps)]
    for row, target in zip(m, rhs):
        p.add(sum(xs[j] for j in np.flatnonzero(row)) == int(target))
    conflicts = []
    if allowed is not None:
        present = [p.new_bool_var(f'p{j}') for j in range(len(xs))]
        for x, flag, cap in zip(xs, present, caps):
            p.add(x <= int(cap)*flag)
            p.add(x >= flag)
        conflicts = list(zip(*np.where(np.triu(~allowed, k=1))))
        for i, j in conflicts:
            p.add(present[i]+present[j] <= 1)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    started = time.monotonic()
    status = solver.solve(p)
    out = {'solver_status': solver.status_name(status), 'seconds': time.monotonic()-started,
           'distinct_mask_conflicts': len(conflicts)}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        out['status'] = 'exact_incidence_witness_only'
        out['witness'] = [
            {'mask': sum(int(v) << i for i, v in enumerate(masks[j])), 'count': solver.value(x)}
            for j, x in enumerate(xs) if solver.value(x)]
        verify_witness(masks, m, rhs, upper, allowed, out['witness'])
    elif status == cp_model.INFEASIBLE:
        out['status'] = 'solver_infeasible_not_certified'
    else:
        out['status'] = 'unresolved'
    return out


def positive_control(core_report):
    a = np.zeros((243, 243), dtype=np.int64)
    for line in (ROOT/'data/srg243/twin243_switched.edges').read_text().splitlines():
        u, v = map(int, line.split())
        a[u, v] = a[v, u] = 1
    core = core_report['positive_control']['core']
    h = a[np.ix_(core, core)]
    masks, m, rhs, upper, _ = model(h, 22)
    adjacent, nonadjacent = pair_statuses(h, masks, 22)
    index = {tuple(b): i for i, b in enumerate(masks.tolist())}
    outside = sorted(set(range(243))-set(core))
    labels = [index[tuple(a[u, core].tolist())] for u in outside]
    for i, u in enumerate(outside):
        for j in range(i):
            v = outside[j]
            assert (adjacent if a[u, v] else nonadjacent)[labels[i], labels[j]]
    counts = Counter(labels)
    witness = [{'mask': sum(int(v) << i for i, v in enumerate(masks[j])), 'count': count}
               for j, count in counts.items()]
    verify_witness(masks, m, rhs, upper, adjacent | nonadjacent, witness)
    return {'actual_outside_vertices': len(outside), 'actual_pairs_retained': len(outside)*(len(outside)-1)//2}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    parser.add_argument('--stride', type=int, default=12)
    parser.add_argument('--seconds', type=float, default=2)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    core_report = json.loads((ROOT/'data/codex_twisted_prism_core.json').read_text())
    extension = json.loads((ROOT/'data/codex_twisted_prism_extension.json').read_text())
    edges = [tuple(e) for e in core_report['optional_edges']]
    pool = [r['bits'] for r in extension['results'] if r['status'] == 'lp_feasible_unresolved']
    from pathlib import Path
    outpath = Path(args.out)
    if args.verify_only:
        report = json.loads(outpath.read_text())
        assert [r['bits'] for r in report['results']] == pool[::report['stride']]
        assert report['positive_control'] == positive_control(core_report)
        for row in report['results']:
            a = matrix(row['bits'], edges)
            masks, m, rhs, upper, _ = model(a)
            adj, nonadj = pair_statuses(a, masks)
            for key, allowed in [('integer_only', None), ('coexistence', adj | nonadj)]:
                if row[key]['status'] == 'exact_incidence_witness_only':
                    verify_witness(masks, m, rhs, upper, allowed, row[key]['witness'])
        print('All archived witnesses and actual positive-control pairs verified exactly')
        return
    report = {'scope': 'necessary integer incidence and H+2 pair-coexistence constraints only',
              'stride': args.stride, 'per_core_solver_seconds': args.seconds,
              'positive_control': positive_control(core_report), 'results': []}
    for bits in pool[::args.stride]:
        a = matrix(bits, edges)
        masks, m, rhs, upper, _ = model(a)
        adj, nonadj = pair_statuses(a, masks)
        row = {'bits': bits, 'masks': len(masks),
               'integer_only': solve(masks, m, rhs, upper, None, args.seconds),
               'coexistence': solve(masks, m, rhs, upper, adj | nonadj, args.seconds)}
        report['results'].append(row)
        print(json.dumps({'bits': bits, 'masks': len(masks),
                          'integer': row['integer_only']['status'],
                          'coexistence': row['coexistence']['status'],
                          'conflicts': row['coexistence']['distinct_mask_conflicts']}), flush=True)
        outpath.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
