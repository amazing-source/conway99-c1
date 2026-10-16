"""Minimal core of the attachment failure (LAB 16/10/2026).
Base = one four-star structure from ext_rate.py (stars 0..3); extra = labels {4,t}.  Model of ext_rows.py (stars 0..3
exact, every other letter as an upper bound, C2 caps inside the set).  If infeasible, shrink by deletion: first the
extra labels (dropped from the model), then the base labels (their fixed adjacency released, the label kept).  The result
is a minimal set of extra labels and of base labels whose fixed adjacency already blocks the attachment.
usage: python ext_rows_core.py <jsonl> <sample> <extra t list, e.g. 6,7,8,9,10,11> <seconds> <out json>"""
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


recs = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
rec = [r for r in recs if r["sample"] == int(sys.argv[2]) and "base_edges" in r][0]
extra_t = [int(t) for t in sys.argv[3].split(",")]
secs = float(sys.argv[4])
out = sys.argv[5]
be = set(frozenset((frozenset(a), frozenset(b))) for a, b in rec["base_edges"])
S4 = [l for l in LABELS if any(y in l for y in (0, 1, 2, 3))]


def solve(extra, active):
    S = S4 + [frozenset((4, t)) for t in extra]
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
            if y in (0, 1, 2, 3):
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
    act = set(active)
    for a, b in itertools.combinations(range(len(S4)), 2):
        if a in act and b in act:
            m.Add(e[(idx[S4[a]], idx[S4[b]])] == (1 if frozenset((S4[a], S4[b])) in be else 0))
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 1
    sv.parameters.max_time_in_seconds = secs
    return sv.StatusName(sv.Solve(m))


t0 = time.time()
active = list(range(len(S4)))
st = solve(extra_t, active)
print("start: extra %s -> %s" % (extra_t, st), flush=True)
assert st == "INFEASIBLE"
extra = list(extra_t)
for t in list(extra):
    trial = [x for x in extra if x != t]
    r = solve(trial, active)
    if r == "INFEASIBLE":
        extra = trial
    print("  drop extra 4,%d -> %s (extra %s)" % (t, r, extra), flush=True)
for a in list(active):
    trial = [x for x in active if x != a]
    r = solve(extra, trial)
    if r == "INFEASIBLE":
        active = trial
    print("  release base %s -> %s (core %d)" % (sorted(S4[a]), r, len(active)), flush=True)
core = [S4[a] for a in active]
res = {"sample": rec["sample"], "extra": extra, "core_labels": [sorted(l) for l in core],
       "core_edges": [[sorted(a), sorted(b)] for a, b in itertools.combinations(core, 2) if frozenset((a, b)) in be],
       "seconds": time.time() - t0}
json.dump(res, open(out, "w"), indent=1)
print("minimal: extra %s, %d base labels %s" % (extra, len(core), res["core_labels"]), flush=True)
print("core edges:", res["core_edges"], flush=True)
