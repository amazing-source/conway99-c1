# independent: orbits of the 114 labelled cores under letter flips of lines 0,1,2 (order 8), and under swap(1,2) x flips
import json, sys
from itertools import product
cores = json.load(open(sys.argv[1]))
reps = json.load(open(sys.argv[2]))["representatives"]
# label = (letter on line 0, letter on other line); index order: Q01 (s,2+t), Q02 (s,4+t)
LAB = [(s, 2 + t) for s in range(2) for t in range(2)] + [(s, 4 + t) for s in range(2) for t in range(2)]
idx = {frozenset(q): i for i, q in enumerate(LAB)}
def act(q, f, swap):
    out = []
    for l in q:
        line, bit = divmod(l, 2)
        if swap and line in (1, 2):
            line = 3 - line
        out.append(2 * line + (bit ^ f[line]))
    return idx[frozenset(out)]
def image(core, f, swap):
    p = [act(q, f, swap) for q in LAB]
    return frozenset(frozenset((p[u], p[v])) for u, v in core["edges"])
E = [frozenset(frozenset(e) for e in c["edges"]) for c in cores]
assert len(set(E)) == len(E) == 114
pos = {e: i for i, e in enumerate(E)}
def orbit(i, swaps):
    return {pos[image(cores[i], f, sw)] for f in product(range(2), repeat=3) for sw in swaps}
orb8 = {}
for i in range(114):
    o = frozenset(orbit(i, (False,)))
    orb8[o] = min(o)
print("flip orbits:", len(orb8), "sizes", sorted(len(o) for o in orb8))
myreps = sorted(orb8.values())
print("my reps == file reps:", myreps == sorted(reps), myreps)
cov = set()
for r in reps:
    cov |= orbit(r, (False,))
print("covered by file reps:", len(cov))
orb16 = {frozenset(orbit(i, (False, True))) for i in range(114)}
print("swap x flip orbits:", len(orb16))
# T must transform consistently (deficit is a function of edges)
def Tof(c):
    nb = [set() for _ in range(8)]
    for u, v in c["edges"]:
        nb[u].add(v); nb[v].add(u)
    out = {}
    for u in range(8):
        for v in range(u + 1, 8):
            sh = len(set(LAB[u]) & set(LAB[v]))
            out["%d-%d" % (u, v)] = 2 - (v in nb[u]) - len(nb[u] & nb[v]) - sh
    return out
print("T consistent with edges for all:", all(Tof(c) == c["T"] for c in cores))
# is the doubly-grid core in the list?
grid01 = frozenset(frozenset(e) for e in [(0,1),(0,2),(1,3),(2,3),(4,5),(4,6),(5,7),(6,7)])
print("double-grid core present:", grid01 in pos)
print("e distribution:", sorted(set(tuple(c["e"]) for c in cores)))
