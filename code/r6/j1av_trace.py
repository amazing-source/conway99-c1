# CHECK on the explicit configuration of j1av_psd_one.py: the averaged Schur-complement test.
# T_tr := trace(N^{-1} M_sV Pi M_Vs) with N = 12I + 4G_star, and the same quantity with M_ss^+ in place of N^{-1}.
# The plane test fails (i.e. the configuration dies) as soon as the M_ss^+ version exceeds 10.
import numpy as np
exec(open(__file__.replace('j1av_trace.py','j1av_psd_one.py')).read().split("eo, ee = cfg")[0])
Q = [(('p', 1), ('s', 1)), (('q', -1), ('t', 1)), (('p', -1), ('s', -1)), (('r', -1), ('u', 1)), (('q', 1), ('t', -1)), (('r', 1), ('u', -1))]
P = [(('p', 1), ('r', -1)), (('p', -1), ('q', 1)), (('q', -1), ('r', 1)), (('s', 1), ('u', -1)), (('s', -1), ('t', 1)), (('t', -1), ('u', 1))]
groups = [[('p', 1), ('q', -1), ('s', 1), ('t', 1)], [('p', -1), ('r', -1), ('s', -1), ('u', 1)], [('q', 1), ('r', 1), ('t', -1), ('u', -1)]]
star = labels[:12]
n = 15
G = np.zeros((n, n))
for (x, y) in Q + P:
    G[idx[x], idx[y]] = G[idx[y], idx[x]] = 1
B = np.zeros((12, 3))
for k, Gk in enumerate(groups):
    for L in Gk:
        B[idx[L], k] = 1
Gs = G[:12, :12]
R = np.array([rvec(L) for L in labels], dtype=float); Rs, RV = R[:12], R[12:]
Mss = 12 * np.eye(12) + 4 * Gs - Rs @ Rs.T
MsV = 4 * B - Rs @ RV.T
Nn = 12 * np.eye(12) + 4 * Gs
Pi = np.eye(3) - np.ones((3, 3)) / 3
Tn = np.trace(np.linalg.inv(Nn) @ MsV @ Pi @ MsV.T)
Tm = np.trace(np.linalg.pinv(Mss) @ MsV @ Pi @ MsV.T)
print('trace with N^-1   :', round(Tn, 4), '  (> 10 kills)')
print('trace with Mss^+  :', round(Tm, 4))
Y = Pi @ MsV.T @ np.linalg.pinv(Mss) @ MsV @ Pi
print('plane eigenvalues of Y (kill iff max > 5):', np.round(np.linalg.eigvalsh(Y), 4))
