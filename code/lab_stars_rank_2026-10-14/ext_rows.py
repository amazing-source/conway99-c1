"""Where does the fifth star break?  (LAB 16/10/2026)
For a four-star base (stars 0..3, adjacency fixed), add only some labels {4,t} (t = 6..13) and ask CP-SAT whether they
can be attached: constraints of cp6.py on the label set S4 u extra, stars 0..3 exact, every other letter (4 included) as
an upper bound, C2 caps inside the set.  Then the full fifth star (letter 4 exact).  Reports, for each prefix size k,
the status for the first k labels {4,6}, ..., {4,5+k}.
usage: python ext_rows.py <jsonl from ext_rate.py> <seconds> [max samples]"""
import itertools
import json
import sys
import time

from ortools.sat.python import cp_model

K = 14
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


def solve(S, exact, base_edges, secs):
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
    S4 = [l for l in S if any(y in l for y in (0, 1, 2, 3))]
    for a, b in itertools.combinations(S4, 2):
        m.Add(e[(idx[a], idx[b])] == (1 if frozenset((a, b)) in base_edges else 0))
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 1
    sv.parameters.max_time_in_seconds = secs
    t0 = time.time()
    return sv.StatusName(sv.Solve(m)), round(time.time() - t0, 1)


recs = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
secs = float(sys.argv[2])
nmax = int(sys.argv[3]) if len(sys.argv) > 3 else len(recs)
S4 = [l for l in LABELS if any(y in l for y in (0, 1, 2, 3))]
X = [frozenset((4, t)) for t in range(6, 14)]
for r in recs[:nmax]:
    if "base_edges" not in r:
        continue
    be = set(frozenset((frozenset(a), frozenset(b))) for a, b in r["base_edges"])
    line = []
    for k in range(1, 9):
        st, t = solve(S4 + X[:k], {0, 1, 2, 3}, be, secs)
        line.append("%d:%s(%.0fs)" % (k, st[:4], t))
        if st == "INFEASIBLE":
            break
    else:
        st, t = solve(S4 + X, {0, 1, 2, 3, 4}, be, secs)
        line.append("full:%s(%.0fs)" % (st[:4], t))
    print("sample %s: %s" % (r["sample"], " ".join(line)), flush=True)
