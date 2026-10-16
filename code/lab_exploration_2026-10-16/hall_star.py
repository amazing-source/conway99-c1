"""Per-star residual b-matching test (exploration, LAB 16/10/2026).
For a four-star block (stars 0..3, K letters, mates 2i/2i+1) and the fifth letter 4: residual R(y) = c(y,4) - |N(y) n C4|
(C4 = {r,4}, r = 0..3).  With all labels {4,u} present (R8 tight), each star L_r must split its residual into |X|
distinct pairs {y, y'}: y, y' in L_r non-adjacent, no block label adjacent to both (cap for a pair sharing the letter r),
every y covered exactly R(y) times.  The test asks, star by star, whether such a b-matching exists (necessary condition
for R8, much weaker than R8).
usage: python hall_star.py <K> <file> [<file> ...]   (json with labels/edges, or jsonl of ext_rate.py records)"""
import itertools
import json
import sys

from ortools.sat.python import cp_model

K = int(sys.argv[1])
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]
B = [l for l in LABELS if l & {0, 1, 2, 3}]


def need(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


def blocks(path):
    if path.endswith(".jsonl"):
        for line in open(path):
            r = json.loads(line)
            if "base_edges" in r:
                yield "%s#%s" % (path.split("\\")[-1].split("/")[-1], r["sample"]), \
                    set(frozenset((frozenset(a), frozenset(b))) for a, b in r["base_edges"])
    else:
        d = json.load(open(path))
        L = [frozenset(x) for x in d["labels"]]
        E = set()
        for i, j in d["edges"]:
            if L[i] & {0, 1, 2, 3} and L[j] & {0, 1, 2, 3}:
                E.add(frozenset((L[i], L[j])))
        yield path.split("\\")[-1].split("/")[-1], E


C4 = [frozenset((r, 4)) for r in range(4)]
nX = K - 6
for path in sys.argv[2:]:
    for name, E in blocks(path):
        adj = {l: set() for l in B}
        for e in E:
            a, b = tuple(e)
            adj[a].add(b)
            adj[b].add(a)
        R = {y: need(y, 4) - len(adj[y] & set(C4)) for y in B}
        res = []
        for r in range(4):
            Lr = [y for y in B if r in y]
            tot = sum(R[y] for y in Lr)
            allowed = []
            for y, z in itertools.combinations(Lr, 2):
                if R[y] < 1 or R[z] < 1 or z in adj[y]:
                    continue
                if adj[y] & adj[z]:
                    continue                      # a block label already is their common neighbour
                allowed.append((y, z))
            m = cp_model.CpModel()
            v = {p: m.NewBoolVar("") for p in allowed}
            for y in Lr:
                m.Add(sum(v[p] for p in allowed if y in p) == R[y])
            sv = cp_model.CpSolver()
            sv.parameters.max_time_in_seconds = 30
            st = sv.StatusName(sv.Solve(m))
            res.append("r%d:%s(R=%d,pairs=%d)" % (r, st[:4], tot, len(allowed)))
        print("%s: %s" % (name, " ".join(res)), flush=True)
