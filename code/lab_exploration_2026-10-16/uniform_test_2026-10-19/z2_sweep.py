"""One-pass sweep of the second-order count design (z2lib, rectangle level) over a list of c = 3 templates (LAB
19/10/2026).  FIRST PASS ONLY, as requested by the user: an LP feasibility verdict per template (HiGHS interior point),
no certificate, no second pass.  INFEASIBLE here is a solver verdict to be certified later (z2_certify.py +
z2_verify.py); FEASIBLE means the design does not kill the template.
usage: python z2_sweep.py <codex code dir> <list.json: [[source, index], ...]> <out.jsonl> <gz catalogue> <g1 json> <g2 json>
       [--time-limit=900]"""
import gzip
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

CODEX, LST, OUT, GZ, G1, G2 = sys.argv[1:7]
TL = float(next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--time-limit=')), 900))
sys.path.insert(0, CODEX)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_z_distribution import RECTANGLES, row_catalogue      # noqa: E402
import z2lib                                                              # noqa: E402

src = {'gz': json.loads(gzip.decompress(Path(GZ).read_bytes()))['open'],
       'g1': json.load(open(G1))['templates'], 'g2': json.load(open(G2))['templates']}
R = [tuple(q) for q in RECTANGLES]
done = set()
if os.path.exists(OUT):
    done = {(json.loads(l)['source'], json.loads(l)['index']) for l in open(OUT) if l.strip()}
for tag, idx in json.load(open(LST)):
    if (tag, idx) in done:
        continue
    t0 = time.process_time()
    rec = {'source': tag, 'index': idx}
    try:
        tpl = src[tag][idx]['template'] if tag == 'gz' else src[tag][idx]
        cat = row_catalogue(tpl, max_free=8)
        rec['catalogue'] = cat['status']
        if cat['status'] != 'ROW_CATALOGUE_COMPLETE':
            rec['verdict'] = 'NO_CATALOGUE'
        else:
            S = z2lib.build_system(tpl, R, cat)
            nv = len(S['names'])

            def mat(rows):
                r, c, v = [], [], []
                for i, row in enumerate(rows):
                    for j, a in row.items():
                        r.append(i); c.append(j); v.append(a)
                return coo_matrix((v, (r, c)), shape=(len(rows), nv)).tocsr()
            res = linprog(np.zeros(nv), A_eq=mat(S['eq']), b_eq=np.array(S['beq'], float),
                          A_ub=mat(S['ub']) if S['ub'] else None, b_ub=np.array(S['bub'], float) if S['ub'] else None,
                          bounds=[(0, u) for u in S['upper']], method='highs-ipm', options={'time_limit': TL})
            rec.update(types=len(S['types']), variables=nv, lp_status=int(res.status),
                       verdict={0: 'FEASIBLE', 2: 'INFEASIBLE'}.get(int(res.status), 'UNDECIDED'),
                       message=res.message[:80], free_dimension=cat['free_dimension'])
    except Exception as e:                                  # recorded, never counted as an exclusion
        rec.update(verdict='ERROR', error=repr(e)[:300])
    rec['cpu'] = round(time.process_time() - t0, 2)
    with open(OUT, 'a') as f:
        f.write(json.dumps(rec) + '\n')
