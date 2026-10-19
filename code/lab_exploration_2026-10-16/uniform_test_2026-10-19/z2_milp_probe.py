"""Strength probe (NOT a proof): the second-order design with integer multiplicities n (and optionally integer M),
solved by HiGHS MILP.  usage: python z2_milp_probe.py <codex dir> <catalogue> <index> <seconds> [--int-m] [--triangles]"""
import gzip, json, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
CODEX, CAT, IDX, SEC = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
sys.path.insert(0, CODEX); sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_z_distribution import RECTANGLES, row_catalogue
import z2lib
t0 = time.process_time()
template = json.loads(gzip.decompress(Path(CAT).read_bytes()))['open'][IDX]['template']
cat = row_catalogue(template, max_free=7)
R = [tuple(q) for q in RECTANGLES]
S = z2lib.build_system(template, R, cat)
if '--triangles' in sys.argv:
    z2lib.add_triangles(S, R)
nv = len(S['names'])
def mat(rows):
    r, c, v = [], [], []
    for i, row in enumerate(rows):
        for j, a in row.items():
            r.append(i); c.append(j); v.append(a)
    return coo_matrix((v, (r, c)), shape=(len(rows), nv)).tocsr()
cons = [LinearConstraint(mat(S['eq']), np.array(S['beq'], float), np.array(S['beq'], float))]
if S['ub']:
    cons.append(LinearConstraint(mat(S['ub']), -np.inf, np.array(S['bub'], float)))
T = len(S['types'])
integrality = np.zeros(nv)
integrality[:T] = 1
if '--int-m' in sys.argv:
    integrality[T:T + len(S['pairs'])] = 1
res = milp(np.zeros(nv), constraints=cons, integrality=integrality, bounds=Bounds(np.zeros(nv), np.array(S['upper'], float)),
           options={'time_limit': SEC, 'disp': False})
print(json.dumps({'index': IDX, 'int_m': '--int-m' in sys.argv, 'triangles': '--triangles' in sys.argv, 'types': T,
                  'variables': nv, 'status': int(res.status), 'message': res.message[:90], 'cpu': round(time.process_time() - t0, 1)}))
