r"""X19k -- export the cell-level infeasibility certificate of the Fano witness for independent verification.
Files (data/x19k_witness_cells.*):
  .npz  : A (CSR: data/indices/indptr/shape, integer coefficients), b (integer rhs), y_int (int64), D (scale)
  .json : tau, sigma, row names, column names (x|z|t with the class type, s|z|t|R|split), conventions
Claim: with all variables in [0,1] (x <= 1 by conv, s <= x by cons),  b.y_int - sum_j max(0, (A^T y_int)_j) > 0,
hence A v = b has no solution v in [0,1]^n: the witness (tau, sigma) is impossible in any srg(99,14,1,2),
PROVIDED every row is an exact consequence -- that is what the verifier should recompute independently.
Row families: conv, cons (sum_k s[z,t,R,k] = x[z,t]), bal, lab, P2 (block level, notes/117), cellcross
(signed cell A_R - B_R  x  block R'), cellsame (cells of one block), cellbal (e(C,C') = e(C',C)),
celllab (sum_{y containing u} c_y(C) = 4).  Cells: A = {c_s d_t : s = t}, B = {s != t} in block {c < d}."""
import sys, json, pickle
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import hstack, identity
sys.path.insert(0, 'scripts')
import x19i_cells as XC

W = pickle.load(open('data/x15_witness.pkl', 'rb'))
tau, sigma = W['tau'], W['sigma']
A, b, nv, rnames, var, T, spec = XC.build(tau, sigma, track=True)
m = A.shape[0]
res = linprog(np.concatenate([np.zeros(nv), np.ones(2 * m)]), A_eq=hstack([A, identity(m, format='csr'),
              -identity(m, format='csr')]).tocsr(), b_eq=b, bounds=[(0, 1)] * nv + [(0, None)] * (2 * m),
              method='highs-ipm')
y = res.eqlin.marginals
D = 10 ** 6
yi = np.rint(np.asarray(y) * D).astype(np.int64)
Ai = A.tocsr().astype(np.int64)
colv = Ai.T @ yi
bi = np.rint(b).astype(np.int64)
val = int(bi @ yi) - int(colv[colv > 0].sum())
print('phase-1', res.fun, ' scaled-integer Farkas value', val, '/', D, '=', val / D, '=>', 'CERTIFIED' if val > 0 else 'NOT')
fmt = lambda l: f'{l[0]}.{l[1]}'
pn = lambda z: '-'.join(fmt(l) for l in sorted(z))
bn = lambda R: ''.join(map(str, sorted(R)))
cnames = []
for v in var:
    if v[0] == 'x':
        _, z, i = v
        cnames.append(f'x|{pn(z)}|{i}|' + ','.join(f'{bn(R)}:{mm}' for R, mm in sorted(T[z][i].items(), key=lambda kv: bn(kv[0]))))
    else:
        _, z, i, R, k = v
        cnames.append(f's|{pn(z)}|{i}|{bn(R)}|A{k[0]}B{k[1]}')
np.savez_compressed('data/x19k_witness_cells.npz', data=Ai.data, indices=Ai.indices, indptr=Ai.indptr,
                    shape=np.array(Ai.shape), b=bi, y_int=yi, D=np.array([D]))
json.dump(dict(note=__doc__, tau={fmt(u): [[fmt(v), fmt(w)] for v, w in tau[u].items() if v < w] for u in tau},
               sigma={str(c): [[fmt(v), fmt(w)] for v, w in sigma[c].items()] for c in sigma},
               specials={pn(z): [pn(w) for w in spec[z]] for z in spec},
               rows=rnames, cols=cnames, farkas_scaled=val, D=D), open('data/x19k_witness_cells.json', 'w'))
print('written data/x19k_witness_cells.npz / .json;', m, 'rows,', nv, 'columns, nnz', Ai.nnz)
