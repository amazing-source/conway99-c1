r"""X19q -- pair x block level (X19n) in phase-1 form: min sum of slacks s.t. A x + s+ - s- = b, x in [0,1].
Optimum > 0 => infeasible; the duals give a Farkas vector, checked exactly (scaled integers).
Usage: python x19q_pairblock_phase1.py <seed11#k | seed21#k> <time_limit>"""
import sys, pickle, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import hstack, identity
sys.path.insert(0, 'scripts')
import x19n_pairblock as PB

name, tlim = sys.argv[1], float(sys.argv[2])
src = 'data/x19_survivors_s11_S0.pkl' if name.startswith('seed11#') else 'data/x19l_final_s21.pkl'
cfg = pickle.load(open(src, 'rb'))[int(name.split('#')[1])]
t0 = time.time()
A, b, nv = PB.build(cfg['tau'], cfg['sigma'])
m = A.shape[0]
res = linprog(np.concatenate([np.zeros(nv), np.ones(2 * m)]),
              A_eq=hstack([A, identity(m, format='csr'), -identity(m, format='csr')]).tocsr(), b_eq=b,
              bounds=[(0, 1)] * nv + [(0, None)] * (2 * m), method='highs-ipm', options=dict(time_limit=tlim))
print(f'{name}: status {res.status} ({res.message}); phase-1 value {res.fun}; {time.time()-t0:.0f}s', flush=True)
if res.status == 0 and res.fun > 1e-6:
    y = res.eqlin.marginals
    Ai = A.tocsr().astype(np.int64); bi = np.rint(b).astype(np.int64)
    for D in (10 ** 6, 10 ** 8):
        yi = np.rint(np.asarray(y) * D).astype(np.int64)
        colv = Ai.T @ yi
        val = int(bi @ yi) - int(colv[colv > 0].sum())
        if val > 0:
            break
    print(f'  exact scaled Farkas {val} (D = {D}) => {"CERTIFIED INFEASIBLE" if val > 0 else "not certified"}', flush=True)
    if val > 0:
        pickle.dump(dict(tau=cfg['tau'], sigma=cfg['sigma'], D=D, y_int=yi, value_scaled=val),
                    open(f'data/x19q_cert_{name.replace("#", "_")}.pkl', 'wb'))
elif res.status == 0:
    print('  => FEASIBLE at the pair x block level (phase-1 value ~ 0)', flush=True)
