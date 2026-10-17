"""Lab session, 2026-10-12. Small isomorphism / automorphism tools (own code, no graph library), for graphs on a few
hundred vertices: 2-dimensional Weisfeiler-Leman colours of the pairs (computed once) + individualisation + colour
refinement + backtracking, all vectorised with numpy.

Hashing: the colour of a multiset is a sum of random integers attached to its elements (exact integer arithmetic).
Equal multisets always give equal sums, so a difference detected by a refinement is a real one; a collision can only
merge classes (less pruning). Every bijection returned is checked edge by edge.

wl2(As)                   joint stable colouring of the ordered pairs of several graphs on the same number of vertices
find_iso(A1, A2, pairs)   a bijection f (list) with f(a) = b for (a, b) in pairs and f(graph 1) = graph 2, or None
aut_group(A)              (order of Aut, generators, base, basic orbit sizes)   [orbit-stabiliser along a base]
python aut_tools.py <edge file> [<edge file 2>]     order of Aut and its vertex orbits; with two files: isomorphism test"""
import sys
import numpy as np
RNG = np.random.default_rng(20261012)
P = 1048573                                                        # prime below 2^20: products below 2^40, sums of 243 below 2^48


def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = 1 + max(max(e) for e in E); A = np.zeros((n, n), dtype=np.int64)
    for a, b in E: A[a, b] = A[b, a] = 1
    return A


def geom_init(A):
    """initial colours of the pairs for a graph with lambda = 1, mu = 2 (2-dimensional WL alone cannot split a strongly
    regular graph): adjacency, diagonal, number of 3x3 grids containing the pair, and for an adjacent pair the number
    of lines parallel to its line (lines joined to it by a perfect matching)."""
    n = len(A); adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
    third = {}
    for x in range(n):
        for y in adj[x]: third[(x, y)] = next(iter(adj[x] & adj[y]))
    G = np.zeros((n, n), dtype=np.int64); F = np.zeros((n, n), dtype=np.int64); grids = set()
    for x in range(n):
        lines = sorted({tuple(sorted((y, third[(x, y)]))) for y in adj[x]})
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                (a, a2), (b, b2) = lines[i], lines[j]
                sec = lambda u, w: next(v for v in adj[u] & adj[w] if v != x)
                c = [sec(a, b), sec(a, b2), sec(a2, b), sec(a2, b2)]
                if c[1] in adj[c[0]] and c[2] in adj[c[0]] and c[3] in adj[c[1]] and c[3] in adj[c[2]]:
                    grids.add(frozenset([x, a, a2, b, b2] + c))
    for g in grids:
        g = sorted(g)
        for a in g:
            for b in g:
                if a != b: G[a, b] += 1
    for x in range(n):
        for y in adj[x]:
            if x < y:
                z = third[(x, y)]
                if x < z and y < z:
                    L = (x, y, z); cnt = 0
                    for w in adj[x]:
                        if w in L: continue
                        w1 = [t for t in adj[w] & adj[y] if t != x][0]; w2 = [t for t in adj[w1] & adj[z] if t != y][0]
                        if w2 in adj[w]: cnt += 1
                    for a in L:
                        for b in L:
                            if a != b: F[a, b] = cnt
    return A + 2 * np.eye(n, dtype=np.int64) + 4 * G + 1024 * F


def wl2(As, inits=None):
    n = len(As[0]); Cs = [A + 2 * np.eye(n, dtype=np.int64) for A in As] if inits is None else [c.copy() for c in inits]; ncol = 0
    while True:
        k = int(max(C.max() for C in Cs)) + 1
        t = [RNG.integers(1, P, size=k) for _ in range(4)]
        rows = [np.stack([C, (t[0][C] @ t[1][C]) % P, (t[2][C] @ t[3][C]) % P], axis=-1).reshape(-1, 3) for C in Cs]
        _, inv = np.unique(np.concatenate(rows), axis=0, return_inverse=True); inv = inv.reshape(-1)
        Cs = [inv[i * n * n:(i + 1) * n * n].reshape(n, n) for i in range(len(As))]
        k2 = int(inv.max()) + 1
        if k2 == ncol: return Cs
        ncol = k2


