"""C1, lab session, 2026-10-07. Theta series of level 7 and a linear programme per determinant exponent d.

  python theta_lp.py [N=100]          (one process, a few minutes, under 1 GB; scipy for the search, exact check in Fractions)

Setting (hand derivation of the lab session, see NOTE.md): for a srg(99,14,1,2), L = Z^99 cap ker(A + 4I), L1 its even
index-3 overlattice, M = sqrt7 L1*. Both are even of rank 44 and level 7, det L1 = 7^d, det M = 7^(44-d), d even.
theta_L1 = sum a_n q^n and theta_M = sum b_n q^n (n = norm / 2) lie in M_22(Gamma_0(7)), of dimension 15, with basis
    F_j = G t^j (j = 0..14),  G = theta_{x^2+xy+2y^2} (eta(7 tau)^7 / eta(tau))^7 = q^14 + ...,  t = (eta(tau)/eta(7 tau))^4,
and if theta_L1 = sum c_j F_j then theta_M = sum c_j 7^(d/2 + 2j - 25) F_(14-j)   (Fricke involution).
The program first CHECKS this formula on E8^a + (sqrt7 E8)^b + A + A (a + b = 5), whose two theta series are known.
Constraints: a_0 = b_0 = 1; a_1 = ... = a_6 = 0 (min L1 >= 14); a_n, b_n >= 0; b_2 >= 462 (triangles), b_3 >= 8316
(non-adjacent differences), b_4 >= 1386 (adjacent differences); a_7k >= b_k (sqrt7 M inside L1). Seven parameters remain,
taken to be b_1..b_7. Mode "a7=0" adds a_7 = 0 (hence b_1 = 0).
For each d the feasibility of the LP is decided in floating point, and an infeasibility is then re-proved exactly: rational
multipliers lambda_i >= 0 with sum lambda_i (linear part) = 0 and sum lambda_i (constant) < 0."""
import sys, math
from fractions import Fraction as Fr
N = int(sys.argv[1]) if len(sys.argv) > 1 else 100


def mul(a, b):
    c = [0] * (N + 1)
    for i, x in enumerate(a):
        if x:
            for j in range(N + 1 - i):
                if b[j]: c[i + j] += x * b[j]
    return c


def inv(a):
    b = [0] * (N + 1); b[0] = 1
    for n in range(1, N + 1): b[n] = -sum(a[k] * b[n - k] for k in range(1, n + 1))
    return b


