"""Components of the cubic line neighbourhoods G[N(l)] for the lines l0 = {v,0,1}, l1 = {v,2,3} of a structure, and the
balance test (k = 14 resonance: every far label z must have n_C(z) = |C|/6 for every component C) on the far labels that
are present (exploration, LAB 16/10/2026).
N(l0) = letters 2..K-1, L_0, L_1; edges: letter mates, letter s - {0,s}, {1,s}, and Gamma inside L_0 u L_1.
usage: python line_components.py <K> <structure json (labels, edges)> [...]"""
import itertools
import json
import sys

K = int(sys.argv[1])
MATE = lambda i: i ^ 1
for path in sys.argv[2:]:
    d = json.load(open(path))
    L = [frozenset(x) for x in d["labels"]]
    E = set(frozenset((L[i], L[j])) for i, j in d["edges"])
    out = []
    for a in (0, 2):
        b = a + 1
        verts = [("L", s) for s in range(K) if s not in (a, b)] + [l for l in L if a in l or b in l]
        adj = {x: set() for x in verts}
        for s in range(K):
            if s in (a, b):
                continue
            adj[("L", s)].add(("L", MATE(s)))
            for r in (a, b):
                lab = frozenset((r, s))
                if lab in adj:
                    adj[("L", s)].add(lab)
                    adj[lab].add(("L", s))
        labs = [x for x in verts if not isinstance(x, tuple)]
        for x, y in itertools.combinations(labs, 2):
            if frozenset((x, y)) in E:
                adj[x].add(y)
                adj[y].add(x)
        degs = sorted(set(len(adj[x]) for x in verts))
        seen, comps = set(), []
        for x in verts:
            if x in seen:
                continue
            stack, comp = [x], []
            seen.add(x)
            while stack:
                u = stack.pop()
                comp.append(u)
                for w in adj[u]:
                    if w not in seen:
                        seen.add(w)
                        stack.append(w)
            comps.append(comp)
        sizes = sorted(len(c) for c in comps)
        bad = 0
        if len(comps) > 1:
            far = [l for l in L if not (l & {a, b})]
            for z in far:
                for c in comps:
                    cs = set(c)
                    n = sum(1 for u in cs if (isinstance(u, tuple) and u[1] in z) or
                            (not isinstance(u, tuple) and frozenset((u, z)) in E))
                    if 6 * n != len(c):
                        bad += 1
        out.append("l%d: %d vertices, degrees %s, components %s%s" % (a // 2, len(verts), degs, sizes,
                   (", balance violations %d" % bad) if len(comps) > 1 else ""))
    print("%s: %s" % (path.replace("\\", "/").split("/")[-1], " | ".join(out)), flush=True)
