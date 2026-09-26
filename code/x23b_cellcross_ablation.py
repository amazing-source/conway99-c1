r"""X23b -- inside the killing family 'cellcross' (signed cell of R x whole block R'): which (R, R') relations are
needed, and are P2 / bal / lab needed?  Short tests (<= 240 s each), guidance for the hand analysis only.
usage: python x23b_cellcross_ablation.py <witness | s11#k | s21c#k>"""
import sys
import numpy as np
sys.path.insert(0, 'scripts')
import x19i_cells as XC
from x23_cell_ablation import load, status

if __name__ == '__main__':
    name = sys.argv[1]
    C = load(name)
    A, b, nv, rn, var, T, spec = XC.build(C['tau'], C['sigma'], track=True)
    fam = np.array([r.split('|')[0] for r in rn])
    rel = np.full(len(rn), -1)
    for i, r in enumerate(rn):
        if r.startswith('cellcross|'):
            _, R, Rp = r.split('|')
            rel[i] = len(set(R) & set(Rp))
    base = np.isin(fam, ['conv', 'cons'])
    cc = fam == 'cellcross'
    tests = [
        ('bal + lab + cellcross (no P2)', base | np.isin(fam, ['bal', 'lab']) | cc),
        ('P2 + cellcross (no bal, lab)', base | (fam == 'P2') | cc),
        ('cellcross only', base | cc),
        ('block + cellcross, |R cap R\'| = 2', base | np.isin(fam, ['bal', 'lab', 'P2']) | (cc & (rel == 2))),
        ('block + cellcross, |R cap R\'| = 1', base | np.isin(fam, ['bal', 'lab', 'P2']) | (cc & (rel == 1))),
        ('block + cellcross, R, R\' disjoint', base | np.isin(fam, ['bal', 'lab', 'P2']) | (cc & (rel == 0))),
        ('block + cellcross, |R cap R\'| >= 1', base | np.isin(fam, ['bal', 'lab', 'P2']) | (cc & (rel >= 1))),
    ]
    print(f'{name}: {A.shape[0]} rows, {nv} vars', flush=True)
    for lab_, m in tests:
        print(f'  {lab_:<38}: {status(A, b, m)}', flush=True)
