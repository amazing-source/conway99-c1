"""Size of the root component cover if every line has c >= 3 (c_min = 3), compared with Codex's c >= 4 (LAB 18/10/2026).
Codex's framework (QUOTIENT_COMPOSANTES_RACINE_2026_10_16.txt sections 1-3): G = graph of the non-grid pairs among the
7 lines at a root; at a line of degree d the non-grid partners split into parts of size >= 2 (a part of size 1 would
be a prism = grid), c = (6 - d) + #parts.  J has one vertex per part, one edge per non-grid pair; dim ker C =
|E(J)| - |V(J)| + #bipartite components (Codex (2)), and rank R <= dim ker C.
Counts LABELED configurations exactly (no enumeration of the products), then samples configurations for the
distribution of dim ker C and of Codex's first exclusion (a coordinate identically zero in ker C).  Seconds, no solver.
usage: python cmin3_count.py [samples]"""
import itertools
import random
import sys
from collections import Counter

import numpy as np

PAIRS = list(itertools.combinations(range(7), 2))


_memo = {}


def choices(nb, cmin):
    """list of (parts, c) for a line with non-grid neighbour set nb, keeping c >= cmin (memoised)."""
    key = (tuple(nb), cmin)
    if key not in _memo:
        _memo[key] = _choices(nb, cmin)
    return _memo[key]


def _choices(nb, cmin):
    d = len(nb)
    out = []
    if d == 0:
        out.append(([], 6))
    elif d == 1:
        return []
    else:
        def splits(rest):
            if not rest:
                yield []
                return
            first, others = rest[0], rest[1:]
            for k in range(1, len(others) + 1):
                for comb in itertools.combinations(others, k):
                    left = [x for x in others if x not in comb]
                    for tail in splits(left):
                        yield [(first,) + comb] + tail
        for parts in splits(sorted(nb)):
            out.append((parts, 6 - d + len(parts)))
    return [(p, c) for p, c in out if c >= cmin]


def kernel_info(G_edges, parts_of):
    comp = {}
    for i in range(7):
        for k, p in enumerate(parts_of[i]):
            for j in p:
                comp[(i, j)] = (i, k)
    verts = sorted(set(comp.values()))
    vid = {v: n for n, v in enumerate(verts)}
    E = [(vid[comp[(i, j)]], vid[comp[(j, i)]]) for i, j in G_edges]
    Cm = np.zeros((len(verts), len(E)))
    for e, (a, b) in enumerate(E):
        Cm[a, e] += 1
        Cm[b, e] += 1
    if not E:
        return 0, False
    u, s, vt = np.linalg.svd(Cm)
    rank = int((s > 1e-9).sum())
    ker = vt[rank:]
    dim = len(E) - rank
    zero_coord = dim == 0 or bool((np.abs(ker).max(axis=0) < 1e-9).any())
    return dim, zero_coord


def run(cmin, samples, rng):
    total = 0
    weighted = []
    for mask in range(1 << 21):
        nbm = [0] * 7
        for k in range(21):
            if mask >> k & 1:
                i, j = PAIRS[k]
                nbm[i] |= 1 << j
                nbm[j] |= 1 << i
        if any(bin(x).count("1") == 1 for x in nbm):
            continue
        ch = [choices(tuple(j for j in range(7) if nbm[i] >> j & 1), cmin) for i in range(7)]
        edges = [PAIRS[k] for k in range(21) if mask >> k & 1]
        if any(not c for c in ch):
            continue
        n = 1
        for c in ch:
            n *= len(c)
        total += n
        weighted.append((n, mask, ch, edges))
    dist = Counter()
    excl = 0
    has3 = 0
    if samples:
        ws = [w[0] for w in weighted]
        for _ in range(samples):
            n, mask, ch, edges = rng.choices(weighted, weights=ws)[0]
            pick = [rng.choice(c) for c in ch]
            parts_of = [p for p, _ in pick]
            dim, z = kernel_info(edges, parts_of)
            dist[dim] += 1
            excl += z
            has3 += any(c == 3 for _, c in pick)
    return total, len(weighted), dist, excl, has3


if __name__ == "__main__":
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    rng = random.Random(20261018)
    for cmin in (4, 3):
        total, ngraphs, dist, excl, has3 = run(cmin, S, rng)
        print("c >= %d: labeled graphs %d, labeled configurations %d" % (cmin, ngraphs, total))
        print("   sample %d: dim ker C distribution %s ; first exclusion (zero coordinate) %.1f%% ; some line with c = 3: %.1f%%"
              % (S, dict(sorted(dist.items())), 100.0 * excl / S, 100.0 * has3 / S))
