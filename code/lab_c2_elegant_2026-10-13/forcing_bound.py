"""Lab session, 2026-10-13. Mission "C2 without computation", step 1: what do modular forms force?

Input: gen_tables_<EMAX>.pkl (span_rank.py), generators spanning the whole space (rank 61 = dimension).
For T = 7, 8, ...: linear programme
   N : coefficient (integral, class 0, E = 0) = 1
   I : no integral vector with 1 <= E <= T
   S : no shadow vector with E < 11.5          (option NOSHADOW=1 drops it)
   P : all coefficients >= 0 on the window E <= EMAX
Feasible  => modular forms alone do not force a vector with E <= T.
Infeasible => every (U; y1, y2) satisfying S has an integral vector with 1 <= E <= T (floating-point LP verdict; an exact
              certificate would have to be extracted before this is used in a proof).
Also printed: dimension of the affine space cut out by N + I + S.
python forcing_bound.py <EMAX> <T first> <T last>        scipy (HiGHS), seconds."""
import sys, os, pickle
import numpy as np
from scipy.optimize import linprog

EMAX, T0, T1 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
desc, tabs = pickle.load(open("gen_tables_%d.pkl" % EMAX, "rb"))
keys = sorted(k for k in set().union(*[set(t) for t in tabs]) if any(t.get(k, 0) for t in tabs))
kidx = {k: i for i, k in enumerate(keys)}
M = np.array([[float(t.get(k, 0)) for k in keys] for t in tabs])
# basis: greedy choice of independent rows (floating rank on scaled columns)
scale = np.maximum(1.0, np.abs(M).max(axis=0))
Ms = M / scale
basis = []
cur = np.zeros((0, Ms.shape[1]))
for i in range(len(Ms)):
    trial = np.vstack([cur, Ms[i]])
    if np.linalg.matrix_rank(trial, tol=1e-9) > len(basis):
        basis.append(i)
        cur = trial
print("basis of %d forms among %d generators" % (len(basis), len(tabs)))
Bm = M[basis]
nb = len(basis)
noshadow = os.environ.get("NOSHADOW") is not None
for T in range(T0, T1 + 1):
    Aeq = []
    beq = []
    for k in keys:
        kind, cl, e4 = k
        col = Bm[:, kidx[k]]
        if kind == "I" and cl == (0, 0) and e4 == 0:
            Aeq.append(col)
            beq.append(1.0)
        elif kind == "I" and 0 < e4 <= 4 * T:
            Aeq.append(col)
            beq.append(0.0)
        elif kind == "S" and e4 < 46 and not noshadow:
            Aeq.append(col)
            beq.append(0.0)
    Aeq = np.array(Aeq)
    beq = np.array(beq)
    eqs = np.maximum(1.0, np.abs(Aeq).max(axis=1))
    rk = np.linalg.matrix_rank(Aeq / eqs[:, None], tol=1e-9)
    res = linprog(c=np.zeros(nb), A_ub=-(Bm / scale).T, b_ub=np.zeros(len(keys)), A_eq=Aeq / eqs[:, None], b_eq=beq / eqs,
                  bounds=[(None, None)] * nb, method="highs")
    verdict = {0: "FEASIBLE", 2: "INFEASIBLE"}.get(res.status, "status %d" % res.status)
    print("T = %2d: %d equalities of rank %d, free dimension %d; with positivity: %s" % (T, len(beq), rk, nb - rk, verdict), flush=True)
    if res.status == 0 and T == T0:
        tab = res.x @ Bm
        small = sorted((k[2] / 4, k[0], k[1], tab[kidx[k]]) for k in keys if k[2] <= 4 * 15 and abs(tab[kidx[k]]) > 1e-6)
        print("   one feasible table, non-zero entries with E <= 15: " + "; ".join("%s E=%g %s: %.2f" % (kd, e, cl, v) for e, kd, cl, v in small[:24]))
