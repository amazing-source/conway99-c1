"""Zero forcing upper bounds for the four-star ball Omega (59 vertices).  For any symmetric matrix with off-diagonal
pattern = the graph Omega, nullity <= Z(Omega).  A_Omega - 3I has this pattern, so mult_3(A_Omega) <= Z(Omega);
Conway needs mult_3 >= 14.  Greedy randomized search for small forcing sets."""
import itertools, json, sys, random
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, rank_mod, relabel, gl_connected, build_H

def closure(adj, black):
    black = set(black)
    changed = True
    while changed:
        changed = False
        for u in list(black):
            white = [w for w in adj[u] if w not in black]
            if len(white) == 1:
                black.add(white[0]); changed = True
    return black

def greedy_Z(adj, n, rng, tries=60):
    best = n
    for t in range(tries):
        black = set()
        cl = closure(adj, black)
        order = list(range(n)); rng.shuffle(order)
        while len(cl) < n:
            # pick the vertex whose addition maximises the closure (sampled)
            cand = [v for v in order if v not in cl]
            rng.shuffle(cand)
            bestv, bestsz = None, -1
            for v in cand[:25]:
                sz = len(closure(adj, cl | {v}))
                if sz > bestsz:
                    bestv, bestsz = v, sz
            black.add(bestv)
            cl = closure(adj, cl | {bestv})
        # prune redundant
        for v in sorted(black, key=lambda _: rng.random()):
            if len(closure(adj, black - {v})) == n:
                black.discard(v)
        best = min(best, len(black))
    return best

def ball_adj(EE):
    V, A = build_H(EE, with_l=True)
    n = len(V)
    adj = [[j for j in range(n) if A[i, j]] for i in range(n)]
    m3 = n - rank_mod((A - 3 * np.eye(n, dtype=np.int64)).tolist(), 1000000007)
    return adj, n, m3

rng = random.Random(1)
mode = sys.argv[1]
tab = Counter()
if mode == "rank30":
    d = json.load(open(sys.argv[2]))
    lab = [frozenset(x) for x in d["labels"]]
    for s in d["structures"][: int(sys.argv[3])]:
        EE = {frozenset((lab[i], lab[j])) for i, j in s["edges"]}
        adj, n, m3 = ball_adj(EE)
        tab[(m3, greedy_Z(adj, n, rng))] += 1
    print("rank-30 objects (c >= 2): (mult_3(A_Omega), greedy upper bound on Z(Omega)) : count")
else:
    k = 0
    for line in open(sys.argv[2]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S0 = [frozenset(x) for x in d["labels"]]
        E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
        for side in (0, 1):
            L, EE = relabel(S0, E0, side)
            conn, degok = gl_connected(EE)
            if not (conn and degok):
                continue
            adj, n, m3 = ball_adj(EE)
            tab[(m3, greedy_Z(adj, n, rng))] += 1
            k += 1
        if k >= int(sys.argv[3]):
            break
    print("c(l)=1 sides: (mult_3(A_Omega), greedy upper bound on Z(Omega)) : count")
for key, c in sorted(tab.items()):
    print("   ", key, c)
