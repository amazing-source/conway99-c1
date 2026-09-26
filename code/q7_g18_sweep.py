"""g- = 18, regime t = 0 (split blocks, det Q_c non-square): R_c = 0, so T_FF = Z (mod 7) on all 30 far orbits.
Unary filter Z_ff = 0 on every far orbit's options, then the local model (i)+(ii)+(iii) (LP/ILP, small), then if needed the
pairwise rigid-row conditions.  Chunked (laptop rule: one process, < 5 min): python q7_g18_sweep.py START END."""
import sys, json, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from q7_g16_test import classes_t_ge, ball_disc, split, unary_filter
from q7_g16_ilp import build_model

start, end = int(sys.argv[1]), int(sys.argv[2])
tcap = float(sys.argv[3]) if len(sys.argv) > 3 else 270
t0 = time.time()
cls = [c for c in classes_t_ge(0) if c[2] == 0]
cls = [c for c in cls if split(*ball_disc(c[0], c[1]))]
print('t = 0 split classes:', len(cls), '; chunk', start, end, flush=True)
out = []
for idx in range(start, min(end, len(cls))):
    if time.time() - t0 > tcap:
        print('time cap at index', idx, flush=True)
        break
    tau, eta, t, osz = cls[idx]
    rec = {'idx': idx, 'tau': tau, 'eta': eta, 'orbit_size': osz}
    built = build_model(tau, eta, pairwise=False)
    if built is None:
        rec['status'] = 'dead-unary'
    else:
        A, lo, hi, nv, info = built
        rec['opts'] = info['opts_per_orbit']
        r = milp(np.zeros(nv), constraints=[LinearConstraint(A, np.array(lo, float), np.array(hi, float))],
                 integrality=np.ones(nv), bounds=Bounds(0, 1), options={'time_limit': 20})
        rec['status'] = {0: 'local-FEASIBLE', 2: 'dead-local'}.get(r.status, 'local-unknown(%d)' % r.status)
        if r.status == 0:
            built2 = build_model(tau, eta, pairwise=True)
            A2, lo2, hi2, nv2, info2 = built2
            r2 = milp(np.zeros(nv2), constraints=[LinearConstraint(A2, np.array(lo2, float), np.array(hi2, float))],
                      integrality=np.ones(nv2), bounds=Bounds(0, 1), options={'time_limit': 30})
            rec['status'] = {0: 'ALIVE-pairwise', 2: 'dead-pairwise'}.get(r2.status, 'pairwise-unknown(%d)' % r2.status)
    out.append(rec)
from collections import Counter
print(Counter(r['status'] for r in out), '(%.0fs)' % (time.time() - t0), flush=True)
json.dump(out, open('g18_t0_%d_%d.json' % (start, end), 'w'))
