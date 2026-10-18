"""One (c_min, grids, graph) job: enumerate templates (cle3_templates filters) for the g-th non-grid graph with
21 - grids edges, then run the Gram test (cle3_gram.solve) on each survivor.  Prints one JSON line.
usage: python cle3_one_graph.py <c_min> <grids> <graph index> <gram seconds> [--exact] [--out file]
--exact: some root line has c = c_min (configurations with all root lines c > c_min belong to the next sweep)."""
import json
import sys
import time
from collections import Counter

import cle3_templates as CT
import cle3_gram as GR

kmin, grids, gi, secs = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
exact = "--exact" in sys.argv
reps = [m for m in CT.graph_reps() if bin(m).count("1") == 21 - grids]
if gi >= len(reps):
    print(json.dumps({"c_min": kmin, "grids": grids, "graph": gi, "graphs": len(reps), "skipped": True}))
    sys.exit(0)
CT.graph_reps = lambda: [reps[gi]]
t0 = time.time()
res = CT.run(kmin, exact=exact)
t1 = time.time()
counts, feas = Counter(), []
for t in res["survivors"]:
    r = GR.solve(t, secs)
    counts[r["status"]] += 1
    if r["status"] != "QUOTIENT_INFEASIBLE":
        feas.append({"template": t, "gram": r})
line = {"c_min": kmin, "exact": exact, "grids": grids, "graph": gi, "graphs": len(reps), "mask": reps[gi],
        "templates": res["survivors_up_to_aut"], "gram_counts": dict(counts), "enum_s": round(t1 - t0, 1),
        "gram_s": round(time.time() - t1, 1)}
print(json.dumps(line))
if out:
    json.dump({**line, "open_templates": feas}, open(out, "w"), default=int)
