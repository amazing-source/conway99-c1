"""C1, lab session. Exact LP with the AUDITED set only (b_2 >= 462, b_3 >= 24948, b_4 >= 1431738, b_5 >= 196812, positivity,
a_7k >= b_k) and Codex's coupled seed bound 7 a_7 + 8 a_8 <= 55440 (note 173: one norm-16 vector per seed, and the seeds of
norm 14 and 16 are disjoint).   python coupled.py <N>
For d = 30..42: feasibility; the ladder (largest m with a_7 = ... = a_(m-1) = 0 feasible); exact minima of the number of
vectors of norm <= 18, 20, 22, 24, 26; and the scenario "no vector of norm 14 or 16"."""
import sys
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
def build(d):
    A, B, C = X.build(d, "ext"); C = [c for c in C if c[0] != "b_4 >= 388080"]
    C.append(("b_4 >= 1431738", T.add(B[4], T.aff(1431738), -1)))
    C.append(("7 a_7 + 8 a_8 <= 55440", T.add(T.aff(55440), T.add(T.sc(A[7], 7), T.sc(A[8], 8)), -1)))
    return A, B, C
for d in range(30, 44, 2):
    A, B, C = build(d); st = X.feasible(C)
    if st[0] == "infeasible": print("d = %d (r = %d): INFEASIBLE: %s" % (d, d + 1, ", ".join(nm for nm, _ in st[1])), flush=True); continue
    lad = None
    for m in range(8, 16):
        if X.feasible(C + [("a_%d <= 0" % n, T.sc(A[n], -1)) for n in range(7, m)])[0] == "infeasible": lad = 2 * (m - 1); break
    line = "d = %d (r = %d): feasible; min(L1) <= %s;" % (d, d + 1, lad); acc = T.aff(0)
    for m in range(7, 14):
        acc = T.add(acc, A[m])
        if m >= 9: line += " N(<=%d) >= %s;" % (2 * m, X.show(X.minimise(C, acc)[1]))
    C78 = C + [("a_7 <= 0", T.sc(A[7], -1)), ("a_8 <= 0", T.sc(A[8], -1))]
    if X.feasible(C78)[0] == "infeasible": line += " no norm 14/16: INFEASIBLE"
    else: line += " no norm 14/16: a_9 >= %s, a_9 + a_10 >= %s" % (X.show(X.minimise(C78, A[9])[1]), X.show(X.minimise(C78, T.add(A[9], A[10]))[1]))
    print(line, flush=True)
