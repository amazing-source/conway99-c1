"""helpers shared by product_test.py style scripts (lab session, 2026-10-09)"""
import os, json


def load(D, name):
    if name == "K3": return 3, [(0, 1), (0, 2), (1, 2)]
    if name == "grid": return 9, [(3 * i + j, 3 * i2 + j2) for i in range(3) for j in range(3) for i2 in range(3) for j2 in range(3) if (i == i2) != (j == j2) and 3 * i + j < 3 * i2 + j2]
    if name in ("bvls243", "twin243_switched"):
        return 243, [tuple(map(int, l.split())) for l in open(os.path.join(D, "srg243", name + ".edges")) if l.strip()]
    A = json.load(open(os.path.join(D, name + ".json"))); m = len(A)
    return m, [(i, j) for i in range(m) for j in range(i + 1, m) if A[i][j]]


def product(g1, g2):
    n1, E1 = g1; n2, E2 = g2
    E = [(a * n2 + y, b * n2 + y) for a, b in E1 for y in range(n2)] + [(x * n2 + a, x * n2 + b) for a, b in E2 for x in range(n1)]
    return n1 * n2, E


def cochains(n, E):
    """adjacency, third points, sign cochain f of PHI' (orders: v then sorted neighbours), two-layer cycle counts c, valency"""
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
    return adj, third, f, c, k
