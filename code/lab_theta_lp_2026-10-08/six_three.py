"""C1, lab session, 2026-10-08. Brute force of nine of the ten branches of the family (6,3) on a real srg(v,k,1,2).

  python -I six_three.py rook|<edge file>

psi = 1_W - 1_Y, |W| = 6, |Y| = 3 disjoint. Signed numbers of pairs (W, Y) by (e(W), e(Y), number of edges between):
  (8,3,0) (8,3,1) (8,2,0) (9,3,0) (9,3,1) (9,3,2) (9,2,0) (9,2,1) (9,1,0)
to be compared with the predictions "six_minus_three_edges<e(W)>_<e(Y)>_cross<c>" of Codex's order-9 packet printed by
census_check243.py. The branch (7,3,0) is NOT done here (about 10^7 six-sets with 7 edges in a 243-graph).
Enumeration of the 6-sets with 8 or 9 edges as in seven_one.py (complete list of shapes, each set re-checked).
For a fixed W, with F = vertices with no neighbour in W and N1 = vertices with exactly one:
  triangles outside W are classified by the sum of the numbers of neighbours of their vertices in W;
  induced paths inside F:           sum_{m in F} C(f_m, 2) - 3 t_FFF;
  induced paths with one N1 vertex: sum_{m in N1} C(f_m, 2) + sum_{m in F} n1_m f_m - 3 t_1FF;
  "edge + far vertex" inside F:     sum over edges uv of F of |F| - 2 - |(N(u) + N(v)) cap F| + 2 ... (see code).
One process, memory below 500 MB."""
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
    n, k, E, adj = load(sys.argv[1]); mask = [sum(1 << u for u in adj[v]) for v in range(n)]; pc = lambda x: bin(x).count("1")
    def bits(S):
        b = 0
        for u in S: b |= 1 << u
        return b
    def edges(S): return sum(pc(mask[u] & bits(S)) for u in S) // 2
    third = lambda a, b: next(iter(adj[a] & adj[b]))
    def second(a, b, c):
        (d,) = (adj[a] & adj[b]) - {c}; return d
    tris = sorted({tuple(sorted((a, b, third(a, b)))) for a, b in E}); six = {}
    def put(S):
        S = frozenset(S)
        if len(S) == 6:
            e = edges(S)
            if e >= 8: six[S] = e
    for t in tris:
        for i, j in ((0, 1), (0, 2), (1, 2)):
            for x in adj[t[i]] - set(t):
                for y in (adj[x] & adj[t[j]]) - set(t):
                    z = third(x, y)
                    if z not in t: put(t + (x, y, z))
    lines = [[] for _ in range(n)]
    for t in tris:
        for v in t: lines[v].append(tuple(u for u in t if u != v))
    for v in range(n):
        for (a, b), (c, d) in itertools.combinations(lines[v], 2):
            for p in (a, b):
                for q in (c, d): put((v, a, b, c, d, second(p, q, v)))
    for x, y in E:
        z = third(x, y)
        for p in adj[y] - {x, z}:
            q = second(p, x, y)
            for s in (second(z, p, y), second(z, q, x)): put((x, y, z, p, q, s))
    hist = {}
    for e in six.values(): hist[e] = hist.get(e, 0) + 1
    print("v = %d, k = %d: 6-sets with 8 / 9 edges: %s" % (n, k, sorted(hist.items())), flush=True)
    tot = {}
    def add(key, v):
        tot[key] = tot.get(key, 0) + 2 * v
    for S, e in six.items():
        L = sorted(S); sm = bits(L); un = 0; dbl = 0
        for u in L: dbl |= un & mask[u]; un |= mask[u]
        F = ((1 << n) - 1) & ~un & ~sm; N1 = un & ~dbl & ~sm
        typ = {}                                                         # number of neighbours in W: 0, 1, 2 (2 = at least 2), -1 inside W
        tc = {}
        for t in tris:
            a, b, c = t
            if (sm >> a | sm >> b | sm >> c) & 1: continue
            key = tuple(sorted((0 if F >> u & 1 else 1 if N1 >> u & 1 else 2) for u in t)); tc[key] = tc.get(key, 0) + 1
        t_fff = tc.get((0, 0, 0), 0); t_1ff = tc.get((0, 0, 1), 0)
        add((e, 3, 0), t_fff); add((e, 3, 1), t_1ff)
        if e == 9: add((9, 3, 2), tc.get((0, 1, 1), 0) + tc.get((0, 0, 2), 0))
        pF = 0; p1 = 0; e10 = 0; f = F; nF = pc(F)
        while f:
            low = f & -f; f ^= low; m = low.bit_length() - 1; fm = pc(mask[m] & F); pF += fm * (fm - 1) // 2
            if e == 9:
                p1 += pc(mask[m] & N1) * fm
                g = mask[m] & F & ~(low - 1) & ~low                       # far neighbours u > m: edge m u inside F
                while g:
                    l2 = g & -g; g ^= l2; u = l2.bit_length() - 1
                    e10 += nF - pc((mask[m] | mask[u] | low | l2) & F)   # far vertices adjacent to neither end
        add((e, 2, 0), pF - 3 * t_fff)
        if e == 9:
            g = N1
            while g:
                low = g & -g; g ^= low; fm = pc(mask[low.bit_length() - 1] & F); p1 += fm * (fm - 1) // 2
            add((9, 2, 1), p1 - 3 * t_1ff); add((9, 1, 0), e10)
    for key in sorted(tot): print("  six_minus_three_edges%d_%d_cross%d = %d" % (key + (tot[key],)), flush=True)


if __name__ == "__main__": main()
