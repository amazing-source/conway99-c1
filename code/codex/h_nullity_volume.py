"""A joint T/U volume obstruction to extra nullity at a fixed h-mean.

Standalone exact SymPy implementation. All input blocks are in the reduced
supports: the lower blocks and both shorted upper blocks are positive definite
by the producer's hypothesis. No peer seed or existing certificate is audited.
"""
import argparse
import json
from pathlib import Path
import random

import sympy as sp


def rational_inertia(matrix):
    """Exact inertia by rational congruence, including zero diagonal pivots."""
    matrix = sp.Matrix(matrix).applyfunc(sp.Rational)
    if matrix != matrix.T:
        raise ValueError('A symmetric rational matrix is required.')
    positive = negative = zero = 0
    while matrix.rows:
        n = matrix.rows
        i = next((i for i in range(n) if matrix[i, i]), None)
        if i is not None:
            pivot = matrix[i, i]
            positive += int(bool(pivot > 0))
            negative += int(bool(pivot < 0))
            keep = [j for j in range(n) if j != i]
            column = matrix.extract(keep, [i])
            matrix = matrix.extract(keep, keep)-column*column.T/pivot
            continue
        pair = next(((i, j) for i in range(n) for j in range(i+1, n) if matrix[i, j]), None)
        if pair is None:
            zero += n
            break
        i, j = pair
        # The 2x2 block [[0,b],[b,0]] has one positive and one negative root.
        positive += 1
        negative += 1
        keep = [k for k in range(n) if k not in pair]
        ci, cj = matrix.extract(keep, [i]), matrix.extract(keep, [j])
        matrix = matrix.extract(keep, keep)-(ci*cj.T+cj*ci.T)/matrix[i, j]
    return dict(positive=positive, negative=negative, zero=zero)


def certify_ordered_ratio_bounds(lower, upper, thresholds):
    """Certify alpha_i>=threshold_i for the smallest generalized eigenvalues.

    The pencil is lower-alpha*upper. The upper block is assumed positive
    definite, so its inertia counts generalized eigenvalues on each side of
    alpha. Threshold validity uses exact rational arithmetic, not floats.
    """
    lower, upper = sp.Matrix(lower), sp.Matrix(upper)
    if lower.shape != upper.shape or lower.rows != lower.cols:
        raise ValueError('Expected equal square blocks on a common support.')
    bounds = list(map(sp.Rational, thresholds))
    if len(bounds) > lower.rows or any(x <= 0 for x in bounds):
        raise ValueError('Supply at most dimension-many strictly positive bounds.')
    if bounds != sorted(bounds):
        raise ValueError('Bounds must be in increasing order, with repetitions allowed.')
    checks = []
    for i, bound in enumerate(bounds):
        inertia = rational_inertia(lower-bound*upper)
        valid = inertia['negative'] <= i
        checks.append(dict(index=i+1, threshold=str(bound), inertia=inertia, valid=valid))
    return dict(all_certified=all(item['valid'] for item in checks), checks=checks,
                product_lower_bound=str(sp.prod(bounds)))


def certify_nullity_drop(lower_even, lower_odd, upper_even_shorted,
                        upper_odd_shorted, even_bounds, odd_bounds,
                        mean_nullity):
    """Reject >=p extra null directions when the two bottom-p products exceed1.

    The lower blocks A,C are positive on their own supports. The upper blocks
    must first be shorted to those respective supports and be positive definite
    there. A singular shorted upper needs a further common-support reduction;
    this function makes no conclusion for such unreduced input.
    """
    p = len(even_bounds)
    if not p or p != len(odd_bounds):
        raise ValueError('Use the same positive number of ordered bounds on each side.')
    even = certify_ordered_ratio_bounds(lower_even, upper_even_shorted, even_bounds)
    odd = certify_ordered_ratio_bounds(lower_odd, upper_odd_shorted, odd_bounds)
    product_bound = sp.Rational(even['product_lower_bound'])*sp.Rational(odd['product_lower_bound'])
    valid = even['all_certified'] and odd['all_certified']
    excluded = valid and product_bound > 1
    return dict(status='EXTRA_NULLITY_EXCLUDED' if excluded else 'INCONCLUSIVE',
                target_extra_nullity=p, mean_nullity=mean_nullity,
                nullity_at_least_excluded=mean_nullity+p if excluded else None,
                nullity_at_most=mean_nullity+p-1 if excluded else None,
                bottom_product_lower_bound=str(product_bound),
                even_certificate=even, odd_certificate=odd,
                scope='Conditional on the stated positive definite support blocks, correct shorting, range constraints, and simultaneous T/U positivity. No claim about other means.')


