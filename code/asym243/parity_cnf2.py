"""Parity skeleton with a WLOG normalisation: BH is rank 3, so Aut(BH) is transitive on non-adjacent pairs;
we force the pair (0, R0) to be of 3/3 type.  UNSAT  =>  every pair is 6/0  =>  eps is a coboundary (rank computation)
=>  every 3-cover of BH that is srg(243,22,1,2) is a Z_3-cover."""
import collections, itertools, sys, numpy as np
from cover import *
A = load_edges("bvls243.edges"); fib = fibres_of(A, 0); ok, Q = is_cover(A, fib)
n = 81; nb = [set(np.nonzero(Q[P])[0]) for P in range(n)]
nv = 0; E = {}; cls = []
def new():
    global nv; nv += 1; return nv
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: E[(P, R)] = E[(R, P)] = new()
def xor_eq(vs, parity):
    for signs in itertools.product((0, 1), repeat=len(vs)):
        if sum(signs) % 2 != parity:
            cls.append([(-v if s else v) for v, s in zip(vs, signs)])
tree = []; seen = {0}; dq = collections.deque([0])
while dq:
    u = dq.popleft()
    for v in sorted(nb[u]):
        if v not in seen: seen.add(v); dq.append(v); tree.append((u, v))
for u, v in tree: cls.append([-E[(u, v)]])
for P in range(n):
    for R in nb[P]:
        if R <= P: continue
        for S in nb[P] & nb[R]:
            if S <= R: continue
            xor_eq([E[(P, R)], E[(R, S)], E[(P, S)]], 0)
R0 = [R for R in range(1, n) if not Q[0, R]][0]
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: continue
        pis = []
        for Z in sorted(nb[P] & nb[R]):
            p = new(); xor_eq([E[(P, Z)], E[(Z, R)], p], 0); pis.append(p)
        allowed = (3,) if (P, R) == (0, R0) else (0, 3, 6)
        for bits in itertools.product((0, 1), repeat=6):
            if sum(bits) not in allowed:
                cls.append([(-v if b else v) for v, b in zip(pis, bits)])
with open(sys.argv[1], "w") as f:
    f.write(f"p cnf {nv} {len(cls)}\n")
    for c in cls: f.write(" ".join(map(str, c)) + " 0\n")
print("vars", nv, "clauses", len(cls), "forced pair", (0, R0))
