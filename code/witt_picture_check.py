"""Consistency checks for the 7-adic quadratic-space picture of notes/102, on existing SRGs with the same shape
(p | r - s, p prime to n):  global W = 1^perp mod p (non-split iff ...), rho_s, rho_r reductions of the eigenlattices,
G = rho_s cap rho_r (radical), U = rho_s / G, U' = rho_r / G; Witt types (split / non-split) predicted by the genus.
Here we simply compute everything directly for Petersen (p=3) and T(7) (p=5) and print dims and discriminants.
"""
import numpy as np
import itertools
import genus_tools as gt
import eigenlattice_check as ec


def rank_mod(M, p):
    return ec.rank_mod([list(map(int, r)) for r in M], p)


def span_basis_mod(vectors, p):
    """row-reduced basis (list of lists) of the span of vectors mod p"""
    M = [[x % p for x in v] for v in vectors]
    rows = []
    for v in M:
        v = v[:]
        for (piv, r) in rows:
            if v[piv]:
                f = v[piv]
                v = [(a - f * b) % p for a, b in zip(v, r)]
        nz = next((i for i, x in enumerate(v) if x), None)
        if nz is not None:
            inv = pow(v[nz], -1, p)
            v = [(x * inv) % p for x in v]
            rows = [(pv, [(a - r[nz] * b) % p for a, b in zip(r, v)]) for (pv, r) in rows]
            rows.append((nz, v))
    return [r for _, r in rows]


def form_type(basis, p):
    """rank and Legendre symbol of the discriminant of the standard form restricted to span(basis), modulo radical."""
    n = len(basis)
    if n == 0:
        return 0, 1
    G = [[sum(a * b for a, b in zip(u, v)) % p for v in basis] for u in basis]
    # reduce: rank and determinant of nondegenerate part via diagonalisation mod p
    G = [row[:] for row in G]
    d = []
    idx = list(range(n))
    while idx:
        i = next((k for k in idx if G[k][k] % p), None)
        if i is None:
            pair = next(((a, b) for a in idx for b in idx if a != b and G[a][b] % p), None)
            if pair is None:
                break
            a, b = pair
            for c in range(n):
                G[a][c] = (G[a][c] + G[b][c]) % p
            for c in range(n):
                G[c][a] = (G[c][a] + G[c][b]) % p
            i = a
        piv = G[i][i]
        d.append(piv)
        inv = pow(piv, -1, p)
        rest = [k for k in idx if k != i]
        for a in rest:
            f = (G[a][i] * inv) % p
            if f:
                for c in range(n):
                    G[a][c] = (G[a][c] - f * G[i][c]) % p
        for a in rest:
            G[a][i] = 0; G[i][a] = 0
        idx = rest
    disc = 1
    for x in d:
        disc = (disc * x) % p
    leg = 1 if pow(disc, (p - 1) // 2, p) == 1 else -1
    return len(d), leg


def split_type(dim, leg, p):
    if dim % 2:
        return 'odd dim'
    r = dim // 2
    target = 1 if (pow(-1 % p, r * (p - 1) // 2, p) == 1) else -1       # Legendre of (-1)^r
    return 'split' if leg == target else 'non-split'


def analyse(name, A, r_ev, s_ev, p):
    A = np.asarray(A, dtype=np.int64); n = len(A)
    Bs = ec.int_kernel((A - s_ev * np.eye(n, dtype=np.int64)).tolist())
    Br = ec.int_kernel((A - r_ev * np.eye(n, dtype=np.int64)).tolist())
    rs = span_basis_mod(Bs, p); rr = span_basis_mod(Br, p)
    # intersection G = rho_s cap rho_r via dimension formula and explicit kernel
    both = span_basis_mod(rs + rr, p)
    dimG = len(rs) + len(rr) - len(both)
    ts, ls = form_type(rs, p)
    tr, lr = form_type(rr, p)
    print(f'{name} (p={p}): dim rho_s={len(rs)}, rho_r={len(rr)}, dim G={dimG}, rank_p(A-rI)={rank_mod(A - r_ev*np.eye(n,dtype=np.int64), p)};'
          f'  U=rho_s/G: dim {ts}, {split_type(ts, ls, p)};  U\'=rho_r/G: dim {tr}, {split_type(tr, lr, p)}')


if __name__ == '__main__':
    analyse('Petersen', ec.petersen(), 1, -2, 3)
    analyse('T(7)', ec.triangular(7), 3, -2, 5)
    analyse('T(8)', ec.triangular(8), 4, -2, 3)
    analyse('T(9)', ec.triangular(9), 5, -2, 7)
