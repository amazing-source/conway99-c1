"""C1, lab session, 2026-10-08. 3-side LP of theta3.py: the MAXIMUM of G = N_3(90/11), the number of induced 3 x 3 grids.

  python theta3_maxG.py <N> <d>

A grid R gives kappa = 1_R with (A - 3I) kappa = 1 and |kappa|^2 = 9: the vectors of the class c = 1 of projected norm
9 - 9/11 = 90/11, and conversely (sixsets.py / NOTE.md section 17). The (-4)-side LP of r35.py shows that rank 35 needs
G >= 43; this script asks the 3-side LP for an upper bound. Constraints: theta_E in the span, B_0 = 1, the audited forced
dual vectors (norm 6: 1386, norm 8: 12474, norm 10: 182952), A_(7m) >= B_m, all shell counts >= 0. No cap on G is imposed.
X.simplex(cols, c, g) MAXIMISES c.lambda subject to cols.lambda = g, lambda >= 0. One process, memory below 1 GB."""
import sys
from fractions import Fraction as Fr
import theta3 as H
import theta_lp_exact as X
N = H.N; H.test_toy(); H.test_fricke()
LOW = {3: 1386, 4: 12474, 5: 182952}
d = int(sys.argv[2])
PH = H.phis(3, 2 * N); V = H.variables(); nv = len(V)
base = [PH[0].get(Fr(2 * n), 0) for n in range(N + 1)]
col = [[(1 if j == 0 else 2) * PH[j].get(Fr(2 * n) - nu, 0) for n in range(N + 1)] for (j, nu) in V]
A = lambda n: [Fr(base[n])] + [Fr(col[v][n]) for v in range(nv)]
add = lambda u, w, s=1: [x + s * y for x, y in zip(u, w)]
c = [None] * 21
for n in range(21):
    j = 20 - n; acc = A(n)
    for i in range(j + 1, 21):
        if H.F30[i][n]: acc = add(acc, c[i], -H.F30[i][n])
    c[j] = acc
eqs = []
for n in range(21, N + 1):
    acc = A(n)
    for i in range(21):
        if H.F30[i][n]: acc = add(acc, c[i], -H.F30[i][n])
    eqs.append(acc)
B = []
for m in range(N + 1):
    acc = [Fr(0)] * (nv + 1)
    for j in range(21):
        fj = H.F30[20 - j][m]
        if fj: acc = add(acc, c[j], Fr(7) ** (2 * j - 35 + d // 2) * fj)
    B.append(acc)
eqs.append(add(B[0], [Fr(1)] + [Fr(0)] * nv, -1))
ineq = [add(B[m], [Fr(LOW.get(m, 0))] + [Fr(0)] * nv, -1) for m in range(1, N + 1)]
ineq += [add(A(7 * m), B[m], -1) for m in range(1, N // 7 + 1)]
ns = len(ineq)
rows = [e[1:] + [Fr(0)] * ns for e in eqs]; rhs = [-e[0] for e in eqs]
for i, f in enumerate(ineq):
    r = f[1:] + [Fr(0)] * ns; r[nv + i] = Fr(-1); rows.append(r); rhs.append(-f[0])
cols = [[rows[r][k] for r in range(len(rows))] for k in range(nv + ns)]
g = V.index((3, Fr(90, 11)))
print("N = %d, d = %d (r = %d): %d shell unknowns, %d equations, %d inequalities" % (N, d, d + 1, nv, len(eqs), ns), flush=True)
for sign, what in ((1, "maximum"), (-1, "minimum")):
    cost = [Fr(0)] * (nv + ns); cost[g] = Fr(sign)
    res = X.simplex(cols, cost, rhs)
    if res[0] != "optimal": print("  %s of G: %s" % (what, res[0]), flush=True); continue
    lam = res[2]; assert all(x >= 0 for x in lam) and all(sum(rows[r][k] * lam[k] for k in range(nv + ns)) == rhs[r] for r in range(len(rows)))
    assert lam[g] == sign * res[1]
    print("  %s of G = %s  (attained by a re-verified feasible point; optimality is the simplex's claim)" % (what, X.show(lam[g])), flush=True)
