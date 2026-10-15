"""Check of the star-complement square-class lemma (LAB, 15/10/2026).

LEMMA.  Let M be an integral symmetric n x n matrix of rank r.  For every r-subset H with det M_H != 0, det M_H lies in
the same class of Q*/Q*^2 (sign included).  Proof: on R = M Z^n put b(Mx, My) = x^T M y (well defined); the r vectors
M e_h (h in H) span a sublattice R_H of full rank r with Gram matrix M_H, so det M_H = disc(R) [R : R_H]^2.
For a graph and an integer eigenvalue mu of multiplicity m, M = mu I - A has rank n - m and the H above are exactly the
star complements for mu.

This script enumerates all r-subsets (small graphs) or samples random ones (larger graphs) and prints the squarefree
part (with sign) of every non-zero det M_H.
usage: python sc_square_class.py petersen|paley9|paley25|cube|random [samples]
"""
import itertools
import math
import random
import sys
from fractions import Fraction as Fr


def det_int(M):
    """Bareiss fraction-free determinant of an integer matrix."""
    A = [row[:] for row in M]
    n = len(A)
    sign, prev = 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if sw is None:
                return 0
            A[k], A[sw] = A[sw], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def squarefree(d):
    s = -1 if d < 0 else 1
    d = abs(d)
    out = 1
    p = 2
    while p * p <= d:
        e = 0
        while d % p == 0:
            d //= p
            e += 1
        if e % 2:
            out *= p
        p += 1
    return s * out * d


def rank_frac(M):
    A = [[Fr(x) for x in row] for row in M]
    n, m = len(A), len(A[0])
    r = 0
    for c in range(m):
        p = next((i for i in range(r, n) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        for i in range(n):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        r += 1
    return r


def graph(name):
    if name == "petersen":
        V = list(itertools.combinations(range(5), 2))
        return [[1 if not set(a) & set(b) else 0 for b in V] for a in V]
    if name in ("paley9", "paley25"):
        q = 9 if name == "paley9" else 25
        p = 3 if q == 9 else 5
        # F_q = F_p[i]/(i^2 - nonresidue); elements (a, b) = a + b i
        nr = 2 if p in (3, 5) else None
        els = [(a, b) for a in range(p) for b in range(p)]
        def mul(x, y):
            return ((x[0] * y[0] + nr * x[1] * y[1]) % p, (x[0] * y[1] + x[1] * y[0]) % p)
        sq = {mul(x, x) for x in els if x != (0, 0)}
        return [[1 if x != y and ((x[0] - y[0]) % p, (x[1] - y[1]) % p) in sq else 0 for y in els] for x in els]
    if name == "cube":
        V = list(range(8))
        return [[1 if bin(a ^ b).count("1") == 1 else 0 for b in V] for a in V]
    raise SystemExit("unknown graph")


def main():
    name = sys.argv[1]
    samples = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    A = graph(name)
    n = len(A)
    # integer eigenvalues: try mu in range
    for mu in range(-n, n + 1):
        M = [[(mu if i == j else 0) - A[i][j] for j in range(n)] for i in range(n)]
        r = rank_frac(M)
        if r == n:
            continue
        classes = {}
        rng = random.Random(7)
        subsets = itertools.combinations(range(n), r) if samples == 0 else (
            sorted(rng.sample(range(n), r)) for _ in range(samples))
        tested = 0
        for H in subsets:
            d = det_int([[M[i][j] for j in H] for i in H])
            if d == 0:
                continue
            tested += 1
            c = squarefree(d)
            classes[c] = classes.get(c, 0) + 1
        print("%s: mu = %d, multiplicity %d, star complements of size %d: %d non-singular tested, square classes %s"
              % (name, mu, n - r, r, tested, classes), flush=True)


main()
