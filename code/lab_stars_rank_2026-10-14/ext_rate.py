"""Extension rate of random four-star structures to a fifth star (LAB 16/10/2026).
For a root with K letters (K = 14 Conway, K = 22 srg(243,22,1,2)): draw admissible four-star structures (stars 0..3;
constraints of cp6.py: C1 exact for the stars, C1' bounds for the other letters, C2 caps) with a random linear objective
(first solution only), then ask whether the structure extends to the five stars 0..4 under the same constraints.
Prints one line per sample: four-star status, extension status, times.  A FEASIBLE extension at K = 14 would be the first
admissible five-star structure; it is saved.
usage: python ext_rate.py <K> <samples> <seconds per solve> <seed> <out jsonl>"""
import itertools
import json
import random
import sys
import time

from ortools.sat.python import cp_model

K, nsamp, secs, seed, out = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


def model(stars):
    S = [l for l in LABELS if any(y in l for y in stars)]
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
            if y in stars:
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
    return m, e, S, idx


rng = random.Random(seed)
m4, e4, S4, idx4 = model([0, 1, 2, 3])
m5, e5, S5, idx5 = model([0, 1, 2, 3, 4])
pairs4 = list(itertools.combinations(range(len(S4)), 2))
with open(out, "a") as f:
    for s in range(nsamp):
        m4.ClearObjective()
        m4.Maximize(sum(rng.randint(-50, 50) * e4[p] for p in pairs4))
        sv = cp_model.CpSolver()
        sv.parameters.num_search_workers = 1
        sv.parameters.max_time_in_seconds = secs
        sv.parameters.stop_after_first_solution = True
        sv.parameters.random_seed = rng.randint(0, 10 ** 6)
        t0 = time.time()
        st = sv.Solve(m4)
        rec = {"K": K, "seed": seed, "sample": s, "four": sv.StatusName(st), "t4": round(time.time() - t0, 1)}
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            edges = [p for p in pairs4 if sv.Value(e4[p])]
            eset = set(edges)
            m5.ClearAssumptions()
            lits = []
            for a, b in pairs4:
                v = e5[(idx5[S4[a]], idx5[S4[b]])]
                lits.append(v if (a, b) in eset else v.Not())
            m5.AddAssumptions(lits)
            sv5 = cp_model.CpSolver()
            sv5.parameters.num_search_workers = 1
            sv5.parameters.max_time_in_seconds = secs
            t1 = time.time()
            st5 = sv5.Solve(m5)
            rec["five"] = sv5.StatusName(st5)
            rec["t5"] = round(time.time() - t1, 1)
            rec["base_edges"] = [[sorted(S4[a]), sorted(S4[b])] for a, b in edges]
            if st5 in (cp_model.OPTIMAL, cp_model.FEASIBLE) and K == 14:
                rec["five_edges"] = [[sorted(S5[a]), sorted(S5[b])] for a, b in itertools.combinations(range(len(S5)), 2)
                                     if sv5.Value(e5[(a, b)])]
        f.write(json.dumps(rec) + "\n")
        f.flush()
        print(s, rec["four"], rec["t4"], rec.get("five"), rec.get("t5"), flush=True)
