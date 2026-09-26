"""Two full-pivot sib blocks c, d: REAL condition on the cross block Sigma (notes/131 sec. 6).
With c full pivot, M_c = 11I + P_pi - J on X_c (12 labels: d+-, then the 10 labels R), M_c^+ = Pi_even'/12 + Pi_odd/10.
For f = (d+, y) in D: w_f = 4 s_f + delta_f, s_f = column y of Sigma on R (0 on d+-), delta_f = e_{d+} - e_{d-} + e_y - e_{sigma y}.
G_D = 3I - (Z_R)_DD with 4 G_D = 11I - J + P_pi - W_D^T M_c^+ W_D must be PSD of real rank <= 4 (principal block of 7 P_4).
Prints, for random admissible Sigma: min eigenvalue of G_D and its numerical rank."""
import random
import numpy as np
n = 10
Ppi = np.zeros((n, n))
for i in range(n):
    Ppi[i, i ^ 1] = 1
I = np.eye(n)
J = np.ones((n, n))
# X_c labels: 0,1 = d+, d- ; 2..11 = R labels (R label i -> index i+2)
N12 = 12
P12 = np.zeros((N12, N12))
for i in range(N12):
    P12[i, i ^ 1] = 1
Mc = 11 * np.eye(N12) + P12 - np.ones((N12, N12))
Mcp = np.linalg.pinv(Mc)


def GD(S):
    W = np.zeros((N12, n))
    for y in range(n):
        W[0, y] += 1
        W[1, y] -= 1
        W[2:, y] += 4 * S[:, y]
        W[2 + y, y] += 1
        W[2 + (y ^ 1), y] -= 1
    return (11 * I - J + Ppi - W.T @ Mcp @ W) / 4


def rand_sigma(rng):
    while True:
        perms, used = [], set()
        ok = True
        for _ in range(4):
            for _t in range(500):
                p = list(range(n))
                rng.shuffle(p)
                if all((i, p[i]) not in used for i in range(n)):
                    break
            else:
                ok = False
                break
            perms.append(p)
            used |= {(i, p[i]) for i in range(n)}
        if ok:
            S = np.zeros((n, n))
            for k, p in enumerate(perms):
                for i in range(n):
                    S[i, p[i]] = 1 if k < 2 else -1
            return S


rng = random.Random(3)
mins, ranks = [], []
for t in range(3000):
    S = rand_sigma(rng)
    ev = np.linalg.eigvalsh(GD(S))
    mins.append(ev.min())
    ranks.append(int((np.abs(ev) > 1e-8).sum()))
mins = np.array(mins)
print('min eigenvalue of G_D over 3000 random Sigma: max %.4f, median %.4f, min %.4f' % (mins.max(), np.median(mins), mins.min()))
print('fraction PSD (min eig >= -1e-9):', (mins >= -1e-9).mean(), ' ranks seen:', sorted(set(ranks)))
S = rand_sigma(rng)
print('check G_D 1 = 0:', np.abs(GD(S) @ np.ones(n)).max())