def joint(c1, e1, c2, e2):
    """joint renumbering of the pairs (c, e) on the two graphs"""
    n = len(c1)
    _, inv = np.unique(np.concatenate([np.stack([c1, e1], 1), np.stack([c2, e2], 1)]), axis=0, return_inverse=True); inv = inv.reshape(-1)
    return inv[:n], inv[n:]


def refine2(A1, col1, A2, col2):
    n = len(A1); ncol = len(np.unique(col1))
    while True:
        r = RNG.integers(1, 1 << 40, size=int(max(col1.max(), col2.max())) + 1)
        n1, n2 = joint(col1, A1 @ r[col1], col2, A2 @ r[col2])
        if not np.array_equal(np.sort(n1), np.sort(n2)): return None
        k = len(np.unique(n1))
        if k == ncol: return n1, n2
        ncol = k; col1, col2 = n1, n2


def find_iso(A1, A2, pairs=(), Cs=None):
    n = len(A1)
    if len(A2) != n: return None
    C1, C2 = Cs if Cs is not None else wl2([A1, A2], [geom_init(A1), geom_init(A2)])
    col1 = np.diag(C1).copy(); col2 = np.diag(C2).copy()
    if not np.array_equal(np.sort(col1), np.sort(col2)): return None
    for (a, b) in pairs:
        if col1[a] != col2[b]: return None
        col1, col2 = joint(col1, C1[a], col2, C2[b])
    def rec(col1, col2):
        r = refine2(A1, col1, A2, col2)
        if r is None: return None
        col1, col2 = r
        cnt = np.bincount(col1)
        if len(cnt) == n:
            inv = np.empty(n, dtype=np.int64); inv[col2] = np.arange(n); f = inv[col1]
            return f.tolist() if np.array_equal(A1, A2[np.ix_(f, f)]) else None
        big = np.nonzero(cnt > 1)[0]; c = big[np.argmin(cnt[big])]
        x = int(np.nonzero(col1 == c)[0][0])
        for y in np.nonzero(col2 == c)[0]:
            a1, a2 = joint(col1, C1[x], col2, C2[int(y)])
            f = rec(a1, a2)
            if f is not None: return f
        return None
    return rec(col1, col2)


def aut_group(A):
    n = len(A); base = []; order = 1; sizes = []; gens = []
    C = wl2([A], [geom_init(A)])[0]; Cs = (C, C)
    while True:
        col = np.diag(C).copy()
        for b in base: col = joint(col, C[b], col, C[b])[0]
        col = refine2(A, col, A, col.copy())[0]
        cnt = np.bincount(col)
        if len(cnt) == n: break
        big = np.nonzero(cnt > 1)[0]; c = big[np.argmax(cnt[big])]
        cell = [int(v) for v in np.nonzero(col == c)[0]]; x = cell[0]
        level = []; orb = {x}
        def close():
            changed = True
            while changed:
                changed = False
                for g in level:
                    for v in list(orb):
                        if g[v] not in orb: orb.add(g[v]); changed = True
        for y in cell:
            if y in orb: continue
            f = find_iso(A, A, [(b, b) for b in base] + [(x, y)], Cs)
            if f is not None: level.append(f); gens.append(f); orb.add(y); close()
        order *= len(orb); sizes.append(len(orb)); base.append(x)
    return order, gens, base, sizes


def vertex_orbits(n, gens):
    rep = list(range(n))
    def find(v):
        while rep[v] != v: rep[v] = rep[rep[v]]; v = rep[v]
        return v
    for g in gens:
        for v in range(n):
            a, b = find(v), find(g[v])
            if a != b: rep[a] = b
    orbs = {}
    for v in range(n): orbs.setdefault(find(v), []).append(v)
    return sorted(orbs.values(), key=lambda o: (len(o), o))


if __name__ == "__main__":
    import time
    A1 = load(sys.argv[1])
    if len(sys.argv) > 2:
        A2 = load(sys.argv[2]); t0 = time.time(); f = find_iso(A1, A2)
        print("isomorphic: %s (%.1f s)" % (f is not None, time.time() - t0))
    else:
        t0 = time.time(); o, gens, base, sizes = aut_group(A1)
        orbs = vertex_orbits(len(A1), gens)
        print("|Aut| = %d (basic orbit sizes %s, base %s, %d generators; %.1f s); vertex orbits: %s" % (o, sizes, base, len(gens), time.time() - t0, [len(x) for x in orbs]), flush=True)
