r"""X19n with HiGHS dual simplex (sometimes faster at detecting infeasibility than IPM).  <= 290 s.
usage: python x19n_try_ds.py <file.pkl#k> [method]"""
import sys, pickle, time
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, 'scripts')
import x19n_pairblock as PB
if __name__ == '__main__':
    f, k = sys.argv[1].split('#'); meth = sys.argv[2] if len(sys.argv) > 2 else 'highs-ds'
    C = pickle.load(open(f, 'rb'))[int(k)]
    t0 = time.time(); A, b, nv = PB.build(C['tau'], C['sigma']); t1 = time.time()
    res = linprog(np.zeros(nv), A_eq=A, b_eq=b, bounds=(0, None), method=meth, options=dict(time_limit=290))
    print(f'{sys.argv[1]} [{meth}]: status {res.status} ({res.message}); build {t1-t0:.0f}s solve {time.time()-t1:.0f}s', flush=True)
