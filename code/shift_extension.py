"""notes/103 sec. 7: try to extend the diagonal shift delta to non-isometric edges.
For an affine bijection f(u) = Lu + t of F_2^2: isometric iff L(11) = 11, delta = t1 + t2.
Non-isometric: A-image a = L(11) in {01, 10}; candidate delta_N(f) = t1 if a = 01, t2 if a = 10 (the coordinate
killed by the functional vanishing on a).  For each edge map phi and each solution triple of the transport rule
{psi_R(u)} = {phi(u), phi(u)+11, phi(u+11)}, print for every transport psi_R: iso?/shift and compare with phi's data.
Transports psi_R = phi_{P'R}^{-1} o phi_{PR} are composites; here we only look at the multiset {psi_R}."""
import itertools
from collections import Counter

V = [(0, 0), (0, 1), (1, 0), (1, 1)]
add = lambda a, b: ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)
bij = [dict(zip(V, p)) for p in itertools.permutations(V)]


def data(f):
    t = f[(0, 0)]
    a = add(f[(1, 1)], t)                        # L(11)
    if a == (1, 1):
        return ('I', (t[0] + t[1]) % 2)
    return ('N', a, t[0] if a == (0, 1) else t[1])


out = Counter()
for phi in bij:
    for tri in itertools.combinations_with_replacement(range(24), 3):
        fs = [bij[t] for t in tri]
        if all(sorted(f[u] for f in fs) == sorted([phi[u], add(phi[u], (1, 1)), phi[add(u, (1, 1))]]) for u in V):
            dp = data(phi)
            key = (dp[0], tuple(sorted(str(data(f)) for f in fs)), dp[-1])
            out[key] += 1
for k, c in sorted(out.items()):
    print(c, 'phi', k[0], 'delta(phi)=%d' % k[2], ' transports:', k[1])

print('\n--- composition defect of the extended shift: c(f,g) = delta(g o f) + delta(f) + delta(g) ---')
def delta(f):
    d = data(f); return d[-1]
def kind(f):
    d = data(f); return 'I' if d[0] == 'I' else 'N' + ''.join(map(str, d[1]))
def comp(g, f):
    return {u: g[f[u]] for u in V}
def inv(f):
    return {f[u]: u for u in V}
tab = {}
for f in bij:
    for g in bij:
        key = (kind(f), kind(g), kind(comp(g, f)))
        tab.setdefault(key, Counter())[(delta(comp(g, f)) + delta(f) + delta(g)) % 2] += 1
for k in sorted(tab):
    print(k, dict(tab[k]))
print('delta(f^-1) + delta(f) by kind:', {k: dict(c) for k, c in
      ((kk, Counter((delta(inv(f)) + delta(f)) % 2 for f in bij if kind(f) == kk)) for kk in ('I', 'N01', 'N10'))})
