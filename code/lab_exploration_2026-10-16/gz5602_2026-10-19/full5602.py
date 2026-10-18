"""Full C2 model of the second subconstituent of gz 5602 (LAB 19/10/2026; own code).

Vertices: root x, 14 letters (a, s) (line a = 0..6, s = 0/1), 84 labels (q, s_a, s_b), q = {a < b}.  Known edges:
x - letters, letter - mate letter, letter (a, s) - labels of rectangles q containing a with corner s on a.
Unknown: the 3486 label-label pairs (Boolean).  Constraints (srg(99,14,1,2), all exact):
  quotas  : a label w has exactly 1 label-neighbour adjacent to each letter of its own lines, and exactly 2 adjacent to
            each letter of any other line (lambda/mu with the letters);
  C2      : two labels have 1 (adjacent) or 2 (non-adjacent) common neighbours, counting shared letters and common
            label-neighbours (products linearised);
  template: the 7 grid rectangles of 5602 carry the grid 4-cycle (sides adjacent, diagonals not); E3 (e(q) != 3) and
            e(q) <= 3 on non-grid rectangles; the 8-core facts of Codex re-checked by core8_check.py: H03 = -H12 rows
            (z03 + z12 = base03 + base12) and e03 = e12 = 2.
Optional --fix <json>: a partial configuration (list of label pairs with 0/1) to extend, e.g. a 36-vertex survivor.
A FEASIBLE answer would be a Conway graph with root template 5602 (the template structure is implied by the
constraints only partly: block partitions are not imposed beyond these consequences); INFEASIBLE is a CP-SAT verdict.
usage: python full5602.py <seconds> <workers> [--fix file.json] [--core] [--out solution.json]"""
import json
import sys
import time
from itertools import combinations

from ortools.sat.python import cp_model

seconds, workers = float(sys.argv[1]), int(sys.argv[2])
FLAGS = sys.argv[3:]
RECT = list(combinations(range(7), 2))
GRID = [(0, 1), (0, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 6)]
L = [(q, sa, sb) for q in RECT for sa in (0, 1) for sb in (0, 1)]
lid = {w: i for i, w in enumerate(L)}


def lets(w):
    (a, b), sa, sb = w
    return {(a, sa), (b, sb)}


m = cp_model.CpModel()
A = {}
for i, j in combinations(range(84), 2):
    A[(i, j)] = m.NewBoolVar("a%d_%d" % (i, j))


def adj(i, j):
    return A[(min(i, j), max(i, j))]


# letters' label neighbourhoods
nbr_of_letter = {(a, s): [lid[w] for w in L if (a, s) in lets(w)] for a in range(7) for s in (0, 1)}
# quotas
for i, w in enumerate(L):
    own = {l[0] for l in lets(w)}
    for a in range(7):
        for s in (0, 1):
            cnt = sum(adj(i, j) for j in nbr_of_letter[(a, s)] if j != i)
            m.Add(cnt == (1 if a in own else 2))
# grid rectangles: 4-cycle (sides adjacent, diagonals not)
for q in GRID:
    for sa in (0, 1):
        for sb in (0, 1):
            i = lid[(q, sa, sb)]
            m.Add(adj(i, lid[(q, sa, 1 - sb)]) == 1)
            m.Add(adj(i, lid[(q, 1 - sa, sb)]) == 1)
            if (sa, sb) == (0, 0) or (sa, sb) == (0, 1):
                m.Add(adj(i, lid[(q, 1 - sa, 1 - sb)]) == 0)
# non-grid rectangles: e(q) <= 2 (E3 excludes 3; 4 would be a grid)
for q in RECT:
    if q in GRID:
        continue
    ids = [lid[(q, sa, sb)] for sa in (0, 1) for sb in (0, 1)]
    m.Add(sum(adj(i, j) for i, j in combinations(ids, 2)) <= 2)
# 5602 core facts: z03 + z12 = base03 + base12 for every label; e03 = e12 = 2
Q03 = [lid[((0, 3), sa, sb)] for sa in (0, 1) for sb in (0, 1)]
Q12 = [lid[((1, 2), sa, sb)] for sa in (0, 1) for sb in (0, 1)]


def base(q, f):
    return 2 if f == q else (0 if set(f) & set(q) else 1)


if "--core" in FLAGS:
    for i, w in enumerate(L):
        z = sum(adj(i, j) for j in Q03 + Q12 if j != i)
        m.Add(z == base(w[0], (0, 3)) + base(w[0], (1, 2)))
    for ids in (Q03, Q12):
        m.Add(sum(adj(i, j) for i, j in combinations(ids, 2)) == 2)
# C2 for label pairs: common neighbours = shared letters + common label-neighbours
P = {}


def prod(i, j, k):
    """Boolean for 'k adjacent to both i and j' (k distinct from i, j)"""
    key = (min(i, j), max(i, j), k)
    if key not in P:
        b = m.NewBoolVar("")
        m.AddBoolAnd([adj(i, k), adj(j, k)]).OnlyEnforceIf(b)
        m.AddBoolOr([adj(i, k).Not(), adj(j, k).Not()]).OnlyEnforceIf(b.Not())
        P[key] = b
    return P[key]


t0 = time.time()
for i, j in combinations(range(84), 2):
    sh = len(lets(L[i]) & lets(L[j]))
    common = sum(prod(i, j, k) for k in range(84) if k != i and k != j)
    # adjacent: sh + common == 1 ; not adjacent: sh + common == 2
    m.Add(sh + common == 1).OnlyEnforceIf(adj(i, j))
    m.Add(sh + common == 2).OnlyEnforceIf(adj(i, j).Not())
if "--fix" in FLAGS:
    fx = json.load(open(FLAGS[FLAGS.index("--fix") + 1]))
    for (wi, wj, v) in fx["pairs"]:
        i, j = lid[tuple([tuple(wi[0]), wi[1], wi[2]])], lid[tuple([tuple(wj[0]), wj[1], wj[2]])]
        m.Add(adj(i, j) == v)
print("model built in %.1fs: %d variables, %d constraints" % (time.time() - t0, len(m.Proto().variables),
                                                              len(m.Proto().constraints)), flush=True)
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = seconds
solver.parameters.num_search_workers = workers
st = solver.Solve(m)
print(json.dumps({"status": solver.StatusName(st), "wall": round(solver.WallTime(), 1)}))
if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    edges = [(L[i], L[j]) for (i, j), v in A.items() if solver.Value(v)]
    out = FLAGS[FLAGS.index("--out") + 1] if "--out" in FLAGS else "full5602_solution.json"
    json.dump({"label_edges": edges}, open(out, "w"))
    print("SOLUTION WRITTEN (to be verified as an srg(99,14,1,2) by an independent checker)")
