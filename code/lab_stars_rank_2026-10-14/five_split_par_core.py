"""Shared construction of the 34 M_4 orbit cases of the five-star problem (same order as five_split_par.py)."""
import itertools
import random

from stars_rank import build

pts = [0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13]


def matchings(p):
    if not p:
        yield []
        return
    a = p[0]
    for i in range(1, len(p)):
        rest = p[1:i] + p[i + 1:]
        for m in matchings(rest):
            yield [(a, p[i])] + m


star_maps = []
for sl in (False, True):
    for s0 in (False, True):
        for s1 in (False, True):
            g = {0: 0, 1: 1, 2: 2, 3: 3}
            if s0:
                g[0], g[1] = 1, 0
            if s1:
                g[2], g[3] = 3, 2
            if sl:
                g = {k: {0: 2, 1: 3, 2: 0, 3: 1}[v] for k, v in g.items()}
            star_maps.append(g)
outer_lines = [(6, 7), (8, 9), (10, 11), (12, 13)]
outer_maps = []
for perm in itertools.permutations(range(4)):
    for flips in itertools.product((0, 1), repeat=4):
        g = {}
        for i, (a, b) in enumerate(outer_lines):
            c, d = outer_lines[perm[i]]
            if flips[i]:
                c, d = d, c
            g[a], g[b] = c, d
        outer_maps.append(g)
group = [dict(list(s.items()) + list(o.items())) for s in star_maps for o in outer_maps]


def canon(m):
    return min(tuple(sorted(tuple(sorted((g[a], g[b]))) for a, b in m)) for g in group)


reps = {}
for m in matchings(pts):
    c = canon(m)
    reps[c] = reps.get(c, 0) + 1
reps = sorted(reps.items(), key=lambda kv: kv[0])
assert len(reps) == 34
S, idx, e, F = build([0, 1, 2, 3, 4], random.Random(1))
base = "\n".join(" ".join(map(str, c)) + " 0" for c in F.clauses)
L4 = [l for l in S if 4 in l]


def write_case(k, path):
    rep, size = reps[k]
    pairs = set(frozenset(p) for p in rep)
    units = []
    for x, y in itertools.combinations(L4, 2):
        a = list(x - {4})[0]
        b = list(y - {4})[0]
        v = e[(idx[x], idx[y])]
        units.append(v if frozenset((a, b)) in pairs else -v)
    with open(path, "w") as fh:
        fh.write("p cnf %d %d\n" % (F.n, len(F.clauses) + len(units)))
        fh.write(base + "\n")
        for u in units:
            fh.write("%d 0\n" % u)
    return rep, size
