"""C1, lab session, 2026-10-09, mandate B. More graphs with lambda = 1 and mu in {0, 2}: the tri-incidence family of the
earlier sessions (code/triincidence.py of the Codex repository): vertices (i, a), i in Z_3, a in Z_N, N = q^2 + q + 1,
(i, a) ~ (i+1, a + d) for d in D_i, with D_0 = S planar difference set, D_1 = u S, D_2 = v S + c.
All (u, v, c) giving the axioms are listed for q = 3 and a sample for q = 5, 7; on each graph the test of
two_layer_test.py (is the sign cochain f equal to c_e + constant up to a coboundary?) and the parity of the faces of
every line are run.     python triinc_test.py      One process, about a minute."""
import itertools, sys, io, contextlib, collections, math
import numpy as np


def singer(q):
    N = q * q + q + 1
    for D in itertools.combinations(range(1, N), q):
        D = (0,) + D
        if sorted((a - b) % N for a in D for b in D if a != b) == list(range(1, N)): return list(D)


def build(N, Ds):
    A = np.zeros((3 * N, 3 * N), dtype=np.int64)
    for i in range(3):
        j = (i + 1) % 3
        for a in range(N):
            for d in Ds[i]: A[i * N + a, j * N + (a + d) % N] = A[j * N + (a + d) % N, i * N + a] = 1
    return A


def ok(A):
    A2 = A @ A; off = ~np.eye(len(A), dtype=bool)
    return set(A2[(A == 1) & off].tolist()) == {1} and set(A2[(A == 0) & off].tolist()) <= {0, 2}


def study(name, A):
    n = len(A); adj = [set(np.nonzero(A[i])[0].tolist()) for i in range(n)]; E = [(i, j) for i in range(n) for j in adj[i] if i < j]
    k = len(adj[0]); third = {}
    for a, b in E:
        t = next(iter(adj[a] & adj[b])); third[(a, b)] = third[(b, a)] = t
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
            if x != b and x != t: d[x] = pi(a, b, x)
        f[(a, b)] = f[(b, a)] = sgn(d, order[a], order[b])
        X = [x for x in adj[a] if x != b and x != t]; seen = set(); cyc = 0
        for x in X:
            if x in seen: continue
            cyc += 1; u = x
            while u not in seen:
                seen.add(u); u1 = third[(a, u)]; seen.add(u1); y = pi(a, b, u1); y1 = third[(b, y)]; u = pi(b, a, y1)
        c[(a, b)] = c[(b, a)] = cyc
    res = {}
    for label, g in (("f", f), ("f+c", {e: (f[e] + c[e]) % 2 for e in f})):
        for const in (0, 1):
            pot = [None] * n; pot[0] = 0; st = [0]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if pot[y] is None: pot[y] = pot[x] ^ g[(x, y)] ^ const; st.append(y)
            if all((pot[a] ^ pot[b]) == (g[(a, b)] ^ const) for a, b in E): res[label] = "coboundary + %d" % const
        res.setdefault(label, "OTHER")
    lines = sorted({tuple(sorted((a, b, third[(a, b)]))) for a, b in E}); faces = collections.Counter()
    for (u, v, w) in lines:
        dom = [x for x in adj[u] if x not in (v, w)]; rho = {x: pi(w, u, pi(v, w, pi(u, v, x))) for x in dom}; seen = set(); cy = 0
        for x in dom:
            if x not in seen:
                cy += 1; z = x
                while z not in seen: seen.add(z); z = rho[z]
        faces[(cy + c[(u, v)] + c[(v, w)] + c[(u, w)]) % 2] += 1
    print("%-26s n %3d k %2d | c_e values %s | class of f: %-14s | f + c: %-14s | lines by parity of the number of faces: %s"
          % (name, n, k, dict(sorted(collections.Counter(c[e] for e in E).items())), res["f"], res["f+c"], dict(faces)))
    return res["f+c"] != "OTHER"


allok = True
for q, limit in ((3, None), (5, 12), (7, 3)):
    N = q * q + q + 1; S = singer(q); units = [u for u in range(1, N) if math.gcd(u, N) == 1]; found = {}
    for u in units:
        D1 = sorted((u * s) % N for s in S)
        for v in units:
            for cc in range(N):
                D2 = sorted((v * s + cc) % N for s in S)
                A = build(N, [S, D1, D2])
                if ok(A):
                    key = tuple(np.round(np.linalg.eigvalsh(A.astype(float)), 4).tolist()) + tuple(sorted(collections.Counter((A @ A @ A).diagonal().tolist()).items()))
                    found.setdefault(key, (u, v, cc, A))
            if limit and len(found) >= limit: break
        if limit and len(found) >= limit: break
    print("q = %d, N = %d: graphs satisfying the axioms, distinct by spectrum: %d" % (q, N, len(found)))
    for (u, v, cc, A) in list(found.values())[:limit or 99]:
        allok &= study("q=%d u=%d v=%d c=%d" % (q, u, v, cc), A)
print("formula 'f + c is a coboundary plus a constant' holds on every graph tested:", allok)
