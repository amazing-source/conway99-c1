"""Test the exact local counting equations of subgraph_lp.py on known strongly regular graphs."""
import time
import networkx as nx
import numpy as np
import graphs
from subgraph_lp import Types, build_equations, brute_counts


def paley(q):
    sq = {(x * x) % q for x in range(1, q)}
    return [[1 if i != j and (i - j) % q in sq else 0 for j in range(q)] for i in range(q)]


def check(name, A, n, k, lam, mu, maxm):
    t0 = time.time()
    T = Types(lam, mu, k, maxm)
    rows, aut = build_equations(T, n, maxm)
    z = brute_counts(A, maxm, T)
    bad = 0
    for row in rows:
        s = sum(c * z.get(var, 0) for var, c in row.items())
        if s != 0:
            bad += 1
    sizes = {m: len(T.reps[m]) for m in T.reps}
    print(f'{name}: types per order {sizes}, {len(rows)} equations, violated: {bad}, '
          f'z_K1 = {z[(1, 0)]} ({time.time() - t0:.1f}s)')


A9 = graphs.srg9()
check('srg(9,4,1,2)', np.asarray(A9).tolist(), 9, 4, 1, 2, 7)
P = nx.to_numpy_array(nx.petersen_graph(), dtype=int).tolist()
check('Petersen (10,3,0,1)', P, 10, 3, 0, 1, 7)
check('Paley(13) (13,6,2,3)', paley(13), 13, 6, 2, 3, 6)
C = np.asarray(graphs.clebsch()).tolist() if hasattr(graphs, 'clebsch') else None
if C is not None:
    check('Clebsch (16,5,0,2)', C, 16, 5, 0, 2, 7)
