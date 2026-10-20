"""Cross-check of the R8 encodings against the definition (LAB 20/10/2026).

For a full assignment of the edge variables, every encoding used here (reified products, sequential counter or
totalizer in the upward direction) is satisfiable iff unit propagation finds no conflict (unforced auxiliary variables
can be set false).  So each CNF defines a set of edge assignments, which must coincide with the set accepted by the
independent checker Model.check.  We compare the three verdicts (checker, my CNF, archive five_cnf.py CNF) on:
  (a) the R7 witnesses of 16/10 (model nx = 7) and all their single-edge flips;
  (b) R8 (nx = 8): R7 witness + random attachments of the 8th label, and random flips;
  (c) random sparse assignments.
usage: python test_encoding.py <archive cnf R7> <archive cnf R8> <witness dir> <out json>"""
import glob
import itertools
import json
import os
import random
import sys
import time

from pysat.solvers import Solver

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r8lib  # noqa: E402


def load_cnf(path):
    cls = []
    with open(path) as fh:
        for line in fh:
            if not line or line[0] in "cp":
                continue
            lits = [int(t) for t in line.split()]
            if lits and lits[-1] == 0:
                lits.pop()
            cls.append(lits)
    return cls


def verdict(sv, M, edges):
    es = set(tuple(sorted(p)) for p in edges)
    ass = [M.var(i, j) if (i, j) in es else -M.var(i, j) for (i, j) in M.pairs]
    ok, _ = sv.propagate(assumptions=ass)
    return bool(ok)


def main():
    a7, a8, wdir, out = sys.argv[1:5]
    rng = random.Random(20261020)
    res = {}
    t0 = time.time()
    for tag, nx, apath in (("R7", 7, a7), ("R8", 8, a8)):
        M = r8lib.Model(14, nx=nx)
        Fm, info = r8lib.encode(M)
        sm = Solver(name="minisat22", bootstrap_with=Fm.clauses)
        sa = Solver(name="minisat22", bootstrap_with=load_cnf(apath))
        stats = {"tests": 0, "agree": 0, "accepted": 0, "disagree": []}

        def test(edges, label):
            c = len(M.check(edges)) == 0
            vm, va = verdict(sm, M, edges), verdict(sa, M, edges)
            stats["tests"] += 1
            stats["accepted"] += int(c)
            if c == vm == va:
                stats["agree"] += 1
            else:
                stats["disagree"].append({"what": label, "checker": c, "mine": vm, "archive": va})

        wit = []
        for f in sorted(glob.glob(os.path.join(wdir, "r7_seed*.json"))):
            d = json.load(open(f))
            labs = [frozenset(x) for x in d["labels"]]
            E = [(min(M.idx[labs[i]], M.idx[labs[j]]), max(M.idx[labs[i]], M.idx[labs[j]])) for i, j in d["edges"]
                 if labs[i] in M.idx and labs[j] in M.idx]
            wit.append((os.path.basename(f), E))
        for name, E in wit:
            test(E, name)
            Es = set(E)
            flips = rng.sample(M.pairs, 400 if tag == "R7" else 200)
            for p in flips:
                test(list(Es ^ {p}), name + " flip %s" % (p,))
            if tag == "R8":
                last = M.n - 1
                for _ in range(200):
                    cand = [(i, last) for i in range(last)]
                    add = rng.sample(cand, rng.choice([6, 8, 10, 12]))
                    test(list(Es | set(add)), name + " attach")
        for _ in range(300):
            E = rng.sample(M.pairs, rng.choice([60, 120, 160]))
            test(E, "random")
        stats["info_mine"] = info
        res[tag] = stats
        print(tag, {k: v for k, v in stats.items() if k != "disagree"}, "disagreements:", len(stats["disagree"]),
              flush=True)
        sm.delete()
        sa.delete()
    res["seconds"] = round(time.time() - t0, 1)
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main()
