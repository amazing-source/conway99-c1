"""C1, lab session, 2026-10-09, mandate B. Signs of the minors det A[N(v), N(w)] for ALL pairs of vertices, in a gauge
(orders of the neighbourhoods) in which the minors of adjacent pairs all have the same sign (such a gauge exists exactly
when the orientation class is zero or the length class). Question: do the minors of the NON-adjacent pairs then all
have one sign as well?   python minors_sign.py <edge list file | clebsch | grid>     One process, below a minute."""
import sys, itertools, collections
import numpy as np
src = sys.argv[1]
if src == "grid":
    V = list(itertools.product(range(3), repeat=2)); ix = {v: i for i, v in enumerate(V)}; n = 9
    E = [(ix[a], ix[b]) for a in V for b in V if a < b and ((a[0] == b[0]) != (a[1] == b[1]))]
elif src == "clebsch":
    V = list(itertools.product(range(2), repeat=4)); ix = {v: i for i, v in enumerate(V)}; n = 16
    G = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (1, 1, 1, 1)]
    E = sorted({tuple(sorted((ix[v], ix[tuple((p + q) % 2 for p, q in zip(v, g))]))) for v in V for g in G})
else:
    E = [tuple(map(int, l.split())) for l in open(src) if l.strip()]; n = 1 + max(max(e) for e in E)
A = np.zeros((n, n)); adj = [set() for _ in range(n)]
for a, b in E: A[a, b] = A[b, a] = 1; adj[a].add(b); adj[b].add(a)
order = [sorted(adj[v]) for v in range(n)]
det = lambda v, w: int(round(np.linalg.det(A[np.ix_(order[v], order[w])])))
# gauge: flip the order of N(v) so that every edge has a minor of sign s0; s0 = +1 or -1, whichever is consistent
raw = {}
def d0(v, w):
    if (v, w) not in raw: raw[(v, w)] = raw[(w, v)] = det(v, w)
    return raw[(v, w)]
for s0 in (1, -1):
    flip = [None] * n; flip[0] = 0; st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if flip[y] is None:
                flip[y] = flip[x] ^ (0 if (1 if d0(x, y) > 0 else -1) == s0 else 1); st.append(y)
    edge_signs = collections.Counter((1 if d0(a, b) > 0 else -1) * (-1) ** (flip[a] + flip[b]) for a, b in E)
    if len(edge_signs) == 1: break
print("%s: minors of adjacent pairs after gauge: %s" % (src, dict(edge_signs)))
vals = collections.Counter()
for v in range(n):
    for w in range(v + 1, n):
        if w in adj[v]: continue
        d = d0(v, w) * (-1) ** (flip[v] + flip[w]); vals[d] += 1
print("   minors of non-adjacent pairs, value : number of pairs  %s" % dict(sorted(vals.items())))
pos = sum(c for d, c in vals.items() if d > 0); neg = sum(c for d, c in vals.items() if d < 0)
print("   non-adjacent pairs: positive %d, negative %d, zero %d  -> %s" % (pos, neg, vals[0], "ONE SIGN" if pos == 0 or neg == 0 else "BOTH SIGNS"))
