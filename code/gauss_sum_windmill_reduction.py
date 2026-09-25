"""notes/113 R4 — windmill reduction of the Gauss sum, tested on random instances (general statement first).
Hypotheses: N(x) is a perfect matching of m pairs {a, a'}; every other vertex y has exactly 2 neighbours in N(x)
(Sigma_a l_a = 2|S2|).  Claim:
    sum_{S ⊆ V} (-1)^{|S| + e(S)}  =  2^{m+1} (-1)^m  sum_{S2 ⊆ Γ2} (-1)^{|S2| + e(S2) + sum_c l_a l_a'}   (m odd),
and 0 when m is even; l = parity vector of the N(x)-neighbour counts of S2.  For 99: m = 7 and -2^72 = -2^8 * 2^64.
Negative control: one vertex of Γ2 with 3 neighbours in N(x) must break the identity (checked on the same draws)."""
import random


def total(n, adj):
    tot, e = 0, [0] * (1 << n)
    for S in range(1, 1 << n):
        v = (S & -S).bit_length() - 1
        R = S & (S - 1)
        e[S] = e[R] + bin(adj[v] & R).count("1")
    for S in range(1 << n):
        tot += -1 if (e[S] + bin(S).count("1")) % 2 else 1
    return tot


def build(m, g, rng, bad=False):
    n = 1 + 2 * m + g
    adj = [0] * n
    def edge(u, v):
        adj[u] |= 1 << v; adj[v] |= 1 << u
    for i in range(1, 2 * m + 1):
        edge(0, i)
    for c in range(m):
        edge(1 + 2 * c, 2 + 2 * c)
    nbrs = {}
    for y in range(1 + 2 * m, n):
        k = 3 if (bad and y == n - 1) else 2
        nbrs[y] = rng.sample(range(1, 2 * m + 1), k)
        for a in nbrs[y]:
            edge(y, a)
    for y in range(1 + 2 * m, n):
        for z in range(y + 1, n):
            if rng.random() < 0.4:
                edge(y, z)
    return n, adj, nbrs


def rhs(m, g, n, adj, nbrs):
    G = list(range(1 + 2 * m, n))
    tot = 0
    for mask in range(1 << g):
        S2 = [G[i] for i in range(g) if mask >> i & 1]
        s = 0
        for i, y in enumerate(S2):
            s += 1 + sum(1 for z in S2[i + 1:] if adj[y] >> z & 1)
        l = [0] * (2 * m + 1)
        for y in S2:
            for a in nbrs[y]:
                l[a] ^= 1
        s += sum(l[1 + 2 * c] * l[2 + 2 * c] for c in range(m))
        tot += -1 if s % 2 else 1
    return (2 ** (m + 1) * (-1) ** m * tot) if m % 2 else 0


rng = random.Random(113)
ok = neg_broken = 0
for trial in range(40):
    m, g = rng.choice([(3, 7), (3, 8), (2, 8), (5, 4), (7, 2)])
    n, adj, nb = build(m, g, rng)
    ok += total(n, adj) == rhs(m, g, n, adj, nb)
    n, adj, nb = build(m, g, rng, bad=True)
    neg_broken += total(n, adj) != rhs(m, g, n, adj, nb)
print(f"identity holds on {ok}/40 random instances; negative control (one vertex with 3 neighbours) breaks it on {neg_broken}/40")
assert ok == 40
