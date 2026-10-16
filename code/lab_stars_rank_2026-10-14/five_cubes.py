"""Cube sampling for the plain five-star question (LAB 16/10/2026): cost estimate, not a proof.
Model = cp6.py on the stars 0..4 (52 labels): C1 exact for 0..4, C1' bounds for the other letters, C2 caps inside S.
A cube fixes the matchings of some stars (M_a = the perfect matching of L_a given by Gamma; C1 exact makes each label of
L_a have exactly one neighbour in L_a).  Cubes are drawn uniformly among LABELLED matchings, so the mean solve time
times the number of labelled cubes divided by the order 3072 of the symmetry group estimates the cost of one cube per
orbit (orbits are mostly free for two or more matchings).
usage: python five_cubes.py <stars to fix, e.g. 4,0> <number of cubes> <seconds per cube> <seed> <out jsonl>"""
import itertools
import json
import random
import sys
import time

from ortools.sat.python import cp_model

MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(14), 2) if w != MATE(u)]
STARS = [0, 1, 2, 3, 4]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


def build():
    S = [l for l in LABELS if any(y in l for y in STARS)]
    idx = {l: i for i, l in enumerate(S)}
    n = len(S)
    m = cp_model.CpModel()
    e = {}
    for i, j in itertools.combinations(range(n), 2):
        e[(i, j)] = e[(j, i)] = m.NewBoolVar("e%d_%d" % (i, j))
    for l in S:
        i = idx[l]
        for y in range(14):
            lits = [e[(i, idx[t])] for t in S if y in t and t != l]
            if not lits:
                continue
            c = count_needed(l, y)
            if y in STARS:
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


def random_matching(items, rng):
    items = list(items)
    rng.shuffle(items)
    return [(items[k], items[k + 1]) for k in range(0, len(items), 2)]


fix = [int(t) for t in sys.argv[1].split(",")]
ncubes, secs, seed, out = int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
rng = random.Random(seed)
t0 = time.time()
m, e, idx = build()
print("model built in %.1f s" % (time.time() - t0), flush=True)
with open(out, "a") as f:
    for c in range(ncubes):
        cube = {}
        assumptions = []
        for a in fix:
            others = [b for b in range(14) if b not in (a, MATE(a))]
            mt = random_matching(others, rng)
            cube[a] = mt
            for b1, b2 in mt:
                assumptions.append(e[(idx[frozenset((a, b1))], idx[frozenset((a, b2))])])
        m.ClearAssumptions()
        m.AddAssumptions(assumptions)
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = secs
        t1 = time.time()
        st = solver.Solve(m)
        rec = {"fix": fix, "seed": seed, "cube": c, "matchings": {str(a): v for a, v in cube.items()},
               "status": solver.StatusName(st), "seconds": round(time.time() - t1, 2)}
        f.write(json.dumps(rec) + "\n")
        f.flush()
        print(c, rec["status"], rec["seconds"], flush=True)
