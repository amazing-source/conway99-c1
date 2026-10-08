"""C1, lab session, 2026-10-08. Cross-check of Codex's trade-off at rank 35: 101160 rho + 4329 P >= 10391999.
  python tradeoff35.py <N>
Same LP as r35.py, with b_4 >= 3826746 + 90 P - 4572 rho (the +6P of Codex's note 168: the differences of two triangles
with one cross edge number exactly 33264 + 6P). Exact minimum of the linear form over the polytope (b_1..b_7, P, rho)."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
import r35 as R
T.selfcheck()
A, B, C = R.build(34)
C = [(nm, f) for nm, f in C if not nm.startswith("b_4 >= 3826746")]
C.append(("b_4 >= 3826746 + 90 P - 4572 rho", R.add(B[4], R.lin(3826746, P=90, rho=-4572), -1)))
for nm, form in (("101160 rho + 4329 P", R.lin(0, P=4329, rho=101160)), ("rho", R.lin(0, rho=1)), ("P", R.lin(0, P=1))):
    lo, y = R.minimise(C, form); print("minimum of %-22s = %s = %s   (at P = %s, rho = %s)" % (nm, lo, X.show(lo), X.show(y[7]), X.show(y[8])), flush=True)
