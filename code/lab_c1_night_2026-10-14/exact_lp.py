"""Exact rational linear programming (dense tableau simplex, Bland's rule, Fractions). Small problems only.

feasible(E, e, G, g): is there a with E a = e and G a >= g ?  -> (True, a) or (False, None)
optimum(c, E, e, G, g, sense): max (sense=+1) or min (sense=-1) of c.a on that set -> value or None if infeasible,
                               "unbounded" if unbounded.
All entries are Fractions or ints. The equalities are eliminated exactly first (a = a0 + K t).
"""
from fractions import Fraction


def rref_solve(E, e, n):
    """Return (a0, K) with {a : E a = e} = {a0 + K t}; None if inconsistent."""
    M = [[Fraction(x) for x in row] + [Fraction(v)] for row, v in zip(E, e)]
    piv = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c)
        r += 1
    for i in range(r, len(M)):
        if M[i][n] != 0:
            return None
    free = [c for c in range(n) if c not in piv]
    a0 = [Fraction(0)] * n
    for i, c in enumerate(piv):
        a0[c] = M[i][n]
    K = []
    for f in free:
        v = [Fraction(0)] * n
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -M[i][f]
        K.append(v)
    return a0, K


def _simplex(T, basis, cost_row_index, ncols):
    """Minimise the objective stored in row cost_row_index (reduced costs, last entry = -value) with Bland's rule.
    T: list of rows (constraints first, objective rows after); each row has ncols + 1 entries (rhs last)."""
    m = cost_row_index
    while True:
        obj = T[m]
        enter = next((j for j in range(ncols) if obj[j] < 0), None)
        if enter is None:
            return "optimal"
        best = None
        for i in range(m):
            a = T[i][enter]
            if a > 0:
                ratio = T[i][-1] / a
                if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        if best is None:
            return "unbounded"
        i = best[1]
        pv = T[i][enter]
        T[i] = [x / pv for x in T[i]]
        for k in range(len(T)):
            if k != i and T[k][enter] != 0:
                f = T[k][enter]
                T[k] = [x - f * y for x, y in zip(T[k], T[i])]
        basis[i] = enter


def _setup(H, r):
    """Rows H t >= r with t free: variables u (d), v (d), s (m), w (artificials). Returns tableau pieces."""
    m, d = len(H), len(H[0]) if H else 0
    rows = []
    basis = []
    art = []
    ncols_base = 2 * d + m
    for i in range(m):
        row = [Fraction(x) for x in H[i]] + [-Fraction(x) for x in H[i]] + [Fraction(0)] * m
        row[2 * d + i] = Fraction(-1)
        rhs = Fraction(r[i])
        if rhs <= 0:
            row = [-x for x in row]
            rhs = -rhs
            rows.append(row + [rhs])
            basis.append(2 * d + i)
        else:
            rows.append(row + [rhs])
            art.append(i)
            basis.append(None)
    na = len(art)
    ncols = ncols_base + na
    for i in range(m):
        rows[i] = rows[i][:-1] + [Fraction(0)] * na + [rows[i][-1]]
    for k, i in enumerate(art):
        rows[i][ncols_base + k] = Fraction(1)
        basis[i] = ncols_base + k
    return rows, basis, ncols, ncols_base, d


def _phase1(H, r):
    rows, basis, ncols, ncols_base, d = _setup(H, r)
    # phase-1 objective: minimise sum of artificials; reduced costs = -(sum of artificial rows) on non-art columns
    obj = [Fraction(0)] * (ncols + 1)
    for i, b in enumerate(basis):
        if b >= ncols_base:
            obj = [o - x for o, x in zip(obj, rows[i])]
    for j in range(ncols_base, ncols):
        obj[j] = Fraction(0)
    T = rows + [obj]
    _simplex(T, basis, len(rows), ncols)
    if T[-1][-1] != 0:
        return None
    return T[:-1], basis, ncols, ncols_base, d


