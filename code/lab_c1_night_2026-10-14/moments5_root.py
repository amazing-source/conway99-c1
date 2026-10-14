"""Largest average prism number allowed by the degree-5 Gram matrix (moments5.gram), by bisection in exact arithmetic,
and comparison with the degree-3 bound 588/59."""
from fractions import Fraction as Fr
from moments4 import det
from moments5 import gram


def ok(p):
    _, M = gram(p)
    return all(det([row[:k] for row in M[:k]]) > 0 for k in range(1, 7))


lo, hi = Fr(39, 4), Fr(10)
assert ok(lo) and not ok(hi)
for _ in range(60):
    mid = (lo + hi) / 2
    if ok(mid):
        lo = mid
    else:
        hi = mid
print("degree-5 bound: pbar <= %.12f" % float(hi))
print("degree-3 bound: 588/59 = %.12f" % (588 / 59))
_, M = gram(Fr(588, 59))
print("positive definite at 588/59:", ok(Fr(588, 59)), "  det6 there: %.6e" % float(det(M)))
print("total prisms <= floor(231 * bound / 2) = %d (degree 3 gave 1151)" % int(231 * hi / 2))
