"""Generic full label-graph model of a root template (LAB 19/10/2026; own code, generalises full5602.py).
Unknown: the 3486 label-label adjacencies at the root.  Constraints (all exact consequences, see NUIT_2026-10-19.md):
  quotas  (F3): 1 label-neighbour at each letter of an own line, 2 at each other letter;
  C2          : shared letters + common label-neighbours = 1 (adjacent) or 2 (non-adjacent), linearised products;
  F2 per label: for a grid rectangle F, z_w(F) = base(w, F) for every label w (h_w(F) = 0), and F's labels carry the
                4-cycle (sides adjacent, diagonals not);
  F1 per label: for every root r and block P at r, sum_{j in P} z_w(Q_rj) = sum_{j in P} base(w, Q_rj) (H sigma = 0);
  E3          : e(F) <= 2 on every non-grid rectangle (e = 3 excluded by E3, e = 4 would be a grid);
  letter flips: symmetry breaking, for each line one lex condition (valid: the 2^7 exchanges act independently).
INFEASIBLE excludes the template (CP-SAT verdict, no certificate); FEASIBLE would be a full Conway graph to check.
usage: python generic_full.py <catalogue.json.gz> <index> <seconds> <workers> [--no-c2] [--no-flip]"""
import gzip
import json
import sys
import time
from itertools import combinations

from ortools.sat.python import cp_model

cat_path, index, seconds, workers = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
FLAGS = sys.argv[5:]
tpl = json.load(gzip.open(cat_path))["open"][index]["template"]
RECT = list(combinations(range(7), 2))
NG = {tuple(e) for e in tpl["nongrid_edges"]}
GRID = [q for q in RECT if q not in NG]
L = [(q, sa, sb) for q in RECT for sa in (0, 1) for sb in (0, 1)]
lid = {w: i for i, w in enumerate(L)}


def lets(w):
    (a, b), sa, sb = w
    return {(a, sa), (b, sb)}


def base(q, f):
    return 2 if f == q else (0 if set(f) & set(q) else 1)


m = cp_model.CpModel()
A = {(i, j): m.NewBoolVar("a%d_%d" % (i, j)) for i, j in combinations(range(84), 2)}


def adj(i, j):
    return A[(min(i, j), max(i, j))]


rect_labels = {q: [lid[(q, sa, sb)] for sa in (0, 1) for sb in (0, 1)] for q in RECT}


def z(i, q):
    return sum(adj(i, j) for j in rect_labels[q] if j != i)


nbr_of_letter = {(a, s): [lid[w] for w in L if (a, s) in lets(w)] for a in range(7) for s in (0, 1)}
for i, w in enumerate(L):
    own = {l[0] for l in lets(w)}
    for a in range(7):
        for s in (0, 1):
            m.Add(sum(adj(i, j) for j in nbr_of_letter[(a, s)] if j != i) == (1 if a in own else 2))
    for F in GRID:                                   # F2 per label
        m.Add(z(i, F) == base(w[0], F))
    for r, groups in enumerate(tpl["nontrivial_component_groups"]):   # F1 per label
        for P in groups:
            qs = [tuple(sorted((r, j))) for j in P]
            m.Add(sum(z(i, q) for q in qs) == sum(base(w[0], q) for q in qs))
for q in GRID:
    for sa in (0, 1):
        for sb in (0, 1):
            i = lid[(q, sa, sb)]
            m.Add(adj(i, lid[(q, sa, 1 - sb)]) == 1)
            m.Add(adj(i, lid[(q, 1 - sa, sb)]) == 1)
            m.Add(adj(i, lid[(q, 1 - sa, 1 - sb)]) == 0)
for q in NG:
    m.Add(sum(adj(i, j) for i, j in combinations(rect_labels[q], 2)) <= 2)
if "--no-flip" not in FLAGS:
    # exchange of the letters of line a swaps s_a in every rectangle containing a; for line a take a rectangle (a, b)
    # and require: sum over its labels with s_a = 0 of their z-profile code <= the same with s_a = 1 (invariant under
    # the exchanges of the other lines, so the 7 conditions are imposed together)
    for a in range(7):
        q = next(q for q in RECT if a in q)
        pa = 0 if q[0] == a else 1
        ref = [j for j in range(84)]
        def code(i):
            return sum((k + 1) * adj(i, j) for k, j in enumerate(rect_labels[RECT[(RECT.index(q) + 1) % 21]]) if j != i)
        lo = [lid[(q, s0, s1)] for s0 in (0, 1) for s1 in (0, 1) if (s0 if pa == 0 else s1) == 0]
        hi = [lid[(q, s0, s1)] for s0 in (0, 1) for s1 in (0, 1) if (s0 if pa == 0 else s1) == 1]
        m.Add(sum(code(i) for i in lo) <= sum(code(i) for i in hi))
t0 = time.time()
if "--no-c2" not in FLAGS:
    P = {}

    def prod(i, j, k):
        key = (min(i, j), max(i, j), k)
        if key not in P:
            b = m.NewBoolVar("")
            m.AddBoolAnd([adj(i, k), adj(j, k)]).OnlyEnforceIf(b)
            m.AddBoolOr([adj(i, k).Not(), adj(j, k).Not()]).OnlyEnforceIf(b.Not())
            P[key] = b
        return P[key]
    for i, j in combinations(range(84), 2):
        sh = len(lets(L[i]) & lets(L[j]))
        common = sum(prod(i, j, k) for k in range(84) if k != i and k != j)
        m.Add(sh + common == 1).OnlyEnforceIf(adj(i, j))
        m.Add(sh + common == 2).OnlyEnforceIf(adj(i, j).Not())
print("template %d dim %s k %d: built in %.1fs, %d variables, %d constraints" % (
    index, tpl["kernel_dimension"], len(GRID), time.time() - t0, len(m.Proto().variables), len(m.Proto().constraints)), flush=True)
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = seconds
solver.parameters.num_search_workers = workers
st = solver.Solve(m)
print(json.dumps({"index": index, "status": solver.StatusName(st), "wall": round(solver.WallTime(), 1),
                  "flags": FLAGS}), flush=True)
