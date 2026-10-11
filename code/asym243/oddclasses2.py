"""Conjugacy classes of elements of order 3 and 5 in Aut(BH) (order 233280), exactly:
order-3 elements all lie in a Sylow 3-subgroup P (order 729); enumerate P's elements of order 3 and split them into
G-conjugacy classes by computing full conjugacy orbits.  Order 5: Sylow 5 has order 5 (one class up to powers)."""
import itertools, numpy as np, sys, pickle
from sympy.combinatorics import Permutation, PermutationGroup
sys.path.insert(0, ".")
from lib243 import aut
V = list(itertools.product(range(3), repeat=4)); I = {v: i for i, v in enumerate(V)}
q = lambda x: (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3
sub = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b))
Q = np.zeros((81, 81), dtype=np.int64)
for a in V:
    for b in V:
        if a != b and q(sub(a, b)) == 0: Q[I[a], I[b]] = 1
o, orb, gens = aut(Q)
G = PermutationGroup([Permutation(g) for g in gens]); N = G.order()
P = G.sylow_subgroup(3); print("|G| =", N, "|Sylow3| =", P.order(), flush=True)
els3 = [g for g in P.generate() if g.order() == 3]
print("order-3 elements in P:", len(els3), flush=True)
gl = G.generators
def conj_orbit(h):
    seen = {tuple(h.array_form)}; stack = [h]
    while stack:
        x = stack.pop()
        for g in gl:
            y = g ** -1 * x * g; t = tuple(y.array_form)
            if t not in seen: seen.add(t); stack.append(y)
    return seen
classes = []
remaining = {tuple(g.array_form): g for g in els3}
while remaining:
    k, h = next(iter(remaining.items()))
    orbit = conj_orbit(h)
    classes.append((h, len(orbit)))
    for t in list(remaining):
        if t in orbit: del remaining[t]
    print("class size", len(orbit), "fixed points", sum(1 for x in range(81) if h.array_form[x] == x), flush=True)
P5 = G.sylow_subgroup(5); g5 = [g for g in P5.generate() if g.order() == 5][0]
print("order 5 class size", len(conj_orbit(g5)))
pickle.dump({"3": [h.array_form for h, _ in classes], "5": g5.array_form}, open("oddclasses.pkl", "wb"))
