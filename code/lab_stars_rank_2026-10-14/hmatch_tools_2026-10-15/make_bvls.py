"""Berlekamp-van Lint-Seidel srg(243,22,1,2): Cayley graph on GF(3)^5, connection set {+-h_i}, h_i = x^i mod g(x),
g | x^11 - 1 over GF(3) of degree 5 (construction as in work/checks/c03_bvls_m11.py).  Writes an edge list.
usage: python make_bvls.py <out edges file>"""
import itertools
import sys

p = 3


def polymod(a, g):
    a = a[:]
    while len(a) >= len(g):
        c = a[-1] % p
        if c:
            sh = len(a) - len(g)
            for i, gi in enumerate(g):
                a[sh + i] = (a[sh + i] - c * gi) % p
        a.pop()
    return [x % p for x in a] + [0] * (len(g) - 1 - len(a))


x11m1 = [p - 1] + [0] * 10 + [1]
g = None
for coeffs in itertools.product(range(3), repeat=5):
    cand = list(coeffs) + [1]
    if coeffs[0] == 0:
        continue
    if all(v == 0 for v in polymod(x11m1, cand)) and cand != [p - 1, 1]:
        g = cand
        break
h = [tuple(polymod([0] * i + [1], g)) for i in range(11)]
S = set()
for v in h:
    S.add(v)
    S.add(tuple((-c) % 3 for c in v))
assert len(S) == 22
V = list(itertools.product(range(3), repeat=5))
ix = {v: i for i, v in enumerate(V)}
E = set()
for v in V:
    for s in S:
        w = tuple((a + b) % 3 for a, b in zip(v, s))
        i, j = ix[v], ix[w]
        E.add((min(i, j), max(i, j)))
with open(sys.argv[1], "w") as fh:
    for i, j in sorted(E):
        fh.write("%d %d\n" % (i, j))
print("g =", g, "edges", len(E))
