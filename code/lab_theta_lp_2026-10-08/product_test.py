"""C1, lab session, 2026-10-09. The Cartesian product of two graphs of the family (every edge in one triangle, pairs at
distance two with two common neighbours) is in the family. Face count of a line T of the first factor in the product:
F = F_1(T) + 5 k_2 / 2, so a universal parity law (F constant over the lines of a graph) forces kappa + k/2 to be the same
for all members. The 42-vertex twisted geometry has kappa + k/2 = 0, all the others 1: test the law on products.
  python product_test.py <codex data folder>       One process, seconds, below 500 MB."""
import sys, os, json, collections
D = sys.argv[1]


def load(name):
    if name == "K3": return 3, [(0, 1), (0, 2), (1, 2)]
    if name == "grid": return 9, [(3 * i + j, 3 * i2 + j2) for i in range(3) for j in range(3) for i2 in range(3) for j2 in range(3) if (i == i2) != (j == j2) and 3 * i + j < 3 * i2 + j2]
    A = json.load(open(os.path.join(D, name + ".json"))); m = len(A)
    return m, [(i, j) for i in range(m) for j in range(i + 1, m) if A[i][j]]


def product(g1, g2):
    n1, E1 = g1; n2, E2 = g2
    E = [(a * n2 + y, b * n2 + y) for a, b in E1 for y in range(n2)] + [(x * n2 + a, x * n2 + b) for a, b in E2 for x in range(n1)]
    return n1 * n2, E


def study(name, n, E):
    adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    k = len(adj[0]); assert all(len(s) == k for s in adj); third = {}
    for a, b in E:
        cn = adj[a] & adj[b]; assert len(cn) == 1; t = next(iter(cn)); third[(a, b)] = third[(b, a)] = t
    pi = lambda v, w, x: next(iter((adj[x] & adj[w]) - {v}))

    def sgn(d, o1, o2):
        pos = {y: i for i, y in enumerate(o2)}; p = [pos[d[x]] for x in o1]; seen = [False] * len(p); s = 0
        for i in range(len(p)):
            if not seen[i]:
                j = i; ln = 0
                while not seen[j]: seen[j] = True; j = p[j]; ln += 1
                s ^= (ln - 1) & 1
        return s
    order = [[v] + sorted(adj[v]) for v in range(n)]; f = {}; c = {}
    for a, b in E:
        t = third[(a, b)]; d = {a: a, b: b, t: t}
        for x in adj[a]:
            if x != b and x != t:
                cn = (adj[x] & adj[b]) - {a}; assert len(cn) == 1; d[x] = next(iter(cn))
        f[(a, b)] = f[(b, a)] = sgn(d, order[a], order[b])
        X = [x for x in adj[a] if x != b and x != t]; seen = set(); cyc = 0
        for x in X:
            if x in seen: continue
            cyc += 1; u = x
            while u not in seen:
                seen.add(u); u1 = third[(a, u)]; seen.add(u1); y = pi(a, b, u1); y1 = third[(b, y)]; u = pi(b, a, y1)
        c[(a, b)] = c[(b, a)] = cyc
    out = []
    for const in (0, 1):
        g = {e: (f[e] + c[e] + const) % 2 for e in f}; pot = [None] * n; pot[0] = 0; st = [0]
        while st:
            x = st.pop()
            for y in adj[x]:
                if pot[y] is None: pot[y] = pot[x] ^ g[(x, y)]; st.append(y)
        out.append(all((pot[a] ^ pot[b]) == g[(a, b)] for a, b in E))
    lines = sorted({tuple(sorted((a, b, third[(a, b)]))) for a, b in E}); par = collections.Counter()
    for u, v, w in lines: par[(f[(u, v)] + f[(v, w)] + f[(w, u)] + c[(u, v)] + c[(v, w)] + c[(w, u)]) % 2] += 1
    print("%-28s n %5d k %2d | lines by parity of (f + c)(T): %s | f + c coboundary %s, f + c + 1 coboundary %s" % (name, n, k, dict(par), out[0], out[1]), flush=True)


for a, b in (("t3_twisted", "K3"), ("t3_twisted_42", "K3"), ("t2_twisted", "K3"), ("t2_twisted", "t3_twisted_42"), ("t3_twisted", "t3_twisted_42"), ("grid", "t3_twisted_42"), ("t2_twisted", "t3_twisted")):
    n, E = product(load(a), load(b)); study(a + " x " + b, n, E)
