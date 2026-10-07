"""For each d: the largest m such that 'no vector of L1 of norm < 2m' is compatible with the ext constraints (exact).
  python ladder.py <N>"""
import sys
import theta_lp_exact as X
X.T.selfcheck()
for d in range(28, 44, 2):
    last = None; cert = None
    for m in range(7, 30):
        A, B, C = X.build(d, "ext+min:%d" % m); st = X.feasible(C)
        if st[0] == "infeasible": cert = [nm for nm, _ in st[1]]; break
        last = m
    print("d = %2d (r = %2d): min(L1) >= %s is compatible, min(L1) >= %d is INFEASIBLE (exact certificate: %s)" % (d, d + 1, "none" if last is None else 2 * last, 2 * m, ", ".join(cert)), flush=True)
