"""Search for HARD c = 1 four-star blocks (exploration, LAB 17/10/2026): positive (T_S, U_S >= 0), c(l) = 1, and NOT
killed by the exact integral lemmas (E3, C2a, RL, C2b of c1_exact_kill.py).  All 1 740 PSD c = 1 sides of our data
are killed; this asks whether positivity survives when the short-vector configurations are forbidden.
Local axioms: the CNF of stars_rank.build (four stars 0..3).  Extra clauses: no rectangle with exactly 3 internal edges
at the roots l = {0,1} and m = {2,3} (Codex's lemma; it is a theorem, so this only removes impossible structures).
Walk: free NFREE labels per move, re-solve with pycryptosat under the remaining assignment, Metropolis on
  score = min(lambda_min T_S, lambda_min U_S) on the complement of the four stars, if c(l) = 1 and the cheap tests
  (E3, forbidden aligned 2-cut, visible norm-14 2-cut vectors) pass; otherwise -9 - (lambda deficit).
Every positive structure that passes the cheap tests is checked with RL (norm-14 lattice) and C2b (balanced 2-cuts);
survivors are saved with their nullity nu(T_S) (Conway needs >= 14).
usage: python c1_hard_walk.py <seed> <seconds> [init json] [NFREE]"""
import itertools
import json
import math
import os
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
from stars_rank import build, kval, LABELS  # noqa: E402
from gg_test import orient, line_graph, components  # noqa: E402
from c1_cutfilter import tests  # noqa: E402
import c1_rlattice as RL  # noqa: E402
from c1_exact_kill import c2b_kills  # noqa: E402

seed, secs = int(sys.argv[1]), float(sys.argv[2])
init = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "-" else None
NFREE = int(sys.argv[4]) if len(sys.argv) > 4 else 4
rng = random.Random(seed)
stars = [0, 1, 2, 3]
S, idx, e, F = build(stars, rng)
n = len(S)
sol = Solver(options={"polar": "rnd", "seed": str(seed)})
for c in F.clauses:
    sol.add_clause(c)
# no rectangle with exactly three internal edges at the two roots
nE3 = 0
CONTROL = "--control" in sys.argv          # control run: no E3 clauses, no penalty, positivity only (c(l) = 1)
for (a0, a1) in (() if CONTROL else ((0, 1), (2, 3))):
    for x in range(0, 14, 2):
        y = x ^ 1
        if {x, y} & {a0, a1}:
            continue
        Q = [idx[frozenset((r, t))] for r in (a0, a1) for t in (x, y)]
        prs = [(Q[i], Q[j]) for i, j in itertools.combinations(range(4), 2)]
        for sub in itertools.combinations(range(6), 3):
            sol.add_clause([-e[prs[k]] if k in sub else e[prs[k]] for k in range(6)])
            nE3 += 1
K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for t in l:
        D[t, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
posL = {l: i for i, l in enumerate(LABELS)}
ix = [posL[l] for l in S]
PiS = Pi[np.ix_(ix, ix)]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T


def perp_min(M):
    ev, V = np.linalg.eigh(Pp @ M @ Pp)
    keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
    return float(ev[keep].min()) if keep else 0.0


def graph_of(model):
    G = np.zeros((n, n), dtype=np.int64)
    for (i, j), v in e.items():
        if i < j and model[v]:
            G[i, j] = G[j, i] = 1
    return G


def evaluate(G):
    edges = [[sorted(S[i]), sorted(S[j])] for i, j in itertools.combinations(range(n), 2) if G[i, j]]
    L, EE = orient(S, edges, 0)
    V, pos, A = line_graph(L, EE)
    if not all(sum(r) == 3 for r in A) or components(A) != 1:
        return -99.0, None
    T = (24 * np.eye(n) - 8 * G - K8) / 8.0
    s = min(perp_min(T), perp_min(7 * PiS - T))
    if CONTROL:
        return s, None
    out, _ = tests(L, EE)
    if out:
        return -9.0 + min(s, 0.0), None
    return s, (L, EE, V, A, T)


ok, model = False, None
if init:
    di = json.load(open(init))
    lab = [frozenset(x) for x in di["labels"]]
    eset = {frozenset((lab[i], lab[j])) for i, j in di["edges"]}
    full = [e[(i, j)] if frozenset((S[i], S[j])) in eset else -e[(i, j)] for i, j in itertools.combinations(range(n), 2)]
    for frac in (1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0):
        part = [x for x in full if rng.random() < frac]
        ok, model = sol.solve(part)
        if ok:
            print("warm start from %s: kept %.0f%% of the pairs" % (init, 100 * frac), flush=True)
            break
else:
    ok, model = sol.solve()
assert ok
cur, info = evaluate(graph_of(model))
temp = float(os.environ.get("TEMP0", "0.2"))
t0 = time.time()
best = cur
nmove = npos = nsurv = 0
while time.time() - t0 < secs:
    nmove += 1
    freed = set(rng.sample(range(n), NFREE))
    assum = [(e[(i, j)] if model[e[(i, j)]] else -e[(i, j)]) for i, j in itertools.combinations(range(n), 2)
             if i not in freed and j not in freed]
    ok2, m2 = sol.solve(assum)
    if not ok2:
        continue
    G = graph_of(m2)
    s2, info2 = evaluate(G)
    if CONTROL and s2 > -1e-9:
        npos += 1
    if s2 > -1e-9 and info2 is not None:
        npos += 1
        L, EE, V, A, T = info2
        o = RL.analyse(L, EE)
        killed_rl = any(k.startswith("killed") for k in o)
        killed_b = (not killed_rl) and c2b_kills(V, A)
        if not killed_rl and not killed_b:
            nsurv += 1
            nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
            fn = os.path.join(HERE, "unbiased_walks", "hard_c1_seed%d_%d.json" % (seed, nsurv))
            json.dump({"labels": [sorted(l) for l in S], "nu": nu,
                       "edges": [[i, j] for i, j in itertools.combinations(range(n), 2) if G[i, j]]}, open(fn, "w"))
            print("move %d: HARD c = 1 PSD block (no exact lemma applies), nu(T_S) = %d, saved %s" % (nmove, nu, fn),
                  flush=True)
        else:
            s2 = -9.0                                  # killed: treat as outside
    if s2 >= cur or rng.random() < math.exp((s2 - cur) / temp):
        model, cur = m2, s2
    if cur > best:
        best = cur
        json.dump({"labels": [sorted(l) for l in S], "score": cur,
                   "edges": [[i, j] for i, j in itertools.combinations(range(n), 2) if graph_of(model)[i, j]]},
                  open(os.path.join(HERE, "unbiased_walks", "hardwalk_best_seed%d%s.json" % (seed, "_control" if CONTROL else "")), "w"))
    temp = max(0.01, temp * 0.999)
    if nmove % 500 == 0:
        print("move %d: score %.4f best %.4f, positive-and-cheap-pass %d, hard survivors %d (%.0f s)" % (
            nmove, cur, best, npos, nsurv, time.time() - t0), flush=True)
print("end: moves %d, best score %.4f, positive passing cheap tests %d, hard survivors %d (E3 clauses %d)" % (
    nmove, best, npos, nsurv, nE3), flush=True)
