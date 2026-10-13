"""Lab session, 2026-10-13. Strategic test of the coclique frame on the sister graphs.
Codex's current line studies cocliques of size 22 (Hoffman bound) and 21 in a srg(99,14,1,2). It covers C1 only if such
cocliques exist. Here: do the eight known srg(243,22,1,2) have a coclique at their Hoffman bound 45, or one below (44)?
  size 45: C is a coclique of size 45  <=>  every vertex outside C has exactly 5 neighbours in C (exact system, SAT);
  size >= s: coclique with at least s vertices (sequential counter), time limit, answer SAT / UNSAT / no decision.
python hoffman_cocliques.py <seconds per question> <edge file> ...     environment PYLIB.  One process, < 1 GB."""
import sys, os, time
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
from pycryptosat import Solver

def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]; n = 1 + max(max(e) for e in E)
    adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    return n, adj, E

class CNF:
    def __init__(self, n, tl): self.s = Solver(time_limit=tl); self.nv = n
    def new(self): self.nv += 1; return self.nv
    def add(self, c): self.s.add_clause(c)
    def counter(self, lits, kmax):
        """returns r[j] (j = 1..kmax+1) with r[j] true iff at least j of lits are true (both directions)"""
        prev = None
        for x in lits:
            cur = [self.new() for _ in range(kmax + 1)]
            if prev is None:
                self.add([-x, cur[0]]); self.add([x, -cur[0]])
                for j in range(1, kmax + 1): self.add([-cur[j]])
            else:
                for j in range(kmax + 1):
                    lo = prev[j - 1] if j > 0 else None
                    self.add([-prev[j], cur[j]])
                    if lo is None: self.add([-x, cur[j]]); self.add([-cur[j], prev[j], x])
                    else: self.add([-x, -lo, cur[j]]); self.add([-cur[j], prev[j], x]); self.add([-cur[j], prev[j], lo])
            prev = cur
        return prev

def hoffman(n, adj, E, tl, need):
    F = CNF(n, tl)
    for a, b in E: F.add([-(a + 1), -(b + 1)])
    for v in range(n):
        r = F.counter([w + 1 for w in sorted(adj[v])], need)          # r[j-1] <=> at least j neighbours in C
        F.add([v + 1, r[need - 1]]); F.add([v + 1, -r[need]])          # outside C: exactly `need` neighbours in C
    F.add([1])                                                          # vertex 0 in C first; then vertex 0 outside
    t = time.time(); sat, sol = F.s.solve()
    return sat, sol, time.time() - t

def atleast(n, adj, E, tl, size):
    F = CNF(n, tl)
    for a, b in E: F.add([-(a + 1), -(b + 1)])
    r = F.counter(list(range(1, n + 1)), size); F.add([r[size - 1]])
    t = time.time(); sat, sol = F.s.solve()
    return sat, sol, time.time() - t

if __name__ == "__main__":
    tl = float(sys.argv[1])
    for path in sys.argv[2:]:
        n, adj, E = load(path); k = len(adj[0]); name = path.replace("\\", "/").split("/")[-1]
        sat, sol, dt = hoffman(n, adj, E, tl, 5)
        if sat:
            C = [v for v in range(n) if sol[v + 1]]; assert len(C) == 45 and all(not (adj[a] & set(C)) for a in C)
        print("%s: coclique of size 45 through vertex 0: %s (%.1f s)" % (name, "YES" if sat else ("NO" if sat is False else "no decision"), dt), flush=True)
        for size in (44, 43, 42, 41, 40):
            sat, sol, dt = atleast(n, adj, E, tl, size)
            if sat:
                C = [v for v in range(n) if sol[v + 1]]; assert len(C) >= size and all(not (adj[a] & set(C)) for a in C)
            print("   coclique of size >= %d: %s (%.1f s)" % (size, "YES, found one of size %d" % len(C) if sat else ("NO" if sat is False else "no decision"), dt), flush=True)
            if sat: break
