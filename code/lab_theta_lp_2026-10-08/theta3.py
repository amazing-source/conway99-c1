"""C1, lab session, 2026-10-07/08. THE 3-SIDE: theta series of level 7 for the eigenvalue 3, through an even lattice of rank 60.

  python theta3.py <N> check                  self-tests only
  python theta3.py <N> run [d ...]            exact LP per d = r - 1 (default 34..42)

Objects (Gamma a srg(99,14,1,2), F = E_3 + R 1, of dimension 55):
  K3  = Z^99 cap F = { kappa : (A - 3I) kappa = c 1 }  (then sum kappa = 9c);   u = (1/3) 1, of norm 11;
  K3' = K3 + Z u : odd lattice of rank 55, level 7, determinant 7^d, characteristic vector w = 1 = 3u (norm 99 = 3 mod 8);
  E   = the even neighbour of K3' + Z^5 :  { (x,n) : |x|^2 + |n|^2 even } union ( the same + (w/2, (1/2)^5) ).
E is even, of rank 60 and level 7, det 7^d: theta_E in M_30(Gamma_0(7)), dimension 21, basis F_j = (eta(7tau)^7/eta(tau))^10 t^j,
j = 0..20, and theta of sqrt7 E* equals sum_j c_j 7^(2j-35+d/2) F_(20-j) when theta_E = sum_j c_j F_j.
Decomposition along u: x = a u + l with a = (x,u)/11 in (1/11)Z and l in a coset of L_3 = Z^99 cap E_3 (class j = 11a mod 11,
j = 3c mod 11). With N_j(nu) = number of vectors of the coset j of projected norm nu,
    theta_E = sum_j Phi_j * Theta_j,     Theta_j = sum_nu N_j(nu) q^(nu/2),
Phi_j = theta series of the coset j of the rank-6 even lattice R6 (points (a, n), a in (1/11)Z or (1/11)Z + 1/2, n in Z^5 or
(Z + 1/2)^5, norm 11 a^2 + |n|^2, with the parity rules of the neighbour construction; function phis below).
SELF-TESTS: (1) the same decomposition for Z^11 + Z^5 (u = 1_11 = w, L_3 replaced by A_10) must give theta of D_16^+, i.e.
E_4^2; (2) the weight-30 basis and Fricke formula on E_4^a E_4(7tau)^(7-a) theta_A^2.
Known zeros: N_0(0) = 1, N_0(nu) = 0 for 0 < nu < 12 (an integer 3-eigenvector has norm >= 12); for the class of c
(|c| <= 5), nu = |kappa|^2 - 9c^2/11 >= 9|c|(1 - |c|/11), with |kappa|^2 = c mod 2.
Dual side: sqrt7 E* is the set of (psi', n') in (Z^99 x Z^5) union ((Z+1/2)^99 x (Z+1/2)^5), 3 | sum psi, sum psi + sum n even,
with norm Q3(psi') + 7 |n'|^2, Q3(psi) = psi^t (4I + A) psi - (sum psi)^2 / 9, modulo L. Forced vectors (n = 0, sum psi = 0;
two of them coincide only if their difference is a non-zero vector of L, of norm >= 14):
  norm 6 : e_u - e_v, u ~ v                                   1386
  norm 8 : e_u - e_v, u not~ v (8316); e_a + e_b - e_c - e_d on the two diagonals of an induced 4-cycle (4158)
  norm 10: e_a + e_b - e_c - e_d on an induced path c - a - d - b ... (91476 paths, two signs)          182952
  norm 14: psi = 0, n = +-e_i +- e_j                                                                      40"""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
N = T.N; mul = T.mul


