"""Line components in the known srg(243,22,1,2): for every line (triangle) l, c(l) = number of connected components of
the cubic graph induced on N(l) (the 60 vertices adjacent to exactly one point of l).  Does c(l) = 1 ever occur in a REAL
member of the lambda = 1, mu = 2 family?
usage: python c243_components.py <edges file> ..."""
import collections, sys, itertools
for path in sys.argv[1:]:
    n = 243
    adj = [set() for _ in range(n)]
    for line in open(path):
        if line.strip():
            i, j = map(int, line.split()); adj[i].add(j); adj[j].add(i)
    lines = set()
    for v in range(n):
        for a in adj[v]:
            b = next(iter(adj[v] & adj[a]))
            lines.add(frozenset((v, a, b)))
    cnt = collections.Counter()
    sizes = collections.Counter()
    for l in lines:
        Nl = set()
        for p in l:
            Nl |= adj[p]
        Nl -= l
        assert len(Nl) == 60
        deg = {u: len(adj[u] & Nl) for u in Nl}
        assert set(deg.values()) == {3}
        seen, comps = set(), []
        for u in Nl:
            if u in seen: continue
            st, comp = [u], {u}; seen.add(u)
            while st:
                x = st.pop()
                for y in adj[x] & Nl:
                    if y not in seen:
                        seen.add(y); comp.add(y); st.append(y)
            comps.append(len(comp))
        cnt[len(comps)] += 1
        sizes[tuple(sorted(comps))] += 1
    print("%s: %d lines; c(l) distribution %s" % (path.split("/")[-1], len(lines), dict(sorted(cnt.items()))))
    print("    component size patterns:", dict(sizes.most_common(6)))
