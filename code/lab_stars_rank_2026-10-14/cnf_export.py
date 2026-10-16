"""Export the admissibility model of a star set (stars_rank.build, the cryptominisat model) as DIMACS CNF, optionally
with the adjacency of a base structure fixed by unit clauses (LAB 16/10).  Also writes the variable map of the edges.
usage: python cnf_export.py <stars> <out.cnf> [base json]"""
import itertools, json, random, sys
from stars_rank import build
stars = [int(t) for t in sys.argv[1].split(",")]
out = sys.argv[2]
S, idx, e, F = build(stars, random.Random(1))
cl = list(F.clauses)
if len(sys.argv) > 3:
    d = json.load(open(sys.argv[3]))
    bl = [frozenset(x) for x in d["labels"]]
    bE = set(tuple(sorted(x)) for x in d["edges"])
    for a, b in itertools.combinations(range(len(bl)), 2):
        if bl[a] in idx and bl[b] in idx:
            v = e[(idx[bl[a]], idx[bl[b]])]
            cl.append([v] if (a, b) in bE else [-v])
with open(out, "w") as fh:
    fh.write("p cnf %d %d\n" % (F.n, len(cl)))
    for c in cl:
        fh.write(" ".join(map(str, c)) + " 0\n")
json.dump({"stars": stars, "labels": [sorted(l) for l in S],
           "edge_vars": {"%d,%d" % (i, j): e[(i, j)] for i, j in itertools.combinations(range(len(S)), 2)}},
          open(out + ".map.json", "w"))
print("wrote %s: %d vars, %d clauses" % (out, F.n, len(cl)))
