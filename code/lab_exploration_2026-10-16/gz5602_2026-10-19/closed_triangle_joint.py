"""Joint system of three pairwise disjoint grids X, Y, Z whose three pairs are CLOSED (LAB 19/10/2026; closed_grid_pairs.py).
For the closed pair (X, Y) the C2 equality reads, for u in X and v in Y:
   2 - [pi_XY(u) = v] - [pi_XY(u) ~_Y v] - [pi_XY^-1(v) ~_X u] = sum over middle grids K of [sigma_K(u) = v],
the middle grids being the grids disjoint from X and Y; Z is one of them, with sigma_Z = pi_YZ^-1 o pi_XZ; the other
middle grids K appear in no other closed pair of the triangle, so their sigma_K are free bijections X -> Y (any
bijection is realised by choosing pi_XK, pi_YK).  After removing [sigma_Z(u) = v] the remainder must therefore be the
sum of (number of free middle grids) permutation matrices: nonnegative with constant row and column sums (a k-regular
bipartite multigraph on 4 + 4 vertices always splits into k perfect matchings, Koenig).
Counts the triples (pi_XY, pi_XZ, pi_YZ) satisfying the three closed-pair systems simultaneously.
usage: python closed_triangle_joint.py <catalogue.json.gz> <index> <X> <Y> <Z>   (grids as 'ab')"""
import gzip
import json
import sys
from itertools import combinations, permutations

recs = json.load(gzip.open(sys.argv[1]))["open"]
t = recs[int(sys.argv[2])]["template"]
X, Y, Z = [tuple(int(c) for c in g) for g in sys.argv[3:6]]
ng = {tuple(e) for e in t["nongrid_edges"]}
grids = [q for q in combinations(range(7), 2) if q not in ng]
CORN = [(0, 0), (0, 1), (1, 1), (1, 0)]
PERMS = list(permutations(range(4)))


def adj(i, j):
    a, b = CORN[i], CORN[j]
    return (a[0] == b[0]) != (a[1] == b[1])


def closed(G, H):
    four = set(G) | set(H)
    return not (set(G) & set(H)) and not any(not (set(q) & four) for q in ng)


for G, H in [(X, Y), (X, Z), (Y, Z)]:
    assert closed(G, H), (G, H)


def middles(G, H):
    four = set(G) | set(H)
    return [K for K in grids if K not in (G, H) and not (set(K) & four)]


def inv(p):
    q = [0] * 4
    for u in range(4):
        q[p[u]] = u
    return tuple(q)


def comp(p, q):          # p o q
    return tuple(p[q[u]] for u in range(4))


def ok(pi, sigma_third, free):
    pinv = inv(pi)
    for u in range(4):
        rows = 0
        for v in range(4):
            r = 2 - (pi[u] == v) - adj(pi[u], v) - adj(pinv[v], u) - (sigma_third[u] == v)
            if r < 0:
                return False
        # row / column sums of the remainder must all equal `free`
    rem = [[2 - (pi[u] == v) - adj(pi[u], v) - adj(pinv[v], u) - (sigma_third[u] == v) for v in range(4)] for u in range(4)]
    return all(sum(rem[u]) == free for u in range(4)) and all(sum(rem[u][v] for u in range(4)) == free for v in range(4))


mXY, mXZ, mYZ = middles(X, Y), middles(X, Z), middles(Y, Z)
assert Z in mXY and Y in mXZ and X in mYZ
fXY, fXZ, fYZ = len(mXY) - 1, len(mXZ) - 1, len(mYZ) - 1
count = 0
for pXY in PERMS:
    for pXZ in PERMS:
        for pYZ in PERMS:
            # (X,Y): sigma_Z = pYZ^-1 o pXZ ; (X,Z): sigma_Y = pZY^-1 o pXY = pYZ o pXY ; (Y,Z): sigma_X = pZX^-1 ... from Y to Z
            sZ = comp(inv(pYZ), pXZ)
            sY = comp(pYZ, pXY)
            sX = comp(pXZ, inv(pXY))          # Y -> X -> Z
            if ok(pXY, sZ, fXY) and ok(pXZ, sY, fXZ) and ok(pYZ, sX, fYZ):
                count += 1
print(json.dumps({"index": int(sys.argv[2]), "triangle": ["%d%d" % X, "%d%d" % Y, "%d%d" % Z],
                  "middle": {"XY": ["%d%d" % K for K in mXY], "XZ": ["%d%d" % K for K in mXZ], "YZ": ["%d%d" % K for K in mYZ]},
                  "joint_solutions": count, "of": 24 ** 3}))
