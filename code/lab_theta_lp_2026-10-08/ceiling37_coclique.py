"""C1, lab session, 2026-10-08. Rank 37 ceilings under the coclique results (what-if table, exact rational simplex).
  python ceiling37_coclique.py <N> [d]
Base constraints as in ceiling37_lap.py (Codex's dual lower bounds, seed cap 7 a_7 + 8 a_8 <= 55440). Rows:
  a_7 <= 842 (Codex, certified census bound), b_1 <= 44 (Codex, from the 22-cocliques of the roots), the laptop
  session's root cut a_7 + 4 b_1 <= 990 (not audited), and the what-if a_7 = 0 ("no 22-coclique": every Fano vector
  contains two of them, laptop session). Prints max b_4 and max b_4 + (651/34) b_3."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
d = int(sys.argv[2]) if len(sys.argv) > 2 else 36
A, B, C0 = X.build(d, "ext"); C0 = [c for c in C0 if not c[0].startswith(("b_2 >=", "b_3 >=", "b_4 >=", "b_5 >="))]
for n, lo in {2: 462, 3: 45528, 4: 3371634, 5: 34087368, 6: 86272956, 7: 208016424, 8: 263126556}.items(): C0.append(("b_%d >= %d" % (n, lo), T.add(B[n], T.aff(lo), -1)))
C0.append(("cap", T.add(T.aff(55440), T.add(T.sc(A[7], 7), T.sc(A[8], 8)), -1)))
def le(c0, terms):
    f = T.aff(c0)
    for coef, form in terms: f = T.add(f, T.sc(form, -coef))
    return f
rows = (("a_7 <= 842, b_1 <= 44", [("a", le(842, [(1, A[7])])), ("b", le(44, [(1, B[1])]))]),
        ("  + a_7 + 4 b_1 <= 990", [("a", le(842, [(1, A[7])])), ("b", le(44, [(1, B[1])])), ("L1", le(990, [(1, A[7]), (4, B[1])]))]),
        ("what-if a_7 = 0 (then b_1 = 0)", [("a", le(0, [(1, A[7])])), ("b", le(0, [(1, B[1])]))]))
print("d = %d (r = %d)" % (d, d + 1))
for nm, extra in rows:
    C = C0 + extra
    if X.feasible(C)[0] == "infeasible": print("%-32s INFEASIBLE" % nm, flush=True); continue
    r1 = X.minimise(C, T.sc(B[4], -1))
    r2 = X.minimise(C, T.sc(T.add(B[4], T.sc(B[3], Fr(651, 34))), -1)); y2 = r2[2]; ev2 = lambda f: f[0] + sum(f[k] * y2[k - 1] for k in range(1, 8))
    print("%-32s max b_4 = %s; max b_4 + (651/34) b_3 = %s [there: a_7 = %s, a_8 = %s, a_9 = %s, a_13 = %s, b_1 = %s]" % (
        nm, X.show(-r1[1]), X.show(-r2[1]), X.show(ev2(A[7])), X.show(ev2(A[8])), X.show(ev2(A[9])), X.show(ev2(A[13])), X.show(ev2(B[1]))), flush=True)
