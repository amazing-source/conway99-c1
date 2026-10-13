"""Lab session, 2026-10-13. Exact test "coclique of size 45 - delta in a srg(243,22,1,2)" (delta = 1 is the analogue of
the cocliques of size 21 at 99). Integer program using the defect law: for a coclique C of size c = 45 - delta,
q_v = 5 - |N(v) n C| outside C satisfies  sum q = 27 delta,  sum q^2 = 6075 - 225 c + 2 c^2  (47 for delta = 1).
Variables: x_v (in C), z_{v,j} (v outside C and q_v = j), j = jmin..5.
  x_v + sum_j z_{v,j} = 1 ;  sum_{w ~ v} x_w = sum_j (5 - j) z_{v,j} ;  sum x = c ;  the two moment equations.
HiGHS through scipy.optimize.milp.   Also: at most one vertex of C on each line (891 inequalities, they strengthen the relaxation).
python near_hoffman_milp.py <seconds> <delta> <edge file> [vertex forced in C]      env MAXIMAL=1: C maximal"""
import sys, time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
tl, delta = float(sys.argv[1]), int(sys.argv[2])
E = [tuple(map(int, l.split())) for l in open(sys.argv[3]) if l.strip()]; n = 1 + max(max(e) for e in E)
adj = [[] for _ in range(n)]
for a, b in E: adj[a].append(b); adj[b].append(a)
c = 45 - delta; S1 = 27 * delta; S2 = 6075 - 225 * c + 2 * c * c
import os
J = [j for j in range(-6, 5 if os.environ.get('MAXIMAL') else 6) if j * j <= S2]      # MAXIMAL: every outside vertex has a neighbour in C
nj = len(J); N = n + n * nj
zi = lambda v, t: n + v * nj + t
lines = sorted({tuple(sorted((a, b, c))) for a, b in E for c in set(adj[a]) & set(adj[b])}); nl = len(lines)     # one vertex of C per line at most
R = 2 * n + 3 + nl
M = lil_matrix((R, N)); lo = np.zeros(R); hi = np.zeros(R)
for i, L in enumerate(lines):
    for v in L: M[2 * n + 3 + i, v] = 1
    hi[2 * n + 3 + i] = 1
for v in range(n):
    M[v, v] = 1
    for t in range(nj): M[v, zi(v, t)] = 1
    lo[v] = hi[v] = 1
    for w in adj[v]: M[n + v, w] = 1
    for t, j in enumerate(J): M[n + v, zi(v, t)] = -(5 - j)
for v in range(n):
    M[2 * n, v] = 1
    for t, j in enumerate(J): M[2 * n + 1, zi(v, t)] = j; M[2 * n + 2, zi(v, t)] = j * j
lo[2 * n] = hi[2 * n] = c; lo[2 * n + 1] = hi[2 * n + 1] = S1; lo[2 * n + 2] = hi[2 * n + 2] = S2
lb = np.zeros(N); ub = np.ones(N)
if len(sys.argv) > 4: lb[int(sys.argv[4])] = 1
t0 = time.time()
res = milp(c=np.zeros(N), constraints=LinearConstraint(M.tocsr(), lo, hi), integrality=np.ones(N), bounds=Bounds(lb, ub), options={"time_limit": tl, "disp": False})
name = sys.argv[3].replace("\\", "/").split("/")[-1]; extra = " through the given vertex" if len(sys.argv) > 4 else ""
if res.status == 0:
    x = np.round(res.x[:n]).astype(int); C = [v for v in range(n) if x[v]]; Cs = set(C)
    assert len(C) == c and all(not (set(adj[v]) & Cs) for v in C)
    b = [len(set(adj[v]) & Cs) for v in range(n) if v not in Cs]
    print("%s: coclique of size %d FOUND (%.1f s); numbers of neighbours in it, outside: %s" % (name, c, time.time() - t0, {k: b.count(k) for k in sorted(set(b))}))
    print("   C = %s" % C)
elif res.status == 2: print("%s: NO coclique of size %d%s, by branch and bound (%.1f s)" % (name, c, extra, time.time() - t0))
else: print("%s: size %d%s: no decision (status %d, %.1f s)" % (name, c, extra, res.status, time.time() - t0))
