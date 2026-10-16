"""Universal mod-p kernel vectors of 8T on a four-star block (exploration, LAB 16/10/2026).
15U = 60I + 15Gamma - 4B^tB + B^tMB - 2J is independent of Gamma modulo 3 and 5, and 8T.15U = 0 in a Conway graph.
So every column of (15U mod p) lies in ker(8T mod p).  Z_p(S) = vectors of col(15U mod p) supported on the block S.
For each germ: is each Z_p vector the reduction of an integral kernel vector of T_SS (i.e. in N_S mod p)?
The number of Z_p directions NOT reached by N_S mod p bounds from below the p-part of disc(Lambda_S).
usage: python zp_vectors.py <germ json> [...]"""
import itertools
import json
import sys

import numpy as np

MATE = lambda i: i ^ 1
LAB = [frozenset((u, w)) for u, w in itertools.combinations(range(14), 2) if w != MATE(u)]
INS = [l for l in LAB if l & {0, 1, 2, 3}]
OUT = [l for l in LAB if not (l & {0, 1, 2, 3})]


def rank_mod(M, p):
    A = [[int(x) % p for x in row] for row in M]
    r = 0
    rows, cols = len(A), len(A[0]) if A else 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
    return r


def nullspace_mod(M, p):
    """basis of {g : M g = 0 mod p}"""
    A = [[int(x) % p for x in row] for row in M]
    rows, cols = len(A), len(A[0])
    pivcols = []
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        pivcols.append(c)
        r += 1
    free = [c for c in range(cols) if c not in pivcols]
    basis = []
    for f in free:
        g = [0] * cols
        g[f] = 1
        for i, c in enumerate(pivcols):
            g[c] = (-A[i][f]) % p
        basis.append(g)
    return basis


def kval(a, b):
    s = len(a & b)
    m = sum(1 for p in a for q in b if q == MATE(p))
    return s, m


# 15U mod p on all 84 labels, independent of Gamma (p = 3, 5): 60I + 15Gamma vanish mod 3 and mod 5
def U15_mod(p):
    M = [[0] * 84 for _ in range(84)]
    for i, a in enumerate(LAB):
        for j, b in enumerate(LAB):
            s, m = kval(a, b)
            M[i][j] = (-4 * s + m - 2) % p
    return M


order = INS + OUT
pos = {l: k for k, l in enumerate(LAB)}
for p in (3, 5):
    U = U15_mod(p)
    # column space restricted: vectors in col(U) vanishing on OUT  <=>  U c with (U c)_OUT = 0
    UO = [[U[pos[o]][j] for j in range(84)] for o in OUT]
    cs = nullspace_mod(UO, p)                     # coefficient vectors c with (U c) zero on OUT
    vecs = []
    for c in cs:
        g = [sum(U[pos[y]][j] * c[j] for j in range(84)) % p for y in INS]
        if any(g):
            vecs.append(g)
    # reduce to a basis
    basis = []
    for g in vecs:
        if rank_mod(basis + [g], p) > len(basis):
            basis.append(g)
    print("p = %d: rank of 15U mod p on 84 labels = %d; dim Z_p(S) = %d" % (p, rank_mod(U, p), len(basis)))
    for g in basis:
        supp = {}
        for y, val in zip(INS, g):
            if val:
                supp.setdefault(val, []).append("".join(str(t) for t in sorted(y)))
        print("   vector: " + "; ".join("%d on %s" % (val, ",".join(v)) for val, v in sorted(supp.items())))
    globals()["Z%d" % p] = basis

for path in sys.argv[1:]:
    d = json.load(open(path))
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((L[i], L[j])) for i, j in d["edges"])
    n = len(INS)
    T8 = np.zeros((n, n), dtype=np.int64)
    for a in range(n):
        for b in range(n):
            s, m = kval(INS[a], INS[b])
            T8[a, b] = (24 if a == b else 0) - 8 * (frozenset((INS[a], INS[b])) in E) - 3 * s - m + 2
    for p in (3, 5):
        Z = globals()["Z%d" % p]
        ok = all(all(int(x) % p == 0 for x in T8.dot(np.array(g))) for g in Z)
        # integral kernel of T8 (rational kernel scaled to integers) and its reduction mod p
        import sympy
        ker = sympy.Matrix(T8.tolist()).nullspace()
        Kint = []
        for v in ker:
            den = sympy.ilcm(*[sympy.fraction(x)[1] for x in v])
            w = [int(x * den) for x in v]
            g0 = 0
            for x in w:
                g0 = sympy.igcd(g0, x)
            Kint.append([x // g0 for x in w])
        # saturate: the lattice N_S = Z^n cap ker; reduction mod p = row space mod p of a saturated basis.  Approximate
        # by the reduction of the rational basis plus the test whether Z_p lies in it (exact up to saturation issues,
        # which can only enlarge N_S mod p; reported as 'lower bound on missing directions').
        rk = rank_mod(Kint, p)
        rk2 = rank_mod(Kint + Z, p)
        print("%s p=%d: Z_p in ker(8T mod p): %s; rank(N mod p) %d, adding Z_p -> %d (missing directions <= %d)"
              % (path.replace("\\", "/").split("/")[-1], p, ok, rk, rk2, rk2 - rk), flush=True)
