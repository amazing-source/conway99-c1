"""Projected relaxations of the V7 column stage.

Keep a subset S of core vertices; aggregate the outside columns by their trace on S (and by their q-label and
grid-class data that matter), and impose only the pair constraints of B B^T = M inside S (+ optional q equations).
Any INFEASIBLE answer is an exact exclusion of the core (the relaxation is implied by the full system).
"""
import itertools, json, sys, time
import numpy as np
from ortools.sat.python import cp_model
from bstage import gen_columns, target_matrix, GRID, MATES, T, P13, QCORE, pdeg


def build(core, S, use_q=True, time_limit=300.0, workers=4, verbose=False, fix_holes=None):
    A = np.array(core["adj"])
    M = target_matrix(A)
    cols = gen_columns(A, set(tuple(p) for p in core["defect"]))
    S = sorted(S)
    Sset = set(S)
    # aggregate: key = (trace on S, q, g, |b cap P13| list if needed for hole rule)
    agg = {}
    for b, q in cols:
        if not use_q and q == 1:
            continue
        g = b[0]
        key = (tuple(v for v in b if v in Sset), q if use_q else None, g,
               tuple(v for v in b if v in P13) if use_q else None)
        agg[key] = agg.get(key, 0) + 1
    keys = list(agg)
    m = cp_model.CpModel()
    h = {v: m.NewBoolVar(f"h{v}") for v in P13}
    m.Add(sum(h.values()) == 4)
    if fix_holes is not None:
        for v in P13:
            m.Add(h[v] == (1 if v in fix_holes else 0))
    n = []
    for idx, key in enumerate(keys):
        tr, q, g, p13 = key
        ub = 72
        x = m.NewIntVar(0, ub, f"n{idx}")
        n.append(x)
        if use_q:
            u = m.NewBoolVar(f"u{idx}")
            m.Add(x >= 1).OnlyEnforceIf(u); m.Add(x == 0).OnlyEnforceIf(u.Not())
            base = 1 if QCORE[g] == 1 else 0
            lim = pdeg(g, q) - base
            if len(p13) > lim:
                m.Add(sum(1 - h[v] for v in p13) <= lim).OnlyEnforceIf(u)
    # grid class sizes
    for g in GRID:
        m.Add(sum(n[i] for i, k in enumerate(keys) if k[2] == g) == int(M[g, g]))
    for i, j in itertools.combinations_with_replacement(S, 2):
        terms = [n[t] for t, k in enumerate(keys) if i in k[0] and j in k[0]]
        m.Add(sum(terms) == int(M[i, j]))
    if use_q:
        for i in S:
            terms = [n[idx] for idx, k in enumerate(keys) if k[1] == 1 and i in k[0]]
            core_nb = np.nonzero(A[i])[0]
            if i in P13:
                m.Add(sum(terms) == 2 + 4 * h[i])
            else:
                qi = QCORE[i]
                const = 6 - 4 * qi - sum(QCORE[w] for w in core_nb if w not in P13)
                p13nb = [w for w in core_nb if w in P13]
                m.Add(sum(terms) == const - sum(1 - h[w] for w in p13nb))
        m.Add(sum(n[idx] for idx, k in enumerate(keys) if k[1] == 1) == 20)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_workers = workers
    s.parameters.log_search_progress = verbose
    t0 = time.time()
    st = s.Solve(m)
    return s.StatusName(st), round(time.time() - t0, 1), len(keys)


if __name__ == "__main__":
    cores = json.load(open("cores27.json"))
    k = int(sys.argv[1]); mode = sys.argv[2]; tl = float(sys.argv[3]) if len(sys.argv) > 3 else 300
    S = {"labels": T + P13, "labels_grid": list(range(27)), "t13x": T + P13 + [0],
         "t13xy": T + P13 + [0, 1], "nogridpairs": T + P13}[mode]
    useq = (len(sys.argv) <= 4 or sys.argv[4] != "noq")
    print(k, mode, "q" if useq else "noq", build(cores[k], S, use_q=useq, time_limit=tl), flush=True)
