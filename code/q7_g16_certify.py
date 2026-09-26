"""Exact certificates (structures' ad/certify.py: rational Farkas / branching) for the 8 t = 2 classes that survive Witt +
unary filters: the LOCAL model (one option per orbit, (i), (ii), (iii); no pairwise rigid-row constraint) is infeasible."""
import sys, json
import numpy as np
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from certify import certify, check
from q7_g16_ilp import build_model

summ = json.load(open('g16_unary_summary.json'))
alive = [s for s in summ if s['t'] == 2 and s['min_opts'] > 0]
out = []
for s in alive:
    A, lo, hi, nv, info = build_model(tuple(s['tau']), tuple(s['eta']), pairwise=False)
    lo = np.array(lo, float); hi = np.array(hi, float)
    lb = np.zeros(nv); ub = np.ones(nv)
    c = certify(A, lo, hi, lb, ub, maxnodes=400)
    ok = check(A, lo, hi, lb, ub, c['tree']) if c['status'] == 'dead' else False
    print(s['tau'], s['eta'], c['status'], c.get('level'), 'nodes', c.get('nodes'), 'exact re-check:', ok, flush=True)
    out.append({'tau': s['tau'], 'eta': s['eta'], 'status': c['status'], 'level': c.get('level'), 'check': ok,
                'tree': c.get('tree')})
json.dump(out, open('g16_stage2_certificates.json', 'w'))
print('all dead and re-checked:', all(o['status'] == 'dead' and o['check'] for o in out))
