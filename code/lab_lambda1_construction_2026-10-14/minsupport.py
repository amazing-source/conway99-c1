"""Minimum support of an eigenvector (14/10/2026), for the trade-size bound of the concentration criterion:
a trade between two srg with the same parameters touches at least max(sigma_r, sigma_s) vertices, where sigma_theta
is the smallest support of a theta-eigenvector (both P and P' in the lemma are nonzero projections onto theta-
eigenvectors supported in the touched set, for theta = r and for theta = s).
A minimal-support eigenvector spans the eigenvectors supported on its support, a rational space: it can be scaled to
an integral vector. MILP (HiGHS via scipy.optimize.milp): x = Q c (Q orthonormal basis of the eigenspace), binary z,
-z_i <= x_i <= z_i, x_{i0} = 1 (so the largest entry is at i0), minimise sum z. One MILP per choice of i0 (a vertex
of each orbit, or a sample); the minimum over i0 is sigma_theta when all i0 are covered.
usage: python minsupport.py <edges> <theta> <comma-separated i0 list or 'all'> <seconds per MILP>"""
import sys
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
n = 1 + max(max(e) for e in E)
A = np.zeros((n, n))
for a, b in E:
    A[a, b] = A[b, a] = 1
theta = float(sys.argv[2])
w, V = np.linalg.eigh(A)
Q = V[:, np.abs(w - theta) < 1e-6]
d = Q.shape[1]
print("n = %d, eigenvalue %g of multiplicity %d" % (n, theta, d), flush=True)
i0s = list(range(n)) if sys.argv[3] == "all" else [int(t) for t in sys.argv[3].split(",")]
secs = float(sys.argv[4])
best = None
for i0 in i0s:
    t0 = time.time()
    # variables: c (d, free), z (n, binary); objective sum z
    cobj = np.concatenate([np.zeros(d), np.ones(n)])
    # x_i - z_i <= 0 and -x_i - z_i <= 0
    A1 = np.hstack([Q, -np.eye(n)])
    A2 = np.hstack([-Q, -np.eye(n)])
    cons = [LinearConstraint(A1, -np.inf, 0), LinearConstraint(A2, -np.inf, 0),
            LinearConstraint(np.concatenate([Q[i0], np.zeros(n)])[None, :], 1, 1)]
    integrality = np.concatenate([np.zeros(d), np.ones(n)])
    bounds = Bounds(np.concatenate([-np.inf * np.ones(d), np.zeros(n)]), np.concatenate([np.inf * np.ones(d), np.ones(n)]))
    res = milp(cobj, constraints=cons, integrality=integrality, bounds=bounds,
               options={"time_limit": secs, "disp": False})
    if res.x is None:
        print("  i0 = %d: no solution (%s, %.0f s)" % (i0, res.message, time.time() - t0), flush=True)
        continue
    x = Q @ res.x[:d]
    supp = np.abs(x) > 1e-6
    vals = sorted(set(np.round(np.abs(x[supp]), 4).tolist()))
    status = "optimal" if res.status == 0 else "time limit (upper bound)"
    print("  i0 = %d: support %d [%s], |entries| %s (%.0f s)" % (i0, int(supp.sum()), status, vals[:6], time.time() - t0),
          flush=True)
    if res.status == 0 and (best is None or supp.sum() < best):
        best = int(supp.sum())
print("smallest support found (optimal runs): %s" % best)
