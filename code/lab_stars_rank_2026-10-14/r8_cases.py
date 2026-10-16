"""Case split of R8 by the matching M_0 of L_0, up to the stabiliser of the letter 0 (LAB 16/10/2026).
R8 = stars 0..3 exact + the eight labels {4,t} (t = 6..13), letter 4 only bounded, C1' bounds, C2 caps (five_cnf.py
--xk 8).  Its symmetry group G (order 3072) contains G_0 = {g : g(0) = 0} = <(2 3)> x hyperoctahedral group on the
outer lines (order 768).  Every solution can be moved by G so that ... the matching M_0 of L_0 (each label {0,s} has
exactly one neighbour in L_0) is the canonical representative of its G_0-orbit; so it suffices to solve one case per
orbit.  This script lists the orbits (the M_0 matchings are perfect matchings of the 12 letters s with {0,s} a label).
usage: python r8_cases.py [--list]"""
import itertools
import sys

pts = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]           # {0,s} for these s are the 12 labels of L_0


def matchings(p):
    if not p:
        yield []
        return
    a = p[0]
    for i in range(1, len(p)):
        rest = p[1:i] + p[i + 1:]
        for m in matchings(rest):
            yield [(a, p[i])] + m


outer = [(6, 7), (8, 9), (10, 11), (12, 13)]
G0 = []
for sw in (False, True):
    for perm in itertools.permutations(range(4)):
        for flips in itertools.product((0, 1), repeat=4):
            g = {2: 3, 3: 2} if sw else {2: 2, 3: 3}
            g[4], g[5] = 4, 5
            for q, (a, b) in enumerate(outer):
                c, d = outer[perm[q]]
                if flips[q]:
                    c, d = d, c
                g[a], g[b] = c, d
            G0.append(g)
assert len(G0) == 768


def canon(m):
    return min(tuple(sorted(tuple(sorted((g[a], g[b]))) for a, b in m)) for g in G0)


reps = {}
for m in matchings(pts):
    c = canon(m)
    reps[c] = reps.get(c, 0) + 1
reps = sorted(reps.items())
print("%d perfect matchings of L_0, %d orbits under G_0 (order 768)" % (sum(v for _, v in reps), len(reps)))
if "--list" in sys.argv:
    for k, (r, sz) in enumerate(reps):
        print(k, sz, r)
