r"""X19j -- exact Farkas certificate for the cell-refined system (X19i) of a given configuration.
All variables are in [0,1] (x <= 1 by convexity, s <= x), so the certificate condition is
      b . y  -  sum_j max(0, col_j . y)  >  0     (checked in exact rationals).
Also reports how the certificate weight splits between row families (block-level vs cell-level)."""
import sys, pickle, time
from fractions import Fraction as Fr
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import hstack, identity
sys.path.insert(0, 'scripts')
import x19i_cells as XC

def family_bounds(tau, sigma):
    """row index ranges per family, recomputed in the same order as XC.build."""
    import itertools
    from x14_triangle_supports import LAB
    sinv = {c: {w: v for v, w in sigma[c].items()} for c in range(7)}
    spec = {z: XC.X.specials(z, tau, sigma, sinv) for z in XC.PAIRS}
    T = {z: XC.X.types_for(z, spec[z]) for z in XC.PAIRS}
    n_conv = 84; n_cons = sum(len(t) for z in XC.PAIRS for t in T[z])
    fam = [('conv', n_conv), ('consistency', n_cons), ('block balance', 210),
           ('label balance', sum(1 for u in LAB for R in XC.BLOCKS if u[0] not in R)), ('P2 blocks', 231),
           ('cell cross (A-B)xR', 441), ('cell same-block', 63), ('cell balance', 861),
           ('cell label balance', sum(1 for u in LAB for C in XC.CELLS if u[0] not in C[0]))]
    return fam

def certify(tau, sigma, fname=None):
    t0 = time.time()
    A, b, nv = XC.build(tau, sigma)
    m = A.shape[0]
    I = identity(m, format='csr')
    res = linprog(np.concatenate([np.zeros(nv), np.ones(2 * m)]), A_eq=hstack([A, I, -I]).tocsr(), b_eq=b,
                  bounds=[(0, 1)] * nv + [(0, None)] * (2 * m), method='highs-ipm')
    y = res.eqlin.marginals
    print(f'phase-1 value {res.fun:.6f} ({time.time()-t0:.0f}s)', flush=True)
    if res.fun < 1e-7:
        return None
    # scaled-integer certificate: y_int = round(D * y); exact integer check (int64 is exact at these sizes)
    for D in (10 ** 6, 10 ** 8, 10 ** 10):
        yi = np.rint(np.asarray(y) * D).astype(np.int64)
        Ai = A.tocsr().astype(np.int64)
        colv = Ai.T @ yi                      # exact integer column values
        bi = np.rint(b).astype(np.int64)
        val = int(bi @ yi) - int(colv[colv > 0].sum())
        if val > 0:
            break
    print(f'exact (scaled-integer, D = {D}) Farkas value {val / D:.6f} => {"CERTIFIED INFEASIBLE" if val > 0 else "not certified"}', flush=True)
    # weight by family
    fam = family_bounds(tau, sigma)
    pos = 0; out = []
    for name, n in fam:
        w = float(sum(abs(y[pos:pos + n])))
        out.append((name, n, round(w, 3))); pos += n
    print('  |y| weight by row family:', out, flush=True)
    if fname:
        pickle.dump(dict(tau=tau, sigma=sigma, y_int=yi.tolist(), D=D, b=[int(round(v)) for v in b], value_scaled=val),
                    open(fname, 'wb'))
    return val

if __name__ == '__main__':
    W = pickle.load(open('data/x15_witness.pkl', 'rb'))
    certify(W['tau'], W['sigma'], 'data/x19j_witness_cells_cert.pkl')
