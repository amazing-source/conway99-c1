"""Plain admissibility of a star set (LAB 16/10): stars_rank.build + cryptominisat, no base.  Prints SAT (and saves the
structure) or UNSAT.  usage: python plain_sat.py <stars> <out json>"""
import json, random, sys, time
from pycryptosat import Solver
from stars_rank import build
stars = [int(t) for t in sys.argv[1].split(",")]
t0 = time.time()
S, idx, e, F = build(stars, random.Random(7))
sol = Solver(threads=1)
for c in F.clauses:
    sol.add_clause(c)
print("model built: %d labels, %d vars, %d clauses (%.1f s)" % (len(S), F.n, len(F.clauses), time.time() - t0), flush=True)
ok, model = sol.solve()
res = {"stars": stars, "status": "SAT" if ok else "UNSAT", "seconds": time.time() - t0}
if ok:
    n = len(S)
    res["labels"] = [sorted(l) for l in S]
    res["edges"] = [[i, j] for i in range(n) for j in range(i + 1, n) if model[e[(i, j)]]]
json.dump(res, open(sys.argv[2], "w"))
print("stars %s: %s in %.1f s" % (stars, res["status"], res["seconds"]), flush=True)
