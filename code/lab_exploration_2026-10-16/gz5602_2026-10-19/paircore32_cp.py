"""K4 family, 32-vertex level as a small exact model (LAB 19/10/2026).  Templates: grid graph contains a K4 on
D = {0,1,2,3} and exactly the edge (4,5) of the complementary triangle, so H_46 = -H_56 (universal relations) and the
pair core S = Q46 + Q56 (shared line a = 6) carries one of the 114 labelled pair cores of paircores8.json.
Unknowns: for each of the 24 labels g of the six D-grids (corner (s_j, s_k) fixed by g) its pair of neighbours in S.
Constraints (each proved in NUIT_2026-10-19.md):
  (sum)   every pair p of S is covered by exactly T_p labels of D-grids (all outside 2-neighbour labels are D-grid labels);
  (dom)   every vertex y of S has exactly one neighbour in each D-grid (perfect domination, y is not adjacent to its
          letters);
  (opp)   inside a grid, if a vertex z of the pair E is K-adjacent to both ends of the pair F, the corners of E and F are
          opposite (mu(z, g_F) = 2);
  (let)   two labels of two D-grids sharing a line, with the same letter on it, have pairs sharing at most one vertex
          (the letter is a common neighbour, they are not adjacent);
  (split) for y in S and l in D: y has exactly 2 label-neighbours at each letter of l; the 3 D-grids containing l give
          one each and only one more can come from Q_l4 + Q_l5 + Q_l6, so the 3 do not all carry the same letter of l.
Counts all solutions per core (CP-SAT enumeration of a small 0/1 model; independent brute-force check on request).
usage: python paircore32_cp.py [first last]"""
import json
import sys
from itertools import combinations

from ortools.sat.python import cp_model

cores = json.load(open("paircores8.json"))
first, last = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, len(cores))
D = [0, 1, 2, 3]
DG = list(combinations(D, 2))
LAB = [(G, s, t) for G in DG for s in (0, 1) for t in (0, 1)]     # label of grid G=(j,k) at corner (s_j, s_k)
P8 = list(combinations(range(8), 2))


def adjacent_corner(g, h):
    return g[0] == h[0] and ((g[1] == h[1]) != (g[2] == h[2]))


class Counter_(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        super().__init__(); self.n = 0

    def on_solution_callback(self):
        self.n += 1


total = 0
res = []
for ci in range(first, min(last, len(cores))):
    core = cores[ci]
    K = {tuple(e) for e in core["edges"]}
    nb = [set() for _ in range(8)]
    for i, j in K:
        nb[i].add(j); nb[j].add(i)
    T = {tuple(map(int, k.split("-"))): v for k, v in core["T"].items()}
    m = cp_model.CpModel()
    x = {(g, p): m.NewBoolVar("") for g in range(24) for p in P8 if T[p] > 0}
    for g in range(24):
        m.AddExactlyOne([x[(g, p)] for p in P8 if (g, p) in x])
    for p in P8:
        if T[p] > 0:
            m.Add(sum(x[(g, p)] for g in range(24)) == T[p])
    for gi, G in enumerate(DG):
        labs = [i for i, l in enumerate(LAB) if l[0] == G]
        for y in range(8):
            m.Add(sum(x[(g, p)] for g in labs for p in P8 if y in p and (g, p) in x) == 1)
        # (opp)
        for g, h in combinations(labs, 2):
            if not adjacent_corner(LAB[g], LAB[h]):
                continue
            for E in P8:
                for F in P8:
                    if (g, E) in x and (h, F) in x and not set(E) & set(F):
                        if any(F[0] in nb[z] and F[1] in nb[z] for z in E) or any(E[0] in nb[z] and E[1] in nb[z] for z in F):
                            m.AddBoolOr([x[(g, E)].Not(), x[(h, F)].Not()])
    # (let)
    for g, h in combinations(range(24), 2):
        G, H = LAB[g][0], LAB[h][0]
        common = set(G) & set(H)
        if G == H or not common:
            continue
        (l,) = common
        if LAB[g][1 + G.index(l)] != LAB[h][1 + H.index(l)]:
            continue
        for p in P8:
            if (g, p) in x and (h, p) in x:
                m.AddBoolOr([x[(g, p)].Not(), x[(h, p)].Not()])
    # (split)
    for y in range(8):
        for l in D:
            for s in (0, 1):
                labs = [i for i, lb in enumerate(LAB) if l in lb[0] and lb[1 + lb[0].index(l)] == s]
                m.Add(sum(x[(g, p)] for g in labs for p in P8 if y in p and (g, p) in x) <= 2)
                m.Add(sum(x[(g, p)] for g in labs for p in P8 if y in p and (g, p) in x) >= 1)
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.max_time_in_seconds = 60
    cb = Counter_()
    st = solver.Solve(m, cb)
    res.append((ci, core["e"], solver.StatusName(st), cb.n))
    total += cb.n
    print(ci, core["e"], solver.StatusName(st), cb.n, flush=True)
print("cores", len(res), "total solutions", total, "statuses", {s for _, _, s, _ in res})
json.dump(res, open("paircore32_cp_%d_%d.json" % (first, last), "w"))
