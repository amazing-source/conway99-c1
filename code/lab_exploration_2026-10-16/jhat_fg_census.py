"""Stage 1 of the global c <= 2 pass: lemma FG (forced grid) on one census file (LAB, 18/10/2026).

Reads a census file (jsonl.gz, one template per line, with its 'canonical' string), keeps the first line of every
canonical string (equal canonical strings are the same template up to relabelling, so they share every verdict),
applies forced_grid_walk (jhat_rows.py, exact BFS; proof in lemmas_c12_2026-10-18/LEMMES_C12_2026-10-18.md, sec. 3)
and writes the survivors and a summary.
usage: python jhat_fg_census.py <census.jsonl.gz> <out prefix>
       -> <out prefix>.surv.jsonl.gz (one surviving template per line, unchanged) and <out prefix>.sum.json"""
import gzip
import json
import sys
import time
from collections import Counter

from jhat_rows import block_graph, forced_grid_walk

src, out = sys.argv[1], sys.argv[2]
t0 = time.time()
seen = set()
lines = dups = killed = alive = 0
dims_killed, dims_alive, first_q = Counter(), Counter(), Counter()
with gzip.open(src, "rt") as fh, gzip.open(out + ".surv.jsonl.gz", "wt", compresslevel=6) as fo:
    for line in fh:
        if not line.strip():
            continue
        lines += 1
        t = json.loads(line)
        key = bytes.fromhex(t["canonical"]) if all(c in "0123456789abcdef" for c in t["canonical"]) else t["canonical"]
        if key in seen:
            dups += 1
            continue
        seen.add(key)
        graph = block_graph(t)
        hit = next((q for q in graph[0] if forced_grid_walk(t, q, graph)), None)
        d = t.get("kernel_dimension")
        if hit is not None:
            killed += 1
            dims_killed[d] += 1
        else:
            alive += 1
            dims_alive[d] += 1
            fo.write(line if line.endswith("\n") else line + "\n")
summary = {"source": src, "lines": lines, "duplicate_canonical_lines": dups, "unique": len(seen),
           "forced_grid_unique": killed, "survivors_unique": alive,
           "by_kernel_dimension": {str(k): {"forced_grid": dims_killed[k], "survivors": dims_alive[k]}
                                   for k in sorted(set(dims_killed) | set(dims_alive), key=lambda x: (x is None, x))},
           "seconds": round(time.time() - t0, 1)}
json.dump(summary, open(out + ".sum.json", "w"), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != "by_kernel_dimension"}))
