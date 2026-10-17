"""Z_2 skeleton of S3-covers of BH: eps on edges, even on every line-triangle, for every non-adjacent pair the 6 two-path
parities split 6/0 or 3/3.  Gauge-fixed (eps = 0 on a BFS spanning tree), so eps != 0  <=>  not a coboundary."""
import collections, time, numpy as np, sys
from ortools.sat.python import cp_model
from cover import *
A = load_edges("bvls243.edges"); fib = fibres_of(A, 0); ok, Q = is_cover(A, fib)
n = 81
m = cp_model.CpModel()
eps = {}
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]:
            eps[(P, R)] = eps[(R, P)] = m.NewBoolVar("")
nb = [set(np.nonzero(Q[P])[0]) for P in range(n)]
tree = []; seen = {0}; dq = collections.deque([0])
while dq:
    u = dq.popleft()
    for v in sorted(nb[u]):
        if v not in seen: seen.add(v); dq.append(v); tree.append((u, v))
for u, v in tree: m.Add(eps[(u, v)] == 0)
for P in range(n):
    for R in nb[P]:
        if R <= P: continue
        for S in nb[P] & nb[R]:
            if S <= R: continue
            m.AddBoolXOr([eps[(P, R)], eps[(R, S)], eps[(P, S)], True])   # sum even
mode = sys.argv[1] if len(sys.argv) > 1 else "split"
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: continue
        CN = sorted(nb[P] & nb[R])
        pp = []
        for Z in CN:
            b = m.NewBoolVar(""); m.AddBoolXOr([eps[(P, Z)], eps[(Z, R)], b.Not()]); pp.append(b)
        k = m.NewIntVar(0, 2, ""); m.Add(sum(pp) == 3 * k)
m.AddBoolOr(list({id(v): v for v in eps.values()}.values()))       # eps not identically 0
s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 1800
t = time.time(); r = s.Solve(m)
print("non-coboundary parity cocycle with 6/0-3/3 splits:", s.StatusName(r), f"{time.time()-t:.1f}s")
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    E = {k: s.Value(v) for k, v in eps.items() if k[0] < k[1]}
    print("odd edges:", sum(E.values()))
    import pickle; pickle.dump(E, open("parity_sol.pkl", "wb"))
