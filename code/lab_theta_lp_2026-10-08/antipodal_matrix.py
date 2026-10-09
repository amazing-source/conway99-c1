"""C1, lab session, 2026-10-09. The antipodal multigraph: Anti[y, y'] = number of centres x (at distance two from y)
with s_x(y) = y'. Distribution of its entries on edges, on pairs at distance two and on farther pairs; is it in the
adjacency algebra; its spectrum on the strongly regular examples.  python antipodal_matrix.py <data> <graph>"""
import sys, collections
import numpy as np
from product_test_lib import load
D = sys.argv[1]; n, E = load(D, sys.argv[2])
adj = [set() for _ in range(n)]
for a, b in E: adj[a].add(b); adj[b].add(a)
k = len(adj[0]); third = {}
for a, b in E:
    t = next(iter(adj[a] & adj[b])); third[(a, b)] = third[(b, a)] = t
Anti = np.zeros((n, n), dtype=np.int64)
for x in range(n):
    for y in range(n):
        if y == x or y in adj[x]: continue
        cn = adj[x] & adj[y]
        if len(cn) != 2: continue
        u, v = sorted(cn); u1, v1 = third[(x, u)], third[(x, v)]
        y1 = next(iter((adj[u1] & adj[v1]) - {x})); Anti[y, y1] += 1
assert (Anti == Anti.T).all()
A = np.zeros((n, n), dtype=np.int64)
for a, b in E: A[a, b] = A[b, a] = 1
A2 = A @ A; dist2 = (A == 0) & (A2 > 0) & ~np.eye(n, dtype=bool); far = (A == 0) & (A2 == 0) & ~np.eye(n, dtype=bool)
print("%s: n %d, k %d, row sums of Anti %s" % (sys.argv[2], n, k, sorted(set(Anti.sum(axis=1).tolist()))))
print("   on edges:", dict(sorted(collections.Counter(Anti[A == 1].tolist()).items())))
print("   at distance two:", dict(sorted(collections.Counter(Anti[dist2].tolist()).items())))
print("   farther:", dict(sorted(collections.Counter(Anti[far].tolist()).items())), " diagonal:", sorted(set(Anti.diagonal().tolist())))
comm = np.abs(Anti @ A - A @ Anti).max(); print("   commutes with A: %s" % (comm == 0))
w = np.linalg.eigvalsh(Anti.astype(float)); vals = collections.Counter(np.round(w, 6).tolist())
print("   spectrum of Anti (%d distinct values):" % len(vals), dict(sorted(vals.items(), key=lambda t: -t[0])) if len(vals) <= 14 else "min %.4f max %.4f" % (w.min(), w.max()))