def phis(kw, bound):
    """{j: {rho: count}} for the cosets of R6; kw = 1 (w = u) or 3 (w = 3u); rho = 11 a^2 + |n|^2 <= bound (Fractions)."""
    R = int(bound ** 0.5) + 2
    one = {0: 1}
    def conv(P, Q):
        out = {}
        for (k1, v1) in P.items():
            for (k2, v2) in Q.items():
                k = (k1[0] + k2[0], (k1[1] + k2[1]) % 4) if isinstance(k1, tuple) else None
                out[k] = out.get(k, 0) + v1 * v2
        return out
    # integer n in Z^5: key (norm, sum mod 4) (only parity is used); half n' = o/2, o odd: key (sum o^2, sum o mod 4)
    base_i = {}; base_h = {}
    for k in range(-R, R + 1):
        if k * k <= bound: base_i[(k * k, k % 4)] = base_i.get((k * k, k % 4), 0) + 1
    for o in range(-2 * R - 1, 2 * R + 2, 2):
        if o * o <= 4 * bound: base_h[(o * o, o % 4)] = base_h.get((o * o, o % 4), 0) + 1
    def power5(base, cap):
        P = {(0, 0): 1}
        for _ in range(5):
            Q = {}
            for (s1, r1), v1 in P.items():
                for (s2, r2), v2 in base.items():
                    if s1 + s2 <= cap: key = (s1 + s2, (r1 + r2) % 4); Q[key] = Q.get(key, 0) + v1 * v2
            P = Q
        return P
    GI = power5(base_i, bound); GH = power5(base_h, 4 * bound)
    out = {j: {} for j in range(11)}
    M = int((11 * bound) ** 0.5) + 12
    for m in range(-M, M + 1):
        j = m % 11
        ra = Fr(m * m, 11)                                               # integer type: a = m/11
        if ra <= bound:
            par = (kw * m) % 2
            for (s, r), v in GI.items():
                if r % 2 == par and ra + s <= bound: out[j][ra + s] = out[j].get(ra + s, 0) + v
        ra = 11 * (Fr(m, 11) + Fr(1, 2)) ** 2                            # half type: a' = m/11 + 1/2
        if ra <= bound:
            tgt = (5 - 2 * kw * m + 11 * kw * (kw - 1)) % 4
            for (s, r), v in GH.items():
                rho = ra + Fr(s, 4)
                if r == tgt and rho <= bound: out[j][rho] = out[j].get(rho, 0) + v
    return out


