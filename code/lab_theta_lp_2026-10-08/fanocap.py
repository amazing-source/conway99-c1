"""C1, lab session, 2026-10-08. Effect of a stronger cap on the Fano vectors: a_7 <= CAP (default 3960).
  python fanocap.py <N> [CAP]
Claim behind CAP = 3960 (NOTE.md 17.10, hand argument, uses Lemma F): for a vertex p0 and four of its lines, two seeds
(p0; q1,q2,q3,q4) and (p0; q1,q2,q3,q4') that differ on one line only cannot both extend to a Fano vector; so at most 8 of
the 16 seeds of each (p0, four lines) extend, and a_7 <= 99 * 35 * 8 / 7 = 3960.
LP of r35.py / tradeoff35.py (b_4 >= 3826746 + 90 P - 4572 rho) with this extra constraint, for r = 35; and for the
other ranks the plain feasibility with rho = P = 0 bounds."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
import r35 as R
T.selfcheck(); CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 3960
for d in (34, 36, 38, 40, 42):
    A, B, C = R.build(d)
    C = [(nm, f) for nm, f in C if not nm.startswith("b_4 >= 3826746")]
    C.append(("b_4 >= 3826746 + 90 P - 4572 rho", R.add(B[4], R.lin(3826746, P=90, rho=-4572), -1)))
    C.append(("a_7 <= %d" % CAP, R.add(R.lin(CAP), A[7], -1)))
    st = R.feasible(C)
    if st[0] == "infeasible":
        m = min(l for _, l in st[1]); print("d = %d (r = %d), a_7 <= %d: INFEASIBLE for all P, rho. Certificate (multipliers / smallest):" % (d, d + 1, CAP))
        for nm, l in st[1]: print("      %-38s %s" % (nm, X.show(l / m)))
        continue
    lo, y = R.minimise(C, R.lin(0, rho=1)); lo2, y2 = R.minimise(C, R.lin(0, P=1)); a7, _ = R.minimise(C, A[7]); a8, _ = R.minimise(C, A[8])
    print("d = %d (r = %d), a_7 <= %d: feasible; min rho = %s (at P = %s); min P = %s; min a_7 = %s; min a_8 = %s" % (d, d + 1, CAP, X.show(lo), X.show(y[7]), X.show(lo2), X.show(a7), X.show(a8)), flush=True)
