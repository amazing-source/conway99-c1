"""Stage 1 of the global c <= 2 pass, key version (LAB, 18/10/2026): lemma FG on every line of one census file, and
the S7 key (census_key.py) of every survivor, written sorted and unique.  Equal keys are the same template up to S7.
usage: python jhat_fg_census2.py <census.jsonl.gz> <out prefix>
       -> <out prefix>.surv.keys.gz (sorted unique S7 keys of the FG survivors) and <out prefix>.sum.json"""
import gzip
import json
import sys
import time
from collections import Counter

from census_key import template_key
from jhat_rows import block_graph, forced_grid_walk

src, out = sys.argv[1], sys.argv[2]
t0 = time.time()
lines = killed = 0
dk, da = Counter(), Counter()
keys = set()
with gzip.open(src, "rt") as fh:
    for line in fh:
        if not line.strip():
            continue
        lines += 1
        t = json.loads(line)
        graph = block_graph(t)
        d = t.get("kernel_dimension")
        if any(forced_grid_walk(t, q, graph) for q in graph[0]):
            killed += 1
            dk[d] += 1
        else:
            da[d] += 1
            keys.add(template_key(t))
with gzip.open(out + ".surv.keys.gz", "wt") as fo:
    for k in sorted(keys):
        fo.write(k + "\n")
s = {"source": src, "lines": lines, "forced_grid_lines": killed, "survivor_lines": lines - killed,
     "survivor_keys": len(keys),
     "by_kernel_dimension": {str(x): {"forced_grid": dk[x], "survivors": da[x]} for x in sorted(set(dk) | set(da))},
     "seconds": round(time.time() - t0, 1)}
json.dump(s, open(out + ".sum.json", "w"), indent=1)
print(json.dumps({k: v for k, v in s.items() if k != "by_kernel_dimension"}))
