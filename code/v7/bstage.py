"""V7, column stage (B-stage), solved simultaneously and exactly with CP-SAT.

For one core C (27 vertices) we choose the multiset of 72 outside columns b_u (core neighbourhoods) with q-labels,
and the 4 holes among the 13 a-positives, subject to:
  * B B^T = 12I + 2J - C - C^2 on the core (every core pair gets exactly its missing common neighbours,
    every core vertex its missing degree);
  * the q eigen-equation (A+4I)q = 6*1 at every core vertex (outside contributions = q-labels of the columns);
  * per-column local rules: exactly one grid neighbour (a(u)=0), k t-neighbours and k+2 a-positive neighbours,
    the core neighbourhood induces a matching, no core vertex sees 3 points of it, type-III columns sit on a
    defect pair, q-class rules (positive degree p(u)), with the holes as variables;
  * two outside vertices share at most 2 core neighbours.
Everything here is a NECESSARY condition: INFEASIBLE excludes the core (for all hole choices); a solution is only a
column multiset, not a graph.
"""
import itertools, json, sys, time
import numpy as np
from ortools.sat.python import cp_model

GRID = list(range(8)); MATES = [3, 4, 6, 7]; T = list(range(8, 14)); P13 = list(range(14, 27))
QCORE = {0: -1, 1: -1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}
for t in T:
    QCORE[t] = 0


def target_matrix(A):
    C2 = A @ A
    n = A.shape[0]
    M = np.zeros_like(A)
    for i in range(n):
        for j in range(n):
            if i == j:
                M[i, i] = 14 - A[i].sum()
            else:
                M[i, j] = (1 if A[i, j] else 2) - C2[i, j]
    return M


def gen_columns(A, defect_pairs):
    """columns = (sorted tuple b, q) ; local rules not depending on holes."""
    nb = [set(np.nonzero(A[i])[0]) for i in range(27)]
    apos = MATES + P13
    cols = []
    for g in GRID:
        for k in (0, 1, 2):
            for Tb in itertools.combinations(T, k):
                if k == 2 and (Tb[0] - 8, Tb[1] - 8) not in defect_pairs:
                    continue
                need = k + 2 - (1 if g in MATES else 0)
                for Pb in itertools.combinations(P13, need):
                    b = (g,) + Tb + Pb
                    bs = set(b)
                    ok = True
                    for w in range(27):
                        c = len(nb[w] & bs)
                        if (w in bs and c > 1) or (w not in bs and c > 2):
                            ok = False; break
                    if not ok:
                        continue
                    for q in (0, 1):
                        if g in (0, 1):
                            pass  # Bx/By (q=1) or Zx/Zy (q=0)
                        cols.append((tuple(sorted(b)), q))
    return cols


def pdeg(g, q):
    """number of q-positive neighbours of an outside vertex with grid neighbour g and value q."""
    if g in (0, 1):
        return 3 if q == 1 else 7
    return 2 if q == 1 else 6


def solve_core(core, time_limit=600.0, workers=4, verbose=False, extra=None):
    A = np.array(core["adj"])
    M = target_matrix(A)
    defect_pairs = set(tuple(p) for p in core["defect"])
    cols = gen_columns(A, defect_pairs)
    m = cp_model.CpModel()
    h = {v: m.NewBoolVar(f"h{v}") for v in P13}
    m.Add(sum(h.values()) == 4)
    n = []
    used = []
    for idx, (b, q) in enumerate(cols):
        cap = 1 if len(b) >= 3 else int(M[b[0], b[1]])
        x = m.NewIntVar(0, cap, f"n{idx}")
        u = m.NewBoolVar(f"u{idx}")
        m.Add(x >= 1).OnlyEnforceIf(u); m.Add(x == 0).OnlyEnforceIf(u.Not())
        n.append(x); used.append(u)
        g = b[0]
        # core positive neighbours <= p(u):  [g positive] + #(b cap P13 non-hole)
        p13 = [v for v in b if v in P13]
        base = 1 if QCORE[g] == 1 else 0
        lim = pdeg(g, q) - base
        if len(p13) > lim:
            m.Add(sum(1 - h[v] for v in p13) <= lim).OnlyEnforceIf(u)
    # pair design B B^T = M on the core
    inc = {}
    for idx, (b, q) in enumerate(cols):
        for i in b:
            for j in b:
                if i <= j:
                    inc.setdefault((i, j), []).append(idx)
    for i in range(27):
        for j in range(i, 27):
            terms = inc.get((i, j), [])
            if M[i, j] < 0:
                raise ValueError("negative target")
            m.Add(sum(n[t] for t in terms) == int(M[i, j]))
    # q eigen-equation at core vertices: sum over outside nbrs of q = 6 - 4 q(i) - core part
    for i in range(27):
        terms = [n[idx] for idx, (b, q) in enumerate(cols) if q == 1 and i in b]
        core_nb = np.nonzero(A[i])[0]
        if i in P13:
            # q(i) = 1 - h_i ; core nbrs are t's (q=0)
            # outside positives = 6 - 4(1-h_i) - 0 = 2 + 4 h_i
            m.Add(sum(terms) == 2 + 4 * h[i])
        else:
            qi = QCORE[i]
            const = 6 - 4 * qi - sum(QCORE[w] for w in core_nb if w not in P13)
            p13nb = [w for w in core_nb if w in P13]
            m.Add(sum(terms) == const - sum(1 - h[w] for w in p13nb))
    # two outside vertices share at most 2 core neighbours
    bysets = [set(b) for b, q in cols]
    nconf = 0
    by_triple = {}
    for idx, b in enumerate(bysets):
        if len(b) >= 3:
            for tr in itertools.combinations(sorted(b), 3):
                by_triple.setdefault(tr, []).append(idx)
    for tr, lst in by_triple.items():
        if len(lst) > 1:
            m.Add(sum(used[i] for i in lst) <= 1)
            nconf += 1
    # class counts (redundant but helpful): 20 positives outside
    m.Add(sum(n[idx] for idx, (b, q) in enumerate(cols) if q == 1) == 20)
    if extra:
        extra(m, cols, n, used, h)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_workers = workers
    s.parameters.log_search_progress = verbose
    t0 = time.time()
    st = s.Solve(m)
    res = {"status": s.StatusName(st), "time": round(time.time() - t0, 2), "ncols": len(cols),
           "triple_conflicts": nconf}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        res["holes"] = [v for v in P13 if s.Value(h[v])]
        res["solution"] = [[list(cols[i][0]), cols[i][1], s.Value(n[i])] for i in range(len(cols)) if s.Value(n[i])]
    return res


if __name__ == "__main__":
    cores = json.load(open(sys.argv[1]))
    which = [int(a) for a in sys.argv[2].split(",")] if len(sys.argv) > 2 else range(len(cores))
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600.0
    out = {}
    for k in which:
        r = solve_core(cores[k], time_limit=tl)
        out[k] = r
        print(k, r["status"], r["time"], "cols", r["ncols"], "conf", r["triple_conflicts"],
              "holes", r.get("holes"), flush=True)
    json.dump(out, open(f"bstage_{'_'.join(map(str, which))}.json", "w"))
