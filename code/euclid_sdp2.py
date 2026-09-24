"""Euclidean SDP for srg(99,14,1,2) with witnessed recipes of degree DEG (default 3), sparse assembly.

x = (t, y): t = the 2 free order-7 variables (all counts of order <= 7 are z0 + V t, exact), y = order-8
counts / s8 (>= 0).  Constraints: z7 >= 0; exact 7 -> 8 counting equations; Gram(x) = C x + c0 PSD for each
kernel.  Gram entries come from euclid_gram.coefficients (validated to 1e-15 on srg(9) and Petersen).
Usage: euclid_sdp2.py DEG KERNELS [objectives]   e.g.  euclid_sdp2.py 3 E-4
"""
import sys, time, pickle, itertools
import numpy as np
import networkx as nx
import scipy.sparse as sps
import cvxpy as cp
from subgraph_lp import Types
from euclid_gram import make_bases, make_recipes_general, coefficients

KER = {'E-4': (28.0, -8.0, 1.0), 'E3': (42.0, 9.0, -2.0)}
DEG = int(sys.argv[1]) if len(sys.argv) > 1 else 3
kernels = sys.argv[2].split(',') if len(sys.argv) > 2 else ['E-4']
extra = sys.argv[3] if len(sys.argv) > 3 else ''
n, k, lam, mu = 99, 14, 1, 2
t0 = time.time()
P7 = pickle.load(open('../data/exact_region_order7.pkl', 'rb'))
C8 = pickle.load(open('../data/order8_coeffs.pkl', 'rb'))
T = Types(lam, mu, k, 8)
for m in range(1, 8):
    assert [sorted(G.edges()) for G in T.reps[m]] == [sorted(map(tuple, e)) for e in P7['reps'][m]]
assert [sorted(G.edges()) for G in T.reps[8]] == [sorted(map(tuple, e)) for e in C8['reps8']]
var7 = P7['var']; idx7 = {v: q for q, v in enumerate(var7)}
z0 = np.array([float(x) for x in P7['z0']]); V = np.array([[float(x) for x in r] for r in P7['V']])
N8 = C8['N8']; nt = V.shape[1]; NX = nt + N8
s8 = 1e9
bases = make_bases(T, 4)
rec = make_recipes_general(bases, DEG)
R = len(rec)
print(f'degree {DEG}: {R} recipes', flush=True)

# linear equality constraints (7 -> 8)
a = C8['a']; aut7 = C8['aut7']
er, ec, ev, eb = [], [], [], []
r = 0
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
        coef = aut7[i] * b
        sc = max([abs(c) * s8 for c in row.values()] + [abs(coef) * max(1.0, abs(z0[q])), 1.0])
        for j, c in row.items():
            er.append(r); ec.append(nt + j); ev.append(c * s8 / sc)
        for p in range(nt):
            if V[q, p] != 0:
                er.append(r); ec.append(p); ev.append(-coef * V[q, p] / sc)
        eb.append(coef * z0[q] / sc)
        r += 1
Aeq = sps.csr_matrix((ev, (er, ec)), shape=(r, NX)); beq = np.array(eb)
x = cp.Variable(NX)
cons = [x[nt:] >= 0, Aeq @ x == beq]
sc7 = np.maximum(1.0, np.abs(z0))
cons.append((V / sc7[:, None]) @ x[:nt] >= -z0 / sc7)

for kn in kernels:
    coef = coefficients(T.reps, bases, rec, KER[kn], 4)
    print(f'  coefficients {kn} ({time.time()-t0:.0f}s)', flush=True)
    rows, cols, vals = [], [], []
    c0 = np.zeros(R * R)
    diag = np.ones(R)
    ent = {}
    for (r1, r2), d in coef.items():
        cst = 0.0; lin = {}
        for (m, i), c in d.items():
            if m <= 7:
                q = idx7[(m, i)]
                cst += c * z0[q]
                for p in range(nt):
                    if V[q, p] != 0:
                        lin[p] = lin.get(p, 0.0) + c * V[q, p]
            else:
                lin[nt + i] = lin.get(nt + i, 0.0) + c * s8
        ent[(r1, r2)] = (cst, lin)
        if r1 == r2:
            diag[r1] = max(1.0, abs(cst) + sum(abs(v) * (1e3 if p < nt else 1e2) for p, v in lin.items()))
    dsc = 1 / np.sqrt(diag)
    for (r1, r2), (cst, lin) in ent.items():
        f = dsc[r1] * dsc[r2]
        for (a1, a2) in {(r1, r2), (r2, r1)}:
            c0[a1 * R + a2] = cst * f
            for p, v in lin.items():
                rows.append(a1 * R + a2); cols.append(p); vals.append(v * f)
    Cm = sps.csr_matrix((vals, (rows, cols)), shape=(R * R, NX))
    Gs = cp.Variable((R, R), symmetric=True)
    cons += [cp.vec(Gs, order='C') == Cm @ x + c0, Gs >> 0]
    pickle.dump({'rec': rec, 'coef': {kk: dict(v) for kk, v in coef.items()}}, open(f'../data/euclid_deg{DEG}_{kn}.pkl', 'wb'))

def gid(edges, m):
    G = nx.Graph(); G.add_nodes_from(range(m)); G.add_edges_from(edges)
    return idx7[(m, T.find(G))]
qP = gid([(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)], 6)
qZ2 = gid([(0,1),(0,2),(1,2),(0,3),(0,4),(3,4),(5,1),(5,3),(6,2),(6,4),(5,6)], 7)
Pexpr = z0[qP] + V[qP] @ x[:nt]
Sexpr = 2 * (z0[qZ2] + V[qZ2] @ x[:nt])
if 'L16' in extra:
    cons.append(Pexpr <= 1151.08)
print(f'model built ({time.time()-t0:.0f}s)', flush=True)
for name, expr in (('P', Pexpr), ('S', Sexpr)):
    for sense, lab in ((1, 'min'), (-1, 'max')):
        prob = cp.Problem(cp.Minimize(sense * expr), cons)
        try:
            prob.solve(solver=cp.CLARABEL)
            val = None if prob.value is None else sense * prob.value
        except Exception as ex:
            val = f'error {ex}'
        print(f'{lab} {name}: {prob.status} {val} ({time.time()-t0:.0f}s)', flush=True)
