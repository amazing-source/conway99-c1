"""All regular spreads of an srg(v,k,1,2): sets of v/3 pairwise disjoint lines covering V such that any two of them are
joined by 0 or 3 edges (equivalently, an equitable partition into lines).  CP-SAT exact enumeration.
Usage: python3 spreads.py GRAPH(.npy|.edges) [limit]"""
import sys, itertools, numpy as np
from ortools.sat.python import cp_model
from lib243 import load_edges, triangles


def regular_spreads(G, limit=1000):
    n = len(G); L = triangles(G); m = cp_model.CpModel()
    x = [m.NewBoolVar("") for _ in L]
    at = [[] for _ in range(n)]
    for i, l in enumerate(L):
        for p in l: at[p].append(i)
    for p in range(n): m.AddExactlyOne([x[i] for i in at[p]])
    Lm = np.zeros((len(L), n), dtype=np.int64)
    for i, l in enumerate(L): Lm[i, list(l)] = 1
    E = Lm @ G @ Lm.T
    bad = np.argwhere(np.triu((E == 1) | (E == 2), 1))
    for i, j in bad:
        if not (set(L[i]) & set(L[j])): m.AddBoolOr([x[i].Not(), x[j].Not()])
    sols = []
    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(s_):
            sols.append(sorted(L[i] for i in range(len(L)) if s_.Value(x[i])))
            if len(sols) >= limit: s_.StopSearch()
    s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
    st = s.Solve(m, CB())
    return sols, s.StatusName(st)


if __name__ == "__main__":
    p = sys.argv[1]
    G = np.load(p) if p.endswith(".npy") else load_edges(p)
    sols, st = regular_spreads(G, int(sys.argv[2]) if len(sys.argv) > 2 else 1000)
    print(p, "regular spreads:", len(sols), "(status", st + ")")
