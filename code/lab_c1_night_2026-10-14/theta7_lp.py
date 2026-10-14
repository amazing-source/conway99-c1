"""Theta series of the line lattice A and of B = sqrt(7) A*, linear feasibility per value of the 7-rank b.

Lattices (NOTE_NIGHT section 19): A = sqrt7 E {z in Z^99 : sum z = 0 mod 3} contains the 231 line vectors q_l
(norm 4), is even of rank 44 and 7-elementary with det A = 7^(44-b); B = sqrt7 A* = K_- + Z f_l is even with
det 7^b and minimum >= 14 (integral -4-eigenvectors have norm >= 14; the cosets of f_l have norm >= 22).
theta_A and theta_B lie in M_22(Gamma_0(7)) (trivial character, b even), and
    theta_A |_22 W_7 = - 7^(b/2 - 11) theta_B.
Constraints used: a_0 = 1, a_n >= 0; c_0 = 1, c_1 = ... = c_6 = 0, c_n >= 0 (q-expansion theta = sum a_n q^n with
a_n = number of vectors of norm 2n); optionally a_2 >= 462 (the lines) and a_1 <= c_7 (a root r of A gives the
vector sqrt7 r of norm 14 in B).

Basis of M_22(Gamma_0(7)): monomials in E2_7 = (7 E_2(7t) - E_2(t))/6 (W-eigenvalue -1), E_4, E_4(7t), E_6,
E_6(7t), Delta, Delta(7t), g6 = (eta(t) eta(7t))^6 (W-eigenvalue -1); F(t)|W_7 = 7^(k/2) F(7t) for level one F.
Self-test: the lattice Lambda_7^22 (Lambda_7 = [[2,1],[1,4]], 7-modular), b = 22, must satisfy theta|W = -theta.

usage: python theta7_lp.py [ncoef]      pure Python + scipy (HiGHS), exact rational linear algebra, a few seconds.
"""
import itertools
import sys
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog

import os
N = int(sys.argv[1]) if (__name__ == "__main__" and len(sys.argv) > 1) else int(os.environ.get("THETA7_N", "60"))


def sigma(k, n):
    return sum(d ** k for d in range(1, n + 1) if n % d == 0)


def mul(f, g):
    h = [0] * N
    for i, a in enumerate(f):
        if a:
            for j in range(N - i):
                h[i + j] += a * g[j]
    return h


