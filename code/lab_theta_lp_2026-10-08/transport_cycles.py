"""C1, lab session, 2026-10-09. The transport on non-edges of the external dossier (DOSSIER_C1_CONVERGENCES, 09/10) read as
a geodesic flow: for a vertex x, s_x is the point reflection of the chart of x (mates exchanged, the second common
neighbour [u, v] of two non-adjacent neighbours of x sent to [u', v']); the centres of a transport cycle satisfy
c_(i+1) = s_(c_i)(c_(i-1)) for consecutive non-adjacent centres. Cycle lengths on the available graphs of the family,
and for every cycle: its length, whether the two strands close as a cylinder or a Moebius band is read from the
vertices u_i, the number of distinct vertices on the ribbon.
  python transport_cycles.py <codex data folder> <graph> [<second factor>]      One process, below 1 GB."""
import sys, collections
from product_test_lib import load, product
D = sys.argv[1]; g = load(D, sys.argv[2])
if len(sys.argv) > 3: g = product(g, load(D, sys.argv[3]))
n, E = g
adj = [set() for _ in range(n)]
for a, b in E: adj[a].add(b); adj[b].add(a)
k = len(adj[0]); third = {}
for a, b in E:
    t = next(iter(adj[a] & adj[b])); third[(a, b)] = third[(b, a)] = t


def reflect(x, y):
    """s_x(y) for y at distance two from x"""
    u, v = sorted(adj[x] & adj[y]); u1, v1 = third[(x, u)], third[(x, v)]
    return next(iter((adj[u1] & adj[v1]) - {x}))


seen = set(); stat = collections.Counter(); detail = collections.Counter()
for c0 in range(n):
    for c1 in range(n):
        if c1 == c0 or c1 in adj[c0] or len(adj[c0] & adj[c1]) != 2 or (c0, c1) in seen: continue
        a, b = c0, c1; cyc = []
        while (a, b) not in seen:
            seen.add((a, b)); cyc.append((a, b)); a, b = b, reflect(b, a)
        L = len(cyc); centres = [p[0] for p in cyc]
        # the ribbon: centres and the common neighbours of consecutive centres
        verts = set(centres)
        for (p, q) in cyc: verts |= (adj[p] & adj[q])
        chords = sum(1 for i in range(L) for j in range(i + 1, L) if centres[j] in adj[centres[i]])
        stat[L] += 1; detail[(L, len(set(centres)), len(verts), chords)] += 1
tot = sum(L * c for L, c in stat.items())
print("%s: n %d, k %d, ordered pairs at distance two %d; directed transport cycles by length: %s" % (" x ".join(sys.argv[2:]), n, k, tot, dict(sorted(stat.items()))))
for (L, dc, nv, ch), c in sorted(detail.items()): print("   length %3d, distinct centres %3d, vertices on the ribbon %3d, adjacent pairs of centres %3d : %d directed cycles" % (L, dc, nv, ch, c))
