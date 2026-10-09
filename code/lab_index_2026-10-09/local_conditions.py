"""C1, lab session, 2026-10-09. Local (Hasse-Witt) conditions for the ball of a line of an srg(99,14,1,2).

For a line T with connected near graph G (cubic, 36 points), H = 3I - G:
  W- = span of the projections of the 36 near points on the (-4)-eigenspace V-, Gram (1/7)(H + J/9);
  W3 = same on the 3-eigenspace V3, Gram (1/7)(4I + G - (2/11) J);
  X- = orthogonal complement of W- in V- (dimension 8)  = Q-span of the integral (-4)-eigenvectors supported on the
       60 far vertices (lattice Lambda-, even, det = 4 * 7^(2k) * tau / (9 j^2), rank of A - 3I mod 7 = 37 + 2k);
  X3 = complement of W3 in V3 (dimension 18), lattice Lambda3, even, det = 5 * 7^(2k) * Theta / (256 j'^2),
       Theta = det(4I + G) / 7.
Rational invariants (c_p = Hasse invariant prod_{i<j} (a_i, a_j)_p):
  V-: d = 1,  c_2 = c_7 = -1, c_p = 1 otherwise;     V3: d = 11, c_7 = c_11 = -1, c_p = 1 otherwise.
  X-: d = tau,  c_p(X-) = c_p(V-) c_p(W-) (tau, -1)_p;   X3: d = 5 Theta, c_p(X3) = c_p(V3) c_p(W3) (55 Theta, 5 Theta)_p.
Conditions tested (a lattice that is unimodular at p needs c_p = 1 for odd p; an even unimodular 2-adic lattice of
rank 18 is H^9 or H^8 + A):
  A3 : v_3(tau) = 2            ->  c_3(X-) = 1
  A7 : 7 does not divide tau   ->  c_7(X-) = 1    (rank 37 only; should be 'tau is a non-residue mod 7')
  B11: 11 does not divide Theta->  c_11(X3) = 1
  B7 : 7 does not divide tau   ->  c_7(X3) = 1    (rank 37 only; same as A7)
  B2 : v_2(Theta) = 8          ->  c_2(X3) = c_2 of the even unimodular lattice of determinant 5 Theta / 256 mod 8
  control: at p = 13 (when 13 divides neither tau nor Theta) both c_13 must be 1 automatically.
python local_conditions.py <seed> <balls> [tri]      One process, a few MB."""
import random, sys, collections
from tau_theta_valuations import ball, val


def minors(M):
    """leading principal minors D_1..D_n of an integer symmetric positive definite matrix (Bareiss, no pivoting)"""
    n = len(M); M = [r[:] for r in M]; prev = 1; D = []
    for k in range(n):
        assert M[k][k] > 0
        D.append(M[k][k])
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return D


def legendre(a, p):
    a %= p
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def hilbert(a, b, p):
    """Hilbert symbol (a, b)_p for non-zero integers (or rationals given as integers up to squares)"""
    al = val(a, p); be = val(b, p); u = a // p ** al; v = b // p ** be
    if p == 2:
        e = lambda x: ((x - 1) // 2) % 2
        w = lambda x: ((x * x - 1) // 8) % 2
        return -1 if (e(u) * e(v) + al * w(v) + be * w(u)) % 2 else 1
    s = 1
    if al % 2 and be % 2 and p % 4 == 3: s = -s
    if be % 2: s *= legendre(u, p)
    if al % 2: s *= legendre(v, p)
    return s


def hasse(D, p):
    """Hasse invariant of the form with leading minors D: prod_j (D_j, -D_(j+1))_p"""
    c = 1
    for j in range(len(D) - 1): c *= hilbert(D[j], -D[j + 1], p)
    return c


def hasse_diag(diag, p):
    c = 1
    for i in range(len(diag)):
        for j in range(i + 1, len(diag)): c *= hilbert(diag[i], diag[j], p)
    return c


def invariants(A):
    n = 36
    Mm = [[9 * ((3 if i == j else 0) - A[i][j]) + 1 for j in range(n)] for i in range(n)]            # 9 (H + J/9)
    M3 = [[11 * ((4 if i == j else 0) + A[i][j]) - 2 for j in range(n)] for i in range(n)]           # 11 (4I + G - 2J/11)
    Dm = minors(Mm); D3 = minors(M3)
    tau = Dm[-1] // (9 ** 36 * 144); assert Dm[-1] == 9 ** 36 * 144 * tau
    theta = D3[-1] // (11 ** 35 * 5); assert D3[-1] == 11 ** 35 * 5 * theta
    return tau, theta, Dm, D3


def c_Xminus(tau, Dm, p):
    cW = hilbert(7, Dm[-1], p) * hasse(Dm, p)                 # W- = 7 * (9H + J) up to squares
    cV = -1 if p in (2, 7) else 1
    return cV * cW * hilbert(tau, -1, p)


def c_X3(theta, D3, p):
    cW = hilbert(77, D3[-1], p) * hasse(D3, p)                # W3 = 77 * (44 I + 11 G - 2J) up to squares
    cV = -1 if p in (7, 11) else 1
    return cV * cW * hilbert(55 * theta, 5 * theta, p)


# even unimodular 2-adic lattices of rank 18: H = <1,-1>, A = <2,6> over Q_2
C2_H9 = hasse_diag([1, -1] * 9, 2)
C2_H8A = hasse_diag([1, -1] * 8 + [2, 6], 2)

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1])); NB = int(sys.argv[2]); allow3 = len(sys.argv) > 3
    st = collections.Counter(); n = 0
    while n < NB:
        b = ball(rng, True, allow3)
        if b is None: continue
        A = b[0]; n += 1
        tau, theta, Dm, D3 = invariants(A)
        if tau % 13 and theta % 13:
            st[("control p=13", c_Xminus(tau, Dm, 13), c_X3(theta, D3, 13))] += 1
        if val(tau, 3) == 2: st[("A3: c_3(X-)", c_Xminus(tau, Dm, 3))] += 1
        else: st[("A3 not applicable, v_3(tau) parity %d: c_3(X-)" % (val(tau, 3) % 2), c_Xminus(tau, Dm, 3))] += 1
        if tau % 7:
            st[("A7: c_7(X-) and (tau|7)", c_Xminus(tau, Dm, 7), legendre(tau, 7))] += 1
            st[("B7: c_7(X3) and (tau|7)", c_X3(theta, D3, 7), legendre(tau, 7))] += 1
        if theta % 11: st[("B11: c_11(X3), (Theta|11)", c_X3(theta, D3, 11), legendre(theta, 11))] += 1
        v2 = val(theta, 2)
        if v2 == 8:
            d = (5 * (theta >> 8)) % 8; want = C2_H9 if d == 7 else C2_H8A
            st[("B2: det mod 8 = %d, c_2(X3) %s expected" % (d, "=" if c_X3(theta, D3, 2) == want else "!="),)] += 1
        st[("c_2(X-) with v_2(tau) = %d" % min(val(tau, 2), 3), c_Xminus(tau, Dm, 2), tau // 2 ** val(tau, 2) % 8)] += 1
    print("balls", n, "| c_2(H^9) =", C2_H9, " c_2(H^8+A) =", C2_H8A)
    for k_, v_ in sorted(st.items(), key=lambda t: str(t[0])): print("  ", k_, v_)
