"""X14f -- which internal structure makes a triangle support violate the Rayleigh bound?
T = graph on the 12 pairs (edges of the octahedron K_{2,2,2} on the 6 labels of the three classes), T-edges = tau/sigma
adjacencies inside the family.  Collect, over admissible triangle supports from random max-twist samples, invariants of
T for violating vs non-violating supports (edges, triangles, 4-cycles, degree sequence, components, bipartite?)."""
import sys, random, itertools
from collections import Counter
import numpy as np
sys.path.insert(0, 'scripts')
from x14_triangle_supports import LAB, random_tau, random_sigma, build, admissible

def inv(T):
    e = int(T.sum() // 2); t = int(np.trace(T @ T @ T) // 6)
    T2 = T @ T; c4 = int((np.trace(T2 @ T2) - 2 * e - 4 * sum(int(d) * (int(d) - 1) // 2 for d in T.sum(1))) // 8)
    degs = tuple(sorted(T.sum(1).astype(int).tolist(), reverse=True))
    ev = np.linalg.eigvalsh(T.astype(float))
    return e, t, c4, degs, round(float(ev.max()), 3)

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
viol = Counter(); ok = Counter(); vmax = []; okmax = []
for _ in range(int(sys.argv[2]) if len(sys.argv) > 2 else 3000):
    tau = {u: random_tau(u, rng) for u in LAB}; sigma = {c: random_sigma(c, rng) for c in range(7)}
    for tri in itertools.combinations(range(7), 3):
        pairs = [frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2) for s in (0, 1) for t in (0, 1)]
        A = build(pairs, tau, sigma)
        if not admissible(A):
            continue
        n = len(A)
        lmax = np.linalg.eigvalsh(A.astype(float) - (11 / 99) * np.ones((n, n))).max()
        T = A[15:, 15:]
        e, t, c4, degs, tmax = inv(T)
        if lmax > 3 + 1e-9:
            viol[(e, t, c4)] += 1; vmax.append(tmax)
        else:
            ok[(e, t, c4)] += 1; okmax.append(tmax)
print('violating supports by (edges, triangles, 4-cycles of T):', sorted(viol.items()))
print('passing supports by (edges, triangles, 4-cycles of T), top 15:', sorted(ok.items(), key=lambda kv: -kv[1])[:15])
print(f'lambda_max(T): violating in [{min(vmax):.3f}, {max(vmax):.3f}], passing in [{min(okmax):.3f}, {max(okmax):.3f}]')
