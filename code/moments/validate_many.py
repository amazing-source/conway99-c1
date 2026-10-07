"""Validate the moment hierarchy on small srg's by brute-force true densities (Liouville test)."""
import sys, itertools, math, numpy as np, networkx as nx
from srg_moments import Hierarchy, canon
def srg_params(G):
    n = G.number_of_nodes(); A = nx.to_numpy_array(G, dtype=int); k = int(A[0].sum()); A2 = A @ A
    lam = {int(A2[i, j]) for i in range(n) for j in range(n) if A[i, j]}
    mu = {int(A2[i, j]) for i in range(n) for j in range(n) if i != j and not A[i, j]}
    assert len(lam) == 1 and len(mu) == 1 and (A.sum(1) == k).all()
    return n, k, lam.pop(), mu.pop(), A
def paley(q):
    sq = {(x * x) % q for x in range(1, q)}
    return nx.Graph([(i, j) for i in range(q) for j in range(i + 1, q) if (j - i) % q in sq])
graphs = {
    "Paley13": paley(13), "Paley17": paley(17),
    "Petersen": nx.petersen_graph(),
    "rook4x4": nx.cartesian_product(nx.complete_graph(4), nx.complete_graph(4)),
    "Clebsch(16,5,0,2)": nx.complement(nx.Graph([(i, j) for i in range(16) for j in range(i + 1, 16)
                                                 if bin(i ^ j).count("1") in (1, 4)])) ,
    "Schlafli-compl(27,10,1,5)": None,
}
# complement of Schlafli = srg(27,10,1,5): collinearity graph of GQ(2,4): build from 27 lines on cubic surface via
# known model: vertices = (i,j) i!=j in 6 (30)?  simpler: halved/folded; use networkx? fall back to skipping if unavailable
del graphs["Schlafli-compl(27,10,1,5)"]
t = int(sys.argv[1]) if len(sys.argv) > 1 else 6
for name, G in graphs.items():
    G = nx.convert_node_labels_to_integers(G)
    try:
        n, k, lam, mu, A = srg_params(G)
    except AssertionError:
        print(name, "not srg"); continue
    H = Hierarchy(n, k, lam, mu, t)
    q = np.zeros(len(H.top))
    for sub in itertools.combinations(range(n), t):
        bits = 0
        for b in range(t):
            for a in range(b):
                if A[sub[a], sub[b]]:
                    bits |= 1 << (b * (b - 1) // 2 + a)
        q[H.index[canon(t, bits)[0]]] += 1
    q /= math.comb(n, t)
    Aeq = H.equalities()
    worst = []
    for nm, s, a, F, c in H.blocks():
        M = np.tensordot(H.block_matrices(s, a, F, c), q, axes=([2], [0]))
        worst.append((np.linalg.eigvalsh(M).min(), nm))
    print(f"{name} srg({n},{k},{lam},{mu}) t={t}: |Aeq q|max={np.abs(Aeq @ q).max():.2e}  min eig={min(worst)[0]:.2e} at {min(worst)[1]}", flush=True)
