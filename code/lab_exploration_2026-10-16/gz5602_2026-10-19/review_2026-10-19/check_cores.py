# Review check: recompute T for each labelled core from its edges; check 2-regularity and the
# letter rule; check that orbit representatives under swap(1,2) x flips(0,1,2) cover all 114 cores.
import json, sys
from itertools import combinations, product
W = sys.argv[1]
cores = json.load(open(W + "/paircores8.json"))
orb = json.load(open(W + "/paircore_orbits16.json"))
CORE = tuple((s, 2*r+t) for r in (1, 2) for s, t in product(range(2), repeat=2))
print("n cores", len(cores), "keys", sorted(cores[0].keys()))
bad = 0
for ci, c in enumerate(cores):
    E = {tuple(sorted(e)) for e in c['edges']}
    adj = [[0]*8 for _ in range(8)]
    for u, v in E: adj[u][v] = adj[v][u] = 1
    deg = [sum(r) for r in adj]
    if deg != [2]*8: print("core", ci, "not 2-regular", deg); bad += 1
    for u, v in combinations(range(8), 2):
        sh = len(set(CORE[u]) & set(CORE[v]))
        com = sum(adj[u][w] and adj[v][w] for w in range(8))
        t = 2 - adj[u][v] - sh - com
        if c['T']['%d-%d' % (u, v)] != t:
            print("core", ci, "T mismatch", u, v, c['T']['%d-%d' % (u, v)], t); bad += 1
        if t < 0: print("core", ci, "negative T", u, v); bad += 1
    # letter rule inside the core: for each core vertex w and letter l, # core nbrs carrying l <= 2-[l in w]-[l^1 in w]
    for w in range(8):
        for l in range(14):
            q = 2 - (l in CORE[w]) - ((l ^ 1) in CORE[w])
            k = sum(adj[w][x] for x in range(8) if l in CORE[x])
            if k > q: print("core", ci, "letter violation", w, l); bad += 1
    if sum(c['T'].values()) != 24: print("core", ci, "sum T", sum(c['T'].values())); bad += 1
print("bad", bad)
# orbit cover
lookup = {q: i for i, q in enumerate(CORE)}
def image(c, swap, flips):
    roots = (0, 2, 1) if swap else (0, 1, 2)
    p = [lookup[tuple(sorted(2*roots[l//2] + ((l % 2) ^ flips[l//2]) for l in q))] for q in CORE]
    return frozenset(tuple(sorted((p[u], p[v]))) for u, v in c['edges'])
keyset = {frozenset(tuple(sorted(e)) for e in c['edges']): i for i, c in enumerate(cores)}
print("distinct cores", len(keyset))
reps = orb['representatives']; print("reps", len(reps), reps)
covered = set()
for r in reps:
    for swap in (0, 1):
        for fl in product(range(2), repeat=3):
            im = image(cores[r], swap, fl)
            assert im in keyset, ("image not in catalogue", r)
            covered.add(keyset[im])
print("covered", len(covered), "of", len(cores))