def feasible(E, e, G, g, n):
    sol = rref_solve(E, e, n)
    if sol is None:
        return False, None
    a0, K = sol
    if not K:
        ok = all(sum(Fraction(x) * y for x, y in zip(row, a0)) >= v for row, v in zip(G, g))
        return ok, (a0 if ok else None)
    H = [[sum(Fraction(x) * kv[j] for j, x in enumerate(row)) for kv in K] for row in G]
    r = [Fraction(v) - sum(Fraction(x) * y for x, y in zip(row, a0)) for row, v in zip(G, g)]
    p1 = _phase1(H, r)
    if p1 is None:
        return False, None
    T, basis, ncols, ncols_base, d = p1
    val = [Fraction(0)] * ncols
    for i, b in enumerate(basis):
        val[b] = T[i][-1]
    t = [val[j] - val[d + j] for j in range(d)]
    a = [a0[k] + sum(t[j] * K[j][k] for j in range(d)) for k in range(n)]
    assert all(sum(Fraction(x) * y for x, y in zip(row, a)) >= v for row, v in zip(G, g))
    assert all(sum(Fraction(x) * y for x, y in zip(row, a)) == v for row, v in zip(E, e))
    return True, a


def optimum(c, E, e, G, g, n, sense=1):
    sol = rref_solve(E, e, n)
    if sol is None:
        return None
    a0, K = sol
    H = [[sum(Fraction(x) * kv[j] for j, x in enumerate(row)) for kv in K] for row in G]
    r = [Fraction(v) - sum(Fraction(x) * y for x, y in zip(row, a0)) for row, v in zip(G, g)]
    p1 = _phase1(H, r)
    if p1 is None:
        return None
    T, basis, ncols, ncols_base, d = p1
    # Drive every artificial variable that is still basic (necessarily at value 0) out of the basis: pivot on any
    # non-artificial column with a nonzero entry in its row; if there is none the row is redundant and is removed.
    # Then delete the artificial columns, so that phase 2 can never make an artificial positive.
    i = 0
    while i < len(T):
        if basis[i] >= ncols_base:
            piv = next((j for j in range(ncols_base) if T[i][j] != 0), None)
            if piv is None:
                del T[i]
                del basis[i]
                continue
            pv = T[i][piv]
            T[i] = [x / pv for x in T[i]]
            for k in range(len(T)):
                if k != i and T[k][piv] != 0:
                    f = T[k][piv]
                    T[k] = [x - f * y for x, y in zip(T[k], T[i])]
            basis[i] = piv
        i += 1
    T = [row[:ncols_base] + [row[-1]] for row in T]
    ncols = ncols_base
    cK = [sum(Fraction(ci) * kv[k] for k, ci in enumerate(c)) for kv in K]
    c0 = sum(Fraction(ci) * a for ci, a in zip(c, a0))
    full = [-sense * x for x in cK] + [sense * x for x in cK] + [Fraction(0)] * (ncols - 2 * d)
    obj = full + [Fraction(0)]
    for i, b in enumerate(basis):
        if obj[b] != 0:
            f = obj[b]
            obj = [o - f * x for o, x in zip(obj, T[i])]
    TT = T + [obj]
    st = _simplex(TT, basis, len(T), ncols)
    if st == "unbounded":
        return "unbounded"
    # recover the optimal point and check it exactly against the original constraints
    val = [Fraction(0)] * ncols
    for i, b in enumerate(basis):
        val[b] = TT[i][-1]
    t = [val[j] - val[d + j] for j in range(d)]
    a = [a0[k] + sum(t[j] * K[j][k] for j in range(d)) for k in range(n)]
    assert all(sum(Fraction(x) * y for x, y in zip(row, a)) >= v for row, v in zip(G, g))
    assert all(sum(Fraction(x) * y for x, y in zip(row, a)) == v for row, v in zip(E, e))
    value = sum(Fraction(ci) * y for ci, y in zip(c, a))
    assert value == c0 + sense * (TT[-1][-1])
    return value
