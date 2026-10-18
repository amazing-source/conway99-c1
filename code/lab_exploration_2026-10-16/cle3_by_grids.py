"""Root templates by the exact number of grids at the root (LAB 18/10/2026), on top of cle3_templates.py (filters P, O',
S', Z, K, all proved there).  usage: python cle3_by_grids.py <c_min (all root lines c >= c_min)> <grids at root> [--out survivors.json]"""
import json
import sys
import time

import cle3_templates as CT

kmin, grids = int(sys.argv[1]), int(sys.argv[2])
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
reps_all = CT.graph_reps()
keep = [m for m in reps_all if bin(m).count("1") == 21 - grids]
CT.graph_reps = lambda: keep
t0 = time.time()
res = CT.run(kmin, exact=False)
print(json.dumps({"c_min_at_root": kmin, "grids_at_root": grids, "graphs": len(keep), "stats": res["stats"],
                  "survivors_up_to_aut": res["survivors_up_to_aut"], "kernel_dim_hist": res["kernel_dimension_histogram"],
                  "seconds": round(time.time() - t0, 1)}))
if out:
    json.dump({"c_min_at_root": kmin, "grids_at_root": grids, "survivors": res["survivors"]}, open(out, "w"))
