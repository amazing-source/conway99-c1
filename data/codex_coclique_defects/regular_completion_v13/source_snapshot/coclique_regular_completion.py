"""Exact SRG completion for an arbitrary binary boundary, including regularity.

For A^2+A=(k-mu)I+mu J, assume DD.T=(k-mu)I+mu J-B-B^2 and
D*1=k*1-B*1. No vertex needs to have its complete neighbourhood in B.
Append 1.T to D to obtain C, and append (k*1-D.T*1).T to the mixed
right-hand side to obtain R. Then E0=C^+R is symmetric and P projects
onto ker(C). All real symmetric regular polynomial completions are
E=E0+r*P+(s-r)*Q, where Q is an orthogonal projector contained in P
and r,s are the roots of x^2+x-(k-mu). Integrality alone forces E to
be an adjacency matrix. See the coexistence note, sections 66-69.

This generalizes the closed-neighbourhood version without changing it.
It supplies no binary factor D and is not a Conway exclusion.
"""
import sympy as sp


def eliminate_regular(B, D, k=14, mu=2):
    B, D = sp.Matrix(B), sp.Matrix(D)
    n, m = D.shape
    assert n > 0 and m > 0 and k >= mu > 0
    assert int(k) == k and int(mu) == mu
    assert k*k == mu*(n+m-1)
    one_n, one_m = sp.ones(n, 1), sp.ones(m, 1)
    assert B.shape == (n, n) and B == B.T
    assert all(x in (0, 1) for x in B) and all(B[i, i] == 0 for i in range(n))
    assert all(x in (0, 1) for x in D)
    assert D*one_m == k*one_n-B*one_n
    K = (k-mu)*sp.eye(n)+mu*sp.ones(n)-B-B*B
    assert D*D.T == K
    F = mu*sp.ones(n, m)-(B+sp.eye(n))*D
    residual_degrees = k*one_m-D.T*one_n
    C = D.col_join(one_m.T)
    R = F.col_join(residual_degrees.T)
    assert C*R.T == R*C.T
    pivot_rows = C.T.rref()[1]
    rank = len(pivot_rows)
    if rank == m:
        E0 = C[list(pivot_rows), :].inv()*R[list(pivot_rows), :]
        P = sp.zeros(m)
    else:
        inverse = C.pinv()
        E0 = inverse*R
        P = sp.eye(m)-inverse*C
    assert C*E0 == R
    assert E0 == E0.T and P == P.T and P*P == P
    assert C*P == sp.zeros(n+1, m) and E0*P == sp.zeros(m)
    assert E0*one_m == residual_degrees
    assert E0*E0+E0+D.T*D == (k-mu)*(sp.eye(m)-P)+mu*sp.ones(m)
    boundary_rank = D.rank()
    return dict(E0=E0, P=P, rank=rank, nullity=m-rank, F=F,
                constraint_matrix=C, constraint_rhs=R,
                boundary_rank=boundary_rank,
                regularity_rank_gain=rank-boundary_rank,
                closed=[i for i in range(n) if sum(B.row(i)) == k])
