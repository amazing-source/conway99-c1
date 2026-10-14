"""Components of Q(v,l) and Q(v,m) for a four-star structure (14/10/2026): partition of the six other lines through v
(given by their letter pairs) induced by the base graph Gamma_X (tau and sigma edges); mu = component sizes; flags the
closed squares (grids, mu = 1).  usage: python comp_view.py <json with labels, edges> ..."""
import json
import sys

LINES = [(2 * k, 2 * k + 1) for k in range(7)]
for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]
    E = [tuple(e) for e in d["edges"]]
    out = []
    for (a, b) in ((0, 1), (2, 3)):
        others = [L for L in LINES if L != (a, b)]
        parent = {L: L for L in others}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        line_of = {}
        for L in others:
            line_of[L[0]] = L
            line_of[L[1]] = L
        for i, j in E:
            li, lj = S[i], S[j]
            if (li & {a, b}) and (lj & {a, b}):
                xi = [y for y in li if y not in (a, b)]
                xj = [y for y in lj if y not in (a, b)]
                if len(xi) == 1 and len(xj) == 1:
                    ri, rj = find(line_of[xi[0]]), find(line_of[xj[0]])
                    if ri != rj:
                        parent[ri] = rj
        comps = {}
        for L in others:
            comps.setdefault(find(L), []).append(L)
        parts = sorted((sorted(v) for v in comps.values()), key=len)
        out.append("line {%d,%d}: mu = %s, parts %s" % (a, b, [len(p) for p in parts],
                                                     ["+".join("%d%d" % L for L in p) for p in parts]))
    print("%s: %s" % (f, " | ".join(out)))
