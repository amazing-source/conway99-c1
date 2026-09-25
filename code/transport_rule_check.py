"""notes/103 sec. 5: transport rule at a Kneser edge (P, P') of a Hamming point (fact D + B of notes/95):
for all u, the multiset {psi_R(u)}_R = {phi(u), phi(u)+11, phi(u+11)}.  Count isometric transports (commuting with +11)
among the solutions, for isometric and non-isometric phi."""
import itertools
from collections import Counter

V = [(0, 0), (0, 1), (1, 0), (1, 1)]
add = lambda a, b: ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)
E = (1, 1)
bij = [dict(zip(V, p)) for p in itertools.permutations(V)]
iso = lambda f: all(f[add(u, E)] == add(f[u], E) for u in V)

for phi in (bij[0], next(f for f in bij if not iso(f))):
    cnt = Counter()
    for tri in itertools.combinations_with_replacement(range(24), 3):
        fs = [bij[t] for t in tri]
        if all(sorted(f[u] for f in fs) == sorted([phi[u], add(phi[u], E), phi[add(u, E)]]) for u in V):
            cnt[sum(iso(f) for f in fs)] += 1
    print('phi isometric' if iso(phi) else 'phi non-isometric', '-> number of isometric transports: counts', dict(cnt))
