"""Four-star (two-line) blocks of REAL srg(243,22,1,2) graphs: nullity of T_S = multiplicity of the eigenvalue 4 of
A_Sigma, Sigma = N[x] u (labels meeting the 4 letters of two lines).  For srg(v,k,1,2) the four-star block has
|S| = 4k - 12 labels, 4 star relations, rank T <= g - k (g = multiplicity of s), hence 5k - 16 - g forced relations
beyond the stars: 10 for (99,14,1,2), -16 (none) for (243,22,1,2).  usage: python fourstar243.py <edges> [vertices]"""
import itertools
import sys
from collections import Counter

import numpy as np

E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
nv = 1 + max(max(e) for e in E)
A = np.zeros((nv, nv))
adj = [set() for _ in range(nv)]
for i, j in E:
    A[i, j] = A[j, i] = 1
    adj[i].add(j)
    adj[j].add(i)
cnt = Counter()
for x in range(int(sys.argv[2]) if len(sys.argv) > 2 else 3):
    Nx = sorted(adj[x])
    mate = {a: [y for y in adj[a] if y in adj[x]][0] for a in Nx}
    lines = sorted({tuple(sorted((a, mate[a]))) for a in Nx})
    for l, m in itertools.combinations(lines, 2):
        labs = set()
        for a in l + m:
            for y in Nx:
                if y not in (a, mate[a]):
                    labs.add([z for z in adj[a] & adj[y] if z != x][0])
        Sig = [x] + Nx + sorted(labs)
        ev = np.linalg.eigvalsh(A[np.ix_(Sig, Sig)])
        cnt[(len(labs), int(np.sum(np.abs(ev - 4) < 1e-7)))] += 1
print(sys.argv[1], "(|S|, nullity of T_S) over all pairs of lines:", dict(cnt))
for k, g in ((14, 44), (22, 110)):
    print("k = %d, g = %d: forced relations beyond the stars at four stars = 5k - 16 - g = %d" % (k, g, 5 * k - 16 - g))
