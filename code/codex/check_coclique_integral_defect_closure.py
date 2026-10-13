"""Controls separating linear transport, integral closure, and open defects."""
from pathlib import Path
import argparse
import itertools
import json
import sympy as sp
from coclique_integral_defect_closure import certify


def check(folder):
    folder.mkdir(parents=True, exist_ok=True)
    cycle = sp.Matrix(5,5,lambda i,j:int((i-j)%5 in (1,4)))
    prism = certify(cycle, sp.eye(5), cycle, k=3, mu=1)
    assert not prism['full_closure'] and not prism['full_mixed_verified']
    assert prism['dimensions'] == [[1,1]] and not prism['integral_events']

    # Paley25, two adjacent residual vertices. Linear transport of ones
    # cannot distinguish them; the new -1 rule closes both columns.
    old = json.loads((folder.parent/'spectral_completion_v8/paley25.json').read_text())
    B, D, E = map(sp.Matrix, (old['B'],old['D'],old['completions'][0]))
    A = B.row_join(D).col_join(D.T.row_join(E))
    pair = next((i,j) for i in range(25) for j in range(i+1,25) if A[i,j])
    border = [i for i in range(25) if i not in pair]
    blocks = (A.extract(border,border), A.extract(border,pair), A.extract(pair,pair))
    linear = certify(*blocks, k=old['k'], mu=old['mu'], integral=False)
    integral = certify(*blocks, k=old['k'], mu=old['mu'])
    assert not linear['full_closure'] and linear['dimensions'][-1][1] == 1
    assert integral['full_closure'] and integral['integral_events']
    assert any(x['side'] == 'residual' and x['eigenvalue'] == -1
               for x in integral['integral_events'])

    # Rook9, two nonadjacent vertices: eigenvalue 0 closes an empty block.
    rook = sp.Matrix(9,9,lambda i,j:int(i!=j and (i//3==j//3 or i%3==j%3)))
    missing = [0,4]
    border = [i for i in range(9) if i not in missing]
    rook_report = certify(rook.extract(border,border),rook.extract(border,missing),
                          rook.extract(missing,missing),k=4,mu=2)
    assert rook_report['full_closure']
    assert any(x['side']=='residual' and x['eigenvalue']==0
               for x in rook_report['integral_events'])

    # Exhaustive small arithmetic check, distinct from graph propagation.
    vectors = 0
    for g in itertools.product(range(-2,3), repeat=4):
        if sum(g):
            continue
        norm = sum(x*x for x in g)
        for d in itertools.product((0,1), repeat=4):
            dot = sum(x*y for x,y in zip(g,d))
            assert 2*abs(dot) <= sum(abs(x) for x in g) <= norm
            assert not norm or dot not in (norm,-norm)
        vectors += 1
    # Without integrality the argument is false: g=(1/2,-1/2), d=(1,0).
    fractional = sp.Matrix([sp.Rational(1,2),-sp.Rational(1,2)])
    assert (fractional.T*fractional)[0] == fractional[0] != 0

    report = dict(status='PASS', prism_counterexample=prism,
                  paley25_adjacent_pair=list(pair), paley25_linear=linear,
                  paley25_integral=integral, rook9_independent_pair=rook_report,
                  integer_zero_sum_vectors_checked=vectors,
                  integrality_is_essential=True,
                  scope='New closure theorem controls, no C1 graph or branch exclusion')
    (folder/'integral_closure_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], prism_open=True,
                         paley_linear_dimensions=linear['dimensions'],
                         paley_integral_dimensions=integral['dimensions'],
                         paley_integral_events=len(integral['integral_events']),
                         rook_integral_events=len(rook_report['integral_events']),
                         integer_vectors=vectors)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    check(parser.parse_args().folder)
