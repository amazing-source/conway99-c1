"""Square-class decomposition of four-star objects in the pencil T + U = 7 Pi (LAB 15/10/2026, SQ30 mechanism hunt).

On Y = (star vectors)^perp the form P = 7 Pi is positive definite and T + U = P.  With A = P^-1 T (eigenvalues in
[0, 1]), E_0 = ker T, C = the P-orthogonal complement of E_0 in Y:
    class(T) = class(P|Y) * class(P|E_0) * class(prod of the non-zero eigenvalues of A)        (in Q*/Q*^2)
and P|E_0 = U|E_0 (x in ker T gives x^T P x = x^T U x).  All classes exact (integer Gram matrices, Bareiss).
Printed per object: class(T) [8T], class(U) [240U, rank r_U], class(P|E_0) [Gram of an integer basis of ker 8T under
1680 Pi], class(prod lambda) deduced, and the rational pencil eigenvalues 3/7, 5/7, 1 with their multiplicities.
usage: python cls_decomp.py <bundle json> [max objects] [stride]"""
import json
import math
import sys
from fractions import Fraction as Fr

from stars_rank import kval, MATE
from sc_square_class import det_int

PR = (1 << 61) - 1


def indep_rows(M):
    """indices of a maximal independent set of rows (mod a large prime, generic)."""
    n = len(M)
    A = [[x % PR for x in row] for row in M]
    basis = []          # list of (pivot col, reduced row)
    rows = []
    for i in range(n):
        v = A[i][:]
        for c, b in basis:
            if v[c]:
                f = v[c]
                v = [(x - f * y) % PR for x, y in zip(v, b)]
        c = next((j for j, x in enumerate(v) if x), None)
        if c is None:
            continue
        inv = pow(v[c], PR - 2, PR)
        v = [x * inv % PR for x in v]
        basis.append((c, v))
        rows.append(i)
    return rows


def sqclass(q):
    """squarefree class of a non-zero rational (sign included), as (sign, sorted primes, leftover)."""
    q = Fr(q)
    s = -1 if q < 0 else 1
    d = abs(q.numerator) * q.denominator
    out = []
    for p in range(2, 2000):
        if p > 2 and any(p % r == 0 for r in range(2, int(p ** 0.5) + 1)):
            continue
        e = 0
        while d % p == 0:
            d //= p
            e += 1
        if e % 2:
            out.append(p)
    r = math.isqrt(d)
    left = 1 if r * r == d else d
    return (s, tuple(out), left)


def fmt(c):
    s, ps, left = c
    t = ("-" if s < 0 else "") + ("*".join(map(str, ps)) if ps else "1")
    return t + ("" if left == 1 else "*[%d]" % left)


def mul(*cs):
    s = 1
    ps = set()
    left = 1
    for c in cs:
        s *= c[0]
        ps ^= set(c[1])
        left *= c[2]
    return (s, tuple(sorted(ps)), left)


def nonzero_class(M):
    I = indep_rows(M)
    d = det_int([[M[i][j] for j in I] for i in I])
    assert d != 0
    return len(I), sqclass(d)


def nullspace_int(M):
    n = len(M)
    A = [[Fr(x) for x in row] for row in M]
    piv = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, n) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(n):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    out = []
    for f in [c for c in range(n) if c not in piv]:
        v = [Fr(0)] * n
        v[f] = Fr(1)
        for i, c in enumerate(piv):
            v[c] = -A[i][f]
        den = 1
        for x in v:
            den = den * x.denominator // math.gcd(den, x.denominator)
        out.append([int(x * den) for x in v])
    return out


def main():
    d = json.load(open(sys.argv[1]))
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    structs = d["structures"] if "structures" in d else [d]
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else len(structs)
    stride = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    def qinv(y, z):
        v = Fr(0)
        if y == z:
            v += Fr(1, 20) + Fr(1, 24)
        if z == MATE(y):
            v += Fr(1, 20) - Fr(1, 24)
        return v - Fr(1, 240)
    Pi = [[(Fr(1) if a == b else Fr(0)) - sum(qinv(y, z) for y in S[a] for z in S[b]) for b in range(n)] for a in range(n)]
    P1680 = [[int(1680 * Pi[a][b]) for b in range(n)] for a in range(n)]
    assert all(1680 * Pi[a][b] == P1680[a][b] for a in range(n) for b in range(n))
    K8 = [[int(round(8 * kval(S[a], S[b]))) for b in range(n)] for a in range(n)]
    rP, cP = nonzero_class(P1680)
    print("P = 7 Pi on Y: rank %d, class %s (of 1680 Pi; even rank so scale-free)" % (rP, fmt(cP)), flush=True)
    tally = {}
    for k in range(0, min(mx * stride, len(structs)), stride):
        s = structs[k]
        G = [[0] * n for _ in range(n)]
        for i, j in s["edges"]:
            G[i][j] = G[j][i] = 1
        M = [[(24 if a == b else 0) - 8 * G[a][b] - K8[a][b] for b in range(n)] for a in range(n)]
        rT, cT = nonzero_class(M)
        U240 = [[2 * P1680[a][b] // 14 * 1 if False else (P1680[a][b] * 240 // 1680 * 7) - 30 * M[a][b] for b in range(n)] for a in range(n)]
        # 240 U = 240 (7 Pi - T) = 1680 Pi - 30 * 8T
        U240 = [[P1680[a][b] - 30 * M[a][b] for b in range(n)] for a in range(n)]
        rU, cU = nonzero_class(U240)
        if rU % 2:
            cU = mul(cU, sqclass(240))       # class(U) = class(240 U) * class(240)^rU
        N = nullspace_int(M)
        GN = [[sum(N[i][a] * sum(P1680[a][b] * N[j][b] for b in range(n)) for a in range(n)) for j in range(len(N))] for i in range(len(N))]
        rE, cE = nonzero_class(GN)
        cl = mul(cT, cP, cE)            # class of prod lambda (8^30 is a square)
        key = (fmt(cT), fmt(cU), rU, fmt(cE), fmt(cl))
        tally[key] = tally.get(key, 0) + 1
        print("%d c=%s | T rank %d class %s | U rank %d class %s | P|kerT rank %d class %s | prod lambda class %s"
              % (k, s.get("c"), rT, fmt(cT), rU, fmt(cU), rE, fmt(cE), fmt(cl)), flush=True)
    print("TALLY (class T, class U, rank U, class P|E0, class prod lambda):")
    for key, c in sorted(tally.items(), key=lambda t: -t[1]):
        print("  %4d  %s" % (c, key))


if __name__ == "__main__":
    main()
