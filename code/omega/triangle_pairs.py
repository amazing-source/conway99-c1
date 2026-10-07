"""Pairs of disjoint triangles of an srg(243,22,1,2) by number of edges between them (Makhnev (*): no pair with exactly 2;
that count is n3 = 3(P_max - P) of Reimbayev).  Run from the repo root."""
import sys, itertools
def load(p, n=243):
    adj = [set() for _ in range(n)]
    for line in open(p):
        if line.strip():
            i, j = map(int, line.split()); adj[i].add(j); adj[j].add(i)
    return adj
for name in ("bvls243", "twin243_switched"):
    adj = load(f"data/srg243/{name}.edges"); n = len(adj)
    tris = set()
    for i in range(n):
        for j in adj[i]:
            for k in adj[i] & adj[j]:
                tris.add(tuple(sorted((i, j, k))))
    tris = sorted(tris)
    # count pairs of disjoint triangles joined by exactly e edges
    cnt = {}
    tri_of = {}
    for t in tris:
        for x in t: tri_of.setdefault(x, []).append(t)
    seen = set()
    for t in tris:
        nb = set()
        for x in t:
            for y in adj[x]:
                for s in tri_of[y]:
                    if s != t and not set(s) & set(t): nb.add(s)
        for s in nb:
            key = (min(s, t), max(s, t))
            if key in seen: continue
            seen.add(key)
            e = sum(1 for x in t for y in s if y in adj[x])
            cnt[e] = cnt.get(e, 0) + 1
    print(name, "triangles", len(tris), "pairs of disjoint triangles by #edges between them:", dict(sorted(cnt.items())))
