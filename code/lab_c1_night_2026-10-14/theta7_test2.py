"""Controls of theta7_lp.py with b = 0 mod 4 (asked by the review of 14/10): lattices
    L  = Lambda_7^(2k+1) + A_6 + E_8^m         (4k + 8m = 36, det 7^(2k+2), b = 42 - 2k)
    L' = Lambda_7^(2k+1) + A_6 + (sqrt7 E_8)^m (det 7^(2k+2+8m), b = 42 - 2k - 8m)
with sqrt7 L* = Lambda_7^(2k+1) + sqrt7 A_6* + (sqrt7 E_8)^m, resp. Lambda_7^(2k+1) + sqrt7 A_6* + E_8^m.
theta_{A_6} and theta_{sqrt7 A_6*} are computed exactly by dynamic programming over the 7 coordinates
(A_6 = {x in Z^7 : sum x = 0}; sqrt7 A_6* = {y/sqrt7 : y in Z^7, all y_i = k mod 7, sum y = 0}, norm |y|^2/7).
Check: theta_L is in M_22(Gamma_0(7)) and theta_L | W_7 = -7^(b/2 - 11) theta_{sqrt7 L*}, coefficient by coefficient.
"""
from fractions import Fraction

import theta7_lp as T

N = T.N


def theta_A6():
    lim = 2 * (N - 1)                          # |x|^2 <= lim
    table = {(0, 0): 1}
    for _ in range(7):
        new = {}
        for (s, n2), c in table.items():
            for v in range(-11, 12):
                m2 = n2 + v * v
                if m2 <= lim:
                    key = (s + v, m2)
                    new[key] = new.get(key, 0) + c
        table = new
    th = [0] * N
    for (s, n2), c in table.items():
        if s == 0:
            assert n2 % 2 == 0
            th[n2 // 2] += c
    return th


def theta_sqrt7_A6dual():
    lim = 14 * (N - 1)                         # |y|^2 / 14 <= N - 1
    th = [0] * N
    for k in range(7):
        table = {(0, 0): 1}
        for _ in range(7):
            new = {}
            for (s, n2), c in table.items():
                for t in range(-5, 6):
                    y = k + 7 * t
                    m2 = n2 + y * y
                    if m2 <= lim:
                        key = (s + y, m2)
                        new[key] = new.get(key, 0) + c
            table = new
        for (s, n2), c in table.items():
            if s == 0:
                assert n2 % 14 == 0, (k, n2)
                th[n2 // 14] += c
    return th


def power(f, k):
    g = [1] + [0] * (N - 1)
    for _ in range(k):
        g = T.mul(g, f)
    return g


A6 = theta_A6()
A6d = theta_sqrt7_A6dual()
assert A6[:3] == [1, 42, 126 * 0 + A6[2]] and A6[1] == 42           # 42 roots
assert A6d[0] == 1 and all(A6d[n] == 0 for n in (1, 2)) and A6d[3] == 14   # sqrt7 A_6*: minimum 6, 14 minimal vectors
E4, E4_7 = T.E4, T.scale7(T.E4)
cases = []
for k, m in ((1, 4), (3, 3), (5, 2), (7, 1), (9, 0)):
    base = T.mul(power(T.th7, 2 * k + 1), A6)
    based = T.mul(power(T.th7, 2 * k + 1), A6d)
    cases.append(("Lambda7^%d+A6+E8^%d" % (2 * k + 1, m), 42 - 2 * k, T.mul(base, power(E4, m)), T.mul(based, power(E4_7, m))))
    if m:
        cases.append(("Lambda7^%d+A6+(sqrt7 E8)^%d" % (2 * k + 1, m), 42 - 2 * k - 8 * m,
                      T.mul(base, power(E4_7, m)), T.mul(based, power(E4, m))))
for name, b, thA, thB in cases:
    x = T.solve_coords(T.bvecs, thA)
    w = T.series(T.apply_W(x))
    s = Fraction(7) ** (b // 2 - 11) if b >= 22 else Fraction(1, 7 ** (11 - b // 2))
    ok = all(w[n] == -s * thB[n] for n in range(N))
    print("%-30s b=%2d (b mod 4 = %d)  Fricke relation exact: %s" % (name, b, b % 4, "OK" if ok else "FAIL"), flush=True)
