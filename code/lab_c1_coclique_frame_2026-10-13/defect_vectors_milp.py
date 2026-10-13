"""Lab session, 2026-10-13. Defect vectors of cocliques of size 45 - delta in a srg(243,22,1,2), searched directly.
A coclique C of size 45 - delta gives q = 5.1 - (A + 5I) 1_C, an integer vector with
    A q = 4 q + 2 delta . 1,   sum q = 27 delta,   sum q^2 = 6075 - 225 c + 2 c^2  (c = 45 - delta),   q <= 5.
Stage 1 (here): integer vectors q with these three properties (one-hot variables for the non-zero values).
Stage 2: for a given q, a coclique exists iff (A + 5I) x = 5.1 - q has a 0/1 solution (checked here too).
The search loops: each q found is tested, then forbidden, until no q is left or the time is over.
python defect_vectors_milp.py <seconds> <delta> <edge file> [vertex with q != 0]    HiGHS (scipy). One process, < 2 GB."""
import sys, time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, vstack, csr_matrix
tl, delta = float(sys.argv[1]), int(sys.argv[2])
E = [tuple(map(int, l.split())) for l in open(sys.argv[3]) if l.strip()]; n = 1 + max(max(e) for e in E)
A = np.zeros((n, n))
for a, b in E: A[a, b] = A[b, a] = 1
adj = [np.nonzero(A[v])[0].tolist() for v in range(n)]
c = 45 - delta; S1 = 27 * delta; S2 = 6075 - 225 * c + 2 * c * c
J = [j for j in range(-6, 6) if j != 0 and j * j <= S2]; nj = len(J); N = n * nj
zi = lambda v, t: v * nj + t
M = lil_matrix((2 * n + 2, N)); lo = np.zeros(2 * n + 2); hi = np.zeros(2 * n + 2)
for v in range(n):
    for t, j in enumerate(J):
        M[v, zi(v, t)] = -4 * j; M[n + v, zi(v, t)] = 1
        for w in adj[v]: M[w, zi(v, t)] = j                             # row w: sum over neighbours of w
        M[2 * n, zi(v, t)] = j; M[2 * n + 1, zi(v, t)] = j * j
    lo[v] = hi[v] = 2 * delta; lo[n + v] = 0; hi[n + v] = 1
lo[2 * n] = hi[2 * n] = S1; lo[2 * n + 1] = hi[2 * n + 1] = S2
if len(sys.argv) > 4: lo[n + int(sys.argv[4])] = 1
M = M.tocsr(); cuts = []; t0 = time.time(); found = 0; name = sys.argv[3].replace("\\", "/").split("/")[-1]
while True:
    left = tl - (time.time() - t0)
    if left <= 1: print("%s: time over after %d defect vectors, none of them from a coclique of size %d: NO DECISION" % (name, found, c)); break
    Mc = vstack([M] + cuts).tocsr() if cuts else M
    l2 = np.concatenate([lo, -np.inf * np.ones(len(cuts))]); h2 = np.concatenate([hi, np.array([S for _, S in cut_rhs])]) if cuts else hi
    res = milp(c=np.zeros(N), constraints=LinearConstraint(Mc, l2, h2), integrality=np.ones(N), bounds=Bounds(np.zeros(N), np.ones(N)), options={"time_limit": left, "disp": False})
    if res.status == 2:
        print("%s: NO %sdefect vector left after %d found, so NO coclique of size %d%s (branch and bound, %.1f s)" % (name, "" if found else "", found, c, " with a defect at the given vertex" if len(sys.argv) > 4 else "", time.time() - t0)); break
    if res.status != 0: print("%s: no decision (status %d) after %d defect vectors (%.1f s)" % (name, res.status, found, time.time() - t0)); break
    z = np.round(res.x).astype(int); q = np.zeros(n, dtype=int)
    for v in range(n):
        for t, j in enumerate(J):
            if z[zi(v, t)]: q[v] = j
    assert (A @ q == 4 * q + 2 * delta).all() and q.sum() == S1 and (q * q).sum() == S2
    found += 1
    r2 = milp(c=np.zeros(n), constraints=LinearConstraint(A + 5 * np.eye(n), 5 - q, 5 - q), integrality=np.ones(n), bounds=Bounds(np.zeros(n), np.ones(n)), options={"time_limit": max(1.0, min(60.0, tl - (time.time() - t0))), "disp": False})
    vals = {int(j): int((q == j).sum()) for j in sorted(set(q.tolist())) if j}
    if r2.status == 0:
        x = np.round(r2.x).astype(int); C = np.nonzero(x)[0]; assert len(C) == c and not A[np.ix_(C, C)].any()
        print("%s: coclique of size %d FOUND (%.1f s); defect values %s; C = %s" % (name, c, time.time() - t0, vals, C.tolist())); break
    print("   defect vector %d: values %s, support %d: %s" % (found, vals, int((q != 0).sum()), "no coclique behind it" if r2.status == 2 else "stage 2 undecided"), flush=True)
    row = lil_matrix((1, N)); ones = np.nonzero(z)[0]
    for i in ones: row[0, i] = 1
    cuts.append(row.tocsr()); cut_rhs = (cut_rhs if found > 1 else []) + [(None, len(ones) - 1)]
