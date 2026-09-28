"""Exact short-dual-class obstruction for Conway rank-17 skeletons.

Input convention: rows of a K-basis have integral Gram G. A dual vector is
specified by integer z, so its K-basis coefficients are G^{-1}z. Skeleton
classes are bit masks in that SAME K-basis, not ambient V coordinates.

This module verifies supplied witnesses; it does not enumerate short vectors.
No norm lower bound on K is assumed: unit vectors are explicitly allowed.
"""
from fractions import Fraction as F
from typing import Iterable, Sequence

FORBIDDEN_N = frozenset((2, 4, 6, 8, 10, 14))  # n = 7 ||kappa||^2


def inverse_and_det(G: Sequence[Sequence[int]]):
    n = len(G)
    if not n or any(len(r) != n for r in G):
        raise ValueError('G must be a nonempty square matrix')
    if any(G[i][j] != G[j][i] for i in range(n) for j in range(n)):
        raise ValueError('G must be symmetric')
    # Exact LDL elimination also checks positive definiteness.
    Q = [[F(v) for v in r] for r in G]
    for k in range(n):
        if Q[k][k] <= 0:
            raise ValueError('G is not positive definite')
        for i in range(k + 1, n):
            for j in range(i, n):
                Q[j][i] = Q[i][j] = Q[i][j] - Q[i][k] * Q[k][j] / Q[k][k]
    A = [[F(G[i][j]) for j in range(n)] + [F(i == j) for j in range(n)] for i in range(n)]
    det = F(1)
    for k in range(n):
        p = next((i for i in range(k, n) if A[i][k]), None)
        if p is None:
            raise ValueError('Singular Gram matrix')
        if p != k:
            A[k], A[p] = A[p], A[k]
            det = -det
        v = A[k][k]
        det *= v
        A[k] = [x / v for x in A[k]]
        for i in range(n):
            if i != k:
                v = A[i][k]
                A[i] = [x - v * y for x, y in zip(A[i], A[k])]
    return [r[n:] for r in A], det


def validate_K(G):
    """Check rank 15, determinant 49, 7-elementary anisotropic discriminant."""
    if len(G) != 15:
        raise ValueError('This theorem is stated for rank-15 K')
    Gi, det = inverse_and_det(G)
    if det != 49:
        raise ValueError('Expected det K = 49')
    if any((7 * x).denominator != 1 for r in Gi for x in r):
        raise ValueError('Discriminant is not 7-elementary')
    cols = [tuple(int(7 * Gi[i][j]) % 7 for i in range(15)) for j in range(15)]
    inds, span = [], {tuple([0] * 15)}
    for j, v in enumerate(cols):
        if v not in span:
            inds.append(j)
            span = {tuple((s[i] + a * v[i]) % 7 for i in range(15))
                    for s in span for a in range(7)}
    if len(inds) != 2 or len(span) != 49:
        raise ValueError('Expected a two-dimensional discriminant group')
    i, j = inds
    for a in range(7):
        for b in range(7):
            if a or b:
                q = a*a*Gi[i][i] + 2*a*b*Gi[i][j] + b*b*Gi[j][j]
                if q.denominator == 1:
                    raise ValueError('The discriminant form is isotropic')
    return Gi


def dual_record(G, Gi, z):
    """Return an exact record for an integer dual-coordinate vector z."""
    d = len(G)
    if len(z) != d or any(F(x).denominator != 1 for x in z):
        raise ValueError('z must have d integer coordinates')
    z = [int(x) for x in z]
    if not any(z):
        return None
    k = [sum(Gi[i][j] * z[j] for j in range(d)) for i in range(d)]
    n = 7 * sum(F(z[i]) * k[i] for i in range(d))
    b = [7 * x for x in k]
    if n.denominator != 1 or any(x.denominator != 1 for x in b):
        raise ValueError('Invalid 7-elementary dual data')
    n = int(n)
    mask = sum((int(b[i]) % 2) << i for i in range(d))
    if n == 14 and any(x.denominator != 1 for x in k):
        raise ValueError('Norm-2 dual is not integral: anisotropy hypothesis failed')
    return {'z': z, 'n': n, 'class': mask, 'forbidden': n in FORBIDDEN_N}


def build_forbidden(G, dual_vectors: Iterable[Sequence[int]]):
    """Omitted short dual vectors only weaken this test; witnesses stay sound."""
    Gi = validate_K(G)
    bad = {}
    for z in dual_vectors:
        rec = dual_record(G, Gi, z)
        if rec is not None and rec['forbidden']:
            if not rec['class']:
                raise ValueError('Unexpected zero-class forbidden witness')
            old = bad.get(rec['class'])
            if old is None or rec['n'] < old['n']:
                bad[rec['class']] = rec
    return bad


def prefix_obstruction(G, generators, bad):
    """Return one certificate excluding ALL completions of a prefix, or None.

    generators = g_2,...,g_{k+1}, k <= 6, as SAME-BASIS bit masks.
    Certificates include the subset XOR and an independently checkable dual z.
    """
    d = len(G)
    if not 0 <= len(generators) <= 6:
        raise ValueError('Expected at most six anchor classes')
    vectors = []
    span = {0: 0}
    for j, g in enumerate(generators):
        g = int(g)
        if not 0 < g < (1 << d) or g in span:
            raise ValueError('Invalid or dependent anchor class')
        v = [(g >> i) & 1 for i in range(d)]
        vv = sum(v[a] * G[a][b] * v[b] for a in range(d) for b in range(d))
        if vv % 4 != 2:
            raise ValueError('An anchor must have q=1')
        for u in vectors:
            uv = sum(u[a] * G[a][b] * v[b] for a in range(d) for b in range(d))
            if uv % 2 != 1:
                raise ValueError('Distinct anchors must pair oddly')
        vectors.append(v)
        new = {s ^ g: sub | (1 << j) for s, sub in span.items()}
        for mask, sub in new.items():
            if mask in bad:
                return {'prefix_length': j + 1, 'subset_mask': sub,
                        'class': mask, 'dual': bad[mask]}
        span.update(new)
    return None


def minkowski_separation(target, domains, dual):
    """Verify an exact separator for a forced K4 sum (or any Minkowski sum).

    All vectors use common integral coordinates. Supply a rational linear
    functional 'dual' in coordinate-dual coordinates, not a metric vector.
    Empty domains certify infeasibility immediately. No LP solver is required.
    """
    d = len(target)
    if len(dual) != d:
        raise ValueError('Wrong functional dimension')
    f = [F(x) for x in dual]
    def dot(v):
        if len(v) != d:
            raise ValueError('Wrong vector dimension')
        return sum(f[i] * F(v[i]) for i in range(d))
    lhs = dot(target)
    rhs = F(0)
    for dom in domains:
        vals = [dot(v) for v in dom]
        if not vals:
            return {'excluded': True, 'reason': 'empty domain'}
        rhs += max(vals)
    return {'excluded': lhs > rhs, 'lhs': str(lhs), 'rhs': str(rhs),
            'gap': str(lhs-rhs)}
