"""Universal column relations at a vertex (LAB 19/10/2026).  At every root a, sum_{b != a} H_ab = 0 (quotas of the two
letters of a; independent of the template).  For a bipartition (X, Y) of the 7 lines, summing over X and subtracting
over Y gives  sum_{e inside X} H_e = sum_{e inside Y} H_e;  grid rectangles have H = 0.  These relations hold at EVERY
vertex of a Conway graph, whatever its blocks.  For each template we list the bipartitions whose relation, after
removing grids, has 1 term (immediate contradiction) or 2 terms (opposite pair inside one side, or equal pair across),
with the shape of the pair (disjoint / touching) and of the grids around it.
usage: python universal_relations_scan.py <catalogue.json.gz> <open.tsv | all>"""
import gzip
import json
import sys
from collections import Counter
from itertools import combinations

recs = json.load(gzip.open(sys.argv[1]))["open"]
sel = None if sys.argv[2] == "all" else {int(l.split()[1]) for l in open(sys.argv[2]) if l.startswith("gz")}
stats = Counter(); per = {}
for idx, r in enumerate(recs):
    if sel is not None and idx not in sel:
        continue
    t = r["template"]
    ng = {tuple(e) for e in t["nongrid_edges"]}
    found = []
    for size in (2, 3):
        for Y in combinations(range(7), size):
            X = [v for v in range(7) if v not in Y]
            xi = [e for e in combinations(X, 2) if e in ng]
            yi = [e for e in combinations(Y, 2) if e in ng]
            n = len(xi) + len(yi)
            if n == 1:
                found.append(("ONE", tuple(X), xi + yi))
            elif n == 2:
                if len(xi) == 2 or len(yi) == 2:
                    pair = xi if len(xi) == 2 else yi
                    shape = "touching" if set(pair[0]) & set(pair[1]) else "disjoint"
                    found.append(("OPP-" + shape, tuple(X), pair))
                else:
                    found.append(("EQ", tuple(X), xi + yi))
    kinds = sorted({f[0] for f in found})
    stats[(t["kernel_dimension"], tuple(kinds))] += 1
    per[idx] = found
for k, v in sorted(stats.items()):
    print(k, v)
json.dump({str(k): v for k, v in per.items()}, open("universal_relations_%s.json" % ("open" if sel is not None else "all"), "w"))
