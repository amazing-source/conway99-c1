"""Lab session, 2026-10-13. Lower bounds on the largest coclique: tabu search for a coclique of a FIXED size k
(set of k vertices, cost = number of edges inside, swap a conflicting vertex with an outside vertex, best non-tabu
move, random tie-break). Result: a verified coclique of size k, or "not found" (which proves nothing).
python tabu_coclique.py <seconds per size> <first size> <edge file> ...      One process, small memory."""
import sys, time, random
def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]; n = 1 + max(max(e) for e in E)
    adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    return n, adj
def tabu(n, adj, k, seconds, seed):
    rnd = random.Random(seed); S = set(rnd.sample(range(n), k)); cnt = [len(adj[v] & S) for v in range(n)]
    cost = sum(cnt[v] for v in S) // 2; tabu_until = [0] * n; it = 0; t0 = time.time()
    while cost and time.time() - t0 < seconds:
        it += 1; best = None; cands = []
        conf = [u for u in S if cnt[u]]
        outs = [v for v in range(n) if v not in S and tabu_until[v] <= it]
        mo = min(cnt[v] for v in outs); outs = [v for v in outs if cnt[v] <= mo + 1]
        for u in conf:
            for v in outs:
                d = cnt[v] - cnt[u] - (1 if v in adj[u] else 0)
                if best is None or d < best: best = d; cands = [(u, v)]
                elif d == best: cands.append((u, v))
        u, v = rnd.choice(cands)
        S.discard(u); S.add(v)
        for w in adj[u]: cnt[w] -= 1
        for w in adj[v]: cnt[w] += 1
        cost += best; tabu_until[u] = it + 6 + rnd.randrange(6)
    return (S if cost == 0 else None), it
if __name__ == "__main__":
    secs, k0 = float(sys.argv[1]), int(sys.argv[2])
    for path in sys.argv[3:]:
        n, adj = load(path); name = path.replace("\\", "/").split("/")[-1]; k = k0; last = None
        while k <= 45:
            S, it = tabu(n, adj, k, secs, 7 * k)
            if S is None: break
            assert len(S) == k and all(not (adj[a] & S) for a in S); last = k; k += 1
        print("%s: coclique of size %s found; size %d not found in %.0f s (%d moves)" % (name, last, k, secs, it) if k <= 45 else "%s: coclique of size 45 found" % name, flush=True)
