"""Controls for theta7_lp.py on real lattices of rank 44 and level 7.

A_k = Lambda_7^(2k) + E_8^m (4k + 8m = 44, det 7^(2k), so b = 44 - 2k) and A'_k = Lambda_7^(2k) + (sqrt7 E_8)^m
(det 7^(2k + 8m), b = 44 - 2k - 8m). For each: (1) theta_A |W = -7^(b/2 - 11) theta_B with B = sqrt7 A* computed
directly from the factors; (2) the exact coefficient vector of theta_A satisfies every inequality of the linear
programme except c_1..c_6 = 0, and the floating-point solver accepts it (a real lattice must be feasible).
usage: python theta7_test.py
"""
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog

import theta7_lp as T

N = T.N
th7 = T.th7
E4 = T.E4
E4_7 = T.scale7(E4)


def power(f, k):
    g = [1] + [0] * (N - 1)
    for _ in range(k):
        g = T.mul(g, f)
    return g


cases = []
for k in (1, 3, 5, 7, 9, 11):
    m = (44 - 4 * k) // 8
    cases.append(("Lambda7^%d+E8^%d" % (2 * k, m), 44 - 2 * k,
                  T.mul(power(th7, 2 * k), power(E4, m)), T.mul(power(th7, 2 * k), power(E4_7, m))))
    if m > 0:
        b2 = 44 - 2 * k - 8 * m
        cases.append(("Lambda7^%d+(sqrt7 E8)^%d" % (2 * k, m), b2,
                      T.mul(power(th7, 2 * k), power(E4_7, m)), T.mul(power(th7, 2 * k), power(E4, m))))
for name, b, thA, thB in cases:
    x = T.solve_coords(T.bvecs, thA)
    w = T.series(T.apply_W(x))
    s = Fraction(7) ** (b // 2 - 11) if b >= 22 else Fraction(1, 7 ** (11 - b // 2))
    ok1 = all(w[n] == -s * thB[n] for n in range(N))
    a = [Fraction(v) for v in thA[:15]]
    sB = -Fraction(7) ** (11 - b // 2) if b <= 22 else -Fraction(1, 7 ** (b // 2 - 11))
    cB = [sB * sum(T.MW_ALL[n][k2] * a[k2] for k2 in range(15)) for n in range(N)]
    ok2 = all(cB[n] == thB[n] for n in range(N))
    # floating LP: fix a = thA[:15] through equalities, keep the inequalities a_n >= 0, c_n >= 0
    rows, rhs = [], []
    for n in range(1, N):
        rows.append([-v for v in T.MA_ALL[n]]); rhs.append(0)
        rows.append([-sB * v for v in T.MW_ALL[n]]); rhs.append(0)
    eq_rows = [[Fraction(int(i == j)) for j in range(15)] for i in range(15)]
    res = T.solve_scaled(eq_rows, a, rows, rhs)
    print("%-26s b=%2d  Fricke %s  B-series %s  LP accepts real point: %s" %
          (name, b, "OK" if ok1 else "FAIL", "OK" if ok2 else "FAIL", res.status == 0), flush=True)

# exact check: each control lattice must be feasible for the exact programme with minB = 1 (no vanishing imposed)
for name, b, thA, thB in cases:
    f, a = T.lp_exact(b, lines=False, roots=True, nmax=45, minB=1)
    print("%-26s b=%2d  exact LP (positivity, c_7m >= a_m) feasible: %s" % (name, b, f), flush=True)
