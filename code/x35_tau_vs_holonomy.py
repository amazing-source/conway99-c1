# Heuristic exploration (not a proof): random line data at P = S = 0 (girth(G(L)) >= 5, connected), is 7 | tau(G(L))
# correlated with the cycle type of the holonomy sigma?
import random, itertools
from collections import Counter, defaultdict
def rank_mod(Mx, p=7):
    Mx = [[v % p for v in r] for r in Mx]; n, m = len(Mx), len(Mx[0]); r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if Mx[i][c]), None)
        if piv is None: continue
        Mx[r], Mx[piv] = Mx[piv], Mx[r]; inv = pow(Mx[r][c], p - 2, p); Mx[r] = [(v * inv) % p for v in Mx[r]]
        for i in range(n):
            if i != r and Mx[i][c]:
                f = Mx[i][c]; Mx[i] = [(a - f * b) % p for a, b in zip(Mx[i], Mx[r])]
        r += 1
    return r
rng = random.Random(7)
labs = list(range(12)); mate = {i: i ^ 1 for i in labs}
def rand_tau():
    while True:
        perm = labs[:]; rng.shuffle(perm); t = {}; ok = True
        for i in range(0, 12, 2):
            a, b = perm[i], perm[i + 1]
            if mate[a] == b: ok = False; break
            t[a], t[b] = b, a
        if ok: return t
def cyc(s):
    out = []; done = set()
    for i in labs:
        if i in done: continue
        c = 0; j = i
        while j not in done: done.add(j); j = s[j]; c += 1
        out.append(c)
    return tuple(sorted(out))
stats = defaultdict(Counter); n = 0; tries = 0
while n < 3000 and tries < 10**6:
    tries += 1
    tu, tb = rand_tau(), rand_tau(); s = labs[:]; rng.shuffle(s); s = dict(zip(labs, s))
    if not all(s[v] not in (v, mate[v], tu[v], tb[v]) for v in labs): continue
    if not all(tb[s[w]] != s[tu[w]] for w in labs): continue
    # Laplacian of G(L): x-layer 0..11, u-layer 12..23, ub-layer 24..35
    A = [[0] * 36 for _ in range(36)]
    def e(a, b): A[a][b] = A[b][a] = 1
    for v in labs:
        e(v, mate[v]); e(12 + v, 12 + tu[v]); e(24 + v, 24 + tb[v]); e(v, 12 + v); e(v, 24 + v); e(12 + v, 24 + s[v])
    L = [[(3 if i == j else 0) - A[i][j] for j in range(36)] for i in range(36)]
    null7 = 36 - rank_mod(L)
    # connectivity: nullity over Q of L = number of components; approximate with nullity mod a large prime
    ncomp = 36 - rank_mod(L, 1000003)
    if ncomp != 1: continue
    n += 1
    stats[cyc(s)][null7 > 1] += 1
tot = Counter()
for k, c in stats.items(): tot[True] += c[True]; tot[False] += c[False]
print(f'{n} connected girth>=5 balls: 7 | tau in {tot[True]} ({100*tot[True]/n:.1f}%)')
rows = sorted(stats.items(), key=lambda kv: -(kv[1][True] + kv[1][False]))
for k, c in rows[:15]:
    m = c[True] + c[False]
    print(f'  sigma cycles {k}: {m:5d} balls, 7 | tau in {c[True]:4d} ({100*c[True]/m:5.1f}%)')
