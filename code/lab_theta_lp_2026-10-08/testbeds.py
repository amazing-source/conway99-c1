"""C1, lab session, 2026-10-08. Brute-force counts on REAL graphs with lambda = 1, mu = 2, to test the census formulas.

  python -I testbeds.py rook|<edge file> [f8]

Counts (pure subgraph counts, valid for any srg(v,k,1,2); the collision theory itself does not transfer to the test beds,
whose positive eigenvalue is not 3):
  T, P (prisms), distribution of P_T, rho (induced 3 x 3 grids), H (copies of D: a bowtie v; ab; cd plus x ~ a,c and
  y ~ b,d with x ~ y), pi (adjacent pairs of second common neighbours sharing an outer vertex; expected 6 P),
  BF = signed number of (bowtie, far edge), HF = signed number of (house, far edge),
  and with the option f8 (needs numpy): F8 = number of ordered pairs of disjoint anticomplete 4-sets with 4 edges each.
Hand formula tested here (NOTE.md 17.13): BF = B [(v - 5k + 11)(k - 10) + 4 (k - 6)] + 12 P + 2 H, B = v C(k/2, 2).
One process; memory below 200 MB (f8: about 10 MB of numpy arrays)."""
import sys, itertools
from math import comb


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
    n, k, E, adj = load(sys.argv[1]); mask = [sum(1 << u for u in adj[v]) for v in range(n)]; full = (1 << n) - 1
    bits = lambda S: sum(1 << u for u in S)
    third = lambda a, b: next(iter(adj[a] & adj[b]))                      # a ~ b
    def second(a, b, c):                                                  # a not~ b, c one common neighbour: the other
        (d,) = (adj[a] & adj[b]) - {c}; return d
    tris = sorted({tuple(sorted((a, b, third(a, b)))) for a, b in E}); T = len(tris); assert T == n * k // 6
    # prisms and grids
    prisms = set(); PT = {t: 0 for t in tris}
    for t in tris:
        a, b, c = t
        for x in adj[a] - set(t):
            for y in (adj[x] & adj[b]) - set(t):
                for z in adj[x] & adj[y] & adj[c]: prisms.add(frozenset(t + (x, y, z))); PT[t] += 1
    P = len(prisms); assert sum(PT.values()) == 2 * P
    grids = set()
    for pr in prisms:
        tr = [t for t in tris if set(t) <= pr]; assert len(tr) == 2
        t1, t2 = tr; xs = []
        for a in t1:
            (b,) = adj[a] & set(t2); xs.append(third(a, b))
        if len(set(xs)) == 3 and xs[1] in adj[xs[0]] and xs[2] in adj[xs[0]] and xs[2] in adj[xs[1]]: grids.add(frozenset(pr | set(xs)))
    dist = {}
    for v_ in PT.values(): dist[v_] = dist.get(v_, 0) + 1
    print("v = %d, k = %d: T = %d, P = %d (P_T distribution %s), grids rho = %d" % (n, k, T, P, sorted(dist.items()), len(grids)), flush=True)
    # bowties: H, pi, far edges
    lines = [[] for _ in range(n)]
    for t in tris:
        for v in t: lines[v].append(tuple(u for u in t if u != v))
    H = PI = BF = 0; nb = 0
    def far_edges(S):
        blocked = bits(S)
        for u in S: blocked |= mask[u]
        far = full & ~blocked; tot = 0; f = far
        while f:
            low = f & -f; f ^= low; tot += bin(mask[low.bit_length() - 1] & far).count("1")
        return tot // 2
    for v in range(n):
        for (a, b), (c, d) in itertools.combinations(lines[v], 2):
            nb += 1; w = {(p, q): second(p, q, v) for p in (a, b) for q in (c, d)}
            H += (w[(b, d)] in adj[w[(a, c)]]) + (w[(b, c)] in adj[w[(a, d)]])
            PI += (w[(a, d)] in adj[w[(a, c)]]) + (w[(b, d)] in adj[w[(b, c)]]) + (w[(b, c)] in adj[w[(a, c)]]) + (w[(b, d)] in adj[w[(a, d)]])
            BF += 2 * far_edges((v, a, b, c, d))
    assert nb == n * comb(k // 2, 2)
    pred = nb * ((n - 5 * k + 11) * (k - 10) + 4 * (k - 6)) + 12 * P + 2 * H
    print("bowties %d: H = %d, pi = %d (6P = %d); BF = %d; hand formula %d  %s" % (nb, H, PI, 6 * P, BF, pred, "OK" if pred == BF and PI == 6 * P else "MISMATCH"), flush=True)
    # houses
    HF = 0; nh = 0; inprism = 0
    for x, y in E:
        z = third(x, y)
        for p in adj[y] - {x, z}:
            q = second(p, x, y); nh += 1; HF += 2 * far_edges((x, y, z, p, q))
    assert nh == len(E) * (k - 2)
    print("houses %d: HF = %d; BF + HF = %d" % (nh, HF, BF + HF), flush=True)
    if "f8" in sys.argv[2:]:
        import numpy as np
        sets4 = set()
        for t in tris:
            for u in t:
                for w in adj[u] - set(t): sets4.add(frozenset(t + (w,)))
        for a in range(n):
            for b in range(a + 1, n):
                if b not in adj[a]: c, d = sorted(adj[a] & adj[b]); sets4.add(frozenset((a, b, c, d)))
        S4 = sorted(tuple(sorted(s)) for s in sets4); m = len(S4); W = (n + 63) // 64
        def words(x): return [(x >> (64 * i)) & ((1 << 64) - 1) for i in range(W)]
        own = np.array([words(bits(s)) for s in S4], dtype=np.uint64); blk = []
        for s in S4:
            b_ = bits(s)
            for u in s: b_ |= mask[u]
            blk.append(words(b_))
        blk = np.array(blk, dtype=np.uint64); tot = 0
        for i in range(m):
            hit = own[:, 0] & blk[i, 0]
            for j in range(1, W): hit |= own[:, j] & blk[i, j]
            tot += int(np.count_nonzero(hit == 0))
        print("4-sets with 4 edges: %d; F8 (ordered far pairs) = %d" % (m, tot), flush=True)


if __name__ == "__main__": main()
