"""X14b -- inspect violating triangle supports: exact certificate + structure of the pattern."""
import sys, random, itertools
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, 'scripts')
from x14_triangle_supports import LAB, LI, mate, random_tau, random_sigma, build, admissible, bounds

def exact_check(A, q, denom=10**6):
    n = len(A); qq = [Fr(int(round(x * denom)), denom) for x in q]
    val = sum(qq[i] * (Fr(int(A[i, j])) - Fr(11, 99)) * qq[j] for i in range(n) for j in range(n))
    return val - 3 * sum(x * x for x in qq)

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
shown = 0
for _ in range(400):
    tau = {u: random_tau(u, rng) for u in LAB}
    sigma = {c: random_sigma(c, rng) for c in range(7)}
    for tri in itertools.combinations(range(7), 3):
        pairs = [frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2) for s in (0, 1) for t in (0, 1)]
        A = build(pairs, tau, sigma)
        if not admissible(A):
            continue
        n = len(A)
        ev, V = np.linalg.eigh(A.astype(float) - (11 / 99) * np.ones((n, n)))
        if ev[-1] > 3 + 1e-9 and shown < 4:
            shown += 1
            g = exact_check(A, V[:, -1])
            sub = A[15:, 15:]
            deg_in = sub.sum(1)
            inner_edges = int(sub.sum() // 2)
            # tau edges inside the triangle: pairs of labels (u; v,w) with v,w in the triangle classes
            tri_labels = [l for l in LAB if l[0] in tri]
            tau_in = sum(1 for u in tri_labels for v in tri_labels if v[0] != u[0] and tau[u][v][0] in tri and tau[u][v][0] != u[0]) // 2
            sig_in = sum(1 for c in tri for v in tri_labels if v[0] != c and sigma[c][v][0] in tri)
            print(f'triangle {tri}: lambda_max = {ev[-1]:.4f}; exact q^T(A-11J/99)q - 3|q|^2 = {float(g):.6f} (>0: {g > 0}); '
                  f'edges among the 12 pairs: {inner_edges}, degrees {sorted(deg_in.tolist())}; '
                  f'tau-transitions staying in the triangle: {tau_in}, sigma staying: {sig_in}')
            q = V[:, -1]
            print('   eigenvector weight on x/labels/pairs:', round(float(q[0]**2), 3), round(float((q[1:15]**2).sum()), 3), round(float((q[15:]**2).sum()), 3))
    if shown >= 4:
        break
