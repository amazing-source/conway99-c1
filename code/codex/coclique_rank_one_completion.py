"""Exact, solver-free completion when one residual eigenspace has rank <=1.

For Conway parameters the search has at most 8192 sign assignments, for
any boundary satisfying V13, and at most two completed labelled graphs.
In particular every boundary with augmented nullity <=3 is covered.
The criterion is conditional on an actual common binary factor B,D.
"""
from itertools import combinations, product
from math import isqrt

import sympy as sp
from sympy.matrices.exceptions import NonInvertibleMatrixError

from coclique_global_completion import encode, integral_completion
from coclique_regular_completion import eliminate_regular


def _positive_boundary_minor(B, D, k, mu, gap):
    """Use one small boundary inverse; return None for a singular minor."""
    n, m = D.shape
    v = n+m
    r = sp.Rational(gap-1, 2)
    total_negative = (k+r*(v-1))/gap
    if n not in (total_negative-1, total_negative):
        return None
    assert n > 0 and m > 0 and k >= mu > 0 and k*k == mu*(v-1)
    assert B.shape == (n,n) and B == B.T
    assert all(x in (0,1) for x in B) and all(B[i,i] == 0 for i in range(n))
    assert all(x in (0,1) for x in D)
    assert D*sp.ones(m,1) == k*sp.ones(n,1)-B*sp.ones(n,1)
    assert D*D.T == (k-mu)*sp.eye(n)+mu*sp.ones(n)-B-B*B
    alpha = sp.Rational(k-r,v)
    H = r*sp.eye(n)-B+alpha*sp.ones(n)
    try:
        inverse = H.inv()
    except NonInvertibleMatrixError:
        return None
    # Under the validated V13 hypotheses H is a principal block of the
    # negative-eigenvalue projector of A0, hence PSD. Invertible means PD.
    X = alpha*sp.ones(n,m)-D
    M = r*sp.eye(m)+alpha*sp.ones(m)-X.T*inverse*X
    C = D.col_join(sp.ones(1,m))
    rank = C.rank(); q = int(total_negative-n)
    assert M == M.T and sp.trace(M) == gap*q
    assert D*M == mu*sp.ones(n,m)-(B+sp.eye(n))*D
    assert M*sp.ones(m,1) == k*sp.ones(m,1)-D.T*sp.ones(n,1)
    report = dict(nullity=m-rank, boundary_rank=D.rank(), augmented_rank=rank,
                  gap=gap, negative_multiplicity=str(q), search_bound=2**(2*gap-1),
                  direct_boundary_inverse=True, completions=[])
    if q == 0:
        if not all(x.is_Integer for x in M):
            return dict(report,status='NO_SRG_COMPLETION',reason='The unique real completion is nonintegral')
        integral_completion(B,D,M,k,mu)
        return dict(report,status='COMPLETE',sign_assignments=1,completions=[encode(M)])
    return _complete_signs(B,D,M,C,gap,-1,report,k,mu)


def complete_rank_one(B, D, k=14, mu=2):
    B, D = sp.Matrix(B), sp.Matrix(D)
    discriminant = 1+4*(k-mu)
    gap = isqrt(discriminant)
    if gap*gap == discriminant:
        direct = _positive_boundary_minor(B,D,k,mu,gap)
        if direct is not None:
            return direct
    data = eliminate_regular(B, D, k, mu)
    E0, P, C = data['E0'], data['P'], data['constraint_matrix']
    h, m = data['nullity'], D.cols
    report = dict(nullity=h, boundary_rank=data['boundary_rank'],
                  augmented_rank=data['rank'], completions=[])
    if gap*gap != discriminant:
        return dict(report, status='NOT_APPLICABLE', reason='Irrational restricted eigenvalues')
    r, s = sp.Rational(gap-1, 2), sp.Rational(-gap-1, 2)
    q = (sp.trace(E0)+r*h)/gap
    report.update(gap=gap, negative_multiplicity=str(q), search_bound=2**(2*gap-1))
    reject = lambda reason, **extra: dict(report, status='NO_SRG_COMPLETION', reason=reason, **extra)
    if not q.is_Integer or q < 0 or q > h:
        return reject('Zero diagonal requires an unavailable projector rank')
    q = int(q)
    if q in (0, h):
        E = E0+(r if q == 0 else s)*P
        if not all(x.is_Integer for x in E):
            return reject('The unique real completion is nonintegral')
        integral_completion(B, D, E, k, mu)
        return dict(report, status='COMPLETE', sign_assignments=1, completions=[encode(E)])
    if q == 1:
        M, sign = E0+r*P, -1
    elif h-q == 1:
        M, sign = E0+s*P, 1
    else:
        return dict(report, status='NOT_APPLICABLE', reason='Both residual eigenspaces have rank >=2')
    return _complete_signs(B,D,M,C,gap,sign,report,k,mu)


