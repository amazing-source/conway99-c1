"""BvLS: candidate far-neighbourhoods per row (integer equations), then the 'other' candidates: symmetric? srg?"""
import numpy as np, time, pickle, os
from ortools.sat.python import cp_model
from graphs_test import bvls243, is_srg
A = bvls243(); n = 243
v = 0; a = int(np.nonzero(A[v])[0][0]); ap = [c for c in np.nonzero(A[v])[0] if A[a, c]][0]
ball = sorted(set([v, a, ap]) | set(np.nonzero(A[v])[0]) | set(np.nonzero(A[a])[0]) | set(np.nonzero(A[ap])[0]))
tri = [v, a, ap]; C = [u for u in ball if u not in tri]; far = [u for u in range(n) if u not in ball]
Af = A[np.ix_(far, far)]; deg = int(Af[0].sum()); F = len(far)
NB = [set(np.nonzero(A[u])[0]) for u in range(n)]
if os.path.exists("far_cands.pkl"):
    cands = pickle.load(open("far_cands.pkl", "rb"))
else:
    cands = []
    for wi, w in enumerate(far):
        m = cp_model.CpModel(); x = [m.NewBoolVar("") for _ in range(F)]
        m.Add(x[wi] == 0); m.Add(sum(x) == deg)
        for u in C:
            tgt = (2 - A[u, w]) - len(NB[u] & NB[w] & set(C))
            m.Add(sum(x[j] for j in range(F) if A[u, far[j]]) == tgt)
        sols = []
        class CB(cp_model.CpSolverSolutionCallback):
            def on_solution_callback(s_): sols.append(frozenset(j for j in range(F) if s_.Value(x[j])))
        s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
        s.Solve(m, CB()); cands.append(sols)
    pickle.dump(cands, open("far_cands.pkl", "wb"))
alt = []
for wi in range(F):
    tr = frozenset(np.nonzero(Af[wi])[0].tolist())
    o = [S for S in cands[wi] if S != tr]
    alt.append(o[0] if o else tr)
sym = all((wj in alt[wi]) == (wi in alt[wj]) for wi in range(F) for wj in range(F) if wi != wj)
diffs = sorted(set(len(alt[wi] ^ frozenset(np.nonzero(Af[wi])[0].tolist())) for wi in range(F)))
print("alternatives symmetric:", sym, "; |alt xor true| per row:", diffs, flush=True)
if sym:
    B2 = A.copy()
    for wi in range(F):
        for wj in range(F):
            B2[far[wi], far[wj]] = 1 if wj in alt[wi] else 0
    ok = is_srg(B2, 243, 22, 1, 2)
    print("twin graph (far block replaced) is srg(243,22,1,2):", ok, flush=True)
# mixed choices: how many rows can take the alternative while keeping symmetry with true rows elsewhere?
