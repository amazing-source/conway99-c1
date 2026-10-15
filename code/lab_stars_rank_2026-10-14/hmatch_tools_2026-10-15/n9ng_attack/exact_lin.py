"""Exact rational linear algebra helpers (Fraction RREF, nullspace, rank)."""
from fractions import Fraction as F

def rref(M):
    M = [[F(x) for x in row] for row in M]
    rows, cols = len(M), (len(M[0]) if M else 0)
    piv = []; r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                fac = M[i][c]
                M[i] = [a - fac * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == rows: break
    return M[:r], piv

def rank(M):
    return len(rref(M)[0]) if M else 0

def nullspace(M):
    """basis of {x : M x = 0}"""
    cols = len(M[0])
    R, piv = rref(M)
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for fc in free:
        v = [F(0)] * cols; v[fc] = F(1)
        for i, pc in enumerate(piv):
            v[pc] = -R[i][fc]
        basis.append(v)
    return basis
