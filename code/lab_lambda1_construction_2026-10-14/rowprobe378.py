"""Row-list sizes for a kept set R = N[v] u N[w] (v, w non-adjacent, 98 kept) in the S3 graph (14/10/2026).
usage: python rowprobe378.py <edges> <cap> <number of free vertices to probe>   (environment PYLIB)"""
import os, sys, time, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_general as CG
E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
n = 1 + max(max(e) for e in E); A = np.zeros((n, n), dtype=np.int64)
for a, b in E: A[a, b] = A[b, a] = 1
adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
rng = random.Random(3); v = rng.randrange(n); w = next(x for x in range(n) if x != v and x not in adj[v])
R = sorted({v, w} | adj[v] | adj[w]); Rs = set(R); F = [x for x in range(n) if x not in Rs]
cap, k = int(sys.argv[2]), int(sys.argv[3])
print("kept %d, free %d" % (len(R), len(F)), flush=True)
for f in F[:k]:
    t = time.time(); rows = CG.rows_of(adj, R, Rs, F, f, cap, 52, 1, 8)
    print("  free vertex %d: %s candidate rows (%.0f s)" % (f, len(rows) if rows is not None else ">%d" % cap, time.time() - t), flush=True)
