"""Small exact toolkit for the asymmetry campaign (14/10/2026): reading Spence's lists, checking the srg
parameters, exact automorphism groups by individualisation-refinement with backtracking (no external library),
orbits, and generators. Pure Python, meant for graphs of at most a few hundred vertices.

Conventions: a graph is a list of sets nb[v] (neighbours of v), vertices 0..n-1.
"""
import itertools


def read_spence(path):
    """Spence's format: a header line 'dim=..., degree=..., lambda=..., mu=...' then 0/1 rows separated by blank lines."""
    graphs, rows = [], []
    header = None
    with open(path) as f:
        for line in f:
            s = line.strip()
            if s.startswith("dim"):
                header = s
                continue
            if not s:
                if rows:
                    graphs.append(rows)
                    rows = []
                continue
            if set(s) <= {"0", "1"}:
                rows.append(s)
    if rows:
        graphs.append(rows)
    out = []
    for rows in graphs:
        n = len(rows)
        assert all(len(r) == n for r in rows), "ragged matrix"
        nb = [set(j for j in range(n) if rows[i][j] == "1") for i in range(n)]
        assert all((j in nb[i]) == (i in nb[j]) for i in range(n) for j in range(n)), "not symmetric"
        assert all(i not in nb[i] for i in range(n)), "loop"
        out.append(nb)
    return header, out


def srg_params(nb):
    """Return (n, k, lambda, mu) if the graph is strongly regular, else None."""
    n = len(nb)
    degs = {len(s) for s in nb}
    if len(degs) != 1:
        return None
    k = degs.pop()
    lam, mu = set(), set()
    for i in range(n):
        for j in range(i + 1, n):
            c = len(nb[i] & nb[j])
            (lam if j in nb[i] else mu).add(c)
    if len(lam) > 1 or len(mu) > 1:
        return None
    return (n, k, lam.pop() if lam else None, mu.pop() if mu else None)


def refine(nb, colour):
    """Equitable refinement of a vertex colouring (list of ints). Returns a canonical-in-the-process list of ints."""
    n = len(nb)
    colour = list(colour)
    while True:
        sig = [(colour[v], tuple(sorted(colour[w] for w in nb[v]))) for v in range(n)]
        keys = sorted(set(sig))
        index = {k: i for i, k in enumerate(keys)}
        new = [index[sig[v]] for v in range(n)]
        if len(keys) == len(set(colour)):
            return new
        colour = new


def _search_iso(nb, cg, nb2, cg2, n):
    """Find all isomorphisms nb -> nb2 compatible with the equitable colourings cg, cg2 (generator-free search:
    used only for small groups). Yields mappings as lists."""
    def rec(c1, c2):
        if len(set(c1)) == n:
            pos = {c: v for v, c in enumerate(c2)}
            phi = [pos[c1[v]] for v in range(n)]
            if all(set(phi[w] for w in nb[v]) == nb2[phi[v]] for v in range(n)):
                yield phi
            return
        # choose the first non-singleton cell (smallest colour with >= 2 members)
        counts = {}
        for c in c1:
            counts[c] = counts.get(c, 0) + 1
        cell = min(c for c, m in counts.items() if m > 1)
        v = next(u for u in range(n) if c1[u] == cell)
        big = max(c1) + 1
        for w in [u for u in range(n) if c2[u] == cell]:
            d1 = list(c1)
            d1[v] = big
            d2 = list(c2)
            d2[w] = big
            r1, r2 = refine(nb, d1), refine(nb2, d2)
            if sorted(r1) != sorted(r2):
                continue
            yield from rec(r1, r2)
    yield from rec(cg, cg2)


def automorphism_group(nb, limit=None):
    """All automorphisms by individualisation-refinement (exact). Returns the list of permutations (lists).
    For large groups use group_order() instead."""
    n = len(nb)
    c0 = refine(nb, [0] * n)
    out = []
    for phi in _search_iso(nb, c0, nb, c0, n):
        out.append(phi)
        if limit and len(out) >= limit:
            break
    return out


def group_order(nb):
    """|Aut| by the orbit-stabiliser chain: individualise vertices one at a time; at each level count the orbit of
    the chosen vertex inside the current pointwise stabiliser by testing, for every candidate w with the same
    refined colour, whether an automorphism of the stabiliser maps v to w (search for one isomorphism only).
    Exact. Returns (order, list of orbit lengths along the chain, base)."""
    n = len(nb)
    colour = refine(nb, [0] * n)
    order, chain, base = 1, [], []
    while len(set(colour)) < n:
        counts = {}
        for c in colour:
            counts[c] = counts.get(c, 0) + 1
        cell = min(c for c, m in counts.items() if m > 1)
        cands = [u for u in range(n) if colour[u] == cell]
        v = cands[0]
        big = max(colour) + 1
        dv = list(colour)
        dv[v] = big
        rv = refine(nb, dv)
        orbit = 1
        for w in cands[1:]:
            dw = list(colour)
            dw[w] = big
            rw = refine(nb, dw)
            if sorted(rw) != sorted(rv):
                continue
            if next(_search_iso(nb, rv, nb, rw, n), None) is not None:
                orbit += 1
        order *= orbit
        chain.append(orbit)
        base.append(v)
        colour = rv
    return order, chain, base


def orbits(nb, gens):
    n = len(nb)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for g in gens:
        for v in range(n):
            a, b = find(v), find(g[v])
            if a != b:
                parent[a] = b
    groups = {}
    for v in range(n):
        groups.setdefault(find(v), []).append(v)
    return sorted(groups.values(), key=lambda s: (-len(s), s))


def vertex_orbits(nb):
    """Vertex orbits of Aut, exact: v ~ w iff some automorphism maps v to w (tested directly)."""
    n = len(nb)
    c0 = refine(nb, [0] * n)
    rep = list(range(n))
    done = [False] * n
    out = []
    for v in range(n):
        if done[v]:
            continue
        big = max(c0) + 1
        dv = list(c0)
        dv[v] = big
        rv = refine(nb, dv)
        orb = [v]
        done[v] = True
        for w in range(v + 1, n):
            if done[w] or c0[w] != c0[v]:
                continue
            dw = list(c0)
            dw[w] = big
            rw = refine(nb, dw)
            if sorted(rw) != sorted(rv):
                continue
            if next(_search_iso(nb, rv, nb, rw, n), None) is not None:
                orb.append(w)
                done[w] = True
        out.append(orb)
    return out


def canonical_form(nb):
    """A canonical certificate (exact, by exhaustive individualisation-refinement over the first non-trivial cell;
    fine for n <= ~40 with small groups, slow otherwise)."""
    n = len(nb)
    best = [None]

    def rec(colour):
        if len(set(colour)) == n:
            order = sorted(range(n), key=lambda v: colour[v])
            pos = {v: i for i, v in enumerate(order)}
            code = tuple(sorted((min(pos[a], pos[b]), max(pos[a], pos[b])) for a in range(n) for b in nb[a] if a < b))
            if best[0] is None or code < best[0]:
                best[0] = code
            return
        counts = {}
        for c in colour:
            counts[c] = counts.get(c, 0) + 1
        cell = min(c for c, m in counts.items() if m > 1)
        big = max(colour) + 1
        for w in [u for u in range(n) if colour[u] == cell]:
            d = list(colour)
            d[w] = big
            rec(refine(nb, d))
    rec(refine(nb, [0] * n))
    return best[0]
