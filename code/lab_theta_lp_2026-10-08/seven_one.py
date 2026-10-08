"""C1, lab session, 2026-10-08. Brute force of the family (7,1) on a real srg(v,k,1,2): psi = 1_W - e_y, |W| = 7.

  python -I seven_one.py rook|<edge file>

Signed numbers of pairs (W, y), y outside W:
  edges10_cross0 : e(W) = 10, y has no neighbour in W      (norm 8 in the 99-graph setting)
  edges11_cross1 : e(W) = 11, y has exactly one neighbour  (norm 8)
  edges11_cross0 : e(W) = 11, y has no neighbour           (norm 6)
to be compared with the predictions of Codex's packet (note 184) printed by census_check243.py.
Enumeration: a 7-set with 10 (11) edges has a vertex of degree <= 2 (<= 3), whose removal leaves a 6-set with at least 8
edges; the 6-sets with 8 or 9 edges are exactly: two triangles joined by two edges, a bowtie plus the second common
neighbour of two outer vertices, a house plus the second common neighbour of the apex and a far vertex, and the prisms
(sixsets.py abstract). Every 6-set found is re-checked by its number of edges. One process, memory below 1 GB."""
import sys, itertools


def load(arg):
    if arg == "rook":
        V = [(i, j) for i in range(3) for j in range(3)]; E = [(a, b) for a in range(9) for b in range(a + 1, 9) if (V[a][0] == V[b][0]) != (V[a][1] == V[b][1])]
    else: E = [tuple(int(x) for x in l.split()[:2]) for l in open(arg) if l.strip()]
    n = 1 + max(max(e) for e in E); adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    k = len(adj[0]); assert all(len(s) == k for s in adj)
    for a in range(n):
        for b in range(a + 1, n): assert len(adj[a] & adj[b]) == (1 if b in adj[a] else 2)
    return n, k, E, adj


def main():
    n, k, E, adj = load(sys.argv[1]); mask = [sum(1 << u for u in adj[v]) for v in range(n)]
    pc = lambda x: bin(x).count("1")
    def bits(S):
        b = 0
        for u in S: b |= 1 << u
        return b
    def edges(S): return sum(pc(mask[u] & bits(S)) for u in S) // 2
    third = lambda a, b: next(iter(adj[a] & adj[b]))
    def second(a, b, c):
        (d,) = (adj[a] & adj[b]) - {c}; return d
    tris = sorted({tuple(sorted((a, b, third(a, b)))) for a, b in E})
    six = {}
    # two disjoint triangles with 2 or 3 cross edges (3 = prism)
    for t in tris:
        a, b, c = t
        for x in adj[a] - set(t):
            for y in (adj[x] & adj[b]) - set(t):                         # x ~ a, y ~ b, x ~ y: the triangle on xy
                z = third(x, y)
                if z in t: continue
                S = frozenset(t + (x, y, z)); e = edges(S)
                if len(S) == 6 and e >= 8: six[S] = e
        for x in adj[a] - set(t):
            for y in (adj[x] & adj[c]) - set(t):
                z = third(x, y)
                if z in t: continue
                S = frozenset(t + (x, y, z)); e = edges(S)
                if len(S) == 6 and e >= 8: six[S] = e
        for x in adj[b] - set(t):
            for y in (adj[x] & adj[c]) - set(t):
                z = third(x, y)
                if z in t: continue
                S = frozenset(t + (x, y, z)); e = edges(S)
                if len(S) == 6 and e >= 8: six[S] = e
    lines = [[] for _ in range(n)]
    for t in tris:
        for v in t: lines[v].append(tuple(u for u in t if u != v))
    for v in range(n):                                                   # bowtie + second common neighbour
        for (a, b), (c, d) in itertools.combinations(lines[v], 2):
            for p in (a, b):
                for q in (c, d):
                    S = frozenset((v, a, b, c, d, second(p, q, v))); e = edges(S)
                    if len(S) == 6 and e >= 8: six[S] = e
    for x, y in E:                                                       # house + second common neighbour of apex and far vertex
        z = third(x, y)
        for p in adj[y] - {x, z}:
            q = second(p, x, y)
            for s in (second(z, p, y), second(z, q, x)):
                S = frozenset((x, y, z, p, q, s)); e = edges(S)
                if len(S) == 6 and e >= 8: six[S] = e
    hist = {}
    for e in six.values(): hist[e] = hist.get(e, 0) + 1
    print("v = %d, k = %d: 6-sets with 8 / 9 edges: %s" % (n, k, sorted(hist.items())), flush=True)
    seven = {}
    for S, e in six.items():
        L = sorted(S); sm = bits(L); ge = [0, 0, 0, 0, 0]                # ge[j] = vertices with at least j neighbours in S
        ge[1] = 0
        for u in L: ge[1] |= mask[u]
        for j in (2, 3, 4):
            acc = 0
            for c in itertools.combinations(L, j):
                m = mask[c[0]]
                for u in c[1:]: m &= mask[u]
                acc |= m
            ge[j] = acc
        for j in (1, 2, 3):
            if e + j in (10, 11):
                ex = ge[j] & ~ge[j + 1] & ~sm
                while ex:
                    low = ex & -ex; ex ^= low; seven[sm | low] = e + j
    h7 = {}
    for e in seven.values(): h7[e] = h7.get(e, 0) + 1
    print("7-sets with 10 / 11 edges: %s" % sorted(h7.items()), flush=True)
    c10 = c11_1 = c11_0 = 0
    for sm, e in seven.items():
        L = [i for i in range(n) if sm >> i & 1]; un = 0; dbl = 0
        for u in L: dbl |= un & mask[u]; un |= mask[u]
        far = n - pc(un | sm)
        if e == 10: c10 += far
        else: c11_0 += far; c11_1 += pc(un & ~dbl & ~sm)
    print("signed counts: edges10_cross0 = %d, edges11_cross1 = %d, edges11_cross0 = %d" % (2 * c10, 2 * c11_1, 2 * c11_0), flush=True)


if __name__ == "__main__": main()
