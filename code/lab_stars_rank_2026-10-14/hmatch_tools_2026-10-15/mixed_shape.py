"""The h-inhomogeneous kernel direction of a broken structure (LAB 15/10/2026, task T3, exact).
N = ker T, Nh = N n hN (= ker(M + hMh) when T >= 0).  Picks x in N outside Nh (reduced modulo Nh on the labels where
possible) and prints its even part x_+ = (x + hx)/2 and odd part x_- = (x - hx)/2 in the orbit bases
(u_y = 1_0y + 1_1y, g_z = 1_2z + 1_3z, c1, c2 even; e_y = 1_0y - 1_1y, f_z = 1_2z - 1_3z, k1 = 1_02 - 1_13, k2 = 1_03 - 1_12
odd), plus the star-matching data M_0, M_1, M_2, M_3 restricted to the outer letters.
usage: python mixed_shape.py <json>"""
import json, sys
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from stars_rank import kval
from cls_decomp import nullspace_int
d = json.load(open(sys.argv[1]))
S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
E = {frozenset((S[a], S[b])) for a, b in d["edges"]}
M8 = [[(24 if a == b else 0) - 8 * (1 if frozenset((S[a], S[b])) in E else 0) - int(round(8 * kval(S[a], S[b]))) for b in range(n)] for a in range(n)]
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
N = nullspace_int(M8)
Mh = [[M8[a][b] + M8[hp[a]][hp[b]] for b in range(n)] for a in range(n)]
Nh = nullspace_int(Mh)
print("nullity %d, dim N n hN = %d" % (len(N), len(Nh)))
def rank(vs):
    A = [[Fr(x) for x in v] for v in vs]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r
base = rank(Nh)
for v in N:
    if rank(Nh + [v]) > base:
        x = v; break
L = lambda a, b: idx[frozenset((a, b))]
hx = [x[hp[i]] for i in range(n)]
xp = [Fr(x[i] + hx[i], 2) for i in range(n)]
xm = [Fr(x[i] - hx[i], 2) for i in range(n)]
fmt = lambda pairs: ", ".join("%s:%s" % (k, v) for k, v in pairs if v != 0)
ev = [("u%d" % y, xp[L(0, y)]) for y in range(4, 14)] + [("g%d" % z, xp[L(2, z)]) for z in range(4, 14)] + [("c1", xp[L(0, 2)]), ("c2", xp[L(0, 3)])]
od = [("e%d" % y, xm[L(0, y)]) for y in range(4, 14)] + [("f%d" % z, xm[L(2, z)]) for z in range(4, 14)] + [("k1", xm[L(0, 2)]), ("k2", xm[L(0, 3)])]
print("even part x_+:", fmt(ev))
print("odd part  x_-:", fmt(od))
for a in range(4):
    pairs = sorted({tuple(sorted([y for y in S[i] if y != a][0:1] + [y for y in S[j] if y != a][0:1])) for i in range(n) for j in range(n)
                    if i < j and a in S[i] and a in S[j] and frozenset((S[i], S[j])) in E})
    print("M_%d: %s" % (a, pairs))
