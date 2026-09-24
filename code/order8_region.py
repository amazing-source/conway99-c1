"""Order-8 local LP for srg(99,14,1,2): what do the exact 7 -> 8 counting equations add to Reimbayev's order 7?

Unknowns: t = the 2 free order-7 variables (affine images of P and S, exact parametrisation from
exact_region.py), and z8 = counts of the admissible 8-vertex graphs.
Constraints: z7(t) = z0 + V t >= 0 ;  z8 >= 0 ;  for every order-7 type F and every U (|U| <= 2):
    sum_G a(F,U,G) z8_G = |Aut F| b(F,U) z7_F(t).
We optimise P and S.  Floating LP on a scaled system; any claimed bound is to be certified afterwards
(exact dual certificate) before being believed.
"""
import sys, time, pickle, itertools
from collections import defaultdict
from fractions import Fraction
import numpy as np
import networkx as nx
from networkx.algorithms import isomorphism as iso
import scipy.sparse as sps
from scipy.optimize import linprog
from subgraph_lp import Types

n, k, lam, mu = 99, 14, 1, 2
t0 = time.time()
D = pickle.load(open('../data/exact_region_order7.pkl', 'rb'))
var7, free, z0, V = D['var'], D['free'], D['z0'], D['V']
T = Types(lam, mu, k, 8)
for m in range(1, 8):  # the type indexing must match the order-7 pickle
    assert [sorted(G.edges()) for G in T.reps[m]] == [sorted(map(tuple, e)) for e in D['reps'][m]], m
N8 = len(T.reps[8])
print(f'order-8 admissible types: {N8} ({time.time()-t0:.0f}s)', flush=True)

# coefficients a(F,U,G) for F of order 7
a = defaultdict(lambda: defaultdict(int))
for j, G in enumerate(T.reps[8]):
    for v in range(8):
        rest = [u for u in range(8) if u != v]
        Gv = nx.relabel_nodes(G.subgraph(rest).copy(), {u: q for q, u in enumerate(rest)})
        i = T.find(Gv)
        F = T.reps[7][i]
        Nv = {rest.index(u) for u in G[v]}
        for phi in iso.GraphMatcher(Gv, F).isomorphisms_iter():
            inv = {fv: gv for gv, fv in phi.items()}
            img = {fv for fv in range(7) if inv[fv] in Nv}
            a[(i, ())][j] += 1
            for u in img:
                a[(i, (u,))][j] += 1
            for u, w in itertools.combinations(sorted(img), 2):
                a[(i, (u, w))][j] += 1
print(f'coefficients done ({time.time()-t0:.0f}s)', flush=True)

aut7 = [sum(1 for _ in iso.GraphMatcher(F, F).isomorphisms_iter()) for F in T.reps[7]]
idx7 = {v: q for q, v in enumerate(var7)}
nt = len(free)
# variable vector x = (t_1..t_nt, y_1..y_N8) with z8 = s8 * y (scaling)
s8 = 1.7e11 / N8
rows_A, rows_b = [], []
eq_data, eq_r, eq_c, eq_b = [], [], [], []
r = 0
for i, F in enumerate(T.reps[7]):
    q7 = idx7[(7, i)]
    Us = [()] + [(u,) for u in range(7)] + list(itertools.combinations(range(7), 2))
    for U in Us:
        if len(U) == 0:
            b = n - 7
        elif len(U) == 1:
            b = k - F.degree(U[0])
        else:
            u, w = U
            b = (lam if F.has_edge(u, w) else mu) - len(set(F[u]) & set(F[w]))
        coef = aut7[i] * b                     # rhs = coef * (z0 + V t)
        row = a[(i, U)]
        sc = max([abs(c) * s8 for c in row.values()] + [abs(coef) * max(1.0, float(abs(z0[q7])))] + [1.0])
        for j, c in row.items():
            eq_data.append(c * s8 / sc); eq_r.append(r); eq_c.append(nt + j)
        for p in range(nt):
            if V[q7][p] != 0:
                eq_data.append(-coef * float(V[q7][p]) / sc); eq_r.append(r); eq_c.append(p)
        eq_b.append(coef * float(z0[q7]) / sc)
        r += 1
Aeq = sps.csr_matrix((eq_data, (eq_r, eq_c)), shape=(r, nt + N8))
beq = np.array(eq_b)
# z7(t) >= 0  <=>  -V t <= z0
V7 = np.array([[float(x) for x in V[q]] for q in range(len(var7))])
z07 = np.array([float(x) for x in z0])
sc7 = np.maximum(1.0, np.abs(z07))
Aub = sps.hstack([sps.csr_matrix(-V7 / sc7[:, None]), sps.csr_matrix((len(var7), N8))]).tocsr()
bub = z07 / sc7
bounds = [(None, None)] * nt + [(0, None)] * N8

def gid7(edges, m):
    G = nx.Graph(); G.add_nodes_from(range(m)); G.add_edges_from(edges)
    return idx7[(m, T.find(G))]
prism = gid7([(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)], 6)
z2 = gid7([(0,1),(0,2),(1,2),(0,3),(0,4),(3,4),(5,1),(5,3),(6,2),(6,4),(5,6)], 7)
out = {}
for name, q in (('P', prism), ('S/2', z2)):
    lohi = []
    for sense in (1, -1):
        c = np.zeros(nt + N8); c[:nt] = sense * V7[q]
        res = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=bounds, method='highs')
        lohi.append(float(z07[q] + V7[q] @ res.x[:nt]) if res.status == 0 else res.message[:50])
    out[name] = lohi
    print(f'{name}: [{lohi[0]}, {lohi[1]}]  ({time.time()-t0:.0f}s)', flush=True)
pickle.dump({'N8': N8, 'reps8': [list(G.edges()) for G in T.reps[8]], 'a': {key: dict(v) for key, v in a.items()},
             'aut7': aut7}, open('../data/order8_coeffs.pkl', 'wb'))
