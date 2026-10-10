"""Bounded integer version of the B/D plus Z/D moment relaxation.

No adjacency on Z or B is constructed. UNKNOWN is not an exclusion.
"""
import json
from ortools.sat.python import cp_model
from norm16_even_margins_probe import instance
from norm16_schur_data import ROOT


def solve(ci, oi, fid, seconds=3):
    matrix, rhs, labels, equations = instance(ci, oi, fid)
    model = cp_model.CpModel()
    columns = matrix.tocsc()
    xs = []
    for i, label in enumerate(labels):
        eqs = columns.indices[columns.indptr[i]:columns.indptr[i+1]]
        xs.append(model.new_int_var(0, min(int(rhs[r]) for r in eqs), f'x{i}'))
    for i, target in enumerate(rhs):
        js = matrix.indices[matrix.indptr[i]:matrix.indptr[i+1]]
        model.add(sum(xs[j] for j in js) == int(target))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    status = solver.solve(model)
    result = {'case': ci, 'orbit': oi, 'forest': fid, 'status': solver.status_name(status),
              'seconds': solver.wall_time, 'branches': solver.num_branches}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        values = [int(solver.value(x)) for x in xs]
        assert list(matrix @ values) == list(rhs)
        result['positive_multiplicities'] = [{'type': label, 'multiplicity': value} for label, value in zip(labels, values) if value]
    return result


if __name__ == '__main__':
    results = []
    for ci, oi in [(0, 226), (0, 241), (0, 242), (4, 1), (4, 2)]:
        for fid in (3, 6, 7):
            item = solve(ci, oi, fid)
            results.append(item)
            print(json.dumps({k: v for k, v in item.items() if k != 'positive_multiplicities'}), flush=True)
    (ROOT/'data/codex_norm16_even_margins_integer.json').write_text(json.dumps({'scope': __doc__, 'results': results}, indent=2)+'\n')
