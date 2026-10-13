"""Lab session, 2026-10-13. Mission "C2 without computation", step 1: the region left by modular forms.

Same linear programme as forcing_bound.py (N, I with 1 <= E <= T, S, P on the window), for one T.
Prints, for the low coefficients, their minimum and maximum over the feasible region (floating-point LP).
Frame facts to compare with: the 84 vectors +-u_o are integral vectors of class 0 with E = 21, the 14 vectors +-h_c
are integral vectors of class 0 with E = 28.
python forcing_region.py <EMAX> <T>        scipy (HiGHS), seconds."""
import sys, pickle
import numpy as np
from scipy.optimize import linprog

EMAX, T = int(sys.argv[1]), int(sys.argv[2])
desc, tabs = pickle.load(open("gen_tables_%d.pkl" % EMAX, "rb"))
keys = sorted(k for k in set().union(*[set(t) for t in tabs]) if any(t.get(k, 0) for t in tabs))
kidx = {k: i for i, k in enumerate(keys)}
M = np.array([[float(t.get(k, 0)) for k in keys] for t in tabs])
scale = np.maximum(1.0, np.abs(M).max(axis=0))
Ms = M / scale
basis = []
cur = np.zeros((0, Ms.shape[1]))
for i in range(len(Ms)):
    trial = np.vstack([cur, Ms[i]])
    if np.linalg.matrix_rank(trial, tol=1e-9) > len(basis):
        basis.append(i)
        cur = trial
Bm = M[basis]
nb = len(basis)
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
    elif kind == "S" and e4 < 46:
        Aeq.append(col)
        beq.append(0.0)
Aeq = np.array(Aeq)
beq = np.array(beq)
eqs = np.maximum(1.0, np.abs(Aeq).max(axis=1))


def opt(vec, sign):
    res = linprog(c=sign * vec, A_ub=-(Bm / scale).T, b_ub=np.zeros(len(keys)), A_eq=Aeq / eqs[:, None], b_eq=beq / eqs,
                  bounds=[(None, None)] * nb, method="highs")
    return None if res.status != 0 else sign * res.fun


print("T = %d, basis %d, window E <= %d" % (T, nb, EMAX))
# sums over classes for each E
byE = {}
for k in keys:
    byE.setdefault((k[0], k[2]), []).append(k)
rows = []
for (kind, e4), ks in sorted(byE.items(), key=lambda kv: (kv[0][1], kv[0][0])):
    if e4 > 4 * 30:
        continue
    vec = sum(Bm[:, kidx[k]] for k in ks)
    s = np.abs(vec).max()
    lo, hi = opt(vec / s, 1), opt(vec / s, -1)
    if lo is None:
        print("infeasible")
        break
    lo, hi = lo * s, hi * s
    if abs(lo) > 1e-6 or abs(hi) > 1e-6:
        rows.append((e4 / 4, kind, len(ks), lo, hi))
for e, kind, n, lo, hi in rows:
    print("   %s  E = %-5g (%d classes): total number of vectors between %.2f and %.2f" % (kind, e, n, lo, hi))
for name, key in (("class 0, E = 14 (roots orthogonal to y1, y2)", ("I", (0, 0), 56)), ("class 0, E = 21 (frame: at least 84)", ("I", (0, 0), 84)), ("class 0, E = 28 (frame: at least 14)", ("I", (0, 0), 112))):
    if key in kidx:
        vec = Bm[:, kidx[key]]
        s = np.abs(vec).max()
        lo, hi = opt(vec / s, 1), opt(vec / s, -1)
        print("   %s: between %.2f and %.2f" % (name, lo * s, hi * s))
