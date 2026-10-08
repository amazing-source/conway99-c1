"""C1, lab session, 2026-10-08. Robustness of the rank-35 exclusion to its ingredients (exact LP, d = 34 only).
  python fanocap3.py <N>
Variants of the b_4 bound: FULL = 3826746 - 30 P - 4572 rho (Codex's twin-safe version); NO-PATH = without the family
triangle minus far path: 3094938 + 78 P - 4572 rho; and of the b_3 bound (with / without the 6-sets with 8 edges).
For each, the largest cap on a_7 (among the listed values) for which rank 35 is infeasible for all P, rho."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
import r35 as R
T.selfcheck()
A, B, C0 = R.build(34)
C0 = [(nm, f) for nm, f in C0 if not nm.startswith(("b_4 >= 3826746", "b_3 >= 66528"))]
B3 = {"b_3 six-sets": R.lin(66528, P=-18, rho=-72), "b_3 audited only": R.lin(24948)}
B4 = {"b_4 FULL": R.lin(3826746, P=-30, rho=-4572), "b_4 NO-PATH": R.lin(3094938, P=78, rho=-4572), "b_4 audited only": R.lin(1431738)}
for n3, f3 in B3.items():
    for n4, f4 in B4.items():
        C = C0 + [(n3, R.add(B[3], f3, -1)), (n4, R.add(B[4], f4, -1))]; res = []
        for cap in (990, 1500, 1980, 2500, 3000, 3500, 3960):
            res.append("%d:%s" % (cap, "INFEASIBLE" if R.feasible(C + [("cap", R.add(R.lin(cap), A[7], -1))])[0] == "infeasible" else "feasible"))
        print("%-18s %-18s  a_7 cap -> %s" % (n3, n4, "  ".join(res)), flush=True)
