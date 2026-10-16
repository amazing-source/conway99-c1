"""Check, on a known srg(243,22,1,2), at a few grid and non-grid pairs of a vertex:
(1) the rational 4- and -5-eigenvectors carried by the 99-ball are the universal ones (A+5I)(e_u-e_w), (A-4I)(e_u-e_w),
    u, w in the 5 points of the two lines;  (2) the local mod-3 kernel of A_W - 4I equals the global mod-3 kernel restricted
    to W (every local mod-3 eigenvector is global).  usage: python cal243_universal.py <edges> [pairs per type]"""
import itertools, sys
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from f7_classform import rref_mod, null_mod  # noqa: E402

P = 1000003
path = sys.argv[1]; per = int(sys.argv[2]) if len(sys.argv) > 2 else 2
n = 243
A = np.zeros((n, n), dtype=np.int64)
for line in open(path):
    if line.strip():
        i, j = map(int, line.split()); A[i, j] = A[j, i] = 1
adj = [set(np.nonzero(A[i])[0].tolist()) for i in range(n)]
I = np.eye(n, dtype=np.int64)
K3 = null_mod(((A - 4 * I) % 3).tolist(), 3)          # global mod-3 kernel, basis
print("global dim ker_F3(A - 4I) =", len(K3))
def lines_at(v):
    out, seen = [], set()
    for a in sorted(adj[v]):
        if a in seen: continue
        b = next(iter(adj[a] & adj[v])); seen |= {a, b}; out.append((a, b))
    return out
def corner(x, y, v): return next(iter((adj[x] & adj[y]) - {v}))
def is_grid(v, l, m):
    (a, a2), (b, b2) = l, m
    w = {(p, q): corner(p, q, v) for p in (a, a2) for q in (b, b2)}
    need = [((a, b), (a, b2)), ((a2, b), (a2, b2)), ((a, b), (a2, b)), ((a, b2), (a2, b2))]
    return all(w[q] in adj[w[p]] for p, q in need)
v = int(sys.argv[3]) if len(sys.argv) > 3 else 12
done = {True: 0, False: 0}
for l, m in itertools.combinations(lines_at(v), 2):
    g = is_grid(v, l, m)
    if done[g] >= per: continue
    done[g] += 1
    pts = [v, l[0], l[1], m[0], m[1]]
    W = sorted({v} | adj[v] | adj[l[0]] | adj[l[1]] | adj[m[0]] | adj[m[1]])
    Z = [u for u in range(n) if u not in set(W)]
    AW = A[np.ix_(W, W)]; IW = np.eye(len(W), dtype=np.int64)
    k4 = null_mod(((AW - 4 * IW) % P).tolist(), P); k5 = null_mod(((AW + 5 * IW) % P).tolist(), P)
    uni4 = [((A + 5 * I) @ (I[:, pts[0]] - I[:, u]))[W] for u in pts[1:]]
    uni5 = [((A - 4 * I) @ (I[:, pts[0]] - I[:, u]))[W] for u in pts[1:]]
    r4 = len(rref_mod([list(x) for x in k4] + [list(x) for x in uni4], P)[0])
    r5 = len(rref_mod([list(x) for x in k5] + [list(x) for x in uni5], P)[0])
    loc = null_mod(((AW - 4 * IW) % 3).tolist(), 3)
    # global kernel vectors vanishing on Z: kernel of the restriction map K3 -> F3^Z
    R = [[K3[i][z] for i in range(len(K3))] for z in Z]
    coef = null_mod(R, 3) if R else []
    glob = [[sum(c[i] * K3[i][w] for i in range(len(K3))) % 3 for w in W] for c in coef]
    both = len(rref_mod(loc + glob, 3)[0])
    print("pair %s: grid=%s  n4=%d (span with universal: %d), n5=%d (span with universal: %d), local ker_F3 = %d,"
          " global ker_F3 on W = %d, span of both = %d" % ((l, m), g, len(k4), r4, len(k5), r5, len(loc), len(rref_mod(glob, 3)[0]), both))
