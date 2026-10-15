"""SAT (LAB 15/10/2026): admissible four-star structure with ALL 24 transversals (t = (12,12): {0,x}~{1,x} for
x = 2..13 and {2,x}~{3,x} for x = 0,1,4..13) and broken star matchings (M_1 != h(M_0), or M_3 != h(M_2) with SIDE=m).
Writes a witness json if SAT.  usage: python twist_sat_full.py <l|m|both> <out json> [seed]"""
import itertools
import json
import random
import sys

from pycryptosat import Solver

sys.path.insert(0, '.')
from stars_rank import build

side, out = sys.argv[1], sys.argv[2]
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 3
S, idx, e, F = build([0, 1, 2, 3], random.Random(seed))
n = len(S)
sol = Solver(options={"polar": "rnd", "seed": str(seed)})
for c in F.clauses:
    sol.add_clause(c)
L = lambda *x: idx[frozenset(x)]
for x in range(2, 14):
    sol.add_clause([e[(L(0, x), L(1, x))]])
for x in [0, 1] + list(range(4, 14)):
    sol.add_clause([e[(L(2, x), L(3, x))]])
h = {0: 1, 1: 0, 2: 3, 3: 2}
nv = F.n


def broken_lits(a, a2):
    global nv
    xs = []
    others = [t for t in range(14) if t not in (a, a2)]
    for y, z in itertools.combinations(others, 2):
        p = e[(L(a, y), L(a, z))]
        q = e[(L(a2, h.get(y, y)), L(a2, h.get(z, z)))]
        nv += 1
        sol.add_clause([-nv, p, q])
        sol.add_clause([-nv, -p, -q])
        xs.append(nv)
    return xs


if side in ("l", "both"):
    sol.add_clause(broken_lits(0, 1))
if side in ("m", "both"):
    sol.add_clause(broken_lits(2, 3))
ok, model = sol.solve()
print("all 24 transversals + broken matchings (%s): %s" % (side, "SAT" if ok else "UNSAT"), flush=True)
if ok:
    json.dump({"labels": [sorted(l) for l in S],
               "edges": [[i, j] for i, j in itertools.combinations(range(n), 2) if model[e[(i, j)]]]}, open(out, "w"))
