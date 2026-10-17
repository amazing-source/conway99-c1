"""3-adic obstruction from the resolvent identity.  If 3 is not an eigenvalue of Gamma_S (44-label graph of the
four-star block), Conway needs D = B (3I - Gamma_S)^{-1} B^T - (3I - M - J/3) = 0.  Every target entry has 3-adic
valuation -1 (the -1/3), so:
  (i)  Gamma_S nonsingular mod 3  =>  (3I - Gamma_S)^{-1} is 3-integral  =>  D != 0  =>  nu(T_S) <= 13: EXCLUDED;
  (ii) otherwise Conway needs D 3-integral (polar part of B R B^T at 3 equal to -J/3): tested exactly (fractions).
usage: python c1_3adic.py <cache.jsonl> <max sides>"""
import itertools, json, sys
from collections import Counter
from fractions import Fraction
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod, relabel, gl_connected

Bm = [[1 if r in l else 0 for l in S] for r in range(14)]

def solve_frac(X, Rhs):
    n = len(X); m = len(Rhs[0])
    A = [[Fraction(x) for x in X[i]] + [Fraction(y) for y in Rhs[i]] for i in range(n)]
    for c in range(n):
        pr = next((i for i in range(c, n) if A[i][c] != 0), None)
        if pr is None:
            return None
        A[c], A[pr] = A[pr], A[c]
        iv = 1 / A[c][c]
        A[c] = [x * iv for x in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [row[n:] for row in A]

def v3(q):
    if q == 0:
        return 99
    a, b, c = q.numerator, q.denominator, 0
    while a % 3 == 0:
        a //= 3; c += 1
    while b % 3 == 0:
        b //= 3; c -= 1
    return c

def side_info(EE):
    G = [[1 if i != j and frozenset((S[i], S[j])) in EE else 0 for j in range(44)] for i in range(44)]
    X = [[(3 if i == j else 0) - G[i][j] for j in range(44)] for i in range(44)]
    if rank_mod(X, 1000000007) < 44:
        return "3_in_spec", None, None
    r3 = rank_mod(G, 3)
    if r3 == 44:
        return "nonsing_mod3_EXCLUDED", 0, None
    Y = solve_frac(X, [[Bm[r][i] for r in range(14)] for i in range(44)])    # X Y = B^T
    BRB = [[sum(Bm[r][i] * Y[i][s] for i in range(44)) for s in range(14)] for r in range(14)]
    D = [[BRB[r][s] - (3 * (r == s) - (1 if s == (r ^ 1) else 0) - Fraction(1, 3)) for s in range(14)] for r in range(14)]
    minv = min(v3(D[r][s]) for r in range(14) for s in range(14))
    return ("D_3integral" if minv >= 0 else "D_not_3integral_EXCLUDED"), 44 - r3, minv

tab = Counter(); done = 0
for line in open(sys.argv[1]):
    d = json.loads(line)
    if len(d["labels"]) != 44:
        continue
    S0 = [frozenset(x) for x in d["labels"]]
    E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
    for side in (0, 1):
        L, EE = relabel(S0, E0, side)
        conn, degok = gl_connected(EE)
        if not (conn and degok):
            continue
        st, k, mv = side_info(EE)
        tab[(st, k, mv)] += 1
        done += 1
    if done >= int(sys.argv[2]):
        break
print("c(l)=1 sides:", done)
print("(status, dim ker(Gamma_S mod 3), min v3(D)) : count")
for key, c in sorted(tab.items(), key=str):
    print("   ", key, c)
