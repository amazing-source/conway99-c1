"""C1, lab session, 2026-10-09, mandate B. For an ARBITRARY orientation xi of the edges, the cochain
  LAMBDA(vw) = #{p in a colour class of the two-layer graph of vw : xi orients p -> mate(p)} + [t -> w] + [t -> v]
has a class that does not depend on xi. Question: is there an orientation xi for which every two-layer cycle of every
edge has its mate edges all oriented along one traversal (then the first term vanishes)?  This is a system of
equalities between arcs: (x -> x') = (y -> y') whenever x' ~ y is a cross edge of the edge third(x,x') third(y,y').
  python arc_coherence.py <data folder>      One process, seconds."""
import sys, os, json, collections, itertools
D = sys.argv[1]


def study(name, n, E):
    adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    third = {}
    for a, b in E:
        t = next(iter(adj[a] & adj[b])); third[(a, b)] = third[(b, a)] = t
    arcs = [(a, b) for a in range(n) for b in adj[a]]; idx = {a: i for i, a in enumerate(arcs)}
    parent = list(range(len(arcs)))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for v in range(n):
        for w in adj[v]:
            t = third[(v, w)]
            for x1 in adj[v]:                               # x1 = exit point of a mate pair at v; cross to y
                if x1 == w or x1 == t: continue
                x = third[(v, x1)]; y = next(iter((adj[x1] & adj[w]) - {v})); y1 = third[(w, y)]
                a, b = find(idx[(x, x1)]), find(idx[(y, y1)])
                if a != b: parent[a] = b
    bad = sum(1 for (a, b) in arcs if a < b and find(idx[(a, b)]) == find(idx[(b, a)]))
    classes = len({find(i) for i in range(len(arcs))})
    print("%-18s arcs %5d, classes %5d, edges whose two arcs fall in the same class: %d -> coherent orientation %s"
          % (name, len(arcs), classes, bad, "EXISTS" if bad == 0 else "does not exist"))


V3 = [(i, j) for i in range(3) for j in range(3)]; ix = {v: i for i, v in enumerate(V3)}
study("grid 3x3", 9, [(ix[a], ix[b]) for a in V3 for b in V3 if a < b and ((a[0] == b[0]) != (a[1] == b[1]))])
for g in ("t2_twisted", "t2_untwisted", "t3_twisted", "t3_twisted_42"):
    A = json.load(open(os.path.join(D, g + ".json"))); m = len(A)
    study(g, m, [(i, j) for i in range(m) for j in range(i + 1, m) if A[i][j]])
for g in ("bvls243", "twin243_switched"):
    study(g, 243, [tuple(map(int, l.split())) for l in open(os.path.join(D, "srg243", g + ".edges")) if l.strip()])
