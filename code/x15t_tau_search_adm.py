"""X15t -- tau search (sigma fixed, KBLDP) with objective: first local admissibility (lambda <= 1, mu <= 2 in all
42 star/triangle supports), then the worst Rayleigh eigenvalue over all families.  Observation only."""
import sys, random, itertools, pickle
import numpy as np
sys.path.insert(0, 'scripts')
from x15_fano_tight import *
from x15h_test_solution import sigma_from
import x14_triangle_supports as X14

sig = sigma_from(np.load('data/x15g_KBLDP.npy'))
fams = [[R for R in BLOCKS if R <= frozenset(t)] for t in itertools.combinations(range(7), 3)] + \
       [[R for R in BLOCKS if c in R] for c in range(7)]
sups = [[frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2) for s in (0, 1) for t in (0, 1)]
        for tri in itertools.combinations(range(7), 3)] + \
       [[frozenset({(c, s), l}) for s in (0, 1) for l in LAB if l[0] != c] for c in range(7)]
keys = [(LAB.index(u), li) for u in LAB for li, L in enumerate(FANO) if u[0] in L]

def tau_from(bits):
    tau = {}
    for u in LAB:
        t = {}
        for li, L in enumerate(FANO):
            if u[0] in L:
                j, k = [c for c in L if c != u[0]]
                flip = bits[(LAB.index(u), li)]
                for s in (0, 1):
                    t[(j, s)], t[(k, s ^ flip)] = (k, s ^ flip), (j, s)
        tau[u] = t
    return tau

def score(bits):
    tau = tau_from(bits)
    nbad = sum(not X14.admissible(X14.build(p, tau, sig)) for p in sups)
    if nbad:
        return -10.0 * nbad, None
    D = config_data(tau, sig)
    return min(min(rayleigh(D, f)) for f in fams), D

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    best = (-1e9, None)
    for restart in range(int(sys.argv[2]) if len(sys.argv) > 2 else 3):
        bits = {k: rng.randint(0, 1) for k in keys}
        s, D = score(bits)
        for it in range(500):
            k = rng.choice(keys); bits[k] ^= 1
            s2, D2 = score(bits)
            if s2 >= s:
                s = s2
            else:
                bits[k] ^= 1
        print(f'restart {restart}: score {s:.5f}', flush=True)
        if s > best[0]:
            best = (s, dict(bits))
    pickle.dump(best[1], open('data/x15t_best_tau.pkl', 'wb'))
    print('best score', best[0])
