"""Local LP of induced-subgraph counts for srg(99,14,1,2) up to order M (default 8).
Reproduces Reimbayev at order 7 (free variables n3, S), then asks what order M adds.
Quantities: P = #prisms (K3 x K2), n3 = 4158 - 3P (twisted line pairs), S = 2 z(Z2) (sigma-adjacent pairs)."""
import sys, time, pickle
import numpy as np
import networkx as nx
import scipy.sparse as sps
from scipy.optimize import linprog
from subgraph_lp import Types, build_equations

M = int(sys.argv[1]) if len(sys.argv) > 1 else 8
n, k, lam, mu = 99, 14, 1, 2
t0 = time.time()
T = Types(lam, mu, k, M)
print('types per order', {m: len(T.reps[m]) for m in T.reps}, f'({time.time()-t0:.0f}s)', flush=True)
rows, aut = build_equations(T, n, M)
print(f'{len(rows)} equations ({time.time()-t0:.0f}s)', flush=True)
var = [(m, i) for m in range(1, M + 1) for i in range(len(T.reps[m]))]
idx = {v: j for j, v in enumerate(var)}
data, ri, ci = [], [], []
for r, row in enumerate(rows):
    for v, c in row.items():
        if c:
            data.append(c); ri.append(r); ci.append(idx[v])
nr = len(rows)
data.append(1); ri.append(nr); ci.append(idx[(1, 0)])
Aeq = sps.csr_matrix((data, (ri, ci)), shape=(nr + 1, len(var)))
beq = np.zeros(nr + 1); beq[nr] = n

def find(edges, m):
    G = nx.Graph(); G.add_nodes_from(range(m)); G.add_edges_from(edges)
    return idx[(m, T.find(G))]

prism = find([(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)], 6)
Z2 = find([(0,1),(0,2),(1,2),(0,3),(0,4),(3,4),(5,1),(5,3),(6,2),(6,4),(5,6)], 7)

def opt(c, sense):
    res = linprog(sense * c, A_eq=Aeq, b_eq=beq, bounds=(0, None), method='highs')
    return (sense * res.fun) if res.status == 0 else res.message

res = {}
for name, j in (('P', prism), ('zZ2', Z2)):
    c = np.zeros(len(var)); c[j] = 1
    res[name] = (opt(c, 1), opt(c, -1))
print(f'order {M}: P in [{res["P"][0]}, {res["P"][1]}], z(Z2) = S/2 in [{res["zZ2"][0]}, {res["zZ2"][1]}]'
      f'  ({time.time()-t0:.0f}s)', flush=True)
pickle.dump({'T_reps': {m: [list(G.edges()) for G in T.reps[m]] for m in T.reps}, 'rows': rows,
             'var': var, 'prism': prism, 'Z2': Z2}, open(f'../data/order{M}_lp.pkl', 'wb'))
