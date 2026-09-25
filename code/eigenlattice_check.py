"""Direct computation of SRG eigenlattices Lambda_theta = Z^n cap ker(A - theta I) (notes/101):
determinant, discriminant group (Smith form), p-adic Jordan symbols, oddity formula, and the relation
alpha = rank_p(A - r I) - 1 between the p-part of disc(Lambda_s) and the p-rank (p | r - s, p prime to n).
Used to validate, on existing graphs, the derivation that excludes k = 30 for srg(99,14,1,2).
"""
import itertools, sys
from fractions import Fraction as Fr
import numpy as np
import genus_tools as gt


def int_kernel(M):
    """Z-basis of {v in Z^n : M v = 0} by unimodular column reduction (exact Python ints)."""
    M = [list(map(int, row)) for row in M]
    m, n = len(M), len(M[0])
    T = [[int(i == j) for j in range(n)] for i in range(n)]        # columns transform
    cols = list(range(n))
    r = 0
    for i in range(m):
        # reduce row i on columns r..n-1 to a single nonzero at column r (Euclid on columns)
        while True:
            nz = [j for j in range(r, n) if M[i][j] != 0]
            if len(nz) <= 1:
                break
            jmin = min(nz, key=lambda j: abs(M[i][j]))
            for j in nz:
                if j != jmin:
                    q = M[i][j] // M[i][jmin]
                    for a in range(m):
                        M[a][j] -= q * M[a][jmin]
                    for a in range(n):
                        T[a][j] -= q * T[a][jmin]
        nz = [j for j in range(r, n) if M[i][j] != 0]
        if nz:
            j = nz[0]
            if j != r:
                for a in range(m):
                    M[a][j], M[a][r] = M[a][r], M[a][j]
                for a in range(n):
                    T[a][j], T[a][r] = T[a][r], T[a][j]
            r += 1
    return [[T[a][j] for a in range(n)] for j in range(r, n)]      # kernel basis vectors


def smith_diag(G):
    import sympy
    from sympy.matrices.normalforms import smith_normal_form
    D = smith_normal_form(sympy.Matrix(G), domain=sympy.ZZ)
    return [abs(int(D[i, i])) for i in range(min(D.shape))]


def rank_mod(M, p):
    M = [[x % p for x in row] for row in M]
    m, n = len(M), len(M[0]); r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], -1, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(m):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r


def analyse(name, A, r_ev, s_ev):
    A = np.asarray(A, dtype=np.int64); n = len(A)
    out = [f'== {name}: n={n}, eigenvalues r={r_ev}, s={s_ev}']
    for th in (s_ev, r_ev):
        M = (A - th * np.eye(n, dtype=np.int64)).tolist()
        B = int_kernel(M)
        G = [[sum(u[i] * v[i] for i in range(n)) for v in B] for u in B]
        D = gt.det_frac(G)
        sd = [d for d in smith_diag(G) if d != 1]
        even = all(G[i][i] % 2 == 0 for i in range(len(G)))
        lhs = None
        if D % 2 == 1:
            lhs = (len(G) + sum(gt.p_excess(G, p) for p in gt.odd_primes(D))) % 8
        syms = {p: gt.jordan_symbol(G, p) for p in gt.odd_primes(D)}
        out.append(f'  Lambda_{th}: rank {len(B)}, det {D}, even {even}, disc invariants {sd}, '
                   f'Jordan {syms}, sig+excess mod 8 = {lhs} (must be 0 if even)')
    p_list = [q for q in gt.odd_primes(r_ev - s_ev)] + ([2] if (r_ev - s_ev) % 2 == 0 else [])
    for p in p_list:
        rk = rank_mod((A - r_ev * np.eye(n, dtype=np.int64)).tolist(), p)
        out.append(f'  rank_{p}(A - rI) = {rk}  -> predicted p-part rank of disc(Lambda_s) = {rk - 1}')
    print('\n'.join(out), flush=True)


def petersen():
    V = list(itertools.combinations(range(5), 2))
    return [[1 if not set(a) & set(b) else 0 for b in V] for a in V]


def triangular(m):
    V = list(itertools.combinations(range(m), 2))
    return [[1 if (a != b and set(a) & set(b)) else 0 for b in V] for a in V]


if __name__ == '__main__':
    analyse('Petersen srg(10,3,0,1)', petersen(), 1, -2)
    analyse('T(7) srg(21,10,5,4)', triangular(7), 3, -2)
    analyse('T(8) srg(28,12,6,4)', triangular(8), 4, -2)
    import graphs
    analyse('srg(9,4,1,2)', graphs.srg9(), 1, -2)
