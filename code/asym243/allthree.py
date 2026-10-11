"""Special case: every non-adjacent pair of type 3/3 <=> a signing A_s of BH with A_s^2 = A_s + 20 I
(eigenvalues 5^36, -4^45), triangle products +1.  Equivalent to an antipodal distance-regular double cover of BH
with c2 = 3.  CNF for kissat: eps on edges, triangle-even, each non-adjacent pair exactly 3 odd paths."""
import itertools, collections, sys, numpy as np
from cover import *
A = load_edges("bvls243.edges"); fib = fibres_of(A, 0); ok, Q = is_cover(A, fib)
n = 81; nb = [set(np.nonzero(Q[P])[0].tolist()) for P in range(n)]
nv = 0; E = {}; cls = []
def new():
    global nv; nv += 1; return nv
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: E[(P, R)] = E[(R, P)] = new()
def xor_eq(vs, parity):
    for signs in itertools.product((0, 1), repeat=len(vs)):
        if sum(signs) % 2 != parity: cls.append([(-v if s else v) for v, s in zip(vs, signs)])
tree, seen, dq = [], {0}, collections.deque([0])
while dq:
    u = dq.popleft()
    for v in sorted(nb[u]):
        if v not in seen: seen.add(v); dq.append(v); tree.append((u, v))
for u, v in tree: cls.append([-E[(u, v)]])
for P in range(n):
    for R in nb[P]:
        for S in nb[P] & nb[R]:
            if P < R < S: xor_eq([E[(P, R)], E[(R, S)], E[(P, S)]], 0)
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: continue
        pis = []
        for Z in sorted(nb[P] & nb[R]):
            p = new(); xor_eq([E[(P, Z)], E[(Z, R)], p], 0); pis.append(p)
        for bits in itertools.product((0, 1), repeat=6):
            if sum(bits) != 3: cls.append([(-v if b else v) for v, b in zip(pis, bits)])
with open(sys.argv[1], "w") as f:
    f.write(f"p cnf {nv} {len(cls)}\n")
    for c in cls: f.write(" ".join(map(str, c)) + " 0\n")
print("vars", nv, "clauses", len(cls))
