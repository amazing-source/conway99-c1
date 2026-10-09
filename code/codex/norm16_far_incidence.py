"""Pilot of D--Z incidences in note251, using saved norm-16 attachments.

This is a necessary local model, not a completion of a Conway graph.
"""
import argparse
import json
from itertools import combinations
from pathlib import Path
import time

from ortools.sat.python import cp_model

ROOT = Path(__file__).resolve().parents[2]


def incidence_model(attachment, forest, d_edge=None):
    model = cp_model.CpModel()
    core_sets = [set(row[:2]) | {8+q for q in row[2:]} for row in attachment]
    az = forest['adjacency_Z']
    ad = [[0]*8 for _ in range(8)]
    if d_edge is not None:
        i, j = d_edge
        ad[i][j] = ad[j][i] = 1
    x = [[model.new_bool_var(f'D{i}Z{j}') for j in range(11)] for i in range(8)]
    for i in range(8):
        model.add(sum(x[i]) == 4+sum(ad[i]))
    for j in range(11):
        model.add(sum(x[i][j] for i in range(8)) == 2+sum(az[j]))
    products = {}

    def both(a, b):
        key = tuple(sorted((a.index, b.index)))
        if key not in products:
            v = model.new_bool_var(f'and{key[0]}_{key[1]}')
            model.add(v <= a)
            model.add(v <= b)
            model.add(v >= a+b-1)
            products[key] = v
        return products[key]

    for i, j in combinations(range(8), 2):
        cap = 2-ad[i][j]-len(core_sets[i] & core_sets[j])
        model.add(sum(both(x[i][z], x[j][z]) for z in range(11)) <= cap)
    for z, w in combinations(range(11), 2):
        cap = 2-az[z][w]-sum(az[z][k]*az[w][k] for k in range(11))
        model.add(sum(both(x[i][z], x[i][w]) for i in range(8)) <= cap)
    for i in range(8):
        for z in range(11):
            common = sum(x[i][w] for w in range(11) if az[z][w])
            common += sum(x[j][z] for j in range(8) if ad[i][j])
            model.add(common <= 2-x[i][z])
    # Only permutations of Z are broken: equal isolated vertices have equal
    # roles, and sorting their incidence columns does not lose any type.
    isolates = [z for z in range(11) if not any(az[z])]
    for z, w in zip(isolates, isolates[1:]):
        model.add(sum((1 << i)*x[i][z] for i in range(8))
                  <= sum((1 << i)*x[i][w] for i in range(8)))
    return model, x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int, default=0)
    parser.add_argument('--orbit', type=int, default=0)
    parser.add_argument('--forest', type=int, default=0, help='0 = all seven with D independent')
    parser.add_argument('--seconds', type=float, default=5)
    args = parser.parse_args()
    data = json.loads((ROOT/'data/codex_norm16_attachments_rank.json').read_text())
    forests = json.loads((ROOT/'data/codex_norm16_far_forest.json').read_text())['forests']
    case = data['cases'][args.case]
    attachment = case['orbits'][args.orbit]['representative']
    for forest in forests:
        if (args.forest and forest['id'] != args.forest) or forest['edges_D']:
            continue
        start = time.monotonic()
        model, x = incidence_model(attachment, forest)
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = args.seconds
        status = solver.solve(model)
        result = {'case': args.case, 'orbit': args.orbit, 'forest': forest['id'],
                  'status': solver.status_name(status), 'seconds': time.monotonic()-start,
                  'branches': solver.num_branches}
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            result['attachment'] = attachment
            result['incidence_D_Z'] = [[solver.value(v) for v in row] for row in x]
            target = ROOT/f'data/codex_norm16_incidence_{args.case}_{args.orbit}_{forest["id"]}.json'
            target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({k: v for k, v in result.items()
                          if k not in ('attachment', 'incidence_D_Z')}), flush=True)


if __name__ == '__main__':
    main()
