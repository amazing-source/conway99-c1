"""C1, lab session, 2026-10-08. 3-side LP of theta3.py: MAXIMA of the shells of K3 (class 0), i.e. of the numbers of
integer 3-eigenvectors of norm 12, 14, 16, 18, 20. Twice the number of twin pairs of special supports of mass m is at
most N_0(2m), so an upper bound here would control the collisions of the dual families.

  python theta3_maxK3.py <N> <d> [capped]

Constraints as in theta3_margins.py; with "capped": N_0(12) <= 3780 (tau <= 1890), N_0(14) <= 3734 (pairs of D,
Omega <= H <= 1867), grids N_3(90/11) <= 126 (Codex's and my order-9/10 caps; exploration).
X.simplex(cols, c, g) maximises c.lambda subject to cols.lambda = g, lambda >= 0."""
import sys
from fractions import Fraction as Fr
import theta3 as H
import theta_lp_exact as X
N = H.N; H.test_toy(); H.test_fricke()
LOW = {3: 1386, 4: 12474, 5: 182952, 7: 40}
d = int(sys.argv[2]); capped = "capped" in sys.argv[3:]
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
def capvar(var, bound):
    f = [Fr(bound)] + [Fr(0)] * nv; f[1 + V.index(var)] = Fr(-1); return f
if capped: ineq += [capvar((0, Fr(12)), 3780), capvar((0, Fr(14)), 3734), capvar((3, Fr(90, 11)), 126)]
ns = len(ineq)
rows = [e[1:] + [Fr(0)] * ns for e in eqs]; rhs = [-e[0] for e in eqs]
for i, f in enumerate(ineq):
    r = f[1:] + [Fr(0)] * ns; r[nv + i] = Fr(-1); rows.append(r); rhs.append(-f[0])
cols = [[rows[r][k] for r in range(len(rows))] for k in range(nv + ns)]
print("N = %d, d = %d (r = %d), %s" % (N, d, d + 1, "capped" if capped else "no cap"), flush=True)
for nu in (12, 14, 16, 18, 20):
    cost = [Fr(0)] * (nv + ns); cost[V.index((0, Fr(nu)))] = Fr(1)
    res = X.simplex(cols, cost, rhs)
    print("  maximum of N_0(%d) (integer 3-eigenvectors of norm %d): %s" % (nu, nu, X.show(res[1]) if res[0] == "optimal" else res[0]), flush=True)