def scale7(f):
    h = [0] * N
    for i in range(0, N, 7):
        h[i] = f[i // 7]
    return h


E2 = [1] + [-24 * sigma(1, n) for n in range(1, N)]
E4 = [1] + [240 * sigma(3, n) for n in range(1, N)]
E6 = [1] + [-504 * sigma(5, n) for n in range(1, N)]
E43 = mul(mul(E4, E4), E4)
E62 = mul(E6, E6)
DEL = [(a - b) // 1728 for a, b in zip(E43, E62)]
assert all((a - b) % 1728 == 0 for a, b in zip(E43, E62)) and DEL[:3] == [0, 1, -24]
E2_7 = [(7 * a - b) // 6 for a, b in zip(scale7(E2), E2)]
assert E2_7[:3] == [1, 4, 12]
# eta(t)^6 eta(7t)^6 = q^2 prod (1 - q^n)^6 (1 - q^(7n))^6
P = [1] + [0] * (N - 1)
for n in range(1, N):
    for _ in range(6):
        fac = [0] * N
        fac[0] = 1
        fac[n] = -1
        P = mul(P, fac)
    if 7 * n < N:
        for _ in range(6):
            fac = [0] * N
            fac[0] = 1
            fac[7 * n] = -1
            P = mul(P, fac)
G6 = [0, 0] + P[:N - 2]

# generators: name, expansion, weight, (W-image index, W-factor exponent of 7 or sign)
GENS = [("E2_7", E2_7, 2), ("E4", E4, 4), ("E4_7", scale7(E4), 4), ("E6", E6, 6), ("E6_7", scale7(E6), 6),
        ("D", DEL, 12), ("D_7", scale7(DEL), 12), ("g6", G6, 6)]
# W-action on generators: image generator index and scalar
WIMG = {0: (0, Fraction(-1)), 1: (2, Fraction(7) ** 2), 2: (1, Fraction(1, 49)), 3: (4, Fraction(7) ** 3),
        4: (3, Fraction(1, 343)), 5: (6, Fraction(7) ** 6), 6: (5, Fraction(1, 7 ** 6)), 7: (7, Fraction(-1))}


def monomials(weight):
    res = []
    ws = [g[2] for g in GENS]
    def rec(i, left, cur):
        if i == len(GENS):
            if left == 0:
                res.append(tuple(cur))
            return
        for e in range(left // ws[i] + 1):
            rec(i + 1, left - e * ws[i], cur + [e])
    rec(0, weight, [])
    return res


EXP = {}


def expansion(mono):
    if mono not in EXP:
        f = [1] + [0] * (N - 1)
        for i, e in enumerate(mono):
            for _ in range(e):
                f = mul(f, GENS[i][1])
        EXP[mono] = f
    return EXP[mono]


def wimage(mono):
    new = [0] * len(GENS)
    c = Fraction(1)
    for i, e in enumerate(mono):
        j, s = WIMG[i]
        new[j] += e
        c *= s ** e
    return tuple(new), c


def rank_basis(vectors):
    """Greedy exact selection of independent vectors (list of lists of ints); returns indices."""
    rows = []
    chosen = []
    for idx, v in enumerate(vectors):
        w = [Fraction(x) for x in v]
        for piv, r in rows:
            if w[piv] != 0:
                f = w[piv] / r[piv]
                w = [a - f * b for a, b in zip(w, r)]
        piv = next((i for i, a in enumerate(w) if a != 0), None)
        if piv is not None:
            rows.append((piv, w))
            chosen.append(idx)
    return chosen


def solve_coords(basis_vecs, target):
    """Exact coordinates of target in the span of basis_vecs (all length N); raises if not in the span."""
    m = len(basis_vecs)
    A = [[Fraction(basis_vecs[j][i]) for j in range(m)] + [Fraction(target[i])] for i in range(N)]
    r = 0
    piv_cols = []
    for c in range(m):
        p = next((i for i in range(r, N) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(N):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv_cols.append(c)
        r += 1
    for i in range(r, N):
        if A[i][m] != 0:
            raise ValueError("not in span")
    x = [Fraction(0)] * m
    for i, c in enumerate(piv_cols):
        x[c] = A[i][m]
    return x


monos = monomials(22)
vecs = [expansion(m) for m in monos]
idx = rank_basis(vecs)
basis = [monos[i] for i in idx]
bvecs = [vecs[i] for i in idx]
print("monomials of weight 22:", len(monos), " rank:", len(basis), " (dim M_22(Gamma_0(7)) = 15)")
assert len(basis) == 15
assert len(rank_basis([v[:15] for v in bvecs])) == 15, "first 15 coefficients do not determine the form"
# W matrix: column i = coordinates of basis_i | W
W = []
for m in basis:
    img, c = wimage(m)
    coords = solve_coords(bvecs, expansion(img))
    W.append([c * x for x in coords])
Wm = [[W[i][j] for i in range(15)] for j in range(15)]          # Wm[j][i]: coefficient of basis_j in basis_i | W


def apply_W(x):
    return [sum(Wm[j][i] * x[i] for i in range(15)) for j in range(15)]


def series(x):
    return [sum(x[i] * bvecs[i][n] for i in range(15)) for n in range(N)]


# self-test with Lambda_7^22
th7 = [0] * N
for xx in range(-20, 21):
    for yy in range(-20, 21):
        v = xx * xx + xx * yy + 2 * yy * yy
        if v < N:
            th7[v] += 1
T = [1] + [0] * (N - 1)
for _ in range(22):
    T = mul(T, th7)
xT = solve_coords(bvecs, T)
TW = series(apply_W(xT))
assert all(TW[n] == -T[n] for n in range(N)), "Fricke normalisation test failed"
print("self-test Lambda_7^22: theta in M_22(Gamma_0(7)) and theta|W = -theta  OK")


def inverse(M):
    n = len(M)
    A = [[Fraction(x) for x in row] + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0)
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [row[n:] for row in A]


# Miller-type parametrisation: the variables are the coefficients a_0..a_14 of theta_A themselves
C15 = [[Fraction(bvecs[i][n]) for i in range(15)] for n in range(15)]
CINV = inverse(C15)                                   # x = CINV a
MA_ALL = [[sum(Fraction(bvecs[i][n]) * CINV[i][k] for i in range(15)) for k in range(15)] for n in range(N)]
WC = [[sum(Wm[j][i] * CINV[i][k] for i in range(15)) for k in range(15)] for j in range(15)]
MW_ALL = [[sum(Fraction(bvecs[j][n]) * WC[j][k] for j in range(15)) for k in range(15)] for n in range(N)]
assert all(MA_ALL[n][k] == int(n == k) for n in range(15) for k in range(15))


def lp(b, lines=True, roots=True, nmax=None, obj=None):
    nmax = nmax or N
    s = -Fraction(7) ** (11 - b // 2) if b <= 22 else -Fraction(1, 7 ** (b // 2 - 11))
    # theta_B = (-7^(11 - b/2)) * (theta_A | W); rows are linear forms in (a_0, ..., a_14)
    MA = MA_ALL[:nmax]
    MWB = [[s * x for x in row] for row in MW_ALL[:nmax]]
    A_eq, b_eq, A_ub, b_ub = [], [], [], []
    A_eq.append(MA[0]); b_eq.append(1)
    A_eq.append(MWB[0]); b_eq.append(1)
    for n in range(1, 7):
        A_eq.append(MWB[n]); b_eq.append(0)
    for n in range(1, nmax):
        A_ub.append([-x for x in MA[n]]); b_ub.append(0)
        if n >= 7:
            A_ub.append([-x for x in MWB[n]]); b_ub.append(0)
    if lines:
        A_ub.append([-x for x in MA[2]]); b_ub.append(-462)
    if roots:
        # sqrt7 A is a sublattice of B: a vector of norm 2m in A gives one of norm 14m in B, so c_{7m} >= a_m
        for m in range(1, (nmax - 1) // 7 + 1):
            A_ub.append([a - c for a, c in zip(MA[m], MWB[7 * m])]); b_ub.append(0)

    return solve_scaled(A_eq, b_eq, A_ub, b_ub, obj)


def solve_scaled(A_eq, b_eq, A_ub, b_ub, obj=None):
    """Exact rational data -> column scaling (variable a_k replaced by D_k y_k, D_k = largest |entry| of column k)
    then row scaling, then HiGHS. Returns the scipy result; x of the result is mapped back to the a-variables."""
    rows = [list(r) for r in A_eq] + [list(r) for r in A_ub]
    D = []
    for k in range(15):
        m = max((abs(r[k]) for r in rows), default=Fraction(1))
        D.append(Fraction(1) / m if m else Fraction(1))

    def fl(rs, rhs):
        R = []
        h = []
        for r, v in zip(rs, rhs):
            rr = [x * d for x, d in zip(r, D)]
            m = max(abs(x) for x in rr + [Fraction(v)]) or 1
            R.append([float(x / m) for x in rr])
            h.append(float(Fraction(v) / m))
        return np.array(R), np.array(h)

    Ae, be = fl(A_eq, b_eq)
    Au, bu = fl(A_ub, b_ub)
    c = np.zeros(15) if obj is None else np.array([float(o * d) for o, d in zip(obj, D)])
    res = linprog(c, A_ub=Au, b_ub=bu, A_eq=Ae, b_eq=be, bounds=[(None, None)] * 15, method="highs")
    if res.status == 0:
        res.a = [float(D[k]) * res.x[k] for k in range(15)]
    return res


def lp_exact(b, lines=True, roots=True, nmax=45, minB=7):
    """Exact feasibility. minB = 7 means c_1..c_6 = 0 (B has minimum >= 14). Returns (feasible, a)."""
    import exact_lp as X
    s = -Fraction(7) ** (11 - b // 2) if b <= 22 else -Fraction(1, 7 ** (b // 2 - 11))
    MA = MA_ALL[:nmax]
    MWB = [[s * x for x in row] for row in MW_ALL[:nmax]]
    E, e, G, g = [], [], [], []
    E.append(MA[0]); e.append(1)
    E.append(MWB[0]); e.append(1)
    for n in range(1, minB):
        E.append(MWB[n]); e.append(0)
    for n in range(1, nmax):
        G.append(MA[n]); g.append(0)
        if n >= minB:
            G.append(MWB[n]); g.append(0)
    if lines:
        G.append(MA[2]); g.append(462)
    if roots:
        for m in range(1, (nmax - 1) // 7 + 1):
            G.append([c - a for a, c in zip(MA[m], MWB[7 * m])]); g.append(0)
    return X.feasible(E, e, G, g, 15)


if __name__ == "__main__":
    for b in range(2, 44, 2):
        f0, _ = lp_exact(b, lines=False, roots=False)
        f1, _ = lp_exact(b, lines=True, roots=True)
        print("b = %2d   min(B) >= 14 only: %-10s   + a_2 >= 462 and c_7m >= a_m: %s"
              % (b, "feasible" if f0 else "INFEASIBLE", "feasible" if f1 else "INFEASIBLE"), flush=True)
