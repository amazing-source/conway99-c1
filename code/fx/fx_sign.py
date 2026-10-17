"""Is there s: N(x) -> F2 with s(a') = s(a)+1 and s(pi_a(b)) = s(b)+1 for all a, b ?  (would prove even F_x cycles)"""
import collections
from fx_cycles import load, rook3
def pis(n, adj, x):
    N = adj[x]; mate = {a: (N & adj[a]).pop() for a in N}; P = {}
    for a in N:
        Z = {b: ((adj[a] & adj[b]) - {x}).pop() for b in N - {a, mate[a]}}
        inv = {z: b for b, z in Z.items()}
        P[a] = {b: inv[((adj[Z[b]] & adj[a]) - {x}).pop()] for b in Z}
    return mate, P
def solve(n, adj, x):
    mate, P = pis(n, adj, x); N = sorted(adj[x])
    # union-find with parity
    par = {a: a for a in N}; d = {a: 0 for a in N}
    def find(a):
        if par[a] == a: return a, 0
        r, p = find(par[a]); par[a] = r; d[a] ^= p; return r, d[a]
    def union(a, b, w):   # s(a) + s(b) = w
        ra, pa = find(a); rb, pb = find(b)
        if ra == rb: return (pa ^ pb) == w
        par[ra] = rb; d[ra] = pa ^ pb ^ w; return True
    ok = all(union(a, mate[a], 1) for a in N)
    bad = 0
    for a in N:
        for b, c in P[a].items():
            if not union(b, c, 1): bad += 1
    return ok and bad == 0, bad
R = '/home/user/strongly-regular-graphs-research/results/srg243_family/'
for name, (n, adj) in [('Paley9', rook3())] + [(f, load(R + f)) for f in ['bvls243.edges', 'twin243.edges', 'gamma3_aut864.edges', 'gamma4_aut3888.edges']]:
    res = collections.Counter(solve(n, adj, x)[0] for x in range(n))
    print(name, 'vertices with a consistent sign:', dict(res))
