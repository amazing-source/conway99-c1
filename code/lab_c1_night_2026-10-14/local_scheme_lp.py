"""Per-vertex spectral bound in the local view of srg(99,14,1,2).

Outer vertices at x = the 84 edges of the cocktail-party graph CP on 14 inner vertices (7 blocks). The group of
block permutations and sign changes has six orbits on ordered pairs of edges e = {a,b}, f:
  R0 f = e;  R1 f = {a,-b} or {-a,b};  R2 f = {-a,-b};  R3 f shares one end with e, other ends in different blocks;
  R4 f disjoint from e and contains -a or -b (not both);  R5 f on two other blocks.
Averaging the adjacency A_out of the outer graph over this group gives sum_r y_r R_r, where y_r is the density of
adjacent pairs in relation r. Section 12 of the note gives y3, y4, y5 in terms of
  y1 = (number of pairs (a, block) respected by the local matchings at x) / 84 = (sum of the prism numbers of the
       seven lines through x) / 84,
  y2 = density of adjacencies [a,b] ~ [-a,-b].
The averaged matrix still has all its eigenvalues on the 70-dimensional space (zero sum around each inner vertex)
inside [-4, 3], because 3 I - A_out and A_out + 4 I are positive semidefinite there. This script computes the
common eigenspaces of the R_r and prints the resulting constraints on (y1, y2). numpy, a few seconds.
"""
import itertools

import numpy as np

inner = list(range(14))
mate = {a: a ^ 1 for a in inner}
edges = [(a, b) for a in inner for b in inner if a < b and mate[a] != b]
idx = {e: i for i, e in enumerate(edges)}
n = len(edges)
assert n == 84


def rel(e, f):
    if e == f:
        return 0
    se, sf = set(e), set(f)
    common = se & sf
    mates_e = {mate[v] for v in e}
    if len(common) == 1:
        (o1,) = se - common
        (o2,) = sf - common
        return 1 if mate[o1] == o2 else 3
    m = len(mates_e & sf)
    if m == 2:
        return 2
    if m == 1:
        return 4
    return 5


R = [np.zeros((n, n)) for _ in range(6)]
for e in edges:
    for f in edges:
        R[rel(e, f)][idx[e], idx[f]] = 1
print("valencies:", [int(r[0].sum()) for r in R])

# common eigenspaces: diagonalise a generic combination
rng = np.random.default_rng(1)
gen = sum(c * r for c, r in zip(rng.normal(size=6), R))
w, v = np.linalg.eigh(gen)
groups = []
for i in range(n):
    if groups and abs(w[i] - w[groups[-1][0]]) < 1e-8:
        groups[-1].append(i)
    else:
        groups.append([i])
print("eigenspaces (dimensions):", [len(g) for g in groups])
N = np.zeros((14, n))
for e in edges:
    N[e[0], idx[e]] = 1
    N[e[1], idx[e]] = 1
table = []
for g in groups:
    vec = v[:, g[0]]
    lam = [float(vec @ r @ vec) for r in R]
    inK = bool(np.allclose(N @ v[:, g], 0, atol=1e-8))
    table.append((len(g), inK, lam))
    print("dim %2d  in K: %-5s  eigenvalues of R0..R5: %s" % (len(g), inK, np.round(lam, 6)))


def theta(lam, y1, y2):
    y3 = (1 - y1) / 10
    y4 = (1 - y1 - y2) / 10
    y5 = (8 + 2 * y1 + y2) / 40
    return y1 * lam[1] + y2 * lam[2] + y3 * lam[3] + y4 * lam[4] + y5 * lam[5]


print("eigenvalue of the averaged outer graph on each eigenspace, as c0 + c1 y1 + c2 y2:")
for dim, inK, lam in table:
    c0 = theta(lam, 0, 0)
    c1 = theta(lam, 1, 0) - c0
    c2 = theta(lam, 0, 1) - c0
    print("  dim %2d in K %-5s : %.6f + (%.6f) y1 + (%.6f) y2" % (dim, inK, c0, c1, c2))

# feasible region: y1, y2 >= 0, y4 >= 0 (y1 + y2 <= 1), eigenvalues on K in [-4, 3], trace on K = 0
best = None
grid = 2001
feasible = []
for i in range(grid):
    y1 = i / (grid - 1)
    for j in range(grid - i):
        y2 = j / (grid - 1)
        ok = True
        tr = 0.0
        for dim, inK, lam in table:
            if inK:
                t = theta(lam, y1, y2)
                tr += dim * t
                if t > 3 + 1e-9 or t < -4 - 1e-9:
                    ok = False
                    break
        if ok:
            feasible.append((y1, y2, tr))
if feasible:
    ymax = max(feasible)
    print("largest feasible y1: %.4f (at y2 = %.4f); in number of respected pairs out of 84: %.2f" % (ymax[0], ymax[1], 84 * ymax[0]))
    print("trace on K over the feasible points: min %.4f max %.4f (must be 0 for a real graph; check it is identically 0)" % (min(t for _, _, t in feasible), max(t for _, _, t in feasible)))
    print("y2 range over feasible points: %.4f .. %.4f" % (min(p[1] for p in feasible), max(p[1] for p in feasible)))
else:
    print("no feasible point")
