"""Short exact controls of V15; no Conway catalogue or solver run."""
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import time

import sympy as sp

from coclique_affine_completion import frame, polynomial_defect, binary_completions
from coclique_global_completion import encode
from coclique_regular_completion import eliminate_regular
from coclique_rank_one_completion import complete_rank_one


def controls(folder):
    folder.mkdir(parents=True, exist_ok=True)
    vertices = list(combinations(range(5), 2))
    petersen = sp.Matrix(10, 10, lambda i,j: int(set(vertices[i]).isdisjoint(vertices[j])))
    rook = sp.Matrix(9, 9, lambda i,j: int(i != j and (i//3 == j//3 or i%3 == j%3)))
    cases = [('petersen_three_border',petersen,[0,1,2],3,1),
             ('petersen_path_border',petersen,[0,7,1],3,1),
             ('rook_three_border',rook,[0,1,4],4,2),
             ('rook_triangle_border',rook,[0,1,2],4,2),
             ('rook_four_border',rook,[0,1,3,4],4,2),
             ('petersen_out_of_scope',petersen,[0],3,1)]
    reports = []
    for name,A,border,k,mu in cases:
        outside = [i for i in range(A.rows) if i not in border]
        B,D = A[border,border], A[border,outside]
        start = time.monotonic()
        result = complete_rank_one(B,D,k,mu)
        report = dict(name=name, B=encode(B),D=encode(D),k=k,mu=mu,
                      elapsed=time.monotonic()-start, **result)
        if result['status'] == 'NOT_APPLICABLE':
            assert name == 'petersen_out_of_scope'
        else:
            assert encode(A[outside,outside]) in result['completions']
            f = frame(B,D,k,mu,regularity=True)
            assert f['dimension'] <= 10
            expected = []
            for bits in product((0,1), repeat=f['dimension']):
                E = f['base']+sum((b*T for b,T in zip(bits,f['basis'])), sp.zeros(len(outside)))
                if all(v in (0,1) for v in E) and polynomial_defect(B,D,E,k,mu) == sp.zeros(len(outside)):
                    expected.append(encode(E))
            assert sorted(map(str,expected)) == sorted(map(str,result['completions']))
            report['affine_assignments'] = 2**f['dimension']
            report['exact_agreement'] = True
            # The residual multiplicity can also be read solely from the
            # boundary spectral Gram matrix, without constructing E.
            v = A.rows; gap = int(result['gap']); r = sp.Rational(gap-1,2)
            g = (k+r*(v-1))/gap
            spectral = r*sp.eye(len(border))-B+sp.Rational(k-r,v)*sp.ones(len(border))
            assert g-spectral.rank() == sp.Rational(result['negative_multiplicity'])
            report['spectral_rank_identity'] = True
            if result.get('direct_boundary_inverse'):
                data = eliminate_regular(B,D,k,mu)
                alpha = sp.Rational(k-r,v)
                X = alpha*sp.ones(B.rows,D.cols)-D
                direct_M = r*sp.eye(D.cols)+alpha*sp.ones(D.cols)-X.T*spectral.inv()*X
                assert direct_M == data['E0']+r*data['P']
                report['direct_formula_agreement'] = True
            if name == 'rook_triangle_border':
                assert result['forced_components'] == 3
                assert result['sign_assignments'] == 4 and len(result['completions']) == 4
                # Four completions here do not contradict the Conway-only
                # bound of two: this graph has different parameters.
                integrated = binary_completions(B,D,k,mu,regularity=True,rank_one_first=True)
                assert integrated['completion_method'] == 'rank_one_signs'
                assert integrated['completions'] == result['completions']
        reports.append(report)
    # A Gram-valid binary factor with no SRG completion from V14. This
    # checks rejection by the new sign method, not a rerun of that method.
    fixture = json.loads((folder.parent/'rank_two_rigidity_v14'/'gram_valid_rejected_factor.json').read_text())
    report = dict(name='gram_valid_negative', **complete_rank_one(fixture['B'],fixture['D'],4,2))
    assert report['status'] == 'NO_SRG_COMPLETION'
    reports.append(report)
    for report in reports:
        (folder/(report['name']+'.json')).write_text(json.dumps(report,indent=2)+'\n')
    summary = dict(result='PASS', cases=[{k:r[k] for k in ('name','status','nullity','negative_multiplicity')}
                                      | dict(completions=len(r['completions']),
                                             sign_assignments=r.get('sign_assignments'),
                                             affine_assignments=r.get('affine_assignments')) for r in reports],
                   sources={p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest()
                            for p in ('coclique_rank_one_completion.py','check_coclique_rank_one_completion.py',
                                      'coclique_affine_completion.py','coclique_regular_completion.py',
                                      'coclique_global_completion.py')},
                   scope='New exact reconstruction route; no Conway graph or family excluded')
    (folder/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary['cases']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('folder',type=Path)
    controls(parser.parse_args().folder)
