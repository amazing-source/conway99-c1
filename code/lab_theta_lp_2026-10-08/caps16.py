"""C1, lab session. Consequences of the cap a_8 <= 90090 (laptop session's hand bound: at most 13 norm-16 configurations per
seed; to be refereed) together with a_7 <= 7920 and b_1 <= 3784, set "ext". Exact.   python caps16.py <N>"""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
for d in (32, 34, 36):
    A, B, C = X.build(d, "ext")
    C.append(("a_7 <= 7920", T.add(T.aff(7920), A[7], -1))); C.append(("b_1 <= 3784", T.add(T.aff(3784), B[1], -1))); C.append(("a_8 <= 90090", T.add(T.aff(90090), A[8], -1)))
    st = X.feasible(C)
    if st[0] == "infeasible": print("d = %d (r = %d): INFEASIBLE: %s" % (d, d + 1, ", ".join(nm for nm, _ in st[1])), flush=True); continue
    out = []
    for nm, f in (("a_7", A[7]), ("a_8", A[8]), ("a_9", A[9]), ("a_10", A[10]), ("a_7+a_9", T.add(A[7], A[9])), ("b_1", B[1])):
        lo = X.minimise(C, f); hi = X.minimise(C, T.sc(f, -1)); out.append("%s in [%s, %s]" % (nm, X.show(lo[1]), X.show(-hi[1]) if hi[0] == "min" else "+inf"))
    C0 = C + [("a_7 <= 0", T.sc(A[7], -1))]; s0 = X.feasible(C0)
    out.append("with a_7 = 0: %s" % ("feasible" if s0[0] == "feasible" else "INFEASIBLE (%s)" % ", ".join(nm for nm, _ in s0[1])))
    for cap9 in (0, 20000, 50000):
        C9 = C + [("a_9 <= %d" % cap9, T.add(T.aff(cap9), A[9], -1))]; s9 = X.feasible(C9)
        out.append("with a_9 <= %d: %s" % (cap9, "feasible" if s9[0] == "feasible" else "INFEASIBLE"))
    print("d = %d (r = %d): %s" % (d, d + 1, "; ".join(out)), flush=True)
