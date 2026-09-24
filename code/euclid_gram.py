"""Gram matrices of tensor sums over small configurations, as linear functions of induced-subgraph counts.

Euclidean representation of an SRG in an eigenspace: vectors p_v with <p_u, p_v> = g0 (u = v), g1 (u ~ v),
g2 (u !~ v).  For a base graph B (<= D vertices, fixed labelling) and a multiset of its vertices of size D
covering all of B ("recipe" r = (B, slots)), set
    w_r = sum over labelled induced embeddings e : B -> Gamma of Sym( p_{e(slot_1)} (x) ... (x) p_{e(slot_D)} ).
Then <w_r, w_r'> = sum_U z_U * c(r, r', U), where U runs over the isomorphism types of the union
e(B) u e'(B') (at most 2D vertices), z_U = number of induced copies of U, and
    c(r, r', U) = sum over pairs (e, e') of embeddings into U covering V(U) of perm(M)/D!,
    M_jk = kernel(e(slot_j), e'(slot'_k)).
The matrix [<w_r, w_r'>] is positive semidefinite.  With D = 3, bases <= 3 points, this is the degree-3
argument of L16 (notes/70); D = 4 needs the counts up to order 8.
"""
import itertools
import math
from collections import defaultdict
import numpy as np
import networkx as nx


def small_canon(edges, m):
    """Canonical form of a graph on m <= 4 vertices: lexicographically smallest edge set over permutations."""
    best = None
    for p in itertools.permutations(range(m)):
        e = tuple(sorted(tuple(sorted((p[u], p[v]))) for u, v in edges))
        if best is None or e < best:
            best = e
    return best


def make_bases(T, D):
    bases = []
    for m in range(1, D + 1):
        for i, G in enumerate(T.reps[m]):
            bases.append({'m': m, 'i': i, 'G': G, 'canon': small_canon(list(G.edges()), m),
                          'aut': [p for p in itertools.permutations(range(m))
                                  if all(G.has_edge(p[u], p[v]) for u, v in G.edges())]})
    return bases


def make_recipes(bases, D):
    """Sym^D recipes: multiplicity vectors (all >= 1, sum D) on the base's vertices, up to Aut(B)."""
    rec = []
    for bi, B in enumerate(bases):
        m = B['m']
        seen = set()
        for mult in itertools.product(range(1, D + 1), repeat=m):
            if sum(mult) != D:
                continue
            key = min(tuple(mult[p[v]] for v in range(m)) for p in B['aut'])
            if key in seen:
                continue
            seen.add(key)
            slots = tuple(v for v in range(m) for _ in range(mult[v]))
            rec.append((bi, slots))
    return rec


def embeddings(U, B):
    """Labelled induced embeddings of base B into graph U (list of tuples)."""
    m = B['m']
    out = []
    nodes = list(U.nodes())
    for S in itertools.combinations(nodes, m):
        sub = [(a, b) for a, b in itertools.combinations(range(m), 2) if U.has_edge(S[a], S[b])]
        if small_canon(sub, m) != B['canon']:
            continue
        for p in itertools.permutations(S):
            if all((U.has_edge(p[u], p[v])) == B['G'].has_edge(u, v) for u, v in itertools.combinations(range(m), 2)):
                out.append(p)
    return out


def perm_avg(M):
    """Average over permutations pi of prod_j M[..., j, pi(j)] (vectorised over leading axes)."""
    D = M.shape[-1]
    tot = 0
    for p in itertools.permutations(range(D)):
        prod = M[..., 0, p[0]]
        for j in range(1, D):
            prod = prod * M[..., j, p[j]]
        tot = tot + prod
    return tot / math.factorial(D)


