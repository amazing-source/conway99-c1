"""Complements of the srg(25,12,5,6), the two-graph of each srg(26,10,3,4), and the group of the two-graph on 10
points behind Paley 9 (asymmetry campaign, 14/10/2026, part 2).
usage: python anatomy26.py <dir of Spence lists>"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srglib as L
import twographs as TW
import anatomy25 as AN

d = sys.argv[1]
h25, g25 = L.read_spence(os.path.join(d, "25-12-5-6.txt"))
c25 = [L.canonical_form(g) for g in g25]
idx25 = {c: i + 1 for i, c in enumerate(c25)}
comp = []
for g in g25:
    n = len(g)
    h = [set(range(n)) - g[v] - {v} for v in range(n)]
    comp.append(idx25[L.canonical_form(h)])
print("complement of srg(25,12,5,6) #i is #j:", {i + 1: comp[i] for i in range(15)}, flush=True)

# two-graph of each srg(26,10,3,4): descendants at its 26 points
two = {}
for gi, g in enumerate(g25):
    key = tuple(sorted(idx25[L.canonical_form(x)] for x in TW.descendants(g)))
    two.setdefault(key, gi + 1)
name = {}
for key, first in two.items():
    name[key] = "T(%s)" % ",".join(str(t) for t in sorted(set(key)))
h26, g26 = L.read_spence(os.path.join(d, "26-10-3-4.txt"))
for gi, H in enumerate(g26):
    n = len(H)
    desc = []
    for y in range(n):
        S = H[y]
        K = [set() for _ in range(n)]
        for a in range(n):
            for b in range(a + 1, n):
                e = b in H[a]
                if (a in S) != (b in S):
                    e = not e
                if e:
                    K[a].add(b)
                    K[b].add(a)
        assert not K[y]
        keep = [u for u in range(n) if u != y]
        ix = {u: i for i, u in enumerate(keep)}
        desc.append([set(ix[w] for w in K[u] if w != y) for u in keep])
    key = tuple(sorted(idx25[L.canonical_form(x)] for x in desc))
    print("srg(26,10,3,4) #%d (|Aut| %d) lies in the switching class of the two-graph with descendants %s"
          % (gi + 1, L.group_order(H)[0], sorted(set(key))), flush=True)

# two-graph on 10 points behind Paley 9
h9, g9 = L.read_spence(os.path.join(d, "9-4-1-2.txt"))
G, canon = AN.two_graph_group(TW.descendants(g9[0]))
orders = {}
for s in G:
    o = AN.perm_order(s)
    orders[o] = orders.get(o, 0) + 1
print("two-graph on 10 points: |Aut| = %d, element orders %s (S6 has 1:1, 2:75, 3:80, 4:180, 5:144, 6:240)"
      % (len(G), dict(sorted(orders.items()))), flush=True)
