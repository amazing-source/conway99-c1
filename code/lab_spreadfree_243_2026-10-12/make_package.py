"""Lab session, 2026-10-13. Data sheet of the eight known srg(243,22,1,2): for each edge list, an independent check with
Python sets only (degree 22, lambda = 1, mu = 2 pair by pair), sha256, graph6 string (written next to the edge list
for the new graphs), order of Aut and vertex orbits (aut_tools), lines parallel to a line, flat lines, grids per vertex,
prisms. Prints a Markdown table.
python make_package.py <edge files ...>"""
import sys, os, hashlib, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aut_tools as T, trade_bfs as B
n = 243
def graph6(adj):
    bits = []
    for j in range(1, n):
        for i in range(j): bits.append(1 if i in adj[j] else 0)
    while len(bits) % 6: bits.append(0)
    head = chr(126) + chr(63 + (n >> 12)) + chr(63 + ((n >> 6) & 63)) + chr(63 + (n & 63)) if n > 62 else chr(63 + n)
    return head + "".join(chr(63 + int("".join(map(str, bits[k:k + 6])), 2)) for k in range(0, len(bits), 6))
rows = []
for path in sys.argv[1:]:
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]; adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    ok = all(len(a) == 22 for a in adj) and all(len(adj[x] & adj[y]) == (1 if y in adj[x] else 2) for x in range(n) for y in range(x + 1, n))
    A = T.load(path); o, gens, base, sizes = T.aut_group(A); orbs = [len(q) for q in T.vertex_orbits(n, gens)]
    par, grids = B.invariant(A); flat = dict(par).get(20, 0); prisms = sum(c * m for c, m in par) // 2
    name = os.path.basename(path)
    if name.startswith("new243"):
        open(path[:-6] + ".g6", "w", newline="\n").write(graph6(adj) + "\n")
    rows.append((name, ok, o, orbs, ", ".join("%d: %d" % (c, m) for c, m in par), flat, ", ".join("%d: %d" % (g, m) for g, m in grids), prisms, hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]))
print("| file | srg(243,22,1,2), set-based check | Aut | vertex orbits | lines parallel to a line (value: lines) | flat lines | grids per vertex (value: vertices) | prisms | sha256 (first 16) |")
print("|---|---|---|---|---|---|---|---|---|")
for r in rows: print("| %s | %s | %d | %s | %s | %d | %s | %d | %s |" % r)
