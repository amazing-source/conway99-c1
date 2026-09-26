"""Anchored K3 survivors (27 C4 choices at the sinks, plus 3 dead digon choices as controls): sib pair model + the Alt
identity between sib pairs sharing a block (alt_sib.py)."""
import sys, time, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from sib_model import from_anchored_motif
from motiflib import two_factors
from sib_labeled import build_sib_labeled
from alt_sib import add_alt_sib

sig = [(1, 3), (1, 5), (3, 5)]
In = {1: [2, 4, 6, 7], 3: [2, 4, 6, 7], 5: [2, 4, 6, 7], 2: [4, 7], 4: [6, 7], 6: [2, 7], 7: []}
fixed = {2: [(4, 7), (4, 7)], 4: [(6, 7), (6, 7)], 6: [(2, 7), (2, 7)]}
opts = two_factors([2, 4, 6, 7], lambda j, k: True)
choices = [c for c in itertools.product((1, 2, 4), repeat=3)] + [(0, 1, 1), (3, 1, 1), (5, 2, 4)]
t0 = time.time()
for choice in choices:
    if time.time() - t0 > 270:
        print('time cap')
        break
    Dg = dict(fixed)
    Dg.update({s: opts[c] for s, c in zip((1, 3, 5), choice)})
    orbs = from_anchored_motif([(a - 1, b - 1) for a, b in sig], {k - 1: [m - 1 for m in v] for k, v in In.items()},
                               {k - 1: [(a - 1, b - 1) for a, b in E] for k, E in Dg.items()})
    A, lo, hi, lb, ub, nvar, phi, ns, y, lab = build_sib_labeled(orbs)
    for use_alt in (False, True):
        if use_alt:
            A2, lo2, hi2, lb2, ub2, n2, npairs = add_alt_sib(A, lo, hi, lb, ub, nvar, phi, orbs)
        else:
            A2, lo2, hi2, lb2, ub2, n2 = A, lo, hi, lb, ub, nvar
        res = milp(np.zeros(n2), constraints=[LinearConstraint(A2, lo2, hi2)], integrality=np.ones(n2),
                   bounds=Bounds(lb2, ub2), options={'time_limit': 30})
        st = {0: 'feasible', 2: 'INFEASIBLE'}.get(res.status, 'unknown(%d)' % res.status)
        print(choice, 'alt' if use_alt else 'base', st, '(%.0fs)' % (time.time() - t0))
    sys.stdout.flush()
