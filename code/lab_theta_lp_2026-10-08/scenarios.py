"""C1, lab session. Which short shells can carry the load at a given rank? Set "ext2" (audited bounds b_2, b_3, b_4 plus
b_5 >= 3415104, b_6 >= 10844064) with the caps a_7 <= 7920, a_8 <= 27720, b_1 <= 3784. For each d and each subset Z of the
shells n = 7..13 forced to be empty: feasible or not; if feasible, the exact minimum of the first non-empty shell.
  python scenarios.py <N> [d ...]"""
import sys
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
ds = [int(x) for x in sys.argv[2:]] or [34, 36, 38, 40, 42]
for d in ds:
    A, B, C = X.build(d, "ext2+caps"); print("d = %d (r = %d)" % (d, d + 1), flush=True)
    for keep in ([7], [8], [9], [7, 8], [7, 9], [8, 9], [10], [9, 10], [10, 11], [11, 12], [12], [12, 13], [13]):
        zero = [n for n in range(7, min(keep)) ] + [n for n in range(min(keep), max(keep) + 1) if n not in keep]
        Cz = C + [("a_%d <= 0" % n, T.sc(A[n], -1)) for n in range(7, max(keep) + 1) if n not in keep]
        st = X.feasible(Cz)
        if st[0] == "infeasible": print("   only shells %s among norms <= %d: infeasible" % (keep, 2 * max(keep)), flush=True); continue
        acc = T.aff(0)
        for n in keep: acc = T.add(acc, A[n])
        print("   only shells %s among norms <= %d: feasible, total >= %s" % (keep, 2 * max(keep), X.show(X.minimise(Cz, acc)[1])), flush=True)
