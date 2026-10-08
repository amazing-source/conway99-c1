"""C1, lab session, 2026-10-08. The branch (7,3,0) of the family (6,3) on an EDGE-TRANSITIVE srg(v,k,1,2) (bvls243).

  python -I six_three_730.py <edge file> [number of edges tested, default 2]

Signed number of pairs (W, Y): W a 6-set with exactly 7 edges, Y a triangle disjoint from W with no edge to W.
Method: all connected 6-sets with exactly 7 edges through a fixed edge (search of sixsets.py), far triangles of each by
bit masks; total = 2 * (#edges / 7) * sum. Valid only if the graph is edge-transitive; the script tests several edges and
stops if they disagree. One process, memory below 200 MB."""
import sys
E = [tuple(int(x) for x in l.split()[:2]) for l in open(sys.argv[1]) if l.strip()]; n = 1 + max(max(e) for e in E)
mask = [0] * n
for a, b in E: mask[a] |= 1 << b; mask[b] |= 1 << a
pc = lambda x: bin(x).count("1"); k = pc(mask[0]); full = (1 << n) - 1
tris = set()
for a, b in E:
    c = (mask[a] & mask[b]).bit_length() - 1; assert pc(mask[a] & mask[b]) == 1; tris.add(tuple(sorted((a, b, c))))
tm = [(1 << a) | (1 << b) | (1 << c) for a, b, c in sorted(tris)]; assert len(tm) == n * k // 6
res = []
for (a, b) in [E[0], E[len(E) // 2], E[-1]][:int(sys.argv[2]) if len(sys.argv) > 2 else 2]:
    tot = [0, 0]
    def rec(S, Sm, e, ext, forb):
        if len(S) == 6:
            if e == 7:
                blocked = Sm
                for u in S: blocked |= mask[u]
                tot[0] += 1; tot[1] += sum(1 for t in tm if not t & blocked)
            return
        while ext:
            low = ext & -ext; ext ^= low; v = low.bit_length() - 1; e2 = e + pc(mask[v] & Sm)
            if e2 <= 7 and e2 + 3 * (5 - len(S)) >= 7: rec(S + [v], Sm | low, e2, ext | (mask[v] & ~Sm & ~forb & ~low), forb | low)
            forb |= low
    Sm = (1 << a) | (1 << b); rec([a, b], Sm, 1, (mask[a] | mask[b]) & ~Sm, Sm)
    res.append(tuple(tot)); print("edge (%d,%d): 6-sets with 7 edges through it: %d; pairs with a far triangle: %d" % (a, b, tot[0], tot[1]), flush=True)
assert all(r == res[0] for r in res), "edges disagree: not edge-transitive"
assert (len(E) * res[0][1]) % 7 == 0
print("v = %d, k = %d: N(6,7) = %d; six_minus_three_edges7_3_cross0 = %d" % (n, k, len(E) * res[0][0] // 7, 2 * len(E) * res[0][1] // 7))
