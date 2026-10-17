# K7-cover class (graph6 of the 21-vertex form, 14 Gamma vertices + 7 matching vertices) -> unit clauses on base.cnf
import sys, pickle
def g6dec(s):
    s = s.strip(); n = ord(s[0]) - 63; bits = []
    for ch in s[1:]:
        v = ord(ch) - 63; bits += [(v >> (5 - i)) & 1 for i in range(6)]
    adj = [set() for _ in range(n)]; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: adj[i].add(j); adj[j].add(i)
            k += 1
    return n, adj
X = pickle.load(open(sys.argv[1], 'rb')); x = lambda i, j: X[(min(i, j), max(i, j))]
lines = open(sys.argv[2]).read().split(); idx = int(sys.argv[3]); out = sys.argv[4]
n, adj = g6dec(lines[idx])
deg = [len(adj[i]) for i in range(n)]
gv = [i for i in range(n) if deg[i] == 4]; mv = [i for i in range(n) if deg[i] == 2]
assert len(gv) == 14 and len(mv) == 7
lab = {}
for t, m in enumerate(mv):
    p, q = sorted(adj[m]); lab[p] = 22 + 2 * t; lab[q] = 23 + 2 * t
edges = sorted({tuple(sorted((lab[u], lab[v]))) for u in gv for v in adj[u] if v in lab})
assert len(edges) == 21
units = []
for pt, (a, b) in enumerate(edges, start=1):
    for blk in range(22, 36): units.append(x(pt, blk) if blk in (a, b) else -x(pt, blk))
base = open(sys.argv[5]).read().split('\n', 1)
nv, nc = map(int, base[0].split()[2:])
with open(out, 'w') as f:
    f.write(f"p cnf {nv} {nc + len(units)}\n"); f.write(base[1])
    for u in units: f.write(f"{u} 0\n")
print("units", len(units))
