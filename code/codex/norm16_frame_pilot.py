"""Construct a norm16 core+Z+one-complete-neighbourhood frame.

Local necessary constraints on core+D+Z+the eight simple neighbours of p0.
CP-SAT feasibility is not existence of an SRG; no completeness claim for the
single frame. All labelling data are taken from the existing core catalogue.
"""
import argparse
import json
from itertools import combinations
import time

from ortools.sat.python import cp_model
from norm16_far_incidence import ROOT, incidence_model
from norm16_attachments_rank import rank


def frame_model(b, attachment, forest):
    model, dz = incidence_model(attachment, forest)
    labels = [{'kind': 'P', 'index': i} for i in range(8)]
    labels += [{'kind': 'Q', 'index': i} for i in range(8)]
    labels += [{'kind': 'D', 'index': i, 'P': row[:2], 'Q': row[2:]}
               for i, row in enumerate(attachment)]
    labels += [{'kind': 'Z', 'index': i} for i in range(11)]
    all_simple = [(p, q, j) for p in range(8) for q in range(8)
                  for j in range(2-b[p][q]-sum(p in d[:2] and q in d[2:]
                                              for d in attachment))]
    simple = [cell for cell in all_simple if cell[0] == 0]
    assert len(simple) == 8
    labels += [{'kind': 'B', 'cell': list(cell[:2]), 'copy': cell[2]}
               for cell in simple]
    n = len(labels)
    assert n == 43
    a = [[0]*n for _ in range(n)]

    def edge(i, j, value):
        a[i][j] = a[j][i] = value

    for p in range(8):
        for q in range(8):
            edge(p, 8+q, b[p][q])
    for d, row in enumerate(attachment):
        for v in row[:2]+[8+q for q in row[2:]]:
            edge(v, 16+d, 1)
        for z in range(11):
            edge(16+d, 24+z, dz[d][z])
    for z, w in combinations(range(11), 2):
        edge(24+z, 24+w, forest['adjacency_Z'][z][w])
    for i, (p, q, _) in enumerate(simple, 35):
        edge(p, i, 1)
        edge(8+q, i, 1)
        for j in range(16, i):
            edge(j, i, model.new_bool_var(f'a{j}_{i}'))
    products = {}

    def both(u, v):
        if isinstance(u, int):
            return v if u else 0
        if isinstance(v, int):
            return u if v else 0
        if u.index == v.index:
            return u
        key = tuple(sorted((u.index, v.index)))
        if key not in products:
            w = model.new_bool_var(f'm{key[0]}_{key[1]}')
            model.add(w <= u)
            model.add(w <= v)
            model.add(w >= u+v-1)
            products[key] = w
        return products[key]

    for i, j in combinations(range(n), 2):
        common = sum(both(a[i][k], a[j][k]) for k in range(n))
        if i == 0:
            model.add(common == 2-a[i][j])
        else:
            model.add(common <= 2-a[i][j])
    for i in range(n):
        model.add(sum(a[i]) <= 14)
    for v in range(35, 43):
        model.add(sum(a[v][z] for z in range(24, 35))
                  == 1+sum(a[v][d] for d in range(16, 24)))
    return model, a, labels, all_simple


def check_local(a, labels):
    n = len(a)
    assert all(a[i][i] == 0 for i in range(n))
    assert all(a[i][j] == a[j][i] in (0, 1) for i in range(n) for j in range(n))
    assert all(sum(row) <= 14 for row in a)
    assert sum(a[0]) == 14
    for i, j in combinations(range(n), 2):
        common = sum(a[i][k]*a[j][k] for k in range(n))
        assert common <= 2-a[i][j]
        if i == 0:
            assert common == 2-a[i][j]
    for i in range(16, 24):
        assert sum(a[i][24:35]) == 4
    for i in range(24, 35):
        assert sum(a[i][16:24]) == 2+sum(a[i][24:35])
    for i in range(35, 43):
        assert sum(a[i][24:35]) == 1+sum(a[i][16:24])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int, default=0)
    parser.add_argument('--orbit', type=int, default=0)
    parser.add_argument('--forest', type=int, default=2)
    parser.add_argument('--seconds', type=float, default=20)
    args = parser.parse_args()
    cases = json.loads((ROOT/'data/codex_norm16_attachments_rank.json').read_text())['cases']
    core_cases = json.loads((ROOT/'data/codex_norm16_cores.json').read_text())['cases']
    core_cases = [c for c in core_cases if c['representatives']]
    forests = json.loads((ROOT/'data/codex_norm16_far_forest.json').read_text())['forests']
    attachment = cases[args.case]['orbits'][args.orbit]['representative']
    forest = next(f for f in forests if f['id'] == args.forest)
    if forest['edges_D']:
        raise ValueError('This first pilot only constructs D-independent frames.')
    b = core_cases[args.case]['representatives'][0]
    start = time.monotonic()
    model, a, labels, all_simple = frame_model(b, attachment, forest)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = args.seconds
    status = solver.solve(model)
    result = {'scope': __doc__, 'case': args.case, 'orbit': args.orbit,
              'forest': args.forest, 'status': solver.status_name(status),
              'seconds': time.monotonic()-start, 'branches': solver.num_branches}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        a = [[v if isinstance(v, int) else solver.value(v) for v in row] for row in a]
        check_local(a, labels)
        keep = list(range(16))+list(range(24, 35))+[i for i in range(16, 24) if a[0][i]]+list(range(35, 43))
        assert len(keep) == 37
        frame = [[a[i][j] for j in keep] for i in keep]
        seidel = [[0 if i == j else 1-2*frame[i][j] for j in range(37)] for i in range(37)]
        result.update({'labels': [labels[i] for i in keep], 'adjacency': frame,
                       'seidel_rank_mod7': rank(seidel), 'support43_labels': labels,
                       'support43_adjacency': a, 'attachment_D': attachment,
                       'all_simple_labels': [list(cell) for cell in all_simple],
                       'frame_indices_in_support43': keep})
        target = ROOT/f'data/codex_norm16_frame_{args.case}_{args.orbit}_{args.forest}.json'
        target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        result['file'] = str(target)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('adjacency', 'labels', 'support43_labels',
                                   'support43_adjacency', 'attachment_D',
                                   'all_simple_labels', 'frame_indices_in_support43')}, indent=2))


if __name__ == '__main__':
    main()
