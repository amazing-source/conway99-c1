"""Export an explicit violating triangle support (the 12 pairs, the edges of T) for independent verification."""
import sys, random, itertools, json
import numpy as np
sys.path.insert(0, 'scripts')
from x14_triangle_supports import LAB, random_tau, random_sigma, build, admissible
rng = random.Random(1)
D6 = None
for _ in range(400):
    tau = {u: random_tau(u, rng) for u in LAB}; sigma = {c: random_sigma(c, rng) for c in range(7)}
    for tri in itertools.combinations(range(7), 3):
        pairs = [frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2) for s in (0, 1) for t in (0, 1)]
        A = build(pairs, tau, sigma)
        if not admissible(A):
            continue
        T = A[15:, 15:]
        labs = [(c, s) for c in tri for s in (0, 1)]
        D = np.zeros((6, 12))
        for j, P in enumerate(pairs):
            for u in P:
                D[labs.index(u), j] = 1
        Pd = D.T @ np.linalg.inv(D @ D.T) @ D
        lam = np.linalg.eigvalsh(T - (3 * np.eye(12) - Pd)).max()
        if lam > 0.05:
            name = lambda P: '{' + ','.join(f'{c}{"+-"[s]}' for c, s in sorted(P)) + '}'
            edges = [(name(pairs[i]), name(pairs[j])) for i, j in itertools.combinations(range(12), 2) if T[i, j]]
            out = dict(triangle=list(tri), pairs=[name(P) for P in pairs], T_edges=edges,
                       lambda_max_T_minus_3I_plus_Pd=round(float(lam), 6))
            print(json.dumps(out, indent=1))
            sys.exit(0)
