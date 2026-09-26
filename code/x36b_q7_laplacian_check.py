"""Exact check: for the cubic graph G(L_c) (36 vertices) with the fixed-point-free involution theta,
(1) det(odd Laplacian L^-) = 4^6 * det(Q_c) exactly (Q_c = P_tau - P_eta - 2P_pi - I), hence det Q_c = det L^- mod squares;
(2) tau(G) = tau(H) * det(L^-) / 2, H = G/theta (Kirchhoff for a double cover), exact integers."""
import random
from fractions import Fraction
def det_int(M):
    # Bareiss fraction-free
    M = [r[:] for r in M]; n = len(M); sign = 1; prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if sw is None: return 0
            M[k], M[sw] = M[sw], M[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]
def rand_fpf_inv(pts):
    pts = pts[:]; random.shuffle(pts); f = {}
    for i in range(0, len(pts), 2): f[pts[i]] = pts[i + 1]; f[pts[i + 1]] = pts[i]
    return f
X = [(d, s) for d in range(6) for s in (1, -1)]
pi = {(d, s): (d, -s) for (d, s) in X}
ok1 = ok2 = 0; T = 300
random.seed(7)
for t in range(T):
    tau = rand_fpf_inv(X); eta = rand_fpf_inv(X)
    h = {w: pi[eta[w]] for w in X}; tau_m = {w: pi[tau[pi[w]]] for w in X}
    V = [('X', w) for w in X] + [('U', w) for w in X] + [('Ub', w) for w in X]
    idx = {v: i for i, v in enumerate(V)}; n = 36
    A = [[0] * n for _ in range(n)]
    def e(a, b): A[idx[a]][idx[b]] += 1; A[idx[b]][idx[a]] += 1
    for w in X:
        if w < pi[w]: e(('X', w), ('X', pi[w]))
        if w < tau[w]: e(('U', w), ('U', tau[w]))
        if w < tau_m[w]: e(('Ub', w), ('Ub', tau_m[w]))
        e(('X', w), ('U', w)); e(('X', w), ('Ub', w)); e(('U', w), ('Ub', h[w]))
    th = {}
    for w in X:
        th[('X', w)] = ('X', pi[w]); th[('U', w)] = ('Ub', pi[w]); th[('Ub', w)] = ('U', pi[w])
    L = [[(sum(A[i]) if i == j else 0) - A[i][j] for j in range(n)] for i in range(n)]
    # odd basis: one rep per orbit
    reps = [('X', (d, 1)) for d in range(6)] + [('U', w) for w in X]
    Lm = [[L[idx[a]][idx[b]] - L[idx[a]][idx[th[b]]] for b in reps] for a in reps]
    Lp = [[L[idx[a]][idx[b]] + L[idx[a]][idx[th[b]]] for b in reps] for a in reps]  # quotient Laplacian H
    Q = [[(tau[w] == v) - (eta[w] == v) - 2 * (pi[w] == v) - (w == v) for v in X] for w in X]
    dLm, dQ = det_int(Lm), det_int(Q)
    ok1 += ((dLm - 4 ** 6 * dQ) % 7 == 0)
    tauG = det_int([r[1:] for r in L[1:]])
    tauH = det_int([r[1:] for r in Lp[1:]])
    ok2 += (2 * tauG == tauH * dLm)
print('det L^- == 4^6 det Q (mod 7):', ok1, '/', T); print('2 tau(G) == tau(H) det L^- :', ok2, '/', T)
