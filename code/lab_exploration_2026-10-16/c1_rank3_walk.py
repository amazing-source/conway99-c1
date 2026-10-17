"""[MAXNU variant: set MAXNU=1 to MAXIMISE nu(T_S) over lemma-free (E3 clauses + C2a cut test) c(l)=1 structures]
Adversarial walk for the mod-3 statement (exploration, LAB 17/10/2026):
In Conway every induced subgraph H has rank_F3(A_H) <= 45 (it is a principal submatrix of A - 3I = A mod 3, whose rank
over Q is 45).  For the four-star ball Omega (59 vertices: l, N(l), the 20 far labels of m) of a c(l) = 1 line, ALL 1 884
c = 1 sides of our data have rank_F3(A_Omega) in [47, 55].  This walk tries to BREAK that: it minimises rank_F3(A_Omega)
over c(l) = 1 four-star structures (local axioms = CNF of stars_rank.build; optional E3 clauses), no positivity asked.
usage: python c1_rank3_walk.py <seed> <seconds> [NFREE] [--e3]"""
import itertools, json, math, os, random, sys, time
import numpy as np
from pycryptosat import Solver
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
from stars_rank import build, kval, LABELS  # noqa: E402
from c1_margin56 import rank_mod, build_H, gl_connected  # noqa: E402

seed, secs = int(sys.argv[1]), float(sys.argv[2])
NFREE = int(sys.argv[3]) if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else 4
TEMP0 = float(os.environ.get("TEMP0", "0.6"))
E3 = "--e3" in sys.argv
rng = random.Random(seed)
S, idx, e, F = build([0, 1, 2, 3], rng)
n = len(S)
sol = Solver(options={"polar": "rnd", "seed": str(seed)})
for c in F.clauses:
    sol.add_clause(c)
if E3:
    for (a0, a1) in ((0, 1), (2, 3)):
        for x in range(0, 14, 2):
            y = x ^ 1
            if {x, y} & {a0, a1}:
                continue
            Q = [idx[frozenset((r, t))] for r in (a0, a1) for t in (x, y)]
            prs = [(Q[i], Q[j]) for i, j in itertools.combinations(range(4), 2)]
            for sub in itertools.combinations(range(6), 3):
                sol.add_clause([-e[prs[k]] if k in sub else e[prs[k]] for k in range(6)])
SYM = "--sym" in sys.argv
TAU = "--tau" in sys.argv
MAXNU = os.environ.get("MAXNU") == "1"
if TAU:      # force the (0 1)(2 3) symmetry
    swapt = {0: 1, 1: 0, 2: 3, 3: 2}
    ft = lambda l: frozenset(swapt.get(x, x) for x in l)
    for (i, j), v in e.items():
        if i < j:
            a, b = idx[ft(S[i])], idx[ft(S[j])]
            w = e[(min(a, b), max(a, b))]
            if w != v:
                sol.add_clause([v, -w]); sol.add_clause([-v, w])
if SYM:      # force the (0 2)(1 3) symmetry exchanging l and m
    swap = {0: 2, 2: 0, 1: 3, 3: 1}
    f = lambda l: frozenset(swap.get(x, x) for x in l)
    for (i, j), v in e.items():
        if i < j:
            a, b = idx[f(S[i])], idx[f(S[j])]
            w = e[(min(a, b), max(a, b))]
            if w != v:
                sol.add_clause([v, -w]); sol.add_clause([-v, w])
K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)


from c1_cutfilter import tests as _cut_tests  # noqa: E402
from gg_test import orient as _orient  # noqa: E402
POS = {l: i for i, l in enumerate(S)}


