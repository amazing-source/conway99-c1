"""Edge structure B_xa (note 177): bipartite 2-regular multigraph between the other triangles through x and through a.
Checks: bijection u -> z_au, cycle types (in triangles per side, 'ell'), symmetry B_xa vs B_ax, and the identities
 sum_e d(e) = 3 t3 (prisms), t2 = (m-1)E - 3 t3 (twisted pairs)."""
import collections, itertools
from fx_cycles import load, rook3
def B_type(adj, x, a):
    N = adj[x]; T0 = (N & adj[a]) | {x, a}            # triangle {x,a,a'}
    ap = ((N & adj[a])).pop()
    U = sorted(N - {a, ap}); W = sorted(adj[a] - {x, ap})
    f = {}
    for u in U:
        c = (adj[u] & adj[a]) - {x}; assert len(c) == 1; f[u] = c.pop()
    assert sorted(f.values()) == W                        # bijection
    tri_x = {u: frozenset({u, (N & adj[u]).pop()}) for u in U}
    tri_a = {w: frozenset({w, ((adj[a] & adj[w]) - {x}).pop()}) for w in W}
    # bipartite multigraph on triangle-nodes: edge tri_x[u] -- tri_a[f[u]]
    g = collections.defaultdict(list)
    for u in U: g[('x', tri_x[u])].append(('a', tri_a[f[u]])); g[('a', tri_a[f[u]])].append(('x', tri_x[u]))
    seen, ells = set(), []
    for v in g:
        if v in seen: continue
        stack, comp = [v], set()
        while stack:
            y = stack.pop()
            if y in comp: continue
            comp.add(y); stack += g[y]
        seen |= comp; ells.append(len(comp) // 2)
    return tuple(sorted(ells))
R = '/home/user/strongly-regular-graphs-research/results/srg243_family/'
for name, (n, adj) in [('Paley9', rook3())] + [(f, load(R + f)) for f in ['bvls243.edges', 'twin243.edges', 'gamma3_aut864.edges', 'gamma4_aut3888.edges']]:
    k = len(adj[0]); m = k // 2; E = n * k // 2
    types = collections.Counter(); sym = 0; d_sum = 0
    for x in range(n):
        for a in adj[x]:
            if a < x: continue
            t1, t2 = B_type(adj, x, a), B_type(adj, a, x); sym += (t1 == t2); types[t1] += 1; d_sum += t1.count(1)
    print(f"== {name}: edges {E}; B_xa == B_ax on all edges: {sym == E}; sum_e d(e) = {d_sum} -> t3 = {d_sum/3:g}, "
          f"t2 = (m-1)E - 3t3 = {(m-1)*E - d_sum}")
    print("   edge types (ell multiset):", dict(types.most_common()))
