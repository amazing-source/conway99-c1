"""Normal form of the family (dim 6, pair core Q01 + Q02 with H01 = -H02, Q12 grid, D-grids 45, 46, 56, non-grid
34, 35, 36): exact catalogue of the 20-vertex level (core + the three D-grids) for Codex (LAB 19/10/2026).
Facts (NUIT_2026-10-19.md section 7, paircore8_check.py): the core S = Q01 + Q02 is one of 114 labelled 2-regular
cores (a = 0, b = 1, c = 2: vertices 0..3 = Q01 corners (s0, s1), 4..7 = Q02 corners (s0, s2)); the 24 labels of the
six rectangles on D = {3,4,5,6} have exactly 2 neighbours in S and cover the deficits T exactly; a D-grid dominates S
perfectly (a perfect matching M_g); so M45 + M46 + M56 + (the 12 pairs of the labels of 34, 35, 36) = T.
Constraints: (dom), (opp) inside each grid; (let) for ANY two labels sharing a letter: their core pairs are not identical
(the letter plus two common core neighbours would exceed lambda = 1 or mu = 2); (q) for a core vertex y and a letter
(l, s) of a line l off y's lines: at most 2 neighbours of y carry (l, s).
Two stages: (1) exact enumeration of the 12 grid labels' pairs with the constraints among them and R = T - sum M >= 0
(enumerate_all_solutions, status must be OPTIMAL = complete); (2) for each such state, existence of a cover of R by the
12 non-grid D-labels under (let) and (q) (feasibility solve).  A state is kept iff (2) is feasible; any UNKNOWN is
reported and kept (never dropped).
usage: python k3family_level20.py <out.json> <core indices, comma separated>"""
import json
import sys
from itertools import combinations

from ortools.sat.python import cp_model

outp = sys.argv[1]
only = [int(x) for x in sys.argv[2].split(",")]
cores = json.load(open("paircores8.json"))
V = [("A", s, t) for s in (0, 1) for t in (0, 1)] + [("B", s, t) for s in (0, 1) for t in (0, 1)]


def vletters(v):
    return {(0, v[1]), (1, v[2])} if v[0] == "A" else {(0, v[1]), (2, v[2])}


GR = [(4, 5), (4, 6), (5, 6)]
NG = [(3, 4), (3, 5), (3, 6)]
LAB = [(R, s, t) for R in GR + NG for s in (0, 1) for t in (0, 1)]
lletters = [{(R[0], s), (R[1], t)} for R, s, t in LAB]
P8 = list(combinations(range(8), 2))


def adjacent_corner(i, j):
    (R, s, t), (R2, s2, t2) = LAB[i], LAB[j]
    return R == R2 and ((s == s2) != (t == t2))


def common_constraints(m, x, labs, nb, ycount):
    for g, h in combinations(labs, 2):
        if lletters[g] & lletters[h]:
            for p in P8:
                if (g, p) in x and (h, p) in x:
                    m.AddBoolOr([x[(g, p)].Not(), x[(h, p)].Not()])
    for y in range(8):
        own = {l for l, _ in vletters(V[y])}
        for line in (3, 4, 5, 6):
            if line in own:
                continue
            for s in (0, 1):
                ls = [g for g in labs if (line, s) in lletters[g]]
                m.Add(sum(x[(g, p)] for g in ls for p in P8 if y in p and (g, p) in x) + ycount.get((y, line, s), 0) <= 2)


class Collect(cp_model.CpSolverSolutionCallback):
    def __init__(self, x):
        super().__init__(); self.x = x; self.sols = []

    def on_solution_callback(self):
        self.sols.append(tuple(next(p for p in P8 if (g, p) in self.x and self.Value(self.x[(g, p)])) for g in range(12)))


