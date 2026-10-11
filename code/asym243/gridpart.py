"""Equitable partitions of an srg(v,k,1,2) into 3x3 grids (each vertex has 0 or 1 neighbour in every other grid,
uniformly over the grid).  Usage: python3 gridpart.py GRAPH [limit]"""
import sys, numpy as np
from ortools.sat.python import cp_model
from lib243 import load_edges
from regions import grids_list
G = np.load(sys.argv[1]) if sys.argv[1].endswith(".npy") else load_edges(sys.argv[1])
n = len(G); gl = grids_list(G)
m = cp_model.CpModel(); x = [m.NewBoolVar("") for _ in gl]
at = [[] for _ in range(n)]
for i, g in enumerate(gl):
    for p in g: at[p].append(i)
for p in range(n): m.AddExactlyOne([x[i] for i in at[p]])
Mi = np.zeros((len(gl), n), dtype=np.int64)
for i, g in enumerate(gl): Mi[i, g] = 1
E = Mi @ G @ Mi.T
bad = np.argwhere(np.triu((E > 0) & (E < 9), 1))
for i, j in bad:
    if not (set(gl[i]) & set(gl[j])): m.AddBoolOr([x[i].Not(), x[j].Not()])
cnt = [0]
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(s_):
        cnt[0] += 1
        if cnt[0] >= int(sys.argv[2]) if len(sys.argv) > 2 else 1000: s_.StopSearch()
s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.max_time_in_seconds = 300
st = s.Solve(m, CB())
print(sys.argv[1], "grids", len(gl), "equitable grid partitions:", cnt[0], s.StatusName(st))
