"""Flag-positivity SDP (types <= 6 vertices, exact counts up to order 8) for srg(99,14,1,2), optionally with the
degree-3 Euclidean Gram (witnessed recipes).  Optimise P and S.   Usage: flag_sdp_run.py [euclid]"""
import sys, time, pickle, itertools
import numpy as np
import networkx as nx
import scipy.sparse as sps
import cvxpy as cp
from subgraph_lp import Types
from flag_sdp import flag_coefficients

use_euclid = len(sys.argv) > 1 and sys.argv[1] == 'euclid'
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
x = cp.Variable(NX)
cons = [x[nt:] >= 0]
# 7 -> 8 equations
a = C8['a']; aut7 = C8['aut7']
er, ec, ev, eb = [], [], [], []
r = 0
for i, F in enumerate(T.reps[7]):
    q = idx7[(7, i)]
    for U in [()] + [(u,) for u in range(7)] + list(itertools.combinations(range(7), 2)):
        if len(U) == 0:
            b = n - 7
        elif len(U) == 1:
            b = k - F.degree(U[0])
        else:
            u, w = U
            b = (lam if F.has_edge(u, w) else mu) - len(set(F[u]) & set(F[w]))
        row = a.get((i, U), {}); coef = aut7[i] * b
        sc = max([abs(c) * s8 for c in row.values()] + [abs(coef) * max(1.0, abs(z0[q])), 1.0])
        for j, c in row.items():
            er.append(r); ec.append(nt + j); ev.append(c * s8 / sc)
        for p in range(nt):
            if V[q, p] != 0:
                er.append(r); ec.append(p); ev.append(-coef * V[q, p] / sc)
        eb.append(coef * z0[q] / sc); r += 1
cons.append(sps.csr_matrix((ev, (er, ec)), shape=(r, NX)) @ x == np.array(eb))
sc7 = np.maximum(1.0, np.abs(z0))
cons.append((V / sc7[:, None]) @ x[:nt] >= -z0 / sc7)

def lin_of(d):
    """dict {(m,i): c} -> (constant, {var: coeff})"""
    cst = 0.0; lin = {}
    for (m, i), c in d.items():
        if m <= 7:
            qq = idx7[(m, i)]; cst += c * z0[qq]
            for p in range(nt):
                if V[qq, p] != 0:
                    lin[p] = lin.get(p, 0.0) + c * V[qq, p]
        else:
            lin[nt + i] = lin.get(nt + i, 0.0) + c * s8
    return cst, lin

def add_psd(entries, R):
    diag = np.ones(R)
    for (r1, r2), (cst, lin) in entries.items():
        if r1 == r2:
            diag[r1] = max(1.0, abs(cst) + sum(abs(v) * (1e3 if p < nt else 1e2) for p, v in lin.items()))
    dsc = 1 / np.sqrt(diag)
    rows, cols, vals = [], [], []; c0 = np.zeros(R * R)
    for (r1, r2), (cst, lin) in entries.items():
        f = dsc[r1] * dsc[r2]
        for (a1, a2) in {(r1, r2), (r2, r1)}:
            c0[a1 * R + a2] = cst * f
            for p, v in lin.items():
                rows.append(a1 * R + a2); cols.append(p); vals.append(v * f)
    Cm = sps.csr_matrix((vals, (rows, cols)), shape=(R * R, NX))
    G = cp.Variable((R, R), symmetric=True)
    return [cp.vec(G, order='C') == Cm @ x + c0, G >> 0]

nblocks = 0
for s in range(1, 7):
    fc = flag_coefficients(T, s, lam, mu, k)
    for i, (pats, coef) in fc.items():
        ent = {key: lin_of(d) for key, d in coef.items()}
        cons += add_psd(ent, len(pats)); nblocks += 1
    print(f'flag blocks for types of order {s} done ({time.time()-t0:.0f}s)', flush=True)
if use_euclid:
    from euclid_gram import make_bases, make_recipes_general, coefficients
    bases = make_bases(T, 4); rec = make_recipes_general(bases, 3)
    coef = coefficients(T.reps, bases, rec, (28.0, -8.0, 1.0), 4)
    cons += add_psd({key: lin_of(d) for key, d in coef.items()}, len(rec))
    print(f'euclidean degree-3 block added ({time.time()-t0:.0f}s)', flush=True)

def gid(edges, m):
    G = nx.Graph(); G.add_nodes_from(range(m)); G.add_edges_from(edges)
    return idx7[(m, T.find(G))]
qP = gid([(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)], 6)
qZ = gid([(0,1),(0,2),(1,2),(0,3),(0,4),(3,4),(5,1),(5,3),(6,2),(6,4),(5,6)], 7)
Pexpr = z0[qP] + V[qP] @ x[:nt]; Sexpr = 2 * (z0[qZ] + V[qZ] @ x[:nt])
print(f'{nblocks} flag blocks; solving ({time.time()-t0:.0f}s)', flush=True)
for name, expr in (('P', Pexpr), ('S', Sexpr)):
    for sense, lab in ((1, 'min'), (-1, 'max')):
        prob = cp.Problem(cp.Minimize(sense * expr), cons)
        try:
            prob.solve(solver=cp.CLARABEL)
            val = None if prob.value is None else sense * prob.value
        except Exception as ex:
            val = f'error {ex}'
        print(f'{lab} {name}: {prob.status} {val} ({time.time()-t0:.0f}s)', flush=True)
