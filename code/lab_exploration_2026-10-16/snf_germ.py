"""Elementary divisors of 8T on a four-star block (exploration, LAB 16/10/2026).
8T_SS = 24I - 8Gamma - 3B^tB - B^tMB + 2J restricted to the 44 labels.  For a generating set of the block lattice the
product of the nonzero invariant factors equals disc(Lambda_S).  Prints rank, and for p = 2, 3, 5, 7 the p-adic
valuations of the nonzero invariant factors (sorted), and the class (primes with odd total valuation).
usage: python snf_germ.py <block json (labels, edges)> [...]"""
import itertools
import json
import sys


def smith_diag(A):
    # elementary divisors of an integer matrix (pure Python, exact)
    A = [row[:] for row in A]
    m, n = len(A), len(A[0])
    diag = []
    r = 0
    for c in range(n):
        if r >= m:
            break
        while True:
            piv = None
            for i in range(r, m):
                for j in range(c, n):
                    if A[i][j] and (piv is None or abs(A[i][j]) < abs(A[piv[0]][piv[1]])):
                        piv = (i, j)
            if piv is None:
                return diag
            i, j = piv
            A[r], A[i] = A[i], A[r]
            for row in A:
                row[c], row[j] = row[j], row[c]
            p = A[r][c]
            done = True
            for i in range(r + 1, m):
                q = A[i][c] // p
                if q:
                    A[i] = [a - q * b for a, b in zip(A[i], A[r])]
                if A[i][c]:
                    done = False
            for j in range(c + 1, n):
                q = A[r][j] // p
                if q:
                    for row in A:
                        row[j] -= q * row[c]
                if A[r][j]:
                    done = False
            if done:
                bad = None
                for i in range(r + 1, m):
                    for j in range(c + 1, n):
                        if A[i][j] % p:
                            bad = i
                            break
                    if bad is not None:
                        break
                if bad is None:
                    diag.append(abs(p))
                    r += 1
                    break
                A[r] = [a + b for a, b in zip(A[r], A[bad])]
    return diag

MATE = lambda i: i ^ 1


def vp(n, p):
    n, k = abs(int(n)), 0
    while n and n % p == 0:
        n //= p
        k += 1
    return k


for path in sys.argv[1:]:
    d = json.load(open(path))
    L = [frozenset(x) for x in d["labels"]]
    idx = [i for i, l in enumerate(L) if l & {0, 1, 2, 3}]
    S = [L[i] for i in idx]
    pos = {i: k for k, i in enumerate(idx)}
    n = len(S)
    G = [[0] * n for _ in range(n)]
    for i, j in d["edges"]:
        if i in pos and j in pos:
            G[pos[i]][pos[j]] = G[pos[j]][pos[i]] = 1
    M = [[0] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            x, y = S[a], S[b]
            s = len(x & y)
            m = sum(1 for p in x for q in y if q == MATE(p))
            M[a][b] = (24 if a == b else 0) - 8 * G[a][b] - 3 * s - m + 2
    diag = smith_diag(M)
    out = {"rank": len(diag)}
    cls = []
    for p in (2, 3, 5, 7):
        v = sorted(vp(t, p) for t in diag)
        nz = [x for x in v if x]
        out[p] = nz
        if sum(nz) % 2:
            cls.append(p)
    print("%s: rank %d; v2 %s; v3 %s; v5 %s; v7 %s; class %s" % (path.replace("\\", "/").split("/")[-1], out["rank"],
          out[2][-6:], out[3], out[5], out[7], "*".join(map(str, cls)) or "1"), flush=True)
