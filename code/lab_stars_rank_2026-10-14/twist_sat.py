"""SAT check (LAB 15/10/2026): can an admissible four-star structure have all ten outer transversals of l
({0,y} ~ {1,y}, y = 4..13) and yet M_1 != h(M_0)?  (optionally also the two cross transversals).
usage: python twist_sat.py [cross]"""
import itertools
import random
import sys

from pycryptosat import Solver

from stars_rank import build

rng = random.Random(3)
S, idx, e, F = build([0, 1, 2, 3], rng)
n = len(S)
sol = Solver()
for c in F.clauses:
    sol.add_clause(c)
L = lambda *x: idx[frozenset(x)]
for y in range(4, 14):
    sol.add_clause([e[(L(0, y), L(1, y))]])
if len(sys.argv) > 1 and sys.argv[1] == "cross":
    sol.add_clause([e[(L(0, 2), L(1, 2))]])
    sol.add_clause([e[(L(0, 3), L(1, 3))]])
h = {0: 1, 1: 0, 2: 3, 3: 2}
others = list(range(2, 14))
xs = []
nv = F.n
for y, z in itertools.combinations(others, 2):
    a = e[(L(0, y), L(0, z))]
    b = e[(L(1, h.get(y, y)), L(1, h.get(z, z)))]
    nv += 1
    x = nv                      # x -> (a xor b)
    sol.add_clause([-x, a, b])
    sol.add_clause([-x, -a, -b])
    xs.append(x)
sol.add_clause(xs)
ok, model = sol.solve()
print("all outer l-transversals%s + M_1 != h(M_0): %s" % (" + cross" if len(sys.argv) > 1 else "", "SAT" if ok else "UNSAT"))
if ok:
    for a in (0, 1):
        M = sorted((y, z) for y, z in itertools.combinations([t for t in range(14) if t not in (a, a ^ 1)], 2)
                   if model[e[(L(a, y), L(a, z))]])
        print("M_%d:" % a, M)