result = []
for ci in only:
    core = cores[ci]
    nb = [set() for _ in range(8)]
    for i, j in core["edges"]:
        nb[i].add(j); nb[j].add(i)
    T = {tuple(map(int, k.split("-"))): v for k, v in core["T"].items()}
    # stage 1: the 12 grid labels
    m = cp_model.CpModel()
    x = {(g, p): m.NewBoolVar("") for g in range(12) for p in P8 if T[p] > 0}
    for g in range(12):
        m.AddExactlyOne([x[(g, p)] for p in P8 if (g, p) in x])
    for p in P8:
        if T[p] > 0:
            m.Add(sum(x[(g, p)] for g in range(12) if (g, p) in x) <= T[p])
    for gi in range(3):
        labs = [i for i in range(12) if LAB[i][0] == GR[gi]]
        for y in range(8):
            m.Add(sum(x[(g, p)] for g in labs for p in P8 if y in p and (g, p) in x) == 1)
        for g, h in combinations(labs, 2):
            if not adjacent_corner(g, h):
                continue
            for E in P8:
                for F in P8:
                    if (g, E) in x and (h, F) in x and not set(E) & set(F):
                        if any(F[0] in nb[z] and F[1] in nb[z] for z in E) or any(E[0] in nb[z] and E[1] in nb[z] for z in F):
                            m.AddBoolOr([x[(g, E)].Not(), x[(h, F)].Not()])
    common_constraints(m, x, list(range(12)), nb, {})
    cb = Collect(x)
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = 240
    st1 = solver.StatusName(solver.Solve(m, cb))
    kept, dead, unk = [], 0, 0
    for state in cb.sols:
        R = dict(T)
        for p in state:
            R[p] -= 1
        ycount = {}
        for g, p in enumerate(state):
            for y in p:
                for (line, s) in lletters[g]:
                    ycount[(y, line, s)] = ycount.get((y, line, s), 0) + 1
        m2 = cp_model.CpModel()
        x2 = {(g, p): m2.NewBoolVar("") for g in range(12, 24) for p in P8 if R[p] > 0}
        for g in range(12, 24):
            ch = [x2[(g, p)] for p in P8 if (g, p) in x2]
            if not ch:
                m2.AddBoolOr([]); break
            m2.AddExactlyOne(ch)
        for p in P8:
            if R[p] > 0:
                m2.Add(sum(x2[(g, p)] for g in range(12, 24) if (g, p) in x2) == R[p])
        # (let) between non-grid labels and between non-grid and grid labels sharing a letter
        for g, h in combinations(range(12, 24), 2):
            if lletters[g] & lletters[h]:
                for p in P8:
                    if (g, p) in x2 and (h, p) in x2:
                        m2.AddBoolOr([x2[(g, p)].Not(), x2[(h, p)].Not()])
        for g in range(12, 24):
            for h in range(12):
                if lletters[g] & lletters[h] and (g, state[h]) in x2:
                    m2.Add(x2[(g, state[h])] == 0)
        for y in range(8):
            own = {l for l, _ in vletters(V[y])}
            for line in (3, 4, 5, 6):
                if line in own:
                    continue
                for s in (0, 1):
                    ls = [g for g in range(12, 24) if (line, s) in lletters[g]]
                    m2.Add(sum(x2[(g, p)] for g in ls for p in P8 if y in p and (g, p) in x2) + ycount.get((y, line, s), 0) <= 2)
        s2 = cp_model.CpSolver(); s2.parameters.max_time_in_seconds = 20; s2.parameters.num_search_workers = 1
        r2 = s2.StatusName(s2.Solve(m2))
        if r2 in ("FEASIBLE", "OPTIMAL"):
            kept.append(state)
        elif r2 == "INFEASIBLE":
            dead += 1
        else:
            unk += 1; kept.append(state)
    result.append({"core": ci, "e": core["e"], "stage1": st1, "stage1_states": len(cb.sols), "kept": kept,
                   "dead_by_residual": dead, "unknown_residual": unk})
    print(ci, core["e"], "stage1", st1, len(cb.sols), "kept", len(kept), "dead", dead, "unknown", unk, flush=True)
json.dump({"scope": __doc__, "labels_of_grids": LAB[:12], "results": result}, open(outp, "w"))
