"""Rooted Euclidean positivity for srg(99,14,1,2): sum over vertices x of the Gram matrix of tensor sums over
configurations (<= 4 points) rooted at x.  Unions of two rooted configurations have <= 7 vertices, so every
entry is an exact affine function of the two order-7 free variables, i.e. of (P, S).  We scan (P, S) over
the order-7 triangle and report where the matrices are PSD.  Families: degree d in {1,2,3,4}, kernel of E_-4
(dim 44) or E_3 (dim 54), plain or harmonic (traceless, d <= 3).
Usage: rooted_scan.py d1:ker:harm,d2:ker:harm,...     e.g. rooted_scan.py 3:E-4:1,2:E-4:1,3:E3:0
"""
import sys, time, pickle
import numpy as np
import networkx as nx
from subgraph_lp import Types
from euclid_gram import make_bases, make_rooted_recipes, coefficients_general

KER = {'E-4': ((28.0, -8.0, 1.0), 44), 'E3': ((42.0, 9.0, -2.0), 54)}
specs = [s.split(':') for s in (sys.argv[1] if len(sys.argv) > 1 else '3:E-4:1').split(',')]
t0 = time.time()
P7 = pickle.load(open('../data/exact_region_order7.pkl', 'rb'))
T = Types(1, 2, 14, 7)
for m in range(1, 8):
    assert [sorted(G.edges()) for G in T.reps[m]] == [sorted(map(tuple, e)) for e in P7['reps'][m]]
var7 = P7['var']; idx7 = {v: q for q, v in enumerate(var7)}
z0 = np.array([float(x) for x in P7['z0']]); V = np.array([[float(x) for x in r] for r in P7['V']])
bases = make_bases(T, 4)

def gid(edges, m):
    G = nx.Graph(); G.add_nodes_from(range(m)); G.add_edges_from(edges)
    return idx7[(m, T.find(G))]
qP = gid([(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)], 6)
qZ = gid([(0,1),(0,2),(1,2),(0,3),(0,4),(3,4),(5,1),(5,3),(6,2),(6,4),(5,6)], 7)
# (P, S) = L t + l0
L = np.array([V[qP], 2 * V[qZ]]); l0 = np.array([z0[qP], 2 * z0[qZ]])
Linv = np.linalg.inv(L)

fams = []
for d, kn, h in specs:
    d = int(d); ker, dim = KER[kn]
    rec = make_rooted_recipes(bases, d)
    coef = coefficients_general(T.reps, bases, rec, ker, 7, rooted=True, harmonic_dim=dim if h == '1' else None)
    R = len(rec)
    G0 = np.zeros((R, R)); G1 = np.zeros((R, R)); G2 = np.zeros((R, R))
    for (r1, r2), dd in coef.items():
        c0 = sum(c * z0[idx7[u]] for u, c in dd.items())
        c1 = sum(c * V[idx7[u], 0] for u, c in dd.items())
        c2 = sum(c * V[idx7[u], 1] for u, c in dd.items())
        for a, b in {(r1, r2), (r2, r1)}:
            G0[a, b] = c0; G1[a, b] = c1; G2[a, b] = c2
    # scale by the diagonal at a central point to make eigenvalues comparable
    fams.append((f'd={d} {kn} harm={h}', R, G0, G1, G2))
    print(f'family d={d} {kn} harmonic={h}: {R} recipes ({time.time()-t0:.0f}s)', flush=True)
pickle.dump({'fams': fams, 'L': L, 'l0': l0}, open('../data/rooted_scan_' + '_'.join(':'.join(s) for s in specs).replace(':', '-') + '.pkl', 'wb'))

def minrel(t, G0, G1, G2):
    G = G0 + t[0] * G1 + t[1] * G2
    d = np.sqrt(np.maximum(np.abs(np.diag(G)), 1e-300))
    Gn = G / d[:, None] / d[None, :]
    return np.linalg.eigvalsh(Gn)[0]

# scan: P in [0, 1386], S in [0, n3] with n3 = 4158 - 3P
res = {}
for Pv in np.linspace(0, 1386, 58):
    n3 = 4158 - 3 * Pv
    row = []
    for Sv in np.linspace(0, n3, 12):
        t = Linv @ (np.array([Pv, Sv]) - l0)
        ok = all(minrel(t, G0, G1, G2) > -1e-9 for _, _, G0, G1, G2 in fams)
        row.append(ok)
    res[Pv] = row
feas_P = [Pv for Pv, row in res.items() if any(row)]
print('feasible P range on the grid:', (min(feas_P), max(feas_P)) if feas_P else None)
for Pv in sorted(res):
    if int(Pv) % 96 == 0 or Pv in (min(feas_P or [0]), max(feas_P or [0])):
        print(f'  P = {Pv:7.1f}: ' + ''.join('#' if ok else '.' for ok in res[Pv]))
print(f'done ({time.time()-t0:.0f}s)')
