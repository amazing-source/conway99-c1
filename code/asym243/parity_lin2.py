"""GF(2) facts for the parity skeleton.
L_PR(eps) = sum of the six 2-path parities = sum of labels of the 12 edges of the K_{2,6} on (P,R).
6/0 pair => L = 0 ; 3/3 pair => L = 1.
(1) Jorgensen: L = 1 on all pairs (+ triangle evenness) has no solution.
(2) The image of eps -> (L_PR) restricted to triangle-even eps: its dimension, and the left kernel K (vectors w with
    sum_PR w_PR L_PR = 0 identically).  Any solution's set T of 3/3 pairs satisfies |T n supp w| even for w in K."""
import numpy as np, itertools
from cover import *
A = load_edges("bvls243.edges"); fib = fibres_of(A, 0); ok, Q = is_cover(A, fib)
n = 81; nb = [set(np.nonzero(Q[P])[0].tolist()) for P in range(n)]
E = {}; el = []
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: E[(P, R)] = E[(R, P)] = len(el); el.append((P, R))
m = len(el)
def reduce_rows(rows, aug=False):
    basis = {}
    for r in rows:
        while r:
            h = r.bit_length() - 1
            if h in basis: r ^= basis[h]
            else: basis[h] = r; break
    return basis
tri = []
for P in range(n):
    for R in nb[P]:
        for S in nb[P] & nb[R]:
            if P < R < S: tri.append((1 << E[(P, R)]) | (1 << E[(R, S)]) | (1 << E[(P, S)]))
pairs = [(P, R) for P in range(n) for R in range(P + 1, n) if not Q[P, R]]
Lrows = []
for P, R in pairs:
    r = 0
    for Z in nb[P] & nb[R]: r ^= (1 << E[(P, Z)]) ^ (1 << E[(Z, R)])
    Lrows.append(r)
# (1) system: tri rows = 0, L rows = 1.  Encode RHS as extra bit m.
# RHS stored in bit 0, variables shifted to bits 1..m so that leading bits are variable bits
B = reduce_rows([t << 1 for t in tri] + [(r << 1) | 1 for r in Lrows])
incons = B.get(0) == 1
print("(1) Jorgensen system L=1 everywhere: inconsistent =", incons)
# (2) rank of L modulo triangle space
Bt = reduce_rows(tri)
def red(r, basis):
    while r:
        h = r.bit_length() - 1
        if h in basis: r ^= basis[h]
        else: return r
    return 0
rk_t = len(Bt)
BL = reduce_rows(tri + Lrows)
print("rank(tri) =", rk_t, " rank(tri + L) =", len(BL), " => dim span of L mod tri =", len(BL) - rk_t,
      " ; number of pairs =", len(Lrows), " => left-kernel dimension =", len(Lrows) - (len(BL) - rk_t))
