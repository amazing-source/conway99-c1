"""Exact new-method checks and independently replayable rational witnesses."""
from itertools import combinations, product
from pathlib import Path
import argparse
import json

import sympy as sp

from coclique_spectral_completion import negative_witness, global_separate
from coclique_modular_coexistence import (petersen_mixed_control, parity_code, verify_code,
                                         residual_polynomials, evaluate)


def replay_global_cut(A, k, mu, cut):
    """Verify a global certificate directly from the two spectral bounds."""
    n = A.rows
    r = (sp.sqrt(1+4*(k-mu))-1)/2
    s = -1-r
    z = sp.Matrix(cut['vector'])
    norm, total = (z.T*z)[0], sum(z)
    if cut['side'] == 'upper':
        constant = r*norm+(k-r)*total**2/n
        weights = [-2*z[u]*z[v] for u, v in cut['pairs']]
        M = r*sp.eye(n)-A+(k-r)*sp.ones(n)/n
    else:
        constant = -s*norm-(k-s)*total**2/n
        weights = [2*z[u]*z[v] for u, v in cut['pairs']]
        M = A-s*sp.eye(n)-(k-s)*sp.ones(n)/n
    assert (z.T*M*z)[0] == sp.Rational(cut['witness_value']) < 0
    assert constant*cut['scale'] == cut['raw_constant']
    assert [w*cut['scale'] for w in weights] == cut['raw_weights']
    assert cut['weights'] == [w//cut['gcd'] for w in cut['raw_weights']]
    assert cut['rhs'] == -(cut['raw_constant']//cut['gcd'])
    assert sum(w*A[u, v] for w, (u, v) in zip(cut['weights'], cut['pairs'])) < cut['rhs']


def check(folder, source):
    checked = []
    # Zero pivots, negative Schur complements and singular PSD matrices.
    for raw, expected_psd in [([[0, 1], [1, 0]], False), ([[1, 2], [2, 1]], False),
                              ([[1, 1], [1, 1]], True), ([[0, 0], [0, 3]], True),
                              ([[2, 1, 0], [1, 2, 1], [0, 1, 2]], True)]:
        M = sp.Matrix(raw)
        w = negative_witness(M, short=False)
        assert (w is None) == expected_psd
        if w is not None:
            assert (w.T*M*w)[0] < 0
    for name in ('rook', 'petersen', 'paley25', 'paley49'):
        report = json.loads((folder/(name+'.json')).read_text(encoding='utf-8'))
        B, D = sp.Matrix(report['B']), sp.Matrix(report['D'])
        k, mu = report['k'], report['mu']
        n, m = D.shape
        assert D*D.T == (k-mu)*sp.eye(n)+mu*sp.ones(n)-B-B*B
        if name in ('rook', 'petersen'):
            affine = json.loads((source/(name+'.json')).read_text(encoding='utf-8'))
            base, basis = sp.Matrix(affine['base']), [sp.Matrix(T) for T in affine['basis']]
            E0 = D.pinv()*(mu*sp.ones(n, m)-(B+sp.eye(n))*D)
            P = sp.eye(m)-D.pinv()*D
            for cut in report['cuts']:
                z = sp.Matrix(cut['vector'])
                assert D*z == sp.zeros(n, 1)
                E = base+sum((x*T for x, T in zip(cut['rejected_free'], basis)), sp.zeros(m))
                M = E0+sp.Rational(report['r'])*P-E if cut['side']=='upper' else E-E0-sp.Rational(report['s'])*P
                assert (z.T*M*z)[0] == sp.Rational(cut['witness_value']) < 0
                c = (sp.Rational(report['r'])*(z.T*z)[0]-(z.T*base*z)[0] if cut['side']=='upper'
                     else (z.T*base*z)[0]-sp.Rational(report['s'])*(z.T*z)[0])
                weights = [(-1 if cut['side']=='upper' else 1)*(z.T*T*z)[0] for T in basis]
                assert [int(w*cut['scale']) for w in weights] == cut['raw_weights']
                assert c*cut['scale'] == cut['raw_constant']
                assert cut['rhs'] == -(cut['raw_constant']//cut['gcd'])
                assert cut['weights'] == [w//cut['gcd'] for w in cut['raw_weights']]
        for raw in report['completions']:
            E = sp.Matrix(raw)
            A = B.row_join(D).col_join(D.T.row_join(E))
            assert A == A.T and all(x in (0, 1) for x in A)
            assert all(A[i, i] == 0 for i in range(A.rows))
            assert A*sp.ones(A.rows, 1) == k*sp.ones(A.rows, 1)
            assert A*A+A == (k-mu)*sp.eye(A.rows)+mu*sp.ones(A.rows)
        checked.append(dict(name=name, cuts=len(report['cuts']), completions=len(report['completions'])))

    # Exhaustive new geometric comparison on the already saved Petersen frame.
    old = json.loads((source/'petersen.json').read_text(encoding='utf-8'))
    B, D, N = sp.Matrix(old['B']), sp.Matrix(old['D']), sp.Matrix(old['kernel'])
    base, basis = sp.Matrix(old['base']), [sp.Matrix(T) for T in old['basis']]
    E0 = D.pinv()*(sp.ones(4, 6)-(B+sp.eye(4))*D)
    P = sp.eye(6)-D.pinv()*D
    polynomials = residual_polynomials(dict(base=base, basis=basis,
                                          selected_pairs=old['selected_pairs']), D, 1)
    original_code = parity_code(polynomials, 3)
    verify_code(polynomials, original_code)
    table = []
    for bits in product((0, 1), repeat=3):
        E = base+sum((b*T for b, T in zip(bits, basis)), sp.zeros(6))
        Q = (E0+P-E)/3
        compressed = N.T*Q*N
        assert all(compressed[list(indices), list(indices)].det() >= 0
                   for size in (1, 2) for indices in combinations(range(3), size))
        valid = sum(bits) % 2 == 0
        assert all(evaluate(f, bits) == 0 for f in polynomials) == valid
        assert all(sum(bits[i] for i in c['indices']) % 2 == c['rhs']
                   for c in original_code['checks']) == valid
        assert (compressed.det() >= 0) == valid
        A = B.row_join(D).col_join(D.T.row_join(E))
        global_cut = global_separate(A, 3, 1)
        assert (global_cut is None) == valid
        if global_cut is not None:
            replay_global_cut(A, 3, 1, global_cut)
        table.append(dict(bits=bits, two_coordinate_psd_checks=True,
                          determinant=str(compressed.det()), complete=valid,
                          global_cut=global_cut))
    fractional = base+sum(basis, sp.zeros(6))/2
    Q = (E0+P-fractional)/3
    assert Q == P/3 and Q*Q != Q and any(x not in (0, 1) for x in fractional)
    geometry = dict(table=table, fractional=dict(free=['1/2']*3, Q='P/3',
        satisfies_convex_bounds=True, is_graph=False),
        scope='Petersen illustration of global coexistence; not C1 nonexistence')
    (folder/'petersen_geometry.json').write_text(json.dumps(geometry, indent=2)+'\n', encoding='utf-8')
    (folder/'petersen_original_parity.json').write_text(json.dumps(dict(
        polynomials=polynomials, code=original_code), indent=2)+'\n', encoding='utf-8')

    mixed = petersen_mixed_control()
    (folder/'petersen_mixed_parity.json').write_text(json.dumps(mixed, indent=2)+'\n', encoding='utf-8')
    # The code is generally only necessary: x*y=0 has no nonzero affine
    # row-span consequence, yet rejects 11. Also check a derived 1=0.
    weak = [dict(constant=0, linear=[0, 0], quadratic=[[0, 1, 1]])]
    assert parity_code(weak, 2)['affine_rank'] == 0
    contradictory = weak+[dict(constant=1, linear=[0, 0], quadratic=[[0, 1, 1]])]
    code = parity_code(contradictory, 2)
    assert code['contradictory']
    verify_code(contradictory, code)
    # Exercise the actual C1 coefficients on an intentionally invalid regular
    # graph. This is a unit control, not an exclusion of a research family.
    A = sp.Matrix(99, 99, lambda u, v: int(bool(0 < min((u-v) % 99, (v-u) % 99) <= 7)))
    cut = global_separate(A)
    assert cut is not None
    replay_global_cut(A, 14, 2, cut)
    (folder/'invalid_regular99_cut.json').write_text(json.dumps(dict(
        construction='Circulant on Z/99 with differences +/-1,...,+/-7',
        expected='14-regular but not SRG; negative control only', certificate=cut), indent=2)+'\n', encoding='utf-8')
    summary = dict(status='PASS', new_method_controls=checked,
                   zero_pivot_and_schur_checks=5, petersen_global_checks=8,
                   fractional_counterexample=True, combined_parity_proof=True,
                   actual_C1_spectral_coefficients_negative_control=True,
                   no_claim_of_C1_exclusion=True)
    (folder/'independent_check.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    parser.add_argument('--source', type=Path, default=Path('data/codex_coclique_defects/affine_completion_v7'))
    args = parser.parse_args()
    check(args.folder, args.source)
