"""Finish line (C), C1 27/09: the proven trap criterion (notes/139) applied to an explicit envelope U.
U = odd unimodular, dim 24, min >= 2, given by generators (rational vectors in R^24) or by an integral Gram matrix.
  (M) every norm-3 vector x has |(r,x)| <= 1 for every root r (automatic in U);
  (E) a frame vector u satisfies n_u := #{roots r : (r,u) = +-1} <= r/4        (Sol's theta theorems, checked on examples);
  (P) any real w with |w|^2 < 8/7 and (w,u) in Z for the 42 u lies in N-perp (dim 2).
Admissible = norm-3 vectors with n_x <= r/4.  L_adm = Z-span of the admissible vectors (it must contain N, so rank >= 22).
If rank(L_adm) = 24 - d, the short vectors of L_adm* (norm < 8/7) together with the d-dimensional orthogonal complement must
span at most 2 dimensions; otherwise U carries no frame.  (Sound: any w integral on all admissible x is integral on the u.)
Usage (module): trap_verdict(gens) -> dict."""
import itertools
from fractions import Fraction as F
import numpy as np


def to_int_basis(gens):
    """Z-basis of the lattice spanned by rational generators (rows), via integer HNF after scaling."""
    den = 1
    for v in gens:
        for x in v:
            den = den * F(x).denominator // np.gcd(den, F(x).denominator)
    M = [[int(F(x) * den) for x in v] for v in gens]
    B = hnf_rows(M)
    return [[F(x, den) for x in row] for row in B]


def hnf_rows(M):
    """Row-style Hermite normal form (integer), returns the nonzero rows."""
    A = [row[:] for row in M]
    m, n = len(A), len(A[0])
    r = 0
    for c in range(n):
        piv = [i for i in range(r, m) if A[i][c] != 0]
        if not piv:
            continue
        while True:
            piv = [i for i in range(r, m) if A[i][c] != 0]
            if len(piv) == 1:
                break
            i0 = min(piv, key=lambda i: abs(A[i][c]))
            A[r], A[i0] = A[i0], A[r]
            for i in range(r + 1, m):
                if A[i][c]:
                    q = A[i][c] // A[r][c]
                    A[i] = [a - q * b for a, b in zip(A[i], A[r])]
        i0 = piv[0]
        A[r], A[i0] = A[i0], A[r]
        if A[r][c] < 0:
            A[r] = [-a for a in A[r]]
        r += 1
        if r == m:
            break
    return [row for row in A[:r]]


def lll(B, delta=0.99):
    """LLL on exact rational rows (Gram-Schmidt in floats, updates exact)."""
    B = [row[:] for row in B]
    n = len(B)
    dot = lambda u, v: sum(a * b for a, b in zip(u, v))

    def gso():
        Bs, mu = [], [[0.0] * n for _ in range(n)]
        Bf = [np.array([float(x) for x in row]) for row in B]
        for i in range(n):
            v = Bf[i].copy()
            for j in range(i):
                mu[i][j] = float(Bf[i] @ Bs[j]) / float(Bs[j] @ Bs[j])
                v = v - mu[i][j] * Bs[j]
            Bs.append(v)
        return Bs, mu
    Bs, mu = gso()
    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                B[k] = [a - q * b for a, b in zip(B[k], B[j])]
                Bs, mu = gso()
        if float(Bs[k] @ Bs[k]) >= (delta - mu[k][k - 1] ** 2) * float(Bs[k - 1] @ Bs[k - 1]):
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            Bs, mu = gso()
            k = max(k - 1, 1)
    return B


def inverse_exact(M):
    n = len(M)
    A = [[F(x) for x in row] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0)
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [row[n:] for row in A]


def gram(B):
    return [[sum(a * b for a, b in zip(u, v)) for v in B] for u in B]


def short_vectors(G, bound, strict=False):
    """All nonzero integer coefficient vectors x (up to sign) with x^T G x <= bound (Fincke-Pohst, exact check)."""
    n = len(G)
    Gf = np.array([[float(x) for x in row] for row in G])
    L = np.linalg.cholesky(Gf)          # G = L L^T
    Q = np.zeros((n, n)); d = np.zeros(n)
    for i in range(n):
        d[i] = L[i, i] ** 2
        for j in range(i + 1, n):
            Q[i, j] = L[j, i] / L[i, i]
    out = []
    x = [0] * n
    eps = 1e-9

    def rec(k, rem):
        c = -sum(Q[k, j] * x[j] for j in range(k + 1, n))
        span_ = np.sqrt(max(rem, 0) / d[k]) + eps
        for xi in range(int(np.ceil(c - span_)), int(np.floor(c + span_)) + 1):
            x[k] = xi
            r2 = rem - d[k] * (xi - c) ** 2
            if r2 < -eps:
                continue
            if k == 0:
                if any(x):
                    val = sum(G[i][j] * x[i] * x[j] for i in range(n) for j in range(n))
                    if (val < bound if strict else val <= bound):
                        out.append((tuple(x), val))
            else:
                rec(k - 1, r2)
        x[k] = 0
    rec(n - 1, float(bound) + eps)
    seen, res = set(), []
    for v, val in out:
        key = tuple(-a for a in v) if next(a for a in v if a) < 0 else v
        if key not in seen:
            seen.add(key); res.append((key, val))
    return res


def trap_verdict(gens):
    B = lll(to_int_basis(gens))
    assert len(B) == 24, len(B)
    G = gram(B)
    det = round(np.linalg.det(np.array([[float(x) for x in r] for r in G])))
    vecs = short_vectors(G, 3)
    roots = [v for v, n in vecs if n == 2]
    n3 = [v for v, n in vecs if n == 3]
    if any(n == 1 for v, n in vecs):
        return {'error': 'norm-1 vectors present'}
    Gm = np.array([[float(x) for x in r] for r in G])
    R = np.array(roots, dtype=float).reshape(-1, 24)
    X = np.array(n3, dtype=float)
    P = X @ Gm @ R.T if len(roots) else np.zeros((len(n3), 0))      # inner products (x, r), roots up to sign
    n_x = 2 * (np.abs(np.rint(P)) == 1).sum(axis=1)                  # count +-r
    rtot = 2 * len(roots)
    adm = [v for v, k in zip(n3, n_x) if k <= rtot / 4]
    res = {'det': det, 'roots': rtot, 'norm3': 2 * len(n3), 'admissible': 2 * len(adm)}
    if not adm:
        res['verdict'] = 'EXCLUDED (no admissible norm-3 vector)'; return res
    A = hnf_rows([list(v) for v in adm])
    rank = len(A); res['rank_Ladm'] = rank
    if rank < 22:
        res['verdict'] = 'EXCLUDED (admissible span has rank < 22, cannot contain N)'; return res
    # dual of L_adm inside its span: reduced real basis of L_adm, exact Gram inverse = Gram of the dual basis
    Areal = lll([[sum(F(a[i]) * B[i][k] for i in range(24)) for k in range(24)] for a in A])
    GA = gram(Areal)
    sv = short_vectors(inverse_exact(GA), F(8, 7), strict=True)
    dim_short = int(np.linalg.matrix_rank(np.array([v for v, n in sv], dtype=float))) if sv else 0
    res.update(short_dual=2 * len(sv), dim_short=dim_short, codim=24 - rank)
    res['verdict'] = ('EXCLUDED (trap: %d short dual dims + %d orthogonal > 2)' % (dim_short, 24 - rank)
                      if dim_short + (24 - rank) > 2 else 'survives the trap')
    return res
