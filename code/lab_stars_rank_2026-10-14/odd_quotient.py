"""h-odd quotient of the 59-vertex four-star graph (15/10/2026, LAB).
For an h-symmetric structure (h = (a a')(b b'), outer letters fixed), the h-odd eigenvectors of A_Sigma vanish on v and on
the outer letters; they are carried by 24 orbits: a^ (a/a'), b^ (b/b'), [ax] (x outer), [by] (y outer), g1 = [ab] = {ab, a'b'},
g2 = [ab'] = {ab', a'b}.  Their signed adjacency A^- (representative ab for g1, ab' for g2) has spectrum in [-4, 3] iff
T and U are PSD on the odd sector, and mult_3(A^-) = nullity of the h-odd sector of T (Haynsworth).  Conjecture ODD-h:
mult_3(A^-) = 2 (the two star differences).
usage: python odd_quotient.py <json>"""
import sys, json
import numpy as np
from ext4 import kval
d = json.load(open(sys.argv[1]))
S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {l: i for i, l in enumerate(S)}
G = np.zeros((n, n), dtype=int)
for i, j in d["edges"]: G[i, j] = G[j, i] = 1
hmap = {0: 1, 1: 0, 2: 3, 3: 2}
perm = [idx[frozenset(hmap.get(y, y) for y in S[i])] for i in range(n)]
assert all(G[perm[i], perm[j]] == G[i, j] for i in range(n) for j in range(n)), "not h-symmetric"
Y = list(range(4, 14))
# vertices of the full 59-vertex graph: v, letters 0..13, labels
V = ['v'] + ['L%d' % y for y in range(14)] + ['S%d' % i for i in range(n)]
N = len(V); pos = {name: k for k, name in enumerate(V)}
A = np.zeros((N, N))
def add(p, q):
    A[pos[p], pos[q]] = A[pos[q], pos[p]] = 1
for y in range(14):
    add('v', 'L%d' % y)
for y in range(0, 14, 2):
    add('L%d' % y, 'L%d' % (y + 1))
for i in range(n):
    for y in S[i]:
        add('L%d' % y, 'S%d' % i)
    for j in range(i + 1, n):
        if G[i, j]: add('S%d' % i, 'S%d' % j)
# h on the full vertex set
def himg(name):
    if name == 'v': return 'v'
    if name[0] == 'L': return 'L%d' % hmap.get(int(name[1:]), int(name[1:]))
    return 'S%d' % perm[int(name[1:])]
H = np.zeros((N, N))
for k, name in enumerate(V): H[pos[himg(name)], k] = 1
assert np.allclose(H @ A @ H.T, A)
# odd basis: (e_p - e_h(p))/sqrt2 for each orbit of size 2 (fixed vertices carry nothing)
orbs, seen = [], set()
for k, name in enumerate(V):
    hn = himg(name)
    if hn == name or name in seen: continue
    seen.add(name); seen.add(hn); orbs.append((name, hn))
B = np.zeros((N, len(orbs)))
for c, (p, q) in enumerate(orbs):
    B[pos[p], c] = 1 / np.sqrt(2); B[pos[q], c] = -1 / np.sqrt(2)
Am = B.T @ A @ B
ev = np.sort(np.linalg.eigvalsh(Am))
full = np.sort(np.linalg.eigvalsh(A))
print('%s: odd quotient has %d vertices; spectrum of A^-:' % (sys.argv[1], len(orbs)))
print('  ', np.round(ev, 4))
print('  mult of 3: %d, min eigenvalue %.4f; full A_Sigma: lambda_1 %.3f, lambda_2 %.4f, lambda_min %.4f, mult_3 %d, mult_-4 %d'
      % (int(np.sum(np.abs(ev - 3) < 1e-7)), ev[0], full[-1], full[-2], full[0], int(np.sum(np.abs(full - 3) < 1e-7)),
         int(np.sum(np.abs(full + 4) < 1e-7))))
