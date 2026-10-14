"""Special lines = lines l whose 36 (resp. 3(k-2)) outer neighbours induce a DISCONNECTED cubic graph H_l
(theorem of 14/10: special <=> lambda_2(H_l) = 3 <=> H_l disconnected, by interlacing). Census over all lines of a
lambda = 1 graph given as an edge list.  usage: python line_components.py <edges file> ..."""
import sys
from collections import Counter


def census(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = 1 + max(max(e) for e in E)
    adj = [set() for _ in range(n)]
    for a, b in E:
        adj[a].add(b)
        adj[b].add(a)
    lines = set()
    for a in range(n):
        for b in adj[a]:
            if b > a:
                c = (adj[a] & adj[b])
                assert len(c) == 1, "lambda must be 1"
                lines.add(tuple(sorted((a, b, next(iter(c))))))
    comp_hist = Counter()
    sizes_hist = Counter()
    for l in lines:
        L = set(l)
        W = set().union(*(adj[u] for u in l)) - L
        # components of the induced subgraph on W
        seen, comps = set(), []
        for s in W:
            if s in seen:
                continue
            stack, comp = [s], set()
            seen.add(s)
            while stack:
                u = stack.pop()
                comp.add(u)
                for w in adj[u] & W:
                    if w not in seen:
                        seen.add(w)
                        stack.append(w)
            comps.append(len(comp))
        degs = {len(adj[u] & W) for u in W}
        assert degs == {3}, degs
        comp_hist[len(comps)] += 1
        sizes_hist[tuple(sorted(comps))] += 1
    return n, len(lines), comp_hist, sizes_hist


for p in sys.argv[1:]:
    n, nl, ch, sh = census(p)
    print("%s: n=%d, lines=%d, components of H_l -> #lines %s" % (p.split('/')[-1], n, nl, dict(sorted(ch.items()))))
    print("   component size patterns (most common):", sh.most_common(5))
