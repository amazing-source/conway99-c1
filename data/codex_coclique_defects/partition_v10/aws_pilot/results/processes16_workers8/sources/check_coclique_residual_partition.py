"""New V10 controls: conservation, encoder, and complete branch bookkeeping."""
from itertools import combinations, product
from pathlib import Path
import json
import sys

import numpy as np
from ortools.sat.python import cp_model
from coclique_residual_partition import branches, add_residual_block


def fixed_status(D, E, mu, caps_only):
    model = cp_model.CpModel()
    R = D.T@D
    edges = {}
    for u, v in combinations(range(len(E)), 2):
        edges[u, v] = model.new_bool_var(f'e{u}_{v}')
        model.add(edges[u, v] == int(E[u, v]))
        x = model.new_int_var(0, D.shape[0], f'overlap{u}_{v}')
        model.add(x == int(R[u, v]))
    edge = lambda u, v: 0 if u == v else edges[tuple(sorted((u, v)))]
    add_residual_block(model, list(range(len(E))), edge, mu, caps_only)
    assert not model.validate(), model.validate()
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.max_time_in_seconds = 5
    return solver.status_name(solver.solve(model))


def check(folder):
    folder.mkdir(parents=True, exist_ok=True)
    control = json.loads((folder.parent/'calibration_v9/moment_control.json').read_text())
    D, E, F = [np.array(control[k], dtype=np.int64) for k in ('D', 'E', 'traded_E')]
    mu, k = control['mu'], control['k']
    valid, invalid = [], []
    for caps in (False, True):
        valid.append(fixed_status(D, E, mu, caps))
        invalid.append(fixed_status(D, F, mu, caps))
    assert valid == ['OPTIMAL']*2 and invalid == ['INFEASIBLE']*2
    L = D.T@D+F@F+F-(k-mu)*np.eye(len(F), dtype=np.int64)-mu
    assert not np.any(L.diagonal()) and L.sum() == 0
    assert L.min() < 0 < L.max()
    # Enumerate the aggregate set-intersection conditions independently of
    # the branch generator. This checks BOTH e/f orientations and the cover,
    # not the existence of graphs in any of the 61 necessary cases.
    expected = set()
    for a, b, location in product(range(1, 7), range(1, 7), ('C8', 'C13', 'ZH', 'Z0')):
        c8e, c8f = a-1, b-1
        c13e, c13f = 6-a, 6-b
        shared8, shared13 = int(location == 'C8'), int(location == 'C13')
        if not (0 <= shared8 <= min(c8e, c8f) and c8e+c8f-shared8 <= 8):
            continue
        if not (0 <= shared13 <= min(c13e, c13f) and c13e+c13f-shared13 <= 13):
            continue
        if location == 'Z0' and min(a, b) == 1:
            continue
        expected.add((min(a,b), max(a,b), location))
    actual = {(x['degrees'][0], x['degrees'][1], x['common_neighbour_class']) for x in branches()}
    assert actual == expected and len(actual) == 61
    report = dict(check='PASS', positive_status=valid, negative_status=invalid,
                  residual_sum=int(L.sum()), negative_residual=int(L.min()),
                  positive_residual=int(L.max()), branches=branches(),
                  scope='New encoder and partition checks; no C1 existence or nonexistence claim')
    (folder/'mathematical_checks.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k != 'branches'}))


if __name__ == '__main__':
    check(Path(sys.argv[1]))
