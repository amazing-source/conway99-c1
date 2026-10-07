"""C1, lab session. Forced numbers of short vectors under set "ext3" and the caps a_7 <= 7920, b_1 <= 3784, a_8 <= 27720.
  python abundance3.py <N>          exact minima, d = 34..42"""
import sys
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
for d in range(34, 44, 2):
    A, B, C = X.build(d, "ext3+caps"); st = X.feasible(C)
    if st[0] == "infeasible": print("d = %d (r = %d): INFEASIBLE: %s" % (d, d + 1, ", ".join(nm for nm, _ in st[1])), flush=True); continue
    line = "d = %d (r = %d):" % (d, d + 1); acc = T.aff(0)
    for m in range(7, 14):
        acc = T.add(acc, A[m])
        if m >= 9: line += " N(<=%d) >= %s;" % (2 * m, X.show(X.minimise(C, acc)[1]))
    line += " min a_9 = %s; min a_10 = %s; min a_11 = %s" % tuple(X.show(X.minimise(C, A[n])[1]) for n in (9, 10, 11))
    for m in range(9, 15):
        Cm = C + [("a_%d <= 0" % n, T.sc(A[n], -1)) for n in range(7, m)]
        if X.feasible(Cm)[0] == "infeasible": line += "; min(L1) >= %d infeasible" % (2 * m); break
    print(line, flush=True)
