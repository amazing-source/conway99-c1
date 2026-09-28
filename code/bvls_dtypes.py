import sys, itertools
from collections import Counter
import numpy as np
sys.path.insert(0, 'C:/home/researcher/Desktop/conway99-involution/code/z2')
from control_bvls import bvls
A, V, ix, cols, neg = bvls()
n, m = 243, 11
x = ix[(0,) * 5]; inner = {}
for i, c in enumerate(cols): inner[ix[c]] = (i + 1, 0); inner[ix[neg(c)]] = (i + 1, 1)
label = {}
for v in range(n):
    if v == x or v in inner: continue
    nb = [inner[w] for w in np.flatnonzero(A[v]) if w in inner]
    label[frozenset(nb)] = v
outer = [(i, j, e) for i in range(1, m + 1) for j in range(i + 1, m + 1) for e in (0, 1)]
rep = [frozenset([(i, 0), (j, e)]) for (i, j, e) in outer]
trep = [frozenset([(i, 1), (j, 1 - e)]) for (i, j, e) in outer]
N = len(outer)
Am = np.array([[A[label[rep[U]], label[rep[W]]] if U != W else 0 for W in range(N)] for U in range(N)])
Bm = np.array([[A[label[rep[U]], label[trep[W]]] if U != W else 0 for W in range(N)] for U in range(N)])
Q = Am + Bm
typ = Counter()
for U in range(N):
    W = int(np.flatnonzero(Q[U] == 2)[0])
    cu = {outer[U][0], outer[U][1]}; cw = {outer[W][0], outer[W][1]}
    typ[{2: 'sib', 1: 'one', 0: 'dis'}[len(cu & cw)]] += 1
print('BvLS m=11 D-types over', N, 'orbits:', dict(typ))
# star structure: in star c (oriented rep containing (c,0)), Q_c/P_c matchings and overlaps
S = Am - Bm
print('S row nonzeros per row:', Counter((S != 0).sum(1).tolist()))
