"""Global integer search with exact spectral cuts for the co-Heawood branch.

For any 14-regular simple graph on 99 vertices, simultaneous PSD of
27I-9A+J and 44I+11A-2J is equivalent to SRG(99,14,1,2).
Floating eigenvectors only propose cuts. Every retained cut is an exact
integer Rayleigh inequality, and every claimed construction is checked
by the integer SRG identity. A time limit is never an exclusion.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time

import numpy as np
from ortools.sat.python import cp_model
from coheawood_completion import boundary


def build_master():
    a, names, b, cells = boundary()
    m = cp_model.CpModel()
    for u, v in combinations(range(99), 2):
        if a[u][v] is None:
            a[u][v] = a[v][u] = m.NewBoolVar(f'e_{u}_{v}')
    for u in range(14, 99):
        m.Add(sum(a[u]) == 14)
    for u in range(14, 84):
        m.Add(sum(a[u][84:]) == 3)
    for u in range(14):
        for v in range(u+1, 99):
            m.Add(sum(a[v][w] for w in range(99) if a[u][w]) + a[u][v] == 2)
    first_row = [r for t in range(7) for r in cells[0, t]]
    masks = [sum((1 << i)*a[r][z] for i, r in enumerate(first_row))
             for z in range(84, 99)]
    for left, right in zip(masks, masks[1:]):
        m.Add(left < right)
    return m, a


def add_pair(m, a, u, v):
    terms = []
    for w in range(99):
        p, q = a[u][w], a[v][w]
        if isinstance(p, int):
            if p:
                terms.append(q)
        elif isinstance(q, int):
            if q:
                terms.append(p)
        else:
            y = m.NewBoolVar(f'pair_{u}_{v}_{w}')
            m.AddMultiplicationEquality(y, [p, q])
            terms.append(y)
    m.Add(sum(terms) + a[u][v] == 2)


def integer_cuts(adj, scale=64):
    for kind, gram in [('upper', 27*np.eye(99)-9*adj+np.ones((99,99))),
                       ('lower', 44*np.eye(99)+11*adj-2*np.ones((99,99)))]:
        vals, vecs = np.linalg.eigh(gram)
        for i in np.flatnonzero(vals < -1e-7):
            vec = vecs[:, i]
            z = np.rint(scale*vec/max(abs(vec))).astype(np.int64)
            norm, total = int(z@z), int(z.sum())
            az = int(z@adj@z)
            rayleigh = (27*norm-9*az+total*total if kind == 'upper'
                        else 44*norm+11*az-2*total*total)
            if rayleigh < 0:
                yield dict(kind=kind, vector=z.tolist(), violation=rayleigh)


def add_spectral_cut(m, a, cut):
    z = cut['vector']
    norm, total = sum(x*x for x in z), sum(z)
    expr = sum(z[u]*z[v]*a[u][v] for u, v in combinations(range(99), 2)
               if z[u] and z[v])
    if cut['kind'] == 'upper':
        m.Add(18*expr <= 27*norm+total*total)
    else:
        m.Add(22*expr >= 2*total*total-44*norm)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=240)
    ap.add_argument('--per-solve', type=float, default=30)
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--pairs-per-round', type=int, default=12)
    ap.add_argument('--resume', help='Reuse all exact cuts and pair equations from a prior run')
    ap.add_argument('--no-presolve', action='store_true')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    start = time.monotonic()
    m, a = build_master()
    report = dict(scope='entire co-Heawood branch', status='RUNNING',
                  method='global exact integer spectral cuts and lazy pair equations',
                  iterations=[], spectral_cuts=[], pair_equations=[])
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    seen, pairs = set(), set()
    if args.resume:
        prior = json.loads(Path(args.resume).read_text(encoding='utf-8'))
        for cut in prior['spectral_cuts']:
            add_spectral_cut(m,a,cut)
            seen.add((cut['kind'],tuple(cut['vector'])))
            report['spectral_cuts'].append(cut)
        for u,v in prior['pair_equations']:
            add_pair(m,a,u,v)
            pairs.add((u,v))
            report['pair_equations'].append([u,v])
        report['resumed_from'] = args.resume
    report['presolve'] = not args.no_presolve
    iteration = 0
    while time.monotonic()-start < args.seconds:
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = min(args.per_solve, args.seconds-(time.monotonic()-start))
        solver.parameters.num_search_workers = args.workers
        solver.parameters.random_seed = 20261012+iteration
        solver.parameters.cp_model_presolve = not args.no_presolve
        status = solver.Solve(m)
        rec = dict(iteration=iteration, solver_status=solver.StatusName(status),
                   solve_seconds=solver.WallTime(), conflicts=solver.NumConflicts(),
                   branches=solver.NumBranches())
        if status == cp_model.INFEASIBLE:
            report['status'] = 'INFEASIBLE'
        elif status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            adj = np.array([[x if isinstance(x, int) else solver.Value(x) for x in row]
                            for row in a], dtype=np.int64)
            err = adj@adj+adj-12*np.eye(99,dtype=np.int64)-2*np.ones((99,99),dtype=np.int64)
            bad = [(u,v,int(err[u,v])) for u,v in combinations(range(99),2) if err[u,v]]
            vals = np.linalg.eigvalsh(adj)
            rec.update(pair_errors=len(bad), least_eigenvalue=float(vals[0]),
                       second_eigenvalue=float(vals[-2]))
            if not bad:
                assert all(adj.sum(axis=1) == 14) and np.array_equal(adj, adj.T)
                report['status'] = 'SRG_FOUND'
                report['adjacency'] = adj.tolist()
            else:
                newcuts = 0
                for cut in integer_cuts(adj):
                    key = (cut['kind'], tuple(cut['vector']))
                    if key in seen:
                        continue
                    seen.add(key)
                    add_spectral_cut(m, a, cut)
                    report['spectral_cuts'].append(cut)
                    newcuts += 1
                rec['new_spectral_cuts'] = newcuts
                for u,v,e in sorted(bad, key=lambda t:(-abs(t[2]), t[:2]))[:args.pairs_per_round]:
                    if (u,v) not in pairs:
                        add_pair(m,a,u,v)
                        pairs.add((u,v))
                        report['pair_equations'].append([u,v])
                rec['total_pair_equations'] = len(pairs)
                assert newcuts or args.pairs_per_round
        report['iterations'].append(rec)
        report['elapsed_seconds'] = time.monotonic()-start
        out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(rec),flush=True)
        if report['status'] != 'RUNNING':
            break
        if status == cp_model.UNKNOWN:
            # Re-solving the identical model with the same budget would
            # simply repeat a possibly unfinished presolve. Keep the cuts
            # for an explicit strategy change instead.
            report['status'] = 'UNKNOWN'
            break
        iteration += 1
    if report['status'] == 'RUNNING':
        report['status'] = 'UNKNOWN'
    report['elapsed_seconds'] = time.monotonic()-start
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=report['status'], iterations=len(report['iterations']),
                         cuts=len(report['spectral_cuts']), elapsed=report['elapsed_seconds'])),flush=True)


if __name__ == '__main__':
    main()
