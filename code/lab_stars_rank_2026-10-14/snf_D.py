"""Elementary divisors of the letter-label incidence D (14 x 84) and det of K = ker D n Z^84."""
import math
from fractions import Fraction as Fr

L = [(x, y) for x in range(14) for y in range(x + 1, 14) if y != x ^ 1]
D = [[1 if i in L[j] else 0 for j in range(len(L))] for i in range(14)]


def snf_diag(M):
    A = [r[:] for r in M]
    m, n = len(A), len(A[0])
    diag = []
    t = 0
    while t < min(m, n):
        # find a non-zero entry of minimal absolute value in the remaining block
        best = None
        for i in range(t, m):
            for j in range(t, n):
                if A[i][j] != 0 and (best is None or abs(A[i][j]) < abs(A[best[0]][best[1]])):
                    best = (i, j)
        if best is None:
            break
        i, j = best
        A[t], A[i] = A[i], A[t]
        for r in A:
            r[t], r[j] = r[j], r[t]
        while True:
            done = True
            for i in range(t + 1, m):
                q = A[i][t] // A[t][t]
                if q:
                    A[i] = [a - q * b for a, b in zip(A[i], A[t])]
                if A[i][t] != 0:
                    done = False
            for j in range(t + 1, n):
                q = A[t][j] // A[t][t]
                if q:
                    for r in A:
                        r[j] -= q * r[t]
                if A[t][j] != 0:
                    done = False
            if done:
                # divisibility condition
                bad = None
                for i in range(t + 1, m):
                    for j in range(t + 1, n):
                        if A[i][j] % A[t][t]:
                            bad = i
                            break
                    if bad is not None:
                        break
                if bad is None:
                    break
                A[t] = [a + b for a, b in zip(A[t], A[bad])]
                continue
            # move the smallest non-zero entry of row/column t to the pivot
            best = (t, t)
            for i in range(t, m):
                if A[i][t] != 0 and abs(A[i][t]) < abs(A[best[0]][best[1]]):
                    best = (i, t)
            for j in range(t, n):
                if A[t][j] != 0 and abs(A[t][j]) < abs(A[best[0]][best[1]]):
                    best = (t, j)
            i, j = best
            A[t], A[i] = A[i], A[t]
            for r in A:
                r[t], r[j] = r[j], r[t]
        diag.append(abs(A[t][t]))
        t += 1
    return diag


def det_frac(M):
    A = [[Fr(x) for x in r] for r in M]
    n = len(A)
    d = Fr(1)
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0)
        if p != c:
            A[c], A[p] = A[p], A[c]
            d = -d
        d *= A[c][c]
        for i in range(c + 1, n):
            f = A[i][c] / A[c][c]
            A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return d


def fac(n):
    out, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


d = snf_diag(D)
print("labels", len(L), "elementary divisors of D:", d)
G = [[sum(D[i][k] * D[j][k] for k in range(len(L))) for j in range(14)] for i in range(14)]
dg = det_frac(G)
print("det D D^T =", dg, fac(int(dg)))
idx = math.prod(d)
print("det K = det(D D^T) / idx^2 =", fac(int(dg) // idx ** 2))
