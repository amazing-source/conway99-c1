"""C1, lab session, 2026-10-08. Rank 37: which joint WHAT-IF lower bounds on (b_3, b_4, b_5) would make the LP infeasible.
  python frontier37.py <N> [d] [b5]
Constraints: positivity, a_7k >= b_k, b_2 >= 462, 7a_7 + 8a_8 <= 55440, a_7 <= 990, b_1 <= 88, Codex's note-175 b_6..b_8,
b_5 >= b5 (default 33224268 = 35123088 - 168 P - 7212 rho at its minimum over rho <= P/6, P <= 1386: the uniform PROVED
value, Codex's note 179 and its correction of 01:30 UTC; the first version of this script used 35 million, which is not
uniform), and the WHAT-IF values below for b_3 and b_4 (proved worst-case values: b_3 >= 24948, b_4 >= 2729034).
The table is not a result: it only says how much a census of larger dual families would have to deliver."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
d = int(sys.argv[2]) if len(sys.argv) > 2 else 36
B5 = int(sys.argv[3]) if len(sys.argv) > 3 else 33224268
assert 35123088 - 168 * 1386 - 7212 * 231 == 33224268
A, B, C0 = X.build(d, "ext"); C0 = [c for c in C0 if not c[0].startswith(("b_2 >=", "b_3 >=", "b_4 >=", "b_5 >="))]
for n, lo in {2: 462, 6: 86272956, 7: 208016424, 8: 263126556}.items(): C0.append(("b_%d >= %d" % (n, lo), T.add(B[n], T.aff(lo), -1)))
C0.append(("cap", T.add(T.aff(55440), T.add(T.sc(A[7], 7), T.sc(A[8], 8)), -1))); C0.append(("b_1 <= 88", T.add(T.aff(88), B[1], -1)))
C0.append(("a_7 <= 990", T.add(T.aff(990), A[7], -1)))
def low(n, v): return ("b_%d >= %d" % (n, v), T.add(B[n], T.aff(v), -1))
print("d = %d (r = %d). Rows: what-if b_3; columns: what-if b_4 (millions); b_5 >= %d. F = feasible, X = infeasible" % (d, d + 1, B5))
b4s = [3, 6, 9, 12, 15, 18, 21, 24, 27]
print("        b_4:  " + "  ".join("%3dM" % x for x in b4s))
for b3 in (24948, 66528, 150000, 300000, 600000, 900000, 1200000):
    row = []
    for b4 in b4s:
        C = C0 + [low(3, b3), low(4, b4 * 10 ** 6), low(5, B5)]
        row.append("  X " if X.feasible(C)[0] == "infeasible" else "  F ")
    print("b_3 >= %7d: %s" % (b3, "  ".join(row)), flush=True)
