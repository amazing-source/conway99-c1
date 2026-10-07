"""C1, lab session, 2026-10-07/08. A second level-7 programme on the (-4)-side that KEEPS the 3-part of the dual:
the vertex vectors sqrt7 P e_v (norm 28/9), lost in M = sqrt7 L1*, come back as vectors of norm 4.

  python theta_pi.py <N> [d ...]

Lattices (L = Z^99 cap ker(A + 4I), P the projector, pi the projection of Z^9 on the hyperplane sum = 0, i.e. on A_8*):
  Lam = { (sqrt7 P psi, pi(z)) : psi in Z^99, z in Z^9, sum psi = sum z mod 9 },   norm  Q'(psi) + |z|^2 - (sum z)^2/9,
        Q'(psi) = 7 |P psi|^2 = (27 |psi|^2 - 9 psi^t A psi + (sum psi)^2) / 9.     Even, rank 52, level 7, det 7^(44-d).
  Pi  = sqrt7 Lam* = { (phi - (t/9) 1, sqrt7 pi(z')) : phi in Z^99, (A + 4I) phi = 2t 1, z' in Z^9, sum z' = -t mod 9 },
        norm |phi|^2 - 11 t^2/9 + 7 (|z'|^2 - (sum z')^2/9).                         Even, rank 52, level 7, det 7^(d+8).
Shells of Pi: t = 0 gives L + sqrt7 A_8 (norm 14: the Fano vectors and the 72 vectors sqrt7 * root; norm 16: the norm-16
vectors of L); t = +-1 starts at norm 18 (|phi|^2 = 11 is impossible), t = +-2 at 28, t = +-3 at 36, t = +-4 at 40.
So theta_Pi = 1 + (a_7 + 72) q^7 + a_8 q^8 + ..., in M_26(Gamma_0(7)) (dimension 17, basis K_j of theta_quartic.py), and
theta_Lam = sum_j e_j 7^(2j-25+d/2) K_(16-j) if theta_Pi = sum_j e_j K_j. Nine free parameters: B_1..B_9 (shells of Lam).
Forced vectors of Lam: pairs (psi, z) with psi of support <= 3 (pairwise distinct in L*: a coincidence needs a non-zero
vector of K3 = Z^99 cap (E_3 + Q1) of support <= 6, and those have support >= 8) and z in the class sum psi mod 9.
Constraints: A_n >= 0, A_7 >= 72, B_n >= forced_n, A_7k >= B_k, and 7 (A_7 - 72) + 8 A_8 <= 55440 (Codex, note 173)."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
import theta_quartic as TQ
N = T.N; K = TQ.K; NV = 9


def a8_classes(maxnorm):
    """{k: {nu: count}}: vectors pi(z) of class k = sum z mod 9, nu = |z|^2 - (sum z)^2/9 <= maxnorm."""
    out = {k: {} for k in range(9)}
    P = {(0, 0): 1}
    for _ in range(9):
        Q = {}
        for (s, m), v in P.items():
            for x in range(-4, 5):
                if m + x * x <= maxnorm + 4: Q[(s + x, m + x * x)] = Q.get((s + x, m + x * x), 0) + v
        P = Q
    for (s, m), v in P.items():
        if 0 <= s <= 8:                                                  # one representative per projection: sum z in 0..8
            nu = Fr(m) - Fr(s * s, 9)
            if nu <= maxnorm: out[s][nu] = out[s].get(nu, 0) + v
    return out


def psi_types():
    """(sum psi, Q', count) for the integer vectors of support <= 3 (and 2 e_v), both signs listed separately."""
    Ty = []
    def add(s, q, c): Ty.append((s, Fr(q), c)); Ty.append((-s, Fr(q), c)) if s != 0 else None
    Ty.append((0, Fr(0), 1))                                             # psi = 0
    add(1, Fr(28, 9), 99); add(2, Fr(112, 9), 99)                        # e_v, 2 e_v
    Ty.append((0, Fr(8), 1386)); Ty.append((0, Fr(6), 8316))             # e_u - e_v (ordered pairs): adjacent, non-adjacent
    add(2, Fr(40, 9), 693); add(2, Fr(58, 9), 4158)                      # e_u + e_v
    for e, c in ((3, 231), (2, 8316), (1, 49896), (0, 98406)): add(3, Fr(10 - 2 * e), c)          # e_u + e_v + e_w
    for s_, c in ((1, 49896), (0, 311850), (-1, 100485), (-2, 8316)): add(1, Fr(82 - 18 * s_, 9), c)   # e_u + e_v - e_w
    assert 49896 + 311850 + 100485 + 8316 == 4851 * 97 and 231 + 8316 + 49896 + 98406 == 99 * 98 * 97 // 6
    return Ty


def forced(maxn):
    A8 = a8_classes(2 * maxn); low = {}
    for s, q, c in psi_types():
        for nu, cz in A8[s % 9].items():
            tot = q + nu
            if tot.denominator == 1 and tot % 2 == 0 and tot // 2 <= maxn: low[int(tot // 2)] = low.get(int(tot // 2), 0) + c * cz
            else: assert tot.denominator != 1 or tot % 2 == 0, "odd norm in an even lattice"
    return low


def aff(c=0): return [Fr(c)] + [Fr(0)] * NV
def add(u, v, s=1): return [x + s * y for x, y in zip(u, v)]
def sc(u, s): return [x * s for x in u]


def family(d):
    e = [None] * 17; e[16] = aff(1)
    for n in range(1, 7):
        j = 16 - n; acc = aff(0)
        for i in range(j + 1, 17): acc = add(acc, sc(e[i], K[i][n]))
        e[j] = sc(acc, -1)
    ep = [None] * 17
    for i in range(0, 7): ep[i] = sc(e[16 - i], Fr(7) ** (7 - 2 * i + d // 2))
    ep[16] = aff(1)
    for n in range(1, 10):
        i0 = 16 - n; acc = aff(0); acc[n] = Fr(1)
        for i in range(i0 + 1, 17): acc = add(acc, sc(ep[i], -K[i][n]))
        ep[i0] = acc
    for j in range(0, 10): e[j] = sc(ep[16 - j], Fr(7) ** (-(7 - 2 * (16 - j) + d // 2)))
    A = [aff(0) for _ in range(N + 1)]; B = [aff(0) for _ in range(N + 1)]
    for n in range(N + 1):
        for j in range(17):
            if K[j][n]: A[n] = add(A[n], sc(e[j], K[j][n])); B[n] = add(B[n], sc(ep[j], K[j][n]))
    assert A[0] == aff(1) and B[0] == aff(1) and all(A[n] == aff(0) for n in range(1, 7))
    return A, B


def build(d, low, extra=()):
    A, B = family(d); C = []
    for n in range(7, N + 1): C.append(("A_%d >= 0" % n, A[n]))
    C.append(("A_7 >= 72", add(A[7], aff(72), -1)))
    for n in range(1, N + 1): C.append(("B_%d >= %d" % (n, low.get(n, 0)), add(B[n], aff(low.get(n, 0)), -1)))
    for k in range(1, N // 7 + 1): C.append(("A_%d >= B_%d" % (7 * k, k), add(A[7 * k], B[k], -1)))
    C.append(("7(A_7-72)+8A_8 <= 55440", add(aff(55440 + 7 * 72), add(sc(A[7], 7), sc(A[8], 8)), -1)))
    for part in extra:
        if part.startswith("min:"):
            C.append(("A_7 <= 72", add(aff(72), A[7], -1)))
            for n in range(8, int(part[4:])): C.append(("A_%d <= 0" % n, sc(A[n], -1)))
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
    T.selfcheck(); TQ.selfcheck()
    A8 = a8_classes(8); assert A8[0][Fr(2)] == 72 and A8[0][Fr(4)] == 756 and A8[1][Fr(8, 9)] == 9 and A8[2][Fr(14, 9)] == 36 and A8[3][Fr(2)] == 84
    low = forced(9); print("forced numbers of vectors of Lam, norm 2n, n = 1..9: %s" % [low.get(n, 0) for n in range(1, 10)], flush=True)
    assert low[1] == 72 and low[2] == 756 + 1782
    ds = [int(x) for x in sys.argv[2:]] or list(range(30, 44, 2))
    for d in ds:
        Af, Bf, C = build(d, low); st = feasible(C)
        if st[0] == "infeasible": print("d = %d (r = %d): INFEASIBLE; certificate on: %s" % (d, d + 1, ", ".join(nm for nm, _ in st[1])), flush=True); continue
        lad = None
        for m in range(8, 16):
            if feasible(build(d, low, ("min:%d" % m,))[2])[0] == "infeasible": lad = 2 * (m - 1); break
        a7 = minimise(C, add(Af[7], aff(72), -1)); acc = add(Af[7], aff(72), -1); line = ""
        for m in range(8, 14):
            acc = add(acc, Af[m]); line += " N(<=%d) >= %s;" % (2 * m, X.show(minimise(C, acc)))
        print("d = %d (r = %d): feasible; ladder: a vector of L (or of a class t != 0) of norm <= %s; min a_7 = %s;%s" % (d, d + 1, lad, X.show(a7), line), flush=True)