def evaluate(model):
    EE = {frozenset((S[i], S[j])) for (i, j), v in e.items() if i < j and model[v]}
    conn, degok = gl_connected(EE)
    if not (conn and degok):
        return None
    if MAXNU:
        Lo, EEo = _orient(S, [(tuple(a), tuple(b)) for a, b in (tuple(x) for x in EE)], 0)
        out, _ = _cut_tests(Lo, EEo)
        if out:
            return None
        G = np.zeros((n, n), dtype=np.int64)
        for a, b in (tuple(x) for x in EE):
            G[POS[a], POS[b]] = G[POS[b], POS[a]] = 1
        T8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
        nu = n - rank_mod(T8.tolist(), 1000000007)
        return 100 - nu, EE                        # minimise 100 - nu  <=>  maximise nu
    V9, A9 = build_H(EE, with_l=True)
    r3 = rank_mod(A9.tolist(), 3)
    return r3, EE


INIT = sys.argv[sys.argv.index("--init") + 1] if "--init" in sys.argv else None
ok, model = sol.solve()
assert ok
if INIT:
    di = json.load(open(INIT))
    lab = [frozenset(x) for x in di["labels"]]
    eset = {frozenset((lab[i], lab[j])) for i, j in di["edges"]}
    full = [e[(i, j)] if frozenset((S[i], S[j])) in eset else -e[(i, j)] for i, j in itertools.combinations(range(n), 2)]
    for frac in (1.0, 0.95, 0.9, 0.8, 0.7, 0.5, 0.3, 0.0):
        part = [x for x in full if rng.random() < frac]
        ok, model = sol.solve(part)
        if ok:
            print("warm start from %s: kept %.0f%% of the pairs" % (os.path.basename(INIT), 100 * frac), flush=True)
            break
cur = evaluate(model)
while cur is None:
    ok, model = sol.solve([v if rng.random() < 0.5 else -v for v in rng.sample(list(e.values()), 30)])
    if ok:
        cur = evaluate(model)
score = -cur[0]
best = score
best_EE = cur[1]
t0 = time.time()
temp = TEMP0
nmove = nc1 = 0
hist = {}
while time.time() - t0 < secs:
    nmove += 1
    freed = set(rng.sample(range(n), NFREE))
    assum = [(e[(i, j)] if model[e[(i, j)]] else -e[(i, j)]) for i, j in itertools.combinations(range(n), 2)
             if i not in freed and j not in freed]
    ok2, m2 = sol.solve(assum)
    if not ok2:
        continue
    ev = evaluate(m2)
    if ev is None:
        continue
    nc1 += 1
    s2 = -ev[0]
    hist[ev[0]] = hist.get(ev[0], 0) + 1
    if s2 >= score or rng.random() < math.exp((s2 - score) / temp):
        model, score = m2, s2
        if score > best:
            best, best_EE = score, ev[1]
    temp = max(0.05, temp * 0.9995)
if MAXNU:
    print("seed %d: %d moves, %d lemma-free c(l)=1 proposals; MAX nu(T_S) reached = %d  (Conway needs >= 14); E3 %s tau %s" % (
        seed, nmove, nc1, 100 + best, E3, TAU), flush=True)
    print("   histogram of visited nu:", dict(sorted((100 - k, v) for k, v in hist.items())))
else:
    print("seed %d: %d moves, %d c(l)=1 proposals; MIN rank_3(A_Omega) reached = %d  (Conway needs <= 45); E3 clauses: %s" % (
        seed, nmove, nc1, -best, E3), flush=True)
if not MAXNU:
    print("   histogram of visited rank_3:", dict(sorted(hist.items())))
Ssorted = [sorted(l) for l in S]
pos = {l: i for i, l in enumerate(S)}
json.dump({"labels": Ssorted, "rank3": -best,
           "edges": [[pos[a], pos[b]] for a, b in (tuple(x) for x in best_EE)]},
          open(os.path.join(HERE, "unbiased_walks", "%s_best_seed%d%s%s.json" % ("maxnu" if MAXNU else "rank3walk", seed, "_e3" if E3 else "", ("_warm" if INIT else "") + ("_sym" if SYM else "") + ("_tau" if TAU else ""))), "w"))
