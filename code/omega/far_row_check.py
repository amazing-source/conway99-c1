"""BvLS check of the far-row equations for a triangle T = {v,a,a'}:
  (int)  for every u in C:  #{w' in N_far(w) : w' ~ u} = (2 - A_uw) - |N_C(u) & N_C(w)|
  (real) sum_{w' in N_far(w)} (P_Z)_{w w'} = r (P_Z)_ww - (r - s) d_w ,  d_w = residual E_s-norm of w (from its column)
Count, for a few far vertices w, all |N_far(w)|-subsets of far \\ {w} satisfying (int), then how many satisfy (real)."""
import numpy as np, sys, time
from ortools.sat.python import cp_model
from graphs_test import bvls243
A = bvls243(); n, k, r, s = 243, 22, 4, -5
w_, V = np.linalg.eigh(A.astype(float)); Es = V[:, np.abs(w_ - s) < 1e-6]
v = 0; a = int(np.nonzero(A[v])[0][0]); ap = [c for c in np.nonzero(A[v])[0] if A[a, c]][0]
ball = sorted(set([v, a, ap]) | set(np.nonzero(A[v])[0]) | set(np.nonzero(A[a])[0]) | set(np.nonzero(A[ap])[0]))
tri = [v, a, ap]; C = [u for u in ball if u not in tri]; far = [u for u in range(n) if u not in ball]
BC = A[np.ix_(C, far)].astype(float)
# P_Z = projection onto ker(B_C^T) in R^far
U_, sv, Vt = np.linalg.svd(BC); rk = int((sv > 1e-8).sum()); Zb = Vt[rk:].T; PZ = Zb @ Zb.T
# residual E_s norm of far vertices w.r.t. ball: d_w = (P_s)_ww where P_s = projection of E_s-vanishing-on-ball part
Ub, sb, Vbt = np.linalg.svd(Es[ball, :]); nul = Vbt[int((sb > 1e-8).sum()):].T; Fs = (Es @ nul)[far]
d = (Fs ** 2).sum(1)
Af = A[np.ix_(far, far)]
print("identity check (true graph): max |row sum - target| =",
      np.abs((Af * PZ).sum(1) - (r * np.diag(PZ) - (r - s) * d)).max())
deg = int(Af[0].sum()); print("far degree =", deg, "|far| =", len(far))
Cn = {u: set(np.nonzero(A[u, C])[0]) for u in range(len(C))}
for wi in [0, 7, 42]:
    w = far[wi]
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{j}") for j in range(len(far))]
    m.Add(x[wi] == 0); m.Add(sum(x) == deg)
    for ui, u in enumerate(C):
        tgt = (2 - A[u, w]) - len(set(np.nonzero(A[u])[0]) & set(np.nonzero(A[w])[0]) & set(C))
        m.Add(sum(x[j] for j in range(len(far)) if A[u, far[j]]) == tgt)
    sols = []
    class CB(cp_model.CpSolverSolutionCallback):
        def __init__(s_): super().__init__()
        def on_solution_callback(s_):
            sols.append([j for j in range(len(far)) if s_.Value(x[j])])
    solver = cp_model.CpSolver(); solver.parameters.enumerate_all_solutions = True
    solver.parameters.max_time_in_seconds = 300; solver.parameters.num_workers = 1
    t = time.time(); st = solver.Solve(m, CB())
    tgt_real = r * PZ[wi, wi] - (r - s) * d[wi]
    good = [S for S in sols if abs(PZ[wi, S].sum() - tgt_real) < 1e-7]
    true = sorted(np.nonzero(Af[wi])[0].tolist())
    print(f"w={wi}: integer-constraint solutions {len(sols)} ({solver.StatusName(st)}, {time.time()-t:.1f}s);"
          f" also satisfying the real equation: {len(good)}; true neighbourhood among them: {true in [sorted(S) for S in good]}", flush=True)
