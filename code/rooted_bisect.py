import sys, pickle, glob
import numpy as np
f = sys.argv[1]
D = pickle.load(open(f, 'rb'))
fams, L, l0 = D['fams'], D['L'], D['l0']
Linv = np.linalg.inv(L)
sel = [int(i) for i in sys.argv[2].split(',')] if len(sys.argv) > 2 else range(len(fams))
def minrel(t, G0, G1, G2):
    G = G0 + t[0] * G1 + t[1] * G2
    d = np.sqrt(np.maximum(np.abs(np.diag(G)), 1e-300))
    return np.linalg.eigvalsh(G / d[:, None] / d[None, :])[0]
def feasible(Pv, nS=121):
    n3 = 4158 - 3 * Pv
    for Sv in np.linspace(0, n3, nS):
        t = Linv @ (np.array([Pv, Sv]) - l0)
        if all(minrel(t, *fams[i][2:5]) > -1e-10 for i in sel):
            return Sv
    return None
lo, hi = 1100.0, 1170.0
assert feasible(lo) is not None
while hi - lo > 1e-3:
    mid = (lo + hi) / 2
    if feasible(mid) is not None:
        lo = mid
    else:
        hi = mid
print('families', [fams[i][0] for i in sel], ': max feasible P ~', round(lo, 3), ' (S witness', feasible(lo), ')')
