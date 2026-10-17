"""Abstract balance test.  W = (+)_{i<q} (R_i + S_i), dim R_i = dim S_i = d.  E subset W of dim q*d (half).
Constraint: compression of P_E to each part Z_i is  alpha on R_i, 1-alpha on S_i  (block-diagonal, no R-S mixing).
243: q = 3 parts, alpha = 2/3.   Measure m - m' and sum cos 2theta of (R, E)."""
import numpy as np, sys
from scipy.optimize import least_squares
q, d, alpha, trials = int(sys.argv[1]), int(sys.argv[2]), float(eval(sys.argv[3])), int(sys.argv[4])
n = 2 * q * d; h = q * d
Kd = np.concatenate([np.concatenate([np.full(d, alpha), np.full(d, 1 - alpha)]) for _ in range(q)])
blocks = [slice(2 * d * i, 2 * d * (i + 1)) for i in range(q)]
Ridx = np.concatenate([np.arange(2 * d * i, 2 * d * i + d) for i in range(q)])
def res(x):
    Q, _ = np.linalg.qr(x.reshape(n, h)); P = Q @ Q.T
    r = []
    for i, b in enumerate(blocks):
        B = P[b, b] - np.diag(Kd[b]); r.append(B[np.triu_indices(2 * d)])
    return np.concatenate(r)
rng = np.random.default_rng(int(sys.argv[5]) if len(sys.argv) > 5 else 0)
stats = {}
for t in range(trials):
    sol = least_squares(res, rng.standard_normal(n * h), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=20000)
    if np.linalg.norm(sol.fun) > 1e-9: continue
    Q, _ = np.linalg.qr(sol.x.reshape(n, h)); P = Q @ Q.T; U = 2 * P - np.eye(n)
    C = U[np.ix_(Ridx, Ridx)]; ev = np.sort(np.linalg.eigvalsh(C))
    m = int(np.sum(ev > 1 - 1e-7)); mp = int(np.sum(ev < -1 + 1e-7))
    inner = ev[(ev <= 1 - 1e-7) & (ev >= -1 + 1e-7)]
    key = (m, mp, round(float(inner.sum()), 6), tuple(np.round(inner, 4)))
    stats[key] = stats.get(key, 0) + 1
for k, v in sorted(stats.items(), key=lambda z: -z[1]):
    print(v, "m=%d m'=%d sum_cos2=%.6f  m-m'+sum=%.6f" % (k[0], k[1], k[2], k[0] - k[1] + k[2]), "inner:", k[3])
