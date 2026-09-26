"""Interlacing lemma (C1, 26/09 night): Alt (21-dim) lies in V35 = ker B+ cap 1^perp where Q has spectrum 3^20 (-4)^15,
so Q_A has eigenvalue 3 with multiplicity >= 6 and -4 with multiplicity >= 1, K = 0 on those eigenvectors, hence
rank K <= 14 with K_{YP} = (phi_{P0}(Y) - phi_{P1}(Y))/2 (pair level).  Here: rank of K in pair-level solutions of the
anchored K3 survivors (sib model + Alt identity), for several random objectives."""
import sys, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from sib_model import from_anchored_motif
from general_model import PAIRS
from motiflib import two_factors
from sib_labeled import build_sib_labeled
from alt_sib3 import add_alt_sib_all

sig = [(1, 3), (1, 5), (3, 5)]
In = {1: [2, 4, 6, 7], 3: [2, 4, 6, 7], 5: [2, 4, 6, 7], 2: [4, 7], 4: [6, 7], 6: [2, 7], 7: []}
fixed = {2: [(4, 7), (4, 7)], 4: [(6, 7), (6, 7)], 6: [(2, 7), (2, 7)]}
opts = two_factors([2, 4, 6, 7], lambda j, k: True)
choice = tuple(int(c) for c in sys.argv[1:4]) if len(sys.argv) > 3 else (1, 1, 1)
Dg = dict(fixed)
Dg.update({s: opts[c] for s, c in zip((1, 3, 5), choice)})
orbs = from_anchored_motif([(a - 1, b - 1) for a, b in sig], {k - 1: [m - 1 for m in v] for k, v in In.items()},
                           {k - 1: [(a - 1, b - 1) for a, b in E] for k, E in Dg.items()})
A, lo, hi, lb, ub, nvar, phi, ns, y, lab = build_sib_labeled(orbs)
A, lo, hi, lb, ub, nvar, _ = add_alt_sib_all(A, lo, hi, lb, ub, nvar, phi, orbs)
by_pair = {P: [i for i, o in enumerate(orbs) if o['pair'] == P] for P in PAIRS}
rng = np.random.default_rng(1)
for trial in range(6):
    c = np.zeros(nvar)
    for (i, P), v in phi.items():
        c[v] = rng.normal()
    res = milp(c, constraints=[LinearConstraint(A, lo, hi)], integrality=np.ones(nvar), bounds=Bounds(lb, ub),
               options={'time_limit': 30})
    if res.status != 0:
        print('trial', trial, 'status', res.status)
        continue
    x = np.round(res.x).astype(int)
    K = np.zeros((21, 21))
    for a, Y in enumerate(PAIRS):
        for b, P in enumerate(PAIRS):
            if Y == P:
                continue
            P0, P1 = by_pair[P]
            K[a, b] = (x[phi[(P0, Y)]] - x[phi[(P1, Y)]]) / 2
    print('trial', trial, 'rank K =', np.linalg.matrix_rank(K), ' (must be <= 14)  nonzero entries', int((K != 0).sum()))
