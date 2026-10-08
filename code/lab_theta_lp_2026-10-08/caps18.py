"""C1, lab session. What a cap on the number of norm-18 vectors would give. Constraints as in top43.py (audited bounds,
Codex's exact small shells, 7 a_7 + 8 a_8 <= 55440, a_8 <= 6930, b_1 <= 88). For each d and each cap X on a_9:
feasible or not, and the exact range of a_13 (norm 26) and of a_10 + a_11 + a_12.     python caps18.py <N>"""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
for d in (34, 36, 38, 40, 42):
    A, B, C = X.build(d, "ext"); C = [c for c in C if not c[0].startswith(("b_4 >=", "b_5 >="))]
    for n, lo in ((4, 1431738), (5, 18001368), (6, 86272956), (7, 208016424)): C.append(("b_%d >= %d" % (n, lo), T.add(B[n], T.aff(lo), -1)))
    C.append(("7 a_7 + 8 a_8 <= 55440", T.add(T.aff(55440), T.add(T.sc(A[7], 7), T.sc(A[8], 8)), -1)))
    C.append(("b_1 <= 88", T.add(T.aff(88), B[1], -1)))
    mid = T.add(T.add(A[10], A[11]), A[12]); line = "d = %d (r = %d):" % (d, d + 1)
    for cap in (0, 1000, 10000, 100000, 1000000):
        Cc = C + [("a_9 <= %d" % cap, T.add(T.aff(cap), A[9], -1))]
        if X.feasible(Cc)[0] == "infeasible": line += " [a_9<=%d: INFEASIBLE]" % cap; continue
        lo13 = X.minimise(Cc, A[13])[1]; hi = X.minimise(Cc, T.sc(A[13], -1)); lom = X.minimise(Cc, mid)[1]
        line += " [a_9<=%d: a_13 in (%s, %s), a_10+a_11+a_12 >= %s]" % (cap, X.show(lo13), X.show(-hi[1]) if hi[0] == "min" else "+inf", X.show(lom))
    print(line, flush=True)
