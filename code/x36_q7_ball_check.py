"""Exact check (F_7) of the hand-derived odd-ball formula for a theta-invariant block line L_c.
Claim 1: rank_7(odd ball matrix of A-3I, 19 orbits) = 6 + rank_7(Q), Q = P_tau - P_eta - 2 P_pi - I (12x12).
Claim 2: if Q is nonsingular, chi_7(disc of nondegenerate part of the odd ball matrix) = chi_7(det Q).
Claim 3: z = 3(e_u - e_ubar) + 1_U - 1_Ubar lies in the kernel of the odd ball matrix.
Abstract balls: tau, eta random fixed-point-free involutions on X (12 pts, 6 blocks), h = pi*eta."""
import random, itertools
P = 7
def rank_mod(M, p=P):
    M = [[x % p for x in r] for r in M]; n = len(M); m = len(M[0]) if n else 0; r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c]), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]; inv = pow(M[r][c], p - 2, p)
        M[r] = [x * inv % p for x in M[r]]
        for i in range(n):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r
def det_mod(M, p=P):
    M = [[x % p for x in r] for r in M]; n = len(M); d = 1
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c]), None)
        if piv is None: return 0
        if piv != c: M[c], M[piv] = M[piv], M[c]; d = -d
        d = d * M[c][c] % p; inv = pow(M[c][c], p - 2, p)
        for i in range(c + 1, n):
            f = M[i][c] * inv % p
            if f: M[i] = [(a - f * b) % p for a, b in zip(M[i], M[c])]
    return d % p
def chi(a, p=P):
    a %= p
    return 0 if a == 0 else (1 if pow(a, (p - 1) // 2, p) == 1 else -1)
def kernel_mod(M, p=P):
    n = len(M[0]); A = [[x % p for x in r] for r in M]; piv = []; r = 0
    for c in range(n):
        pr = next((i for i in range(r, len(A)) if A[i][c]), None)
        if pr is None: continue
        A[r], A[pr] = A[pr], A[r]; inv = pow(A[r][c], p - 2, p); A[r] = [x * inv % p for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]; A[i] = [(a - f * b) % p for a, b in zip(A[i], A[r])]
        piv.append(c); r += 1
    free = [c for c in range(n) if c not in piv]; K = []
    for fc in free:
        v = [0] * n; v[fc] = 1
        for i, pc in enumerate(piv): v[pc] = (-A[i][fc]) % p
        K.append(v)
    return K
def nondeg_disc(M, p=P):
    n = len(M); K = kernel_mod(M, p); r = n - len(K)
    # complement of ker: coordinates outside the pivot columns of RREF(K)
    kp = []
    if K:
        B = [row[:] for row in K]; rr = 0
        for c in range(n):
            pr = next((i for i in range(rr, len(B)) if B[i][c]), None)
            if pr is None: continue
            B[rr], B[pr] = B[pr], B[rr]; inv = pow(B[rr][c], p - 2, p); B[rr] = [x * inv % p for x in B[rr]]
            for i in range(len(B)):
                if i != rr and B[i][c]:
                    f = B[i][c]; B[i] = [(a - f * b) % p for a, b in zip(B[i], B[rr])]
            kp.append(c); rr += 1
    I = [i for i in range(n) if i not in kp]
    assert len(I) == r
    d = det_mod([[M[a][b] for b in I] for a in I], p); assert d != 0
    return r, d
def rand_fpf_inv(pts):
    pts = pts[:]; random.shuffle(pts); f = {}
    for i in range(0, len(pts), 2): f[pts[i]] = pts[i + 1]; f[pts[i + 1]] = pts[i]
    return f
X = [(d, s) for d in range(6) for s in (1, -1)]
pi = {(d, s): (d, -s) for (d, s) in X}
def trial():
    tau = rand_fpf_inv(X); eta = rand_fpf_inv(X)
    h = {w: pi[eta[w]] for w in X}           # eta = pi o h
    tau_m = {w: pi[tau[pi[w]]] for w in X}   # tau at c- = pi tau pi
    V = ['x', 'u', 'ub'] + [('X', w) for w in X] + [('U', w) for w in X] + [('Ub', w) for w in X]
    idx = {v: i for i, v in enumerate(V)}; n = len(V)
    A = [[0] * n for _ in range(n)]
    def e(a, b): A[idx[a]][idx[b]] = A[idx[b]][idx[a]] = 1
    e('x', 'u'); e('x', 'ub'); e('u', 'ub')
    for w in X:
        e('x', ('X', w)); e('u', ('U', w)); e('ub', ('Ub', w))
        e(('X', w), ('X', pi[w])); e(('U', w), ('U', tau[w])); e(('Ub', w), ('Ub', tau_m[w]))
        e(('X', w), ('U', w)); e(('X', w), ('Ub', w)); e(('U', w), ('Ub', h[w]))
    th = {'x': 'x', 'u': 'ub', 'ub': 'u'}
    for w in X:
        th[('X', w)] = ('X', pi[w]); th[('U', w)] = ('Ub', pi[w]); th[('Ub', w)] = ('U', pi[w])
    for a in V:
        for b in V:
            assert A[idx[a]][idx[b]] == A[idx[th[a]]][idx[th[b]]], 'theta not an automorphism'
    reps = ['u'] + [('X', (d, 1)) for d in range(6)] + [('U', w) for w in X]
    N = [[A[idx[a]][idx[b]] - A[idx[a]][idx[th[b]]] - 3 * (a == b) for b in reps] for a in reps]
    Q = [[(tau[w] == v) - (eta[w] == v) - 2 * (pi[w] == v) - (w == v) for v in X] for w in X]
    rN, rQ = rank_mod(N), rank_mod(Q)
    z = [3] + [0] * 6 + [1] * 12
    kz = all(sum(N[i][j] * z[j] for j in range(19)) % P == 0 for i in range(19))
    res = {'rN': rN, 'rQ': rQ, 'claim1': rN == 6 + rQ, 'claim3': kz}
    if rQ == 12:
        r, d = nondeg_disc(N)
        res['claim2'] = chi(d) == chi(det_mod(Q)); res['chiQ'] = chi(det_mod(Q))
    return res
random.seed(1)
stats = {'n': 0, 'c1': 0, 'c3': 0, 'c2n': 0, 'c2': 0, 'chi+': 0, 'chi-': 0}
ranks = {}
for t in range(3000):
    r = trial(); stats['n'] += 1; stats['c1'] += r['claim1']; stats['c3'] += r['claim3']
    ranks[r['rN']] = ranks.get(r['rN'], 0) + 1
    if 'claim2' in r:
        stats['c2n'] += 1; stats['c2'] += r['claim2']; stats['chi+' if r['chiQ'] == 1 else 'chi-'] += 1
print(stats); print('odd ball ranks:', dict(sorted(ranks.items())))
