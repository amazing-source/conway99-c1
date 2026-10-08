"""C1, lab session, 2026-10-08. Rank 37 ceiling with the laptop session's cuts on roots and seeds (its message of 08:30 UTC;
hand proofs and a local CP-SAT search, NOT yet audited here or by Codex: the lines below are what-if until then).
  python ceiling37_lap.py <N> [d]
Base constraints as in ceiling37.py, with Codex's b_3 >= 45528 (note 186). Cuts:
  L1: a_7 + 4 b_1 <= 990                    (the 6 pairs of a root seed lie in no other Fano seed)
  L2: 7 a_7 + 8 a_8 + 273 b_1 <= 55440      (combinatorial seed count beside root seeds)
  L3: 21 a_7 + 24 a_8 + 1939 b_1 <= 166320  (with the Bessel bounds S(5) <= 2, S(6) = 0; needs S(4) <= 186, pending)
  L4: b_1 <= 78                             (Bessel with integrality on the edges)"""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
d = int(sys.argv[2]) if len(sys.argv) > 2 else 36
A, B, C0 = X.build(d, "ext"); C0 = [c for c in C0 if not c[0].startswith(("b_2 >=", "b_3 >=", "b_4 >=", "b_5 >="))]
for n, lo in {2: 462, 3: 45528, 4: 3371634, 5: 34087368, 6: 86272956, 7: 208016424, 8: 263126556}.items(): C0.append(("b_%d >= %d" % (n, lo), T.add(B[n], T.aff(lo), -1)))
C0.append(("cap", T.add(T.aff(55440), T.add(T.sc(A[7], 7), T.sc(A[8], 8)), -1))); C0.append(("b_1 <= 88", T.add(T.aff(88), B[1], -1)))
C0.append(("a_7 <= 990", T.add(T.aff(990), A[7], -1)))
def comb(c0, terms):
    f = T.aff(c0)
    for coef, form in terms: f = T.add(f, T.sc(form, -coef))
    return f
L1 = ("L1", comb(990, [(1, A[7]), (4, B[1])])); L2 = ("L2", comb(55440, [(7, A[7]), (8, A[8]), (273, B[1])]))
L3 = ("L3", comb(166320, [(21, A[7]), (24, A[8]), (1939, B[1])])); L4 = ("L4", comb(78, [(1, B[1])]))
print("d = %d (r = %d)" % (d, d + 1))
for nm, extra in (("base (b_3 >= 45528)", []), ("L1", [L1]), ("L1 + L2 + L4", [L1, L2, L4]), ("L1 + L2 + L3 + L4", [L1, L2, L3, L4])):
    C = C0 + extra
    if X.feasible(C)[0] == "infeasible": print("%-22s INFEASIBLE" % nm, flush=True); continue
    r1 = X.minimise(C, T.sc(B[4], -1)); y = r1[2]; ev = lambda f: f[0] + sum(f[k] * y[k - 1] for k in range(1, 8))
    r2 = X.minimise(C, T.sc(T.add(B[4], T.sc(B[3], Fr(651, 34))), -1)); y2 = r2[2]; ev2 = lambda f: f[0] + sum(f[k] * y2[k - 1] for k in range(1, 8))
    print("%-22s max b_4 = %s; max b_4 + (651/34) b_3 = %s [there: a_7 = %s, a_8 = %s, a_9 = %s, a_10 = %s, a_12 = %s, a_13 = %s, b_1 = %s]" % (
        nm, X.show(-r1[1]), X.show(-r2[1]), X.show(ev2(A[7])), X.show(ev2(A[8])), X.show(ev2(A[9])), X.show(ev2(A[10])), X.show(ev2(A[12])), X.show(ev2(A[13])), X.show(ev2(B[1]))), flush=True)
