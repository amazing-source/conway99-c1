"""Lab session, 2026-10-13. Short integral eigenvectors with entries in {-1,0,1} for the negative eigenvalue of a
srg(243,22,1,2) (s = -5): the analogue of the forced vectors of norm 14 to 26 at 99. A positive model of such a "world"
in a real graph would be a test bed for any exclusion argument or solver model written for the world of norm 18.
Integer program: v = a - b, a, b binary, a_x + b_x <= 1, (A + 5I) v = 0, a_0 = 1 (vertex 0 in the positive support),
minimise the norm sum(a + b); or with an upper bound on the norm.
python short_eigvec_milp.py <seconds> <edge file> [max norm]        HiGHS (scipy). One process, < 2 GB.
env NOPRESOLVE=1: the presolve of HiGHS crashes (segmentation fault) on new243_tricayley_Z3x4_grids25.edges.
A returned point is used only if it is integral, has a_0 = 1 and satisfies (A + 5I) v = 0 exactly."""
import sys, os, time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix, hstack, identity, vstack
E = [tuple(map(int, l.split())) for l in open(sys.argv[2]) if l.strip()]; n = 1 + max(max(e) for e in E)
A = np.zeros((n, n))
for a, b in E: A[a, b] = A[b, a] = 1
M = csr_matrix(A + 5 * np.eye(n)); I = identity(n, format="csr")
cons = [LinearConstraint(hstack([M, -M]).tocsr(), np.zeros(n), np.zeros(n)), LinearConstraint(hstack([I, I]).tocsr(), np.zeros(n), np.ones(n))]
if len(sys.argv) > 3: cons.append(LinearConstraint(np.ones((1, 2 * n)), 0, float(sys.argv[3])))
lb = np.zeros(2 * n); ub = np.ones(2 * n); lb[0] = 1
t = time.time()
res = milp(c=np.ones(2 * n), constraints=cons, integrality=np.ones(2 * n), bounds=Bounds(lb, ub), options={"time_limit": float(sys.argv[1]), "disp": False, "presolve": os.environ.get("NOPRESOLVE") is None})
name = sys.argv[2].replace("\\", "/").split("/")[-1]
valid = res.x is not None and np.abs(res.x - np.round(res.x)).max() < 1e-6 and round(res.x[0]) == 1 and not ((A + 5 * np.eye(n)) @ (np.round(res.x[:n]) - np.round(res.x[n:]))).any()
if valid:
    x = np.round(res.x).astype(int); v = x[:n] - x[n:]; assert not ((A + 5 * np.eye(n)) @ v).any()
    P = np.nonzero(v == 1)[0]; Q = np.nonzero(v == -1)[0]
    eP = int(A[np.ix_(P, P)].sum()) // 2; eQ = int(A[np.ix_(Q, Q)].sum()) // 2
    print("%s: eigenvector of norm %d through vertex 0 (%s, %.1f s): |P| = %d, |Q| = %d, edges inside P %d, inside Q %d"
          % (name, len(P) + len(Q), "OPTIMAL: shortest" if res.status == 0 else "best found, not proved shortest (lower bound %.1f)" % res.mip_dual_bound, time.time() - t, len(P), len(Q), eP, eQ))
    print("   P = %s\n   Q = %s" % (P.tolist(), Q.tolist()))
else: print("%s: %s (status %d, %.1f s)" % (name, "no such vector" if res.status == 2 else "no valid vector returned, no decision", res.status, time.time() - t))
