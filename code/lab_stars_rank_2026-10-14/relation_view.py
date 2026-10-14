"""Exact kernel of T_S for saved three-star structures: basis of the relations beyond the stars (14/10/2026).
Prints the extra relation(s) as primitive integer vectors (normalised modulo the stars), their letter values
g_i = (t_i - w)/8, and checks c(l), PSD of T and U, and the star relations.
usage: python relation_view.py <found json> [index]"""
import json
import sys
from fractions import Fraction
from math import gcd

import numpy as np

from stars_rank import kval, LABELS


def nullspace(M):
    A = [[Fraction(x) for x in row] for row in M]
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
    free = [c for c in range(m) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * m
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -A[i][f]
        basis.append(v)
    return basis


def primitive(v):
    den = 1
    for x in v:
        den = den * x.denominator // gcd(den, x.denominator)
    w = [int(x * den) for x in v]
    g = 0
    for x in w:
        g = gcd(g, abs(x))
    return [x // g for x in w] if g else w


d = json.load(open(sys.argv[1]))
k = int(sys.argv[2]) if len(sys.argv) > 2 else 0
S = [frozenset(l) for l in d["labels"]]
n = len(S)
G = np.zeros((n, n), dtype=int)
for i, j in d["found"][k]["edges"]:
    G[i, j] = G[j, i] = 1
M8 = [[int(round(8 * ((3 if i == j else 0) - G[i][j] - kval(S[i], S[j])))) for j in range(n)] for i in range(n)]
B = nullspace(M8)
print("nullity", len(B))
stars = [0, 1, 2]
St = [[Fraction(1 if y in l else 0) for l in S] for y in stars]
# project out the stars: find a basis vector not in span(stars) and reduce it to have zeros on chosen star labels
A = np.array([[float(x) for x in v] for v in B])
Sm = np.array([[float(x) for x in v] for v in St])
for v in B:
    # least squares remove star components (exact): solve for coefficients making v - sum c_s star_s vanish on
    # three labels {0,4},{1,4},{2,4} (one per star, outside the other stars)
    pos = {l: i for i, l in enumerate(S)}
    ids = [pos[frozenset((0, 4))], pos[frozenset((1, 4))], pos[frozenset((2, 4))]]
    coef = [v[ids[0]], v[ids[1]], v[ids[2]]]
    w = [v[i] - sum(coef[s] * St[s][i] for s in range(3)) for i in range(n)]
    if all(x == 0 for x in w):
        continue
    p = primitive(w)
    print("extra relation (zero on 04, 14, 24), entries by label:")
    for i in range(n):
        if p[i]:
            print("   %s: %d" % (sorted(S[i]), p[i]))
    z = p
    dd = [sum(z[i] for i in range(n) if y in S[i]) for y in range(14)]
    wsum = sum(z)
    t = [3 * dd[y] + dd[y ^ 1] for y in range(14)]
    g = [Fraction(t[y] - wsum, 8) for y in range(14)]
    print("   weight w = %d, letter degrees d = %s" % (wsum, dd))
    print("   letter values g = (t - w)/8 = %s" % [str(x) for x in g])
    Gz = G @ np.array(z)
    print("   check (Gamma z)_ij = 3 z_ij - g_i - g_j:", all(
        Fraction(int(Gz[i])) == 3 * z[i] - sum(g[y] for y in S[i]) for i in range(n)))
    break

# nicest representative modulo integer star combinations: minimise the number of nonzero entries, then the L1 norm
best = None
Lst = [[1 if y in l else 0 for l in S] for y in stars]
for a in range(-8, 9):
    for b in range(-8, 9):
        for c in range(-8, 9):
            v = [z[i] + a * Lst[0][i] + b * Lst[1][i] + c * Lst[2][i] for i in range(n)]
            key = (sum(1 for x in v if x), sum(abs(x) for x in v))
            if best is None or key < best[0]:
                best = (key, v, (a, b, c))
print("nicest representative (support %d, L1 %d), added stars %s:" % (best[0][0], best[0][1], best[2]))
for name, cond in (("L0 only", lambda l: 0 in l and 2 not in l and 3 not in l),
                   ("L1 only", lambda l: 1 in l and 2 not in l and 3 not in l),
                   ("C4", lambda l: (0 in l or 1 in l) and (2 in l or 3 in l)),
                   ("B", lambda l: 2 in l and 0 not in l and 1 not in l)):
    print("   %-8s %s" % (name, {"".join(str(t) for t in sorted(S[i])): best[1][i] for i in range(n)
                                if cond(S[i]) and best[1][i]}))
