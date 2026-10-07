"""Does an srg(243,22,1,2) contain the 'biplane configuration' of norm 22 for the eigenvalue -5?  (C1, lab, 2026-10-07)
  python -I biplane_test.py <edge list file>
Configuration (hand analysis of the laptop session, not refereed): P, Q independent 11-sets, every vertex of P has exactly 5
neighbours in Q and conversely, every pair of P has both its common neighbours in Q (the graph between P and Q is the incidence
graph of a 2-(11,5,2) biplane). Then phi = 1_P - 1_Q is an integer eigenvector of A for -5, of squared norm 22.
Search, exhaustive: for each vertex p0 (taken in P): its 5 neighbours in Q are pairwise non-adjacent, so at most one in each of
the 11 triangles on p0; each pair of them has exactly one common neighbour besides p0, which gives the 10 other vertices of P;
then everything is verified, and A phi = -5 phi is checked in integers. Each configuration is met once per vertex of P and, with
the roles exchanged, once per vertex of Q: 22 times."""
import sys, itertools
E = [tuple(int(x) for x in l.replace(",", " ").split()[:2]) for l in open(sys.argv[1]) if l.strip() and l.strip()[0].isdigit()]
n = max(max(e) for e in E) + 1; lo = min(min(e) for e in E); assert lo in (0, 1)
if lo == 1: E = [(a - 1, b - 1) for a, b in E]; n -= 1
adj = [set() for _ in range(n)]
for a, b in E: adj[a].add(b); adj[b].add(a)
assert n == 243 and all(len(s) == 22 for s in adj)
for a in range(n):                                                       # srg(243,22,1,2), exact
    for b in range(a + 1, n): assert len(adj[a] & adj[b]) == (1 if b in adj[a] else 2)
found = set(); cand = 0
for p0 in range(n):
    N = sorted(adj[p0]); tri = []; seen = set()
    for x in N:
        if x in seen: continue
        (y,) = adj[p0] & adj[x]; tri.append((x, y)); seen |= {x, y}
    assert len(tri) == 11
    for T5 in itertools.combinations(range(11), 5):
        for pick in itertools.product((0, 1), repeat=5):
            Q5 = [tri[t][s] for t, s in zip(T5, pick)]; cand += 1; P = {p0}; ok = True
            for i in range(5):
                for j in range(i + 1, 5):
                    c = adj[Q5[i]] & adj[Q5[j]]
                    if len(c) != 2: ok = False; break
                    (x,) = c - {p0}
                    if x in P or x in adj[p0] or any(x in adj[p] for p in P): ok = False; break
                    P.add(x)
                if not ok: break
            if not ok or len(P) != 11: continue
            Q = set()
            for a, b in itertools.combinations(sorted(P), 2): Q |= adj[a] & adj[b]
            if len(Q) != 11 or Q & P: continue
            if any(len(adj[p] & Q) != 5 or (adj[p] & P) for p in P): continue
            if any(len(adj[q] & P) != 5 or (adj[q] & Q) for q in Q): continue
            phi = [0] * n
            for p in P: phi[p] = 1
            for q in Q: phi[q] = -1
            assert all(sum(phi[w] for w in adj[v]) == -5 * phi[v] for v in range(n)), "not an eigenvector"
            found.add((frozenset(P), frozenset(Q)))
pairs = {frozenset([c, (c[1], c[0])]) for c in found}
print("graph %s: srg(243,22,1,2) verified; candidates examined %d; ordered configurations (P,Q) found %d; eigenvectors of norm 22 up to sign: %d" % (sys.argv[1].replace(chr(92), "/").split("/")[-1], cand, len(found), len(pairs)))
