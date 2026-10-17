"""Shared integer populations and complete stars around a norm-18 core.

This is a necessary relaxation, not an SRG constructor. No spectral or
floating point rejection is used. The core is the bipartite 4-regular
induced graph on two independent 9-sets. Types are generated exhaustively
from the local SRG bounds, including j=4 (never silently omitted).
"""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import time

from ortools.sat.python import cp_model


def prepare(incidence):
    assert len(incidence) == 9 and all(len(r) == 9 for r in incidence)
    assert all(v in (0, 1) for r in incidence for v in r)
    assert all(sum(r) == 4 for r in incidence)
    assert all(sum(incidence[i][j] for i in range(9)) == 4 for j in range(9))
    B = [[0] * 18 for _ in range(18)]
    for i in range(9):
        for j in range(9):
            B[i][9+j] = B[9+j][i] = incidence[i][j]
    K = [[12 * (i == j) + 2 - B[i][j]
          - sum(B[i][v] * B[v][j] for v in range(18))
          for j in range(18)] for i in range(18)]
    assert all(K[i][j] >= 0 for i in range(18) for j in range(18))
    types = []
    # A selected P-vertex has 4 Q-neighbours; its unique triangle allows
    # at most one of these to lie in the chosen Q-set. Thus j<=6. The
    # complete local conditions below also test j=4,5,6 explicitly.
    for j in range(7):
        sides = []
        for side in (range(9), range(9, 18)):
            sides.append([s for s in combinations(side, j)
                          if all(K[a][b] >= 1 for a, b in combinations(s, 2))])
        for left in sides[0]:
            for right in sides[1]:
                support = left + right
                mask = sum(1 << a for a in support)
                demand = [2 - ((mask >> a) & 1) - sum(B[a][b] for b in support)
                          for a in range(18)]
                if min(demand) < 0:
                    continue
                types.append(dict(mask=mask, j=j, support=list(support), demand=demand))
    return B, K, types


def build(incidence, root=None, fixed_population=None, complete_star=False,
          population_triples=False):
    B, K, types = prepare(incidence)
    model = cp_model.CpModel()
    population = []
    for t, item in enumerate(types):
        supp = item['support']
        cap = min([81] + [K[a][b] for a, b in combinations(supp, 2)])
        population.append(model.NewIntVar(0, cap, f'n{t}'))
    model.Add(sum(population) == 81)
    for a in range(18):
        model.Add(sum(population[t] for t, s in enumerate(types) if a in s['support']) == 10)
        for b in range(a+1, 18):
            model.Add(sum(population[t] for t, s in enumerate(types)
                          if a in s['support'] and b in s['support']) == K[a][b])
    # Any three vertices have at most one common neighbour, since any
    # two vertices have at most two. Account also for neighbours in B.
    if population_triples:
        for triple in combinations(range(18), 3):
            core_common = sum(all(B[a][b] for a in triple) for b in range(18))
            terms = [population[t] for t, s in enumerate(types)
                     if all(a in s['support'] for a in triple)]
            if terms or core_common > 1:
                model.Add(sum(terms) <= 1-core_common)
    if fixed_population is not None:
        assert len(fixed_population) == len(types)
        for var, value in zip(population, fixed_population):
            model.Add(var == value)
    selected = {}; mates = {}
    if root is not None:
        root_type = types[root]
        model.Add(population[root] >= 1)
        root_mask = root_type['mask']
        for t, item in enumerate(types):
            common = (root_mask & item['mask']).bit_count()
            if common > 1:
                continue
            # A root-neighbour cannot spend a coordinate of zero demand.
            if any(root_type['demand'][a] == 0 for a in item['support']):
                continue
            selected[t] = model.NewIntVar(0, 14, f'y{t}')
            model.Add(selected[t] <= population[t] - int(t == root))
        model.Add(sum(selected.values()) == 14-2*root_type['j'])
        for a in range(18):
            model.Add(sum(var for t, var in selected.items() if a in types[t]['support'])
                      == root_type['demand'][a])
        if complete_star:
            # Two outside neighbours of the root cannot share two more
            # common neighbours in the core. This also bounds repeated types.
            for a, b in combinations(range(18), 2):
                model.Add(sum(var for t, var in selected.items()
                              if a in types[t]['support'] and b in types[t]['support']) <= 1)
            free = [t for t in selected if not (types[t]['mask'] & root_mask)]
            incident = {t: [] for t in free}
            for i, t in enumerate(free):
                for s in free[i:]:
                    if types[t]['mask'] & types[s]['mask']:
                        continue
                    z = model.NewIntVar(0, 7, f'm{t}_{s}')
                    mates[t, s] = z
                    incident[t].append((2 if t == s else 1)*z)
                    if t != s:
                        incident[s].append(z)
            for t in free:
                model.Add(sum(incident[t]) == selected[t])
    return model, types, population, selected, mates


def run(args):
    raw = args.cores.read_bytes()
    entry = next(c for c in json.loads(raw)['classes'] if c['index'] == args.core)
    incidence = entry['incidence_rows_points_columns_blocks']
    _, _, types = prepare(incidence)
    roots = [i for i, t in enumerate(types) if t['j'] == args.root_j]
    root = roots[args.root_number] if args.root_j >= 0 else None
    fixed = json.loads(args.population.read_text())['population'] if args.population else None
    model, types, population, selected, mates = build(
        incidence, root, fixed, args.complete_star, args.population_triples)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 1
    start = time.monotonic()
    status = solver.Solve(model)
    report = dict(core=args.core, incidence=incidence, root=root,
                  root_type=types[root] if root is not None else None,
                  complete_star=args.complete_star, population_triples=args.population_triples,
                  type_counts={j: sum(t['j'] == j for t in types) for j in range(7)},
                  status=solver.StatusName(status), elapsed=time.monotonic()-start,
                  variables=len(model.Proto().variables), constraints=len(model.Proto().constraints),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  cores_sha256=hashlib.sha256(raw).hexdigest(),
                  scope='Necessary shared-population/star relaxation; feasibility is not an SRG')
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        report['population'] = [solver.Value(v) for v in population]
        report['selected'] = {str(t): solver.Value(v) for t, v in selected.items() if solver.Value(v)}
        report['mates'] = {f'{a},{b}': solver.Value(v) for (a,b), v in mates.items() if solver.Value(v)}
        report['used_types'] = {str(t): types[t] for t, n in enumerate(report['population']) if n}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('core','root','status','elapsed','variables','constraints','type_counts')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cores', required=True, type=Path)
    parser.add_argument('--core', type=int, default=3)
    parser.add_argument('--root-j', type=int, default=3)
    parser.add_argument('--root-number', type=int, default=0)
    parser.add_argument('--complete-star', action='store_true')
    parser.add_argument('--population-triples', action='store_true')
    parser.add_argument('--population', type=Path)
    parser.add_argument('--seconds', type=float, default=10)
    parser.add_argument('--out', required=True, type=Path)
    run(parser.parse_args())
