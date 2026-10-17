import itertools, random, numpy as np, sys
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
G = PermutationGroup([Permutation(g) for g in gens])
random.seed(7); reps = {}
for _ in range(40000):
    g = G.random(); k = g.order()
    for p in (3, 5):
        if k % p == 0:
            h = g ** (k // p); a = h.array_form
            fixed = [x for x in range(81) if a[x] == x]
            fe = sum(1 for x in range(81) for y in range(x + 1, 81) if Q[x, y] and {a[x], a[y]} == {x, y})
            # invariant: cycle type, fixed points, fixed edges, edges inside fixed set, #orbits on edges
            ef = int(Q[np.ix_(fixed, fixed)].sum()) // 2 if fixed else 0
            key = (p, len(fixed), fe, ef)
            reps.setdefault(key, h)
print(sorted(reps.keys()))
import pickle; pickle.dump({k: v.array_form for k, v in reps.items()}, open("oddreps.pkl", "wb"))
