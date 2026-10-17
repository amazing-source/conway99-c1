"""Anatomy of ker T_S on rank-30 objects (Conway-compatible four-star blocks, all with c >= 2):
dimensions of kernel intersections with coordinate subspaces, and an LLL-reduced integer basis."""
import itertools, json, sys
from fractions import Fraction
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8

IDX = {l: i for i, l in enumerate(S)}
XL = [i for i, l in enumerate(S) if l & {0, 1}]
Y = [i for i, l in enumerate(S) if not (l & {0, 1})]
YP = [i for i, l in enumerate(S) if (l & {0, 1}) and not (l & {2, 3})]
Q = [i for i, l in enumerate(S) if (l & {0, 1}) and (l & {2, 3})]
K8 = [[k8(a, b) for b in S] for a in S]


def nullspace_frac(M):
    n = len(M[0])
    A = [[Fraction(x) for x in r] for r in M]
    piv = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        iv = 1 / A[r][c]
        A[r] = [x * iv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * n
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -A[i][f]
        basis.append(v)
    return basis


def to_int(v):
    from math import lcm, gcd
    d = 1
    for x in v:
        d = lcm(d, x.denominator)
    w = [int(x * d) for x in v]
    g = 0
    for x in w:
        g = gcd(g, x)
    return [x // g for x in w] if g else w


def lll(B, delta=Fraction(3, 4)):
    B = [list(map(Fraction, b)) for b in B]
    n = len(B)
    def dot(u, v):
        return sum(a * b for a, b in zip(u, v))
    def gs(B):
        Bs, mu = [], [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            v = B[i][:]
            for j in range(i):
                mu[i][j] = dot(B[i], Bs[j]) / dot(Bs[j], Bs[j])
                v = [a - mu[i][j] * b for a, b in zip(v, Bs[j])]
            Bs.append(v)
        return Bs, mu
    Bs, mu = gs(B)
    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                B[k] = [a - q * b for a, b in zip(B[k], B[j])]
                Bs, mu = gs(B)
        if dot(Bs[k], Bs[k]) >= (delta - mu[k][k - 1] ** 2) * dot(Bs[k - 1], Bs[k - 1]):
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            Bs, mu = gs(B)
            k = max(k - 1, 1)
    return [[int(x) for x in b] for b in B]


def rank_frac(M):
    return len(M[0]) - len(nullspace_frac(M)) if M else 0


def main():
    d = json.load(open(sys.argv[1]))
    lab = [frozenset(x) for x in d["labels"]]
    pick = [int(t) for t in sys.argv[2].split(",")]
    for k in pick:
        s = d["structures"][k]
        EE = {frozenset((lab[i], lab[j])) for i, j in s["edges"]}
        G = [[1 if i != j and frozenset((S[i], S[j])) in EE else 0 for j in range(44)] for i in range(44)]
        T8 = [[24 * (i == j) - 8 * G[i][j] - K8[i][j] for j in range(44)] for i in range(44)]
        ker = nullspace_frac(T8)
        Ki = [to_int(v) for v in ker]
        print("object", k, "c =", s["c"], "gens", s["gens"], "nu =", len(ker))
        # intersections with coordinate subspaces
        def inter_dim(zero_idx):
            # vectors in ker vanishing on zero_idx: ker basis matrix restricted
            M = [[Ki[b][i] for b in range(len(Ki))] for i in zero_idx]
            return len(Ki) - rank_frac(M)
        print("  dim ker on X_l only (vanish on Y):", inter_dim(Y), "| vanish on X_l:", inter_dim(XL),
              "| vanish on Y':", inter_dim(YP), "| vanish on Q:", inter_dim(Q))
        R = lll(Ki)
        R.sort(key=lambda v: sum(x * x for x in v))
        for v in R:
            supp = [(sorted(S[i]), v[i]) for i in range(44) if v[i]]
            print("   norm %d supp %d :" % (sum(x * x for x in v), len(supp)),
                  " ".join("%d%d:%+d" % (a[0], a[1], c) for a, c in supp))


if __name__ == "__main__":
    main()
