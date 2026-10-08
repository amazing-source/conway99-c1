"""C1, lab session, 2026-10-08. Calibration on real graphs of a 10-vertex dual family: far pairs of 5-sets with 6 edges.

  python -I five_five.py rook|<edge file> [cross]     (needs numpy; 'cross' also counts the pairs with one cross edge, slow)

psi = 1_X - 1_Y with |X| = |Y| = 5 disjoint, sum 0: Q = 30 - 2 (e(X) + e(Y) - e(X,Y)). The 5-sets with 6 edges are the
bowties and the houses. This script counts the ordered pairs (X, Y) of such sets that are disjoint with no edge between
them (norm 6 in the 99-graph setting) and those with exactly one edge between them (norm 8), and prints the ratio to the
naive value N^2 (f/v)^5 with f the generic number of far vertices. It is a calibration of heuristics, not a result on the
99-graph. One process, memory below 300 MB."""
import sys, itertools
import numpy as np


def load(arg):
    if arg == "rook":
        V = [(i, j) for i in range(3) for j in range(3)]; E = [(a, b) for a in range(9) for b in range(a + 1, 9) if (V[a][0] == V[b][0]) != (V[a][1] == V[b][1])]
    else: E = [tuple(int(x) for x in l.split()[:2]) for l in open(arg) if l.strip()]
    n = 1 + max(max(e) for e in E); adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    return n, len(adj[0]), E, adj


n, k, E, adj = load(sys.argv[1]); mask = [sum(1 << u for u in adj[v]) for v in range(n)]
third = lambda a, b: next(iter(adj[a] & adj[b]))
def second(a, b, c):
    (d,) = (adj[a] & adj[b]) - {c}; return d
tris = sorted({tuple(sorted((a, b, third(a, b)))) for a, b in E}); lines = [[] for _ in range(n)]
for t in tris:
    for v in t: lines[v].append(tuple(u for u in t if u != v))
sets5 = set()
for v in range(n):
    for (a, b), (c, d) in itertools.combinations(lines[v], 2): sets5.add(frozenset((v, a, b, c, d)))
nb = len(sets5)
for x, y in E:
    z = third(x, y)
    for p in adj[y] - {x, z}: sets5.add(frozenset((x, y, z, p, second(p, x, y))))
S5 = sorted(tuple(sorted(s)) for s in sets5); m = len(S5); W = (n + 63) // 64
def words(x): return [(x >> (64 * i)) & ((1 << 64) - 1) for i in range(W)]
def bits(S): return sum(1 << u for u in S)
own = np.array([words(bits(s)) for s in S5], dtype=np.uint64)
nbr = np.array([words(0)] * m, dtype=np.uint64); blk = []
for s in S5:
    b_ = bits(s)
    for u in s: b_ |= mask[u]
    blk.append(words(b_))
blk = np.array(blk, dtype=np.uint64)
far = one = 0; DO_CROSS = 'cross' in sys.argv[2:]   # the one-cross-edge count is slow: only on request
pc8 = np.array([bin(i).count("1") for i in range(256)], dtype=np.uint8)
def popcount(a): return pc8[a.view(np.uint8)].reshape(a.shape[0], -1).sum(axis=1).astype(np.int64)
rowmask = [np.array([words(mask[u]) for u in s], dtype=np.uint64) for s in S5]
for i in range(m):
    hit = own[:, 0] & blk[i, 0]
    for j in range(1, W): hit |= own[:, j] & blk[i, j]
    far += int(np.count_nonzero(hit == 0))
    disj = own[:, 0] & own[i, 0]
    for j in range(1, W): disj |= own[:, j] & own[i, j]
    cand = np.nonzero((disj == 0) & (hit != 0))[0] if DO_CROSS else []
    if len(cand):
        cross = np.zeros(len(cand), dtype=np.int64)
        for r in range(5): cross += popcount(np.ascontiguousarray(own[cand] & rowmask[i][r]))
        one += int(np.count_nonzero(cross == 1))
f = n - 5 * k + 11.5; naive = m * m * (f / n) ** 5
print("v = %d, k = %d: bowties %d, houses %d; ordered far pairs (norm 6) = %d (naive %.3g, ratio %.3f); ordered pairs with exactly one cross edge (norm 8) = %d" % (n, k, nb, m - nb, far, naive, far / naive if naive else 0, one), flush=True)
