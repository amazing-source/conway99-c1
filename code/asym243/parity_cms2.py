"""Parity skeleton of S3-covers of BH, strengthened (CryptoMiniSat with native XORs):
- eps on edges, eps = 0 on a BFS tree from 0 (gauge), triangle-even;
- per non-adjacent pair: t = xor of the 6 path parities (Jorgensen), t=0 => all equal, t=1 => exactly 3 odd;
- per quadrangle Q (4-cycle P-Z-R-Z'): q = parity of Q; q => t(P,R) and q => t(Z,Z')   (odd holonomy needs 3/3 at
  both diagonals);
- WLOG (BH rank 3 + pair stabiliser): (0,R0) is 3/3 with the odd-path set of the given class; the class
  representative is chosen so that the path through the BFS parent of R0 is even (gauge-compatible).
Usage: python3 parity_cms2.py CLASS(3a|3b) THREADS TIMELIMIT"""
import collections, itertools, sys, time, numpy as np
import pycryptosat
from cover import *
from curvature import bh_grids
cls_name, threads, tlim = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
A = load_edges("bvls243.edges"); fib = fibres_of(A, 0); ok, Q = is_cover(A, fib)
n = 81; nb = [set(np.nonzero(Q[P])[0].tolist()) for P in range(n)]
s = pycryptosat.Solver(threads=threads, time_limit=tlim)
nv = 0
def new():
    global nv; nv += 1; return nv
E = {}
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: E[(P, R)] = E[(R, P)] = new()
tree, seen, dq = [], {0}, collections.deque([0])
while dq:
    u = dq.popleft()
    for v in sorted(nb[u]):
        if v not in seen: seen.add(v); dq.append(v); tree.append((u, v))
for u, v in tree: s.add_clause([-E[(u, v)]])
for P in range(n):
    for R in nb[P]:
        for S_ in nb[P] & nb[R]:
            if P < R < S_: s.add_xor_clause([E[(P, R)], E[(R, S_)], E[(P, S_)]], False)
T = {}; PI = {}
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: continue
        t = new(); T[(P, R)] = T[(R, P)] = t; pis = []
        for Z in sorted(nb[P] & nb[R]):
            p = new(); s.add_xor_clause([E[(P, Z)], E[(Z, R)], p], False); pis.append(p); PI[(P, R, Z)] = p
        s.add_xor_clause(pis + [t], False)
        for i, j in itertools.permutations(range(6), 2): s.add_clause([t, -pis[i], pis[j]])
        for k in (1, 5):
            for cc in itertools.combinations(range(6), k):
                s.add_clause([-t] + [(-pis[i] if i in cc else pis[i]) for i in range(6)])
# quadrangle propagation
nq = 0
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: continue
        CN = sorted(nb[P] & nb[R])
        for Z, Z2 in itertools.combinations(CN, 2):
            q = new(); s.add_xor_clause([PI[(P, R, Z)], PI[(P, R, Z2)], q], False)
            s.add_clause([-q, T[(P, R)]]); s.add_clause([-q, T[(Z, Z2)]]); nq += 1
# WLOG pattern at (0, R0)
R0 = [R for R in range(1, n) if not Q[0, R]][0]
CN0 = sorted(nb[0] & nb[R0])
grids, _ = bh_grids(Q)
pairs = [(Z, Z2) for Z, Z2 in itertools.combinations(CN0, 2) if any({0, R0, Z, Z2} <= g for g in grids)]
parent = [u for u, v in tree if v == R0][0]
(a1, a2), (b1, b2), (c1, c2) = pairs
odd = {a1, b1, c1} if cls_name == "3a" else {a1, a2, b1}
if parent in odd: odd = set(CN0) - odd
for Z in CN0: s.add_clause([PI[(0, R0, Z)] if Z in odd else -PI[(0, R0, Z)]])
print(f"class {cls_name}: vars {nv}, quadrangles {nq}, odd paths at (0,{R0}): {sorted(odd)} (parent {parent})", flush=True)
t0 = time.time(); sat, sol = s.solve()
status = "SAT" if sat is True else ("UNSAT" if sat is False else "UNKNOWN (time limit)")
print(f"class {cls_name}: {status} after {time.time()-t0:.0f}s", flush=True)
if sat:
    import pickle
    pickle.dump({k: sol[v] for k, v in E.items() if k[0] < k[1]}, open(f"parity_sol_{cls_name}.pkl", "wb"))
    print("3/3 pairs:", sum(1 for k, v in T.items() if k[0] < k[1] and sol[v]))