def coefficients(types_by_order, bases, recipes, kernel, D):
    """c[(r, r')][(order, index)] for r <= r'.  types_by_order: dict m -> list of graphs (canonical reps)."""
    g0, g1, g2 = kernel
    by_base = defaultdict(list)
    for r, (bi, slots) in enumerate(recipes):
        by_base[bi].append((r, np.array(slots)))
    coef = defaultdict(dict)
    for m in sorted(types_by_order):
        if m > 2 * D:
            continue
        for ui, U in enumerate(types_by_order[m]):
            n = m
            G = np.full((n, n), float(g2))
            for a, b in U.edges():
                G[a, b] = G[b, a] = g1
            np.fill_diagonal(G, g0)
            embs = {bi: embeddings(U, bases[bi]) for bi in by_base}
            full = (1 << n) - 1
            masks = {bi: [sum(1 << v for v in e) for e in embs[bi]] for bi in embs}
            for b1 in by_base:
                for b2 in by_base:
                    if b2 < b1:
                        continue
                    E1, E2 = embs[b1], embs[b2]
                    if not E1 or not E2:
                        continue
                    pairs = [(x, y) for x, mx in enumerate(masks[b1]) for y, my in enumerate(masks[b2]) if mx | my == full]
                    if not pairs:
                        continue
                    A1 = np.array([E1[x] for x, _ in pairs])
                    A2 = np.array([E2[y] for _, y in pairs])
                    Gb = G[A1[:, :, None], A2[:, None, :]]          # (npairs, |B1|, |B2|)
                    for r1, s1 in by_base[b1]:
                        for r2, s2 in by_base[b2]:
                            if b1 == b2 and r2 < r1:
                                continue
                            M = Gb[:, s1][:, :, s2]
                            val = float(perm_avg(M).sum())
                            if val == 0:
                                continue
                            key = (min(r1, r2), max(r1, r2))
                            coef[key][(m, ui)] = coef[key].get((m, ui), 0.0) + val
            # when b1 != b2 only (b1, b2) with b1 < b2 is enumerated: by symmetry of the kernel
            # c(r2, r1) = c(r1, r2), so one key per unordered recipe pair is exact.
    return coef


def gram_from_counts(coef, nrec, z):
    Gm = np.zeros((nrec, nrec))
    for (r1, r2), d in coef.items():
        v = sum(c * z.get(u, 0) for u, c in d.items())
        Gm[r1, r2] += v
        if r1 != r2:
            Gm[r2, r1] += v
    return Gm


def make_recipes_general(bases, d, maxbase=4):
    """Sym^d recipes with witnesses: any multiset of d vertices of B (B up to maxbase vertices), up to Aut(B).
    The tensor uses only the slot vertices; the other vertices of B are witnesses (they weight the tuples)."""
    rec = []
    for bi, B in enumerate(bases):
        m = B['m']
        if m > maxbase:
            continue
        seen = set()
        for slots in itertools.combinations_with_replacement(range(m), d):
            key = min(tuple(sorted(p[v] for v in slots)) for p in B['aut'])
            if key in seen:
                continue
            seen.add(key)
            rec.append((bi, tuple(slots)))
    return rec


def make_rooted_recipes(bases, d, maxbase=4):
    """Rooted recipes (bi, root, slots): base B with a distinguished root vertex, a multiset of d vertices of B;
    up to automorphisms of B fixing the root."""
    rec = []
    for bi, B in enumerate(bases):
        m = B['m']
        if m > maxbase:
            continue
        roots_seen = set()
        for rho in range(m):
            rk = min(p[rho] for p in B['aut'])
            if rk in roots_seen:
                continue
            roots_seen.add(rk)
            stab = [p for p in B['aut'] if p[rho] == rho]
            seen = set()
            for slots in itertools.combinations_with_replacement(range(m), d):
                key = min(tuple(sorted(p[v] for v in slots)) for p in stab)
                if key in seen:
                    continue
                seen.add(key)
                rec.append((bi, rho, tuple(slots)))
    return rec


