# J2 probe: star(0) structures (Q0, Pi0) on the 12 labels of star(0) (0-reps e0 + s e_x, x=1..6; x=1 = Z labels, h=0).
# Star Gram A0 = 11I + S - J + 4(Pi - Q) (0-reps) is always PSD of rank 11 (kernel = 1).
# a-test: F = sum a_L f_L has |F|^2 = 28|a|^2 = 672 and <F, f_L> = 28 a_L, so 784 a0^T A0^+ a0 <= 672.
import numpy as np, random, itertools
rng = random.Random(1)
labs = [(x, s) for x in range(1, 7) for s in (1, -1)]      # index 0,1 = Z (x=1)
S = np.zeros((12, 12))
for i, (x, s) in enumerate(labs):
    for j, (y, t) in enumerate(labs):
        if x == y and s != t: S[i, j] = 1
def rand_inv():
    p = list(range(12)); rng.shuffle(p)
    inv = [0] * 12
    for k in range(0, 12, 2): inv[p[k]] = p[k + 1]; inv[p[k + 1]] = p[k]
    return inv
def A0(Q, P):
    T = np.zeros((12, 12))
    for i in range(12):
        T[i, Q[i]] += 1; T[i, P[i]] -= 1
    return 11 * np.eye(12) + S - np.ones((12, 12)) - 4 * T, T
# alpha patterns: cells x=2..6; choose pattern with k S-cells ++, k S-cells --, rest X
def alpha_pattern(kind):
    a = np.zeros(12)
    for c, typ in enumerate(kind):
        x = c + 2
        i, j = labs.index((x, 1)), labs.index((x, -1))
        if typ == '++': a[i] = a[j] = 1
        elif typ == '--': a[i] = a[j] = -1
        else: a[i] = 1; a[j] = -1
    return a
for kind in [('X',) * 5, ('++', '--', 'X', 'X', 'X'), ('++', '++', '--', '--', 'X')]:
    a = alpha_pattern(kind)
    vals = []; ok = 0; N = 20000
    for _ in range(N):
        Q, P = rand_inv(), rand_inv()
        A, T = A0(Q, P)
        w, V = np.linalg.eigh(A)
        keep = w > 1e-9
        Ap = (V[:, keep] / w[keep]) @ V[:, keep].T
        q = a @ Ap @ a
        vals.append(q)
        if q <= 6 / 7 + 1e-9: ok += 1
    vals = np.array(vals)
    print(kind, 'a-test pass %d/%d  min %.3f  median %.3f' % (ok, N, vals.min(), np.median(vals)))
