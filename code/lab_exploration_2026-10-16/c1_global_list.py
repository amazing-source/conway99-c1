"""The c = 1 case list on the EXACT global model (exploration, LAB 17/10/2026), as Codex does for his templates.
Global model: Codex's build_global (c1-asymmetry-audit/code/codex/conway_global_cover.py, imported read-only):
Gamma on all 84 labels of a vertex o, with the exact equations
    sum_{q containing r} Gamma[p,q] = 2 - [r in p] - [r^1 in p],      (Gamma^2)[p,q] + Gamma[p,q] + |p n q| = 2,
EQUIVALENT to srg(99,14,1,2) (no relaxation: positivity and rank 30 are automatic).  No star normalization (it would
relabel the mate pairs and move the case data).
Case data (line l = {o,0,1}): rectangle profile at l (c1_cases.all_cases: e of Q_{(0,1),(2,3)}, then the five outer
rectangles sorted), c(l) = 1 (the rectangle multigraph M_0 at l is connected: every proper cut is crossed),
E3 (no rectangle with exactly 3 internal edges) at all seven lines through o (Codex's lemma).
usage: python c1_global_list.py <case range a-b> <seconds> <status.json> [--build-only]"""
import itertools
import json
import os
import sys
import time

from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CODEX = r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-asymmetry-audit\code\codex"
sys.path.insert(0, CODEX)
from conway_global_cover import build_global  # noqa: E402
import c1_cases as CS  # noqa: E402


def add_case(model, labels, graph, case):
    index = {p: i for i, p in enumerate(labels)}
    lab = lambda a, b: index[tuple(sorted((a, b)))]
    pairs = [(2 * j, 2 * j + 1) for j in range(7)]
    # E3 at all seven lines through o: rectangle Q_{ij} = {a b : a in line i, b in line j}
    rect = {}
    for (i, li), (j, lj) in itertools.combinations(enumerate(pairs), 2):
        q = [lab(a, b) for a in li for b in lj]
        rect[(i, j)] = q
        model.Add(sum(graph[p][r] for p, r in itertools.combinations(q, 2)) != 3)
    # profile at l = line 0: rectangles (0, j), j = 1..6 in the order of c1_cases.ROOT_L
    for k, j in enumerate(range(1, 7)):
        q = rect[(0, j)]
        model.Add(sum(graph[p][r] for p, r in itertools.combinations(q, 2)) == case[k])
    # c(l) = 1: M_0 connected
    Q = [rect[(0, j)] for j in range(1, 7)]
    for size in range(1, 6):
        for sub in itertools.combinations(range(6), size):
            if 0 not in sub:
                continue
            ins = [p for k in sub for p in Q[k]]
            out = [p for k in range(6) if k not in sub for p in Q[k]]
            model.AddBoolOr([graph[p][r] for p in ins for r in out])
    branch = os.environ.get("BRANCH", "")
    if branch == "A":
        # every line through o has c = 1 (branch A: no vertex carries a c = 1 line and a c >= 2 line)
        for i in range(1, 7):
            Qi = [rect[tuple(sorted((i, j)))] for j in range(7) if j != i]
            for size in range(1, 6):
                for sub in itertools.combinations(range(6), size):
                    if 0 not in sub:
                        continue
                    ins = [p for k in sub for p in Qi[k]]
                    out = [p for k in range(6) if k not in sub for p in Qi[k]]
                    model.AddBoolOr([graph[p][r] for p in ins for r in out])
    if branch == "B":
        add_forced_kernel_m(model, labels, graph, rect)
    if os.environ.get("CM"):
        sub = tuple(int(t) for t in os.environ["CM"].split(","))
        if not add_fixed_zero_cut_m(model, labels, graph, rect, sub):
            model.Add(graph[0][1] == 0)
            model.Add(graph[0][1] == 1)          # arithmetic contradiction: make the model trivially infeasible
    if os.environ.get("VTYPE"):
        # vertex type: for every other line j through o, its full component partition (Codex-style template),
        # given as  j:blocks;j:blocks  with blocks = comma lists of the OTHER line index k (rectangle Q_{jk}) joined by '|'
        for spec in os.environ["VTYPE"].split(";"):
            j, blocks = spec.split(":")
            j = int(j)
            for block in blocks.split("|"):
                ks = [int(t) for t in block.split(",")]
                if not add_zero_cut_line(model, labels, graph, rect, j, ks):
                    model.Add(graph[0][1] == 0)
                    model.Add(graph[0][1] == 1)
    if os.environ.get("CMP"):
        # full component partition of the six rectangles at m, blocks separated by '|'
        for block in os.environ["CMP"].split("|"):
            sub = tuple(int(t) for t in block.split(","))
            if not add_fixed_zero_cut_m(model, labels, graph, rect, sub):
                model.Add(graph[0][1] == 0)
                model.Add(graph[0][1] == 1)
    return rect


def add_zero_cut_line(model, labels, graph, rect, j, ks):
    """the rectangles Q_{jk} (k in ks) at the root line j form a union of components of M_j: zero cut + T x = 0."""
    n = len(labels)
    Qj = {k: rect[tuple(sorted((j, k)))] for k in range(7) if k != j}
    rootj = sorted(set(p for q in Qj.values() for p in q))
    inside = set(p for k in ks for p in Qj[k])
    for p in inside:
        for r in rootj:
            if r not in inside:
                model.Add(graph[p][r] == 0)
    for r in range(n):
        k8x = sum(k8(labels[r], labels[q]) for q in inside)
        if k8x % 8:
            return False
        val = 3 * (1 if r in inside else 0) - k8x // 8
        if val < 0:
            return False
        model.Add(sum(graph[r][q] for q in inside if q != r) == val)
    return True


