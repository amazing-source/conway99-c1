"""Same exhaustive test as biplane_test.py, with parameters, used as a POSITIVE CONTROL on the 3 x 3 rook's graph (u = 1).
  python -I biplane_test_general.py rook        -> srg(9,4,1,2), eigenvalue -2, configuration K_{2,2} (m = 2, block size 2)
  python -I biplane_test_general.py <edge file> <n> <k> <block size> <eigenvalue>"""
import sys, itertools
if sys.argv[1] == "rook":
    V = [(i, j) for i in range(3) for j in range(3)]; E = [(a, b) for a in range(9) for b in range(a + 1, 9) if (V[a][0] == V[b][0]) != (V[a][1] == V[b][1])]
    n, k, bs, ev = 9, 4, 2, -2
else:
    E = [tuple(int(x) for x in l.split()[:2]) for l in open(sys.argv[1]) if l.strip()]; n, k, bs, ev = [int(x) for x in sys.argv[2:6]]
adj = [set() for _ in range(n)]
for a, b in E: adj[a].add(b); adj[b].add(a)
assert all(len(s) == k for s in adj)
for a in range(n):
    for b in range(a + 1, n): assert len(adj[a] & adj[b]) == (1 if b in adj[a] else 2)
m = 1 + bs * (bs - 1) // 2; found = set(); cand = 0
for p0 in range(n):
    tri = []; seen = set()
    for x in sorted(adj[p0]):
        if x in seen: continue
        (y,) = adj[p0] & adj[x]; tri.append((x, y)); seen |= {x, y}
    for T in itertools.combinations(range(len(tri)), bs):
        for pick in itertools.product((0, 1), repeat=bs):
            Qb = [tri[t][s] for t, s in zip(T, pick)]; cand += 1; P = {p0}; ok = True
            for i in range(bs):
                for j in range(i + 1, bs):
                    (x,) = (adj[Qb[i]] & adj[Qb[j]]) - {p0}
                    if x in P or x in adj[p0] or any(x in adj[p] for p in P): ok = False; break
                    P.add(x)
                if not ok: break
            if not ok or len(P) != m: continue
            Q = set()
            for a, b in itertools.combinations(sorted(P), 2): Q |= adj[a] & adj[b]
            if len(Q) != m or Q & P: continue
            if any(len(adj[p] & Q) != bs or (adj[p] & P) for p in P) or any(len(adj[q] & P) != bs or (adj[q] & Q) for q in Q): continue
            phi = [0] * n
            for p in P: phi[p] = 1
            for q in Q: phi[q] = -1
            assert all(sum(phi[w] for w in adj[v]) == ev * phi[v] for v in range(n))
            found.add((frozenset(P), frozenset(Q)))
print("n=%d k=%d block size %d (m=%d): candidates %d; ordered (P,Q) %d; eigenvectors of norm %d up to sign: %d" % (n, k, bs, m, cand, len(found), 2 * m, len({frozenset([c, (c[1], c[0])]) for c in found})))
