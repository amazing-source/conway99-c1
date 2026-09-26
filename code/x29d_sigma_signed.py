# Check on BvLS the general identity for the triangle signed matrix  A_S = N0 - N2 - 2 N3  (weights 1 - #rungs on
# disjoint triangle pairs, 0 on triangles sharing a vertex):  A_S^2 = (k/2 + s)*... derived for 99 as A_S^2 = 13 A_S + 68 I.
# General form: G = B^T E_s B is a multiple of a projection; entries of G on triangle pairs are affine in #rungs.
import itertools, numpy as np
exec(open('code/x29_bvls_triangle.py').read().split('# a triangle through 0')[0])
v = 243
nb = [set(np.nonzero(A[i])[0]) for i in range(v)]
tris = set()
for a in range(v):
    for b in nb[a]:
        if b > a:
            c = (nb[a] & nb[b]).pop(); tris.add(frozenset((a, b, c)))
tris = list(tris); t = len(tris)
B = np.zeros((v, t))
for j, T in enumerate(tris):
    for i in T: B[i, j] = 1
# s = -5 eigenspace projection
w, U = np.linalg.eigh(A.astype(float))
Us = U[:, np.abs(w + 5) < 1e-6]
G = B.T @ Us @ Us.T @ B
ev = np.linalg.eigvalsh(G)
print('BvLS: triangle Gram in the -5 eigenspace: distinct eigenvalues', sorted(set(np.round(ev, 6))))
# entries by relation
rel = {}
for i in range(t):
    for j in range(t):
        if i == j: key = 'diag'
        elif tris[i] & tris[j]: key = 'share'
        else:
            key = 'rungs%d' % sum(1 for p in tris[i] for q in tris[j] if q in nb[p])
        rel.setdefault(key, set()).add(round(G[i, j], 6))
print({k: sorted(vv) for k, vv in rel.items()})
