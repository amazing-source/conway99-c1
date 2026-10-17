"""GF(2) linear algebra for the parity skeleton.  Unknown eps on the 810 edges of BH.
Linear part: triangle sums = 0.  If every non-adjacent pair had a 6/0 split (all 6 two-path parities equal) the
condition would be linear; we compute the dimension of that solution space modulo coboundaries."""
import numpy as np, itertools
from cover import *
A = load_edges("bvls243.edges"); fib = fibres_of(A, 0); ok, Q = is_cover(A, fib)
n = 81
E = {}; elist = []
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: E[(P, R)] = E[(R, P)] = len(elist); elist.append((P, R))
nb = [set(np.nonzero(Q[P])[0]) for P in range(n)]
def rank_gf2(rows):
    rows = [r for r in rows if r]; basis = {}
    for r in rows:
        while r:
            h = r.bit_length() - 1
            if h in basis: r ^= basis[h]
            else: basis[h] = r; break
    return len(basis)
tri = []
for P in range(n):
    for R in nb[P]:
        if R <= P: continue
        for S in nb[P] & nb[R]:
            if S <= R: continue
            tri.append((1 << E[(P, R)]) | (1 << E[(R, S)]) | (1 << E[(P, S)]))
cob = []
for P in range(n):
    r = 0
    for R in nb[P]: r |= 1 << E[(P, R)]
    cob.append(r)
eq = []
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: continue
        CN = sorted(nb[P] & nb[R])
        forms = [(1 << E[(P, Z)]) | (1 << E[(Z, R)]) for Z in CN]
        for f in forms[1:]: eq.append(forms[0] ^ f)
rt = rank_gf2(tri); rc = rank_gf2(cob)
print("edges", len(elist), "rank(triangles)", rt, "rank(coboundaries)", rc, "dim H^1 =", len(elist) - rt - rc)
r_all = rank_gf2(tri + eq)
print("all pairs 6/0: dim of solution space", len(elist) - r_all, "(coboundaries satisfy it: their dim is", rc, ")")