def test_toy():
    B = 2 * min(N, 12); PH = phis(1, B)
    # cosets of A_10: x in Z^11 with sum x = s (s = 0..10): count by norm
    P = {(0, 0): 1}
    for _ in range(11):
        Q = {}
        for (sm, nm), v in P.items():
            for k in range(-5, 6):
                if nm + k * k <= B + 12: Q[(sm + k, nm + k * k)] = Q.get((sm + k, nm + k * k), 0) + v
        P = Q
    tot = {}
    for (sm, nm), v in P.items():
        if 0 <= sm <= 10:
            nu = Fr(nm) - Fr(sm * sm, 11)
            for rho, c in PH[sm % 11].items():
                if (rho + nu) <= B: tot[rho + nu] = tot.get(rho + nu, 0) + v * c
    E4 = [1] + [240 * sum(k ** 3 for k in range(1, n + 1) if n % k == 0) for n in range(1, N + 1)]; E8 = mul(E4, E4)
    assert all(k.denominator == 1 and k % 2 == 0 for k in tot), "odd or fractional norm"
    for n in range(0, B // 2 + 1): assert tot.get(Fr(2 * n), 0) == E8[n], ("toy fails at", n, tot.get(Fr(2 * n), 0), E8[n])
    print("toy test passed: Z^11 + Z^5 decomposed along u gives theta of D_16^+ = E_4^2 to q^%d" % (B // 2), flush=True)


EP = T.powers(T.E, -10, 70); E7P = T.powers(T.sub7(T.E), -10, 70)
F30 = []
for j in range(21):
    f = mul(EP[4 * j - 10], E7P[70 - 4 * j]); s = 20 - j; f = [0] * s + f[:N + 1 - s]; assert f[s] == 1 and not any(f[:s]); F30.append(f)


def test_fricke():
    E4 = [1] + [240 * sum(k ** 3 for k in range(1, n + 1) if n % k == 0) for n in range(1, N + 1)]; E47 = T.sub7(E4); TA2 = mul(T.TA, T.TA)
    for a in range(8):
        f = TA2; g = TA2
        for _ in range(a): f = mul(f, E4); g = mul(g, E47)
        for _ in range(7 - a): f = mul(f, E47); g = mul(g, E4)
        c = [Fr(0)] * 21; h = [Fr(x) for x in f]
        for n in range(21):
            j = 20 - n; c[j] = h[n]
            for m in range(n, N + 1): h[m] -= c[j] * F30[j][m]
        assert not any(h), "not in the span (weight 30)"
        d = 8 * (7 - a) + 2
        img = [sum(c[j] * Fr(7) ** (2 * j - 35 + d // 2) * F30[20 - j][n] for j in range(21)) for n in range(N + 1)]
        assert img == [Fr(x) for x in g], "weight-30 Fricke formula fails"
    print("weight 30: basis and Fricke formula checked on E4^a E4(7tau)^(7-a) theta_A^2, a = 0..7, to q^%d" % N, flush=True)


# ---- the unknowns: (class j in 0..5, nu); class j <-> c with 3c = j mod 11, |c| <= 5
CLS = {0: 0, 3: 1, 5: -2, 2: -3, 1: 4, 4: 5}
def variables():
    V = []
    for j, c in CLS.items():
        lo = Fr(12) if j == 0 else Fr(9 * abs(c)) - Fr(9 * c * c, 11)
        nu = lo
        while nu / 2 <= N: V.append((j, nu)); nu += 2
    return V


def system(d, lows):
    """rows of M x = g, x >= 0, x = (N_j(nu) ..., slacks ...)."""
    PH = phis(3, 2 * N); V = variables(); nv = len(V)
    base = [PH[0].get(Fr(2 * n), 0) for n in range(N + 1)]               # N_0(0) = 1
    col = []
    for (j, nu) in V:
        mult = 1 if j == 0 else 2                                        # classes j and -j
        col.append([mult * PH[j].get(Fr(2 * n) - nu, 0) for n in range(N + 1)])
    # A_n = base[n] + sum_v col[v][n] x_v ; affine forms as lists [const, coef_1..coef_nv]
    def A(n): return [Fr(base[n])] + [Fr(col[v][n]) for v in range(nv)]
    add = lambda u, w, s=1: [x + s * y for x, y in zip(u, w)]
    c = [None] * 21
    for n in range(21):
        j = 20 - n; acc = A(n)
        for i in range(j + 1, 21):
            if F30[i][n]: acc = add(acc, c[i], -F30[i][n])
        c[j] = acc
    rows = []; rhs = []; labels = []
    for n in range(21, N + 1):                                           # theta_E lies in the span
        acc = A(n)
        for i in range(21):
            if F30[i][n]: acc = add(acc, c[i], -F30[i][n])
        rows.append(acc[1:]); rhs.append(-acc[0]); labels.append("span n=%d" % n)
    Bm = []
    for m in range(N + 1):
        acc = [Fr(0)] * (nv + 1)
        for j in range(21):
            fj = F30[20 - j][m]
            if fj: acc = add(acc, c[j], Fr(7) ** (2 * j - 35 + d // 2) * fj)
        Bm.append(acc)
    rows.append(Bm[0][1:]); rhs.append(1 - Bm[0][0]); labels.append("B_0 = 1")
    ns = N                                                               # slacks for B_m >= low_m, m = 1..N
    M = [r + [Fr(0)] * ns for r in rows]
    for m in range(1, N + 1):
        r = Bm[m][1:] + [Fr(0)] * ns; r[nv + m - 1] = Fr(-1); M.append(r); rhs.append(Fr(lows.get(m, 0)) - Bm[m][0]); labels.append("B_%d >= %d" % (m, lows.get(m, 0)))
    return V, M, rhs, labels


LOWS = {3: 1386, 4: 12474, 5: 182952, 7: 40}


def solve(d, zero=(), objective=None, lows=LOWS):
    V, M, rhs, labels = system(d, lows); nv = len(V); ncol = len(M[0])
    keep = [k for k in range(ncol) if not (k < nv and V[k] in zero)]
    cols = [[M[r][k] for r in range(len(M))] for k in keep]
    cost = [Fr(0)] * len(keep)
    if objective is not None:
        for i, k in enumerate(keep):
            if k < nv and V[k] in objective: cost[i] = Fr(-1)
    res = X.simplex(cols, cost, rhs)
    if res[0] == "infeasible": return ("infeasible",)
    if res[0] == "unbounded": return ("unbounded",)
    lam = res[2]
    assert all(x >= 0 for x in lam) and all(sum(M[r][k] * lam[i] for i, k in enumerate(keep)) == rhs[r] for r in range(len(M))), "solution does not satisfy the system"
    return ("feasible", -res[1], {V[k]: lam[i] for i, k in enumerate(keep) if k < nv and lam[i]})


if __name__ == "__main__":
    test_toy(); test_fricke()
    if sys.argv[2] == "run":
        ds = [int(x) for x in sys.argv[3:]] or list(range(34, 44, 2))
        V = variables(); print("N = %d, %d unknown shell counts; first shells: %s" % (N, len(V), ", ".join("j=%d nu=%s" % v for v in V if v[1] < 16)), flush=True)
        for d in ds:
            r0 = solve(d)
            print("d = %d (r = %d): %s" % (d, d + 1, r0[0]), flush=True)
