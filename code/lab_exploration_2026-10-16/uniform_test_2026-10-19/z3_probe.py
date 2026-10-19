"""LP feasibility of the second-order design with the third-order triangle layer (z2lib.build_system + add_triangles).
usage: python z3_probe.py <codex code dir> <catalogue.json.gz> <index> [--no-triangles] [--method=highs-ipm]"""
import gzip
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

CODEX, CAT, IDX = sys.argv[1], sys.argv[2], int(sys.argv[3])
METHOD = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--method=')), 'highs-ipm')
sys.path.insert(0, CODEX)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_z_distribution import RECTANGLES, row_catalogue      # noqa: E402
import z2lib                                                              # noqa: E402

t0 = time.process_time()
template = json.loads(gzip.decompress(Path(CAT).read_bytes()))['open'][IDX]['template']
cat = row_catalogue(template, max_free=7)
R = [tuple(q) for q in RECTANGLES]
S = z2lib.build_system(template, R, cat)
if '--no-triangles' not in sys.argv:
    z2lib.add_triangles(S, R)
nv = len(S['names'])


def mat(rows):
    r, c, v = [], [], []
    for i, row in enumerate(rows):
        for j, a in row.items():
            r.append(i); c.append(j); v.append(a)
    return coo_matrix((v, (r, c)), shape=(len(rows), nv)).tocsr()


build = time.process_time() - t0
res = linprog(np.zeros(nv), A_eq=mat(S['eq']), b_eq=np.array(S['beq'], float),
              A_ub=mat(S['ub']) if S['ub'] else None, b_ub=np.array(S['bub'], float) if S['ub'] else None,
              bounds=[(0, u) for u in S['upper']], method=METHOD)
print(json.dumps({'index': IDX, 'triangles': '--no-triangles' not in sys.argv, 'types': len(S['types']),
                  'variables': nv, 'equalities': len(S['eq']), 'build_cpu': round(build, 2),
                  'lp_status': int(res.status), 'lp_message': res.message[:80],
                  'cpu_total': round(time.process_time() - t0, 2)}))
