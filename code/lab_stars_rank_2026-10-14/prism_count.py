"""Transversals (prisms) of the lines l = {v,0,1} and m = {v,2,3} visible in a star structure (14/10/2026).
A transversal of l through the letter x of v is the triangle {x, z_0x, z_1x}: it exists iff z_0x ~ z_1x (the matching
sigma between L_0 and L_1 is 'straight' at x). t(l) = number of such x (each transversal of l has exactly one vertex
adjacent to v). Global facts (CONWAY_CONSTRAINTS C4-C5): prisms P = (1/2) sum_l t(l) <= 852 in any Conway graph,
i.e. the average t(l) is at most 7.38.  usage: python prism_count.py <json with labels and edges, or 'found'/'structures'> ..."""
import json
import sys
import numpy as np



def load(f):
    d = json.load(open(f))
    if "edges" in d:
        return d["labels"], d["edges"], d
    if "structures" in d:
        return d["labels"], d["structures"][0]["edges"], d
    if "found" in d:
        return d["labels"], d["found"][0]["edges"], d
    return d["labels"], d["best"]["edges"], d


for f in sys.argv[1:]:
    labels, edges, d = load(f)
    S = [frozenset(l) for l in labels]
    idx = {l: i for i, l in enumerate(S)}
    E = {(min(i, j), max(i, j)) for i, j in edges}
    adj = lambda a, b: (min(a, b), max(a, b)) in E
    out = []
    for (a, b) in ((0, 1), (2, 3)):
        if frozenset((a, 4)) not in idx or frozenset((b, 4)) not in idx:
            continue
        t = sum(1 for x in range(14) if x not in (a, b) and frozenset((a, x)) in idx and frozenset((b, x)) in idx
                and adj(idx[frozenset((a, x))], idx[frozenset((b, x))]))
        out.append("t(%d%d) = %d" % (a, b, t))
    print("%-28s %s %s" % (f, ", ".join(out), "c = %s" % d.get("c", "")))
