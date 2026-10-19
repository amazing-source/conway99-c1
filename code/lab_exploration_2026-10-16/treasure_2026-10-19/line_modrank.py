"""Universal F_p structure of the line geometry of a real srg(v,k,1,2) (LAB 19/10/2026).
Z_p = {y in F_p^V : sum of y over every line = 0}; dim Z_p = v - rank_p(N), N = point-line incidence.
For p = 3 and BvLS (points = Z_3^5, lines = affine lines) Z_3 contains the affine functions (dim >= 6).
Also prints rank_p(A + 7I) (= rank_p(N N^T)).
usage: python line_modrank.py <edges> [p ...]"""
import sys
import numpy as np
def rank_mod(M, p):
    M = M.copy() % p
    r = 0
    rows, cols = M.shape
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i, c]:
                piv = i; break
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        nz = np.nonzero(M[:, c])[0]
        nz = nz[nz != r]
        if len(nz):
            M[nz] = (M[nz] - np.outer(M[nz, c], M[r])) % p
        r += 1
        if r == rows:
            break
    return r
edges = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
v = 1 + max(max(e) for e in edges)
adj = [set() for _ in range(v)]
for a, b in edges:
    adj[a].add(b); adj[b].add(a)
lines = sorted({tuple(sorted((a, b, c))) for a in range(v) for b in adj[a] for c in adj[a] & adj[b]})
N = np.zeros((v, len(lines)), dtype=np.int64)
for j, L in enumerate(lines):
    for x in L:
        N[x, j] = 1
A = np.zeros((v, v), dtype=np.int64)
for a, b in edges:
    A[a, b] = A[b, a] = 1
k = int(A[0].sum())
out = []
for p in [int(x) for x in sys.argv[2:]] or [3]:
    rN = rank_mod(N.T, p)
    rA = rank_mod(A + (len(adj[0]) // 2) * np.eye(v, dtype=np.int64), p)
    out.append("p=%d: rank N = %d, dim Z = %d, rank(A + %dI) = %d" % (p, rN, v - rN, k // 2, rA))
print(sys.argv[1].split('/')[-1], "v", v, "lines", len(lines), "; ".join(out))
