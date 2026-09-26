"""Deletion filter on constraint GROUPS (LP level) for a dead K3 D-choice -> minimal infeasible set of facts."""
import sys, time
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from sib_model import from_anchored_motif
from motiflib import two_factors
from sib_labeled import build_sib_labeled

sig = [(1, 3), (1, 5), (3, 5)]
In = {1: [2, 4, 6, 7], 3: [2, 4, 6, 7], 5: [2, 4, 6, 7], 2: [4, 7], 4: [6, 7], 6: [2, 7], 7: []}
fixed = {2: [(4, 7), (4, 7)], 4: [(6, 7), (6, 7)], 6: [(2, 7), (2, 7)]}
opts = two_factors([2, 4, 6, 7], lambda j, k: True)
choice = tuple(int(c) for c in sys.argv[1:4])
Dg = dict(fixed)
Dg.update({s: opts[c] for s, c in zip((1, 3, 5), choice)})
orbs = from_anchored_motif([(a - 1, b - 1) for a, b in sig], {k - 1: [m - 1 for m in v] for k, v in In.items()},
                           {k - 1: [(a - 1, b - 1) for a, b in E] for k, E in Dg.items()})
A, lo, hi, lb, ub, nvar, phi, ns, y, lab = build_sib_labeled(orbs)


def gkey(l):
    if l[0] in ('F1', 'ns'):
        return ('F1', l[1])
    if l[0] == 'bal':
        return ('bal', l[1], l[2])
    if l[0] == 'ydef':
        return ('ydef', l[2])
    return l


groups = {}
for r, l in enumerate(lab):
    groups.setdefault(gkey(l), []).append(r)
keys = [k for k in groups if k[0] != 'ydef']


def feasible(active):
    rows = [r for k in active for r in groups[k]]
    for k in active:
        if k[0] == 'dich':
            rows += groups.get(('ydef', k[1]), [])
    if not rows:
        return True
    Asub = A[rows]
    res = linprog(np.zeros(nvar), A_ub=np.vstack([Asub, -Asub]), b_ub=np.concatenate([hi[rows], -lo[rows]]),
                  bounds=list(zip(lb, ub)), method='highs')
    return res.status == 0


assert not feasible(keys)
rank = {'dich': 0, 'sym': 1, 'bal': 2, 'F1': 3}
order = sorted(keys, key=lambda k: rank[k[0]])
keep = list(keys)
t0 = time.time()
for k in order:
    trial = [x for x in keep if x != k]
    if not feasible(trial):
        keep = trial
print('minimal groups', len(keep), '(%.0fs)' % (time.time() - t0))


def oname(i):
    o = orbs[i]
    P = o['pair']
    piv = o['pivot']
    piv = 'sib' if piv == 'sib' else ('dis' if piv is None else str(piv + 1))
    part = orbs[o['partner']]['pair'] if o['partner'] is not None else None
    return '%d%d/%d(piv %s, D in %s)' % (P[0] + 1, P[1] + 1, i % 2, piv,
                                         '%d%d' % (part[0] + 1, part[1] + 1) if part else '-')


for k in sorted(keep, key=str):
    if k[0] == 'dich':
        print('DICH pair %d%d' % (k[1][0] + 1, k[1][1] + 1))
    elif k[0] == 'sym':
        print('SYM %d%d~%d%d' % (k[1][0] + 1, k[1][1] + 1, k[2][0] + 1, k[2][1] + 1))
    elif k[0] == 'F1':
        print('F1 orbit', oname(k[1]))
    elif k[0] == 'bal':
        print('BAL orbit', oname(k[1]), 'at block', k[2] + 1)
