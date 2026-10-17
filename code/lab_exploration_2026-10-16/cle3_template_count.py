"""Size of the root-template list for the branch min c <= 3 (Codex's quotient, extended).  A template = a simple graph G on
the 7 root lines (edge = non-grid pair) and, for each line i, a partition of its G-neighbours into blocks of size >= 2
(nontrivial components; grid partners are the singletons).  c_i = (6 - deg_i) + #blocks.  Branch c_min = k: all c_i >= k
and some c_i = k (root chosen on a line of globally minimal c).  Here we only COUNT raw templates per graph orbit
(product of admissible partitions), with Codex's Gray-code enumeration of graph representatives.
usage: python cle3_template_count.py"""
from itertools import combinations, permutations, product
from collections import Counter
import time

EDGES = tuple(combinations(range(7), 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}
def relabel(mask, perm):
    r = 0
    for k, (a, b) in enumerate(EDGES):
        if mask & (1 << k):
            r |= 1 << EDGE_INDEX[tuple(sorted((perm[a], perm[b])))]
    return r
def set_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for sub in set_partitions(rest):
        for i in range(len(sub)):
            yield sub[:i] + [[first] + sub[i]] + sub[i + 1:]
        yield [[first]] + sub
def admissible(items, kmin):
    out = []
    for P in set_partitions(list(items)):
        if all(len(b) >= 2 for b in P):
            c = 6 - len(items) + len(P)
            if c >= kmin:
                out.append((tuple(tuple(sorted(b)) for b in P), c))
    return out
t0 = time.time()
# graph representatives up to isomorphism (all degrees), as in Codex's code but without the degree filter
seen, reps = set(), []
deg = [0] * 7; prev = 0
for index in range(1 << 21):
    mask = index ^ (index >> 1)
    if index:
        ch = mask ^ prev; k = ch.bit_length() - 1; inc = 1 if mask & ch else -1
        a, b = EDGES[k]; deg[a] += inc; deg[b] += inc
    prev = mask
    if deg != sorted(deg) or mask in seen:
        continue
    groups = [[i for i, d in enumerate(deg) if d == v] for v in sorted(set(deg))]
    orbit = set()
    for imgs in product(*(permutations(g) for g in groups)):
        perm = list(range(7))
        for g, t in zip(groups, imgs):
            for x, y in zip(g, t):
                perm[x] = y
        orbit.add(relabel(mask, perm))
    seen.update(orbit)
    reps.append(min(orbit))
print("graph representatives (all degrees):", len(reps), "in %.0f s" % (time.time() - t0))
for kmin in (3, 2, 1):
    total, graphs = 0, 0
    for mask in reps:
        edges = [e for i, e in enumerate(EDGES) if mask & (1 << i)]
        nb = [[b if a == i else a for a, b in edges if i in (a, b)] for i in range(7)]
        opts = [admissible(nb[i], kmin) for i in range(7)]
        if any(len(o) == 0 for o in opts):
            continue
        # need some line with c exactly kmin: count tuples with min c == kmin
        cnt_all = 1
        for o in opts: cnt_all *= len(o)
        cnt_gt = 1
        for o in opts: cnt_gt *= sum(1 for _, c in o if c > kmin)
        n = cnt_all - cnt_gt
        if n:
            graphs += 1
            total += n
    print("c_min = %d: graph orbits with templates %d ; raw templates (graph orbit x labelled partition choices) %.3g" % (kmin, graphs, total))
