"""Exact controls of the NEW closure criterion, including a counterexample."""
from pathlib import Path
import json
import sys
import sympy as sp
from coclique_mixed_closure import certify, add_leaf_columns
from ortools.sat.python import cp_model


def check(folder):
    # Pentagonal prism: cubic, both 5x5 blocks satisfy the Petersen equation,
    # but mixed equations fail. Thus closing the two blocks alone is NOT enough.
    cycle = sp.Matrix(5,5,lambda i,j:int((i-j)%5 in (1,4)))
    prism = certify(cycle, sp.eye(5), cycle, k=3, mu=1)
    assert not prism['full_mixed_verified'] and prism['residual_walk_dimension'] == 1
    # Same interface, complementary pentagon: Petersen, now exact.
    petersen = certify(cycle, sp.eye(5), sp.ones(5)-sp.eye(5)-cycle,
                      k=3, mu=1, known_rows=[0,1])
    assert petersen['full_mixed_verified'] and petersen['completion_forced_by_border_control']
    # Saved Paley25, with a nonsymmetric induced block chosen deterministically.
    old = json.loads((folder.parent/'spectral_completion_v8/paley25.json').read_text())
    B,D,E = map(sp.Matrix, (old['B'],old['D'],old['completions'][0]))
    A = B.row_join(D).col_join(D.T.row_join(E))
    M = [1,2,5,7,10,11,15,16,20,22]
    border = [i for i in range(25) if i not in M]
    paley = certify(A.extract(border,border), A.extract(border,M), A.extract(M,M),
                    k=old['k'],mu=old['mu'])
    assert paley['residual_walk_determinant'] == '18761760'
    # Check the new conditional leaf encoder on the 3x3 rook graph (mu=2),
    # then exchange two boundary incidences, preserving every vertex degree.
    rook = sp.Matrix(9,9,lambda i,j:int(i!=j and (i//3==j//3 or i%3==j%3)))
    labels = list(range(25,31))+[37,38,63]
    order = [2,3,4,6,7,8,0,1,5]
    positive = rook.extract(order,order)
    negative = positive.copy()
    for u,v,value in ((1,6,0),(2,7,0),(1,7,1),(2,6,1)):
        negative[u,v] = negative[v,u] = value
    assert positive*sp.ones(9,1) == negative*sp.ones(9,1)
    statuses = []
    for adjacency in (positive,negative):
        model = cp_model.CpModel()
        edges = {}
        for i,u in enumerate(labels):
            for j in range(i+1,len(labels)):
                v = labels[j]
                x = model.new_bool_var(f'a{u}_{v}')
                model.add(x == int(adjacency[i,j]))
                edges[u,v] = x
        edge = lambda u,v: 0 if u==v else edges[tuple(sorted((u,v)))]
        for u in (37,38):
            degree = model.new_int_var(1,1,f'v10_degree{u}')
            model.add(degree == sum(edge(u,v) for v in (37,38,63) if u!=v))
        add_leaf_columns(model,labels[:6],labels[6:],edge)
        assert not model.validate(),model.validate()
        solver = cp_model.CpSolver()
        solver.parameters.num_workers = 1
        solver.parameters.max_time_in_seconds = 5
        statuses.append(solver.status_name(solver.solve(model)))
    assert statuses == ['OPTIMAL','INFEASIBLE']
    report = dict(check='PASS', prism_counterexample=prism, petersen=petersen,
                  paley25=dict(**paley, missing=M),
                  leaf_encoder=dict(positive_status=statuses[0], traded_status=statuses[1],
                                    all_degrees_preserved=True),
                  scope='Conditional completion theorem controls, no new C1 exclusion')
    (folder/'mixed_closure_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k != 'prism_counterexample'}))


if __name__ == '__main__':
    check(Path(sys.argv[1]))
