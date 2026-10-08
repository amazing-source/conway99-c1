"""C1, lab session, 2026-10-08. Moment LP on point types for tau_g (pairs of grids on a common line), with Codex's new cut.
  python profile_lp.py
NEW FACT USED (Codex, note 203 in preparation, general certificate from the rank bound 56 - r mod 7, r >= 37): on a
line in six grids, if two points have three hub lines each, the third has only one; hence, with n_h = number of
vertices on exactly h lines contained in six grids,  3 n_3 <= 2 n_1 + n_2.
Point type = the grid graph Xi on the 7 lines through a vertex. Kept types: degrees in {0,1,2,3,4,6} (a line is never
in exactly 5 grids), at most 17 edges, and D1 (the non-edges, if any, contain two disjoint pairs). For a distribution
x_t of the 99 vertices: rho = sum e_t x_t / 9, tau_g = sum cherries_t x_t / 3, h_t = number of vertices of degree 6.
Floating LP (HiGHS): maximum of tau_g for given rho, without and with the cut; and the supporting lines
tau_g <= alpha rho + beta. My type list may be larger than Codex's (it uses more local lemmas): the first column is
only a calibration against its bound tau_g <= 11 rho + 17."""
import networkx as nx, numpy as np
from itertools import combinations
from scipy.optimize import linprog
types = []
for G in nx.graph_atlas_g():
    if G.number_of_nodes() != 7: continue
    deg = [d for _, d in G.degree()]
    if any(d == 5 for d in deg) or G.number_of_edges() > 17: continue
    non = [e for e in combinations(range(7), 2) if not G.has_edge(*e)]
    if non and not any(not (set(a) & set(b)) for a, b in combinations(non, 2)): continue
    types.append((G.number_of_edges(), sum(d * (d - 1) // 2 for d in deg), sum(d == 6 for d in deg)))
T = np.array(types, dtype=float); n = len(T)
print("%d point types kept; hub counts present: %s" % (n, sorted(set(int(h) for h in T[:, 2]))))
def solve(rho, cut):
    A_eq = [np.ones(n), T[:, 0]]; b_eq = [99.0, 9.0 * rho]; A_ub = []; b_ub = []
    if cut: A_ub.append(np.where(T[:, 2] == 3, 3.0, 0.0) - np.where(T[:, 2] == 1, 2.0, 0.0) - np.where(T[:, 2] == 2, 1.0, 0.0)); b_ub.append(0.0)
    r = linprog(-T[:, 1] / 3, A_ub=np.array(A_ub) if A_ub else None, b_ub=b_ub if A_ub else None, A_eq=np.array(A_eq), b_eq=b_eq, bounds=[(0, None)] * n, method="highs")
    if r.status != 0: return None
    alpha = -r.eqlin.marginals[1] * 9.0                                       # d tau / d rho
    return -r.fun, alpha, r.x
print("  rho | max tau_g without the cut (11 rho + 17 = Codex) | with 3 n_3 <= 2 n_1 + n_2 | slope | types used with the cut (x, edges, cherries, hubs)")
lines = set()
for rho in (126, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10):
    a = solve(rho, False); b = solve(rho, True)
    used = [(round(float(b[2][i]), 1), int(T[i, 0]), int(T[i, 1]), int(T[i, 2])) for i in np.argsort(-b[2])[:4] if b[2][i] > 1e-6]
    print("  %3d | %8.1f  (%d) | %8.1f | %6.3f | %s" % (rho, a[0], 11 * rho + 17, b[0], b[1], used))
    lines.add((round(b[1], 4), round(b[0] - b[1] * rho, 2)))
print("supporting lines tau_g <= alpha rho + beta with the cut:", sorted(lines))
