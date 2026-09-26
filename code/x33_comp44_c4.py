# 4-label component of G(L) at P = 0 (S unrestricted): tau_u, tau_ub mate-free matchings A<->B, sigma fixed-point free,
# condition (c) (no prism with rung u-ubar). Count 4-cycles (all are type (ii) = S-events), triangles must be 0.
import itertools, networkx as nx
from collections import Counter
labels = [0, 1, 2, 3]; mate = {0: 1, 1: 0, 2: 3, 3: 2}
M = [{0: 2, 2: 0, 1: 3, 3: 1}, {0: 3, 3: 0, 1: 2, 2: 1}]
res = Counter()
for tu in M:
    for tb in M:
        for perm in itertools.permutations(labels):
            s = dict(zip(labels, perm))
            if any(s[v] == v for v in labels): continue
            if any(tb[s[w]] == s[tu[w]] for w in labels): continue      # (c)
            G = nx.Graph()
            for v in labels:
                G.add_edge(('x', v), ('x', mate[v])); G.add_edge(('u', v), ('u', tu[v])); G.add_edge(('b', v), ('b', tb[v]))
                G.add_edge(('x', v), ('u', v)); G.add_edge(('x', v), ('b', v)); G.add_edge(('u', v), ('b', s[v]))
            if not nx.is_connected(G): continue
            tri = sum(nx.triangles(G).values()) // 3
            c4 = sum(1 for c in nx.simple_cycles(G, length_bound=4) if len(c) == 4)
            ev = (sum(s[v] == mate[v] for v in labels), sum(s[v] == tu[v] for v in labels), sum(s[v] == tb[v] for v in labels))
            res[(tri, c4, ev)] += 1
for k, v in sorted(res.items()):
    print(f'triangles {k[0]}, 4-cycles {k[1]}, S-events (sigma=mate, sigma=tau_u, sigma=tau_ub) = {k[2]}: {v} configurations')
