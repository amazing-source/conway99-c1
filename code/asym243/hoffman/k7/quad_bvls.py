import collections, itertools
R = '/home/user/strongly-regular-graphs-research/results/srg243_family/'
n = 243; adj = [set() for _ in range(n)]
for line in open(R + 'bvls243.edges'):
    if line.strip():
        u, v = map(int, line.split()); adj[u].add(v); adj[v].add(u)
C = set(map(int, open(R + 'bvls243_hoffman_coclique.txt').read().split()))
pat = collections.Counter(); patC = collections.Counter()
for c in range(n):
    N = sorted(adj[c]); mate = {a: next(iter(adj[a] & adj[c])) for a in N}
    E = sorted({tuple(sorted((a, mate[a]))) for a in N})
    z = {}
    for w in range(n):
        if w != c and w not in adj[c]:
            p = tuple(sorted(adj[w] & adj[c])); z[p] = w
    for (a, a2), (b, b2) in itertools.combinations(E, 2):
        Q = {(a, b): z[tuple(sorted((a, b)))], (a, b2): z[tuple(sorted((a, b2)))],
             (a2, b): z[tuple(sorted((a2, b)))], (a2, b2): z[tuple(sorted((a2, b2)))]}
        ks = list(Q)
        edges = []
        for p, q in itertools.combinations(ks, 2):
            if Q[q] in adj[Q[p]]: edges.append('side' if set(p) & set(q) else 'diag')
        key = tuple(sorted(edges)); pat[key] += 1
        if c in C: patC[(key, sum(Q[k] in C for k in ks))] += 1
print('quadruple induced edge patterns (all c):', dict(pat))
print('for c in C, (pattern, #points of C in quadruple):', dict(patC))
