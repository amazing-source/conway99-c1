"""Lab session, 2026-10-13. Test of the conjectures (G), (E), (L), (P) of Codex's notes 176 and 177 on graphs with
lambda = 1, mu = 2 that are NOT 3-fold covers of the Brouwer-Haemers graph (the four srg(243,22,1,2) without regular
spread found on 12-13/10), and re-computation on the four covers as a check of this implementation against note 176.

Definitions (note 176). x a vertex, N(x) its neighbours, a' the mate of a (third vertex of the triangle x a a').
Far vertices of x <-> non-adjacent pairs {a,b} of N(x): z_ab = the common neighbour of a and b other than x.
s_a(z) = third vertex of the triangle on the edge z-a.  F_x = the 2-factor on the far vertices with edges z - s_a(z).
pi_a = perfect matching of N(x) minus {a,a'} with s_a(z_ab) = z_{a,pi_a(b)}; pi_a together with the mate matching
gives alternating cycles carrying l mate pairs each (the type of (x,a)).
  (G) the 4-cycles of F_x are exactly the 3x3 grids through x;   (E) every cycle of F_x is even;
  (L) no l = 2 and no l = 5;                                     (P) every (x,a) has at least one l = 1 (a prism).

python fx_test.py <edge file> [<edge file> ...]        One process, a few seconds per graph, memory small."""
import sys, collections, itertools

def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = 1 + max(max(e) for e in E); adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    return n, adj

def analyse(path):
    n, adj = load(path); k = len(adj[0])
    assert all(len(adj[v]) == k for v in range(n))
    for u in range(n):                                                  # strongly regular with lambda = 1, mu = 2
        for v in range(u + 1, n): assert len(adj[u] & adj[v]) == (1 if v in adj[u] else 2)
    third = {}                                                          # third vertex of the triangle on an edge
    for u in range(n):
        for v in adj[u]: third[(u, v)] = next(iter(adj[u] & adj[v]))
    fx = collections.Counter(); types = collections.Counter(); bad_G = 0; odd = 0; noprism = 0; ngrid_tot = 0
    for x in range(n):
        N = sorted(adj[x]); mate = {a: third[(x, a)] for a in N}
        z = {}
        for a, b in itertools.combinations(N, 2):
            if b == mate[a]: continue
            w = next(iter((adj[a] & adj[b]) - {x})); z[(a, b)] = w; z[(b, a)] = w
        far = sorted(set(z.values())); assert len(far) == k * (k - 2) // 2
        pair_of = {}
        for (a, b), w in z.items():
            if a < b: pair_of[w] = (a, b)
        nb = {w: (third[(w, pair_of[w][0])], third[(w, pair_of[w][1])]) for w in far}      # the two special neighbours
        assert all(u in pair_of for w in far for u in nb[w]) and all(nb[w][0] != nb[w][1] for w in far)
        seen = set(); lens = []
        for w in far:
            if w in seen: continue
            L = 0; prev = None; cur = w
            while True:
                seen.add(cur); L += 1; nxt = nb[cur][0] if nb[cur][0] != prev else nb[cur][1]
                prev, cur = cur, nxt
                if cur == w: break
            lens.append(L)
        grids = 0                                                       # 3x3 grids through x
        lines = sorted({tuple(sorted((a, mate[a]))) for a in N})
        for (a, a2), (b, b2) in itertools.combinations(lines, 2):
            if z[(a, b2)] in adj[z[(a, b)]] and z[(a2, b2)] in adj[z[(a2, b)]] and z[(a2, b)] in adj[z[(a, b)]] and z[(a2, b2)] in adj[z[(a, b2)]]:
                grids += 1
        ngrid_tot += grids
        if lens.count(4) != grids: bad_G += 1
        odd += sum(1 for L in lens if L % 2)
        fx[(tuple(sorted(collections.Counter(lens).items())), grids)] += 1
        for a in N:
            rest = [b for b in N if b != a and b != mate[a]]
            pi = {b: next(c for c in pair_of[third[(z[(a, b)], a)]] if c != a) for b in rest}
            assert all(pi[pi[b]] == b and pi[b] != b for b in rest)
            done = set(); t = []
            for b in rest:
                if b in done: continue
                l = 0; cur = b
                while True:
                    done.add(cur); done.add(mate[cur]); l += 1; cur = pi[mate[cur]]
                    if cur == b: break
                t.append(l)
            t = tuple(sorted(t)); types[t] += 1
            if 1 not in t: noprism += 1
    print("%s: n = %d, k = %d" % (path.replace("\\", "/").split("/")[-1], n, k))
    for (cyc, g), c in sorted(fx.items(), key=lambda kv: -kv[1]):
        print("   F_x: %s   grids through x: %d   (%d vertices)" % (" + ".join("%dx%d" % (m, L) for L, m in cyc), g, c))
    ls = sorted({l for t in types for l in t})
    print("   types of (x,a): %s" % ", ".join("%s (%d)" % (" ".join("%d^%d" % (l, m) for l, m in sorted(collections.Counter(t).items())), c) for t, c in sorted(types.items(), key=lambda kv: -kv[1])))
    print("   values of l present: %s" % ls)
    print("   (G) vertices where #4-cycles != #grids: %d      (E) odd cycles of F_x: %d      (L) l=2 present: %s, l=5 present: %s      (P) pairs (x,a) without prism: %d of %d"
          % (bad_G, odd, 2 in ls, 5 in ls, noprism, n * k), flush=True)

if __name__ == "__main__":
    for p in sys.argv[1:]: analyse(p)
