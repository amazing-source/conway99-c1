"""Certified XOR consequences of combinations of quadratic Boolean equations.

The affine code depends on the recorded integer polynomial presentation.
It is a necessary filter, not a replacement for the original equations.
Unlike the V7 extractor, quadratic monomials may cancel between rows.
"""
from itertools import combinations, product
from math import gcd, lcm

import sympy as sp


def residual_polynomials(data, D, mu):
    base, basis = data['base'], data['basis']
    gram = D.T*D
    result = []
    for u, v in data['selected_pairs']:
        dot = lambda X, Y: (X.row(u)*Y[:, v])[0]
        c = gram[u, v]+dot(base, base)+base[u, v]-mu
        linear = [dot(base, T)+dot(T, base)+dot(T, T)+T[u, v] for T in basis]
        pairs = list(combinations(range(len(basis)), 2))
        quadratic = [dot(basis[i], basis[j])+dot(basis[j], basis[i]) for i, j in pairs]
        values = [c]+linear+quadratic
        denominator = lcm(*(int(x.q) for x in values))
        integers = [int(x*denominator) for x in values]
        divisor = gcd(*integers) or 1
        integers = [x//divisor for x in integers]
        result.append(dict(pair=[u, v], constant=integers[0],
            linear=integers[1:1+len(basis)],
            quadratic=[[i, j, a] for (i, j), a in zip(pairs, integers[1+len(basis):]) if a]))
    return result


def parity_code(polynomials, dimension):
    """Basis of every affine consequence in the F2 row span of the inputs.

    Every output carries the XOR of input rows that proves it. Boolean
    squares must already be reduced to x_i before calling this function.
    """
    pairs = list(combinations(range(dimension), 2))
    positions = {pair: i for i, pair in enumerate(pairs)}
    quadratic_pivots, affine_pivots = {}, {}
    contradictory = False
    for row, polynomial in enumerate(polynomials):
        assert len(polynomial['linear']) == dimension
        q = 0
        for i, j, coefficient in polynomial['quadratic']:
            if coefficient % 2:
                q ^= 1 << positions[i, j]
        a = (polynomial['constant'] % 2) << dimension
        for i, coefficient in enumerate(polynomial['linear']):
            if coefficient % 2:
                a ^= 1 << i
        proof = 1 << row
        while q:
            pivot = (q & -q).bit_length()-1
            if pivot not in quadratic_pivots:
                quadratic_pivots[pivot] = (q, a, proof)
                break
            old_q, old_a, old_proof = quadratic_pivots[pivot]
            q, a, proof = q ^ old_q, a ^ old_a, proof ^ old_proof
        if q:
            continue
        while a:
            pivot = (a & -a).bit_length()-1
            if pivot not in affine_pivots:
                affine_pivots[pivot] = (a, proof)
                contradictory |= pivot == dimension
                break
            old_a, old_proof = affine_pivots[pivot]
            a, proof = a ^ old_a, proof ^ old_proof
    checks = [dict(indices=[i for i in range(dimension) if (a >> i) & 1],
                   rhs=(a >> dimension) & 1,
                   source_rows=[i for i in range(len(polynomials)) if (proof >> i) & 1])
              for _, (a, proof) in sorted(affine_pivots.items())]
    return dict(dimension=dimension, input_rows=len(polynomials),
                quadratic_rank=len(quadratic_pivots), affine_rank=len(checks),
                contradictory=contradictory, checks=checks,
                individual_affine_rows=sum(all(a % 2 == 0 for _, _, a in f['quadratic'])
                                           for f in polynomials))


def verify_code(polynomials, code):
    """Replay each proof without using either elimination table."""
    d = code['dimension']
    for check in code['checks']:
        constant, linear, quadratic = 0, [0]*d, {}
        for row in check['source_rows']:
            f = polynomials[row]
            constant ^= f['constant'] % 2
            linear = [a ^ (b % 2) for a, b in zip(linear, f['linear'])]
            for i, j, a in f['quadratic']:
                quadratic[i, j] = quadratic.get((i, j), 0) ^ (a % 2)
        assert not any(quadratic.values())
        assert [i for i, a in enumerate(linear) if a] == check['indices']
        assert constant == check['rhs']
    return True


def evaluate(polynomial, bits):
    return (polynomial['constant']+sum(a*x for a, x in zip(polynomial['linear'], bits))
            + sum(a*bits[i]*bits[j] for i, j, a in polynomial['quadratic']))


def petersen_mixed_control():
    # These are (f1+f2)/2, (f1+f3)/2, (f2+f3)/2 for V7's three
    # Petersen residuals. Their transformation is invertible over Q.
    polynomials = [dict(constant=0, linear=[0, 0, -1], quadratic=[[0, 2, 1], [1, 2, 1]]),
                   dict(constant=0, linear=[0, -1, 0], quadratic=[[0, 1, 1], [1, 2, 1]]),
                   dict(constant=0, linear=[-1, 0, 0], quadratic=[[0, 1, 1], [0, 2, 1]])]
    code = parity_code(polynomials, 3)
    verify_code(polynomials, code)
    assert code['individual_affine_rows'] == 0 and code['affine_rank'] == 1
    assert code['checks'][0]['indices'] == [0, 1, 2] and code['checks'][0]['rhs'] == 0
    table = []
    for bits in product((0, 1), repeat=3):
        exact = all(evaluate(f, bits) == 0 for f in polynomials)
        accepted = all(sum(bits[i] for i in c['indices']) % 2 == c['rhs'] for c in code['checks'])
        assert exact == accepted  # Sufficiency is specific to this control.
        table.append(dict(bits=bits, exact=exact, code_accepts=accepted))
    return dict(polynomials=polynomials, code=code, table=table,
                scope='Equivalent Petersen equations, not a new C1 exclusion')
