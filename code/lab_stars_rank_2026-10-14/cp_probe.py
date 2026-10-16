"""Why is the five-star search slow where a solution exists?  (LAB 16/10/2026)
Same model as cp_generic.py (cp6 constraints for a root with K letters), with solver variants:
  --lin L        linearization_level (CP-SAT default 1)
  --sym S        symmetry_level (default 2)
  --order base|x|none   decision strategy: branch first on the pairs inside the stars 0..3 (base), or first on the pairs
                 touching the labels {4,t} of the fifth star (x)
  --workers W    number of workers (default 1)
  --seed R       random seed
  --log          print the CP-SAT search log
Prints status, wall time, conflicts, branches, and the presolved model size.
usage: python cp_probe.py <K> <stars> <seconds> [options]"""
import itertools
import sys
import time

from ortools.sat.python import cp_model


def opt(name, default, cast=str):
    return cast(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


K = int(sys.argv[1])
stars = [int(t) for t in sys.argv[2].split(",")]
secs = float(sys.argv[3])
lin, sym, order = opt("--lin", None, int), opt("--sym", None, int), opt("--order", "none")
workers, seed = opt("--workers", 1, int), opt("--seed", 0, int)
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]


def count_needed(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


S = [l for l in LABELS if any(y in l for y in stars)]
xk = opt("--xk", None, int)
if xk is not None:
    # partial fifth star: the stars given are exact, plus the first xk labels {4,6}, {4,7}, ... (letter 4 only bounded)
    S = S + [frozenset((4, t)) for t in range(6, K) if frozenset((4, t)) not in S][:xk]
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
        if "--reify" in sys.argv:
            # p is exactly the product: p <= e_it, p <= e_jt (the aux variable stops being a free slack)
            m.AddImplication(p, e[(i, t)])
            m.AddImplication(p, e[(j, t)])
        prods.append(p)
    m.Add(sum(prods) + s + e[(i, j)] <= 2)
last = max(stars) if xk is None else None
inner = [l for l in S if any(y in l for y in stars if y != last)]
inner_set = set(inner)
pairs = list(itertools.combinations(range(n), 2))
base_vars = [e[p] for p in pairs if S[p[0]] in inner_set and S[p[1]] in inner_set]
x_vars = [e[p] for p in pairs if not (S[p[0]] in inner_set and S[p[1]] in inner_set)]
vsel = cp_model.SELECT_MIN_VALUE if opt("--vsel", "max") == "min" else cp_model.SELECT_MAX_VALUE
if order == "base":
    m.AddDecisionStrategy(base_vars, cp_model.CHOOSE_FIRST, vsel)
elif order == "x":
    m.AddDecisionStrategy(x_vars, cp_model.CHOOSE_FIRST, vsel)
elif order == "all":
    # every edge variable, base first then the fifth-star pairs; the aux products are never decided directly
    m.AddDecisionStrategy(base_vars + x_vars, cp_model.CHOOSE_FIRST, vsel)
sv = cp_model.CpSolver()
sv.parameters.num_search_workers = workers
sv.parameters.max_time_in_seconds = secs
sv.parameters.random_seed = seed
if lin is not None:
    sv.parameters.linearization_level = lin
if sym is not None:
    sv.parameters.symmetry_level = sym
if order != "none":
    sv.parameters.search_branching = cp_model.FIXED_SEARCH if workers == 1 else cp_model.AUTOMATIC_SEARCH
if "--log" in sys.argv:
    sv.parameters.log_search_progress = True
t0 = time.time()
st = sv.Solve(m)
print("K=%d stars=%s labels=%d lin=%s sym=%s order=%s workers=%d seed=%d: %s in %.1f s, conflicts %d, branches %d"
      % (K, stars, n, lin, sym, order, workers, seed, sv.StatusName(st), time.time() - t0, sv.NumConflicts(),
         sv.NumBranches()), flush=True)
