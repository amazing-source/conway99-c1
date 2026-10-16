"""Which constraint breaks first when the eighth label {4,t} is forced?  (LAB 16/10/2026)
Base = the four-star block of a seven-label witness (adjacency fixed).  Variables = all pairs touching the eight labels
{4,t}.  Every constraint that involves those variables gets a violation counter (integer slack >= 0):
  C1 (x, r)      x = {4,t}, r = 0..3: |N(x) n L_r| = 2               (slack both ways)
  B1 (x, u)      x, other letter u: |N(x) n L_u n S| <= c(x,u)
  L4 (y)         block label y: |N(y) n L_4| <= c(y,4)
  C2 (a, b)      common neighbours inside S + shared letters + [a ~ b] <= 2, for every pair whose count involves the
                 new variables
CP-SAT minimises the total violation.  The optimum and the list of violated constraints tell where the eighth label
fails.  usage: python r8_soft.py <witness json> <seconds> [--forbid-type T]"""
import itertools
import json
import sys
import time

from ortools.sat.python import cp_model

K = 14
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]


def need(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


w = json.load(open(sys.argv[1]))
secs = float(sys.argv[2])
WL = [frozenset(x) for x in w["labels"]]
WE = set(frozenset((WL[i], WL[j])) for i, j in w["edges"])
B = [l for l in LABELS if l & {0, 1, 2, 3}]
X = [frozenset((4, t)) for t in range(6, 14)]
S = B + X
idx = {l: i for i, l in enumerate(S)}
n = len(S)
m = cp_model.CpModel()
e = {}
for i, j in itertools.combinations(range(n), 2):
    if S[i] in X or S[j] in X:
        e[(i, j)] = e[(j, i)] = m.NewBoolVar("")
    else:
        e[(i, j)] = e[(j, i)] = 1 if frozenset((S[i], S[j])) in WE else 0
viol = []                                     # (name, slack var)


def slack(name, ub=8):
    v = m.NewIntVar(0, ub, name)
    viol.append((name, v))
    return v


for x in X:
    i = idx[x]
    for y in range(K):
        lits = [e[(i, idx[t])] for t in S if y in t and t != x]
        c = need(x, y)
        if y in (0, 1, 2, 3):
            sp, sm = slack("C1 %s r%d +" % (sorted(x), y)), slack("C1 %s r%d -" % (sorted(x), y))
            m.Add(sum(lits) == c + sp - sm)
        else:
            m.Add(sum(lits) <= c + slack("B1 %s u%d" % (sorted(x), y)))
for yl in B:
    i = idx[yl]
    for y in range(K):
        lits = [e[(i, idx[t])] for t in S if y in t and t != yl]
        if not any(not isinstance(z, int) for z in lits):
            continue                                       # untouched by the new variables (base already valid)
        c = need(yl, y)
        if y in (0, 1, 2, 3):
            m.Add(sum(lits) == c)                          # counts towards the stars are fixed by the base
        else:
            m.Add(sum(lits) <= c + slack("L%d %s" % (y, sorted(yl))))
for i, j in itertools.combinations(range(n), 2):
    terms = []
    touched = not isinstance(e[(i, j)], int)
    for t in range(n):
        if t in (i, j):
            continue
        a, b = e[(i, t)], e[(j, t)]
        if isinstance(a, int) and isinstance(b, int):
            terms.append(a * b)
        elif isinstance(a, int):
            touched = True
            terms.append(b if a else 0)
        elif isinstance(b, int):
            touched = True
            terms.append(a if b else 0)
        else:
            touched = True
            p = m.NewBoolVar("")
            m.Add(p >= a + b - 1)
            terms.append(p)
    if not touched:
        continue
    s = len(S[i] & S[j])
    m.Add(sum(terms) + s + e[(i, j)] <= 2 + slack("C2 %s %s" % (sorted(S[i]), sorted(S[j]))))
m.Minimize(sum(v for _, v in viol))
sv = cp_model.CpSolver()
sv.parameters.num_search_workers = 4
sv.parameters.max_time_in_seconds = secs
t0 = time.time()
st = sv.Solve(m)
print("status %s, total violation %s (bound %s), %.1f s" % (sv.StatusName(st), sv.ObjectiveValue() if st in (
    cp_model.OPTIMAL, cp_model.FEASIBLE) else None, sv.BestObjectiveBound(), time.time() - t0), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for name, v in viol:
        if sv.Value(v):
            print("  violated: %s by %d" % (name, sv.Value(v)), flush=True)