def _complete_signs(B,D,M,C,gap,sign,report,k,mu):
    m = D.cols
    reject = lambda reason, **extra: dict(report,status='NO_SRG_COMPLETION',reason=reason,**extra)
    a = [-sign*M[i, i] for i in range(m)]
    if any(x < 0 for x in a):
        return reject('The rank-one projector would have a negative diagonal')
    assert sum(a) == gap
    active = [i for i in range(m) if a[i]]
    forced = {i: [] for i in active}
    for i, j in combinations(range(m), 2):
        if not a[i] or not a[j]:
            if M[i, j] not in (0, 1):
                return reject('A zero projector coordinate forces a nonbinary entry', pair=[i,j])
            continue
        amplitude = sp.sqrt(a[i]*a[j])
        if not amplitude.is_Rational:
            return reject('A required off-diagonal square root is irrational', pair=[i,j])
        allowed = [t for t in (-1, 1) if M[i,j]+sign*t*amplitude in (0,1)]
        if not allowed:
            return reject('Neither sign gives a binary off-diagonal entry', pair=[i,j])
        if len(allowed) == 1:
            forced[i].append((j, allowed[0]))
            forced[j].append((i, allowed[0]))
        else:
            assert M[i,j] == sp.Rational(1,2) and amplitude == sp.Rational(1,2)
    relative = {}; components = []
    for start in active:
        if start in relative:
            continue
        relative[start] = 1
        component = []; todo = [start]
        while todo:
            i = todo.pop(); component.append(i)
            for j, parity in forced[i]:
                required = relative[i]*parity
                if j in relative:
                    if relative[j] != required:
                        return reject('Inconsistent forced sign cycle')
                else:
                    relative[j] = required; todo.append(j)
        components.append(component)
    count = len(components)
    assert count >= 1
    if count >= 3:
        # Every pair across distinct components has both signs allowed.
        # Three components force a_i=1/2 on every active coordinate.
        assert all(a[i] == sp.Rational(1,2) for i in active)
        assert len(active) == 2*gap
    assignments = 2**(count-1)
    assert assignments <= report['search_bound']
    report.update(forced_components=count, active_coordinates=len(active),
                  sign_assignments=assignments, sign=sign,
                  projector_diagonal_numerators=list(map(str,a)))
    anchor = a[active[0]]
    vectors = []
    for component in components:
        v = sp.zeros(m, 1)
        for i in component:
            v[i] = relative[i]*sp.sqrt(anchor*a[i])
            assert v[i].is_Rational
        vectors.append(v)
    images = [C*v for v in vectors]
    answers = []
    for tail in product((-1,1), repeat=count-1):
        orientations = (1,)+tail
        if any(sum(t*g[i] for t,g in zip(orientations, images)) for i in range(C.rows)):
            continue
        v = sum((t*z for t,z in zip(orientations, vectors)), sp.zeros(m,1))
        assert (v.T*v)[0] == gap*anchor
        E = M+sign*(v*v.T)/anchor
        # This full exact verification is only reached for actual completions.
        integral_completion(B, D, E, k, mu)
        answers.append(encode(E))
    if k == 14 and mu == 2:
        assert len(answers) <= 2, 'Conway rank-two rigidity and small-support automorphisms'
    return dict(report, status='COMPLETE' if answers else 'NO_SRG_COMPLETION',
                completions=answers, kernel_rejections=assignments-len(answers))
