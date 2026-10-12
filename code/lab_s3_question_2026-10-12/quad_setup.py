"""Lab session, 2026-10-12. Algebraic form of the parity skeleton problem over F_2, for linearisation.

A parity skeleton class is a point eps of H^1 = Z^1 / B^1 (dimension 460): line-even edge functions modulo switching.
For a non-adjacent pair p with path parities pi_0..pi_5 (linear forms on H^1 once a gauge is fixed), put
rho_i = pi_i + pi_0 (i = 1..5) and L_p = rho_1 + ... + rho_5 (the parity of the bundle of p).
FACT (checked below on the 32 patterns): the weight of (pi_0..pi_5) is 0, 3 or 6  iff
      rho_i (1 + L_p) = 0  for i = 1..5      and      e_2(rho_1..rho_5) + L_p = 0,
i.e. the skeletons are the common zeros of 6 x 2430 quadrics on F_2^460 (5 x 2430 independent ones).

This script fixes the gauge (edges at P = 0 and one edge of every far vertex are 0), solves the 270 line equations,
keeps 460 free edge variables, and writes for every pair the five vectors rho_i in F_2^460 (hexadecimal), for quad_xl.c.
python quad_setup.py <out file>"""
import sys, itertools
from local_lib import *

# check of the FACT
for bits in itertools.product((0, 1), repeat=5):
    w6 = sum(bits); ok_w = (w6 in (0, 3))                       # pattern (0, rho): weight of rho is 0 or 3 <=> weight of pi in {0,3,6}
    Lp = sum(bits) % 2; e2 = sum(bits[i] * bits[j] for i in range(5) for j in range(i + 1, 5)) % 2
    quad = all(bits[i] * (1 + Lp) % 2 == 0 for i in range(5)) and (e2 + Lp) % 2 == 0
    assert ok_w == quad, bits

P = 0
edges = [(i, j) for i in range(n) for j in sorted(nbs[i]) if i < j]; eidx = {e: k for k, e in enumerate(edges)}
far = [r for r in range(n) if r != P and r not in nbs[P]]
fixed = {eidx[key(P, z)] for z in nbs[P]} | {eidx[key(r, CN[key(P, r)][0])] for r in far}
assert len(fixed) == 80
lines = sorted({tuple(sorted((i, j, next(iter(nbs[i] & nbs[j]))))) for (i, j) in edges})
# Gaussian elimination on the unknown edges (bit k of an int = edge k): equations = lines (sum of three edges = 0)
piv = {}                                                         # pivot edge -> equation (int), reduced
for t in lines:
    v = 0
    for a, b in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2])):
        k = eidx[key(a, b)]
        if k not in fixed: v ^= 1 << k
    while v:
        p = v.bit_length() - 1
        if p in piv: v ^= piv[p]
        else: piv[p] = v; break
assert len(piv) == 270
free = [k for k in range(810) if k not in fixed and k not in piv]; assert len(free) == 460
fpos = {k: i for i, k in enumerate(free)}
# full reduction: express every pivot edge through free edges
expr = {}
for k in fixed: expr[k] = 0
for k in free: expr[k] = 1 << fpos[k]
for p in sorted(piv):                                            # increasing pivots: lower terms already expressed
    v = piv[p] ^ (1 << p); acc = 0
    while v:
        b = v.bit_length() - 1; v ^= 1 << b
        acc ^= expr[b]
    expr[p] = acc
for t in lines: assert expr[eidx[key(t[0], t[1])]] ^ expr[eidx[key(t[1], t[2])]] ^ expr[eidx[key(t[0], t[2])]] == 0
Ex = lambda a, b: expr[eidx[key(a, b)]]
out = open(sys.argv[1], "w", newline="\n"); npairs = 0
for (a, b), c in sorted(CN.items()):
    pi = [Ex(a, z) ^ Ex(z, b) for z in c]
    out.write("%d %d %s\n" % (a, b, " ".join("%x" % (pi[i] ^ pi[0]) for i in range(1, 6)))); npairs += 1
out.close()
print("460 free edge variables; %d pairs written (five vectors rho_i each) to %s" % (npairs, sys.argv[1]))
