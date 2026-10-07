"""C1, lab session, 2026-10-07. The weight-26 cusp form of the quartic harmonic, added to the exact LP of theta_lp_exact.py.

  python theta_quartic.py <N> table|ladder [d ...]

H(f) = sum_v f_v^4 - (2/69) |f|^4 is harmonic of degree 4 on the (-4)-eigenspace (P_vv = 4/9, dimension 44). So
    Theta4 = sum_{f in L1} H(f) q^(|f|^2/2)   and   Theta4M = sum_{m in M} H(m) q^(|m|^2/2)     (H(m) = H(sqrt7 m)/49)
are cusp forms of weight 26 on Gamma_0(7) (dimension 15), and Theta4(-1/(7 tau)) = -7^(24-d/2) tau^26 Theta4M(tau).
Basis of M_26: K_j = G26 t^j (j = 0..16), G26 = theta_A^2 (eta(7tau)^7/eta(tau))^8 = q^16 + ..., cusp forms j = 1..15, and
K_j(-1/(7 tau)) = -7^(2j-3) tau^26 K_(16-j); so Theta4 = sum e_j K_j gives Theta4M = sum e_j 7^(2j-27+d/2) K_(16-j).
The K-formula is CHECKED below on E4(tau)^a E4(7tau)^(6-a) theta_A^2. Theta4 = O(q^7) leaves nine parameters e_1..e_9.
New constraints, with S(n) = sum of sum_v f_v^4 over the vectors of L1 of norm 2n:  lo(n) a_n <= S(n) <= hi(n) a_n, where
[lo(n), hi(n)] contains sum_v f_v^4 for EVERY vector of L1 of norm 2n (function bounds below), and likewise for the vectors
of sqrt7 M, of norm 14k, with b_k. Exact at norms 14, 16, 18 (entries 0, +-1) and for the roots of M.
Variables: b_1..b_7, e_1..e_9 (sixteen). Exact rational simplex of theta_lp_exact."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
N = T.N; NV = 16
mul = T.mul
TA2 = mul(T.TA, T.TA); EP = T.powers(T.E, -8, 56); E7P = T.powers(T.sub7(T.E), -8, 56)
K = []
for j in range(17):
    f = mul(TA2, mul(EP[4 * j - 8], E7P[56 - 4 * j])); s = 16 - j; f = [0] * s + f[:N + 1 - s]
    assert f[s] == 1 and not any(f[:s]); K.append(f)


def selfcheck():
    E4 = [1] + [240 * sum(k ** 3 for k in range(1, n + 1) if n % k == 0) for n in range(1, N + 1)]; E47 = T.sub7(E4)
    for a in range(7):
        f = TA2; g = TA2
        for _ in range(a): f = mul(f, E4); g = mul(g, E47)
        for _ in range(6 - a): f = mul(f, E47); g = mul(g, E4)
        e = [Fr(0)] * 17; h = [Fr(x) for x in f]
        for n in range(17):
            j = 16 - n; e[j] = h[n]
            for m in range(n, N + 1): h[m] -= e[j] * K[j][m]
        assert not any(h), "not in the span"
        img = [sum(e[j] * Fr(7) ** (2 * j - 3) * K[16 - j][n] for j in range(17)) for n in range(N + 1)]
        assert img == [Fr(7) ** (4 * a + 1) * x for x in g], "weight-26 Fricke formula fails"
    print("weight 26: basis and Fricke formula checked on E4^a E4(7tau)^(6-a) theta_A^2, a = 0..6, to q^%d" % N, flush=True)


def bounds(n):
    """[lo, hi] containing sum_v f_v^4 for every vector f of L1 of norm 2n (n >= 7)."""
    if n in (7, 8, 9): lo_i = hi_i = Fr(2 * n)                           # integer vectors: entries 0, +-1 below norm 20
    else:
        h = 1
        while (h + 1) ** 2 + 7 * (h + 1) <= 2 * n: h += 1                # an entry of absolute value h needs norm >= h^2 + 7h
        lo_i = Fr(2 * n); hi_i = Fr(2 * n + 12 * (n - 8)) if h == 2 else Fr(h * h * 2 * n)
    if n < 11: return lo_i, hi_i
    e = n - 11; vals = None                                               # coset: f = phi - 1/3, sum phi = 33, sum phi(phi-1) = 2e
    if e <= 6:
        vals = []
        def rec(rest, minc, phis):
            if rest == 0:
                ones = 33 - sum(phis); zeros = 99 - len(phis) - ones
                if ones >= 0 and zeros >= 0: vals.append(sum((Fr(p) - Fr(1, 3)) ** 4 for p in phis) + ones * Fr(16, 81) + zeros * Fr(1, 81))
                return
            for j in range(minc, 4):                                      # cost j(j+1)/2 = 1, 3, 6 for phi in {-j, j+1}
                c = j * (j + 1) // 2
                if c <= rest:
                    for p in (-j, j + 1): rec(rest - c, j, phis + [p])
        rec(e, 1, [])
    if vals: lo_c, hi_c = min(vals), max(vals)
    else:
        j = 0
        while (j + 1) * (j + 2) <= 2 * e: j += 1
        lo_c = Fr(4 * n * n, 99); hi_c = (Fr(j) + Fr(2, 3)) ** 2 * 2 * n
    return min(lo_i, lo_c), max(hi_i, hi_c)


def ext(f): return list(f) + [Fr(0)] * (NV + 1 - len(f))


def build(d, extra=()):
    A, B = T.family(d); A = [ext(f) for f in A]; B = [ext(f) for f in B]
    A4 = []; B4 = []                                                     # B4 = 49 * (coefficient of Theta4M)
    for n in range(N + 1):
        fa = [Fr(0)] * (NV + 1); fb = [Fr(0)] * (NV + 1)
        for j in range(1, 10):
            fa[7 + j] = Fr(K[j][n]); fb[7 + j] = 49 * Fr(7) ** (2 * j - 27 + d // 2) * K[16 - j][n]
        A4.append(fa); B4.append(fb)
    add = lambda u, v, s=1: [x + s * y for x, y in zip(u, v)]; sc = lambda u, s: [x * s for x in u]; cst = lambda c: [Fr(c)] + [Fr(0)] * NV
    C = []
    for n in range(7, N + 1): C.append(("a_%d >= 0" % n, A[n]))
    for n in range(1, N + 1): C.append(("b_%d >= 0" % n, B[n]))
    for n, lo in ((2, 462), (3, 24948), (4, 388080), (5, 196812)): C.append(("b_%d >= %d" % (n, lo), add(B[n], cst(lo), -1)))
    for k in range(1, N // 7 + 1): C.append(("a_%d >= b_%d" % (7 * k, k), add(A[7 * k], B[k], -1)))
    for n in range(7, N + 1):                                            # lo a_n <= S(n) = A4_n + (8 n^2/69) a_n <= hi a_n
        lo, hi = bounds(n); c0 = Fr(8 * n * n, 69)
        C.append(("S(%d) >= lo a" % n, add(A4[n], sc(A[n], c0 - lo)))); C.append(("S(%d) <= hi a" % n, add(sc(A[n], hi - c0), A4[n], -1)))
    for k in range(1, N // 7 + 1):                                       # same for the vectors of sqrt7 M, norm 14k
        lo, hi = bounds(7 * k); c0 = Fr(2 * 196 * k * k, 69)
        low = add(B4[k], sc(B[k], c0 - lo)); up = add(sc(B[k], hi - c0), B4[k], -1)
        if k == 2: up = add(up, cst(462 * (Fr(52, 3) - hi)))             # S <= 462 * 52/3 + (b_2 - 462) hi  (sign corrected: Codex, 07/10)
        C.append(("SM(%d) >= lo b" % k, low)); C.append(("SM(%d) <= hi b" % k, up))
    for part in extra:
        if part.startswith("min:"):
            for n in range(7, int(part[4:])): C.append(("a_%d <= 0" % n, sc(A[n], -1)))
        elif part == "a7": C.append(("a_7 <= 0", sc(A[7], -1)))
    return A, B, C


def feasible(C):
    res = X.simplex([f[1:] for _, f in C], [-f[0] for _, f in C], [Fr(0)] * NV)
    if res[0] == "unbounded":
        lam = res[1]; assert all(x >= 0 for x in lam)
        assert all(sum(l * f[k] for l, (_, f) in zip(lam, C) if l) == 0 for k in range(1, NV + 1)) and sum(l * f[0] for l, (_, f) in zip(lam, C)) < 0
        return ("infeasible", [(C[i][0], lam[i]) for i in range(len(C)) if lam[i]])
    assert res[0] == "optimal" and res[1] == 0
    return ("feasible", None)


def minimise(C, form):
    res = X.simplex([f[1:] for _, f in C], [-f[0] for _, f in C], form[1:])
    if res[0] != "optimal": return None
    _, val, lam, y = res
    assert all(x >= 0 for x in lam) and all(sum(l * f[k] for l, (_, f) in zip(lam, C) if l) == form[k] for k in range(1, NV + 1))
    assert all(f[0] + sum(f[k] * y[k - 1] for k in range(1, NV + 1)) >= 0 for _, f in C)
    return form[0] + val


if __name__ == "__main__":
    what = sys.argv[2]; ds = [int(x) for x in sys.argv[3:]] or list(range(26, 44, 2))
    T.selfcheck(); selfcheck()
    for d in ds:
        if what == "table":
            A, B, C = build(d); st = feasible(C)
            if st[0] == "infeasible": print("d = %2d (r = %2d): INFEASIBLE with the quartic constraints; certificate: %s" % (d, d + 1, ", ".join(nm for nm, _ in st[1])), flush=True); continue
            parts = []
            for nm, f in (("a_7", A[7]), ("a_8", A[8]), ("b_1", B[1]), ("b_2", B[2]), ("b_3", B[3])):
                lo = minimise(C, f); hi = minimise(C, [-x for x in f])
                parts.append("%s in [%s, %s]" % (nm, X.show(lo) if lo is not None else "-inf", X.show(-hi) if hi is not None else "+inf"))
            print("d = %2d (r = %2d): feasible; %s" % (d, d + 1, "; ".join(parts)), flush=True)
        else:
            last = None
            for m in range(7, 30):
                A, B, C = build(d, ("min:%d" % m,)); st = feasible(C)
                if st[0] == "infeasible": break
                last = m
            print("d = %2d (r = %2d): min(L1) >= %s compatible, >= %d INFEASIBLE (%s)" % (d, d + 1, "none" if last is None else 2 * last, 2 * m, ", ".join(nm for nm, _ in st[1])), flush=True)
