"""C1, lab session, 2026-10-09, mandate B. The orientation class of the neighbourhood bundle of a graph with lambda = 1,
mu = 2, and its values on lines and quadrangles. Falsification on the available graphs (3x3 grid, the two srg(243,22,1,2)).

For adjacent v, w with third point t, PHI_vw : N[v] -> N[w] fixes v, w, t and sends x in N(v) minus {w, t} to the unique
common neighbour of x and w other than v. PHI_wv is the inverse. The sign of the holonomy of a closed walk on N[v] is a
homomorphism from the cycle space to Z/2 (choose an order on every N[v]: the sign of each PHI_vw is then a 1-cochain f).
Every edge lies in k - 2 quadrangles (even), so the sum over ALL quadrangles of the holonomy bit is 0 mod 2.

  python holonomy_class.py <edge list file | grid>
One process, a few seconds, below 300 MB."""
import sys, itertools, collections
src = sys.argv[1]
if src == "grid":
    n = 9; E = [(3 * i + j, 3 * i2 + j2) for i in range(3) for j in range(3) for i2 in range(3) for j2 in range(3)
                if (i == i2) != (j == j2) and 3 * i + j < 3 * i2 + j2]
elif src.endswith(".json"):                                                # adjacency matrix (the small twisted geometries)
    import json
    _A = json.load(open(src)); n = len(_A); E = [(i, j) for i in range(n) for j in range(i + 1, n) if _A[i][j]]
else:
    E = [tuple(map(int, l.split())) for l in open(src) if l.strip()]; n = 1 + max(max(e) for e in E)
adj = [set() for _ in range(n)]
for a, b in E: adj[a].add(b); adj[b].add(a)
k = len(adj[0]); assert all(len(s) == k for s in adj)
for a, b in E: assert len(adj[a] & adj[b]) == 1
third = {}
for a, b in E:
    t = next(iter(adj[a] & adj[b])); third[(a, b)] = third[(b, a)] = t
nonedges = [(a, b) for a in range(n) for b in range(a + 1, n) if b not in adj[a] and adj[a] & adj[b]]   # pairs at distance 2
assert all(len(adj[a] & adj[b]) == 2 for a, b in nonedges)
per_edge = {}
for a, b in nonedges:
    for c in adj[a] & adj[b]:
        for e in ((a, c), (b, c)): per_edge[tuple(sorted(e))] = per_edge.get(tuple(sorted(e)), 0) + 1
assert all(per_edge[tuple(sorted(e))] == 2 * (k - 2) for e in E)          # counted once per diagonal: k - 2 quadrangles per edge
lines = sorted({tuple(sorted((a, b, third[(a, b)]))) for a, b in E})
quads = sorted({(min(a, b), max(a, b)) + tuple(sorted(adj[a] & adj[b])) for a, b in nonedges
                if (a, b) < tuple(sorted(adj[a] & adj[b]))})
print("%s: n %d, k %d, edges %d, lines %d, quadrangles %d (each edge in %d quadrangles)" % (src, n, k, len(E), len(lines), len(quads), k - 2))


def pi(v, w, x):
    """x in N(v) minus the line vw -> its unique neighbour in N(w) other than v"""
    return next(iter((adj[x] & adj[w]) - {v}))


def phi(v, w):
    """PHI'_vw as a dictionary on N[v]"""
    t = third[(v, w)]; d = {v: v, w: w, t: t}
    for x in adj[v]:
        if x != w and x != t: d[x] = pi(v, w, x)
    return d


def sign_of_bijection(d, order_from, order_to):
    """sign of the bijection d between two ordered sets"""
    pos = {y: i for i, y in enumerate(order_to)}; p = [pos[d[x]] for x in order_from]
    seen = [False] * len(p); s = 0
    for i in range(len(p)):
        if not seen[i]:
            j = i; ln = 0
            while not seen[j]: seen[j] = True; j = p[j]; ln += 1
            s ^= (ln - 1) & 1
    return s


def cycles(perm, dom):
    seen = set(); out = []
    for s in dom:
        if s in seen: continue
        ln = 0; u = s
        while u not in seen: seen.add(u); u = perm[u]; ln += 1
        out.append(ln)
    return tuple(sorted(out))


