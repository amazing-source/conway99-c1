"""Family laws test (LAB 19/10/2026): for a real srg(v,k,1,2), the two canonical 'third points' of a non-adjacent pair.
For x, y non-adjacent with common neighbours a, b: lines {x,a,a'}, {x,b,b'}, {y,a,a*}, {y,b,b*};
  z1 = sigma_x(y) = the common neighbour of a', b' other than x   (the point reflection at x of the label {a,b})
  z2 = sigma_y(x) = the common neighbour of a*, b* other than y.
In a Cayley graph on Z_3^n with a symmetric generating set, z1 = z2 = -x-y (affine third point).  Tally of the relation
between z1 and z2 (equal / adjacent / non-adjacent), of the triple {x,y,z1} (independent?), and of whether the point
reflection sigma_x is an automorphism, for every vertex x.
usage: python third_point.py <edges file>"""
import sys
from collections import Counter
edges = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
v = 1 + max(max(e) for e in edges)
adj = [set() for _ in range(v)]
for a, b in edges:
    adj[a].add(b); adj[b].add(a)
def third(a, b):                       # third point of the line through adjacent a, b
    (c,) = adj[a] & adj[b]
    return c
def other_common(a, b, x):             # common neighbour of non-adjacent a, b other than x
    s = (adj[a] & adj[b]) - {x}
    assert len(s) == 1, (a, b, x, s)
    return next(iter(s))
rel = Counter(); trip = Counter(); refl_ok = 0
for x in range(v):
    sigma = {x: x}
    for a in adj[x]:
        sigma[a] = third(x, a)
    far = [y for y in range(v) if y != x and y not in adj[x]]
    for y in far:
        a, b = sorted(adj[x] & adj[y])
        sigma[y] = other_common(sigma[a], sigma[b], x)
    # is sigma_x an automorphism?
    if all((sigma[p] in adj[sigma[q]]) == (p in adj[q]) for p in range(v) for q in adj[p] if q > p) and \
       len(set(sigma.values())) == v:
        # also non-edges are preserved iff it is a bijection preserving edges (counts equal)
        refl_ok += 1
    for y in far:
        if y < x:
            continue
        a, b = sorted(adj[x] & adj[y])
        z1 = sigma[y]
        z2 = other_common(third(y, a), third(y, b), y)
        if z1 == z2:
            rel["equal"] += 1
        elif z1 in adj[z2]:
            rel["adjacent"] += 1
        else:
            rel["non-adjacent"] += 1
        trip["z1 indep of x,y" if (z1 not in adj[x] and z1 not in adj[y] and z1 not in (x, y)) else "z1 touches"] += 1
print(sys.argv[1].split('/')[-1], "v", v, "pairs", sum(rel.values()), dict(rel), dict(trip), "sigma_x automorphisms:", refl_ok, "of", v)
