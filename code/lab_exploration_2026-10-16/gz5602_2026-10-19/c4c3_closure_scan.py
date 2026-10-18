"""Scan for the C4+C3 grid pattern (LAB 19/10/2026), closure lemma of Codex (main aa3e8a9e and later):
if the grid graph at a vertex contains a 4-cycle on 4 of its 7 lines and a triangle on the other 3, both diagonals of
the 4-cycle are grids (otherwise H_d1 = -H_d2 from the universal relations sum_{b != a} H_ab = 0, and the exhaustive
enumeration 8 -> 20 -> 36 -> frontier of 5602 applies; it uses only the core and these 7 grids).
A template is killed when its grid graph contains such a C4 + C3 with at least one non-grid diagonal of the C4.
usage: python c4c3_closure_scan.py <catalogue.json.gz | keys file> <open.tsv | all>"""
import gzip
import json
import sys
from collections import Counter
from itertools import combinations, permutations

recs = json.load(gzip.open(sys.argv[1]))["open"]
sel = None if sys.argv[2] == "all" else {int(l.split()[1]) for l in open(sys.argv[2]) if l.startswith("gz")}


def killed(grid):
    """grid: set of frozenset edges among 0..6 that are grid rectangles"""
    for Y in combinations(range(7), 3):
        if not all(frozenset(p) in grid for p in combinations(Y, 2)):
            continue
        X = [v for v in range(7) if v not in Y]
        # 4-cycles on X: 3 of them; diagonals = the 2 non-cycle pairs
        for a, b, c, d in [(X[0], X[1], X[2], X[3]), (X[0], X[1], X[3], X[2]), (X[0], X[2], X[1], X[3])]:
            cyc = [frozenset((a, b)), frozenset((b, c)), frozenset((c, d)), frozenset((d, a))]
            if all(e in grid for e in cyc):
                diag = [frozenset((a, c)), frozenset((b, d))]
                if not all(e in grid for e in diag):
                    return (Y, (a, b, c, d))
    return None


stats = Counter(); hits = []
for idx, r in enumerate(recs):
    if sel is not None and idx not in sel:
        continue
    t = r["template"]
    ng = {frozenset(e) for e in t["nongrid_edges"]}
    grid = {frozenset(p) for p in combinations(range(7), 2)} - ng
    k = killed(grid)
    stats[(t["kernel_dimension"], bool(k))] += 1
    if k:
        hits.append(idx)
print(dict(sorted(stats.items())))
print("killed by the C4+C3 closure:", len(hits), hits[:30])
json.dump(hits, open("c4c3_hits_%s.json" % ("open" if sel is not None else "all"), "w"))
