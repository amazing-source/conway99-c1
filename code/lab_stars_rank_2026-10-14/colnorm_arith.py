"""Arithmetic of the column norms of a rank-30 three-star object (14/10/2026).

For a three-star object S (34 labels, T_S PSD of rank 30) and an outside label u, the real graph needs
m^T H^-1 m = 20 exactly, where M = 8 T_S, H = a nonsingular 30 x 30 principal block of M (indices I) and
m = 8 T(S_I, u) = -8 Gamma(S_I, u) - 8 K(S_I, u) for the profile of u (its neighbours in the stars; Codex's filter).
Here: enumerate the local profiles of u = {3,4} (2 neighbours in L_0, 2 in L_1, 1 in L_2, caps C2 and partial counts
with the structure inside S), compute the exact rational norm, and report the 2-adic and 7-adic valuations of
norm - 20 and the denominators.
usage: python colnorm_arith.py <structure json> [index] [outside label, default 3,4]
"""
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction

import numpy as np

from stars_rank import kval, count_needed


def vp(x, p):
    if x == 0:
        return None
    x = Fraction(x)
    n, d, v = x.numerator, x.denominator, 0
    while n % p == 0:
        n //= p
        v += 1
    while d % p == 0:
        d //= p
        v -= 1
    return v


def solve_exact(H, m):
    n = len(H)
    A = [[Fraction(H[i][j]) for j in range(n)] + [Fraction(m[i])] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0)
        A[c], A[p] = A[p], A[c]
        piv = A[c][c]
        A[c] = [a / piv for a in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return [A[i][n] for i in range(n)]


def main():
    d = json.load(open(sys.argv[1]))
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    u = frozenset(int(t) for t in (sys.argv[3] if len(sys.argv) > 3 else "3,4").split(","))
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    if "structures" in d:
        edges = d["structures"][k]["edges"]
    elif "valid_edges" in d:
        edges = d["valid_edges"][k]
    else:
        edges = [x for x in d["found"] if not x["grid"]][0]["edges"]
    G = np.zeros((n, n), dtype=int)
    for i, j in edges:
        G[i, j] = G[j, i] = 1
    M = [[int(round(8 * ((3 if i == j else 0) - G[i][j] - kval(S[i], S[j])))) for j in range(n)] for i in range(n)]
    # pick 30 independent indices greedily (exact rank)
    I = []
    for i in range(n):
        cand = I + [i]
        sub = [[Fraction(M[a][b]) for b in cand] for a in cand]
        # exact determinant test via elimination
        A = [row[:] for row in sub]
        ok = True
        for c in range(len(cand)):
            p = next((r for r in range(c, len(cand)) if A[r][c] != 0), None)
            if p is None:
                ok = False
                break
            A[c], A[p] = A[p], A[c]
            for r in range(c + 1, len(cand)):
                f = A[r][c] / A[c][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
        if ok:
            I.append(i)
        if len(I) == 30:
            break
    H = [[M[a][b] for b in I] for a in I]
    stars = [0, 1, 2]
    groups = {y: [i for i in range(n) if y in S[i]] for y in stars}
    need = {y: count_needed(u, y) for y in stars}
    profiles = []
    for c0 in itertools.combinations(groups[0], need[0]):
        for c1 in itertools.combinations(groups[1], need[1]):
            for c2 in itertools.combinations(groups[2], need[2]):
                nb = set(c0) | set(c1) | set(c2)
                if len(nb) != len(c0) + len(c1) + len(c2) and False:
                    continue
                # exact counts per star must hold with overlaps ({0,2} is in L_0 and L_2, etc.)
                if any(sum(1 for i in nb if y in S[i]) != need[y] for y in stars):
                    continue
                # partial counts towards the other letters
                if any(sum(1 for i in nb if y in S[i]) > count_needed(u, y) for y in range(14) if y not in stars):
                    continue
                # caps: common neighbours of u and each i in S (inside S plus shared letters)
                bad = False
                for i in range(n):
                    common = sum(1 for j in nb if j != i and G[i][j]) + len(S[i] & u)
                    if common > (1 if i in nb else 2):
                        bad = True
                        break
                if bad:
                    continue
                profiles.append(tuple(sorted(nb)))
    profiles = sorted(set(profiles))
    stats2, stats7, dens = Counter(), Counter(), Counter()
    exact = 0
    for nb in profiles:
        m = [-8 * (1 if i in nb else 0) - int(round(8 * kval(S[i], u))) for i in I]
        x = solve_exact(H, m)
        norm = sum(Fraction(a) * b for a, b in zip(m, x))
        diff = norm - 20
        if diff == 0:
            exact += 1
        stats2[vp(diff, 2)] += 1
        stats7[vp(diff, 7)] += 1
        dens[norm.denominator] += 1
    print("structure %s[%d], outside label %s: %d local profiles, %d with norm exactly 20"
          % (sys.argv[1], k, sorted(u), len(profiles), exact))
    print("  2-adic valuation of (norm - 20):", dict(sorted(stats2.items(), key=lambda t: (t[0] is None, t[0] or 0))))
    print("  7-adic valuation of (norm - 20):", dict(sorted(stats7.items(), key=lambda t: (t[0] is None, t[0] or 0))))
    print("  most common denominators:", dens.most_common(6))


if __name__ == "__main__":
    main()
