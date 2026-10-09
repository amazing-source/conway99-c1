"""C1, lab session, 2026-10-09, mandate B. A fifth diameter-two test of the sub-lemma "every quadrangle has even
holonomy": the Gewirtz graph srg(56,10,0,2) (one class of 56 hyperovals of PG(2,4), adjacent when disjoint).
  python gewirtz_test.py        One process, seconds. Uses run() of holonomy_mu2.py."""
import itertools, sys, io, contextlib
# F_4 = {0, 1, w, w^2} coded 0, 1, 2, 3; addition is XOR, multiplication by the table
MUL = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
pts = [p for p in itertools.product(range(4), repeat=3) if any(p) and p[next(i for i in range(3) if p[i])] == 1]
assert len(pts) == 21
def det3(a, b, c):
    m = lambda x, y: MUL[x][y]
    return (m(a[0], m(b[1], c[2])) ^ m(a[0], m(b[2], c[1])) ^ m(a[1], m(b[0], c[2])) ^ m(a[1], m(b[2], c[0]))
            ^ m(a[2], m(b[0], c[1])) ^ m(a[2], m(b[1], c[0])))
col = {t: det3(pts[t[0]], pts[t[1]], pts[t[2]]) == 0 for t in itertools.combinations(range(21), 3)}
hyper = []
def ext(cur, start):
    if len(cur) == 6: hyper.append(frozenset(cur)); return
    for p in range(start, 21):
        if all(not col[(a, b, p)] for a, b in itertools.combinations(cur, 2)): ext(cur + [p], p + 1)
ext([], 0); assert len(hyper) == 168, len(hyper)
# classes: two hyperovals are equivalent when they meet in an even number of points
cls = [None] * 168; k = 0
for i in range(168):
    if cls[i] is None:
        cls[i] = k; st = [i]
        while st:
            x = st.pop()
            for j in range(168):
                if cls[j] is None and len(hyper[x] & hyper[j]) % 2 == 0: cls[j] = k; st.append(j)
        k += 1
assert k == 3 and all(cls.count(c) == 56 for c in range(3))
V = [h for h, c in zip(hyper, cls) if c == 0]
E = [(i, j) for i in range(56) for j in range(i + 1, 56) if not (V[i] & V[j])]
sys.argv = [sys.argv[0]]
with contextlib.redirect_stdout(io.StringIO()): import holonomy_mu2 as h
h.run("Gewirtz (56,10,0,2)", 56, E)

# ---- the canonical cochain in diameter two (lambda = 0, k even): PSI_vw is the permutation of ALL vertices
# v <-> w, x <-> pi(x) for x in N(v) minus w, and [x, y]_v -> [pi x, pi y]_w on the common non-neighbours,
# where [x, y]_v is the vertex other than v adjacent to x and y. Claim checked: its sign is a cochain of the class.
import collections
adj = [set() for _ in range(56)]
for a, b in E: adj[a].add(b); adj[b].add(a)
def psi_sign(v, w):
    pi = {x: next(iter((adj[x] & adj[w]) - {v})) for x in adj[v] if x != w}
    P = {v: w, w: v}
    for x, y in pi.items(): P[x] = y; P[y] = x
    for z in range(56):
        if z in P: continue
        x, y = sorted(adj[z] & adj[v]); P[z] = next(iter((adj[pi[x]] & adj[pi[y]]) - {w}))
    assert sorted(P.values()) == list(range(56))
    seen = set(); s = 0
    for a in range(56):
        if a not in seen:
            ln = 0; u = a
            while u not in seen: seen.add(u); u = P[u]; ln += 1
            s ^= (ln - 1) & 1
    return s
g = {}
for a, b in E: g[(a, b)] = psi_sign(a, b); g[(b, a)] = psi_sign(b, a)
print("sign of PSI_vw over the %d edges: %s; symmetric in (v, w): %s" % (len(E), dict(collections.Counter(g[e] for e in E)), all(g[(a, b)] == g[(b, a)] for a, b in E)))
# compare with the gauge-dependent cochain of PHI (v <-> w swapped) on open neighbourhoods: same class?
order = [sorted(adj[v]) for v in range(56)]
def phi_sign(v, w):
    d = {w: v}
    for x in adj[v]:
        if x != w: d[x] = next(iter((adj[x] & adj[w]) - {v}))
    pos = {y: i for i, y in enumerate(order[w])}; p = [pos[d[x]] for x in order[v]]; seen = [False] * len(p); s = 0
    for i in range(len(p)):
        if not seen[i]:
            j = i; ln = 0
            while not seen[j]: seen[j] = True; j = p[j]; ln += 1
            s ^= (ln - 1) & 1
    return s
diff = {e: phi_sign(*e) ^ g[e] for e in E}
pot = [None] * 56; pot[0] = 0; st = [0]
while st:
    x = st.pop()
    for y in adj[x]:
        if pot[y] is None: pot[y] = pot[x] ^ diff[tuple(sorted((x, y)))]; st.append(y)
print("cochain of PHI minus sign(PSI) is a coboundary: %s" % all((pot[a] ^ pot[b]) == diff[(a, b)] for a, b in E))
