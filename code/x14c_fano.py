"""X14c -- Fano-twisted vertex (tau_u maps class j to class Phi(class u, j)) with ARBITRARY generic sigma:
do the triangle supports on the 7 Fano lines violate the Rayleigh bound?  Sign choices of tau and sigma random."""
import sys, random, itertools
import numpy as np
sys.path.insert(0, 'scripts')
from x14_triangle_supports import LAB, LI, mate, random_sigma, build, admissible

FANO = [(0, 1, 3), (1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 0), (5, 6, 1), (6, 0, 2)]
third = {}
for L in FANO:
    for i, j in itertools.permutations(L, 2):
        third[(i, j)] = [c for c in L if c not in (i, j)][0]

def fano_tau(u, rng):
    i = u[0]; t = {}
    for L in FANO:
        if i in L:
            j, k = [c for c in L if c != i]
            flip = rng.randint(0, 1)
            for s in (0, 1):
                b, c = (j, s), (k, s ^ flip)
                t[b], t[c] = c, b
    return t

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 500
killed = tested = 0; lines_viol = []
for _ in range(trials):
    tau = {u: fano_tau(u, rng) for u in LAB}
    sigma = {c: random_sigma(c, rng) for c in range(7)}
    worst = -1e9; any_adm = False
    for L in FANO:
        pairs = [frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(L, 2) for s in (0, 1) for t in (0, 1)]
        A = build(pairs, tau, sigma)
        if not admissible(A):
            continue
        any_adm = True
        n = len(A)
        lmax = np.linalg.eigvalsh(A.astype(float) - (11 / 99) * np.ones((n, n))).max()
        lmin = np.linalg.eigvalsh(A.astype(float)).min()
        worst = max(worst, lmax - 3, -4 - lmin)
    if any_adm:
        tested += 1; killed += worst > 1e-9; lines_viol.append(worst)
print(f'Fano-twisted vertices with random sigma: {tested} tested, {killed} killed by a triangle support '
      f'(max excess {max(lines_viol):.4f}, min excess {min(lines_viol):.4f})')
