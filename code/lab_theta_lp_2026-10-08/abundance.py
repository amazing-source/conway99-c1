"""C1, lab session. Forced abundance of short vectors: exact LP minima under proved caps.

  python abundance.py <N>

Set "ext" of theta_lp_exact.py plus the caps
    a_7 <= 7920   (a Fano vector is determined by a vertex of P and its 4 neighbours in Q: 99 * 560 / 7)
    b_1 <= 3784   (the roots of the even lattice M form a root system of rank <= 44; the largest is D_44)
For each d = r - 1:
  (1) the minimum of a_8 (number of vectors of norm 16), and the minimum of a_8 when a_7 = 0;
  (2) for m = 8..13 the minimum of a_7 + a_8 + ... + a_m (number of non-zero vectors of L1 of norm <= 2m)."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
N = X.N
T.selfcheck()
for d in range(30, 44, 2):
    A, B, C = X.build(d, "ext")
    C.append(("a_7 <= 7920", T.add(T.aff(7920), A[7], -1))); C.append(("b_1 <= 3784", T.add(T.aff(3784), B[1], -1)))
    st = X.feasible(C)
    if st[0] == "infeasible": print("d = %2d (r = %2d): INFEASIBLE with the caps: %s" % (d, d + 1, ", ".join(nm for nm, _ in st[1])), flush=True); continue
    r1 = X.minimise(C, A[8]); C0 = C + [("a_7 <= 0", T.sc(A[7], -1))]; r0 = X.minimise(C0, A[8]) if X.feasible(C0)[0] == "feasible" else None
    line = "d = %2d (r = %2d): min a_8 = %s (with a_7 = 0: %s); min of a_7+..+a_m:" % (d, d + 1, X.show(r1[1]), X.show(r0[1]) if r0 else "infeasible")
    acc = T.aff(0)
    for m in range(7, 14):
        acc = T.add(acc, A[m]); rm = X.minimise(C, acc)
        if m >= 8: line += " m=%d: %s;" % (m, X.show(rm[1]))
    print(line, flush=True)
