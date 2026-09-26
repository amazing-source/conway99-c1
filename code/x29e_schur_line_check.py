# Exact mod-7 check of the Schur-complement formula of notes/102 sec. 8 for a line ball:
#   rank_7 Q = rank_7 Q_BB + rank_7 R_L,  R_L[w,w'] = Q_ww' - 6 + 1_{N_w}^T L_G^+ 1_{N_w'}  (w != w'),
#   R_L[w,w] = Q_ww - 6 + 1_{N_w}^T L_G^+ 1_{N_w},  Q = A - 3I + 3J,  L_G^+ = pseudo-inverse of 3I - M_T mod 7 on 1-perp.
# The ball (line T and N_1(T)) is built from random local data (C, tau_u, tau_ubar, sigma_U); the far part (60 vertices,
# their 6 shadow points, far-far adjacency) is RANDOM: the identity is pure linear algebra, it must hold regardless.
import random, itertools
import numpy as np
p = 7
def rank_mod(M, p=7):
    M = [list(map(lambda v: v % p, r)) for r in M]
    n, m = len(M), len(M[0]); r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] % p), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(v * inv) % p for v in M[r]]
        for i in range(n):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r
def inv_on_perp(Lm, p=7):
    """pseudo-inverse of symmetric L (n x n, kernel = constants, rank n-1 mod p): X with L X = I - J/n, X 1 = 0."""
    n = len(Lm)
    # solve L X = I - (1/n) J with sum-zero columns: augment with a row of ones
    ninv = pow(n % p, p - 2, p)
    rhs = [[((1 if i == j else 0) - ninv) % p for j in range(n)] for i in range(n)]
    A = [list(Lm[i]) + rhs[i] for i in range(n)] + [[1] * n + [0] * n]
    # gaussian elimination on augmented system
    rows = [[v % p for v in r] for r in A]; N = len(rows); r = 0; piv_cols = []
    for c in range(n):
        piv = next((i for i in range(r, N) if rows[i][c]), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], p - 2, p); rows[r] = [(v * inv) % p for v in rows[r]]
        for i in range(N):
            if i != r and rows[i][c]:
                f = rows[i][c]; rows[i] = [(a - f * b) % p for a, b in zip(rows[i], rows[r])]
        piv_cols.append(c); r += 1
    assert r == n, 'L not of rank n-1 with constant kernel (d(L) > 1)'
    X = [[0] * n for _ in range(n)]
    for i, c in enumerate(piv_cols):
        X[c] = rows[i][n:]
    return X
rng = random.Random(3)
def trial():
    labs = list(range(12)); mate = {i: i ^ 1 for i in labs}          # classes {0,1},{2,3},...
    def rand_tau():
        while True:
            perm = labs[:]; rng.shuffle(perm)
            t = {}
            ok = True
            for i in range(0, 12, 2):
                a, b = perm[i], perm[i + 1]
                if mate[a] == b: ok = False; break
                t[a], t[b] = b, a
            if ok: return t
    tu, tub = rand_tau(), rand_tau()
    sig = labs[:]
    while True:
        rng.shuffle(sig)
        if all(sig[v] != v for v in labs): break
    # ball: T = {x,y,z} = 0,1,2 ; N1: layer x = 3..14 (labels), layer y = 15..26 (u-pairs), layer z = 27..38 (ubar-pairs)
    nB = 39; B = np.zeros((nB, nB), dtype=int)
    X = lambda v: 3 + v; Y = lambda v: 15 + v; Z = lambda v: 27 + v
    for a, b in ((0, 1), (0, 2), (1, 2)): B[a, b] = B[b, a] = 1
    for v in labs:
        B[0, X(v)] = B[X(v), 0] = 1; B[1, Y(v)] = B[Y(v), 1] = 1; B[2, Z(v)] = B[Z(v), 2] = 1
        B[X(v), X(mate[v])] = 1; B[Y(v), Y(tu[v])] = 1; B[Z(v), Z(tub[v])] = 1
        B[X(v), Y(v)] = B[Y(v), X(v)] = 1; B[X(v), Z(v)] = B[Z(v), X(v)] = 1
        B[Y(v), Z(sig[v])] = B[Z(sig[v]), Y(v)] = 1
    M = B[3:, 3:]
    assert (M.sum(1) == 3).all()
    LG = (3 * np.eye(36, dtype=int) - M) % p
    try:
        Lp = np.array(inv_on_perp(LG.tolist()))
    except AssertionError:
        return None
    # random far part: 60 far vertices, each with 2 random shadow points per layer, random symmetric far adjacency
    nF = 60
    N = np.zeros((36, nF), dtype=int)
    for w in range(nF):
        for base in (0, 12, 24):
            for v in rng.sample(range(12), 2): N[base + v, w] = 1
    AF = np.zeros((nF, nF), dtype=int)
    for i in range(nF):
        for j in range(i + 1, nF):
            if rng.random() < 0.13: AF[i, j] = AF[j, i] = 1
    n = nB + nF
    A = np.zeros((n, n), dtype=int); A[:nB, :nB] = B; A[3:nB, nB:] = N; A[nB:, 3:nB] = N.T; A[nB:, nB:] = AF
    Q = (A - 3 * np.eye(n, dtype=int) + 3) % p
    rQ, rB = rank_mod(Q.tolist()), rank_mod(Q[:nB, :nB].tolist())
    G = (N.T @ Lp @ N) % p
    R = (Q[nB:, nB:] - 6 + G) % p
    rR = rank_mod(R.tolist())
    return rQ, rB, rR
done = 0
for t in range(40):
    res = trial()
    if res is None: continue
    rQ, rB, rR = res
    print(f'rank Q = {rQ}, rank Q_BB = {rB}, rank R_formula = {rR}, rank Q_BB + rank R = {rB + rR}', 'OK' if rQ == rB + rR else 'MISMATCH')
    done += 1
    if done >= 6: break
