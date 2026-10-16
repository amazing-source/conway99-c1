"""Describe pair-level cores from r8_core.py: label types and fact types (LAB 16/10/2026)."""
import collections
import json
import sys


def ltype(l):
    l = set(l)
    if l <= {0, 1, 2, 3}:
        return "K"
    if 4 in l:
        return "C4"
    if 5 in l:
        return "C5"
    return "O"                       # outer-old label {r, u}, u in 6..13


def ftype(a, b, edge):
    a, b = set(a), set(b)
    shared = a & b
    ta, tb = ltype(a), ltype(b)
    rel = "same-star" if shared & {0, 1, 2, 3} else ("share-outer" if shared else "disjoint")
    return "%s %s-%s %s" % ("E" if edge else "N", min(ta, tb), max(ta, tb), rel)


for path in sys.argv[1:]:
    d = json.load(open(path))
    core = d["core"]
    labs = collections.Counter()
    seen = set()
    types = collections.Counter()
    for f in core:
        a, b = f["pair"]
        for l in (a, b):
            if tuple(l) not in seen:
                seen.add(tuple(l))
                labs[ltype(l)] += 1
        types[ftype(a, b, f["edge"])] += 1
    print("%s: %d facts (%d edges), %d labels %s" % (path.split("\\")[-1].split("/")[-1], len(core),
                                                    sum(f["edge"] for f in core), len(seen), dict(labs)))
    for t, c in sorted(types.items(), key=lambda kv: -kv[1]):
        print("    %3d  %s" % (c, t))
