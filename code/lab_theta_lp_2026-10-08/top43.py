"""C1, lab session. r = 43 (d = 42): how the forced short vectors of L1 can be distributed over the norms 16..26.
Constraints: audited set (b_2 >= 462, b_3 >= 24948, b_4 >= 1431738) with Codex's exact small shells (note 175: b_5 >=
18001368, b_6 >= 86272956, b_7 >= 208016424), positivity, a_7k >= b_k, 7 a_7 + 8 a_8 <= 55440.
 (1) exact minimum of a_8 + ... + a_13;  (2) for each n: exact minimum of a_n when the other five shells are empty, and
 exact minimum of the sum when shell n is empty;  (3) exact minimum of t with a_n <= t for n = 8..13.
  python top43.py <N> [d]"""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
d = int(sys.argv[2]) if len(sys.argv) > 2 else 42
A, B, C = X.build(d, "ext"); C = [c for c in C if not c[0].startswith(("b_4 >=", "b_5 >="))]
for n, lo in ((4, 1431738), (5, 18001368), (6, 86272956), (7, 208016424)): C.append(("b_%d >= %d" % (n, lo), T.add(B[n], T.aff(lo), -1)))
C.append(("7 a_7 + 8 a_8 <= 55440", T.add(T.aff(55440), T.add(T.sc(A[7], 7), T.sc(A[8], 8)), -1)))
assert X.feasible(C)[0] == "feasible"
S = T.aff(0)
for n in range(8, 14): S = T.add(S, A[n])
print("d = %d (r = %d): min (a_8 + ... + a_13) = %s" % (d, d + 1, X.minimise(C, S)[1]), flush=True)
for n in range(8, 14):
    Cz = C + [("a_%d <= 0" % m, T.sc(A[m], -1)) for m in range(8, 14) if m != n]
    alone = X.minimise(Cz, A[n])[1] if X.feasible(Cz)[0] == "feasible" else None
    Ce = C + [("a_%d <= 0" % n, T.sc(A[n], -1))]
    without = X.minimise(Ce, S)[1] if X.feasible(Ce)[0] == "feasible" else None
    print("  norm %d: alone (other shells 16..26 empty): %s;  if this shell is empty, min of the sum: %s" % (2 * n, "infeasible" if alone is None else X.show(alone), "infeasible" if without is None else X.show(without)), flush=True)
# (3) min t with a_n <= t: one more variable
NV = 8
ext = lambda f: list(f) + [Fr(0)]
C8 = [(nm, ext(f)) for nm, f in C]
for n in range(8, 14): g = ext(T.sc(A[n], -1)); g[8] = Fr(1); C8.append(("t >= a_%d" % n, g))
res = X.simplex([f[1:] for _, f in C8], [-f[0] for _, f in C8], [Fr(0)] * 7 + [Fr(1)])
assert res[0] == "optimal"; lam = res[2]
assert all(x >= 0 for x in lam) and all(sum(l * f[k] for l, (_, f) in zip(lam, C8) if l) == (1 if k == 8 else 0) for k in range(1, 9))
print("  min over the polytope of max(a_8..a_13) = %s = %.3f" % (res[1], float(res[1])), flush=True)
