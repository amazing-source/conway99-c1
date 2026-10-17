import sys, collections, itertools
R = '/home/user/strongly-regular-graphs-research/results/srg243_family/'
n = 243; adj = [set() for _ in range(n)]
for line in open(R + 'bvls243.edges'):
    if line.strip():
        u, v = map(int, line.split()); adj[u].add(v); adj[v].add(u)
C = list(map(int, open(R + 'bvls243_hoffman_coclique.txt').read().split()))
assert len(C) == 45 and all(not (adj[a] & {b}) for a in C for b in C)
Cs = set(C); dist = collections.Counter(); kinds = collections.Counter()
for c in C:
    N = sorted(adj[c]); mate = {a: next(iter(adj[a] & adj[c])) for a in N}
    edges = sorted({tuple(sorted((a, mate[a]))) for a in N}); eid = {}
    for i, (a, b) in enumerate(edges): eid[a] = eid[b] = i
    per = collections.Counter(); gam = []
    for x in C:
        if x == c: continue
        cn = sorted(adj[c] & adj[x]); assert len(cn) == 2
        a, b = cn; gam.append((a, b))
        per[tuple(sorted((eid[a], eid[b])))] += 1
    for pr in itertools.combinations(range(len(edges)), 2): dist[per[pr]] += 1
    # same-vertex vs disjoint when two points share a mate-edge pair
    bypair = collections.defaultdict(list)
    for a, b in gam: bypair[tuple(sorted((eid[a], eid[b])))].append((a, b))
    for pr, L in bypair.items():
        for (a, b), (a2, b2) in itertools.combinations(L, 2):
            kinds['share a vertex' if {a, b} & {a2, b2} else 'disjoint'] += 1
print('distribution of #points per pair of mate-edges (over all c):', dict(sorted(dist.items())))
print('when 2 points sit on the same pair of mate-edges:', dict(kinds))
