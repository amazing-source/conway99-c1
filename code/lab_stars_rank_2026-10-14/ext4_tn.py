"""(ext4_tn.py, 15/10/2026: copy of ext4.py that also prints the exact values p^T T_S^+ p of the (Tr) survivors.)
Extension test for a four-star structure of full rank, EXACT (15/10/2026).

Setting (stars 0,1 = line l, stars 2,3 = line m; mate of x = x xor 1).  In a Conway graph, T (84 x 84) is PSD of
rank 30 and U = 7 Pi - T is PSD of rank 40 (P1, P10).  If T_S (S = the 44 four-star labels) has rank 30, the 44 label
vectors span the whole 30-dimensional space, so for every outer label u (both letters outside l and m) with
neighbour set nb = N(u) n S, two exact conditions are forced:
  (Tr) p = T(S,u) is orthogonal to ker T_S   (a null vector of a principal block of a PSD matrix is a null vector of
       the whole matrix);
  (Tn) p^T T_S^+ p = T(u,u) = 5/2            (u lies in the span of the 44 vectors);
with T(i,u) = -[i in nb] - K(i,u).  Likewise for U if rank U_S = 40: (Ur) q = U(S,u) orthogonal to ker U_S and
(Un) q^T U_S^+ q = U(u,u).
Admissible profiles are enumerated from scratch: exactly two neighbours in each of the four stars, at most
need(u,z) labels of L_z in nb for every other letter z, and the caps (common neighbours inside S plus shared letters
<= 1 if adjacent, <= 2 if not).  (Tr) is tested in exact integer arithmetic (integer kernel basis); (Tn), (Ur), (Un)
are computed with Fractions on the (Tr)-survivors.  Output: per outer label, the counts; a label with no profile
passing all conditions certifies that the structure is not contained in any Conway graph.
usage: python ext4.py <json with labels, edges> [outer label x,y | all]
"""
import itertools
import json
import math
import sys
from fractions import Fraction as Fr

import numpy as np

MATE = lambda x: x ^ 1
STARS = (0, 1, 2, 3)


def kval(a, b):
    inter = len(a & b)
    m = sum(1 for x in a for y in b if y == MATE(x))
    return Fr(-1, 4) + Fr(3, 8) * inter + Fr(1, 8) * m


