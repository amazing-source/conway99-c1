"""(H-MATCH) relation in REAL srg(v,k,1,2) graphs (LAB 15/10/2026): for each vertex x, its lines {x,a,a'} (lambda = 1),
the matchings M_a induced on N(a) minus {x, a'} (labels {a,y} = common neighbours of a and y other than x), and for each
pair of lines (l, m) at x: l-half 'M_{a'} = s_m(M_a)' (s_m = transposition of the letters of m), m-half likewise,
grid (the four cross labels form a 4-cycle).  Prints, per graph: number of (vertex, pair) with both halves, one
half, none; grids per vertex; Hamming points (all pairs grids).
usage: python hmatch243.py <edges file> [max vertices]"""
import sys
from collections import Counter
from itertools import combinations

E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
nv = 1 + max(max(e) for e in E)
adj = [set() for _ in range(nv)]
for i, j in E:
    adj[i].add(j)
    adj[j].add(i)
maxv = int(sys.argv[2]) if len(sys.argv) > 2 else nv
tot = Counter()
gridhist = Counter()
ham = 0
for x in range(min(nv, maxv)):
    Nx = sorted(adj[x])
    mate = {}
    for a in Nx:
        b = [y for y in adj[a] if y in adj[x]]
        assert len(b) == 1
        mate[a] = b[0]
    lines = sorted({tuple(sorted((a, mate[a]))) for a in Nx})
    def lab(a, y):                 # the common neighbour of a and y other than x (a, y non-mates in N(x))
        c = [w for w in adj[a] & adj[y] if w != x]
        assert len(c) == 1
        return c[0]
    M = {}
    for a in Nx:
        others = [y for y in Nx if y not in (a, mate[a])]
        L = {lab(a, y): y for y in others}
        pairs = set()
        for w, y in L.items():
            p = [z for z in adj[w] if z in L]
            assert len(p) == 1
            pairs.add(frozenset((y, L[p[0]])))
        M[a] = pairs
    def s(mline, P):
        u, v = mline
        sw = {u: v, v: u}
        return {frozenset(sw.get(t, t) for t in q) for q in P}
    g = 0
    allgrid = True
    for l, m in combinations(lines, 2):
        a, a2 = l
        y, y2 = m
        lhalf = M[a2] == s(m, M[a])
        mhalf = M[y2] == s(l, M[y])
        grid = (frozenset((y, y2)) in M[a] and frozenset((y, y2)) in M[a2] and frozenset((a, a2)) in M[y]
                and frozenset((a, a2)) in M[y2])
        g += grid
        allgrid &= grid
        tot[("both" if lhalf and mhalf else "one" if (lhalf or mhalf) else "none", "grid" if grid else "nogrid")] += 1
    gridhist[g] += 1
    ham += allgrid
print("%s: %d vertices examined, %d lines per vertex" % (sys.argv[1], min(nv, maxv), len(lines)))
print("  (H-MATCH halves at the pair, grid): count over (vertex, pair):", dict(sorted(tot.items())))
print("  grids per vertex histogram:", dict(sorted(gridhist.items())), " Hamming points:", ham)
