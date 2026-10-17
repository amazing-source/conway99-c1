"""Detail of F_x cycles: sequence of N(x)-vertices a_i (z_i = z_{a_i a_{i+1}}), projected to the triangles through x."""
import collections, sys
from fx_cycles import load, rook3
def cycles(n, adj, x):
    N = adj[x]; mate = {a: (N & adj[a]).pop() for a in N}
    tri = {}; t = 0
    for a in sorted(N):
        if a not in tri: tri[a] = tri[mate[a]] = t; t += 1
    D = [z for z in range(n) if z != x and z not in N]
    pair = {z: tuple(sorted(N & adj[z])) for z in D}
    via = {}
    for z in D:
        for a in pair[z]:
            w = ((adj[z] & adj[a]) - {x}).pop(); via[(z, a)] = w
    out, seen = [], set()
    for z0 in D:
        if z0 in seen: continue
        a, b = pair[z0]; seq = [a, b]; z = z0; cur_shared = b
        zs = [z0]; seen.add(z0)
        while True:
            w = via[(z, cur_shared)]
            if w == z0: break
            c = [u for u in pair[w] if u != cur_shared][0]
            seq.append(c); zs.append(w); seen.add(w); z = w; cur_shared = c
        out.append(([tri[u] for u in seq[:-1]] if len(seq) > len(zs) else [tri[u] for u in seq], seq, zs, mate))
    return out
R = '/home/user/strongly-regular-graphs-research/results/srg243_family/'
for f in ['twin243.edges', 'gamma3_aut864.edges', 'gamma4_aut3888.edges']:
    n, adj = load(R + f); shown = collections.Counter()
    print('==', f)
    for x in range(n):
        for tris, seq, zs, mate in cycles(n, adj, x):
            L = len(zs)
            if L == 4: continue
            key = (L,)
            if shown[key] >= 1: continue
            shown[key] += 1
            # how many times each triangle (mate pair) occurs, and steps where next = mate of the one before previous (grid-like step)
            occ = collections.Counter(tris[:L])
            gridsteps = sum(1 for i in range(L) if seq[(i + 2) % L] == mate[seq[i % L]])
            quads = collections.Counter(tuple(sorted((tris[i % L], tris[(i + 1) % L]))) for i in range(L))
            print(f"  x={x} L={L}: triangle visits {dict(sorted(occ.items()))}; grid-like steps {gridsteps}/{L}; "
                  f"distinct quadruples {len(quads)}, visits per quadruple {sorted(quads.values())}")
