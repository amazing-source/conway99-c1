"""c(T) distribution over all lines of a real srg(v,k,1,2) (LAB 19/10/2026). usage: python c_dist.py <edges>"""
import sys
from collections import Counter
edges = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
v = 1 + max(max(e) for e in edges)
adj = [set() for _ in range(v)]
for a, b in edges:
    adj[a].add(b); adj[b].add(a)
lines = sorted({tuple(sorted((a, b, c))) for a in range(v) for b in adj[a] for c in adj[a] & adj[b]})
dist, sizes = Counter(), Counter()
for T in lines:
    Ts = set(T)
    near = {u for t in T for u in adj[t]} - Ts
    seen, comps = set(), []
    for x in near:
        if x in seen: continue
        st, cnt = [x], 0
        seen.add(x)
        while st:
            y = st.pop(); cnt += 1
            for z in adj[y] & near:
                if z not in seen:
                    seen.add(z); st.append(z)
        comps.append(cnt)
    dist[len(comps)] += 1
    sizes[tuple(sorted(comps))] += 1
print(sys.argv[1].split('/')[-1], 'lines', len(lines), 'c distribution', dict(sorted(dist.items())), 'size profiles', dict(sizes.most_common(6)))
