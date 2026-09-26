"""Export (no solving) of the 48 pair-level models of 3K2_or14 step 1 (notes/131 sec. 7), for exact certification
elsewhere (structures' ad/certify.py: certify(A, lo, hi, lb, ub)).
Model: sib model + Alt identities on the unique feasible fixed D of 3K2_or14 (same build as k3k2_types.py).
Case (P, t, m, val): the phi variable of sib orbit t of sib pair P on the sink pair {2, m} is fixed to val in {0, 2}
(a (2,0) type).  All 48 infeasible  <=>  every sib orbit has perm type (phi = 1) on every sink-2 pair, i.e. its shadow
on star(2) has one label per block - the input of the rigid-row argument.
Output: ../../data/k3k2_step1_models/case_NN.npz (A as CSR: A_data, A_indices, A_indptr, A_shape; lo, hi, lb, ub,
integrality) and index.json (case -> P, t, m, val, fixed variable)."""
import sys, json, os
import numpy as np
import scipy.sparse as sp
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from sib_model import from_anchored_motif
from general_model import pr
from sib_labeled import build_sib_labeled
from alt_sib3 import add_alt_sib_all

here = os.path.dirname(os.path.abspath(__file__))
data = os.path.join(here, '..', '..', 'data')
d = json.load(open(os.path.join(data, 'fixedD_anchored_C1.json')))['C1_anch_3K2_or14'][0]
Dg = {int(k): [tuple(e) for e in v] for k, v in d.items()}
In0 = {0: [5, 6], 1: [0, 4], 2: [0, 1, 3, 4, 5, 6], 3: [0, 4], 4: [5, 6], 5: [1, 3], 6: [1, 3]}
orbs = from_anchored_motif([(0, 4), (1, 3), (5, 6)], In0, Dg)
A, lo, hi, lb, ub, nvar, phi, ns, y, lab = build_sib_labeled(orbs)
A, lo, hi, lb, ub, nvar, _ = add_alt_sib_all(A, lo, hi, lb, ub, nvar, phi, orbs)
A = sp.csr_matrix(A)
lo, hi, lb, ub = (np.asarray(v, dtype=float) for v in (lo, hi, lb, ub))
integ = np.ones(nvar, dtype=np.int8)
print('model: %d rows x %d vars, nnz %d' % (A.shape[0], A.shape[1], A.nnz))
print('non-integer coefficients:', int(np.sum(np.abs(A.data - np.round(A.data)) > 0)),
      '| infinite row bounds:', int(np.sum(~np.isfinite(lo))), int(np.sum(~np.isfinite(hi))))

sibs = {}
for i, o in enumerate(orbs):
    if o['pivot'] == 'sib':
        sibs.setdefault(o['pair'], []).append(i)
out = os.path.join(data, 'k3k2_step1_models')
os.makedirs(out, exist_ok=True)
index = []
k = 0
for P, orbits_P in sibs.items():
    for t, i0 in enumerate(orbits_P):
        for m in range(7):
            if m == 2 or m in P:
                continue
            v = phi[(i0, pr(2, m))]
            for val in (0, 2):
                lb2, ub2 = lb.copy(), ub.copy()
                lb2[v] = ub2[v] = val
                np.savez_compressed(os.path.join(out, 'case_%02d.npz' % k), A_data=A.data, A_indices=A.indices,
                                    A_indptr=A.indptr, A_shape=np.array(A.shape), lo=lo, hi=hi, lb=lb2, ub=ub2,
                                    integrality=integ)
                index.append({'case': k, 'sib_pair': list(P), 'orbit': t, 'orbit_index': i0, 'sink_pair': [2, m],
                              'var': int(v), 'value': val})
                k += 1
json.dump({'model': '3K2_or14 fixed D, sib model + Alt identities (k3k2_types.py build)',
           'claim': 'all cases infeasible (scipy/HiGHS MILP, 48/48, not yet certified exactly)',
           'rows': int(A.shape[0]), 'vars': int(nvar), 'cases': index}, open(os.path.join(out, 'index.json'), 'w'),
          indent=1)
# reload check
z = np.load(os.path.join(out, 'case_00.npz'))
A2 = sp.csr_matrix((z['A_data'], z['A_indices'], z['A_indptr']), shape=tuple(z['A_shape']))
assert (A2 != A).nnz == 0 and np.array_equal(z['lo'], lo) and np.array_equal(z['hi'], hi)
print('exported %d cases to %s' % (k, os.path.normpath(out)))
