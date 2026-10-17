"""New moment constraints: positive example and degree-preserving negative trade."""
from itertools import combinations, permutations
from pathlib import Path
import json
import sys
import numpy as np
from ortools.sat.python import cp_model
from coclique_residual_moments import add_moments


def residual(D, E, mu):
    R = D.T@D
    return R.sum(axis=1)-R.diagonal()+E@E.sum(axis=1)-mu*(len(E)-1)


def solve_fixed(D, E, mu):
    m = len(E)
    model = cp_model.CpModel()
    R = D.T@D
    edges = {}
    for u, v in combinations(range(m), 2):
        x = model.new_bool_var(f'e{u}_{v}')
        model.add(x == int(E[u, v]))
        edges[u, v] = x
        y = model.new_int_var(0, D.shape[0], f'overlap{u}_{v}')
        model.add(y == int(R[u, v]))
    edge = lambda u, v: 0 if u == v else edges[tuple(sorted((u, v)))]
    add_moments(model, list(range(m)), edge, mu=mu)
    assert not model.validate()
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.max_time_in_seconds = 5
    return solver.status_name(solver.solve(model))


def check(folder):
    old = json.loads((folder.parent/'spectral_completion_v8'/'paley25.json').read_text())
    B, D, E = [np.array(x, dtype=np.int64) for x in (old['B'], old['D'], old['completions'][0])]
    A = np.block([[B, D], [D.T, E]])
    # Move two residual vertices into the border so residual degrees vary.
    b = len(B)+2
    D, E = A[:b, b:], A[b:, b:]
    mu, k = old['mu'], old['k']
    assert np.array_equal(A@A+A, (k-mu)*np.eye(len(A), dtype=np.int64)+mu)
    assert not np.any(residual(D, E, mu))
    assert solve_fixed(D, E, mu) == 'OPTIMAL'
    found = None
    for a, b, c, d in permutations(range(len(E)), 4):
        if E[a,b] and E[c,d] and not E[a,c] and not E[b,d]:
            F = E.copy()
            for u,v,value in [(a,b,0),(c,d,0),(a,c,1),(b,d,1)]:
                F[u,v] = F[v,u] = value
            if np.any(residual(D, F, mu)):
                found = (a,b,c,d,F)
                break
    assert found is not None
    a,b,c,d,F = found
    assert np.array_equal(F.sum(axis=1), E.sum(axis=1))
    assert solve_fixed(D, F, mu) == 'INFEASIBLE'
    # The new obstruction occurs with unchanged B, D and all residual degrees.
    # It is a control example, NOT an exclusion in the C1 family.
    report = dict(check='PASS', source='saved Paley25 control, repartitioned',
                  mu=mu, k=k, D=D.tolist(), E=E.tolist(), traded_E=F.tolist(),
                  removed=[[a,b],[c,d]], added=[[a,c],[b,d]],
                  degrees=E.sum(axis=1).tolist(),
                  moment_residual=residual(D,F,mu).tolist(),
                  positive_status='OPTIMAL', negative_status='INFEASIBLE',
                  scope='Moment encoder control only; no C1 exclusion')
    (folder/'moment_control.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ['check','removed','added','degrees','moment_residual']}))


if __name__ == '__main__':
    check(Path(sys.argv[1]))
