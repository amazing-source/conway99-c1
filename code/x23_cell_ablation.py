r"""X23 -- which row families carry the cell-level deaths?  For one configuration killed at the cell level (X19i),
re-solve with (a) the block level plus ONE cell family, (b) everything minus ONE family.  conv/cons always kept.
Short tests (<= 240 s each) that only guide the hand analysis.
usage: python x23_cell_ablation.py <witness | s11#k | s21c#k>"""
import sys, pickle, time
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, 'scripts')
import x19i_cells as XC

BLOCK = ['bal', 'lab', 'P2']
CELL = ['cellcross', 'cellsame', 'cellbal', 'celllab']

def load(name):
    if name == 'witness':
        return pickle.load(open('data/x15_witness.pkl', 'rb'))
    src, k = name.split('#')
    f = {'s11': 'data/x19_survivors_s11_S0.pkl', 's21c': 'data/x19_cellkilled_s21.pkl'}[src]
    return pickle.load(open(f, 'rb'))[int(k)]

def status(A, b, mask, tl=240):
    t0 = time.time()
    res = linprog(np.zeros(A.shape[1]), A_eq=A[mask], b_eq=b[mask], bounds=(0, None), method='highs-ipm',
                  options=dict(time_limit=tl))
    st = {0: 'feasible', 2: 'INFEASIBLE'}.get(res.status, 'status %d' % res.status)
    return f'{st} ({time.time() - t0:.0f}s)'

if __name__ == '__main__':
    name = sys.argv[1]
    C = load(name)
    A, b, nv, rn, var, T, spec = XC.build(C['tau'], C['sigma'], track=True)
    fam = np.array([r.split('|')[0] for r in rn])
    base = np.isin(fam, ['conv', 'cons'])
    print(f'{name}: {A.shape[0]} rows, {nv} vars', flush=True)
    print(f'  full                : {status(A, b, np.ones(len(fam), bool))}', flush=True)
    print(f'  block only          : {status(A, b, base | np.isin(fam, BLOCK))}', flush=True)
    for f in CELL:
        print(f'  block + {f:<12}: {status(A, b, base | np.isin(fam, BLOCK + [f]))}', flush=True)
    for f in BLOCK + CELL:
        print(f'  all - {f:<14}: {status(A, b, fam != f)}', flush=True)
