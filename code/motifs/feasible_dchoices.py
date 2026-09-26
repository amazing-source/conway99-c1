"""For one anchored motif orientation (index in motiflib.survivors_full), list all D-graph choices (per pivot) that pass T+
and are feasible in the sib pair model.  Usage: python feasible_dchoices.py <motif> <orientation> <seconds>"""
import sys, time, itertools, json
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from sib_model import from_anchored_motif, feasible_sib
from motiflib import MOTIFS, B, survivors_full, two_factors
from run_k2_sweep_lib import tplus_ok

name, n_or, tlim = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
sig = MOTIFS[name]
Sset = set(frozenset(p) for p in sig)
sibp = {k: [m for m in B if frozenset((k, m)) in Sset] for k in B}
arc, indeg, o, In = survivors_full(name, sig)[n_or]
piv = [i for i in B if indeg[i] >= 2]
allowed_at = lambda i: (lambda j, k: o[k] >= 3 + ((k, j) in arc) and o[j] >= 3 + ((j, k) in arc))
Dopts = [two_factors(In[i], allowed_at(i)) for i in piv]
print(name, n_or, 'pivots', piv, 'options per pivot', [len(d) for d in Dopts])
t0 = time.time()
feas, tested, tp = [], 0, 0
for Dchoice in itertools.product(*Dopts):
    if time.time() - t0 > tlim:
        print('time cap')
        break
    Dg = dict(zip(piv, Dchoice))
    if not tplus_ok(sig, arc, o, In, Dg, sibp):
        continue
    tp += 1
    orbs = from_anchored_motif([(a - 1, b - 1) for a, b in sig], {k - 1: [m - 1 for m in v] for k, v in In.items()},
                               {k - 1: [(a - 1, b - 1) for a, b in E] for k, E in Dg.items()})
    r = feasible_sib(orbs, time_limit=20)
    tested += 1
    if r is not None and not isinstance(r, str):
        feas.append({str(k - 1): [[a - 1, b - 1] for a, b in E] for k, E in Dg.items()})
print('passing T+:', tp, ' tested:', tested, ' feasible:', len(feas), '(%.0fs)' % (time.time() - t0))
json.dump(feas, open('feasD_%s_or%d.json' % (name, n_or), 'w'))
for f in feas[:6]:
    print(f)
