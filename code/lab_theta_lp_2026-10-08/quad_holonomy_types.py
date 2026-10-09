"""C1, lab session, 2026-10-09. Is there a NON-ABELIAN version of the quadrangle law?  For every quadrangle Q, the cycle
type of the full holonomy of PHI' on N[v] against the multiset of the two-layer types (partitions) of its four sides.
  python quad_holonomy_types.py <codex data folder> <graph name> [<second factor>]     One process, below 1 GB."""
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
pi = lambda v, w, x: next(iter((adj[x] & adj[w]) - {v}))


def phi(v, w):
    t = third[(v, w)]; d = {v: v, w: w, t: t}
    for x in adj[v]:
        if x != w and x != t: d[x] = pi(v, w, x)
    return d


shape = {}
for a, b in E:
    t = third[(a, b)]; X = [x for x in adj[a] if x != b and x != t]; seen = set(); cyc = []
    for x in X:
        if x in seen: continue
        u = x; ln = 0
        while u not in seen:
            seen.add(u); u1 = third[(a, u)]; seen.add(u1); y = pi(a, b, u1); y1 = third[(b, y)]; u = pi(b, a, y1); ln += 1
        cyc.append(ln)
    shape[(a, b)] = shape[(b, a)] = tuple(sorted(cyc))


def ctype(perm, dom):
    seen = set(); out = []
    for s in dom:
        if s in seen: continue
        ln = 0; u = s
        while u not in seen: seen.add(u); u = perm[u]; ln += 1
        out.append(ln)
    return tuple(sorted(out))


tab = collections.defaultdict(collections.Counter)
for v in range(n):
    for w in range(v + 1, n):
        if w in adj[v]: continue
        cn = sorted(adj[v] & adj[w])
        if len(cn) != 2: continue
        a, b = cn
        if (v, w) > (a, b): continue
        d1, d2, d3, d4 = phi(v, a), phi(a, w), phi(w, b), phi(b, v)
        hol = {x: d4[d3[d2[d1[x]]]] for x in [v] + list(adj[v])}
        ct = ctype(hol, [v] + sorted(adj[v]))
        sides = tuple(sorted([shape[(v, a)], shape[(a, w)], shape[(w, b)], shape[(b, v)]]))
        tab[sides][ct] += 1
print("%s: n %d, k %d; rows = multiset of the four side types, then the holonomy cycle types on N[v] with counts" % (" x ".join(sys.argv[2:]), n, k))
for sides, cnt in sorted(tab.items()):
    print("  sides %s" % (sides,))
    for ct, c in sorted(cnt.items(), key=lambda t: -t[1])[:8]: print("       holonomy %s : %d" % (ct, c))
