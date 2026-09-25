"""notes/103 sec. 10: is the composition defect of the extended shift a function of the LINEAR PARTS only?
We need delta(psi) for psi = g^{-1} o f (transports) and delta(g o f).  Try several candidate extensions of delta to
non-isometric maps: delta = t . w(L) for a vector w(L) depending on the linear part (all 2^(2*6) choices are too many;
we search w: GL(2,2) -> F_2^2 with w(L) = (1,1) on the two isometric L, and test whether
d(f, g) = delta(g^{-1} f) + delta(f) + delta(g) depends only on (L_f, L_g))."""
import itertools

V = [(0, 0), (0, 1), (1, 0), (1, 1)]
add = lambda a, b: ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)
bij = [dict(zip(V, p)) for p in itertools.permutations(V)]
def lin(f):
    t = f[(0, 0)]
    return tuple(add(f[v], t) for v in [(0, 1), (1, 0)]), t
Ls = sorted({lin(f)[0] for f in bij})
iso = [L for L in Ls if add(L[0], L[1]) == (1, 1)]     # L(11) = L(01) + L(10) = 11
def inv(f): return {f[u]: u for u in V}
def comp(g, f): return {u: g[f[u]] for u in V}
others = [L for L in Ls if L not in iso]
good = []
for choice in itertools.product([(0, 0), (0, 1), (1, 0), (1, 1)], repeat=len(others)):
    w = {L: (1, 1) for L in iso}
    w.update(dict(zip(others, choice)))
    def delta(f):
        L, t = lin(f); return (t[0] * w[L][0] + t[1] * w[L][1]) % 2
    table, ok = {}, True
    for f in bij:
        for g in bij:
            key = (lin(f)[0], lin(g)[0])
            val = (delta(comp(inv(g), f)) + delta(f) + delta(g)) % 2
            if table.setdefault(key, val) != val:
                ok = False; break
        if not ok: break
    if ok:
        good.append(dict(w))
print('candidate extensions w (on the 4 non-isometric L) with defect depending only on linear parts:', len(good))
for w in good[:4]:
    print('  ', {str(k): v for k, v in w.items() if k not in iso})
