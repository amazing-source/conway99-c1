"""Twist type of an edge x-a (pure combinatorics, exploratory).
At x, the lines other than m = line(x,a) are the classes {c, c'} (mate pairs); at a, the lines other than m pair the
points {a,b} (b a label at x) as {a,b} ~ {a,tau_a(b)}. The union of the mate matching and tau_a on the 2t labels is a
disjoint union of even cycles; a cycle through c classes gives a part c. The twist type of x-a is this partition of t
(1^t = untwisted edge; parts >= 2 = twisted classes, twisted together). Also: sigma_m (holonomy around the line m, a
permutation of the 2t labels at x off m) and its cycle type.  We look for laws relating the types of the three edges
of a line and the cycle type of sigma_m, on every available geometry.
"""
import json
from collections import Counter
import numpy as np
import graphs, rooted


def partition_of(match1, match2, labels):
    seen, parts = set(), []
    for s in labels:
        if s in seen:
            continue
        cyc, u, use1 = 0, s, True
        while True:
            seen.add(u)
            v = match1[u] if use1 else match2[u]
            cyc += 1
            use1 = not use1
            u = v
            if u == s and use1:
                break
        parts.append(cyc // 2)
    return tuple(sorted(parts, reverse=True))


def cycle_type(perm, labels):
    seen, parts = set(), []
    for s in labels:
        if s in seen:
            continue
        n, u = 0, s
        while u not in seen:
            seen.add(u)
            u = perm[u]
            n += 1
        parts.append(n)
    return tuple(sorted(parts, reverse=True))


def analyse(name, A):
    A = np.asarray(A)
    adj = rooted.adjacency_lists(A)
    n = len(A)
    lines = [tuple(l) for l in rooted.lines(A)]
    line_of = {}
    for l in lines:
        for u in l:
            for v in l:
                if u != v:
                    line_of[(u, v)] = l

    def edge_type(x, a):
        m = line_of[(x, a)]
        labs = [b for b in adj[x] if b not in m]
        mate = {b: next(c for c in adj[x] if c != b and A[b, c] and c not in m) for b in labs}
        tau = {}
        for b in labs:
            z = next(iter((adj[a] & adj[b]) - {x}))
            lz = line_of[(a, z)]
            z2 = next(w for w in lz if w not in (a, z))
            c = next(iter((adj[z2] & set(labs))))
            tau[b] = c
        return partition_of(mate, tau, labs), tau, mate

    def sigma(x, m):
        a, ab = [u for u in m if u != x]
        labs = [b for b in adj[x] if b not in m]
        s = {}
        for b in labs:
            z = next(iter((adj[a] & adj[b]) - {x}))            # {a,b}
            w = next(u for u in adj[z] if ab in adj[u] and u != a and u not in m and u not in adj[x])  # {ab, s(b)}
            s[b] = next(iter(adj[w] & set(labs)))
        return cycle_type(s, labs), s

    types = Counter()
    triples = Counter()
    law_same_x = 0
    tot_lines = 0
    for l in lines:
        x, a, ab = l
        t_xa, _, _ = edge_type(x, a)
        t_xab, _, _ = edge_type(x, ab)
        t_aab, _, _ = edge_type(a, ab)
        for tt in (t_xa, t_xab, t_aab):
            types[tt] += 1
        cs, _ = sigma(x, l)
        triples[(tuple(sorted([t_xa, t_xab, t_aab])), cs)] += 1
        tot_lines += 1
    print(f'== {name}: {n} vertices, {tot_lines} lines; twist types of edges: {dict(types)}')
    for (tt, cs), c in sorted(triples.items(), key=lambda z: -z[1])[:12]:
        print(f'   line edge-types {tt}   sigma cycle type {cs}   x{c}')


if __name__ == '__main__':
    analyse('twist t=2 (20)', json.load(open('../data/t2_twisted.json')))
    analyse('twist t=3 (39)', json.load(open('../data/t3_twisted.json')))
    analyse('twist t=3 (42)', json.load(open('../data/t3_twisted_42.json')))
    analyse('srg9', graphs.srg9())
