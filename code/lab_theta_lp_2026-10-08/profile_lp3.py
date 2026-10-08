"""C1, lab session, 2026-10-08. Codex's moment LP + the cut of its note 203 + the laptop session's DIMENSION COUNT.
  python profile_lp3.py <codex-grid-hub-profiles.json>
NEW FACT USED (laptop session): classes of grid indicators live in 19 dimensions mod 7 at rank 37 (with [1]); the six
grids of a line in six grids satisfy one relation. If there are c further independent relations mod 7 among these
classes, then rho + 1 - x6 - c <= 19, i.e.   rho <= 18 + c + x6,   x6 = number of lines in six grids = sum_v u6(v) / 3.
This script adds that constraint to profile_lp2.py (same model, cut 3 n3 <= 2 n1 + n2 included) and prints, for each
c, the maximum of tau_g and of rho. Target of NOTE 17.49: 27 828 tau_g + 31 976 tau_n < 17.1 million.
c is NOT bounded by anything proved: this is the conversion table between "extra relations" and the accounting."""
import sys, json
import numpy as np
from scipy.optimize import linprog
D = json.load(open(sys.argv[1])); prof = D["refined_profiles"]
def solve(s, c, objective, dim=18):
    cols = []
    for (e, ch, h2, u6) in prof:
        ins = 1 if e >= 14 else 0
        if ins and s == 0: continue
        for d in range(0, min(s - ins, 14 if ins else 2 * h2) + 1): cols.append((e, ch, u6, ins, d))
    n = len(cols); E = np.array([q[0] for q in cols], float); C = np.array([q[1] for q in cols], float); U = np.array([q[2] for q in cols], float); I = np.array([q[3] for q in cols], float); Dn = np.array([q[4] for q in cols], float)
    z = lambda *v: np.concatenate([np.zeros(n), v])
    A_eq = [np.concatenate([I, [0, 0]]), np.concatenate([1 - I, [0, 0]]), np.concatenate([E, [-9, 0]]), np.concatenate([Dn, [0, 0]]), np.concatenate([Dn * Dn + I * Dn, [0, 0]])]
    b_eq = [s, 99 - s, 0, 14 * s, 12 * s + 2 * s * s]
    A_ub = [np.concatenate([I * Dn, [0, 0]]), z(6, -1), z(5, 1), np.concatenate([-(2.0 * (U == 1) + 1.0 * (U == 2) - 3.0 * (U == 3)), [0, 0]])]; b_ub = [3 * s + s * s / 9, 0, 1386, 0]
    if c is not None: A_ub.append(np.concatenate([-U / 3, [1, 0]])); b_ub.append(dim + c)          # rho - x6 <= dim + c
    obj = np.concatenate([-C / 3, [0, 0]]) if objective == "tau_g" else z(-1, 0)
    r = linprog(obj, A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq), b_eq=b_eq, bounds=[(0, None)] * n + [(0, 126), (0, 852)], method="highs")
    return None if r.status != 0 else (-r.fun, r.x[n], float((r.x[:n] * U).sum()) / 3)
print("  c (extra relations) | max tau_g | 27828 tau_g | rho there | x6 there | max rho | verdict if there is no non-grid pair")
for c in (0, 4, 8, 10, 12, 13, 14, 16, 20, 25, 30, 40, None):
    best = max((solve(s, c, "tau_g") for s in range(0, 74)), key=lambda o: -1 if o is None else o[0]); br = max((solve(s, c, "rho") or (-1,))[0] for s in range(0, 74))
    cost = 27828 * best[0] / 1e6
    print("  %-19s | %8.1f | %7.2fM | %8.1f | %7.1f | %6.1f | %s" % ("none" if c is None else c, best[0], cost, best[1], best[2], br, "EXCLUDED (below 17.1M)" if cost < 17.1 else "not enough"), flush=True)
print("other ranks, c = 0 (dimension 56 - r - 1): ", end="")
for r_, dim in ((39, 16), (41, 14), (43, 12)):
    best = max((solve(s, 0, "tau_g", dim) for s in range(0, 74)), key=lambda o: -1 if o is None else o[0]); print("r = %d: tau_g <= %.1f, rho there %.1f;  " % (r_, best[0], best[1]), end="")
print()
