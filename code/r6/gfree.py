# CHECK: the G-free combination 2*even + odd = 36I + 2J - 2|R||R|^T - RR^T (minus 8D_UU = 0 in J1a) must be PSD on U.
# It depends only on the D7 vectors of the support labels (positive reps). J1a type (v), all a-cases.
import numpy as np, itertools
blocks = ['c', 'p', 'q', 'r', 's', 't', 'u']; bi = {b: i for i, b in enumerate(blocks)}
def run(a):
    labs = [(b, t) for b in 'pqrstu' for t in (1, -1)] + ['V1', 'V2', 'V3']
    R = []
    for L in labs:
        v = [0] * 7
        if L == 'V1': v[bi['p']] = 1; v[bi['q']] = -1
        elif L == 'V2': v[bi['q']] = 1; v[bi['r']] = -1
        elif L == 'V3': v[bi['r']] = 1; v[bi['p']] = -1
        else: b, t = L; v[0] = a[b]; v[bi[b]] = t
        R.append(v)
    R = np.array(R, float); Ra = np.abs(R); n = len(labs)
    M = 36 * np.eye(n) + 2 * np.ones((n, n)) - 2 * Ra @ Ra.T - R @ R.T
    return np.linalg.eigvalsh(M)
for plus in itertools.combinations('pqrstu', 3):
    a = {b: (1 if b in plus else -1) for b in 'pqrstu'}
    w = run(a)
    print('B+ =', ''.join(plus), ' min eig', round(w[0], 3), ' #neg', int(np.sum(w < -1e-9)))
