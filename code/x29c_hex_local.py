# Check on BvLS the local rung bookkeeping for induced hexagons through a vertex x:
# H(x) = (1/2) sum_{q at distance 2} N(q), N(q) = # ordered pairs of 'rungs' (u,p) (x~u~p~q, u not~ q, p not~ x)
# with u'!=u, u' not~ u, p'!=p, p' not~ p, u not~ p', u' not~ p.  Compare with a direct count of induced 6-cycles through x.
import itertools, numpy as np
exec(open('code/x29_bvls_triangle.py').read().split('# a triangle through 0')[0])
v = 243
nb = [set(np.nonzero(A[i])[0]) for i in range(v)]
x = 0
Nx = nb[x]
far = [q for q in range(v) if q != x and q not in Nx]
tot = 0
for q in far:
    rungs = [(u, p) for u in Nx if u not in nb[q] for p in nb[u] & nb[q] if p != x and p not in Nx]
    cnt = 0
    for (u, p), (u2, p2) in itertools.permutations(rungs, 2):
        if u2 == u or u2 in nb[u]: continue
        if p2 == p or p2 in nb[p]: continue
        if p2 in nb[u] or p in nb[u2]: continue
        cnt += 1
    tot += cnt
Hx_rungs = tot // 2
# direct: induced 6-cycles through x
Hx = 0
for u, u2 in itertools.combinations(Nx, 2):
    if u2 in nb[u]: continue
    for p in nb[u] - Nx - {x}:
        for p2 in nb[u2] - Nx - {x}:
            if p2 == p: continue
            for q in (nb[p] & nb[p2]) - {x}:
                S6 = [x, u, p, q, p2, u2]
                if len(set(S6)) < 6: continue
                e = sum(1 for a, b in itertools.combinations(S6, 2) if b in nb[a])
                if e == 6: Hx += 1
print('BvLS vertex 0: induced hexagons through x, rung formula =', Hx_rungs, ' direct =', Hx)
