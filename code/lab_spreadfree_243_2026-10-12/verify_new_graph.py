"""Lab session, 2026-10-12. INDEPENDENT check of a graph given by its edge list (no import of the census code):
A^2 = 20 I - A + 2 J in integers, spectrum, lines, number of lines parallel to each line (two disjoint lines joined by a
perfect matching), flat lines (20 parallel lines), prisms.   python -I verify_new_graph.py <edge file>"""
# independent check of the new graph: no import of the census code
import sys, itertools, collections, hashlib
import numpy as np
path = sys.argv[1]
E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
print("file sha256:", hashlib.sha256(open(path, "rb").read()).hexdigest())
n = 243; A = np.zeros((n, n), dtype=np.int64)
for a, b in E:
    assert a != b; A[a, b] = A[b, a] = 1
print("vertices", n, "edges", len(set(tuple(sorted(e)) for e in E)), "symmetric", (A == A.T).all(), "zero diagonal", (np.diag(A) == 0).all())
J = np.ones((n, n), dtype=np.int64); I = np.eye(n, dtype=np.int64)
print("A^2 = 20 I - A + 2 J :", (A @ A == 20 * I - A + 2 * J).all(), "; row sums all 22:", (A.sum(1) == 22).all())
w = np.linalg.eigvalsh(A.astype(float)); print("spectrum:", sorted(collections.Counter(np.round(w, 6)).items()))
adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
lines = sorted({tuple(sorted((x, y, next(iter(adj[x] & adj[y]))))) for x in range(n) for y in adj[x] if x < y})
print("lines (triangles):", len(lines))
# parallel lines: two disjoint lines joined by a perfect matching; flat line = 20 parallel lines
lineof = {}
for L in lines:
    for x in L: lineof.setdefault(x, []).append(L)
par = collections.Counter(); 
for L in lines:
    cnt = 0
    p = L[0]
    for w0 in adj[p]:
        if w0 in L: continue
        for M in lineof[w0]:
            if p in M: continue
            if all(len(adj[x] & set(M)) == 1 for x in L): cnt += 1
    par[cnt] += 1
print("number of lines parallel to a line (value: number of lines):", sorted(par.items()))
print("flat lines (20 parallel lines):", par.get(20, 0), " -> a regular spread would consist of 81 flat lines")
print("prisms K3 x K2:", sum(c * m for c, m in par.items()) // 2)
