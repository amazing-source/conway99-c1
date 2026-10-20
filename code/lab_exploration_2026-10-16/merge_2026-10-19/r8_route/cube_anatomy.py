"""Anatomy of a hard R8 cube (LAB 20/10/2026): what is left, and is the residual a pure counting problem?

Input: a knuth_la.py record with its cube (edge literals).  Steps:
 1. unit propagation of R8 (+L4B,XPAIR CNF) under the cube (pysat) -> fixed edge literals;
 2. residual table: free edge variables by region (base-base, base-X, X-X), residual demands of the exact counts;
 3. CP-SAT (diagnostic only, not a proof) on two relaxations of the residual:
      (a) C1 only (exact letters 0..3 and letter 4 on B, upper bounds for the others), no C2 caps;
      (b) the full model (C1, C1', C2' with exact products), same as five_cnf.py --reify;
    with the fixed literals imposed.
usage: python cube_anatomy.py <cnf> <records jsonl> <record index> <seconds> <out json>"""
import itertools
import json
import os
import sys
import time

from ortools.sat.python import cp_model
from pysat.solvers import Solver

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r8lib  # noqa: E402
from knuth_la import load_cnf  # noqa: E402


def cpsat(M, fixed, caps, secs, l4b=True):
    m = cp_model.CpModel()
    e = {}
    for p in M.pairs:
        e[p] = m.NewBoolVar("")
        v = M.var(*p)
        if v in fixed:
            m.Add(e[p] == 1)
        elif -v in fixed:
            m.Add(e[p] == 0)
    E = lambda i, j: e[(min(i, j), max(i, j))]
    for i, l in enumerate(M.S):
        for y in range(M.K):
            lits = [E(i, j) for j in range(M.n) if j != i and y in M.S[j]]
            if not lits:
                continue
            c = r8lib.c_need(l, y)
            if y in M.exact or (l4b and y == 4 and i < len(M.B)):
                m.Add(sum(lits) == c)
            else:
                m.Add(sum(lits) <= c)
    if caps:
        for i, j in M.pairs:
            s = len(M.S[i] & M.S[j])
            prods = []
            for t in range(M.n):
                if t in (i, j):
                    continue
                p = m.NewBoolVar("")
                m.AddBoolAnd([E(i, t), E(j, t)]).OnlyEnforceIf(p)
                m.AddBoolOr([E(i, t).Not(), E(j, t).Not()]).OnlyEnforceIf(p.Not())
                prods.append(p)
            m.Add(sum(prods) + s + E(i, j) <= 2)
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 1
    sv.parameters.max_time_in_seconds = secs
    t0 = time.time()
    st = sv.Solve(m)
    return sv.StatusName(st), round(time.time() - t0, 1)


def main():
    cnf, recs, k, secs, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    rows = [json.loads(l) for l in open(recs) if l.strip()]
    rows = [r for r in rows if "cube" in r]
    r = rows[k]
    M = r8lib.Model(14)
    NE = len(M.pairs)
    cls, nv = load_cnf(cnf)
    sv = Solver(name="glucose4", bootstrap_with=cls)
    ok, imp = sv.propagate(assumptions=r["cube"])
    sv.delete()
    fixed = set(v for v in imp if abs(v) <= NE)
    nB = len(M.B)
    reg = {"BB": [0, 0, 0], "BX": [0, 0, 0], "XX": [0, 0, 0]}      # [true, false, free]
    for (i, j) in M.pairs:
        key = "BB" if j < nB else ("BX" if i < nB else "XX")
        v = M.var(i, j)
        reg[key][0 if v in fixed else (1 if -v in fixed else 2)] += 1
    # residual demands of exact counts
    dem = []
    for i, l in enumerate(M.S):
        for y in range(5):
            if y == 4 and i >= nB:
                continue
            lits = [M.var(i, j) for j in range(M.n) if j != i and y in M.S[j]]
            t = sum(1 for v in lits if v in fixed)
            f = sum(1 for v in lits if v not in fixed and -v not in fixed)
            need = r8lib.c_need(l, y) - t
            if need > 0:
                dem.append([sorted(l), y, need, f])
    res = {"record": k, "depth": r["depth"], "propagation_ok": ok, "fixed": len(fixed), "regions": reg,
           "open_exact_demands": len(dem), "tight_demands(need==free)": sum(1 for d in dem if d[2] == d[3]),
           "demand_sample": dem[:12]}
    print(json.dumps(res), flush=True)
    res["cpsat_C1_only"] = cpsat(M, fixed, False, secs)
    print("C1 only:", res["cpsat_C1_only"], flush=True)
    res["cpsat_full"] = cpsat(M, fixed, True, secs)
    print("full:", res["cpsat_full"], flush=True)
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main()
