"""C1, lab session, 2026-10-08. Codex's neighbour-moment LP for the twin bound (its note 196), with the cut of its note 203.
  python profile_lp2.py <codex-grid-hub-profiles.json>
Model (Codex's export, source code/codex/grid_neighbour_moment_bounds.py): for every integer s = 0..73 (number of
vertices with e >= 14, the set S), variables x[profile, d] >= 0 = number of vertices with profile (e pairs of lines in
a grid, c cherries, h2, u6 lines in six grids) and d neighbours in S, 0 <= d <= min(s - [e>=14], 14 if e >= 14 else 2 h2).
Equalities: sum inside = s; sum outside = 99 - s; sum e x = 9 rho; sum d x = 14 s; sum (d^2 + [e>=14] d) x = 12 s + 2 s^2.
Inequalities: sum_inside d x <= 3 s + s^2/9; P >= 6 rho; P + 5 rho <= 1386; rho <= 126; P <= 852.
Objectives: tau_g = sum c x / 3; tau_bound = P - 6 rho + sum c x / 3.
NEW CUT (note 203, from the rank bound 56 - r mod 7, r >= 37): sum_v (2 [u6 = 1] + [u6 = 2] - 3 [u6 = 3]) >= 0.
Floating LP (HiGHS). Prints the maxima over s without and with the cut, and tau_g as a function of rho."""
import sys, json
import numpy as np
from scipy.optimize import linprog
D = json.load(open(sys.argv[1])); prof = D["refined_profiles"]
def solve(s, cut, objective, rho_fixed=None):
    cols = []
    for (e, c, h2, u6) in prof:
        ins = 1 if e >= 14 else 0
        if ins and s == 0: continue
        dmax = min(s - ins, 14 if ins else 2 * h2)
        for d in range(0, dmax + 1): cols.append((e, c, u6, ins, d))
    n = len(cols); E = np.array([c_[0] for c_ in cols], float); C = np.array([c_[1] for c_ in cols], float); U = np.array([c_[2] for c_ in cols]); I = np.array([c_[3] for c_ in cols], float); Dn = np.array([c_[4] for c_ in cols], float)
    # variables: x (n), rho, P
    z = lambda *v: np.concatenate([np.zeros(n), v])
    A_eq = [np.concatenate([I, [0, 0]]), np.concatenate([1 - I, [0, 0]]), np.concatenate([E, [-9, 0]]), np.concatenate([Dn, [0, 0]]), np.concatenate([Dn * Dn + I * Dn, [0, 0]])]
    b_eq = [s, 99 - s, 0, 14 * s, 12 * s + 2 * s * s]
    A_ub = [np.concatenate([I * Dn, [0, 0]]), z(6, -1), z(5, 1)]; b_ub = [3 * s + s * s / 9, 0, 1386]
    if cut: A_ub.append(np.concatenate([-(2.0 * (U == 1) + 1.0 * (U == 2) - 3.0 * (U == 3)), [0, 0]])); b_ub.append(0)
    if rho_fixed is not None: A_eq.append(z(1, 0)); b_eq.append(rho_fixed)
    obj = np.concatenate([-C / 3, [0, 0]]) if objective == "tau_g" else np.concatenate([-C / 3, [6, -1]])
    r = linprog(obj, A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq), b_eq=b_eq, bounds=[(0, None)] * n + [(0, 126), (0, 852)], method="highs")
    if r.status != 0: return None
    x = r.x; return -r.fun, x[n], x[n + 1], float((x[:n] * (U == 3)).sum()), float((x[:n] * (U >= 1)).sum())
for objective in ("tau_bound", "tau_g"):
    for cut in (False, True):
        best = None
        for s in range(0, 74):
            o = solve(s, cut, objective)
            if o and (best is None or o[0] > best[0][0]): best = (o, s)
        o, s = best
        print("max %-9s %s: %.2f  (s = %d, rho = %.1f, P = %.1f, vertices with three six-grid lines %.1f, with at least one %.1f)" % (
            objective, "WITH the cut 3 n3 <= 2 n1 + n2" if cut else "without the cut          ", o[0], s, o[1], o[2], o[3], o[4]), flush=True)
print("tau_g as a function of rho (max over s):   rho | without the cut | with the cut")
for rho in (126, 110, 90, 70, 50, 30, 10):
    v = []
    for cut in (False, True):
        b = max((solve(s, cut, "tau_g", rho) or (-1,))[0] for s in range(0, 74)); v.append(b)
    print("   %3d | %8.2f (11 rho + 17 = %d) | %8.2f" % (rho, v[0], 11 * rho + 17, v[1]), flush=True)
