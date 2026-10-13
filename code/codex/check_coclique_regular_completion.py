"""Small exact controls of the new completion theorem without a closed star.

Checks the failure addressed by the theorem, reconstructs known missing
blocks, and exhausts 8/128 affine assignments on two new open boundaries.
No catalogue, large graph audit, or Conway solver campaign is performed.
"""
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import platform
import time
import sympy as sp
from coclique_global_completion import eliminate, encode, integral_completion
from coclique_regular_completion import eliminate_regular
from coclique_affine_completion import frame, binary_completions, polynomial_defect


def control(name, A, border, k, mu, affine=False, closed=False):
    outside = [i for i in range(A.rows) if i not in border]
    B, D, actual = A[border, border], A[border, outside], A[outside, outside]
    data = eliminate_regular(B, D, k, mu)
    E0, P = data['E0'], data['P']
    assert bool(data['closed']) == closed
    root = sp.sqrt(1+4*(k-mu))
    r, s = (-1+root)/2, (-1-root)/2
    Q = (E0+r*P-actual)/(r-s)
    assert Q == Q.T and Q*Q == Q and P*Q == Q
    assert E0+r*P+(s-r)*Q == actual
    integral_completion(B, D, actual, k, mu)
    legacy = D.pinv()*data['F']
    report = dict(name=name, k=k, mu=mu, border=border, outside=outside,
                  B=encode(B), D=encode(D), E=encode(actual),
                  E0=encode(E0), P=encode(P), Q=encode(Q),
                  rank=data['rank'], boundary_rank=data['boundary_rank'],
                  nullity=data['nullity'], regularity_rank_gain=data['regularity_rank_gain'],
                  closed=data['closed'], old_formula_symmetric=legacy == legacy.T)
    if len(border) == 1:
        assert legacy != legacy.T, 'This control must exhibit the old obstruction'
        # Independent closed formula for a regular boundary (here d=0).
        n, m = D.shape
        b = D.T*sp.ones(n, 1)
        degree = sum(B.row(0))
        t = k-degree
        kap = k-mu+mu*n-degree-degree*degree
        w = sp.ones(m, 1)-sp.Rational(t, kap)*b
        zeta = (w.T*w)[0]
        assert D*w == sp.zeros(n, 1) and zeta == sum(w)
        c = sp.Rational(mu, kap)
        a = (k-c*n*t)/zeta
        assert E0 == legacy+c*w*b.T+a*w*w.T
        old_P = sp.eye(m)-D.pinv()*D
        assert P == old_P-w*w.T/zeta
        report.update(regular_formula_checked=True, w=encode(w), w_norm_squared=str(zeta))
    if closed:
        old = eliminate(B, D, k, mu)
        assert old['E0'] == E0 and old['P'] == P
        assert data['regularity_rank_gain'] == 0
        report['legacy_agreement'] = True
    if affine:
        f = frame(B, D, k, mu, regularity=True)
        assert f['status'] == 'AFFINE_FRAME'
        m, delta = D.cols, f['dimension']
        assert delta <= 10
        binary_count, answers, first_rejected = 0, [], None
        C = data['constraint_matrix']
        for bits in product((0, 1), repeat=delta):
            E = f['base']+sum((x*T for x, T in zip(bits, f['basis'])), sp.zeros(m))
            assert E*sp.ones(m, 1) == k*sp.ones(m, 1)-D.T*sp.ones(D.rows, 1)
            if not all(x in (0, 1) for x in E):
                continue
            binary_count += 1
            defect = polynomial_defect(B, D, E, k, mu)
            assert C*defect == sp.zeros(C.rows, m)
            assert all(defect[i, i] == 0 for i in range(m))
            selected_zero = all(defect[u, v] == 0 for u, v in f['selected_pairs'])
            assert selected_zero == (defect == sp.zeros(m))
            if selected_zero:
                integral_completion(B, D, E, k, mu)
                answers.append(encode(E))
            elif first_rejected is None:
                first_rejected = dict(bits=bits, E=encode(E), defect=encode(defect))
        assert encode(actual) in answers
        solved = binary_completions(B, D, k, mu, seconds=10, enumerate_all=True, regularity=True)
        assert solved['complete']
        canonical = lambda matrices: sorted(json.dumps(E) for E in matrices)
        assert canonical(solved['completions']) == canonical(answers)
        report.update(affine_dimension=delta, affine_assignments=2**delta,
                      binary_linear_candidates=binary_count, completions=len(answers),
                      selected_pairs=f['selected_pairs'], all_completions=answers,
                      rejected_candidate=first_rejected, solver_verdict=solved['verdict'])
    return report


