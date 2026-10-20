"""p-rank calibration on real strongly regular graphs (LAB, 20/10/2026, NOTE_BORNE_RANG).

For an srg with eigenvalues k > r > s (multiplicities 1, f, g) and a prime p with p | (r - s), print
rank_p(A - r I) (= rank_p(A - s I) when p | r - s), the bound min(f, g) + 1 (van Eijl / Brouwer-van Eijl) and the
'glue rank' rank_p - 1 = 7-rank analogue of disc(E_s).  Question: where do real graphs sit between the smallest and
the largest allowed p-rank, and does the p-rank go up when the automorphism group gets smaller?

usage: python prank_calib.py <edges or builtin name> ...   (builtin: rook3, petersen, T7)
"""
import itertools
import math
import sys

import numpy as np


def rank_mod(M, p):
    M = (M % p).astype(np.int64)
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        if r == rows:
            break
        piv = np.nonzero(M[r:, c])[0]
        if len(piv) == 0:
            continue
        i = r + piv[0]
        if i != r:
            M[[r, i]] = M[[i, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        nz = np.nonzero(M[:, c])[0]
        nz = nz[nz != r]
        if len(nz):
            M[nz] = (M[nz] - np.outer(M[nz, c], M[r])) % p
        r += 1
    return r


def builtin(name):
    if name == "rook3":
        V = [(a, b) for a in range(3) for b in range(3)]
        adj = lambda x, y: x != y and (x[0] == y[0] or x[1] == y[1])
    elif name == "petersen":
        V = list(itertools.combinations(range(5), 2))
        adj = lambda x, y: not set(x) & set(y)
    elif name == "T7":
        V = list(itertools.combinations(range(7), 2))
        adj = lambda x, y: x != y and bool(set(x) & set(y))
    else:
        raise SystemExit("unknown builtin " + name)
    n = len(V)
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for j in range(n):
            if adj(V[i], V[j]):
                A[i, j] = 1
    return A


def load(path):
    edges = [tuple(map(int, l.split()[:2])) for l in open(path) if l.strip() and not l.startswith("#")]
    n = 1 + max(max(e) for e in edges)
    A = np.zeros((n, n), dtype=np.int64)
    for a, b in edges:
        A[a, b] = A[b, a] = 1
    return A


def params(A):
    n = len(A)
    k = int(A[0].sum())
    A2 = A @ A
    lam = {int(A2[i, j]) for i in range(n) for j in range(n) if i != j and A[i, j]}
    mu = {int(A2[i, j]) for i in range(n) for j in range(n) if i != j and not A[i, j]}
    assert len(lam) == 1 and len(mu) == 1 and (A.sum(1) == k).all(), "not an srg"
    lam, mu = lam.pop(), mu.pop()
    disc = (lam - mu) ** 2 + 4 * (k - mu)
    sq = math.isqrt(disc)
    assert sq * sq == disc, "conference-type eigenvalues"
    r, s = ((lam - mu) + sq) // 2, ((lam - mu) - sq) // 2
    f = (-k - s * (n - 1)) // (r - s)
    g = n - 1 - f
    return n, k, lam, mu, r, s, f, g


def primes_of(m):
    out, d = [], 2
    while d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d
                e += 1
            out.append((d, e))
        d += 1
    if m > 1:
        out.append((m, 1))
    return out


def main():
    for arg in sys.argv[1:]:
        A = builtin(arg) if not arg.endswith(".edges") else load(arg)
        n, k, lam, mu, r, s, f, g = params(A)
        name = arg.replace("\\", "/").split("/")[-1]
        for p, e in primes_of(r - s):
            rk = rank_mod(A - r * np.eye(n, dtype=np.int64), p)
            print("%-34s srg(%d,%d,%d,%d) r=%d s=%d f=%d g=%d | p=%d (p^%d || r-s) rank_p(A-rI)=%d  min(f,g)+1=%d"
                  % (name, n, k, lam, mu, r, s, f, g, p, e, rk, min(f, g) + 1), flush=True)


if __name__ == "__main__":
    main()
