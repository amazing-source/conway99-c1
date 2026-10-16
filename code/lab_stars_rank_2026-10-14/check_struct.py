"""Independent checker of a k-star structure (labels + edges): C1 exact for the given exact letters, upper bounds for the
other letters, C2 caps (common label neighbours inside the set + shared letters + adjacency <= 2)."""
import itertools, json, sys
d = json.load(open(sys.argv[1]))
exact = [int(t) for t in sys.argv[2].split(",")]
K = d.get("K", 14)
L = [frozenset(x) for x in d["labels"]]
n = len(L)
adj = [[0] * n for _ in range(n)]
for i, j in d["edges"]:
    adj[i][j] = adj[j][i] = 1
mate = lambda y: y ^ 1
need = lambda l, y: 1 if (y in l or mate(y) in l) else 2
bad = []
for i, l in enumerate(L):
    assert adj[i][i] == 0
    for y in range(K):
        cnt = sum(adj[i][j] for j in range(n) if y in L[j] and j != i)
        c = need(l, y)
        if (y in exact and cnt != c) or cnt > c:
            bad.append(("C1", sorted(l), y, cnt, c))
for i, j in itertools.combinations(range(n), 2):
    com = sum(adj[i][t] and adj[j][t] for t in range(n))
    if com + len(L[i] & L[j]) + adj[i][j] > 2:
        bad.append(("C2", sorted(L[i]), sorted(L[j]), com))
print("%d labels, %d edges, exact letters %s: %s" % (n, len(d["edges"]), exact, "OK" if not bad else "VIOLATIONS %d %s" % (len(bad), bad[:3])))
