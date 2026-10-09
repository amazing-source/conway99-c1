"""C1, lab session, 2026-10-09, mandate B. Test of a precise formula: is the orientation class represented by the
canonical cochain  e -> c_e (number of two-layer cycles of the edge e) + constant ?  Equivalently: is f + c a
coboundary or a coboundary plus the constant 1, where f is the sign cochain of PHI' in any gauge.
  python two_layer_test.py <data folder>     One process, seconds."""
import sys, os, json, collections
D = sys.argv[1]


def study(name, n, E):
    adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    k = len(adj[0]); third = {}
    for a, b in E:
        t = next(iter(adj[a] & adj[b])); third[(a, b)] = third[(b, a)] = t
    pi = lambda v, w, x: next(iter((adj[x] & adj[w]) - {v}))

    def phi(v, w):
        t = third[(v, w)]; d = {v: v, w: w, t: t}
        for x in adj[v]:
            if x != w and x != t: d[x] = pi(v, w, x)
        return d

    def sgn(d, o1, o2):
        pos = {y: i for i, y in enumerate(o2)}; p = [pos[d[x]] for x in o1]; seen = [False] * len(p); s = 0
        for i in range(len(p)):
            if not seen[i]:
                j = i; ln = 0
                while not seen[j]: seen[j] = True; j = p[j]; ln += 1
                s ^= (ln - 1) & 1
        return s
    order = [[v] + sorted(adj[v]) for v in range(n)]
    f = {}; c = {}; lens = collections.Counter()
    for a, b in E:
        f[(a, b)] = f[(b, a)] = sgn(phi(a, b), order[a], order[b])
        t = third[(a, b)]; X = [x for x in adj[a] if x != b and x != t]; seen = set(); cyc = 0
        for x in X:                                        # cycle: x -mate- x' -cross- y -mate- y' -cross- ...
            if x in seen: continue
            cyc += 1; u = x; ln = 0
            while u not in seen:
                seen.add(u); u1 = third[(a, u)]; seen.add(u1); y = pi(a, b, u1); y1 = third[(b, y)]; u = pi(b, a, y1); ln += 1
            lens[ln] += 1
        c[(a, b)] = c[(b, a)] = cyc
    out = []
    for const in (0, 1):
        g = {e: (f[e] + c[e] + const) % 2 for e in f}
        pot = [None] * n; pot[0] = 0; st = [0]
        while st:
            x = st.pop()
            for y in adj[x]:
                if pot[y] is None: pot[y] = pot[x] ^ g[(x, y)]; st.append(y)
        out.append(all((pot[a] ^ pot[b]) == g[(a, b)] for a, b in E))
    print("%-18s edges by number of two-layer cycles %s (cycle lengths in pairs of lines: %s) | f + c coboundary: %s, f + c + 1 coboundary: %s"
          % (name, dict(sorted(collections.Counter(c[e] for e in E).items())), dict(sorted(lens.items())), out[0], out[1]))


for g in ("t2_twisted", "t2_untwisted", "t3_twisted", "t3_twisted_42"):
    A = json.load(open(os.path.join(D, g + ".json"))); m = len(A)
    study(g, m, [(i, j) for i in range(m) for j in range(i + 1, m) if A[i][j]])
for g in ("bvls243", "twin243_switched"):
    study(g, 243, [tuple(map(int, l.split())) for l in open(os.path.join(D, "srg243", g + ".edges")) if l.strip()])
