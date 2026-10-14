"""Brute-force check, on the real srg(243,22,1,2), of the general formulas of NOTE_NIGHT 25.1 (they use only
lambda = 1, mu = 2): non-adjacent pairs, induced paths, edge + far vertex, far edges of an edge, independent triples."""
import itertools
from math import comb

A6x5 = [(1, 1, 1, 1, 1), (0, 1, 2, 2, 1), (1, 0, 1, 2, 2), (2, 1, 0, 1, 2), (2, 2, 1, 0, 1), (1, 2, 2, 1, 0)]
cols = [tuple((-a) % 3 for a in row) for row in A6x5] + [tuple(1 if i == j else 0 for i in range(5)) for j in range(5)]
conn = set(cols) | {tuple((-c) % 3 for c in h) for h in cols}
verts = list(itertools.product(range(3), repeat=5))
idx = {v: i for i, v in enumerate(verts)}
n, k = len(verts), 22
nb = [set() for _ in range(n)]
for v in verts:
    for h in conn:
        nb[idx[v]].add(idx[tuple((a + b) % 3 for a, b in zip(v, h))])
adj = lambda a, b: b in nb[a]
edges = [(a, b) for a in range(n) for b in nb[a] if a < b]
# brute force counts over triples
t = [0, 0, 0, 0]
for a, b, c in itertools.combinations(range(n), 3):
    t[adj(a, b) + adj(a, c) + adj(b, c)] += 1
# far edges of one edge (same for all edges by the formula; check a sample)
def far_edges(x, y):
    R = [z for z in range(n) if z not in (x, y) and not adj(z, x) and not adj(z, y)]
    Rs = set(R)
    return len(R), sum(1 for z in R for w in nb[z] if w in Rs) // 2
samples = {far_edges(*e) for e in edges[::97]}
print("brute force: independent", t[0], "one edge", t[1], "paths", t[2], "lines", t[3], "far set / far edges", samples)
lines = n * k // 6
paths = n * (comb(k, 2) - k // 2)
one = (n * k // 2) * (n - 2 * k + 1)
R = n - 2 * k + 1
eR = ((k - 2) * (k - 3) + (R - (k - 2)) * (k - 4)) // 2
print("formulas:    independent", comb(n, 3) - lines - paths - one, "one edge", one, "paths", paths, "lines", lines,
      "far set / far edges", (R, eR))

# induced P4 (a-b-c-d with a!~c, b!~d, a!~d), counted as undirected paths, versus n (C(k,2) - k/2)(k - 3)
p4 = 0
for b_ in range(n):
    for a_ in nb[b_]:
        for c_ in nb[b_]:
            if c_ == a_ or adj(a_, c_):
                continue
            for d_ in nb[c_]:
                if d_ in (a_, b_) or adj(d_, b_) or adj(d_, a_):
                    continue
                p4 += 1
print("induced P4: brute force", p4 // 2, " formula", paths * (k - 3))
# claws (center with 3 pairwise non-adjacent neighbours) versus n * C(k/2, 3) * 8
claw = 0
for v in range(n):
    L = sorted(nb[v])
    for a_, b_, c_ in itertools.combinations(L, 3):
        if not adj(a_, b_) and not adj(a_, c_) and not adj(b_, c_):
            claw += 1
print("claws: brute force", claw, " formula", n * comb(k // 2, 3) * 8)
