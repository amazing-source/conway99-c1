"""Anchored K3 survivor class (notes/130 sec. 6): which D-graph choices at the sinks 1,3,5 stay feasible in the coupled
pair model with sib pairs.  Representative: Sigma = {13,15,35}, source 7, cycle 2->6->4->2 (In(2)={4,7}, In(4)={6,7},
In(6)={2,7}); sinks have In = {2,4,6,7}.  Blocks are 1-based here and converted to 0-based for sib_model."""
import sys, time, itertools, json
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from sib_model import feasible_sib, from_anchored_motif
from motiflib import two_factors
sig = [(1, 3), (1, 5), (3, 5)]
In = {1: [2, 4, 6, 7], 3: [2, 4, 6, 7], 5: [2, 4, 6, 7], 2: [4, 7], 4: [6, 7], 6: [2, 7], 7: []}
fixed = {2: [(4, 7), (4, 7)], 4: [(6, 7), (6, 7)], 6: [(2, 7), (2, 7)]}
opts = two_factors([2, 4, 6, 7], lambda j, k: True)
print('2-factors on {2,4,6,7}:', len(opts), opts)
t0 = time.time(); feas = []; n = 0
for choice in itertools.product(range(len(opts)), repeat=3):
    if time.time() - t0 > 270: print('time cap at', n); break
    Dg = dict(fixed); Dg.update({s: opts[c] for s, c in zip((1, 3, 5), choice)})
    orbs = from_anchored_motif([(a-1, b-1) for a, b in sig], {k-1: [m-1 for m in v] for k, v in In.items()},
                               {k-1: [(a-1, b-1) for a, b in E] for k, E in Dg.items()})
    r = feasible_sib(orbs, time_limit=30); n += 1
    if r is not None and not isinstance(r, str): feas.append(choice)
    elif isinstance(r, str): print('unknown', choice)
print('tested', n, 'feasible', len(feas), feas, '(%.0fs)' % (time.time() - t0))
