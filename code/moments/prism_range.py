"""Range of the prism count P allowed by the order-t moment hierarchy (srg_moments.py), for given parameters.
Usage: python3 prism_range.py n k lam mu t"""
import sys, math, numpy as np, cvxpy as cp
from srg_moments import Hierarchy, canon, extend
n, k, lam, mu, t = map(int, sys.argv[1:6])
H = Hierarchy(n, k, lam, mu, t)
Aeq = H.equalities(); mats = [H.block_matrices(s, a, F, c) for _, s, a, F, c in H.blocks()]
# prism K3 x K2 on vertices 0,1,2 / 3,4,5 with matching i -- i+3
bits = 0
from srg_moments import pid
for (i, j) in [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4), (2, 5)]:
    bits |= 1 << pid(i, j)
Pc = canon(6, bits)[0]
dens6 = H.dens[(6, Pc)]                       # induced density of the prism as a linear form in q
q = cp.Variable(len(H.top))
cons = [q >= 0, cp.sum(q) == 1, Aeq @ q == 0]
for m in mats:
    d = m.shape[0]; M = cp.reshape(m.reshape(d * d, -1) @ q, (d, d), order="C"); cons.append((M + M.T) / 2 >> 0)
res = []
for sense in (cp.Minimize, cp.Maximize):
    pr = cp.Problem(sense(dens6 @ q), cons); pr.solve(solver="CLARABEL")
    res.append((pr.status, pr.value * math.comb(n, 6)))
print(f"srg({n},{k},{lam},{mu}) order {t}: prisms P in [{res[0][1]:.3f}, {res[1][1]:.3f}]  ({res[0][0]}, {res[1][0]})")