order = [[v] + sorted(adj[v]) for v in range(n)]                      # an arbitrary order on every closed neighbourhood
f = {}                                                                # the 1-cochain
for a, b in E:
    s = sign_of_bijection(phi(a, b), order[a], order[b]); f[(a, b)] = f[(b, a)] = s
    assert s == sign_of_bijection(phi(b, a), order[b], order[a])

# ---- lines: the cross permutation rho_T on N(u) minus T, its cycles, the cochain sum
line_stat = collections.Counter(); bad = 0; omega_line = {}
for T in lines:
    u, v, w = T; dom = [x for x in adj[u] if x not in T]
    rho = {x: pi(w, u, pi(v, w, pi(u, v, x))) for x in dom}; ct = cycles(rho, dom)
    bit = (f[(u, v)] + f[(v, w)] + f[(w, u)]) % 2; omega_line[T] = bit
    if bit != (len(dom) - len(ct)) % 2: bad += 1
    line_stat[(ct, bit)] += 1
print("lines: cochain sum equal to the parity of the cross permutation for all lines: %s" % (bad == 0))
for (ct, bit), c in sorted(line_stat.items()): print("   cross cycles %s  omega %d : %d lines" % (ct, bit, c))

# ---- quadrangles: band permutation on N(v) minus {a, b}, prism type, cochain sum
quad_stat = collections.Counter(); bad = 0; odd = 0; omega_quad = {}
for v, w, a, b in quads:
    ea, eb, pa, pb = third[(v, a)], third[(v, b)], third[(a, w)], third[(w, b)]     # ears on va, vb, aw, wb
    prisms = int(pb in adj[ea]) + int(pa in adj[eb])                                  # extensions that are prisms
    d1, d2, d3, d4 = phi(v, a), phi(a, w), phi(w, b), phi(b, v)
    hol = {x: d4[d3[d2[d1[x]]]] for x in [v] + list(adj[v])}
    dom = [x for x in adj[v] if x != a and x != b]
    assert set(hol[x] for x in dom) == set(dom)
    ct = cycles(hol, dom); bit = (f[(v, a)] + f[(a, w)] + f[(w, b)] + f[(b, v)]) % 2; omega_quad[(v, w, a, b)] = bit
    full = cycles(hol, [v] + list(adj[v]))
    if bit != (k + 1 - len(full)) % 2: bad += 1
    odd += bit; quad_stat[(prisms, bit, ct)] += 1
print("quadrangles: cochain sum equal to the parity of the holonomy on N[v] for all quadrangles: %s" % (bad == 0))
print("quadrangles with odd holonomy: %d of %d   (law: this number is even)  -> %s" % (odd, len(quads), "OK" if odd % 2 == 0 else "VIOLATED"))
by = collections.Counter()
for (prisms, bit, ct), c in quad_stat.items(): by[(prisms, bit)] += c
for key, c in sorted(by.items()): print("   prism extensions %d, omega %d : %d quadrangles" % (key[0], key[1], c))
print("   distinct (prism extensions, omega, band cycle type): %d; the ten most frequent:" % len(quad_stat))
for (prisms, bit, ct), c in sorted(quad_stat.items(), key=lambda t: -t[1])[:10]: print("      %d  %d  %s : %d" % (prisms, bit, ct, c))

# ---- is the class zero in H^1(graph; F_2)?  potentials along a spanning tree, then every other edge
pot = [None] * n; pot[0] = 0; stack = [0]; tree = set()
while stack:
    x = stack.pop()
    for y in adj[x]:
        if pot[y] is None: pot[y] = pot[x] ^ f[(x, y)]; stack.append(y); tree.add((min(x, y), max(x, y)))
viol = sum(1 for a, b in E if (pot[a] ^ pot[b]) != f[(a, b)])
print("class omega in H^1(graph; F_2): %s (edges off the tree with a non-zero value after gauge: %d of %d)"
      % ("ZERO" if viol == 0 else "NON-ZERO", viol, len(E) - len(tree)))
print("lines with omega = 1: %d of %d; quadrangles with omega = 1: %d of %d" % (sum(omega_line.values()), len(lines), odd, len(quads)))
