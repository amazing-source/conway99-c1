"""In a local neighbourhood (as enum_local.py), tabulate: l-twist (M_1 != h(M_0)), number of missing outer l-transversals,
m-twist, missing outer m-transversals, numerical nullity, PSD."""
import itertools, json, sys, random, time
from collections import Counter
import numpy as np
from pycryptosat import Solver
sys.path.insert(0, '.')
from stars_rank import build, kval, LABELS
start, free_s, maxsec = sys.argv[1], sys.argv[2], float(sys.argv[3])
rng = random.Random(1)
S, idx, e, F = build([0, 1, 2, 3], rng); n = len(S)
sol = Solver()
for c in F.clauses: sol.add_clause(c)
d = json.load(open(start)); E0 = {tuple(x) for x in d["edges"]}
free = {idx[frozenset(int(t) for t in p.split("-"))] for p in free_s.split(",")}
fixed = [(i, j) for i, j in itertools.combinations(range(n), 2) if i not in free and j not in free]
var_pairs = [(i, j) for i, j in itertools.combinations(range(n), 2) if i in free or j in free]
assum = [e[p] if p in E0 else -e[p] for p in fixed]
K = np.array([[kval(a, b) for b in S] for a in S])
L = lambda *x: idx[frozenset(x)]
h = {0: 1, 1: 0, 2: 3, 3: 2}
def matching(G, a):
    others = [y for y in range(14) if y not in (a, a ^ 1)]
    return {frozenset((y, z)) for y in others for z in others if y < z and G[L(a, y), L(a, z)]}
cnt = Counter(); t0 = time.time()
while time.time() - t0 < maxsec:
    ok, model = sol.solve(assum)
    if not ok: print("COMPLETE"); break
    sol.add_clause([-e[p] if model[e[p]] else e[p] for p in var_pairs])
    G = np.zeros((n, n))
    for (i, j), v in e.items():
        if i < j and model[v]: G[i, j] = G[j, i] = 1
    M = [matching(G, a) for a in range(4)]
    tw_l = M[1] != {frozenset(h.get(y, y) for y in p) for p in M[0]}
    tw_m = M[3] != {frozenset(h.get(y, y) for y in p) for p in M[2]}
    ml = sum(1 for y in range(4, 14) if not G[L(0, y), L(1, y)])
    mm = sum(1 for y in range(4, 14) if not G[L(2, y), L(3, y)])
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(3*np.eye(n) - G - K)) < 1e-8))
    cnt[(tw_l, ml, tw_m, mm, nul)] += 1
print("(l-twist, missing outer l-transv, m-twist, missing outer m-transv, nullity): count")
for k, v in sorted(cnt.items()): print("  ", k, v)
