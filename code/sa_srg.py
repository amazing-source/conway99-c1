"""Simulated annealing for strongly regular graphs with the Thakkar-Severini score, as a CONTROL experiment:
does the ~70% plateau observed for srg(99,14,1,2) also appear for parameter sets where SRGs exist?

State: a k-regular graph (degree constraints always satisfied).  Moves: degree-preserving double edge swaps.
Score = n (degree constraints) + #{pairs i<j : C_ij = lam if i~j, mu otherwise},  C = A^2, out of n + n(n-1)/2
(for n = 99: 99 + 4851 = 4950, their normalisation).  Energy = number of violated pair constraints.
C is updated incrementally (A' = A +- E  =>  C' = C +- (AE + EA) + E^2) and re-checked from scratch at the end.
Usage: sa_srg.py n k lam mu seconds seed
"""
import sys, time, math, random
import numpy as np
import networkx as nx


class SA:
    def __init__(self, n, k, lam, mu, seed=0):
        self.n, self.k, self.lam, self.mu = n, k, lam, mu
        random.seed(seed)
        G = nx.random_regular_graph(k, n, seed=seed)
        self.adj = [set(G[v]) for v in range(n)]
        A = nx.to_numpy_array(G, dtype=np.int64)
        self.C = (A @ A).astype(np.int64)
        self.edges = [(i, j) for i in range(n) for j in self.adj[i] if i < j]
        self.viol = self.count_viol()

    def bad(self, i, j):
        return self.C[i, j] != (self.lam if j in self.adj[i] else self.mu)

    def count_viol(self):
        return sum(1 for i in range(self.n) for j in range(i + 1, self.n) if self.bad(i, j))

    def toggle(self, a, b, d, touched):
        Na, Nb = list(self.adj[a]), list(self.adj[b])        # old neighbourhoods
        for i in Na:
            self.C[i, b] += d; self.C[b, i] += d
            if i != b:
                touched.add((i, b) if i < b else (b, i))
        for i in Nb:
            self.C[i, a] += d; self.C[a, i] += d
            if i != a:
                touched.add((i, a) if i < a else (a, i))
        self.C[a, a] += 0; self.C[b, b] += 0                  # diagonal not used
        if d > 0:
            self.adj[a].add(b); self.adj[b].add(a)
        else:
            self.adj[a].discard(b); self.adj[b].discard(a)
        touched.add((a, b) if a < b else (b, a))

    def swap(self, a, b, c, d, touched):
        self.toggle(a, b, -1, touched); self.toggle(c, d, -1, touched)
        self.toggle(a, c, +1, touched); self.toggle(b, d, +1, touched)

    def unswap(self, a, b, c, d):
        t = set()
        self.toggle(a, c, -1, t); self.toggle(b, d, -1, t)
        self.toggle(a, b, +1, t); self.toggle(c, d, +1, t)


def run(n, k, lam, mu, seconds, seed, T0=2.0, T1=0.05):
    S = SA(n, k, lam, mu, seed)
    best = S.viol
    t0 = time.time(); it = 0
    edges = S.edges
    while S.viol > 0:
        el = time.time() - t0
        if el > seconds:
            break
        it += 1
        T = T0 * (T1 / T0) ** (el / seconds)
        i1, i2 = random.randrange(len(edges)), random.randrange(len(edges))
        a, b = edges[i1]; c, d = edges[i2]
        if random.random() < 0.5:
            c, d = d, c
        if len({a, b, c, d}) < 4 or c in S.adj[a] or d in S.adj[b]:
            continue
        # old badness on the pairs that can change: collect them with a dry run
        tp = set()
        S.swap(a, b, c, d, tp)
        new_bad = sum(1 for (i, j) in tp if S.bad(i, j))
        S.unswap(a, b, c, d)
        old_bad = sum(1 for (i, j) in tp if S.bad(i, j))
        delta = new_bad - old_bad
        if delta <= 0 or random.random() < math.exp(-delta / T):
            S.swap(a, b, c, d, set())
            edges[i1] = (min(a, c), max(a, c)); edges[i2] = (min(b, d), max(b, d))
            S.viol += delta
            best = min(best, S.viol)
    # exact re-check from scratch
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for j in S.adj[i]:
            A[i, j] = 1
    C = A @ A
    exact = sum(1 for i in range(n) for j in range(i + 1, n)
                if C[i, j] != (lam if A[i, j] else mu))
    assert (A.sum(1) == k).all() and exact == S.viol, (exact, S.viol)
    return it, best, exact, A


if __name__ == '__main__':
    n, k, lam, mu = (int(a) for a in sys.argv[1:5])
    secs = float(sys.argv[5]); seed = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    it, best, exact, A = run(n, k, lam, mu, secs, seed)
    pairs = n * (n - 1) // 2
    total = n + pairs
    print(f'srg({n},{k},{lam},{mu}) seed {seed}: {it} moves; best {best} violated -> score {total - best}/{total} = '
          f'{100 * (total - best) / total:.2f}% (pairs {100 * (pairs - best) / pairs:.2f}%); final {exact}'
          + ('  SOLVED' if exact == 0 else ''), flush=True)
