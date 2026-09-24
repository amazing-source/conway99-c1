import itertools, time
import numpy as np
import networkx as nx
from networkx.algorithms import isomorphism as iso
import graphs
from subgraph_lp import Types, brute_counts
from flag_sdp import flag_coefficients, flag_matrix

def direct(A, sig, pats):
    Gg = nx.from_numpy_array(np.asarray(A, dtype=float))
    pidx = {p: q for q, p in enumerate(pats)}
    s = sig.number_of_nodes()
    M = np.zeros((len(pats), len(pats)))
    # labelled copies: injective maps sigma -> Gg that are induced isomorphisms
    GM = iso.GraphMatcher(Gg, sig)
    for m in GM.subgraph_isomorphisms_iter():     # Gg-vertex -> sigma-vertex (induced)
        inv = {b: a for a, b in m.items()}
        x = np.zeros(len(pats))
        img = set(m.keys())
        for w in Gg.nodes():
            if w in img:
                continue
            Tw = frozenset(m[u] for u in Gg[w] if u in img)
            x[pidx[Tw]] += 1
        M += np.outer(x, x)
    return M

def run(name, A, lam, mu, k, smax):
    T = Types(lam, mu, k, smax + 2)
    z = brute_counts(np.asarray(A).tolist(), smax + 2, T)
    worst = 0
    for s in range(1, smax + 1):
        fc = flag_coefficients(T, s, lam, mu, k)
        for i, (pats, coef) in fc.items():
            Mc = flag_matrix(pats, coef, z)
            Md = direct(A, T.reps[s][i], pats)
            worst = max(worst, np.abs(Mc - Md).max() / max(1, np.abs(Md).max()))
    print(f'{name}: types up to order {smax}, worst relative error {worst:.2e}')

run('srg(9,4,1,2)', graphs.srg9(), 1, 2, 4, 5)
run('Petersen', nx.to_numpy_array(nx.petersen_graph(), dtype=int), 0, 1, 3, 5)
