"""B for c = 1, second encoding (exploration, LAB 17/10/2026).
Unknowns: adjacency e between the 44 labels of the four-star block (stars 0..3, K = 14 letters).
  (A) local axioms (cp6, as cp_probe.py);  (B) c(l) = 1 for l = {v,0,1} (letter-graph connectivity, flow);
  (C) N vectors x_1..x_N in ker(8 T_S) over F_p, linearly independent modulo the 4 universal kernel vectors
      chi_0..chi_3 (indicators of the stars; they are in ker T_S by C1):  every x_i vanishes on the 4 coordinates
      {0,4}, {1,4}, {2,4}, {3,4} (where chi_r restricts to the identity), and the x_i have distinct pivots (x_i = 1 at
      its pivot, x_j = 0 there), pivots increasing.
Conway: nu(T_S) >= 14 over Q, hence >= 14 over F_p, i.e. N = 10 must be satisfiable.  Data (c = 1): nu <= 10 (N <= 6).
8 T_S[u][w] = 24 [u = w] - 8 e_uw - 3 |u n w| - m(u, w) + 2  (m = number of mate pairs between the letters of u and w).
usage: python c1_cpsat2.py N p seconds [workers] [--nocon] [--sym]"""
import itertools
import json
import sys
import time

from ortools.sat.python import cp_model

N, p, secs = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
workers = int(sys.argv[4]) if len(sys.argv) > 4 and not sys.argv[4].startswith("--") else 2
K = 14
MATE = lambda i: i ^ 1
stars = [0, 1, 2, 3]
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]
S = [l for l in LABELS if l & set(stars)]
idx = {l: i for i, l in enumerate(S)}
n = len(S)
m = cp_model.CpModel()
e = {}
for i, j in itertools.combinations(range(n), 2):
    e[(i, j)] = e[(j, i)] = m.NewBoolVar("e%d_%d" % (i, j))
for l in S:
    i = idx[l]
    for y in range(K):
        lits = [e[(i, idx[t])] for t in S if y in t and t != l]
        if not lits:
            continue
        c = 1 if (y in l or MATE(y) in l) else 2
        m.Add(sum(lits) == c) if y in stars else m.Add(sum(lits) <= c)
for i, j in itertools.combinations(range(n), 2):
    s = len(S[i] & S[j])
    prods = []
    for t in range(n):
        if t in (i, j):
            continue
        q = m.NewBoolVar("")
        m.AddBoolOr([e[(i, t)].Not(), e[(j, t)].Not(), q])
        m.AddImplication(q, e[(i, t)])
        m.AddImplication(q, e[(j, t)])
        prods.append(q)
    m.Add(sum(prods) + s + e[(i, j)] <= 2)
letters = list(range(2, 14))
if "--nocon" not in sys.argv:
    link = {}
    for a, b in itertools.combinations(letters, 2):
        if b == MATE(a):
            continue
        cands = []
        for (r, s_) in ((0, 0), (1, 1), (0, 1), (1, 0)):
            la, lb = frozenset((r, a)), frozenset((s_, b))
            cands.append(e[(idx[la], idx[lb])])
        z = m.NewBoolVar("")
        m.AddMaxEquality(z, cands)
        link[(a, b)] = link[(b, a)] = z
    flow = {}
    for a in letters:
        for b in letters:
            if a != b:
                f = m.NewIntVar(0, 11, "")
                if b != MATE(a):
                    m.Add(f <= 11 * link[(a, b)])
                flow[(a, b)] = f
    for a in letters:
        out_ = sum(flow[(a, b)] for b in letters if b != a)
        in_ = sum(flow[(b, a)] for b in letters if b != a)
        m.Add(out_ - in_ == 11) if a == 2 else m.Add(in_ - out_ == 1)
# (C) kernel vectors of 8 T_S mod p
def mates(u, w):
    return sum(1 for a in u for b in w if b == MATE(a))
fixed0 = [idx[frozenset((r, 4))] for r in stars]
X = [[m.NewIntVar(0, p - 1, "") for k in range(n)] for i in range(N)]
for i in range(N):
    for k in fixed0:
        m.Add(X[i][k] == 0)
    for u in range(n):
        terms = []
        for w in range(n):
            const = (24 if u == w else 0) - 3 * len(S[u] & S[w]) - mates(S[u], S[w]) + 2
            const %= p
            if const:
                terms.append(const * X[i][w])
            if u != w:
                pr = m.NewIntVar(0, p - 1, "")
                ee = e[(u, w)]
                m.Add(pr == X[i][w]).OnlyEnforceIf(ee)
                m.Add(pr == 0).OnlyEnforceIf(ee.Not())
                terms.append(((-8) % p) * pr)
        kk = m.NewIntVar(0, 2000, "")
        m.Add(sum(terms) == p * kk)
free_cols = [k for k in range(n) if k not in fixed0]
piv = [{k: m.NewBoolVar("") for k in free_cols} for i in range(N)]
pp = []
for i in range(N):
    m.AddExactlyOne(list(piv[i].values()))
    for k in free_cols:
        m.Add(X[i][k] == 1).OnlyEnforceIf(piv[i][k])
        for i2 in range(N):
            if i2 != i:
                m.Add(X[i2][k] == 0).OnlyEnforceIf(piv[i][k])
    q = m.NewIntVar(0, n, "")
    m.Add(q == sum(k * piv[i][k] for k in free_cols))
    pp.append(q)
for i in range(N - 1):
    m.Add(pp[i] < pp[i + 1])
for k in free_cols:
    m.AddAtMostOne([piv[i][k] for i in range(N)])
sv = cp_model.CpSolver()
sv.parameters.num_search_workers = workers
sv.parameters.max_time_in_seconds = secs
t0 = time.time()
st = sv.Solve(m)
print("N=%d p=%d c(l)=1: %s in %.1f s (workers %d)" % (N, p, sv.StatusName(st), time.time() - t0, workers), flush=True)
if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    E = [[i, j] for i, j in itertools.combinations(range(n), 2) if sv.Value(e[(i, j)])]
    fn = "c1_cpsat2_witness_N%d_p%d.json" % (N, p)
    json.dump({"labels": [sorted(l) for l in S], "edges": E}, open(fn, "w"))
    print("witness saved:", fn)
