"""Lab session, 2026-10-12. Independent audit of the graphs claimed on branch claude/v7-simultaneous (note 165):
four srg(243,22,1,2) given as edge lists (BvLS, "twin", Gamma3 with |Aut| = 864, Gamma4 with |Aut| = 3888).

Nothing here uses the campaign's code, nauty or a solver. For one edge list the script
 1. checks the parameters exactly (A^2 + A = 20 I + 2 J, integers);
 2. counts the lines (triangles), the induced 3 x 3 grids (K3 x K3) and their number through every vertex, and the
    induced prisms (K3 x K2);
 3. computes the order of the automorphism group by a stabiliser chain: at each level the orbit of the base point
    under the stabiliser of the previous base points is found by explicit automorphisms (individualisation and
    colour refinement on both sides, backtracking on the first non-trivial cell, every map found is verified as an
    automorphism); a vertex is declared outside the orbit only after the whole search tree is exhausted;
 4. lists the regular spreads (partitions into 81 lines, two lines joined by 0 or 3 edges). Such a spread is
    determined by its line through the vertex 0: if x is adjacent to the point a of a spread line {a,b,c}, the line
    of x must be {x, y_b, y_c}, y_b the second common neighbour of x and b; so at most 11 spreads, found by
    propagation; the quotient is checked to be a srg(81,20,1,6).

python audit243.py <file.edges> [noaut]         One process, below 1 GB."""
import sys, time, itertools
import numpy as np
n = 243

def load(path):
    A = np.zeros((n, n), dtype=np.int64); m = 0
    for line in open(path):
        if line.strip():
            i, j = map(int, line.split()); assert i != j and A[i, j] == 0; A[i, j] = A[j, i] = 1; m += 1
    return A, m

_RNG = np.random.default_rng(20261012)
_W = _RNG.integers(1, 2 ** 62, size=n + 1, dtype=np.uint64)   # one fixed random weight per colour number

def _rank(keys):
    """canonical renumbering: colours = ranks of the distinct rows of keys (keys: tuple of arrays, most significant first)"""
    order = np.lexsort(keys[::-1]); new = np.empty(n, dtype=np.int64); c = 0
    prev = tuple(k[order[0]] for k in keys); new[order[0]] = 0
    for i in order[1:]:
        cur = tuple(k[i] for k in keys)
        if cur != prev: c += 1; prev = cur
        new[i] = c
    return new, c + 1

def refine(A, col):
    """colour refinement. The neighbour colours of a vertex are summarised by the sum of fixed random 64-bit weights
    (a function of the multiset of neighbour colours, so two equivalent vertices always get the same value; a collision
    can only keep two cells together, never split wrongly). Colours are renumbered by the rank of (old colour, sum)."""
    Au = A.astype(np.uint64); k = int(col.max()) + 1
    while True:
        s = Au @ _W[col]
        new, k2 = _rank((col, s))
        if k2 == k: return new
        col, k = new, k2

def individualise(A, col, v):
    c2 = col * 2; c2[v] += 1                                # v gets a colour of its own, just after its old cell
    c3, _ = _rank((c2,))
    return refine(A, c3)

def find_map(A, colL, colR, stats):
    """an automorphism compatible with the two coloured copies (colour i on the left -> colour i on the right), or None"""
    stats[0] += 1
    hL = np.bincount(colL); hR = np.bincount(colR)
    if len(hL) != len(hR) or (hL != hR).any(): return None
    if len(hL) == n:
        perm = np.empty(n, dtype=np.int64); perm[np.argsort(colL)] = np.argsort(colR)       # left vertex of colour i -> right vertex of colour i
        return perm if (A[np.ix_(perm, perm)] == A).all() else None
    c = int(np.nonzero(hL > 1)[0][0]); v = int(np.nonzero(colL == c)[0][0]); cL = individualise(A, colL, v)
    for w in np.nonzero(colR == c)[0]:
        g = find_map(A, cL, individualise(A, colR, int(w)), stats)
        if g is not None: return g
    return None

def aut_order(A):
    col = refine(A, np.zeros(n, dtype=np.int64)); order = 1; base = []; orbits = []; gens = []; stats = [0]
    while True:
        h = np.bincount(col)
        if len(h) == n: break
        c = int(np.nonzero(h > 1)[0][0]); cell = [int(x) for x in np.nonzero(col == c)[0]]; b = cell[0]
        colb = individualise(A, col, b)
        # orbit of b under the stabiliser of the previous base points
        parent = {x: x for x in cell}
        def find(x):
            while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def close():
            for g in gens:
                if all(g[y] == y for y in base):            # g lies in the current stabiliser
                    for x in cell:
                        rx, ry = find(x), find(int(g[x]))
                        if rx != ry: parent[rx] = ry
        close()
        decided_out = set()
        for w in cell[1:]:
            if find(w) == find(b) or find(w) in decided_out: continue
            g = find_map(A, colb, individualise(A, col, w), stats)
            if g is None: decided_out.add(find(w))
            else:
                assert g[b] == w and all(g[y] == y for y in base)
                gens.append(g); close()
        orb = [x for x in cell if find(x) == find(b)]
        order *= len(orb); base.append(b); orbits.append(len(orb)); col = colb
    return order, base, orbits, gens, stats[0]

def vertex_orbits(gens):
    parent = list(range(n))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for g in gens:
        for x in range(n):
            rx, ry = find(x), find(int(g[x]))
            if rx != ry: parent[rx] = ry
    sizes = {}
    for x in range(n): sizes[find(x)] = sizes.get(find(x), 0) + 1
    return sorted(sizes.values())

