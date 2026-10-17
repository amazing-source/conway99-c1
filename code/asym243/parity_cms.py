"""Parity skeleton with native XORs (CryptoMiniSat, Gauss-Jordan).  WLOG: t(0,R0) = 1 (pair (0,R0) of type 3/3),
eps = 0 on a BFS tree.  SAT => a non-coboundary parity cocycle exists (S3-covers not excluded at parity level);
UNSAT => every 3-cover of BH that is srg(243,22,1,2) is a Z_3-cover."""
import collections, itertools, sys, time, numpy as np
import pycryptosat
from cover import *
A = load_edges("bvls243.edges"); fib = fibres_of(A, 0); ok, Q = is_cover(A, fib)
n = 81; nb = [set(np.nonzero(Q[P])[0].tolist()) for P in range(n)]
s = pycryptosat.Solver(threads=int(sys.argv[1]) if len(sys.argv) > 1 else 4)
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
        for S in nb[P] & nb[R]:
            if P < R < S: s.add_xor_clause([E[(P, R)], E[(R, S)], E[(P, S)]], False)
R0 = min(R for R in range(1, n) if not Q[0, R])
T = {}
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: continue
        t = new(); T[(P, R)] = t
        pis = []
        for Z in sorted(nb[P] & nb[R]):
            p = new(); s.add_xor_clause([E[(P, Z)], E[(Z, R)], p], False); pis.append(p)
        s.add_xor_clause(pis + [t], False)                     # xor(pis) = t  (Jorgensen relation)
        for i, j in itertools.permutations(range(6), 2):       # t = 0 => all equal
            s.add_clause([t, -pis[i], pis[j]])
        for k in (1, 5):                                       # t = 1 => weight exactly 3
            for c in itertools.combinations(range(6), k):
                s.add_clause([-t] + [(-pis[i] if i in c else pis[i]) for i in range(6)])
s.add_clause([T[(0, R0)]])
t0 = time.time(); sat, sol = s.solve()
print("SAT" if sat else "UNSAT", f"{time.time()-t0:.1f}s", flush=True)
if sat:
    tt = sum(1 for k, v in T.items() if sol[v]); print("number of 3/3 pairs:", tt)
    import pickle; pickle.dump({k: sol[v] for k, v in E.items() if k[0] < k[1]}, open("parity_cms_sol.pkl", "wb"))
