"""Lab session, 2026-10-12. Connection sets D_ij of a tri-Cayley graph over Z_3^4 written by tricayley_census.py
(vertex 81 i + index of g in the lexicographic order of F_3^4).   python -I connection_sets.py <edge file>"""
import sys, itertools
H = list(itertools.product(range(3), repeat=4))
E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
adj = [set() for _ in range(243)]
for a, b in E: adj[a].add(b); adj[b].add(a)
for i in range(3):
    for j in range(i, 3):
        D = sorted(H[w - 81 * j] for w in adj[81 * i] if 81 * j <= w < 81 * j + 81)
        if i == j: D = [d for d in D if d < tuple((-x) % 3 for x in d)]
        print("D_%d%d%s = %s" % (i, j, " (up to sign)" if i == j else "", " ".join("".join(map(str, d)) for d in D)))
