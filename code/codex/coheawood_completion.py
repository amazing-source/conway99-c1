"""Exact C1 completion with two Hoffman cocliques meeting in 15 points.

Canonical boundary: co-Heawood on S+T (7+7), 70 vertices indexed by
the 49 pairs, and a 15-coclique Z. The only WLOG normalisation fixes
the six-vertex matching in each S-row, by swapping the two labels in
each of its three double cells. No symmetry of the completed graph
is imposed. A time limit is not an infeasibility result.
"""
from itertools import combinations
import argparse
import json
from pathlib import Path
import time
from ortools.sat.python import cp_model


def boundary():
    b = [[(s & t).bit_count() % 2 for t in range(1, 8)] for s in range(1, 8)]
    names = [('s', s) for s in range(7)] + [('t', t) for t in range(7)]
    cells = {}
    for s in range(7):
        for t in range(7):
            cells[s, t] = []
            for k in range(2-b[s][t]):
                cells[s, t].append(len(names))
                names.append(('r', s, t, k))
    assert len(names) == 84
    names += [('z', z) for z in range(15)]
    a = [[None]*99 for _ in range(99)]

    def fix(u, v, val):
        assert a[u][v] is None or a[u][v] == val
        a[u][v] = a[v][u] = val

    for u in range(99):
        fix(u, u, 0)
    for u in range(14):
        for v in range(99):
            if v < 14:
                val = b[u][v-7] if u < 7 <= v else b[v][u-7] if v < 7 <= u else 0
            elif v < 84:
                _, s, t, _ = names[v]
                val = int(u == s or u == 7+t)
            else:
                val = 0
            fix(u, v, val)
    for u in range(84, 99):
        for v in range(84, 99):
            fix(u, v, 0)
    for s in range(7):
        row = [r for t in range(7) for r in cells[s, t]]
        zero = [t for t in range(7) if not b[s][t]]
        e0, e1, e2 = [cells[s, t] for t in zero]
        pairs = {tuple(sorted(e)) for e in [(e0[0],e1[0]),(e1[1],e2[0]),(e2[1],e0[1])]}
        for u, v in combinations(row, 2):
            fix(u, v, int((u, v) in pairs))
    for t in range(7):
        col = [r for s in range(7) for r in cells[s, t]]
        for u, v in combinations(col, 2):
            # The four flag vertices are paired with the corresponding S
            # vertices in N(t), so have no neighbours in this column.
            if b[names[u][1]][t] or b[names[v][1]][t]:
                fix(u, v, 0)
    return a, names, b, cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=45)
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--output', required=True)
    ap.add_argument('--linear-only', action='store_true')
    ap.add_argument('--canonical-z', action='store_true',
                    help='Order all 15 Z points by their distinct masks in the first S row')
    ap.add_argument('--log-progress', action='store_true')
    ap.add_argument('--cuts', help='JSON of exact global spectral cuts to reuse')
    ap.add_argument('--no-presolve', action='store_true')
    args = ap.parse_args()
    start = time.monotonic()
    a, names, b, cells = boundary()
    m = cp_model.CpModel()
    edges = {}
    for u, v in combinations(range(99), 2):
        if a[u][v] is None:
            x = m.NewBoolVar(f'e_{u}_{v}')
            edges[u, v] = x
            a[u][v] = a[v][u] = x
    for u in range(14, 99):
        m.Add(sum(a[u]) == 14)
    for u in range(14, 84):
        m.Add(sum(a[u][84:]) == 3)
    # Every Z point has two neighbours in the first S row. These pairs
    # are distinct: a repeated pair would have S[0] plus two Z common
    # neighbours. Thus sorting their 10-bit masks removes the ENTIRE
    # S_15 labelling freedom, without imposing a graph automorphism.
    if args.canonical_z:
        first_row = [r for t in range(7) for r in cells[0, t]]
        masks = [sum((1 << i)*a[r][z] for i, r in enumerate(first_row))
                 for z in range(84, 99)]
        for left, right in zip(masks, masks[1:]):
            m.Add(left < right)
    else:
        for z in range(84, 99):
            m.Add(a[14][z] == int(z < 87))
    products = 0
    for u, v in combinations(range(99), 2):
        if args.linear_only and u >= 14 and v >= 14:
            continue
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
                y = m.NewBoolVar(f'w_{u}_{v}_{w}')
                m.AddMultiplicationEquality(y, [p, q])
                terms.append(y)
                products += 1
        m.Add(sum(terms) + a[u][v] == 2)
    cut_count = 0
    if args.cuts:
        from coheawood_global_cuts import add_spectral_cut
        cuts = json.loads(Path(args.cuts).read_text(encoding='utf-8'))['spectral_cuts']
        for cut in cuts:
            add_spectral_cut(m, a, cut)
        cut_count = len(cuts)
    build_seconds = time.monotonic()-start
    print(json.dumps(dict(event='built', edge_variables=len(edges), products=products,
                          build_seconds=build_seconds, linear_only=args.linear_only)), flush=True)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = 20261012
    solver.parameters.log_search_progress = args.log_progress
    solver.parameters.cp_model_presolve = not args.no_presolve
    status = solver.Solve(m)
    report = dict(status=solver.StatusName(status), scope='co-Heawood branch',
                  linear_only=args.linear_only, seconds=solver.WallTime(),
                  canonical_z=args.canonical_z,
                  spectral_cuts=cut_count, presolve=not args.no_presolve,
                  build_seconds=build_seconds, edge_variables=len(edges),
                  products=products, conflicts=solver.NumConflicts(),
                  branches=solver.NumBranches(), solver_stats=solver.ResponseStats())
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        adj = [[x if isinstance(x, int) else solver.Value(x) for x in row] for row in a]
        report['adjacency'] = adj
        errors = [(u,v,sum(adj[u][w]*adj[v][w] for w in range(99)))
                  for u,v in combinations(range(99),2)
                  if sum(adj[u][w]*adj[v][w] for w in range(99)) != 2-adj[u][v]]
        report['full_srg_errors'] = len(errors)
        if not args.linear_only:
            assert not errors and all(sum(row)==14 for row in adj)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('adjacency','solver_stats')}), flush=True)


if __name__ == '__main__':
    main()
