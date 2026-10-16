"""Sharing-graph count of a four-star block (exploration, LAB 16/10/2026).
In R8 (all labels {4,u} present) every block label y has exactly R(y) = c(y,4) - |N(y) n C4| neighbours in X.  Two labels
of X share at most one block neighbour (none if adjacent), so the block labels with R(y) = 2 give distinct pairs of X:
    beta = #{y in B : R(y) = 2} <= C(|X|, 2) - a,    a = number of edges inside X.
beta depends only on the block.  Prints beta, the per-star counts t_r = #{y in L_r : R(y) = 2}, and C(|X|, 2).
usage: python sharing.py <K> <file> [...]"""
import itertools
import json
import sys

K = int(sys.argv[1])
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]
B = [l for l in LABELS if l & {0, 1, 2, 3}]
C4 = set(frozenset((r, 4)) for r in range(4))
need = lambda l, y: 1 if (y in l or MATE(y) in l) else 2


def blocks(path):
    if path.endswith(".jsonl"):
        for line in open(path):
            r = json.loads(line)
            if "base_edges" in r:
                yield "%s#%s" % (path.replace("\\", "/").split("/")[-1], r["sample"]), \
                    set(frozenset((frozenset(a), frozenset(b))) for a, b in r["base_edges"])
    else:
        d = json.load(open(path))
        L = [frozenset(x) for x in d["labels"]]
        yield path.replace("\\", "/").split("/")[-1], set(
            frozenset((L[i], L[j])) for i, j in d["edges"] if L[i] & {0, 1, 2, 3} and L[j] & {0, 1, 2, 3})


nx = K - 6
for path in sys.argv[2:]:
    for name, E in blocks(path):
        adj = {l: set() for l in B}
        for e in E:
            a, b = tuple(e)
            adj[a].add(b)
            adj[b].add(a)
        R = {y: need(y, 4) - len(adj[y] & C4) for y in B}
        beta = sum(1 for y in B if R[y] == 2)
        t = [sum(1 for y in B if r in y and R[y] == 2) for r in range(4)]
        c4c4 = sum(1 for a, b in itertools.combinations(sorted(C4, key=sorted), 2) if b in adj[a])
        print("%s: beta %d (t_r %s), C(|X|,2) = %d, corner-corner edges %d" % (name, beta, t, nx * (nx - 1) // 2, c4c4))
