import collections, itertools, sys
def check(fn, n):
    adj = [set() for _ in range(n)]
    for line in open(fn):
        if line.strip():
            u, v = map(int, line.split()); adj[u].add(v); adj[v].add(u)
    pat = collections.Counter()
    for c in range(n):
        N = sorted(adj[c]); mate = {a: next(iter(adj[a] & adj[c])) for a in N}
        E = sorted({tuple(sorted((a, mate[a]))) for a in N}); z = {}
        for w in range(n):
            if w != c and w not in adj[c]: z[tuple(sorted(adj[w] & adj[c]))] = w
        for (a, a2), (b, b2) in itertools.combinations(E, 2):
            Q = {k: z[tuple(sorted(k))] for k in [(a, b), (a, b2), (a2, b), (a2, b2)]}
            e = sorted('side' if set(p) & set(q) else 'diag' for p, q in itertools.combinations(Q, 2) if Q[q] in adj[Q[p]])
            pat[tuple(e)] += 1
    print(fn.split('/')[-1], dict(pat))
R = '/home/user/strongly-regular-graphs-research/results/srg243_family/'
for f in ['twin243.edges', 'gamma3_aut864.edges', 'gamma4_aut3888.edges']: check(R + f, 243)