def report():
    # An algebraic mean permits one extra null vector but forbids two. This is
    # deliberately not presented as a Conway mean or an actual graph.
    a, c = sp.eye(2), sp.eye(2)
    s, q = sp.diag(2, sp.Rational(1, 4)), sp.eye(2)
    one = certify_nullity_drop(a, c, s, q, [sp.Rational(1, 2)], [1], 12)
    two = certify_nullity_drop(a, c, s, q, [sp.Rational(1, 2), 4], [1, 1], 12)
    assert one['status'] == 'INCONCLUSIVE'
    assert two['status'] == 'EXTRA_NULLITY_EXCLUDED'
    assert two['nullity_at_most'] == 13
    b = sp.diag(1, 0)
    lower = a.row_join(b).col_join(b.T.row_join(c))
    upper = s.row_join(-b).col_join((-b.T).row_join(q))
    lower_inertia, upper_inertia = rational_inertia(lower), rational_inertia(upper)
    assert lower_inertia == dict(positive=3, negative=0, zero=1)
    assert upper_inertia == dict(positive=4, negative=0, zero=0)
    # A proposed threshold larger than the true first ratio is not certified.
    rejected_bound = certify_ordered_ratio_bounds(a, s, [1])
    assert not rejected_bound['all_certified']
    assert rational_inertia(sp.Matrix([[0, 2], [2, 0]])) == dict(positive=1, negative=1, zero=0)
    assert rational_inertia(sp.zeros(3)) == dict(positive=0, negative=0, zero=3)
    # New rational congruences with known inertia, not producer certificates.
    rng = random.Random(801)
    for trial in range(18):
        n = 2+trial % 5
        signature = [rng.choice((-2, 0, 3)) for _ in range(n)]
        change = sp.eye(n)
        for i in range(n):
            for j in range(i):
                change[i, j] = rng.randrange(-2, 3)
        matrix = change*sp.diag(*signature)*change.T
        assert rational_inertia(matrix) == dict(positive=signature.count(3),
                                                negative=signature.count(-2), zero=signature.count(0))
    return dict(status='JOINT_T_U_VOLUME_OBSTRUCTION_TO_EXTRA_NULLITY',
                setup='Let T=[[A,B],[B^T,C]] in h parity and T0=diag(A,C). Let i=nullity(T0). Reduce to the positive supports of A,C and short the U diagonal blocks to those supports, obtaining S,Q. Assume S,Q are positive definite there.',
                kernel_fact='For T PSD, ker(T0)=ker(T) intersection h*ker(T), since 2*T0=T+h*T*h. Put K=A^(-1/2)*B*C^(-1/2). T PSD iff all singular values of K are<=1. Exactly p singular values equal1 iff nullity(T)=i+p.',
                upper_fact='U PSD implies L=S^(-1/2)*B*Q^(-1/2)=P*K*R is a contraction, where P=S^(-1/2)*A^(1/2) and R=C^(1/2)*Q^(-1/2).',
                necessary_volume='If nullity(T)>=i+p, then product_{j=1}^p alpha_j * product_{j=1}^p beta_j <=1, where alpha_j are the p SMALLEST generalized eigenvalues of (A,S) and beta_j those of (C,Q).',
                proof=[
                    'On the positive lower supports, congruence reduces T to [[I,K],[K^T,I]]. Each singular value1 of K supplies exactly one additional null vector; positivity bounds every singular value by1.',
                    'If at least p singular values equal1, the operator norm of the p-th exterior power of K is1. K=P^(-1)*L*R^(-1) and ||exterior^p L||<=1 imply the product of the p smallest singular values of P and of R is<=1.',
                    'Squaring gives the asserted product of generalized eigenvalues: squared singular values of P are those of (A,S), and squared singular values of R are those of (C,Q).',
                    'For rational t, negative inertia of A-t*S counts generalized eigenvalues strictly below t. At most j-1 negative directions certifies alpha_j>=t, including equality and repeated eigenvalues. Rational lower bounds whose combined product exceeds1 certify the obstruction without algebraic root isolation.'
                ],
                fixture=dict(one_direction_test=one, two_direction_test=two,
                             lower_with_one_saturated_direction=lower_inertia,
                             upper_with_same_coupling=upper_inertia,
                             common_zero_modes='The displayed4x4 matrices have no common zero modes; direct sum with12 common zeros realizes the reported13-versus14 illustration algebraically.'),
                own_checks=dict(known_signature_congruences=18, zero_diagonal_pivot='PASS',
                                invalid_threshold_not_certified='PASS'),
                limitations='No peer mean read or excluded. The test targets a mean of nullity12 when seeking nullity14; it says nothing with p=0 about the earlier rank(A)=10, rank(C)=20 means of nullity14. Actual KHOMOG classes may allow the mean kernel to grow; use its actual nullity, not just an included12-dimensional subspace.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = report()
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('status', 'necessary_volume', 'own_checks', 'limitations')}))
