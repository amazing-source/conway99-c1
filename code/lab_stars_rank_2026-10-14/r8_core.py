"""Minimal set of base FACTS (edges and non-edges of a four-star block) that forbids attaching the eight labels {4,t}
(LAB 16/10/2026).  R8 CNF from five_cnf.py (stars 0..3 exact + all eight labels {4,t}, letter 4 bounded); the facts of a
seven-label witness block are passed to an incremental CaDiCaL (python-sat) as assumptions.  UNSAT core, then
deletion-based minimisation (every fact of the result is necessary).  Prints the core in label notation.
usage: python r8_core.py <R8 cnf> <witness json (labels/edges)> <out json> [seconds per solve]"""
import itertools
import json
import sys
import time

from pysat.formula import CNF
from pysat.solvers import Solver

cnf_path, wit, out = sys.argv[1], sys.argv[2], sys.argv[3]
K = 14
MATE = lambda i: i ^ 1
LABELS = [frozenset((u, w)) for u, w in itertools.combinations(range(K), 2) if w != MATE(u)]
S = [l for l in LABELS if any(y in l for y in (0, 1, 2, 3))]
S = S + [frozenset((4, t)) for t in range(6, 14) if frozenset((4, t)) not in S][:8]
n = len(S)
var = {p: k + 1 for k, p in enumerate(itertools.combinations(range(n), 2))}
w = json.load(open(wit))
WL = [frozenset(x) for x in w["labels"]]
WE = set(frozenset((WL[i], WL[j])) for i, j in w["edges"])
base = [l for l in S if l & {0, 1, 2, 3}]
facts = []
for a, b in itertools.combinations(base, 2):
    i, j = sorted((S.index(a), S.index(b)))
    v = var[(i, j)]
    facts.append(v if frozenset((a, b)) in WE else -v)
t0 = time.time()
F = CNF(from_file=cnf_path)
s = Solver(name="cadical195", bootstrap_with=F.clauses)
print("loaded %d clauses, %d facts (%.1f s)" % (len(F.clauses), len(facts), time.time() - t0), flush=True)
t1 = time.time()
ok = s.solve(assumptions=facts)
print("all facts: %s (%.1f s)" % ("SAT" if ok else "UNSAT", time.time() - t1), flush=True)
assert not ok
core = list(s.get_core())
print("first core: %d facts" % len(core), flush=True)
budget = int(sys.argv[4]) if len(sys.argv) > 4 else 200000      # conflicts per deletion test
k = 0
undecided = 0
while k < len(core):
    trial = core[:k] + core[k + 1:]
    t1 = time.time()
    s.conf_budget(budget)
    r = s.solve_limited(assumptions=trial)
    if r is False:
        sub = set(s.get_core())
        core = [x for x in trial if x in sub]           # keep the (possibly smaller) new core, same order
    else:
        if r is None:
            undecided += 1                              # budget exhausted: keep the fact (core stays valid)
        k += 1
    print("  pos %d, core %d (%s, %.1f s)" % (k, len(core), {True: "SAT", False: "UNSAT", None: "BUDGET"}[r],
                                                time.time() - t1), flush=True)
print("deletion done: %d tests stopped by the budget (the core is minimal only up to those)" % undecided, flush=True)
assert s.solve(assumptions=core) is False                # final full check of the core
inv = {v: p for p, v in var.items()}
res = []
for x in core:
    i, j = inv[abs(x)]
    res.append({"pair": [sorted(S[i]), sorted(S[j])], "edge": x > 0})
json.dump({"witness": wit, "core": res, "seconds": time.time() - t0}, open(out, "w"), indent=1)
print("minimal core: %d facts (%d edges, %d non-edges)" % (len(res), sum(r["edge"] for r in res),
                                                           sum(not r["edge"] for r in res)), flush=True)
for r in res:
    print("  %s %s %s" % (r["pair"][0], "~" if r["edge"] else "!~", r["pair"][1]), flush=True)