def norm18_moments():
    """Symbolic consequences of the two moments, not a constructed C1 factor."""
    n, m, k, mu, d = 18, 81, 14, 2, 4
    t, kap = k-d, k-mu+mu*n-d-d*d
    sum_b, norm_b = n*t, n*kap
    zeta = m-sp.Rational(n*t*t, kap)
    assert (sum_b, norm_b, zeta) == (180, 504, sp.Rational(117, 7))
    c = sp.Rational(mu, kap)
    a = (k-c*n*t)/zeta
    assert c == sp.Rational(1, 14) and a == sp.Rational(8, 117)
    # Moment scalar products on span{b,w}, where w=1-(5/14)b.
    metric = sp.diag(norm_b, zeta)
    forced = sp.Matrix([[sp.Rational(55, 7), sp.Rational(117, 98)],
                        [36, sp.Rational(8, 7)]])
    one = sp.Matrix([sp.Rational(5, 14), 1])
    b = sp.Matrix([1, 0])
    assert metric*forced == forced.T*metric
    assert forced*one == k*one-b
    assert forced*b == 36*one-5*b
    assert forced*forced+forced+28*sp.diag(1, 0) == 12*sp.eye(2)+2*one*one.T*metric
    return dict(status='PASS', scope='Conditional exact identities, no binary D constructed',
                sum_b=sum_b, norm_b_squared=norm_b, w_norm_squared=str(zeta),
                correction_c=str(c), correction_a=str(a), integral_w_norm_squared=819,
                forced_matrix_in_b_w_basis=encode(forced))


def main(folder):
    start = time.monotonic()
    folder.mkdir(parents=True, exist_ok=True)
    rook = sp.Matrix(9, 9, lambda i, j: int(i != j and (i//3 == j//3 or i%3 == j%3)))
    vertices = list(combinations(range(5), 2))
    petersen = sp.Matrix(10, 10, lambda i, j: int(set(vertices[i]).isdisjoint(vertices[j])))
    reports = [
        control('rook_one_vertex', rook, [0], 4, 2),
        control('rook_open_edge', rook, [0, 1], 4, 2, affine=True),
        control('rook_irregular_border', rook, [0, 1, 3], 4, 2, affine=True),
        control('rook_open_injective', rook, [0, 1, 2, 3, 4], 4, 2, affine=True),
        control('petersen_one_vertex', petersen, [0], 3, 1),
        control('petersen_open_pair', petersen, [0, 1], 3, 1, affine=True),
        control('rook_closed_compatibility', rook, [0, 1, 2, 3, 6], 4, 2, closed=True),
    ]
    for report in reports:
        (folder/(report['name']+'.json')).write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    moments = norm18_moments()
    (folder/'norm18_moments.json').write_text(json.dumps(moments, indent=2)+'\n', encoding='utf-8')
    keys = ('name', 'boundary_rank', 'rank', 'nullity', 'regularity_rank_gain',
            'old_formula_symmetric', 'affine_dimension', 'affine_assignments',
            'binary_linear_candidates', 'completions', 'solver_verdict', 'legacy_agreement')
    sources = ('coclique_global_completion.py', 'coclique_regular_completion.py',
               'coclique_affine_completion.py', 'check_coclique_regular_completion.py')
    summary = dict(status='PASS', controls=[{key: report[key] for key in keys if key in report}
                                           for report in reports],
                   norm18_symbolic_status=moments['status'],
                   python=platform.python_version(), sympy=sp.__version__,
                   sources={name: hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                            for name in sources}, seconds=time.monotonic()-start,
                   scope='Generalized completion theorem on new small boundaries; no Conway factor or exclusion')
    (folder/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    main(parser.parse_args().folder)
