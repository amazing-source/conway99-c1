"""Lab session, 2026-10-12. Looking for the reason why the number of lines parallel to a line is even (observed in
the five graphs). For every line L: the set Par(L) of its parallel lines; for M, M' in Par(L) the number of edges
between M and M' (0..3; 3 = the three lines form a 3x3 grid). Printed: for each j the distribution of the degrees in
the graph "j edges" on Par(L), and whether all degrees have the same parity (a relation whose degrees are all odd
would explain the even size by the handshake lemma).
python -I parallel_parity.py <edge files ...>"""
import sys, collections
def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = 1 + max(max(e) for e in E); adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    return n, adj
for path in sys.argv[1:]:
    n, adj = load(path)
    lines = sorted({tuple(sorted((x, y, next(iter(adj[x] & adj[y]))))) for x in range(n) for y in adj[x] if x < y})
    lineset = {L: set(L) for L in lines}; at = collections.defaultdict(list)
    for L in lines:
        for x in L: at[x].append(L)
    stats = {j: collections.Counter() for j in range(4)}; meet = collections.Counter()
    for L in lines:
        p = L[0]; par = []
        for w in adj[p]:
            if w in L: continue
            for M in at[w]:
                if p not in M and all(len(adj[x] & lineset[M]) == 1 for x in L): par.append(M)
        for M in par:
            deg = [0, 0, 0, 0]; inter = 0
            for M2 in par:
                if M2 == M: continue
                if lineset[M] & lineset[M2]: inter += 1; continue
                deg[sum(len(adj[x] & lineset[M2]) for x in M)] += 1
            for j in range(4): stats[j][deg[j]] += 1
            meet[inter] += 1
    print(path.split("/")[-1])
    print("   parallels of L meeting a given parallel M in a point: %s" % sorted(meet.items()))
    for j in range(4): print("   degrees in the relation '%d edges' among the parallels of a line: %s" % (j, sorted(stats[j].items())))
