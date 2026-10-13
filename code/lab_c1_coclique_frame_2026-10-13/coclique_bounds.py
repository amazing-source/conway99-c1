"""Lab session, 2026-10-13. Size of large cocliques in the known srg(243,22,1,2) (sister graphs of the 99-graph).
  (1) lower bound: local search (insertions, (1,2)-swaps, random kicks), fixed seed;
  (2) exact: a coclique of size 45 (Hoffman bound) <=> x in {0,1}^243 with (A + 5I) x = 5.1 ; SAT with the parity
      equations (A + I) x = 1 mod 2 given to the solver as XOR constraints.
python coclique_bounds.py <seconds of local search> <seconds for SAT> <edge file> ...   env PYLIB. One process, < 1 GB."""
import sys, os, time, random
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
from pycryptosat import Solver
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hoffman_cocliques import load, CNF

def local_search(n, adj, seconds, seed):
    rnd = random.Random(seed); S = set(); tight = [0] * n; best = set(); t0 = time.time(); it = 0
    def add(v):
        S.add(v)
        for w in adj[v]: tight[w] += 1
    def rem(v):
        S.discard(v)
        for w in adj[v]: tight[w] -= 1
    def improve():
        changed = True
        while changed:
            changed = False
            free = [v for v in range(n) if v not in S and tight[v] == 0]
            if free: add(rnd.choice(free)); changed = True; continue
            ones = {}
            for v in range(n):
                if v not in S and tight[v] == 1:
                    u = next(w for w in adj[v] if w in S); ones.setdefault(u, []).append(v)
            cands = list(ones.items()); rnd.shuffle(cands)
            for u, L in cands:
                if len(L) < 2: continue
                rnd.shuffle(L); done = False
                for i in range(len(L)):
                    for j in range(i + 1, len(L)):
                        if L[j] not in adj[L[i]]:
                            rem(u); add(L[i]); add(L[j]); changed = True; done = True; break
                    if done: break
                if done: break
    while time.time() - t0 < seconds:
        improve(); it += 1
        if len(S) > len(best): best = set(S)
        for _ in range(rnd.choice((1, 1, 1, 2, 3))):                    # kick: force a random outside vertex in
            v = rnd.choice([u for u in range(n) if u not in S])
            for w in list(adj[v] & S): rem(w)
            add(v)
        if len(S) < len(best) - 4: 
            for v in list(S): rem(v)
            for v in best: add(v)
    assert all(not (adj[a] & best) for a in best)
    return best, it

def exact45(n, adj, E, tl):
    F = CNF(n, tl)
    for a, b in E: F.add([-(a + 1), -(b + 1)])
    for v in range(n):
        r = F.counter([w + 1 for w in sorted(adj[v])], 5)
        F.add([v + 1, r[4]]); F.add([v + 1, -r[5]])
        F.s.add_xor_clause([v + 1] + [w + 1 for w in sorted(adj[v])], True)
    t = time.time(); sat, sol = F.s.solve()
    if sat:
        C = [v for v in range(n) if sol[v + 1]]; assert len(C) == 45 and all(not (adj[a] & set(C)) for a in C)
    return sat, time.time() - t

if __name__ == "__main__":
    ls, tl = float(sys.argv[1]), float(sys.argv[2])
    for path in sys.argv[3:]:
        n, adj, E = load(path); name = path.replace("\\", "/").split("/")[-1]
        best, it = local_search(n, adj, ls, 2026)
        sat, dt = exact45(n, adj, E, tl)
        print("%s: local search finds a coclique of size %d (%d rounds, %.0f s); coclique of size 45: %s (%.1f s)"
              % (name, len(best), it, ls, "YES" if sat else ("NO, proved" if sat is False else "no decision"), dt), flush=True)
