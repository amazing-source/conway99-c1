"""3K2_or14 fixed D (the unique feasible one): can a sib orbit have (2,0)-type (phi in {0,2}) on a sink pair {2,m}?
Test: sib model + Alt identities, plus the constraint phi_{u}(2m) != 1 for one chosen (sib orbit u, m)."""
import sys, json
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from sib_model import from_anchored_motif
from general_model import pr
from sib_labeled import build_sib_labeled
from alt_sib3 import add_alt_sib_all
d = json.load(open('fixedD_anchored_C1.json'))['C1_anch_3K2_or14'][0]
Dg = {int(k): [tuple(e) for e in v] for k, v in d.items()}
In0 = {0: [5, 6], 1: [0, 4], 2: [0, 1, 3, 4, 5, 6], 3: [0, 4], 4: [5, 6], 5: [1, 3], 6: [1, 3]}
orbs = from_anchored_motif([(0, 4), (1, 3), (5, 6)], In0, Dg)
A, lo, hi, lb, ub, nvar, phi, ns, y, lab = build_sib_labeled(orbs)
A, lo, hi, lb, ub, nvar, _ = add_alt_sib_all(A, lo, hi, lb, ub, nvar, phi, orbs)
sibs = {o['pair']: [] for o in orbs if o['pivot'] == 'sib'}
for i, o in enumerate(orbs):
    if o['pivot'] == 'sib':
        sibs[o['pair']].append(i)
base = milp(np.zeros(nvar), constraints=[LinearConstraint(A, lo, hi)], integrality=np.ones(nvar), bounds=Bounds(lb, ub), options={'time_limit': 60})
print('base feasible:', base.status == 0)
x = np.round(base.x)
for P, (i0, i1) in sibs.items():
    print('sib', P, 'phi on sink pairs:', {m: int(x[phi[(i0, pr(2, m))]]) for m in range(7) if m != 2 and m not in P})
# force a (2,0) type: phi_{u}(2m) = 2 for u = first orbit of pair (0,4), m = 5
for (P, m) in [((0, 4), 5), ((0, 4), 1), ((1, 3), 0), ((5, 6), 1)]:
    i0 = sibs[P][0]
    lb2, ub2 = lb.copy(), ub.copy()
    v = phi[(i0, pr(2, m))]
    for val in (0, 2):
        lb2[v] = ub2[v] = val
        r = milp(np.zeros(nvar), constraints=[LinearConstraint(A, lo, hi)], integrality=np.ones(nvar), bounds=Bounds(lb2, ub2), options={'time_limit': 60})
        print('sib', P, 'orbit0 phi(2%d) forced to %d :' % (m, val), {0: 'FEASIBLE', 2: 'infeasible'}.get(r.status, r.status))
print('--- all combinations ---')
bad = []
for P, orbits_P in sibs.items():
    for t, i0 in enumerate(orbits_P):
        for m in range(7):
            if m == 2 or m in P:
                continue
            v = phi[(i0, pr(2, m))]
            for val in (0, 2):
                lb2, ub2 = lb.copy(), ub.copy()
                lb2[v] = ub2[v] = val
                r = milp(np.zeros(nvar), constraints=[LinearConstraint(A, lo, hi)], integrality=np.ones(nvar),
                         bounds=Bounds(lb2, ub2), options={'time_limit': 60})
                if r.status != 2:
                    bad.append((P, t, m, val, r.status))
print('combinations not proven infeasible:', bad if bad else 'none (all 48 infeasible)')
