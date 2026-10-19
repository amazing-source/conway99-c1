"""Grid skeleton of a root template (LAB 19/10/2026): the labels of the grid rectangles only.  Facts (grid perfect
domination, lambda = 1, mu = 2, letters):
  * a grid's 4 labels form the 4-cycle 00-01-11-10 (sides share a letter);
  * two grids sharing a line have no edge between their labels;
  * two disjoint grids are joined by a perfect matching (each label has exactly one neighbour in the other grid);
  * C2 between skeleton labels, counting shared letters and common skeleton neighbours, must not exceed the
    lambda/mu value; for two opposite corners of one grid it is already 2 inside the grid, so nothing else; for two
    adjacent corners of one grid the shared letter is the only common neighbour.
Unknowns: the perfect matchings between disjoint grids.  CP-SAT feasibility (INFEASIBLE = verdict on the skeleton,
which is a necessary sub-structure of the whole graph).
usage: python grid_skeleton.py <catalogue.json.gz> <index> <seconds> <workers>"""
import gzip
import json
import sys
from itertools import combinations, product

from ortools.sat.python import cp_model

tpl = json.load(gzip.open(sys.argv[1]))["open"][int(sys.argv[2])]["template"]
seconds, workers = float(sys.argv[3]), int(sys.argv[4])
ng = {tuple(e) for e in tpl["nongrid_edges"]}
GR = [q for q in combinations(range(7), 2) if q not in ng]
LAB = [(g, s, t) for g in GR for s in (0, 1) for t in (0, 1)]
lid = {l: i for i, l in enumerate(LAB)}
n = len(LAB)


def letters(l):
    (a, b), s, t = l
    return {(a, s), (b, t)}


m = cp_model.CpModel()
E = {}
for i, j in combinations(range(n), 2):
    gi, gj = LAB[i][0], LAB[j][0]
    if gi == gj:
        si, ti = LAB[i][1], LAB[i][2]; sj, tj = LAB[j][1], LAB[j][2]
        E[(i, j)] = 1 if (si == sj) != (ti == tj) else 0
    elif set(gi) & set(gj):
        E[(i, j)] = 0
    else:
        E[(i, j)] = m.NewBoolVar("")


def e(i, j):
    return E[(min(i, j), max(i, j))]


# perfect matchings between disjoint grids
for g, h in combinations(GR, 2):
    if set(g) & set(h):
        continue
    gl = [lid[(g, s, t)] for s in (0, 1) for t in (0, 1)]
    hl = [lid[(h, s, t)] for s in (0, 1) for t in (0, 1)]
    for i in gl:
        m.AddExactlyOne([e(i, j) for j in hl])
    for j in hl:
        m.AddExactlyOne([e(i, j) for i in gl])
# C2 upper bounds (and exact zero for the in-grid cases)
for i, j in combinations(range(n), 2):
    sh = len(letters(LAB[i]) & letters(LAB[j]))
    terms = []
    for k in range(n):
        if k in (i, j):
            continue
        a, b = e(i, k), e(j, k)
        if isinstance(a, int) and isinstance(b, int):
            if a and b:
                terms.append(1)
            continue
        if isinstance(a, int) or isinstance(b, int):
            c = a if isinstance(b, int) else b
            if (b if isinstance(b, int) else a) == 1:
                terms.append(c)
            continue
        p = m.NewBoolVar("")
        m.AddBoolAnd([a, b]).OnlyEnforceIf(p)
        m.AddBoolOr([a.Not(), b.Not()]).OnlyEnforceIf(p.Not())
        terms.append(p)
    eij = e(i, j)
    if isinstance(eij, int):
        m.Add(sh + sum(terms) <= (1 if eij else 2))
    else:
        m.Add(sh + sum(terms) <= 1).OnlyEnforceIf(eij)
        m.Add(sh + sum(terms) <= 2).OnlyEnforceIf(eij.Not())
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = seconds
solver.parameters.num_search_workers = workers
st = solver.Solve(m)
print(json.dumps({"index": int(sys.argv[2]), "grids": len(GR), "skeleton_labels": n, "status": solver.StatusName(st),
                  "wall": round(solver.WallTime(), 1)}))
