"""2-factor F_x of the second subconstituent of an srg(v,k,1,2) (note 176).
For z in Delta_x adjacent to a,b in N(x): special neighbour via a = third vertex of the triangle on edge z-a.
Prints, per graph, the distribution of cycle-length multisets of F_x over all vertices x."""
import sys, collections, itertools
def load(fn):
    E = [tuple(map(int, l.split())) for l in open(fn) if l.strip()]
    n = 1 + max(max(e) for e in E); adj = [set() for _ in range(n)]
    for u, v in E: adj[u].add(v); adj[v].add(u)
    return n, adj
def rook3():
    n = 9; adj = [set() for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if u != v and (u // 3 == v // 3 or u % 3 == v % 3): adj[u].add(v)
    return n, adj
def fx(n, adj, x):
    N = adj[x]; D = [z for z in range(n) if z != x and z not in N]
    sp = {}
    for z in D:
        ab = N & adj[z]; assert len(ab) == 2
        nb = []
        for a in ab:
            w = (adj[z] & adj[a]) - {x}; assert len(w) == 1; w = w.pop(); assert w in D; nb.append(w)
        sp[z] = nb
    seen, lens = set(), []
    for z in D:
        if z in seen: continue
        L, prev, cur = 0, None, z
        while True:
            seen.add(cur); L += 1
            nxt = sp[cur][0] if sp[cur][0] != prev else sp[cur][1]
            if prev is None: nxt = sp[cur][0]
            prev, cur = cur, nxt
            if cur == z: break
        lens.append(L)
    return tuple(sorted(lens))
if __name__ == "__main__":
    R = '/home/user/strongly-regular-graphs-research/results/srg243_family/'
    graphs = [('Paley9 (3x3 rook)', rook3())] + [(f, load(R + f)) for f in
              ['bvls243.edges', 'twin243.edges', 'gamma3_aut864.edges', 'gamma4_aut3888.edges']]
    for name, (n, adj) in graphs:
        dist = collections.Counter(fx(n, adj, x) for x in range(n))
        print(f"== {name}: v={n}, |Delta_x|={n-1-len(adj[0])}")
        for lens, c in sorted(dist.items(), key=lambda t: -t[1]):
            print(f"   {c:4d} vertices: cycle lengths {dict(sorted(collections.Counter(lens).items()))}")
