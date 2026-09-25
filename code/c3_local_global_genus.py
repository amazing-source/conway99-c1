"""notes/113 R1 — local vs global genus test (C3's "two lattices" step, without symmetry).

Lambda_theta contains K_theta(x) ⊥ S_theta(x), where K_theta(x) = Lambda_theta ∩ Z^{Γ2(x)} (L17) and S_theta(x) is its
orthogonal complement. span_Z{E_theta e_y : y ∈ B1(x)} ⊆ S^# has full rank, so its Gram (E_theta restricted to the
windmill) fixes v_p(det S) mod 2 and the unit class of det S at p = 7.
Expected if everything is consistent:
  theta = 3  : v11 odd (= v11 det Lambda_3 = 1, since L17's K_3 is 11-free), v7 = -14 (no 7-glue), (unit|7) = +1;
  theta = -4 : v7 = -14, (unit|7) = +1 (oddity: delta_V ≡ delta_VK ≡ k/2, so delta_VS must be 0).
"""
import sympy as sp

n = 15                                    # 0 = x, 1..14 = N(x), mates (2c+1, 2c+2)
A = sp.zeros(n, n)
for i in range(1, n):
    A[0, i] = A[i, 0] = 1
for c in range(7):
    A[1 + 2 * c, 2 + 2 * c] = A[2 + 2 * c, 1 + 2 * c] = 1
I, J = sp.eye(n), sp.ones(n, n)


def report(name, E):
    cols = []
    for j in range(n):
        if E.extract(list(range(n)), cols + [j]).rank() > len(cols):
            cols.append(j)
    d = sp.nsimplify(E.extract(cols, cols).det())
    num, den = sp.fraction(d)
    f = {p: e for p, e in sp.factorint(num).items()}
    for p, e in sp.factorint(den).items():
        f[p] = f.get(p, 0) - e
    unit = d / sp.Integer(7) ** f.get(7, 0)
    un, ud = sp.fraction(unit)
    leg = sp.legendre_symbol(int(un) % 7, 7) * sp.legendre_symbol(int(ud) % 7, 7)
    print(f"{name}: rank {len(cols)}, det Gram = {f}, v7 = {f.get(7, 0)}, v11 = {f.get(11, 0)}, (unit|7) = {int(leg):+d}")
    return f, leg


f3, l3 = report("theta = 3 ", (A + 4 * I) / 7 - sp.Rational(2, 77) * J)
f4, l4 = report("theta = -4", (3 * I - A) / 7 + J / 63)
assert f3.get(11, 0) % 2 == 1 and f3.get(7) == -14 and l3 == 1
assert f4.get(7) == -14 and l4 == 1
print("consistent at 7 and 11 on both sides: no local-global genus contradiction")
