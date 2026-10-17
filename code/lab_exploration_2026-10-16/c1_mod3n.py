"""3-adic route, exact facts per structure:
  k3   = dim ker_F3(Gamma_S)   (universal part: z0 - z1, z2 - z3)
  s3   = 3 in spec(Gamma_S) over Q ?
  v3   = 3-adic valuation of det(3I - Gamma_S)  (Bareiss, exact) when nonzero
  nB1  = exists n in F_3^S with Gamma_S n = 0 and B n = 1 (all 14 letter sums 1)   [needed by Conway when s3 is False
         and all elementary divisors of 3I - Gamma_S are 1 or 3, i.e. v3 == k3]
  polar = D 3-integral ?  (exact Fractions; Conway needs yes)
usage: python c1_mod3n.py cache file max | walks f1 ... | rank30 file max"""
import itertools, json, sys
from fractions import Fraction
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, rank_mod, relabel, gl_connected

Bm = [[1 if r in l else 0 for l in S] for r in range(14)]


def rank3(M):
    return rank_mod(M, 3)


def solvable_mod3(Arows, b):
    """is A x = b solvable over F_3"""
    aug = [list(r) + [bb] for r, bb in zip(Arows, b)]
    return rank_mod([r[:-1] for r in aug], 3) == rank_mod(aug, 3)


def bareiss_det(M):
    A = [list(map(int, r)) for r in M]
    n = len(A); sign, prev = 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if sw is None:
                return 0
            A[k], A[sw] = A[sw], A[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def v3int(x):
    if x == 0:
        return 99
    c = 0
    while x % 3 == 0:
        x //= 3; c += 1
    return c


def solve_frac(X, Rhs):
    n = len(X)
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


def v3f(q):
    if q == 0:
        return 99
    a, b, c = q.numerator, q.denominator, 0
    while a % 3 == 0:
        a //= 3; c += 1
    while b % 3 == 0:
        b //= 3; c -= 1
    return c


def info(EE, do_polar=True):
    G = [[1 if i != j and frozenset((S[i], S[j])) in EE else 0 for j in range(44)] for i in range(44)]
    k3 = 44 - rank3(G)
    X = [[(3 if i == j else 0) - G[i][j] for j in range(44)] for i in range(44)]
    det = bareiss_det(X)
    s3 = det == 0
    v3 = v3int(det) if not s3 else None
    # n with Gamma n = 0, B n = 1 over F_3
    rows = [list(r) for r in G] + [list(r) for r in Bm]
    rhs = [0] * 44 + [1] * 14
    nB1 = solvable_mod3(rows, rhs)
    polar = None
    if do_polar and not s3:
        Y = solve_frac(X, [[Bm[r][i] for r in range(14)] for i in range(44)])
        BRB = [[sum(Bm[r][i] * Y[i][s] for i in range(44)) for s in range(14)] for r in range(14)]
        D = [[BRB[r][s] - (3 * (r == s) - (1 if s == (r ^ 1) else 0) - Fraction(1, 3)) for s in range(14)] for r in range(14)]
        polar = min(v3f(D[r][s]) for r in range(14) for s in range(14)) >= 0
    return k3, s3, v3, nB1, polar


def main():
    tab = Counter()
    which = sys.argv[1]
    if which == "cache":
        mx = int(sys.argv[3]); done = 0
        for line in open(sys.argv[2]):
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
                tab[info(EE)] += 1; done += 1
            if done >= mx:
                break
    elif which == "walks":
        for f in sys.argv[2:]:
            d = json.load(open(f))
            lab = [frozenset(x) for x in d["labels"]]
            EE = {frozenset((lab[i], lab[j])) for i, j in d["edges"]}
            r = info(EE)
            print(f.split("/")[-1].split("\\")[-1], r)
            tab[r] += 1
    else:
        d = json.load(open(sys.argv[2]))
        lab = [frozenset(x) for x in d["labels"]]
        for s in d["structures"][: int(sys.argv[3])]:
            EE = {frozenset((lab[i], lab[j])) for i, j in s["edges"]}
            tab[info(EE, do_polar=False)] += 1
    print("(k3 = dim ker_F3 Gamma_S, 3 in spec, v3(det(3I-Gamma_S)), exists n: Gamma n=0 & Bn=1 mod 3, D 3-integral) : count")
    for k, v in sorted(tab.items(), key=str):
        print("   ", k, v)


if __name__ == "__main__":
    main()