def sub7(a):
    b = [0] * (N + 1)
    for i in range(N // 7 + 1): b[7 * i] = a[i]
    return b


def powers(a, lo, hi):                                                    # {k: a^k} for lo <= k <= hi (lo <= 0 <= hi)
    P = {0: [1] + [0] * N}; ai = inv(a)
    for k in range(1, hi + 1): P[k] = mul(P[k - 1], a)
    for k in range(-1, lo - 1, -1): P[k] = mul(P[k + 1], ai)
    return P


E = [1] + [0] * N
for n in range(1, N + 1):
    for i in range(N, n - 1, -1): E[i] -= E[i - n]
TA = [0] * (N + 1); R = int(math.isqrt(4 * N)) + 2
for x in range(-R, R + 1):
    for y in range(-R, R + 1):
        v = x * x + x * y + 2 * y * y
        if v <= N: TA[v] += 1
EP = powers(E, -7, 49); E7P = powers(sub7(E), -7, 49)
F = []
for j in range(15):
    f = mul(TA, mul(EP[4 * j - 7], E7P[49 - 4 * j])); s = 14 - j; f = [0] * s + f[:N + 1 - s]
    assert f[s] == 1 and not any(f[:s]); F.append(f)


def coords(f):                                                            # f = sum c_j F_j, from the first 15 coefficients; checked to q^N
    c = [Fr(0)] * 15; g = [Fr(x) for x in f]
    for n in range(15):
        j = 14 - n; c[j] = g[n]
        for m in range(n, N + 1): g[m] -= c[j] * F[j][m]
    assert not any(g), "not in the span of the basis"
    return c


def fricke(c, d): return [c[14 - i] * Fr(7) ** (d // 2 + 3 - 2 * i) for i in range(15)]      # coordinates of theta of sqrt7 Lambda*


def comb(c): return [sum(c[j] * F[j][n] for j in range(15)) for n in range(N + 1)]


def selfcheck():                                                          # the basis and the Fricke formula on lattices with known theta series
    E4 = [1] + [240 * sum(k ** 3 for k in range(1, n + 1) if n % k == 0) for n in range(1, N + 1)]; E47 = sub7(E4); TA2 = mul(TA, TA)
    for a in range(6):
        b = 5 - a; f = TA2; g = TA2
        for _ in range(a): f = mul(f, E4); g = mul(g, E47)
        for _ in range(b): f = mul(f, E47); g = mul(g, E4)
        assert comb(fricke(coords(f), 8 * b + 2)) == [Fr(x) for x in g], "Fricke formula fails"
    print("basis and Fricke formula checked on E8^a + (sqrt7 E8)^(5-a) + A + A, a = 0..5, to q^%d" % N, flush=True)


# ---- the affine family: everything as const + sum_k coef_k b_k (k = 1..7)
def aff(const=0): return [Fr(const)] + [Fr(0)] * 7
def add(u, v, s=1): return [x + s * y for x, y in zip(u, v)]
def sc(u, s): return [x * s for x in u]


def family(d):
    c = [None] * 15; c[14] = aff(1)
    for n in range(1, 7):                                                # a_1 = ... = a_6 = 0 fixes c_13 .. c_8
        j = 14 - n; acc = aff(0)
        for i in range(j + 1, 15): acc = add(acc, sc(c[i], F[i][n]))
        c[j] = sc(acc, -1)
    cp = [None] * 15                                                     # coordinates of theta_M
    for i in range(0, 7): cp[i] = sc(c[14 - i], Fr(7) ** (d // 2 + 3 - 2 * i))
    cp[14] = aff(1)                                                      # b_0 = 1  (c_0 = 7^(25 - d/2))
    for n in range(1, 8):                                                # b_n = beta_n fixes cp_(14-n)
        i0 = 14 - n; acc = aff(0); acc[n] = Fr(1)
        for i in range(i0 + 1, 15): acc = add(acc, sc(cp[i], -F[i][n]))
        cp[i0] = acc
    for j in range(0, 8): c[j] = sc(cp[14 - j], Fr(7) ** (-(d // 2 + 3 - 2 * (14 - j))))
    A = [aff(0) for _ in range(N + 1)]; B = [aff(0) for _ in range(N + 1)]
    for n in range(N + 1):
        for j in range(15):
            if F[j][n]: A[n] = add(A[n], sc(c[j], F[j][n])); B[n] = add(B[n], sc(cp[j], F[j][n]))
    assert A[0] == aff(1) and B[0] == aff(1) and all(A[n] == aff(0) for n in range(1, 7))
    for n in range(1, 8): e = aff(0); e[n] = Fr(1); assert B[n] == e
    return A, B


def constraints(d, a7zero):
    A, B = family(d); C = []                                              # each: (label, affine form required >= 0)
    for n in range(7, N + 1): C.append(("a_%d >= 0" % n, A[n]))
    for n in range(1, N + 1): C.append(("b_%d >= 0" % n, B[n]))
    for n, lo in ((2, 462), (3, 8316), (4, 1386)): C.append(("b_%d >= %d" % (n, lo), add(B[n], aff(lo), -1)))
    for k in range(1, N // 7 + 1): C.append(("a_%d >= b_%d" % (7 * k, k), add(A[7 * k], B[k], -1)))
    if a7zero: C.append(("a_7 <= 0", sc(A[7], -1)))
    return A, B, C


def solve(d, a7zero):
    import numpy as np
    from scipy.optimize import linprog
    A, B, C = constraints(d, a7zero)
    S = []
    for k in range(1, 8):                                                # column scales
        v = [math.log(abs(float(f[k]))) - math.log(abs(float(f[0]))) for _, f in C if f[k] and f[0]]
        S.append(math.exp(-sorted(v)[len(v) // 2]) if v else 1.0)
    rows = []; rhs = []
    for _, f in C:                                                       # f0 + sum f_k b_k >= 0   <=>   -sum f_k S_k u_k <= f0
        g = [-float(f[k]) * S[k - 1] for k in range(1, 8)]; h = float(f[0]); m = max([abs(x) for x in g] + [abs(h)]) or 1.0
        rows.append([x / m for x in g] + [-1.0]); rhs.append(h / m)
    res = linprog([0.0] * 7 + [1.0], A_ub=np.array(rows), b_ub=np.array(rhs), bounds=[(None, None)] * 7 + [(-1.0, None)], method="highs")
    if res.status != 0: return {"status": "LP solver status %d" % res.status}
    out = {"s": float(res.fun)}
    if res.fun <= 1e-9:
        out["status"] = "feasible (floating point)"; rng = {}
        for name, f in (("a_7", A[7]), ("b_1", B[1]), ("b_2", B[2]), ("a_8", A[8])):
            lohi = []
            for sgn in (1, -1):
                r2 = linprog([sgn * float(f[k]) * S[k - 1] for k in range(1, 8)], A_ub=np.array([r[:7] for r in rows]), b_ub=np.array(rhs), bounds=[(None, None)] * 7, method="highs")
                lohi.append(float(f[0]) + sgn * r2.fun if r2.status == 0 else None)
            rng[name] = lohi
        out["ranges"] = rng; return out
    lam = [-x for x in res.ineqlin.marginals]; top = max(lam); sup = [i for i, x in enumerate(lam) if x > 1e-7 * top]
    out["status"] = "infeasible (floating point)"; out["support"] = [C[i][0] for i in sup]
    # exact: lambda on the support with sum lambda_i (coef) = 0, sum lambda = 1
    M = [[C[i][1][k] for i in sup] + [Fr(0)] for k in range(1, 8)] + [[Fr(1)] * len(sup) + [Fr(1)]]
    piv = []; rr = 0
    for col in range(len(sup)):
        p = next((i for i in range(rr, len(M)) if M[i][col] != 0), None)
        if p is None: continue
        M[rr], M[p] = M[p], M[rr]; q = M[rr][col]; M[rr] = [x / q for x in M[rr]]
        for i in range(len(M)):
            if i != rr and M[i][col] != 0: fct = M[i][col]; M[i] = [x - fct * y for x, y in zip(M[i], M[rr])]
        piv.append(col); rr += 1
        if rr == len(M): break
    if any(all(x == 0 for x in row[:-1]) and row[-1] != 0 for row in M): out["exact"] = "exact system inconsistent on this support"; return out
    lamx = [Fr(0)] * len(sup)
    for i, col in enumerate(piv): lamx[col] = M[i][-1]
    lin = [sum(l * C[i][1][k] for l, i in zip(lamx, sup)) for k in range(1, 8)]; cst = sum(l * C[i][1][0] for l, i in zip(lamx, sup))
    good = all(l >= 0 for l in lamx) and not any(lin) and cst < 0
    out["exact"] = "EXACT CERTIFICATE OK" if good else "exact check failed (min lambda %s, const sign %s)" % (float(min(lamx)), "neg" if cst < 0 else "nonneg")
    if good: out["certificate"] = [(C[i][0], str(l)) for l, i in zip(lamx, sup) if l]
    return out


if __name__ == "__main__":
    import json
    selfcheck(); allout = {}
    for a7zero in (False, True):
        print("\n== mode: min >= 14%s" % (", a_7 = 0" if a7zero else ""), flush=True)
        for d in range(2, 44, 2):
            o = solve(d, a7zero); allout["%s_d%d" % ("a7zero" if a7zero else "base", d)] = o
            line = "d = %2d (r = %2d): %s" % (d, d + 1, o["status"])
            if "exact" in o: line += "; " + o["exact"] + "; support: " + ", ".join(o["support"])
            if "ranges" in o: line += "; " + "; ".join("%s in [%s, %s]" % ((k,) + tuple("%.6g" % x if x is not None else "unbounded" for x in v)) for k, v in o["ranges"].items())
            print(line, flush=True)
    json.dump(allout, open("theta_lp_out_N%d.json" % N, "w"), indent=1)
