"""c = 1 as an exhaustive CP-SAT model (exploration, LAB 17/10/2026).
Unknowns: the adjacency e between the 44 labels of a four-star block (stars 0..3 among K = 14 letters).
Constraints (all NECESSARY in a Conway graph):
  (A) local axioms of cp_probe.py: for each label l and letter y, #neighbours of l among the labels containing y equals
      2 - [y in l] - [y' in l] for the four star letters, and is at most that otherwise; for each pair of labels,
      common label-neighbours + shared letters + [adjacent] <= 2 (lambda = 1, mu = 2 caps);
  (B) c(l) = 1 for l = {v,0,1}: the letter graph on {2..13} with edges mate, {0a}~{0b}, {1a}~{1b}, {0a}~{1b} is
      connected (single-commodity flow from letter 2);
  (C) W' = N(l) u Y (12 letters + the 44 labels) has at least N linearly independent kernel vectors of 3I - A_W' over
      F_p (Conway: mult_3(A_W') >= 56 - 45 = 11 over Q, hence over every F_p).  Independence by a pivot structure.
UNSAT for N <= 11 would exclude every Conway graph with a line of c = 1 (verdict of CP-SAT, not a portable
certificate).  Data (c = 1 sides): nullity over F_5 and F_7 at most 8.
usage: python c1_cpsat.py N p seconds [workers] [--nocon]"""
import itertools
import sys
import time

from ortools.sat.python import cp_model

N, p, secs = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
workers = int(sys.argv[4]) if len(sys.argv) > 4 and not sys.argv[4].startswith("--") else 4
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
# (A) local axioms
for l in S:
    i = idx[l]
    for y in range(K):
        lits = [e[(i, idx[t])] for t in S if y in t and t != l]
        if not lits:
            continue
        c = 1 if (y in l or MATE(y) in l) else 2
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
        q = m.NewBoolVar("")
        m.AddBoolOr([e[(i, t)].Not(), e[(j, t)].Not(), q])
        m.AddImplication(q, e[(i, t)])
        m.AddImplication(q, e[(j, t)])
        prods.append(q)
    m.Add(sum(prods) + s + e[(i, j)] <= 2)
# (B) c(l) = 1: connectivity of the letter graph on {2..13}
letters = list(range(2, 14))
link = {}
for a, b in itertools.combinations(letters, 2):
    if b == MATE(a):
        continue
    cands = []
    for (r, s_) in ((0, 0), (1, 1), (0, 1), (1, 0)):
        la, lb = frozenset((r, a)), frozenset((s_, b))
        if la in idx and lb in idx and la != lb:
            cands.append(e[(idx[la], idx[lb])])
    z = m.NewBoolVar("")
    m.AddMaxEquality(z, cands)
    link[(a, b)] = link[(b, a)] = z
if "--nocon" not in sys.argv:
    flow = {}
    for a in letters:
        for b in letters:
            if a == b:
                continue
            cap = 11
            f = m.NewIntVar(0, cap, "")
            if b == MATE(a):
                pass
            else:
                m.Add(f <= cap * link[(a, b)])
            flow[(a, b)] = f
    root = 2
    for a in letters:
        out_ = sum(flow[(a, b)] for b in letters if b != a)
        in_ = sum(flow[(b, a)] for b in letters if b != a)
        if a == root:
            m.Add(out_ - in_ == len(letters) - 1)
        else:
            m.Add(in_ - out_ == 1)
# (C) N independent kernel vectors of 3I - A_W' over F_p
Wl = [("L", a) for a in letters] + list(S)            # 56 vertices
pos = {v: k for k, v in enumerate(Wl)}
def fixed_nbrs(v):
    if isinstance(v, tuple):
        a = v[1]
        out_ = [("L", MATE(a))] + [l for l in S if a in l]
        return out_
    return [("L", a) for a in v if a in letters]
X = [[m.NewIntVar(0, p - 1, "x%d_%d" % (i, k)) for k in range(56)] for i in range(N)]
for i in range(N):
    for v in Wl:
        k = pos[v]
        terms = [X[i][pos[w]] for w in fixed_nbrs(v)]
        if not isinstance(v, tuple):
            iv = idx[v]
            for w in S:
                if w == v:
                    continue
                pr = m.NewIntVar(0, p - 1, "")
                ee = e[(iv, idx[w])]
                xw = X[i][pos[w]]
                m.Add(pr == xw).OnlyEnforceIf(ee)
                m.Add(pr == 0).OnlyEnforceIf(ee.Not())
                terms.append(pr)
        kk = m.NewIntVar(-60, 60, "")
        m.Add(sum(terms) - 3 * X[i][k] == p * kk)
# independence: vector i has a pivot column piv_i (x = 1 there), pivots distinct, other vectors vanish at it
piv = [[m.NewBoolVar("") for k in range(56)] for i in range(N)]
for i in range(N):
    m.AddExactlyOne(piv[i])
    for k in range(56):
        m.Add(X[i][k] == 1).OnlyEnforceIf(piv[i][k])
        for i2 in range(N):
            if i2 != i:
                m.Add(X[i2][k] == 0).OnlyEnforceIf(piv[i][k])
for k in range(56):
    m.AddAtMostOne([piv[i][k] for i in range(N)])
# symmetry breaking between the N vectors: pivot positions increasing
pp = []
for i in range(N):
    q = m.NewIntVar(0, 55, "")
    m.Add(q == sum(k * piv[i][k] for k in range(56)))
    pp.append(q)
for i in range(N - 1):
    m.Add(pp[i] < pp[i + 1])
sv = cp_model.CpSolver()
sv.parameters.num_search_workers = workers
sv.parameters.max_time_in_seconds = secs
t0 = time.time()
st = sv.Solve(m)
print("N=%d p=%d c(l)=1%s: %s in %.1f s (workers %d)" % (N, p, " (connectivity OFF)" if "--nocon" in sys.argv else "",
                                                      sv.StatusName(st), time.time() - t0, workers), flush=True)
if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    E = [(S[i], S[j]) for i, j in itertools.combinations(range(n), 2) if sv.Value(e[(i, j)])]
    import json
    out = {"labels": [sorted(l) for l in S], "edges": [[idx[a], idx[b]] for a, b in E]}
    fn = "c1_cpsat_witness_N%d_p%d.json" % (N, p)
    json.dump(out, open(fn, "w"))
    print("witness saved:", fn, "edges", len(E))
