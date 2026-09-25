"""X15h -- Rayleigh tests (X15 compressions, far-block criterion X15f) on sigma solutions of the ILP X15g."""
import sys, random, itertools
import numpy as np
sys.path.insert(0, 'scripts')
from x15_fano_tight import *
from x15g_ilp import VARS, VI
from x15f_farblock import ball, profile, criterion

def sigma_from(x):
    sigma = {P: {} for P in range(7)}
    for i, (P, v, w) in enumerate(VARS):
        if x[i] > 0.5:
            sigma[P][v] = w
    return sigma

def full_tests(D, label=''):
    tri = [[R for R in BLOCKS if R <= frozenset(t)] for t in itertools.combinations(range(7), 3)]
    stars = [[R for R in BLOCKS if c in R] for c in range(7)]
    w1 = min(rayleigh(D, f)[0] for f in tri + stars)
    w2 = min(rayleigh(D, f)[1] for f in tri + stars)
    fb = []
    for cc in range(7):
        N, AG = ball(D, cc)
        for R in BLOCKS:
            if cc not in R:
                sU, sL = criterion(AG, profile(D, N, R), 4, 0)
                fb.append(min(sU, sL))
    print(f'{label} kappa_bad {D["kappa_bad"]}, block imbalance {D["imbalance"]}, label imbalance {D["lab_bad"]} | '
          f'Rayleigh min eig: upper {w1:.6f}, lower {w2:.6f} | far-block min slack {min(fb):.6f}', flush=True)
    return w1, w2, min(fb)

if __name__ == '__main__':
    rng = random.Random(1)
    for mode in sys.argv[1:] or ['KBL']:
        x = np.load(f'data/x15g_{mode}.npy')
        sigma = sigma_from(x)
        tau = fano_tau(rng)
        D = config_data(tau, sigma)
        full_tests(D, mode)
