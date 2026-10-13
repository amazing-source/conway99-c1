"""Lab session, 2026-10-13. Exact test "coclique of size 45 (Hoffman bound) in a srg(243,22,1,2)" as an integer
program: x binary, (A + 5I) x = 5.1 (equivalent to: coclique of size 45), optional x_v = 1 for a given vertex.
HiGHS through scipy.optimize.milp.     python hoffman45_milp.py <seconds> <edge file> [vertex]     One process, < 2 GB."""
import sys, time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
E = [tuple(map(int, l.split())) for l in open(sys.argv[2]) if l.strip()]; n = 1 + max(max(e) for e in E)
A = np.zeros((n, n))
for a, b in E: A[a, b] = A[b, a] = 1
lb = np.zeros(n); ub = np.ones(n)
if len(sys.argv) > 3: lb[int(sys.argv[3])] = 1
t = time.time()
res = milp(c=np.zeros(n), constraints=LinearConstraint(A + 5 * np.eye(n), 5 * np.ones(n), 5 * np.ones(n)), integrality=np.ones(n), bounds=Bounds(lb, ub), options={"time_limit": float(sys.argv[1]), "disp": False})
name = sys.argv[2].replace("\\", "/").split("/")[-1]
if res.status == 0:
    x = np.round(res.x).astype(int); C = np.nonzero(x)[0]
    assert len(C) == 45 and not A[np.ix_(C, C)].any()
    print("%s: coclique of size 45 FOUND (%.1f s): %s" % (name, time.time() - t, C.tolist()))
elif res.status == 2: print("%s: NO coclique of size 45%s, proved by branch and bound (%.1f s)" % (name, " through the given vertex" if len(sys.argv) > 3 else "", time.time() - t))
else: print("%s: no decision (status %d, %s, %.1f s)" % (name, res.status, res.message, time.time() - t))
