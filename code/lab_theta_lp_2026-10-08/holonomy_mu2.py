"""C1, lab session, 2026-10-09, mandate B. The same orientation class for ANY graph in which two vertices at distance two
have exactly two common neighbours (any lambda): for adjacent v, w, PHI_vw : N[v] -> N[w] is the identity on the common
closed neighbourhood and sends x in N(v) minus N[w] to the common neighbour of x and w other than v.
Question decided here: is the class zero on every available graph of DIAMETER TWO with mu = 2?
  python holonomy_mu2.py        (builds the test graphs itself; one process, seconds)"""
import itertools, collections


def run(name, n, E):
    adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    k = len(adj[0]); assert all(len(s) == k for s in adj)
    lam = {len(adj[a] & adj[b]) for a, b in E}
    dist2 = [(a, b) for a in range(n) for b in range(a + 1, n) if b not in adj[a] and adj[a] & adj[b]]
    assert all(len(adj[a] & adj[b]) == 2 for a, b in dist2), name
    diam2 = len(dist2) + len(E) == n * (n - 1) // 2

    def phi(v, w):
        d = {x: x for x in ({v, w} | (adj[v] & adj[w]))}
        for x in adj[v]:
            if x not in d: d[x] = next(iter((adj[x] & adj[w]) - {v}))
        return d

    def sgn(d, o1, o2):
        pos = {y: i for i, y in enumerate(o2)}; p = [pos[d[x]] for x in o1]; seen = [False] * len(p); s = 0
        for i in range(len(p)):
            if not seen[i]:
                j = i; ln = 0
                while not seen[j]: seen[j] = True; j = p[j]; ln += 1
                s ^= (ln - 1) & 1
        return s
    order = [[v] + sorted(adj[v]) for v in range(n)]; f = {}
    for a, b in E:
        d = phi(a, b); assert sorted(d.values()) == sorted(order[b])
        f[(a, b)] = f[(b, a)] = sgn(d, order[a], order[b])
    quads = {(a, b) + tuple(sorted(adj[a] & adj[b])) for a, b in dist2 if (a, b) < tuple(sorted(adj[a] & adj[b]))}
    odd = sum((f[(v, a)] + f[(a, w)] + f[(w, b)] + f[(b, v)]) % 2 for v, w, a, b in quads)
    tri = {tuple(sorted((a, b, c))) for a, b in E for c in adj[a] & adj[b]}
    oddt = sum((f[(a, b)] + f[(b, c)] + f[(a, c)]) % 2 for a, b, c in tri)
    per_edge = collections.Counter()
    for v, w, a, b in quads:
        for e in ((v, a), (a, w), (w, b), (b, v)): per_edge[tuple(sorted(e))] += 1
    pe = set(per_edge.values())
    pot = [None] * n; pot[0] = 0; st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if pot[y] is None: pot[y] = pot[x] ^ f[(x, y)]; st.append(y)
    zero = all((pot[a] ^ pot[b]) == f[(a, b)] for a, b in E)
    pot2 = [None] * n; pot2[0] = 0; st = [0]                             # the same test for f + 1 (class = length mod 2)
    while st:
        x = st.pop()
        for y in adj[x]:
            if pot2[y] is None: pot2[y] = pot2[x] ^ f[(x, y)] ^ 1; st.append(y)
    length = all((pot2[a] ^ pot2[b]) == (f[(a, b)] ^ 1) for a, b in E)
    print("%-22s n %3d k %2d lambda %s diameter two: %-5s quadrangles per edge %s | odd triangles %d of %d, odd quadrangles %d of %d | class %s"
          % (name, n, k, sorted(lam), diam2, sorted(pe), oddt, len(tri), odd, len(quads), "ZERO" if zero else "LENGTH MOD 2" if length else "OTHER"))


def cayley(elems, add, gens):
    idx = {e: i for i, e in enumerate(elems)}
    return len(elems), sorted({tuple(sorted((idx[e], idx[add(e, g)]))) for e in elems for g in gens})


F24 = list(itertools.product(range(2), repeat=4)); x4 = lambda a, b: tuple((p + q) % 2 for p, q in zip(a, b))
run("Clebsch (16,5,0,2)", *cayley(F24, x4, [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (1, 1, 1, 1)]))
Z44 = list(itertools.product(range(4), repeat=2)); a4 = lambda a, b: ((a[0] + b[0]) % 4, (a[1] + b[1]) % 4)
for m in (3,):                                                            # lambda >= 2 is outside the construction (PHI is not a bijection)
    V = list(itertools.product(range(m), repeat=2)); idx = {v: i for i, v in enumerate(V)}
    run("rook %dx%d" % (m, m), m * m, [(idx[a], idx[b]) for a in V for b in V if a < b and ((a[0] == b[0]) != (a[1] == b[1]))])
for d in (3, 4, 5):
    V = list(itertools.product(range(2), repeat=d)); idx = {v: i for i, v in enumerate(V)}
    run("cube Q%d" % d, 2 ** d, [(idx[a], idx[b]) for a in V for b in V if a < b and sum(p != q for p, q in zip(a, b)) == 1])
V = list(itertools.product(range(2), repeat=5)); idx = {}
reps = []
for v in V:
    c = tuple(1 - t for t in v)
    if c not in idx: idx[v] = len(reps); idx[c] = len(reps); reps.append(v)
run("folded 5-cube", 16, sorted({tuple(sorted((idx[a], idx[b]))) for a in V for b in V if sum(p != q for p, q in zip(a, b)) == 1 and idx[a] != idx[b]}))

import json, os, sys
D = sys.argv[1] if len(sys.argv) > 1 else None
if D:
    for g in ("t2_twisted", "t2_untwisted", "t3_twisted", "t3_twisted_42"):
        A = json.load(open(os.path.join(D, g + ".json"))); m = len(A)
        run(g, m, [(i, j) for i in range(m) for j in range(i + 1, m) if A[i][j]])
    for g in ("bvls243", "twin243_switched"):
        E = [tuple(map(int, l.split())) for l in open(os.path.join(D, "srg243", g + ".edges")) if l.strip()]
        run(g, 243, E)
