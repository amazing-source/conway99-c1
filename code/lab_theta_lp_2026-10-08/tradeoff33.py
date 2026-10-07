"""C1, lab session. r = 33 (d = 32): exact minimum of a_9, and of a_9 + a_10, for several caps on a_7, with a_8 <= 27720,
b_1 <= 3784, set "ext".   python tradeoff33.py <N>"""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
A, B, C0 = X.build(32, "ext")
C0.append(("b_1 <= 3784", T.add(T.aff(3784), B[1], -1))); C0.append(("a_8 <= 27720", T.add(T.aff(27720), A[8], -1)))
for cap7 in (7920, 4000, 2000, 1000, 500, 200, 94):
    C = C0 + [("a_7 <= %d" % cap7, T.add(T.aff(cap7), A[7], -1))]
    if X.feasible(C)[0] == "infeasible": print("a_7 <= %d: INFEASIBLE" % cap7, flush=True); continue
    m9 = X.minimise(C, A[9]); m910 = X.minimise(C, T.add(A[9], A[10])); m10 = X.minimise(C, A[10]); M9 = X.minimise(C, T.sc(A[9], -1))
    print("a_7 <= %5d: min a_9 = %s; min a_10 = %s; min (a_9 + a_10) = %s; max a_9 = %s" % (cap7, X.show(m9[1]), X.show(m10[1]), X.show(m910[1]), X.show(-M9[1]) if M9[0] == "min" else "+inf"), flush=True)
