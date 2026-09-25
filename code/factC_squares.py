"""notes/103 sec. 10: square holonomies.  For a T7 pair (P, P'), the six intermediates R form three complementary
couples {R, Rbar}.  Square holonomy q = psi_Rbar^{-1} o psi_R in Sym(Q_P).  For every fact-C solution (multiset of 6
affine maps) and every pairing into 3 couples, record the multiset of conjugacy classes of q."""
import itertools
from collections import Counter

V = [(0, 0), (0, 1), (1, 0), (1, 1)]
bij = [dict(zip(V, p)) for p in itertools.permutations(V)]
target = {u: {z: (1 if z[0] == u[0] else 2) for z in V} for u in V}
img = [[V.index(f[u]) for u in V] for f in bij]


def ctype(p):  # p: dict V -> V
    seen, cyc = set(), []
    for a in V:
        if a in seen: continue
        l, b = 0, a
        while b not in seen:
            seen.add(b); b = p[b]; l += 1
        cyc.append(l)
    return {(1, 1, 1, 1): 'id', (1, 1, 2): 'tr', (2, 2): 'dt', (1, 3): '3c', (4,): '4c'}[tuple(sorted(cyc))]


def square(f, g):   # q = g^{-1} o f  (both Q_P -> Q_P')
    ginv = {g[u]: u for u in V}
    return ctype({u: ginv[f[u]] for u in V})


def pairings(items):
    if not items:
        yield []; return
    a = items[0]
    for i in range(1, len(items)):
        for rest in pairings(items[1:i] + items[i + 1:]):
            yield [(a, items[i])] + rest


sols = []
for ms in itertools.combinations_with_replacement(range(24), 6):
    ok = True
    for a, u in enumerate(V):
        c = [0, 0, 0, 0]
        for t in ms:
            c[img[t][a]] += 1
        if any(c[b] != target[u][z] for b, z in enumerate(V)):
            ok = False; break
    if ok:
        sols.append(ms)
allcls, min_nontriv = Counter(), []
for ms in sols:
    best = 9
    for pr in pairings(list(ms)):
        cls = tuple(sorted(square(bij[a], bij[b]) for a, b in pr))
        allcls[cls] += 1
        best = min(best, sum(c != 'id' for c in cls))
    min_nontriv.append(best)
print('solutions', len(sols), '; min number of non-identity squares over pairings:', Counter(min_nontriv))
print('square-class triples reachable (count over solutions x pairings):')
for k, v in sorted(allcls.items(), key=lambda kv: -kv[1]):
    print('  ', k, v)
