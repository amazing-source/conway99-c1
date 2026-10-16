"""Attachment limit for bases with fewer stars (LAB 16/10/2026).
Base = an admissible structure on the stars B (e.g. 0,1 or 0,1,2), drawn with a random objective (cp6 constraints).
Then attach the labels {4,6}, {4,7}, ... one prefix at a time: stars B exact for every label, every other letter as an
upper bound, C2 caps inside the set, base adjacency fixed.  Reports the largest prefix that can be attached.
Also with --plain: no base, find any structure on B plus the prefix (relaxation of the five-star problem when B is a
subset of 0..3).
usage: python attach_limit.py <B, e.g. 0,1,2> <samples> <seconds> <seed> [--plain k]"""
import itertools
import random
import sys
import time

from ortools.sat.python import cp_model

K = 14
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


def build(S, exact):
    idx = {l: i for i, l in enumerate(S)}
    n = len(S)
    m = cp_model.CpModel()
    e = {}
    for i, j in itertools.combinations(range(n), 2):
        e[(i, j)] = e[(j, i)] = m.NewBoolVar("")
    for l in S:
        i = idx[l]
        for y in range(K):
            lits = [e[(i, idx[t])] for t in S if y in t and t != l]
            if not lits:
                continue
            c = count_needed(l, y)
            if y in exact:
                m.Add(sum(lits) == c)
            else:
                m.Add(sum(lits) <= c)
    for i, j in itertools.combinations(range(n), 2):
        s = len(S[i] & S[j])
        prods = []
        for t in range(n):
            if t in (i, j):
                continue
            p = m.NewBoolVar("")
            m.Add(p >= e[(i, t)] + e[(j, t)] - 1)
            prods.append(p)
        m.Add(sum(prods) + s + e[(i, j)] <= 2)
    return m, e, idx


def run(m, secs, first=False, seed=0):
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 1
    sv.parameters.max_time_in_seconds = secs
    if first:
        sv.parameters.stop_after_first_solution = True
    sv.parameters.random_seed = seed
    t0 = time.time()
    st = sv.Solve(m)
    return sv, st, round(time.time() - t0, 1)


B = [int(t) for t in sys.argv[1].split(",")]
nsamp, secs, seed = int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
SB = [l for l in LABELS if any(y in l for y in B)]
X = [frozenset((4, t)) for t in range(6, 14)]
X = [x for x in X if x not in SB]
if "--plain" in sys.argv:
    k = int(sys.argv[sys.argv.index("--plain") + 1])
    m, e, idx = build(SB + X[:k], set(B))
    sv, st, t = run(m, secs)
    print("plain: stars %s + %d labels {4,t}: %s in %.1f s" % (B, k, sv.StatusName(st), t), flush=True)
    sys.exit()
rng = random.Random(seed)
mb, eb, idxb = build(SB, set(B))
pairs = list(itertools.combinations(range(len(SB)), 2))
for s in range(nsamp):
    mb.ClearObjective()
    mb.Maximize(sum(rng.randint(-50, 50) * eb[p] for p in pairs))
    sv, st, t = run(mb, secs, first=True, seed=rng.randint(0, 10 ** 6))
    if sv.StatusName(st) not in ("OPTIMAL", "FEASIBLE"):
        print("sample %d: base %s" % (s, sv.StatusName(st)), flush=True)
        continue
    edges = set(p for p in pairs if sv.Value(eb[p]))
    line = []
    for k in range(1, len(X) + 1):
        S = SB + X[:k]
        m, e, idx = build(S, set(B))
        for a, b in pairs:
            m.Add(e[(idx[SB[a]], idx[SB[b]])] == (1 if (a, b) in edges else 0))
        sv2, st2, t2 = run(m, secs)
        line.append("%d:%s(%.0fs)" % (k, sv2.StatusName(st2)[:4], t2))
        if sv2.StatusName(st2) != "OPTIMAL":
            break
    print("sample %d (base %.0fs): %s" % (s, t, " ".join(line)), flush=True)