def coefficients_general(types_by_order, bases, recipes, kernel, maxorder, rooted=False, harmonic_dim=None):
    """Like coefficients(), with two options:
    rooted: recipes are (bi, root, slots) and only pairs of embeddings with the same root image are summed
            (this is sum_x Gram_x of the recipes rooted at x);
    harmonic_dim: if set (= dimension of the eigenspace), the Sym^d tensors are replaced by their harmonic
            (traceless) projections; implemented for d = 1, 2, 3."""
    g0, g1, g2 = kernel
    by_base = defaultdict(list)
    for r, rc in enumerate(recipes):
        if rooted:
            bi, rho, slots = rc
        else:
            (bi, slots), rho = rc, None
        by_base[bi].append((r, rho, np.array(slots)))
    coef = defaultdict(dict)
    for m in sorted(types_by_order):
        if m > maxorder:
            continue
        for ui, U in enumerate(types_by_order[m]):
            G = np.full((m, m), float(g2))
            for a, b in U.edges():
                G[a, b] = G[b, a] = g1
            np.fill_diagonal(G, g0)
            embs = {bi: embeddings(U, bases[bi]) for bi in by_base}
            full = (1 << m) - 1
            masks = {bi: [sum(1 << v for v in e) for e in embs[bi]] for bi in embs}
            for b1 in by_base:
                for b2 in by_base:
                    if b2 < b1:
                        continue
                    E1, E2 = embs[b1], embs[b2]
                    if not E1 or not E2:
                        continue
                    pairs = [(x, y) for x, mx in enumerate(masks[b1]) for y, my in enumerate(masks[b2]) if mx | my == full]
                    if not pairs:
                        continue
                    A1 = np.array([E1[x] for x, _ in pairs])
                    A2 = np.array([E2[y] for _, y in pairs])
                    Gb = G[A1[:, :, None], A2[:, None, :]]
                    for r1, rho1, s1 in by_base[b1]:
                        for r2, rho2, s2 in by_base[b2]:
                            if b1 == b2 and r2 < r1:
                                continue
                            if rooted:
                                sel = A1[:, rho1] == A2[:, rho2]
                                if not sel.any():
                                    continue
                                Gs_, P1, P2 = Gb[sel], A1[sel], A2[sel]
                            else:
                                Gs_, P1, P2 = Gb, A1, A2
                            M = Gs_[:, s1][:, :, s2]
                            vals = perm_avg(M)
                            if harmonic_dim is not None:
                                vals = vals - trace_correction(G, P1[:, s1], P2[:, s2], harmonic_dim)
                            val = float(vals.sum())
                            if val == 0:
                                continue
                            key = (min(r1, r2), max(r1, r2))
                            coef[key][(m, ui)] = coef[key].get((m, ui), 0.0) + val
    return coef


def trace_correction(G, X, Y, dim):
    """<P x, P y> for the non-harmonic part, x = Sym(p_X1 ... p_Xd), y = Sym(p_Y1 ... p_Yd), vectorised over rows.
    d = 1: 0.  d = 2: tr x tr y / dim.  d = 3: (3/(dim+2)) <tr x, tr y>, tr x = (1/3) sum_{pairs} <.,.> p_other."""
    d = X.shape[1]
    if d == 1:
        return 0.0
    rows = np.arange(X.shape[0])
    if d == 2:
        trx = G[X[:, 0], X[:, 1]]
        try_ = G[Y[:, 0], Y[:, 1]]
        return trx * try_ / dim
    if d == 3:
        # tr x = (1/3)(K(x0,x1) p_x2 + K(x0,x2) p_x1 + K(x1,x2) p_x0)
        cx = [(G[X[:, 0], X[:, 1]], X[:, 2]), (G[X[:, 0], X[:, 2]], X[:, 1]), (G[X[:, 1], X[:, 2]], X[:, 0])]
        cy = [(G[Y[:, 0], Y[:, 1]], Y[:, 2]), (G[Y[:, 0], Y[:, 2]], Y[:, 1]), (G[Y[:, 1], Y[:, 2]], Y[:, 0])]
        ip = 0
        for ax, vx in cx:
            for ay, vy in cy:
                ip = ip + ax * ay * G[vx, vy]
        return (3.0 / (dim + 2)) * ip / 9.0
    raise NotImplementedError
