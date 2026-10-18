"""Split job for roots WITHOUT grid (non-grid graph K7), any c_min (LAB, 18/10/2026).

Root templates (filters P, O', S', Z, K of cle3_templates.py) are enumerated with the partition of root line 0 fixed to
ONE representative of its type (complete up to Aut(K7) = S7, whose stabiliser of line 0 is S6 acting transitively on
the partitions of each type), and the partition of line 1 fixed to its option number j.  Then each surviving template
gets the Gram test of cle3_gram.py.  exact: some root line has c = c_min (the configurations with all root lines
c > c_min belong to the sweep of c_min + 1).
usage: python cle3_k7_split.py <c_min> <exact 0|1> <type of line 0: 6|42|33|222> <option j of line 1> <gram s> [--out f]"""
import json
import sys
import time
from collections import Counter

import cle3_templates as CT
import cle3_gram as GR

kmin, exact, typ, j1, secs = int(sys.argv[1]), bool(int(sys.argv[2])), sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
REP = {"6": ((1, 2, 3, 4, 5, 6),), "42": ((1, 2, 3, 4), (5, 6)), "33": ((1, 2, 3), (4, 5, 6)),
       "222": ((1, 2), (3, 4), (5, 6))}[typ]
K7 = (1 << 21) - 1
original = CT.admissible
NB0, NB1 = (1, 2, 3, 4, 5, 6), (0, 2, 3, 4, 5, 6)
opts1 = original(list(NB1), kmin)
if j1 >= len(opts1):
    print(json.dumps({"c_min": kmin, "type0": typ, "j1": j1, "skipped": True}))
    sys.exit(0)


def patched(items, k):
    full = original(items, k)
    if tuple(items) == NB0:
        return [o for o in full if o[0] == REP]
    if tuple(items) == NB1:
        return [opts1[j1]]
    return full


CT.admissible = patched
CT.graph_reps = lambda: [K7]
t0 = time.time()
res = CT.run(kmin, exact=exact)
t1 = time.time()
counts, open_t = Counter(), []
for t in res["survivors"]:
    r = GR.solve(t, secs)
    counts[r["status"]] += 1
    if r["status"] != "QUOTIENT_INFEASIBLE":
        open_t.append({"template": t, "gram": r})
line = {"c_min": kmin, "exact": exact, "type0": typ, "j1": j1, "option1": opts1[j1][0], "templates": res["survivors_up_to_aut"],
        "stats": res["stats"], "kernel_hist": res["kernel_dimension_histogram"], "gram_counts": dict(counts),
        "enum_s": round(t1 - t0, 1), "gram_s": round(time.time() - t1, 1)}
print(json.dumps(line))
if out:
    json.dump({**line, "open_templates": open_t}, open(out, "w"), default=int)
