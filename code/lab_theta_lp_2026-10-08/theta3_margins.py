"""C1, lab session, 2026-10-08. 3-side LP of theta3.py: MARGINS of the dual shells.

  python theta3_margins.py <N> <d> [m ...]

For the rank r = d + 1: the exact maximum of each dual shell B_m (number of vectors of norm 2m of sqrt7 E*, i.e. of classes
psi mod L with Q3(psi) + 7|n'|^2 = 2m) compatible with: theta_E in the span, B_0 = 1, all primal shell counts >= 0 with the
known zeros (class 0: nothing below norm 12; class c: nothing below 9|c|(1 - |c|/11)), the audited forced dual vectors
(norm 6: 1386, norm 8: 12474, norm 10: 182952, norm 14: 40), and A_(7m) >= B_m.
Why: on this side two representatives collide only through a vector of L (norm >= 14, at most 990 Fano vectors), so a
census of dense induced bipartite subgraphs (alternating 4-cycles and cubes at norm 8, dominoes at norm 10, 6-cycles at
norm 12, ...) gives clean lower bounds on the B_m; a proved B_m above the maximum printed here excludes the rank.
X.simplex(cols, c, g) maximises c.lambda subject to cols.lambda = g, lambda >= 0. One process, memory below 1 GB."""
import sys
from fractions import Fraction as Fr
import theta3 as H
import theta_lp_exact as X
N = H.N; H.test_toy(); H.test_fricke()
LOW = {3: 1386, 4: 12474, 5: 182952, 7: 40}
d = int(sys.argv[2]); ms = [int(x) for x in sys.argv[3:]] or [3, 4, 5, 6, 7, 8]
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
print("N = %d, d = %d (r = %d): %d shell unknowns, %d equations, %d inequalities" % (N, d, d + 1, nv, len(eqs), ns), flush=True)
for m in ms:
    cost = [B[m][1 + k] for k in range(nv)] + [Fr(0)] * ns
    res = X.simplex(cols, cost, rhs)
    if res[0] == "infeasible": print("  the system is INFEASIBLE", flush=True); break
    if res[0] != "optimal": print("  B_%d (norm %d): no finite maximum (%s); bound in use %d" % (m, 2 * m, res[0], LOW.get(m, 0)), flush=True); continue
    lam = res[2]; assert all(x >= 0 for x in lam) and all(sum(rows[r][k] * lam[k] for k in range(nv + ns)) == rhs[r] for r in range(len(rows)))
    val = B[m][0] + sum(B[m][1 + k] * lam[k] for k in range(nv))
    print("  B_%d (norm %d): maximum %s; bound in use %d" % (m, 2 * m, X.show(val), LOW.get(m, 0)), flush=True)
