"""Stage 2 of the global c <= 2 pass (LAB, 18/10/2026), on S7 keys that survived lemma FG.
For each key: R1 (jhat_design.py, first-order global design, CP-SAT verdict, bounds kept in Python), then for the R1
survivors Codex's Farkas certificate on the full count design (jhat_zpipeline.run with design_seconds = 0: Codex's
linear_system + find_certificate unchanged, DFS catalogue, integer re-check of the certificate).
usage: python jhat_stage2.py <codex dir> <keys.gz> <first> <last> <out prefix> [--r1-seconds S]
       -> <out prefix>.jsonl (one verdict line per key) and <out prefix>.open.keys.gz (keys left open)"""
import gzip
import json
import sys
import time

codex = sys.argv[1]
sys.path.insert(0, codex)
from jhat_design import design            # noqa: E402
from jhat_zpipeline import run as zrun    # noqa: E402
from jhat_fg_keys import decode           # noqa: E402

src, first, last, out = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
r1s = float(sys.argv[sys.argv.index("--r1-seconds") + 1]) if "--r1-seconds" in sys.argv else 10.0
t0 = time.time()
with gzip.open(src, "rt") as fh, open(out + ".jsonl", "w") as fo, gzip.open(out + ".open.keys.gz", "wt") as fk:
    for i, line in enumerate(fh):
        if i < first:
            continue
        if i >= last:
            break
        key = line.strip()
        if not key:
            continue
        t, _ = decode(key)
        rec = {"key": key, "dim": t["kernel_dimension"]}
        st, wall = design(t, "R1", r1s)
        rec["r1"] = st
        rec["r1_wall"] = round(wall, 3)
        if st != "INFEASIBLE":
            z = zrun(t, design_seconds=0)
            rec["lp"] = z["status"]
            rec["lp_cpu"] = z.get("cpu_seconds")
            if z["status"] != "EXCLUDED_BY_INTEGER_CERTIFICATE":
                fk.write(key + "\n")
        fo.write(json.dumps(rec) + "\n")
        fo.flush()
print(json.dumps({"source": src, "range": [first, last], "seconds": round(time.time() - t0, 1)}))
