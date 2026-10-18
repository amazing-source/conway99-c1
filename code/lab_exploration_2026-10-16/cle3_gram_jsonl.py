"""Run the integer Gram test of cle3_gram.py on every template of C++ jsonl files (LAB, 18/10/2026).
usage: python cle3_gram_jsonl.py <seconds per template> <output.json> <file.jsonl>..."""
import json
import sys
import time
from collections import Counter

import cle3_gram as GR

secs, out = float(sys.argv[1]), sys.argv[2]
counts, recs, t0 = Counter(), [], time.time()
for path in sys.argv[3:]:
    for n, line in enumerate(open(path)):
        t = json.loads(line)
        r = GR.solve(t, secs) if t["nongrid_edges"] else {"status": "QUOTIENT_FEASIBLE", "note": "no non-grid rectangle: empty system"}
        counts[r["status"]] += 1
        recs.append({"file": path, "line": n, "nongrid_edges": len(t["nongrid_edges"]),
                     "kernel_dimension": t["kernel_dimension"], "template": t, **r})
json.dump({"counts": dict(counts), "records": recs}, open(out, "w"), default=int)
print(json.dumps({"counts": dict(counts), "seconds": round(time.time() - t0, 1)}))
