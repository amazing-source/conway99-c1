"""Run Codex's root_component_corner_moment_bounds.analyze_gram, unchanged, on some Grams of a cover (LAB, 18/10/2026).
A separate process, so that Codex's modules of that commit never mix with the other Codex modules of the model.
usage: python codex_moment_batch.py <codex dir> <cover json(.gz)> <comma-separated Gram numbers> <out.json>"""
import gzip
import json
import sys
import time
from pathlib import Path

codex, cover_path, picks, out = Path(sys.argv[1]), sys.argv[2], [int(x) for x in sys.argv[3].split(",") if x], sys.argv[4]
sys.path.insert(0, str(codex.resolve()))
import root_component_corner_moment_bounds as CMB      # noqa: E402

cover = json.load(gzip.open(cover_path, "rt") if cover_path.endswith(".gz") else open(cover_path))
edges = [tuple(e) for e in cover["edges"]]
res = {}
for k in picks:
    t0 = time.process_time()
    try:
        r = CMB.analyze_gram(edges, cover["grams"][k])
        res[k] = {"status": r.get("status"), "cpu": round(time.process_time() - t0, 2)}
    except Exception as exc:                            # e.g. rank > 5: no verdict
        res[k] = {"status": "ERROR", "error": str(exc)[:200]}
json.dump(res, open(out, "w"))
