"""C1, lab session, 2026-10-08. What rank 37 (and 39) needs on the short shells of L1, under WHAT-IF caps on a_8, a_9.
  python needs37.py <N> [d ...]
Constraints: r35.py with the twin-safe b_4, P and rho free, a_7 <= 990 (NOTE.md 17.10; pending audit). The caps on a_8
and a_9 tried below are hypothetical (a packing argument like the one for a_7 might give them): the output says what
each would force, not that it holds."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
import r35 as R
T.selfcheck()
for d in ([int(x) for x in sys.argv[2:]] or [36]):
    A, B, C = R.build(d)
    C = [(nm, f) for nm, f in C if not nm.startswith("b_4 >= 3826746")]
    C.append(("b_4 twin-safe", R.add(B[4], R.lin(3826746, P=-30, rho=-4572), -1))); C.append(("a_7 <= 990", R.add(R.lin(990), A[7], -1)))
    for c8, c9 in ((6930, None), (866, None), (866, 100000), (866, 20000), (866, 5000), (866, 1000), (0, 0)):
        Cc = C + [("a_8 cap", R.add(R.lin(c8), A[8], -1))] + ([("a_9 cap", R.add(R.lin(c9), A[9], -1))] if c9 is not None else [])
        if R.feasible(Cc)[0] == "infeasible": print("d = %d (r = %d), a_8 <= %s, a_9 <= %s: INFEASIBLE" % (d, d + 1, c8, c9), flush=True); continue
        out = []
        for n in range(9, 14): out.append("min a_%d = %s" % (n, X.show(R.minimise(Cc, A[n])[0])))
        s = R.lin(0)
        for n in range(10, 14): s = R.add(s, A[n])
        out.append("min a_10+..+a_13 = %s" % X.show(R.minimise(Cc, s)[0]))
        print("d = %d (r = %d), a_8 <= %s, a_9 <= %s: %s" % (d, d + 1, c8, c9, "; ".join(out)), flush=True)
