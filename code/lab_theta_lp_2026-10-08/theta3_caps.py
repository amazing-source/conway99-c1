"""C1, lab session. 3-side LP of theta3.py with two more constraints from Codex's note 174:
  G = N_3(90/11) <= 231 (number of 3 x 3 grids),  and  A_(7m) >= B_m for 7m <= N (sqrt7 E^sharp inside E).
Audited forced dual vectors only (norm 6: 1386, norm 8: 12474, norm 10: 182952).     python theta3_caps.py <N> [d ...]"""
import sys
from fractions import Fraction as Fr
import theta3 as H
import theta_lp_exact as X
N = H.N; H.test_toy(); H.test_fricke()
LOW = {3: 1386, 4: 12474, 5: 182952}


_CACHE = {}
def system2(d):
    if d not in _CACHE: _CACHE[d] = _system2(d)
    return _CACHE[d]


def _system2(d):
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
    eqs = []                                                             # (affine form == 0)
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
    one = [Fr(1)] + [Fr(0)] * nv
    eqs.append(add(B[0], one, -1))
    ineq = [add(B[m], [Fr(LOW.get(m, 0))] + [Fr(0)] * nv, -1) for m in range(1, N + 1)]          # >= 0
    ineq += [add(A(7 * m), B[m], -1) for m in range(1, N // 7 + 1)]
    g = [Fr(231)] + [Fr(0)] * nv; g[1 + V.index((3, Fr(90, 11)))] = Fr(-1); ineq.append(g)        # 231 - G >= 0
    return V, eqs, ineq


def solve2(d, zero=(), objective=None):
    V, eqs, ineq = system2(d); nv = len(V); ns = len(ineq)
    rows = [e[1:] + [Fr(0)] * ns for e in eqs]; rhs = [-e[0] for e in eqs]
    for i, f in enumerate(ineq):
        r = f[1:] + [Fr(0)] * ns; r[nv + i] = Fr(-1); rows.append(r); rhs.append(-f[0])
    keep = [k for k in range(nv + ns) if not (k < nv and V[k] in zero)]
    cols = [[rows[r][k] for r in range(len(rows))] for k in keep]
    cost = [Fr(-1) if (objective is not None and k < nv and V[k] in objective) else Fr(0) for k in keep]
    res = X.simplex(cols, cost, rhs)
    if res[0] != "optimal": return (res[0],)
    lam = res[2]; assert all(x >= 0 for x in lam) and all(sum(rows[r][k] * lam[i] for i, k in enumerate(keep)) == rhs[r] for r in range(len(rows)))
    return ("feasible", -res[1], {V[k]: lam[i] for i, k in enumerate(keep) if k < nv and lam[i]})


V = H.variables(); nus = sorted({v[1] for v in V})
for d in ([int(x) for x in sys.argv[2:]] or [34, 38, 42]):
    if solve2(d)[0] != "feasible": print("d = %d (r = %d): INFEASIBLE" % (d, d + 1), flush=True); continue
    lad = None
    for t in [x for x in nus if x >= 18]:                                # earlier runs: nothing is forced below 18
        if solve2(d, zero={v for v in V if v[1] < t})[0] != "feasible": break
        lad = t
    r20 = solve2(d, objective={v for v in V if v[1] < 21}); rg = solve2(d, objective={(3, Fr(90, 11))})
    print("d = %d (r = %d): feasible; shells nu < %s may all be empty, nu <= %s not; N(nu<21) >= %.6g; min G = %s" % (d, d + 1, lad, lad, float(r20[1]), X.show(rg[1])), flush=True)
