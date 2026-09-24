"""Program D probe: parity data of line holonomies sigma_L (permutation of N(x) minus L around the line L)
and edge twist types, on every available geometry.  Looking for local/global parity laws."""
import json, itertools
from collections import Counter
import numpy as np
import graphs, rooted

def perm_sign(p, dom):
    seen, sgn = set(), 1
    for s in dom:
        if s in seen:
            continue
        n, u = 0, s
        while u not in seen:
            seen.add(u); u = p[u]; n += 1
        if n % 2 == 0:
            sgn = -sgn
    return sgn

def analyse(name, A):
    A = np.asarray(A); adj = rooted.adjacency_lists(A); n = len(A)
    lines = [tuple(l) for l in rooted.lines(A)]
    line_of = {}
    for l in lines:
        for u in l:
            for v in l:
                if u != v:
                    line_of[(u, v)] = l
    def holonomy(x, m):
        a, ab = [u for u in m if u != x]
        labs = [b for b in adj[x] if b not in m]
        s = {}
        for b in labs:
            # b -> unique neighbour of b in N(a)\m -> its unique neighbour in N(ab)\m -> its unique neighbour in N(x)\m
            c1 = next(iter((adj[b] & adj[a]) - set(m)))
            c2 = next(iter((adj[c1] & adj[ab]) - set(m)))
            c3 = next(iter((adj[c2] & adj[x]) - set(m)))
            s[b] = c3
        return s, labs
    sgn_by_t = Counter(); per_vertex = Counter(); tot_minus = 0
    base_dep = 0
    for m in lines:
        sg = []
        for x in m:
            s, labs = holonomy(x, m)
            t = sum(1 for b in labs if s[b] != b)
            sg.append((perm_sign(s, labs), t))
        if len(set(sg)) > 1:
            base_dep += 1
        sgn, t = sg[0]
        sgn_by_t[(t, sgn)] += 1
        tot_minus += (sgn == -1)
    for x in range(n):
        prod = 1
        for m in lines:
            if x in m:
                s, labs = holonomy(x, m)
                prod *= perm_sign(s, labs)
        per_vertex[prod] += 1
    print(f'{name}: lines {len(lines)}; (t, sign) counts {dict(sorted(sgn_by_t.items()))}; '
          f'#odd holonomies {tot_minus}; base-point dependence {base_dep}; product of signs per vertex {dict(per_vertex)}')

for name, A in [('t2 (20)', json.load(open('../data/t2_twisted.json'))),
                ('t3 (39)', json.load(open('../data/t3_twisted.json'))),
                ('t3 (42)', json.load(open('../data/t3_twisted_42.json'))),
                ('srg9', graphs.srg9()), ('bvls', graphs.bvls())]:
    analyse(name, A)
