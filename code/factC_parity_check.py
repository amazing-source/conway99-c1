"""notes/103: fact C (mu between two grids sharing class i) for P = {i,j}, P' = {i,k}: the six transports
psi_R : Q_P -> Q_P' (R in [7] minus {i,j,k}) send each u to the two points of Q_P' with the same i-sign once each and to
the two with the opposite i-sign twice each (i = first coordinate on both sides).  Enumerate all multisets of 6
bijections of F_2^2 with this property; report the number of isometries (commuting with +11) in each."""
import itertools
from collections import Counter

V = [(0, 0), (0, 1), (1, 0), (1, 1)]
add = lambda a, b: ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)
bij = [dict(zip(V, p)) for p in itertools.permutations(V)]
iso = [all(f[add(u, (1, 1))] == add(f[u], (1, 1)) for u in V) for f in bij]
target = {u: {z: (1 if z[0] == u[0] else 2) for z in V} for u in V}
img = [[V.index(f[u]) for u in V] for f in bij]

sols, niso = 0, Counter()
for ms in itertools.combinations_with_replacement(range(24), 6):
    ok = True
    for a, u in enumerate(V):
        c = [0, 0, 0, 0]
        for t in ms:
            c[img[t][a]] += 1
        if any(c[b] != target[u][z] for b, z in enumerate(V)):
            ok = False; break
    if ok:
        sols += 1; niso[sum(iso[t] for t in ms)] += 1
print('multisets satisfying fact C:', sols, '; number of isometries among the six -> count:', dict(sorted(niso.items())))

# fine types: I0 / I1 (isometric, diagonal shift 0 / 1), or N(x, y): A(P) -> pi_x(P'), pi_y(P) -> A(P')
# coordinates: P = (s_i, s_j), P' = (s_i, s_k).  pi_i = cosets of <01>, pi_j / pi_k = cosets of <10>, A = cosets of <11>
def part_of(v):
    return {(0, 1): 'i', (1, 0): 'second', (1, 1): 'A'}[v]


def lin(f):
    t = f[(0, 0)]
    return {v: add(f[v], t) for v in V if v != (0, 0)}


def ftype(f):
    L = lin(f)
    if L[(1, 1)] == (1, 1):
        t = f[(0, 0)]
        return 'I%d' % ((t[0] + t[1]) % 2)
    x = part_of(L[(1, 1)])                                  # image of A(P): 'i' or 'second' (= k)
    y = part_of(next(v for v in L if L[v] == (1, 1)))        # preimage of A(P'): 'i' or 'second' (= j)
    return 'N(%s,%s)' % ('i' if x == 'i' else 'k', 'i' if y == 'i' else 'j')


prof = Counter()
for ms in itertools.combinations_with_replacement(range(24), 6):
    ok = all(sorted(img[t][a] for t in ms) == sorted(sum(([b] * target[u][z] for b, z in enumerate(V)), [])) for a, u in enumerate(V))
    if ok:
        prof[tuple(sorted(Counter(ftype(bij[t]) for t in ms).items()))] += 1
for p, c in sorted(prof.items(), key=lambda kv: -kv[1]):
    print(c, dict(p))
