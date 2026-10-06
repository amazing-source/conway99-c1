"""Column stage + exact linear consequences of the F-stage that involve B only.
r_i(b) = (2 - [i in b]) - |N_C(i) cap b|  = number of outside neighbours of u lying in O_i (fiber of core vertex i).
 (L1) for core i<j : sum_{u: j in b_u} r_i(b_u) = sum_{u: i in b_u} r_j(b_u)          (F symmetric)
 (L2) for core i   : sum_u r_i(b_u) = sum_{u: i in b_u} (14 - |b_u|)                    (row sums of F)
 (L3) for core i   : sum_{u: q_u=1} r_i(b_u) = sum_{u: i in b_u} (p(u) - cpos(u))         (q eigen-equation at u)
"""
import itertools, json, sys, time
import numpy as np
from ortools.sat.python import cp_model
from bstage import gen_columns, target_matrix, GRID, MATES, T, P13, QCORE, pdeg

def model(core, use_q=True, fix_holes=None, time_limit=300, workers=4, L=(1,2,3), verbose=False, colmask=None):
    A = np.array(core["adj"]); M = target_matrix(A)
    cols = gen_columns(A, set(tuple(p) for p in core["defect"]))
    if colmask is not None:
        cols = [c for c, keep in zip(cols, colmask) if keep]
    if not use_q:
        cols = [c for c in cols if c[1] == 0]
    nb = [set(np.nonzero(A[i])[0]) for i in range(27)]
    m = cp_model.CpModel()
    h = {v: m.NewBoolVar(f"h{v}") for v in P13}
    m.Add(sum(h.values()) == 4)
    if fix_holes is not None:
        for v in P13: m.Add(h[v] == (1 if v in fix_holes else 0))
    n, used = [], []
    for idx, (b, q) in enumerate(cols):
        cap = 1 if len(b) >= 3 else int(M[b[0], b[1]])
        x = m.NewIntVar(0, cap, f"n{idx}"); u = m.NewBoolVar(f"u{idx}")
        m.Add(x >= 1).OnlyEnforceIf(u); m.Add(x == 0).OnlyEnforceIf(u.Not())
        n.append(x); used.append(u)
        if use_q:
            g = b[0]; p13 = [v for v in b if v in P13]
            lim = pdeg(g, q) - (1 if QCORE[g] == 1 else 0)
            if len(p13) > lim:
                m.Add(sum(1 - h[v] for v in p13) <= lim).OnlyEnforceIf(u)
    inc = {}
    for idx, (b, q) in enumerate(cols):
        for i in b:
            for j in b:
                if i <= j: inc.setdefault((i, j), []).append(idx)
    for i in range(27):
        for j in range(i, 27):
            m.Add(sum(n[t] for t in inc.get((i, j), [])) == int(M[i, j]))
    by_triple = {}
    for idx, (b, q) in enumerate(cols):
        if len(b) >= 3:
            for tr in itertools.combinations(b, 3): by_triple.setdefault(tr, []).append(idx)
    for tr, lst in by_triple.items():
        if len(lst) > 1: m.Add(sum(used[i] for i in lst) <= 1)
    R = [[(2 - (1 if i in b else 0)) - len(nb[i] & set(b)) for i in range(27)] for b, q in cols]
    if 1 in L:
        for i, j in itertools.combinations(range(27), 2):
            lhs = sum(R[idx][i] * n[idx] for idx, (b, q) in enumerate(cols) if j in b and R[idx][i])
            rhs = sum(R[idx][j] * n[idx] for idx, (b, q) in enumerate(cols) if i in b and R[idx][j])
            m.Add(lhs == rhs)
    if 2 in L:
        for i in range(27):
            m.Add(sum(R[idx][i] * n[idx] for idx in range(len(cols)) if R[idx][i]) ==
                  sum((14 - len(b)) * n[idx] for idx, (b, q) in enumerate(cols) if i in b))
    if use_q:
        # q eigen-equation at core vertices
        for i in range(27):
            terms = [n[idx] for idx, (b, q) in enumerate(cols) if q == 1 and i in b]
            core_nb = np.nonzero(A[i])[0]
            if i in P13:
                m.Add(sum(terms) == 2 + 4 * h[i])
            else:
                const = 6 - 4 * QCORE[i] - sum(QCORE[w] for w in core_nb if w not in P13)
                m.Add(sum(terms) == const - sum(1 - h[w] for w in core_nb if w in P13))
        m.Add(sum(n[idx] for idx, (b, q) in enumerate(cols) if q == 1) == 20)
        if 3 in L:
            # outside positive nbrs of u = p(u) - cpos(u), cpos(u) = [g positive] + #(b cap P13 non-hole)
            # product n_idx * h_v needed: use per-column int var for cpos contribution
            for i in range(27):
                lhs = sum(R[idx][i] * n[idx] for idx, (b, q) in enumerate(cols) if q == 1 and R[idx][i])
                rhs_terms = []
                for idx, (b, q) in enumerate(cols):
                    if i not in b: continue
                    g = b[0]; p13 = [v for v in b if v in P13]
                    const = pdeg(g, q) - (1 if QCORE[g] == 1 else 0)
                    if not p13:
                        rhs_terms.append(const * n[idx])
                    else:
                        # n_idx * (const - #nonhole p13) ; n_idx in {0,1} when |b|>=3
                        cap = 1 if len(b) >= 3 else int(M[b[0], b[1]])
                        y = m.NewIntVar(-cap * len(p13), cap * const, f"y{i}_{idx}")
                        # y = n*(const - sum(1-h_v))
                        z = m.NewIntVar(-len(p13), const, f"z{i}_{idx}")
                        m.Add(z == const - sum(1 - h[v] for v in p13))
                        m.AddMultiplicationEquality(y, [n[idx], z])
                        rhs_terms.append(y)
                m.Add(lhs == sum(rhs_terms))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_workers = workers; s.parameters.log_search_progress = verbose
    t0 = time.time(); st = s.Solve(m)
    out = {"status": s.StatusName(st), "time": round(time.time() - t0, 1), "ncols": len(cols)}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        out["holes"] = [v for v in P13 if s.Value(h[v])]
        out["solution"] = [[list(cols[i][0]), cols[i][1], s.Value(n[i])] for i in range(len(cols)) if s.Value(n[i])]
    return out

if __name__ == "__main__":
    cores = json.load(open("cores27.json"))
    k = int(sys.argv[1]); useq = sys.argv[2] == "q"; tl = float(sys.argv[3])
    Ls = tuple(int(c) for c in sys.argv[4]) if len(sys.argv) > 4 else (1, 2, 3)
    r = model(cores[k], use_q=useq, time_limit=tl, L=Ls)
    print(k, sys.argv[2], Ls, r["status"], r["time"], r["ncols"], r.get("holes"), flush=True)
    json.dump(r, open(f"b2_{k}_{sys.argv[2]}_{''.join(map(str,Ls))}.json", "w"))
