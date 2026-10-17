"""Exact elimination of the unbuilt graph from a binary boundary factor.

For A^2+A=(k-mu)I+mu J, B is an induced border, D its binary
incidence with the m missing vertices, and K=(k-mu)I+mu J-B-B^2.
If DD^t=K, D1=k1-B1 and B contains one complete neighbourhood,
the unbuilt block is E=E0+rP+(s-r)Q. Here E0=D^+F,
F=mu J-(B+I)D, P projects onto ker D, and Q is an orthogonal
projector contained in P. For C1, r=3,s=-4. INTEGRALITY of E
alone forces zero diagonal and binary off-diagonal entries.

This is an exact completion criterion, not a C1 exclusion. In
particular, the required single binary Gram factor D is not provided
by independently feasible degree factors or a PSD test of K.
"""
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json
import time
import sympy as sp


def encode(matrix):
    return [[str(x) for x in row] for row in matrix.tolist()]


def eliminate(B, D, k=14, mu=2):
    B, D = sp.Matrix(B), sp.Matrix(D)
    n, m = D.shape
    assert mu > 0 and m > 0
    one_n, one_m = sp.ones(n, 1), sp.ones(m, 1)
    assert B.shape == (n, n) and B == B.T
    assert all(x in (0, 1) for x in B) and all(B[i, i] == 0 for i in range(n))
    assert all(x in (0, 1) for x in D)
    assert k * (k + 1) == k - mu + mu * (n + m)
    assert D * one_m == k * one_n - B * one_n
    K = (k - mu) * sp.eye(n) + mu * sp.ones(n) - B - B * B
    assert D * D.T == K
    closed = [i for i in range(n) if sum(B.row(i)) == k]
    assert closed, 'One complete neighbourhood is a hypothesis of this version'
    for s in closed:
        assert D.T * B[:, s] == mu * one_m
    F = mu * sp.ones(n, m) - (B + sp.eye(n)) * D
    pivot_rows = D.T.rref()[1]
    rank = len(pivot_rows)
    if rank == m:
        # A square row subsystem avoids a larger normal-equations inverse.
        square = D[list(pivot_rows), :]
        E0 = square.inv() * F[list(pivot_rows), :]
        P = sp.zeros(m)
    else:
        inverse = D.pinv()
        E0 = inverse * F
        P = sp.eye(m) - inverse * D
    assert D * E0 == F
    assert E0 == E0.T and P == P.T and P * P == P
    assert D * P == sp.zeros(n, m) and E0 * P == sp.zeros(m)
    assert P * one_m == sp.zeros(m, 1)
    assert E0 * one_m == k * one_m - D.T * one_n
    assert E0 * E0 + E0 + D.T * D == (k - mu) * (sp.eye(m) - P) + mu * sp.ones(m)
    return dict(E0=E0, P=P, rank=rank, nullity=m-rank, closed=closed, F=F)


def integral_completion(B, D, E, k=14, mu=2):
    """Independent row sum and polynomial hypotheses imply adjacency."""
    B, D, E = sp.Matrix(B), sp.Matrix(D), sp.Matrix(E)
    A = B.row_join(D).col_join(D.T.row_join(E))
    assert A == A.T
    assert all(x.is_Integer for x in E)
    assert A * sp.ones(A.rows, 1) == k * sp.ones(A.rows, 1)
    assert A * A + A == (k-mu) * sp.eye(A.rows) + mu * sp.ones(A.rows)
    for i in range(A.rows):
        # Sum of nonnegative INTEGERS, not a floating point tolerance.
        terms = [A[i, i]**2] + [A[i, j]*(A[i, j]-1) for j in range(A.rows) if j != i]
        assert all(x >= 0 for x in terms) and sum(terms) == 0
    assert all(A[i, i] == 0 for i in range(A.rows))
    assert all(x in (0, 1) for x in A)
    return A


def control_case(A, border, k, name, source=None):
    outside = sorted(set(range(A.rows))-set(border))
    B, D, actual = A[border, border], A[border, outside], A[outside, outside]
    start = time.monotonic()
    result = eliminate(B, D, k=k)
    E0, P = result['E0'], result['P']
    root = sp.sqrt(4*k-7)
    r, s = (-1+root)/2, (-1-root)/2
    Q = (E0+r*P-actual)/(r-s)
    assert Q == Q.T and Q*Q == Q and P*Q == Q
    rebuilt = E0+r*P+(s-r)*Q
    assert rebuilt == actual
    integral_completion(B, D, rebuilt, k=k)
    report = dict(name=name, k=k, mu=2, border=border, outside=outside,
                  B=encode(B), D=encode(D), E0=encode(E0), P=encode(P), Q=encode(Q),
                  E=encode(actual), r=str(r), s=str(s), rank=result['rank'],
                  nullity=result['nullity'], closed=result['closed'],
                  seconds=time.monotonic()-start, checked='Exact rational arithmetic')
    if source:
        report['source']=str(source)
        report['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    if result['nullity']==1:
        other=E0+r*P
        report['other_projector_zero_integral']=all(x.is_Integer for x in other)
        report['other_projector_zero_matrix']=encode(other)
    return report


def controls(folder, bvls):
    folder.mkdir(parents=True, exist_ok=True)
    rook=sp.Matrix(9,9,lambda i,j:int(i!=j and (i//3==j//3 or i%3==j%3)))
    # These exercise both a uniquely forced block and a genuine hidden mode.
    reports=[control_case(rook,[0,1,2,3,6],4,'rook_singular'),
             control_case(rook,[0,1,2,3,4,6],4,'rook_injective')]
    A=sp.zeros(243)
    for line in bvls.read_text().splitlines():
        parts=line.split()
        if len(parts)!=2 or not all(x.isdigit() for x in parts):continue
        u,v=map(int,parts)
        if u==243 and v==2673:continue
        A[u,v]=A[v,u]=1
    assert sum(A[:,0])==22
    # Apply the NEW elimination theorem to one existing known graph;
    # this is not a repetition of the prior four-graph research audit.
    outside=[u for u in range(1,243) if not A[0,u]][:39]
    border=sorted(set(range(243))-set(outside))
    reports.append(control_case(A,border,22,'bvls_missing39',bvls))
    for report in reports:
        (folder/(report['name']+'.json')).write_text(json.dumps(report,indent=2)+'\n')
    summary=[{k:r[k] for k in ('name','rank','nullity','seconds','checked')} for r in reports]
    (folder/'summary.json').write_text(json.dumps(dict(status='PASS',controls=summary,
        scope='New completion criterion checked on known graphs, not a C1 existence or nonexistence certificate'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',controls=summary)),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('folder',type=Path)
    parser.add_argument('--bvls',type=Path,default=Path('data/srg243/bvls243.edges'))
    args=parser.parse_args();controls(args.folder,args.bvls)
