import collections, itertools
from fx_cycles import load, rook3, fx
R = '/home/user/strongly-regular-graphs-research/results/srg243_family/'
def triangles(n, adj):
    return [t for t in itertools.combinations(range(n), 3) if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]]
def twisted(n, adj, T):
    # pairs of disjoint triangles joined by exactly 2 edges (count via vertex -> triangle index)
    tri_of = collections.defaultdict(list)
    for i, t in enumerate(T):
        for u in t: tri_of[u].append(i)
    cnt = collections.Counter()
    for i, t in enumerate(T):
        for u in t:
            for w in adj[u]:
                if w in t: continue
                for j in tri_of[w]:
                    if j > i and not set(T[j]) & set(t): cnt[(i, j)] += 1
    return collections.Counter(cnt.values())
def pi_structure(n, adj, x):
    N = adj[x]; mate = {a: (N & adj[a]).pop() for a in N}
    out = collections.Counter()
    for a in N:
        Z = {}
        for b in N - {a, mate[a]}:
            z = ((adj[a] & adj[b]) - {x}).pop(); Z[b] = z
        inv = {z: b for b, z in Z.items()}
        pi = {b: inv[((adj[Z[b]] & adj[a]) - {x}).pop()] for b in Z}
        # cycle type of the union of pi and mate matching on N(x)-{a,a'}
        seen, lens = set(), []
        for b in Z:
            if b in seen: continue
            L, u, use_pi = 0, b, True
            while True:
                seen.add(u); L += 1
                u = pi[u] if use_pi else mate[u]; use_pi = not use_pi
                if u == b and use_pi: break
            lens.append(L)
        out[tuple(sorted(lens))] += 1
    return out
for name, (n, adj) in [('Paley9', rook3())] + [(f, load(R + f)) for f in ['bvls243.edges', 'twin243.edges', 'gamma3_aut864.edges', 'gamma4_aut3888.edges']]:
    T = triangles(n, adj); tw = twisted(n, adj, T)
    nongrid = sum(sum(L for L in fx(n, adj, x) if L != 4) for x in range(n))
    pis = collections.Counter()
    for x in range(n): pis += pi_structure(n, adj, x)
    print(f"== {name}: triangles {len(T)}, pairs by #edges {dict(sorted(tw.items()))}; n3(2 edges)={tw.get(2,0)}; sum_x nongrid|Delta_x| = {nongrid} (= 2 n3 ? {nongrid == 2*tw.get(2,0)})")
    print(f"   pi_a u M cycle types (half-lengths, i.e. #pi-edges per alternating cycle) over all (x,a): {dict(pis.most_common(6))}")
