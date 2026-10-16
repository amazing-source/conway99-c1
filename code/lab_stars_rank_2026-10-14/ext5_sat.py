"""Independent check of the fifth-star extension (LAB 16/10/2026): stars_rank.build (cryptominisat model, the one used by
all the four-star tools) on the stars of the target set, with the adjacency of a given base structure fixed by unit
clauses.  Prints SAT / UNSAT.
usage: python ext5_sat.py <stars, e.g. 0,1,2,3,4> <base json> [<base json> ...]"""
import itertools
import json
import random
import sys
import time

from pycryptosat import Solver

from stars_rank import build

stars = [int(t) for t in sys.argv[1].split(",")]
for f in sys.argv[2:]:
    t0 = time.time()
    S, idx, e, F = build(stars, random.Random(1))
    sol = Solver()
    for c in F.clauses:
        sol.add_clause(c)
    d = json.load(open(f))
    bl = [frozenset(x) for x in d["labels"]]
    bE = set(tuple(sorted(x)) for x in d["edges"])
    nfix = 0
    for a, b in itertools.combinations(range(len(bl)), 2):
        if bl[a] in idx and bl[b] in idx:
            v = e[(idx[bl[a]], idx[bl[b]])]
            sol.add_clause([v] if (a, b) in bE else [-v])
            nfix += 1
    ok, model = sol.solve()
    print("%s: stars %s, %d fixed pairs -> %s (%.1f s)" % (f.split("/")[-1], stars, nfix, "SAT" if ok else "UNSAT",
                                                         time.time() - t0), flush=True)
