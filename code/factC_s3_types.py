"""notes/103 sec. 8: full S_3 type (action on the three pair-partitions) of the six transports allowed by fact C,
P = {i,j} (coords (s_i, s_j)), P' = {i,k} (coords (s_i, s_k)).  Partitions: 'i' = cosets of <01>, 'o' (other: j or
k) = cosets of <10>, 'A' = cosets of <11>.  Type = images of (A, i, o).  Find all F_2-linear relations between the
counts of the 6 types valid for all 58 solutions."""
import itertools
from collections import Counter
import numpy as np

V = [(0, 0), (0, 1), (1, 0), (1, 1)]
add = lambda a, b: ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)
bij = [dict(zip(V, p)) for p in itertools.permutations(V)]
target = {u: {z: (1 if z[0] == u[0] else 2) for z in V} for u in V}
img = [[V.index(f[u]) for u in V] for f in bij]
name = {(0, 1): 'i', (1, 0): 'o', (1, 1): 'A'}


def s3type(f):
    t = f[(0, 0)]
    L = {v: add(f[v], t) for v in [(1, 1), (0, 1), (1, 0)]}
    return ''.join(name[L[v]] for v in [(1, 1), (0, 1), (1, 0)])   # images of A, i, o


types = sorted({s3type(f) for f in bij})
rows = []
for ms in itertools.combinations_with_replacement(range(24), 6):
    ok = True
    for a, u in enumerate(V):
        c = [0, 0, 0, 0]
        for t in ms:
            c[img[t][a]] += 1
        if any(c[b] != target[u][z] for b, z in enumerate(V)):
            ok = False; break
    if ok:
        cnt = Counter(s3type(bij[t]) for t in ms)
        rows.append([cnt[t] for t in types])
M = np.array(rows) % 2
print('types (images of A,i,o):', types, ' solutions:', len(rows))
# relations: vectors r with M r = const (mod 2) for all rows; test all 2^6 subsets
for mask in range(1, 64):
    r = np.array([(mask >> b) & 1 for b in range(6)])
    vals = set(int(x) for x in (M @ r) % 2)
    if len(vals) == 1:
        print('  sum of counts of', [types[b] for b in range(6) if r[b]], '== %d (mod 2) always' % vals.pop())
