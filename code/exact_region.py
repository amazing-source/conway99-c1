"""Feasible region of the local counting system in terms of its free variables (exact parametrisation + LP).
z = z0 + V t ; constraints z >= 0.  The LP in t is small; it is solved in floating point on a well-scaled
system and the optimal vertices are then re-checked in exact arithmetic."""
import sys, time, pickle
from fractions import Fraction
import numpy as np
import networkx as nx
from scipy.optimize import linprog
from exact_system import solve_exact

M = int(sys.argv[1]) if len(sys.argv) > 1 else 7
n, k, lam, mu = (int(x) for x in sys.argv[2:6]) if len(sys.argv) > 5 else (99, 14, 1, 2)
TAG = sys.argv[6] if len(sys.argv) > 6 else ""
t0 = time.time()
T, var, R, piv, free, incons = solve_exact(n, k, lam, mu, M)
N = len(var)
assert not incons
print(f'order {M}: {N} variables, rank {len(piv)}, {len(free)} free: {[var[c] for c in free]} ({time.time()-t0:.0f}s)', flush=True)
# z_piv = R[N] - sum_f R[f] t_f ; z_free = t_f
z0 = [Fraction(0)] * N
V = [[Fraction(0)] * len(free) for _ in range(N)]
for r, c in zip(R, piv):
    z0[c] = r[N]
    for j, f in enumerate(free):
        V[c][j] = -r[f]
for j, f in enumerate(free):
    V[f][j] = Fraction(1)

def gid(edges, m):
    G = nx.Graph(); G.add_nodes_from(range(m)); G.add_edges_from(edges)
    return var.index((m, T.find(G)))
prism = gid([(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)], 6)
exprs = {'P': prism}
if M >= 7:
    exprs['S/2 = z(Z2)'] = gid([(0,1),(0,2),(1,2),(0,3),(0,4),(3,4),(5,1),(5,3),(6,2),(6,4),(5,6)], 7)
# scaled float LP: variables t (free); constraints -V t <= z0
Vf = np.array([[float(x) for x in row] for row in V])
z0f = np.array([float(x) for x in z0])
scale = np.maximum(1.0, np.abs(Vf).max(axis=1))
A_ub = -Vf / scale[:, None]; b_ub = z0f / scale
for name, j in exprs.items():
    out = []
    for sense in (1, -1):
        c = sense * Vf[j]
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(None, None)] * len(free), method='highs')
        if res.status != 0:
            out.append(res.message[:40]); continue
        t = [Fraction(x).limit_denominator(10**6) for x in res.x]
        val = z0[j] + sum(V[j][q] * t[q] for q in range(len(free)))
        viol = min(z0[i] + sum(V[i][q] * t[q] for q in range(len(free))) for i in range(N))
        out.append((float(val), float(viol)))
    print(f'  {name}: min {out[0]}, max {out[1]}   [(value, most negative z at rounded optimum)]', flush=True)
pickle.dump({'var': var, 'free': [var[c] for c in free], 'z0': z0, 'V': V,
             'reps': {m: [list(G.edges()) for G in T.reps[m]] for m in T.reps}},
            open(f'../data/exact_region_order{M}{TAG}.pkl', 'wb'))
print(f'done ({time.time()-t0:.0f}s)')
