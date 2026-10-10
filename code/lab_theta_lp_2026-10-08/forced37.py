"""C1, lab session, 2026-10-10. Rank 37 (d = 36) with a_7 = 0 (lemma N14, NOTE 17.95): what the level-7 theta
programme forces on the numbers a_8, a_9, a_10 of integral (-4)-eigenvectors of norm 16, 18, 20 (both signs counted).
Exact rational simplex of theta_lp_exact.py; the dual solution of each minimisation is re-verified and printed as an
inequality valid on the whole polytope.

  python forced37.py <N> [mode]        mode = ext (default, the audited rows of NOTE section 2) | ext2 | ext3
One process, a minute or two."""
import sys
from fractions import Fraction as Fr
import theta_lp_exact as X
T = X.T
mode = sys.argv[2] if len(sys.argv) > 2 else "ext"
T.selfcheck()
A, B, C0 = X.build(36, mode + "+a7")
print("d = 36 (r = 37), mode %s with a_7 <= 0 (so b_1 = 0 by a_7 >= b_1), N = %d" % (mode, X.N))

def lp(extra, form, what):
    """minimise the affine form; print the value and the dual inequality on a_8, a_9, a_10"""
    C = C0 + extra
    res = X.simplex([f[1:] for _, f in C], [-f[0] for _, f in C], form[1:])
    if res[0] != "optimal": print("%s: %s" % (what, "INFEASIBLE" if res[0] == "unbounded" else res[0])); return None
    _, val, lam, y = res
    assert all(x >= 0 for x in lam) and all(sum(l * f[k] for l, (_, f) in zip(lam, C)) == form[k] for k in range(1, 8))
    assert all(f[0] + sum(f[k] * y[k - 1] for k in range(1, 8)) >= 0 for _, f in C)
    value = form[0] + val
    # form = sum lam_i f_i (linear parts); so form(beta) = sum lam_i (f_i(beta) - f_i[0]) + form[0] >= form[0] - sum lam_i f_i[0] = value
    assert form[0] - sum(l * f[0] for l, (_, f) in zip(lam, C)) == value
    used = [(C[i][0], lam[i]) for i in range(len(C)) if lam[i]]
    print("%s: minimum %s   (%.3f)" % (what, value, float(value)))
    print("      dual support: " + ", ".join("%s [%s]" % (nm, l) for nm, l in used))
    return value, dict(used)

a8, a9, a10 = A[8], A[9], A[10]
zero = lambda n: ("a_%d <= 0" % n, T.sc(A[n], -1))
lp([], T.add(T.add(a8, a9, 1), a10, 1), "min a_8 + a_9 + a_10")
r10 = lp([zero(8), zero(9)], a10, "min a_10 when a_8 = a_9 = 0")
r9 = lp([zero(8), zero(10)], a9, "min a_9 when a_8 = a_10 = 0")
r8 = lp([zero(9), zero(10)], a8, "min a_8 when a_9 = a_10 = 0")
if r10:
    v, du = r10; m8 = du.get("a_8 <= 0", Fr(0)); m9 = du.get("a_9 <= 0", Fr(0))
    print("valid inequality at rank 37 with a_7 = 0 (from the dual of the second programme):")
    print("      a_10 + (%s) a_9 + (%s) a_8 >= %s        i.e. a_10 + %.4f a_9 + %.4f a_8 >= %.3f" % (m9, m8, v, float(m9), float(m8), float(v)))
    # check that it is tight on the three axes
    w = T.add(T.add(a10, T.sc(a9, m9), 1), T.sc(a8, m8), 1)
    lp([], w, "check: minimum of that combination over the whole polytope")
