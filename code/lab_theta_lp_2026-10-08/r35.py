"""C1, lab session, 2026-10-08. Rank 35 against the 6-subsets: exact LP in (b_1..b_7, P, rho).

  python r35.py <N> [d ...]

P = number of prisms (two triangles joined by a perfect matching), rho = number of induced 3 x 3 rook's graphs ("grids") of
the hypothetical srg(99,14,1,2); 0 <= 6 rho <= P <= 1386 (a grid contains 6 prisms, a prism lies in at most one grid, a
triangle lies in at most 12 prisms).
New lower bounds on the dual shells (NOTE.md, section 17; formulas tested by sixsets.py on k = 4 and k = 22):
  norm 8:  b_4 >= 1431738                      audited (Codex 172/173)
               + 731808 + 12 P                 1_T - 1_path, T a triangle, the path induced, no edge between them (class s = 0)
               + 2 (831600 + 36 P - 2286 rho)  +-1_W, W a 6-set with exactly 7 edges (class s = +-6)
  norm 6:  b_3 >= 24948 + 2 (20790 - 9 P - 36 rho)        +-1_W, W a 6-set with exactly 8 edges
The terms in rho are the only coincidences with the audited families: 1_W = e_z - 1_S or 1_W = -1_Y in M exactly when the
difference is the indicator of a grid (an integer vector phi with A phi = 3 phi + 1 and sum 9).
Other constraints as in margins.py: positivity, a_7k >= b_k, b_2 >= 462, b_5..b_8 of Codex's note 175,
7 a_7 + 8 a_8 <= 55440, b_1 <= 88. Exact rational simplex; every answer is re-verified (Farkas certificate or primal point)."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
NV = 9                                                                   # b_1..b_7, P, rho
LOW = {2: 462, 5: 18001368, 6: 86272956, 7: 208016424, 8: 263126556}


def ext(f): return list(f) + [Fr(0)] * (NV + 1 - len(f))
def lin(c, **kw):
    f = [Fr(c)] + [Fr(0)] * NV
    for k, v in kw.items(): f[{"P": 8, "rho": 9}[k]] = Fr(v)
    return f
def add(u, v, s=1): return [x + s * y for x, y in zip(u, v)]


def build(d, use_high=True):
    A, B, C = X.build(d, "ext"); A = [ext(f) for f in A]; B = [ext(f) for f in B]
    C = [(nm, ext(f)) for nm, f in C if not nm.startswith(("b_2 >=", "b_3 >=", "b_4 >=", "b_5 >="))]
    for n, lo in LOW.items():
        if n == 2 or use_high: C.append(("b_%d >= %d" % (n, lo), add(B[n], lin(lo), -1)))
    C.append(("b_3 >= 66528 - 18 P - 72 rho", add(B[3], lin(66528, P=-18, rho=-72), -1)))
    C.append(("b_4 >= 3826746 + 84 P - 4572 rho", add(B[4], lin(3826746, P=84, rho=-4572), -1)))
    C.append(("7 a_7 + 8 a_8 <= 55440", add(lin(55440), add([7 * x for x in A[7]], [8 * x for x in A[8]]), -1)))
    C.append(("b_1 <= 88", add(lin(88), B[1], -1)))
    C.append(("P >= 0", lin(0, P=1))); C.append(("rho >= 0", lin(0, rho=1)))
    C.append(("P <= 1386", lin(1386, P=-1))); C.append(("6 rho <= P", lin(0, P=1, rho=-6)))
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
    assert res[0] == "optimal", res[0]
    _, val, lam, y = res
    assert all(x >= 0 for x in lam) and all(sum(l * f[k] for l, (_, f) in zip(lam, C) if l) == form[k] for k in range(1, NV + 1))
    assert all(f[0] + sum(f[k] * y[k - 1] for k in range(1, NV + 1)) >= 0 for _, f in C)
    return form[0] + val, y


if __name__ == "__main__":
    T.selfcheck()
    for d in ([int(x) for x in sys.argv[2:]] or [34]):
        print("d = %d (r = %d)" % (d, d + 1), flush=True)
        for use_high in (True, False):
            A, B, C = build(d, use_high); tag = "with" if use_high else "WITHOUT"
            st = feasible(C + [("rho <= 0", lin(0, rho=-1))])
            if st[0] == "infeasible":
                m = min(l for _, l in st[1]); print("  no grid (rho = 0), %s b_5..b_8: INFEASIBLE for every P. Certificate (multipliers / smallest):" % tag)
                for nm, l in st[1]: print("      %-38s %s" % (nm, X.show(l / m)))
            else: print("  no grid (rho = 0), %s b_5..b_8: feasible" % tag)
            st = feasible(C)
            if st[0] == "infeasible": print("  any rho, %s b_5..b_8: INFEASIBLE" % tag, flush=True); continue
            lo, y = minimise(C, lin(0, rho=1)); print("  any rho, %s b_5..b_8: feasible; minimum of rho = %s (at P = %s)" % (tag, X.show(lo), X.show(y[7])), flush=True)
            if use_high:
                for Pv in (0, 100, 200, 300, 400, 500, 600, 800, 1000, 1200, 1386):
                    CP = C + [("P = %d (a)" % Pv, lin(-Pv, P=1)), ("P = %d (b)" % Pv, lin(Pv, P=-1))]
                    if feasible(CP)[0] == "infeasible": print("    P = %4d: INFEASIBLE" % Pv, flush=True)
                    else:
                        lo, _ = minimise(CP, lin(0, rho=1)); print("    P = %4d: needs rho >= %s (maximum possible %s)" % (Pv, X.show(lo), X.show(Fr(Pv, 6))), flush=True)