def need(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


def rref_kernel(M):
    A = [row[:] for row in M]
    n, m = len(A), len(A[0])
    piv, r = [], 0
    for c in range(m):
        p = next((i for i in range(r, n) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(n):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    ker = []
    for f in [c for c in range(m) if c not in piv]:
        v = [Fr(0)] * m
        v[f] = Fr(1)
        for i, c in enumerate(piv):
            v[c] = -A[i][f]
        ker.append(v)
    return r, ker


def inv14():
    DDt = [[Fr(12 if x == y else (0 if y == MATE(x) else 1)) for y in range(14)] for x in range(14)]
    A = [row[:] + [Fr(1 if i == j else 0) for j in range(14)] for i, row in enumerate(DDt)]
    for c in range(14):
        p = next(i for i in range(c, 14) if A[i][c] != 0)
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for i in range(14):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [row[14:] for row in A]


INV = inv14()


def Pi(a, b):
    return (1 if a == b else 0) - sum(INV[x][y] for x in a for y in b)


def exact_norm(M, ker, p):
    """p^T M^+ p for p orthogonal to ker M: solve M x = p with x orthogonal to ker M."""
    n = len(M)
    A = [[M[i][j] for j in range(n)] + [p[i]] for i in range(n)] + [list(k) + [Fr(0)] for k in ker]
    rows, r, piv = len(A), 0, []
    for c in range(n):
        q = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if q is None:
            continue
        A[r], A[q] = A[q], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    assert all(all(x == 0 for x in A[i]) for i in range(r, rows)), "p is not in the range"
    x = [Fr(0)] * n
    for i, c in enumerate(piv):
        x[c] = A[i][n]
    return sum(a * b for a, b in zip(p, x))


def int_rows(ker):
    out = []
    for k in ker:
        L = 1
        for x in k:
            L = L * x.denominator // math.gcd(L, x.denominator)
        row = [int(x * L) for x in k]
        g = 0
        for x in row:
            g = math.gcd(g, abs(x))
        out.append([x // g for x in row])
    return np.array(out, dtype=np.int64)


def main():
    d = json.load(open(sys.argv[1]))
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    assert set(S) == {frozenset((a, x)) for a in STARS for x in range(14) if x not in (a, MATE(a))}
    Gl = [[0] * n for _ in range(n)]
    for i, j in d["edges"]:
        Gl[i][j] = Gl[j][i] = 1
    G = np.array(Gl, dtype=np.int64)
    T = [[(3 if i == j else 0) - Gl[i][j] - kval(S[i], S[j]) for j in range(n)] for i in range(n)]
    U = [[7 * Pi(S[i], S[j]) - T[i][j] for j in range(n)] for i in range(n)]
    rT, kT = rref_kernel(T)
    rU, kU = rref_kernel(U)
    print("rank T_S = %d, rank U_S = %d" % (rT, rU))
    if rT != 30:
        print("rank T_S < 30: outer vectors are not determined by the profile; stop")
        return
    KTi = int_rows(kT)  # integer kernel basis of T_S
    outer = [frozenset(c) for c in itertools.combinations(range(4, 14), 2) if MATE(c[0]) != c[1]]
    if which != "all":
        outer = [frozenset(int(t) for t in which.split(","))]
    star = {s: [i for i in range(n) if s in S[i]] for s in STARS}
    Lmat = np.array([[1 if z in S[i] else 0 for z in range(14)] for i in range(n)], dtype=np.int64)  # n x 14
    rest2 = [i for i in range(n) if 2 in S[i] and not (S[i] & {0, 1})]
    rest3 = [i for i in range(n) if 3 in S[i] and not (S[i] & {0, 1})]
    summary = {}
    for u in outer:
        K8 = np.array([int(8 * kval(S[i], u)) for i in range(n)], dtype=np.int64)
        shared = np.array([len(S[i] & u) for i in range(n)], dtype=np.int64)
        needv = np.array([need(u, z) for z in range(14)], dtype=np.int64)
        rows = []
        for A0 in itertools.combinations(star[0], 2):
            for A1 in itertools.combinations(star[1], 2):
                base = np.zeros(n, dtype=np.int64)
                base[list(A0)] = 1
                base[list(A1)] = 1
                c2 = int(sum(base[i] for i in star[2]))
                c3 = int(sum(base[i] for i in star[3]))
                if c2 > 2 or c3 > 2:
                    continue
                B2 = list(itertools.combinations(rest2, 2 - c2))
                B3 = list(itertools.combinations(rest3, 2 - c3))
                X = np.repeat(base[None, :], len(B2) * len(B3), axis=0)
                r = 0
                for b2 in B2:
                    for b3 in B3:
                        X[r, list(b2)] = 1
                        X[r, list(b3)] = 1
                        r += 1
                # letter counts towards the other letters
                cnt = X @ Lmat
                ok = np.all(cnt[:, 4:] <= needv[None, 4:], axis=1)
                assert np.all(cnt[:, 0:4] == 2)
                X = X[ok]
                if len(X) == 0:
                    continue
                common = X @ G + shared[None, :]
                ok = np.all(common <= 2 - X, axis=1)
                X = X[ok]
                if len(X):
                    rows.append(X)
        X = np.concatenate(rows) if rows else np.zeros((0, n), dtype=np.int64)
        # exact (Tr): KTi @ (8 p) = -KTi @ (8 X + K8) = 0
        R = (8 * X + K8[None, :]) @ KTi.T
        tr = np.all(R == 0, axis=1)
        Xr = X[tr]
        nTn = nU = 0
        vals = []
        for x in Xr:
            p = [-int(x[i]) - kval(S[i], u) for i in range(n)]
            nv = exact_norm(T, kT, p)
            vals.append(nv)
            if nv != 3 - kval(u, u):
                continue
            nTn += 1
            q = [7 * Pi(S[i], u) - p[i] for i in range(n)]
            if not all(sum(a * b for a, b in zip(k, q)) == 0 for k in kU):
                continue
            if rU == 40 and exact_norm(U, kU, q) != 7 * Pi(u, u) - (3 - kval(u, u)):
                continue
            nU += 1
        summary["%d,%d" % tuple(sorted(u))] = [int(len(X)), int(tr.sum()), nTn, nU]
        print("outer label %s: %d admissible profiles; (Tr) exact %d; (Tr)+(Tn) exact %d; all four exact %d"
              % (sorted(u), len(X), int(tr.sum()), nTn, nU), flush=True)
        if vals:
            print("   p^T T^+ p - 5/2 on the (Tr) survivors:", sorted(set(str(v - Fr(5, 2)) for v in vals)), flush=True)
    dead = [k for k, v in summary.items() if v[3] == 0]
    print("outer labels with NO admissible placement: %d of %d %s" % (len(dead), len(summary), dead))
    json.dump({"structure": sys.argv[1], "rank_T": rT, "rank_U": rU,
               "per_label [profiles, Tr, Tr+Tn, all]": summary},
              open(sys.argv[1].replace(".json", "_ext4tn.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
