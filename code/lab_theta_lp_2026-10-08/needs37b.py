"""C1, lab session, 2026-10-08. What rank 37 REQUIRES on the shells of norm 18 to 26 of L1 (exact rational simplex).
  python needs37b.py <N> [d]
Constraints: a_n >= 0, b_n >= 0 (n <= N), a_7k >= b_k, Codex's dual lower bounds (b_2 >= 462, b_3 >= 45766,
b_4 >= 3371634, b_5.. of its note 175), the seed budget 7 a_7 + 8 a_8 <= 55440, a_7 <= 842, b_1 <= 44.
No census, no collision count. Prints exact minima of several linear forms in (a_9, ..., a_13): any proved upper
bound below one of them excludes the rank. "Seed uses" = 9 a_9 + 10 a_10 + 11 a_11 + 12 a_12 (a binary eigenvector of
norm 2n with independent supports has n positive vertices, each with exactly 4 negative neighbours); 55440 = 99 * 560 is
the number of seeds (vertex, independent 4-subset of its neighbourhood)."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck()
d = int(sys.argv[2]) if len(sys.argv) > 2 else 36
A, B, C0 = X.build(d, "ext"); C0 = [c for c in C0 if not c[0].startswith(("b_2 >=", "b_3 >=", "b_4 >=", "b_5 >="))]
for n, lo in {2: 462, 3: 45766, 4: 3371634, 5: 34087368, 6: 86272956, 7: 208016424, 8: 263126556}.items(): C0.append(("b_%d >= %d" % (n, lo), T.add(B[n], T.aff(lo), -1)))
def le(c0, terms):
    f = T.aff(c0)
    for coef, form in terms: f = T.add(f, T.sc(form, -coef))
    return f
C0 += [("cap", le(55440, [(7, A[7]), (8, A[8])])), ("a7", le(842, [(1, A[7])])), ("b1", le(44, [(1, B[1])]))]
def comb(terms):
    f = T.aff(0)
    for coef, form in terms: f = T.add(f, T.sc(form, coef))
    return f
print("d = %d (r = %d): %s" % (d, d + 1, X.feasible(C0)[0]), flush=True)
forms = [("539 a_9 + 392 a_10 + 147 a_11 + 49 a_12", comb([(539, A[9]), (392, A[10]), (147, A[11]), (49, A[12])])),
         ("seed uses 9 a_9 + 10 a_10 + 11 a_11 + 12 a_12", comb([(9, A[9]), (10, A[10]), (11, A[11]), (12, A[12])])),
         ("seed uses including norm 26: + 13 a_13", comb([(9, A[9]), (10, A[10]), (11, A[11]), (12, A[12]), (13, A[13])])),
         ("a_9 + a_10 + a_11 + a_12", comb([(1, A[9]), (1, A[10]), (1, A[11]), (1, A[12])])),
         ("a_9 + a_10 + a_11 + a_12 + a_13", comb([(1, A[n]) for n in range(9, 14)])),
         ("16 a_9 + a_13", comb([(16, A[9]), (1, A[13])])), ("a_13", A[13]), ("a_12 + a_13", comb([(1, A[12]), (1, A[13])]))]
for nm, f in forms:
    r_ = X.minimise(C0, f); y = r_[2]; ev = lambda g: g[0] + sum(g[k] * y[k - 1] for k in range(1, 8))
    print("  min %-48s = %s   [at a_7 = %s, a_8 = %s, a_9 = %s, a_10 = %s, a_11 = %s, a_12 = %s, a_13 = %s, b_1 = %s]" % (
        nm, X.show(r_[1]), X.show(ev(A[7])), X.show(ev(A[8])), X.show(ev(A[9])), X.show(ev(A[10])), X.show(ev(A[11])), X.show(ev(A[12])), X.show(ev(A[13])), X.show(ev(B[1]))), flush=True)
