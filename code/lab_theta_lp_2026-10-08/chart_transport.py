"""C1, lab session, 2026-10-09. Diameter two: the matched transport T~_vw : N(v) -> N(w) (shift by two along the
oriented two-layer cycles; it sends mates to mates) extends canonically to a permutation T^_vw of ALL vertices:
v -> w, x -> T~(x), [x, y]_v -> [T~x, T~y]_w  ([x, y]_v = the common neighbour of x, y other than v).
Printed for a sample of edges: cycle type and sign of T^, and how far it is from an automorphism.
  python chart_transport.py <edge list> [number of edges]     One process, seconds."""
import sys, collections, random
E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]; n = 1 + max(max(e) for e in E)
SAMPLE = int(sys.argv[2]) if len(sys.argv) > 2 else 12
adj = [set() for _ in range(n)]
for a, b in E: adj[a].add(b); adj[b].add(a)
third = lambda a, b: next(iter(adj[a] & adj[b]))
pi = lambda v, w, x: next(iter((adj[x] & adj[w]) - {v}))
other = lambda x, y, v: next(iter((adj[x] & adj[y]) - {v}))


def transport(v, w):
    t = third(v, w); X = [x for x in adj[v] if x != w and x != t]
    T = {w: t, t: v}; seen = set(); ncyc = 0; lens = []
    for x in X:
        if x in seen: continue
        ncyc += 1; z = x; ln = 0
        while z not in seen:                      # z entry point at v, z1 exit, y entry at w, y1 exit
            seen.add(z); z1 = third(v, z); seen.add(z1); y = pi(v, w, z1); y1 = third(w, y)
            T[z] = y; T[z1] = y1; z = pi(w, v, y1); ln += 1
        lens.append(ln)
    return T, ncyc, tuple(sorted(lens))


def extend(v, w, T):
    P = {v: w}; P.update(T)
    for z in range(n):
        if z in P: continue
        x, y = sorted(adj[z] & adj[v]); P[z] = other(T[x], T[y], w)
    assert sorted(P.values()) == list(range(n))
    return P


def cyc(P):
    seen = set(); out = []
    for a in range(n):
        if a not in seen:
            ln = 0; u = a
            while u not in seen: seen.add(u); u = P[u]; ln += 1
            out.append(ln)
    return collections.Counter(out)


random.seed(2); stat = collections.Counter()
for (a, b) in random.sample(E, SAMPLE):
    T, c, lens = transport(a, b); P = extend(a, b, T); ct = cyc(P)
    sign = sum((l - 1) * m for l, m in ct.items()) % 2
    kept = sum(1 for x, y in E if P[y] in adj[P[x]])
    stat[(lens, sign, kept == len(E))] += 1
    print("edge %s: two-layer cycle sizes %s | cycles of T^ %s | sign %d | edges mapped to edges %d of %d"
          % ((a, b), lens, dict(sorted(ct.items())), sign, kept, len(E)))
print(dict(stat))
