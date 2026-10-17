"""Exact propagation of mixed-defect kernels, with an integrality rule.

Assume binary regular A=[[B,D],[D.T,E]], integer mu=lambda+1, correct parameter
count, and both diagonal blocks of its SRG defect zero. For a defect
column g=G[:,u], ||g||^2 = D[:,u].T (2B+I) g. Consequently a column
lying in the B-eigenspace 0 or -1 must vanish (integer, zero sum).

The propagation routine uses only the matrices and supplied kernel seeds;
it does not inspect the actual defect to invent new seeds. This is a
completion criterion, not a nonexistence result for a parameter family.
"""
import sympy as sp


def span(*matrices):
    joined = sp.Matrix.hstack(*matrices)
    columns = joined.columnspace()
    return sp.Matrix.hstack(*columns) if columns else sp.zeros(joined.rows, 0)


def annihilator(basis):
    columns = basis.T.nullspace()
    return sp.Matrix.hstack(*columns).T if columns else sp.zeros(0, basis.rows)


def propagate(B, D, E, known_rows=(), known_columns=(),
              row_relations=(), column_relations=(), integral=True):
    """Return certified subspaces U<=ker G.T, V<=ker G.

    Callers must justify the hypotheses above and every supplied seed.
    certify() checks them on a concrete candidate. No floating arithmetic.
    """
    B, D, E = map(sp.Matrix, (B, D, E))
    b, m = B.rows, E.rows
    Ib, Im = sp.eye(b), sp.eye(m)
    U = span(sp.ones(b, 1), Ib.extract(range(b), list(known_rows)),
             *[sp.Matrix(x) for x in row_relations])
    V = span(sp.ones(m, 1), Im.extract(range(m), list(known_columns)),
             *[sp.Matrix(x) for x in column_relations])
    events = []
    dimensions = [[U.cols, V.cols]]
    while True:
        # These transports follow from BG=GE, DG.T=GD.T, D.TG=G.TD.
        while True:
            next_U = span(U, B*U, D*V)
            next_V = span(V, E*V, D.T*U)
            if (next_U.cols, next_V.cols) == (U.cols, V.cols):
                break
            U, V = next_U, next_V
            dimensions.append([U.cols, V.cols])
        if not integral:
            break
        additions = [[], []]
        for side, block, basis in ((0, B, U), (1, E, V)):
            null = annihilator(basis)
            identity = sp.eye(block.rows)
            for u in range(block.rows):
                unit = identity[:, u]
                if (null*unit).is_zero_matrix:
                    continue
                for eigenvalue in (0, -1):
                    witness = block[:, u]-eigenvalue*unit
                    if (null*witness).is_zero_matrix:
                        coefficients = basis.gauss_jordan_solve(witness)[0]
                        assert basis*coefficients == witness
                        additions[side].append(unit)
                        events.append(dict(side='border' if side == 0 else 'residual',
                                           vertex=u, eigenvalue=eigenvalue,
                                           basis_dimension=basis.cols,
                                           witness=[str(x) for x in witness],
                                           coefficients=[str(x) for x in coefficients]))
                        break
        if not any(additions):
            break
        U = span(U, *additions[0])
        V = span(V, *additions[1])
        dimensions.append([U.cols, V.cols])
    row_null, col_null = annihilator(U), annihilator(V)
    rows = [u for u in range(b) if (row_null*Ib[:,u]).is_zero_matrix]
    cols = [u for u in range(m) if (col_null*Im[:,u]).is_zero_matrix]
    return U, V, dict(dimensions=dimensions, integral_events=events,
                      exact_rows=rows, exact_columns=cols,
                      full_closure=U.cols == b or V.cols == m)


def certify(B, D, E, k, mu, **seeds):
    """Check the theorem's assumptions and each conclusion exactly."""
    assert sp.sympify(k).is_Integer and sp.sympify(mu).is_Integer
    B, D, E = map(sp.Matrix, (B, D, E))
    b, m = B.rows, E.rows
    A = B.row_join(D).col_join(D.T.row_join(E))
    assert A == A.T and all(A[i,i] == 0 for i in range(b+m))
    assert all(x in (0,1) for x in A)
    assert A*sp.ones(b+m, 1) == k*sp.ones(b+m, 1)
    assert k*k == mu*(b+m-1)
    T = A*A+A-(k-mu)*sp.eye(b+m)-mu*sp.ones(b+m)
    assert T[:b,:b].is_zero_matrix and T[b:,b:].is_zero_matrix
    G = T[:b,b:]
    assert B*G == G*E and D.T*G == G.T*D and D*G.T == G*D.T
    assert (G*sp.ones(m,1)).is_zero_matrix
    assert (G.T*sp.ones(b,1)).is_zero_matrix
    for u in range(m):
        g = G[:,u]
        assert (g.T*g)[0] == (D[:,u].T*(2*B+sp.eye(b))*g)[0]
    for u in seeds.get('known_rows', ()):
        assert G[u,:].is_zero_matrix
    for u in seeds.get('known_columns', ()):
        assert G[:,u].is_zero_matrix
    for vector in seeds.get('row_relations', ()):
        assert (G.T*sp.Matrix(vector)).is_zero_matrix
    for vector in seeds.get('column_relations', ()):
        assert (G*sp.Matrix(vector)).is_zero_matrix
    U, V, report = propagate(B, D, E, **seeds)
    assert (G.T*U).is_zero_matrix and (G*V).is_zero_matrix
    if report['full_closure']:
        assert G.is_zero_matrix
    report.update(full_mixed_verified=bool(G.is_zero_matrix),
                  mixed_defect_squared_norm=int(sum(x*x for x in G)))
    return report
