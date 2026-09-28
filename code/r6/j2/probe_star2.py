# Same probe, but restricted to star(0) structures obeying the exact J2 profile rules (hand-derived, notes/151 s2ter):
#  for a cut label L with z = #Z among {Q0 L, Pi0 L} and s0 = alpha_L (alpha_Q - alpha_Pi):
#   z=2 -> P_sigma ; z=1 -> s0 = -1 (P0 or P_sigma) or s0 = +1 (P_sigma) ; z=0 -> s0 in {0,-2} (either) or +2 (P_sigma)
#   forced-P_sigma labels: at most 2 per alpha sign.
#  Z labels: the h-sum of z's star(0) cut partners must be compensated by star(1) (|.| <= 2 - #Z-partners) -> always ok here.
import numpy as np, random
rng = random.Random(2)
labs = [(x, s) for x in range(1, 7) for s in (1, -1)]
S = np.zeros((12, 12))
for i, (x, s) in enumerate(labs):
    for j, (y, t) in enumerate(labs):
        if x == y and s != t: S[i, j] = 1
def rand_inv():
    p = list(range(12)); rng.shuffle(p); inv = [0] * 12
    for k in range(0, 12, 2): inv[p[k]] = p[k + 1]; inv[p[k + 1]] = p[k]
    return inv
def alpha_pattern(kind):
    a = np.zeros(12)
    for c, typ in enumerate(kind):
        x = c + 2; i, j = labs.index((x, 1)), labs.index((x, -1))
        if typ == '++': a[i] = a[j] = 1
        elif typ == '--': a[i] = a[j] = -1
        else: a[i] = 1; a[j] = -1
    return a
def profile_ok(Q, P, a):
    forced = {1: 0, -1: 0}
    for L in range(2, 12):
        zc = (Q[L] < 2) + (P[L] < 2)
        s0 = a[L] * (a[Q[L]] - a[P[L]]) if Q[L] != P[L] else 0
        if zc == 2: forced[a[L]] += 1
        elif zc == 1:
            if s0 == 1: forced[a[L]] += 1
        else:
            if s0 == 2: forced[a[L]] += 1
    return forced[1] <= 2 and forced[-1] <= 2
for kind in [('X',) * 5, ('++', '--', 'X', 'X', 'X'), ('++', '++', '--', '--', 'X')]:
    a = alpha_pattern(kind)
    n = ok = okp = 0
    while n < 20000:
        Q, P = rand_inv(), rand_inv(); n += 1
        if not profile_ok(Q, P, a): continue
        okp += 1
        T = np.zeros((12, 12))
        for i in range(12): T[i, Q[i]] += 1; T[i, P[i]] -= 1
        A = 11 * np.eye(12) + S - np.ones((12, 12)) - 4 * T
        w, V = np.linalg.eigh(A); keep = w > 1e-9
        q = a @ ((V[:, keep] / w[keep]) @ V[:, keep].T) @ a
        if q <= 6 / 7 + 1e-9: ok += 1
    print(kind, 'profile ok %d/%d, then a-test %d' % (okp, n, ok))
