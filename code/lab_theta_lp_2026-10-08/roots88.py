"""C1, lab session. Effect of the cap b_1 <= 88 (the roots of M are pairwise orthogonal: two Fano vectors never differ by a
Fano vector; NOTE.md section 14) on the exact LP. Constraints as in top43.py.   python roots88.py <N> [d ...]"""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
for d in ([int(x) for x in sys.argv[2:]] or [42, 40, 38, 36, 34]):
    A, B, C = X.build(d, "ext"); C = [c for c in C if not c[0].startswith(("b_4 >=", "b_5 >="))]
    for n, lo in ((4, 1431738), (5, 18001368), (6, 86272956), (7, 208016424)): C.append(("b_%d >= %d" % (n, lo), T.add(B[n], T.aff(lo), -1)))
    C.append(("7 a_7 + 8 a_8 <= 55440", T.add(T.aff(55440), T.add(T.sc(A[7], 7), T.sc(A[8], 8)), -1)))
    S = T.aff(0)
    for n in range(8, 14): S = T.add(S, A[n])
    before = X.minimise(C, S)[1]; a7max0 = -X.minimise(C, T.sc(A[7], -1))[1]
    C.append(("b_1 <= 88", T.add(T.aff(88), B[1], -1)))
    if X.feasible(C)[0] == "infeasible": print("d = %d (r = %d): INFEASIBLE with b_1 <= 88" % (d, d + 1), flush=True); continue
    after = X.minimise(C, S)[1]; a7max = -X.minimise(C, T.sc(A[7], -1))[1]; a7min = X.minimise(C, A[7])[1]
    lad = None
    for m in range(8, 16):
        if X.feasible(C + [("a_%d <= 0" % n, T.sc(A[n], -1)) for n in range(7, m)])[0] == "infeasible": lad = 2 * (m - 1); break
    print("d = %d (r = %d): min(a_8+..+a_13): %s -> %s with b_1 <= 88; a_7 in [%s, %s] (max was %s); ladder %s" % (d, d + 1, X.show(before), X.show(after), X.show(a7min), X.show(a7max), X.show(a7max0), lad), flush=True)
