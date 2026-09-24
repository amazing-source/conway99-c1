"""Degree-4 Euclidean SDP for srg(99,14,1,2)  ("L16 at degree 4").

Unknowns: t (2 free order-7 variables, exact affine parametrisation of all counts of order <= 7) and the
counts z8 >= 0 of the 916 admissible 8-vertex graphs, tied by the exact 7 -> 8 counting equations.
Constraint: the Gram matrix of the 20 symmetric degree-4 tensor sums over configurations of <= 4 points in
E_{-4} (kernel 28, -8, 1) is PSD; its entries are linear in the counts (euclid_gram.py, validated on srg(9)
and Petersen to 1e-15).  Also optional: kernel of E_3 (42, 9, -2).  We optimise P (prisms).
Floating-point SDP: any bound that beats L16 must be certified exactly before being believed.
"""
import sys, time, pickle, itertools
import numpy as np
import networkx as nx
import cvxpy as cp
from subgraph_lp import Types
from euclid_gram import make_bases, make_recipes, make_recipes_general, coefficients

KER = {'E-4': (28.0, -8.0, 1.0), 'E3': (42.0, 9.0, -2.0)}
DEG = int(sys.argv[1]) if len(sys.argv) > 1 else 3
kernels = sys.argv[2].split(",") if len(sys.argv) > 2 else ["E-4"]
use_L16 = len(sys.argv) > 3 and sys.argv[3] == "L16"
D = 4
t0 = time.time()
n, k, lam, mu = 99, 14, 1, 2
P7 = pickle.load(open('../data/exact_region_order7.pkl', 'rb'))
C8 = pickle.load(open('../data/order8_coeffs.pkl', 'rb'))
T = Types(lam, mu, k, 8)
for m in range(1, 8):
    assert [sorted(G.edges()) for G in T.reps[m]] == [sorted(map(tuple, e)) for e in P7['reps'][m]]
assert [sorted(G.edges()) for G in T.reps[8]] == [sorted(map(tuple, e)) for e in C8['reps8']]
var7 = P7['var']; idx7 = {v: q for q, v in enumerate(var7)}
z0 = np.array([float(x) for x in P7['z0']]); V = np.array([[float(x) for x in r] for r in P7['V']])
N8 = C8['N8']; nt = V.shape[1]
bases = make_bases(T, D)
rec = make_recipes_general(bases, DEG)
print(f'{len(rec)} recipes; computing coefficients ...', flush=True)
coefs = {}
for kn in kernels:
    coefs[kn] = coefficients(T.reps, bases, rec, KER[kn], D)
    print(f'  kernel {kn} done ({time.time()-t0:.0f}s)', flush=True)
pickle.dump({'rec': rec, 'coefs': {kk: {key: dict(v) for key, v in c.items()} for kk, c in coefs.items()}},
            open(f'../data/euclid_deg{DEG}_coefs.pkl', 'wb'))

# affine map: count of type (m,i) = (z0 + V t) for m <= 7 ; = s8 * y_j for m = 8
s8 = 1e9
t = cp.Variable(nt)
y = cp.Variable(N8, nonneg=True)
def count_expr(m, i):
    if m <= 7:
        q = idx7[(m, i)]
        return z0[q] + V[q] @ t
    return s8 * y[i]
cons = []
sc7 = np.maximum(1.0, np.abs(z0))
cons.append((z0 + V @ t) / sc7 >= 0)
# 7 -> 8 equations
a = C8['a']; aut7 = C8['aut7']
for i, F in enumerate(T.reps[7]):
    q = idx7[(7, i)]
    Us = [()] + [(u,) for u in range(7)] + list(itertools.combinations(range(7), 2))
    for U in Us:
        if len(U) == 0:
            b = n - 7
        elif len(U) == 1:
            b = k - F.degree(U[0])
        else:
            u, w = U
            b = (lam if F.has_edge(u, w) else mu) - len(set(F[u]) & set(F[w]))
        row = a.get((i, U), {})
        rhs = aut7[i] * b * (z0[q] + V[q] @ t)
        lhs = sum(c * s8 * y[j] for j, c in row.items()) if row else 0
        scale = max([abs(c) * s8 for c in row.values()] + [abs(aut7[i] * b) * max(1.0, abs(z0[q])), 1.0])
        cons.append((lhs - rhs) / scale == 0)
# Gram matrices
for kn in kernels:
    R = len(rec)
    entries = {}
    for (r1, r2), d in coefs[kn].items():
        entries[(r1, r2)] = sum(c * count_expr(m, i) for (m, i), c in d.items())
    # scaling by a reference magnitude per recipe
    diag_mag = np.ones(R)
    for r in range(R):
        d = coefs[kn].get((r, r), {})
        diag_mag[r] = max(1.0, sum(abs(c) * (abs(z0[idx7[(m, i)]]) if m <= 7 else 1e11 / N8 * 10)
                                   for (m, i), c in d.items()))
    dsc = 1 / np.sqrt(diag_mag)
    Gm = [[0] * R for _ in range(R)]
    for r1 in range(R):
        for r2 in range(R):
            e = entries.get((min(r1, r2), max(r1, r2)), 0)
            Gm[r1][r2] = e * (dsc[r1] * dsc[r2])
    Gexpr = cp.bmat([[Gm[r1][r2] if not isinstance(Gm[r1][r2], (int, float)) else cp.Constant(float(Gm[r1][r2]))
                      for r2 in range(R)] for r1 in range(R)])
    Gs = cp.Variable((R, R), symmetric=True)
    cons += [Gs == Gexpr, Gs >> 0]
def gid(edges, m):
    G = nx.Graph(); G.add_nodes_from(range(m)); G.add_edges_from(edges)
    return idx7[(m, T.find(G))]
qP = gid([(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)], 6)
Pexpr = z0[qP] + V[qP] @ t
if use_L16:
    cons.append(Pexpr <= 1151.08)
print(f'model built ({time.time()-t0:.0f}s); solving', flush=True)
for sense, name in ((1, 'min'), (-1, 'max')):
    prob = cp.Problem(cp.Minimize(sense * Pexpr), cons)
    try:
        prob.solve(solver=cp.CLARABEL)
    except Exception as ex:
        print(name, 'solver error', ex); continue
    print(f'{name} P: status {prob.status}, value {None if prob.value is None else sense * prob.value}'
          f' ({time.time()-t0:.0f}s)', flush=True)
