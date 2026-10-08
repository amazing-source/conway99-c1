"""C1, lab session, 2026-10-08. Rank 37 (and others): the ceiling of b_4 and what the optimum uses on the L1 side.
  python ceiling37.py <N> [d]
Constraints: positivity, a_7k >= b_k, b_2 >= 462, b_3 >= 43848, b_4 >= 3371634, b_5 >= 34087368 (Codex's uniform
bounds on distinct vectors, note 182), its note-175 b_6..b_8, 7a_7 + 8a_8 <= 55440, a_7 <= 990, b_1 <= 88.
For each WHAT-IF set of extra caps on a_8, a_9, ... (hypothetical, to see which L1-side caps would lower the ceiling):
the exact maximum of b_4 and of b_4 + (651/34) b_3, and the values of a_7..a_13, b_1..b_3 at the first optimum."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
d = int(sys.argv[2]) if len(sys.argv) > 2 else 36
A, B, C0 = X.build(d, "ext"); C0 = [c for c in C0 if not c[0].startswith(("b_2 >=", "b_3 >=", "b_4 >=", "b_5 >="))]
for n, lo in {2: 462, 3: 43848, 4: 3371634, 5: 34087368, 6: 86272956, 7: 208016424, 8: 263126556}.items(): C0.append(("b_%d >= %d" % (n, lo), T.add(B[n], T.aff(lo), -1)))
C0.append(("cap", T.add(T.aff(55440), T.add(T.sc(A[7], 7), T.sc(A[8], 8)), -1))); C0.append(("b_1 <= 88", T.add(T.aff(88), B[1], -1)))
C0.append(("a_7 <= 990", T.add(T.aff(990), A[7], -1)))
def cap(n, v): return ("a_%d <= %d" % (n, v), T.add(T.aff(v), A[n], -1))
def capb(n, v): return ("b_%d <= %d" % (n, v), T.add(T.aff(v), B[n], -1))
variants = [("no extra cap", []), ("b_1 = 0", [capb(1, 0)]), ("b_1 = 0, a_8 <= 866", [capb(1, 0), cap(8, 866)]), ("a_7 <= 500", [cap(7, 500)]), ("a_7 <= 500, a_8 <= 866", [cap(7, 500), cap(8, 866)]),
            ("a_7 <= 250, b_1 = 0, a_8 <= 866", [cap(7, 250), capb(1, 0), cap(8, 866)]), ("a_7 = 0", [cap(7, 0)]), ("a_8 <= 866", [cap(8, 866)]), ("a_7 = 0 and a_8 <= 866", [cap(7, 0), cap(8, 866)]), ("a_8 <= 866, a_9 <= 20000", [cap(8, 866), cap(9, 20000)]),
            ("a_11 <= 100000", [cap(11, 100000)]), ("a_12 <= 100000", [cap(12, 100000)]), ("a_11, a_12 <= 100000", [cap(11, 100000), cap(12, 100000)]),
            ("a_11, a_12 <= 100000 and a_8 <= 866", [cap(11, 100000), cap(12, 100000), cap(8, 866)])]
print("d = %d (r = %d)" % (d, d + 1))
for nm, extra in variants:
    C = C0 + extra
    if X.feasible(C)[0] == "infeasible": print("%-40s INFEASIBLE" % nm, flush=True); continue
    r1 = X.minimise(C, T.sc(B[4], -1)); y = r1[2]; ev = lambda f: f[0] + sum(f[k] * y[k - 1] for k in range(1, 8))
    r2 = X.minimise(C, T.sc(T.add(B[4], T.sc(B[3], Fr(651, 34))), -1))
    print("%-40s max b_4 = %s; max b_4 + (651/34) b_3 = %s; at the first optimum: %s; b_1 = %s, b_2 = %s, b_3 = %s" % (
        nm, X.show(-r1[1]), X.show(-r2[1]), ", ".join("a_%d = %s" % (n, X.show(ev(A[n]))) for n in range(7, 14)), X.show(ev(B[1])), X.show(ev(B[2])), X.show(ev(B[3]))), flush=True)