def add_fixed_zero_cut_m(model, labels, graph, rect, sub):
    """template-style: the rectangles 'sub' of the root m (indices into Qm, 0 = shared) form a union of components of
    M_m (zero cut), with T x = 0 imposed as plain equalities.  Returns False if 3x - Kx is not a nonnegative integer."""
    n = len(labels)
    Qm = [rect[tuple(sorted((1, j)))] for j in range(7) if j != 1]
    rootm = sorted(set(p for q in Qm for p in q))
    inside = set(p for k in sub for p in Qm[k])
    for p in inside:
        for r in rootm:
            if r not in inside:
                model.Add(graph[p][r] == 0)
    for r in range(n):
        k8x = sum(k8(labels[r], labels[j]) for j in inside)
        if k8x % 8:
            return False
        val = 3 * (1 if r in inside else 0) - k8x // 8
        if val < 0:
            return False
        model.Add(sum(graph[r][j] for j in inside if j != r) == val)
    return True


def k8(a, b):
    s = len(set(a) & set(b))
    m = sum(1 for x in a for y in b if y == (x ^ 1))
    return 3 * s + m - 2


def add_forced_kernel_m(model, labels, graph, rect):
    """branch B: the line m = {o,2,3} (line 1) has a zero cut; for a zero cut C, x = 1_{Q_m(C)} satisfies x^t T x = 0,
    hence T x = 0 on all 84 labels: sum_{j in Q_m(C)} Gamma_rj = 3 x_r - (K x)_r for every label r."""
    n = len(labels)
    Qm = [rect[tuple(sorted((1, j)))] for j in range(7) if j != 1]       # Qm[0] = rect (0,1), shared with l
    rootm = sorted(set(p for q in Qm for p in q))
    K8 = [[k8(labels[a], labels[b]) for b in range(n)] for a in range(n)]
    bs = []
    for size in range(1, 6):
        for sub in itertools.combinations(range(6), size):
            if 0 not in sub:
                continue
            inside = set(p for k in sub for p in Qm[k])
            outside = [p for p in rootm if p not in inside]
            b = model.NewBoolVar("")
            cross = [graph[p][r] for p in inside for r in outside]
            model.Add(sum(cross) == 0).OnlyEnforceIf(b)
            model.Add(sum(cross) >= 1).OnlyEnforceIf(b.Not())
            ok = True
            rhs = []
            for r in range(n):
                k8x = sum(K8[r][j] for j in inside)
                if k8x % 8:
                    ok = False
                    break
                val = 3 * (1 if r in inside else 0) - k8x // 8
                if val < 0:
                    ok = False
                    break
                rhs.append(val)
            if not ok:
                model.Add(b == 0)
            else:
                for r in range(n):
                    model.Add(sum(graph[r][j] for j in inside if j != r) == rhs[r]).OnlyEnforceIf(b)
            bs.append(b)
    model.AddBoolOr(bs)


def main():
    lo, hi = [int(t) for t in sys.argv[1].split("-")]
    secs = float(sys.argv[2])
    statf = sys.argv[3]
    build_only = "--build-only" in sys.argv
    status = json.load(open(statf)) if os.path.exists(statf) else {}
    cases = CS.all_cases()
    for ci in range(lo, min(hi, len(cases))):
        case = cases[ci]
        key = "%d:%s" % (ci, "".join(map(str, case)))
        if status.get(key, {}).get("status") == "INFEASIBLE":
            continue
        t0 = time.time()
        model, labels, graph, selectors, info = build_global(normalize_star=False)
        add_case(model, labels, graph, case)
        tb = time.time() - t0
        if build_only:
            print("case %s built in %.1f s: %d variables, %d constraints, %d products" % (
                key, tb, len(model.Proto().variables), len(model.Proto().constraints), info["product_variables"]), flush=True)
            continue
        sv = cp_model.CpSolver()
        sv.parameters.num_search_workers = int(os.environ.get("WORKERS", "2"))
        sv.parameters.max_time_in_seconds = secs
        sv.parameters.cp_model_probing_level = int(os.environ.get("PROBING", "0"))
        sv.parameters.linearization_level = int(os.environ.get("LINEAR", "0"))
        sv.parameters.symmetry_level = 0
        if os.environ.get("NOPRESOLVE"):
            sv.parameters.cp_model_presolve = False
        st = sv.Solve(model)
        name = sv.StatusName(st)
        res = {"status": "INFEASIBLE" if name == "INFEASIBLE" else ("FEASIBLE" if name in ("OPTIMAL", "FEASIBLE") else "UNKNOWN"),
               "build_s": round(tb, 1), "solve_s": round(sv.WallTime(), 1), "branches": sv.NumBranches(),
               "conflicts": sv.NumConflicts()}
        status[key] = res
        json.dump(status, open(statf, "w"), indent=0)
        print("case %s: %s" % (key, res), flush=True)
    tally = {}
    for v in status.values():
        tally[v["status"]] = tally.get(v["status"], 0) + 1
    print("TALLY:", tally, flush=True)


if __name__ == "__main__":
    main()
