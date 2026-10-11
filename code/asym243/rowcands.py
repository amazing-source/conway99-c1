"""Row-candidate counts for the far region of a general fixed substructure X (vertex, edge, line, two lines through
a point, grid): for a far vertex w, all N_F(w) compatible with the linear equations from the ball of X."""
import sys, numpy as np, time
from ortools.sat.python import cp_model
from lib243 import *
from regions import ball, grids_list

def row_cands(G, X, wlist, cap=2000):
    n = len(G); R = ball(G, X); F = sorted(set(range(n)) - R); Fi = {w: i for i, w in enumerate(F)}
    NB = [set(np.nonzero(G[u])[0].tolist()) for u in range(n)]
    out = []
    for w in wlist:
        if w not in Fi: continue
        m = cp_model.CpModel(); x = [m.NewBoolVar("") for _ in F]
        m.Add(x[Fi[w]] == 0); m.Add(sum(x) == len(NB[w] - R))
        for u in R:
            tgt = (1 if G[u, w] else 2) - len(NB[u] & NB[w] & R)
            m.Add(sum(x[Fi[z]] for z in NB[u] if z in Fi) == tgt)
        cnt = [0]
        class CB(cp_model.CpSolverSolutionCallback):
            def on_solution_callback(s_):
                cnt[0] += 1
                if cnt[0] >= cap: s_.StopSearch()
        s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
        s.parameters.max_time_in_seconds = 120
        r = s.Solve(m, CB()); out.append((cnt[0], s.StatusName(r)))
    return len(F), out

if __name__ == "__main__":
    G = np.load(sys.argv[1]) if sys.argv[1].endswith(".npy") else load_edges(sys.argv[1])
    tri = triangles(G); rng = np.random.default_rng(0)
    t = tri[0]; x = t[0]
    other = [l for l in tri if x in l and l != t][0]
    gl = grids_list(G)
    for name, X in (("vertex", [x]), ("edge", list(t[:2])), ("line", list(t)), ("two lines", sorted(set(t) | set(other))),
                    ("grid", gl[0])):
        R = ball(G, X); F = [w for w in range(len(G)) if w not in R]
        ws = [F[i] for i in rng.choice(len(F), 5, replace=False)]
        nF, res = row_cands(G, X, ws)
        print(f"{name:9s} |F|={nF:3d} candidates per sampled row: {res}", flush=True)