def main():
    path = sys.argv[1]; t0 = time.time(); A, m = load(path)
    print("file %s: %d edges" % (path, m), flush=True)
    ok = (A @ A + A == 20 * np.eye(n, dtype=np.int64) + 2).all() and (A.sum(0) == 22).all()
    print("srg(243,22,1,2), A^2 + A = 20 I + 2 J:", "TRUE" if ok else "FALSE")
    if not ok: return
    adj = [set(int(y) for y in np.nonzero(A[x])[0]) for x in range(n)]
    lines = sorted({tuple(sorted((x, y, next(iter(adj[x] & adj[y]))))) for x in range(n) for y in adj[x]})
    line_of = {}
    for l in lines:
        for a, b in itertools.combinations(l, 2): line_of[(a, b)] = line_of[(b, a)] = l
    print("lines (triangles): %d" % len(lines))
    # grids: two lines through x, {x,a,b} and {x,c,d}, with the four other points e_ac = second common neighbour of a and c, ...
    per_vertex = [0] * n; grids = set()
    for x in range(n):
        Lx = [l for l in lines if x in l]
        for l1, l2 in itertools.combinations(Lx, 2):
            a, b = [p for p in l1 if p != x]; c, d = [p for p in l2 if p != x]
            e = []
            for p in (a, b):
                for q in (c, d):
                    cn = (adj[p] & adj[q]) - {x}
                    e.append(next(iter(cn)) if len(cn) == 1 else None)
            if None in e: continue
            S = [x, a, b, c, d] + e
            if len(set(S)) == 9 and all(len(adj[s] & set(S)) == 4 for s in S):
                per_vertex[x] += 1; grids.add(tuple(sorted(S)))
    dist = {}
    for v in per_vertex: dist[v] = dist.get(v, 0) + 1
    assert sum(per_vertex) == 9 * len(grids)
    print("induced 3x3 grids: %d; through a vertex: %s" % (len(grids), dict(sorted(dist.items()))))
    # prisms: two disjoint lines joined by a perfect matching and no other edge
    prisms = 0
    for i, l1 in enumerate(lines):
        nb = {}
        for p in l1:
            for q in adj[p]:
                if q not in l1:
                    l2 = [l for l in (line_of[(q, r)] for r in adj[q] if r not in l1 and (q, r) in line_of) if not set(l) & set(l1)]
                    for l in set(l2): nb.setdefault(l, set()).add((p, q))
        for l2, pairs in nb.items():
            if l2 > l1:
                e = sum(1 for p in l1 for q in l2 if q in adj[p])
                if e == 3 and len({p for p in l1 for q in l2 if q in adj[p]}) == 3 and len({q for p in l1 for q in l2 if q in adj[p]}) == 3: prisms += 1
    print("induced prisms (two disjoint lines joined by a perfect matching): %d" % prisms)
    # regular spreads through propagation
    spreads = []
    for l0 in [l for l in lines if 0 in l]:
        lineof = {}; queue = [l0]; good = True
        for p in l0: lineof[p] = l0
        while queue and good:
            l = queue.pop()
            for a in l:
                others = [p for p in l if p != a]
                for x in adj[a]:
                    if x in l: continue
                    ys = []
                    for b in others:
                        cn = (adj[x] & adj[b]) - {a}
                        if len(cn) != 1: good = False; break
                        ys.append(next(iter(cn)))
                    if not good: break
                    cand = tuple(sorted([x] + ys))
                    if len(set(cand)) != 3 or ys[1] not in adj[ys[0]]: good = False; break
                    for p in cand:
                        if p in lineof and lineof[p] != cand: good = False
                    if not good: break
                    if x not in lineof:
                        for p in cand: lineof[p] = cand
                        queue.append(cand)
                if not good: break
        if good and len(lineof) == n:
            S = sorted(set(lineof.values())); idx = {l: i for i, l in enumerate(S)}
            if len(S) != 81: continue
            Q = np.zeros((81, 81), dtype=np.int64); reg = True
            for i, l1 in enumerate(S):
                for l2 in S[i + 1:]:
                    e = int(A[np.ix_(l1, l2)].sum())
                    if e not in (0, 3): reg = False
                    if e == 3: Q[i, idx[l2]] = Q[idx[l2], i] = 1
            # srg(81,20,1,6): Q^2 = 20 I + 1 Q + 6 (J - I - Q)  <=>  Q^2 + 5 Q = 14 I + 6 J
            bh = reg and (Q @ Q + 5 * Q == 14 * np.eye(81, dtype=np.int64) + 6).all()
            spreads.append((l0, reg, bh))
    print("regular spreads: %d (line through the vertex 0, regular, quotient srg(81,20,1,6)): %s" % (len(spreads), [(l, bool(r), bool(b)) for l, r, b in spreads]), flush=True)
    if len(sys.argv) > 2: print("[%.0f s]" % (time.time() - t0)); return
    order, base, orbits, gens, calls = aut_order(A)
    f = {}; o = order
    for p in (2, 3, 5, 7, 11):
        while o % p == 0: f[p] = f.get(p, 0) + 1; o //= p
    print("automorphism group: order %d = %s%s; base %s, orbit lengths along the chain %s; %d generators found, %d search calls" % (
        order, " . ".join("%d^%d" % (p, e) for p, e in f.items()), "" if o == 1 else " . %d" % o, base, orbits, len(gens), calls))
    print("vertex orbits of the group generated by the automorphisms found: %s" % vertex_orbits(gens))
    print("[%.0f s]" % (time.time() - t0))

if __name__ == "__main__":
    main()
