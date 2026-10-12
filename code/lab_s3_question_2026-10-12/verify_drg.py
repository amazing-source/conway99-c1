"""Lab session, 2026-10-12. Independent check on an edge list of a graph on 243 vertices:
  1. it is a strongly regular graph with parameters (243,22,1,2);
  2. all its REGULAR SPREADS are found: partitions of the vertex set into 81 triangles, any two of them joined by 0 or 3
     edges (exhaustive backtracking on the 891 triangles);
  3. for each spread: the quotient is a srg(81,20,1,6); the graph minus the 243 spread edges is distance-regular with
     intersection array {20,18,4,1; 1,2,18,20} (checked on every pair of vertices), an antipodal 3-cover of the quotient;
     the cover is CYCLIC (the three sheets can be cyclically oriented so that every matching between adjacent fibres
     respects the orientation) or not.
  4. invariants for telling graphs apart: for each spread, the number of grid squares of the quotient (closed walks
     x, a, x+..., 4-cycles) whose lift is closed is not needed here; the script prints the sorted degree sequence of the
     "second common neighbour" structure: the number of 3x3 grids (induced K3 x K3) through each vertex.
python verify_drg.py <edge file> [<edge file> ...]        (standard library only; about a minute per graph)"""
import sys, itertools, collections


def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = 1 + max(max(e) for e in E); adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    return n, adj


def check_srg(n, adj, k, lam, mu):
    if any(len(a) != k for a in adj): return False
    for x in range(n):
        for y in range(x + 1, n):
            c = len(adj[x] & adj[y])
            if c != (lam if y in adj[x] else mu): return False
    return True


def spreads(n, adj):
    tri = sorted({tuple(sorted((x, y, next(iter(adj[x] & adj[y]))))) for x in range(n) for y in adj[x] if x < y})
    assert len(tri) == n * 22 // 6, len(tri)
    through = [[] for _ in range(n)]
    for i, t in enumerate(tri):
        for x in t: through[x].append(i)
    def compatible(s, t):
        if set(s) & set(t): return False
        e = sum(1 for x in s for y in t if y in adj[x])
        return e in (0, 3) and (e == 0 or all(sum(1 for y in t if y in adj[x]) == 1 for x in s))
    comp = {}
    def ok(i, j):
        key = (i, j) if i < j else (j, i)
        if key not in comp: comp[key] = compatible(tri[i], tri[j])
        return comp[key]
    found = []
    def rec(chosen, covered):
        if len(covered) == n: found.append(list(chosen)); return
        x = min(v for v in range(n) if v not in covered)
        for i in through[x]:
            if any(v in covered for v in tri[i]): continue
            if all(ok(i, j) for j in chosen):
                chosen.append(i); rec(chosen, covered | set(tri[i])); chosen.pop()
    rec([], frozenset())
    return [[tri[i] for i in sp] for sp in found]


def analyse(n, adj, spread):
    fib = {}
    for i, t in enumerate(spread):
        for x in t: fib[x] = i
    # quotient
    q = [set() for _ in spread]
    for x in range(n):
        for y in adj[x]:
            if fib[x] != fib[y]: q[fib[x]].add(fib[y])
    quotient_ok = check_srg(len(spread), q, 20, 1, 6)
    # cover = graph minus spread edges
    cov = [set(y for y in adj[x] if fib[y] != fib[x]) for x in range(n)]
    # distance-regularity
    b = [20, 18, 4, 1]; c = [1, 2, 18, 20]; drg = True
    for x in range(n):
        dist = {x: 0}; frontier = [x]
        while frontier:
            nxt = []
            for u in frontier:
                for w in cov[u]:
                    if w not in dist: dist[w] = dist[u] + 1; nxt.append(w)
            frontier = nxt
        if len(dist) != n or max(dist.values()) != 4: drg = False; break
        for y in range(n):
            d = dist[y]
            cc = sum(1 for w in cov[y] if dist[w] == d - 1); bb = sum(1 for w in cov[y] if dist[w] == d + 1)
            if d > 0 and cc != c[d - 1]: drg = False
            if d < 4 and bb != b[d]: drg = False
        if not drg: break
    # cyclic? orient the fibres: sigma[x] in Z3 on each fibre with a cyclic order; matchings must be rotations
    order = {i: list(t) for i, t in enumerate(spread)}          # reference cyclic order of each fibre
    pos = {x: order[fib[x]].index(x) for x in range(n)}
    flip = {0: 0}; stack = [0]; cyclic = True
    while stack:
        i = stack.pop()
        for j in q[i]:
            # matching fibre i -> fibre j
            img = [pos[next(y for y in adj[x] if fib[y] == j)] for x in order[i]]
            rot = img in ([0, 1, 2], [1, 2, 0], [2, 0, 1])               # orientation preserving for the reference orders
            want = flip[i] ^ (0 if rot else 1)
            if j not in flip: flip[j] = want; stack.append(j)
            elif flip[j] != want: cyclic = False
    return quotient_ok, drg, cyclic


def grids_through(n, adj):
    """number of induced 3x3 grids through each vertex: pairs of lines through x spanning a grid"""
    line = {}
    for x in range(n):
        for y in adj[x]:
            if x < y: z = next(iter(adj[x] & adj[y])); line[(x, y)] = z; line[(y, x)] = z
    cnt = []
    for x in range(n):
        lines = sorted({tuple(sorted((y, line[(x, y)]))) for y in adj[x]})
        c = 0
        for (a, a2), (b, b2) in itertools.combinations(lines, 2):
            def second(u, w): return next(v for v in adj[u] & adj[w] if v != x)
            cab, cab2, ca2b, ca2b2 = second(a, b), second(a, b2), second(a2, b), second(a2, b2)
            if cab2 in adj[cab] and ca2b in adj[cab] and ca2b2 in adj[cab2] and ca2b2 in adj[ca2b]: c += 1
        cnt.append(c)
    return collections.Counter(cnt)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        n, adj = load(path)
        srg = check_srg(n, adj, 22, 1, 2)
        print("%s: %d vertices; srg(243,22,1,2): %s" % (path.replace("\\", "/").split("/")[-1], n, srg), flush=True)
        if not srg: continue
        print("  number of 3x3 grids through a vertex (value: number of vertices): %s" % sorted(grids_through(n, adj).items()), flush=True)
        sps = spreads(n, adj)
        print("  regular spreads found (exhaustive): %d" % len(sps), flush=True)
        res = collections.Counter(analyse(n, adj, sp) for sp in sps)
        for (qok, drg, cyc), m in sorted(res.items()):
            print("    %d spread(s): quotient srg(81,20,1,6): %s; graph minus spread distance-regular {20,18,4,1;1,2,18,20}: %s; cyclic cover: %s" % (m, qok, drg, cyc), flush=True)
