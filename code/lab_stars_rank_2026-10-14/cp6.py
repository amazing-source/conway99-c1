"""CP-SAT model of admissible k-line structures (LAB 16/10/2026), same constraints as stars_rank.build:
  (C1)  |N(l) n L_y| = 1 if y or mate(y) is a letter of l, else 2, for every star letter y;
  (C1') the same count as an upper bound for the non-star letters;
  (C2)  common label neighbours inside S + shared letters + [l ~ l'] <= 2   (lambda = 1, mu = 2 caps).
Optional (env) HREL = "p-q,...": (H-MATCH) matching relations at pairs of star lines (see enum6.py).
Optional (env) GENS = generators as in sym4g.py: invariance of the structure.
Reports FEASIBLE (with one structure saved), INFEASIBLE (exhaustive proof by CP-SAT, no certificate) or UNKNOWN.
usage: python cp6.py <stars> <seconds> <out json>"""
import itertools
import json
import os
import sys
import time

from ortools.sat.python import cp_model

MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(14), 2) if w != MATE(u)]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


def parse(cyc):
    h = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    assert all(h[i ^ 1] == h[i] ^ 1 for i in range(14))
    return h


stars = [int(t) for t in sys.argv[1].split(",")]
secs = float(sys.argv[2])
out = sys.argv[3]
S = [l for l in LABELS if any(y in l for y in stars)]
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
hrel = [tuple(int(t) for t in pq.split("-")) for pq in os.environ.get("HREL", "").split(",") if pq]
nties = 0
for p, q in hrel:
    for a, other in ((p, q), (q, p)):
        a1 = a ^ 1
        o0, o1 = other & ~1, (other & ~1) | 1
        sw = {o0: o1, o1: o0}
        letters = [y for y in range(14) if y not in (a, a1)]
        for y, z in itertools.combinations(letters, 2):
            l1, l2 = frozenset((a, y)), frozenset((a, z))
            m1, m2 = frozenset((a1, sw.get(y, y))), frozenset((a1, sw.get(z, z)))
            if all(t in idx for t in (l1, l2, m1, m2)):
                m.Add(e[(idx[l1], idx[l2])] == e[(idx[m1], idx[m2])])
                nties += 1
gens = [parse(c) for c in os.environ.get("GENS", "").split("|") if c]
for h in gens:
    assert set(h[y] for y in stars) == set(stars)
    for i, j in itertools.combinations(range(n), 2):
        a = idx[frozenset(h[y] for y in S[i])]
        b = idx[frozenset(h[y] for y in S[j])]
        m.Add(e[(i, j)] == e[(a, b)])
base = os.environ.get("BASE", "")
nfix = 0
if base:
    # fix the adjacency among the labels of a given structure (e.g. a four-star germ on stars 0..3)
    bd = json.load(open(base))
    bl = [frozenset(x) for x in bd["labels"]]
    bE = set(tuple(sorted(x)) for x in bd["edges"])
    for a, b in itertools.combinations(range(len(bl)), 2):
        if bl[a] in idx and bl[b] in idx:
            m.Add(e[(idx[bl[a]], idx[bl[b]])] == (1 if (a, b) in bE else 0))
            nfix += 1
# FORCE (env): "a-b:c-d;..." forces the edge {a,b} ~ {c,d}; MATEALIGN (env): star letters whose matching M_a must
# pair every letter b with its mate b^1 (edges {a,b} ~ {a,b^1}).
nforce = 0
for item in [t for t in os.environ.get("FORCE", "").split(";") if t]:
    p, q = item.split(":")
    l1 = frozenset(int(t) for t in p.split("-"))
    l2 = frozenset(int(t) for t in q.split("-"))
    m.Add(e[(idx[l1], idx[l2])] == 1)
    nforce += 1
for a in [int(t) for t in os.environ.get("MATEALIGN", "").split(",") if t]:
    for b in range(14):
        if b in (a, a ^ 1) or b > (b ^ 1):
            continue
        l1, l2 = frozenset((a, b)), frozenset((a, b ^ 1))
        m.Add(e[(idx[l1], idx[l2])] == 1)
        nforce += 1
print("labels %d, HREL %s (%d ties), GENS %s, BASE %s (%d fixed pairs), %d forced edges"
      % (n, hrel, nties, os.environ.get("GENS", ""), base, nfix, nforce), flush=True)
solver = cp_model.CpSolver()
solver.parameters.num_search_workers = 1
solver.parameters.max_time_in_seconds = secs
t0 = time.time()
st = solver.Solve(m)
name = solver.StatusName(st)
res = {"stars": stars, "HREL": hrel, "GENS": os.environ.get("GENS", ""), "status": name, "seconds": time.time() - t0}
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    res["labels"] = [sorted(l) for l in S]
    res["edges"] = [[i, j] for i, j in itertools.combinations(range(n), 2) if solver.Value(e[(i, j)])]
json.dump(res, open(out, "w"))
print("status %s in %.1f s" % (name, res["seconds"]), flush=True)
