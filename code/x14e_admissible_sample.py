"""X14e -- rejection-sample locally admissible max-twist vertex configurations (all 35 triangle + 7 star supports
pass lambda<=1, mu<=2 inside W) and measure the fraction killed by the Rayleigh bound on some support.
Also records which failure (star vs triangle, lambda vs mu) rejects configurations."""
import sys, random, itertools, time
from collections import Counter
import numpy as np
sys.path.insert(0, 'scripts')
from x14_triangle_supports import LAB, mate, random_tau, random_sigma, build

SUP = []
for c in range(7):
    SUP.append(('star', c, [frozenset({(c, s), l}) for s in (0, 1) for l in LAB if l[0] != c]))
for tri in itertools.combinations(range(7), 3):
    SUP.append(('tri', tri, [frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2) for s in (0, 1) for t in (0, 1)]))

def first_failure(tau, sigma):
    mats = []
    for kind, key, pairs in SUP:
        A = build(pairs, tau, sigma)
        A2 = A @ A; n = len(A); off = ~np.eye(n, dtype=bool)
        if (A2[(A == 1) & off] > 1).any():
            return (kind, 'lambda'), None
        if (A2[(A == 0) & off] > 2).any():
            return (kind, 'mu'), None
        mats.append((kind, key, A))
    return None, mats

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
tries = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
fail = Counter(); adm = killed = 0; excess = []; t0 = time.time()
for _ in range(tries):
    tau = {u: random_tau(u, rng) for u in LAB}; sigma = {c: random_sigma(c, rng) for c in range(7)}
    f, mats = first_failure(tau, sigma)
    if f:
        fail[f] += 1; continue
    adm += 1; worst = -1e9
    for kind, key, A in mats:
        n = len(A)
        lmax = np.linalg.eigvalsh(A.astype(float) - (11 / 99) * np.ones((n, n))).max()
        lmin = np.linalg.eigvalsh(A.astype(float)).min()
        worst = max(worst, lmax - 3, -4 - lmin)
    excess.append(worst); killed += worst > 1e-9
print(f'{tries} random max-twist configs ({time.time()-t0:.0f}s): first local failures {dict(fail)}')
print(f'locally admissible: {adm}; killed by a Rayleigh violation: {killed}; surviving: {adm - killed}')
if excess:
    print(f'max Rayleigh excess among admissible: {max(excess):.4f}; median {float(np.median(excess)):.4f}')
