"""C1, lab session, 2026-10-09, mandate B. For a cyclic orientation o of the lines, d_o(e) = number of mate pairs at the
two ends of the edge e (the lines through them other than the line of e) oriented against the traversal of their
two-layer cycle. The sign cochain is c + d_o in the gauge induced by o. Questions:
  1. is there an orientation with an even number of sides against the traversal in EVERY quadrangle ("balanced")?
  2. for such an orientation (or a random one), what does d_o look like: constant? coboundary plus constant?
  python balanced_orient.py <data folder>     One process, seconds."""
import sys, os, json, collections, random
D = sys.argv[1]; random.seed(5)


def gauss(rows, rhs, nv):
    piv = {}
    for r, b in zip(rows, rhs):
        m = r | (b << nv)
        while m & ((1 << nv) - 1):
            h = (m & ((1 << nv) - 1)).bit_length() - 1
            if h in piv: m ^= piv[h]
            else: piv[h] = m; break
        else:
            if m >> nv: return None
    sol = 0                                                 # back substitution, free variables = 0
    for h in sorted(piv):
        m = piv[h]; val = (m >> nv) & 1; low = m & ((1 << h) - 1)
        val ^= bin(low & sol).count("1") & 1
        if val: sol |= 1 << h
    return sol


def study(name, n, E):
    adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    k = len(adj[0]); third = {}
    for a, b in E:
        t = next(iter(adj[a] & adj[b])); third[(a, b)] = third[(b, a)] = t
    lines = sorted({tuple(sorted((a, b, third[(a, b)]))) for a, b in E}); lid = {L: i for i, L in enumerate(lines)}
    line_of = lambda a, b: lid[tuple(sorted((a, b, third[(a, b)])))]
    ref = lambda a, b: 0 if (lines[line_of(a, b)].index(b) - lines[line_of(a, b)].index(a)) % 3 == 1 else 1
    pi = lambda v, w, x: next(iter((adj[x] & adj[w]) - {v}))
    quads = []
    for v in range(n):
        for w in range(v + 1, n):
            if w in adj[v] or not (adj[v] & adj[w]): continue
            a, b = sorted(adj[v] & adj[w])
            if (v, w) < (a, b): quads.append((v, a, w, b))
    rows = []; rhs = []
    for (v, a, w, b) in quads:                               # arcs v->a, a->w, w->b, b->v : number against must be even
        m = 0; r = 0
        for p, q in ((v, a), (a, w), (w, b), (b, v)): m ^= 1 << line_of(p, q); r ^= ref(p, q)
        rows.append(m); rhs.append(r)
    sol = gauss(rows, rhs, len(lines))

    def d_of(o):                                            # o: bitmask over lines (1 = reversed reference)
        against = lambda p, q: ref(p, q) ^ ((o >> line_of(p, q)) & 1)       # arc p -> q against the orientation
        d = {}
        for a, b in E:
            t = third[(a, b)]; X = [x for x in adj[a] if x != b and x != t]; seen = set(); tot = 0
            for x in X:
                if x in seen: continue
                u = x
                while u not in seen:
                    seen.add(u); u1 = third[(a, u)]; seen.add(u1); tot += against(u, u1)
                    y = pi(a, b, u1); y1 = third[(b, y)]; tot += against(y, y1); u = pi(b, a, y1)
            d[(a, b)] = d[(b, a)] = tot % 2
        return d

    def shape(d):
        res = []
        for const in (0, 1):
            pot = [None] * n; pot[0] = 0; st = [0]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if pot[y] is None: pot[y] = pot[x] ^ d[(x, y)] ^ const; st.append(y)
            res.append(all((pot[a] ^ pot[b]) == (d[(a, b)] ^ const) for a, b in E))
        return "coboundary" if res[0] else "coboundary + 1" if res[1] else "OTHER"
    o_rand = random.getrandbits(len(lines)); d = d_of(o_rand)
    msg = "random orientation: d is %s" % shape(d)
    if sol is None: print("%-18s balanced orientation: NONE | %s" % (name, msg))
    else:
        d2 = d_of(sol); cnt = collections.Counter(d2[e] for e in E)
        print("%-18s balanced orientation: exists; d on the edges: %s (%s) | %s" % (name, dict(cnt), shape(d2), msg))


V3 = [(i, j) for i in range(3) for j in range(3)]; ix = {v: i for i, v in enumerate(V3)}
study("grid 3x3", 9, [(ix[a], ix[b]) for a in V3 for b in V3 if a < b and ((a[0] == b[0]) != (a[1] == b[1]))])
for g in ("t2_twisted", "t2_untwisted", "t3_twisted", "t3_twisted_42"):
    A = json.load(open(os.path.join(D, g + ".json"))); m = len(A)
    study(g, m, [(i, j) for i in range(m) for j in range(i + 1, m) if A[i][j]])
for g in ("bvls243", "twin243_switched"):
    study(g, 243, [tuple(map(int, l.split())) for l in open(os.path.join(D, "srg243", g + ".edges")) if l.strip()])
