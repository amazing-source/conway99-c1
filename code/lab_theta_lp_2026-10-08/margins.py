"""C1, lab session. Margins: for each rank, the exact maximum of each dual shell b_k (k = 2..9) compatible with the current
constraints, next to the lower bound in use. A proved lower bound above the maximum excludes the rank.
Constraints: audited b_2, b_3, b_4, Codex's note-175 b_5..b_8, positivity, a_7k >= b_k, 7 a_7 + 8 a_8 <= 55440, b_1 <= 88.
  python margins.py <N> [d ...] [b<k>=<value> ...]
An argument b<k>=<value> replaces the lower bound of b_k by a WHAT-IF value (not a proved bound): it shows what a
stronger count of the vectors of norm 2k of M would give."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
LOW = {2: 462, 3: 24948, 4: 1431738, 5: 18001368, 6: 86272956, 7: 208016424, 8: 263126556}
for arg in [x for x in sys.argv[2:] if "=" in x]:
    k, v = arg.split("="); LOW[int(k[1:])] = int(v); print("WHAT-IF (not proved): b_%d >= %d" % (int(k[1:]), int(v)), flush=True)
for d in ([int(x) for x in sys.argv[2:] if "=" not in x] or [34, 36, 38]):
    A, B, C = X.build(d, "ext"); C = [c for c in C if not c[0].startswith(("b_2 >=", "b_3 >=", "b_4 >=", "b_5 >="))]
    for n, lo in LOW.items(): C.append(("b_%d >= %d" % (n, lo), T.add(B[n], T.aff(lo), -1)))
    C.append(("7 a_7 + 8 a_8 <= 55440", T.add(T.aff(55440), T.add(T.sc(A[7], 7), T.sc(A[8], 8)), -1)))
    C.append(("b_1 <= 88", T.add(T.aff(88), B[1], -1)))
    if X.feasible(C)[0] == "infeasible": print("d = %d (r = %d): INFEASIBLE" % (d, d + 1), flush=True); continue
    line = "d = %d (r = %d):" % (d, d + 1)
    for k in range(2, 10):
        hi = X.minimise(C, T.sc(B[k], -1))
        mx = -hi[1] if hi[0] == "min" else None
        line += " b_%d: low %d, max %s (x%.2f);" % (k, LOW.get(k, 0), "inf" if mx is None else X.show(mx), (float(mx) / LOW[k]) if (mx is not None and k in LOW) else float("nan"))
    print(line, flush=True)
